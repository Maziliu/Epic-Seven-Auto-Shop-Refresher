from dataclasses import dataclass
import time
from typing import Optional, Tuple
from Xlib import X, display
from Xlib.ext import xtest
import cv2
import numpy as np
from PIL import Image

DEFAULT_MATCH_THRESHOLD: float = 0.85
DEFAULT_CLICK_HOLD_DELAY: float = 0.2

_cachedDisplay: Optional[display.Display] = None
_templateCache: dict[str, np.ndarray] = {}

@dataclass
class WindowGeometry:
    x: int
    y: int
    width: int
    height: int

def getDisplay() -> display.Display:
    global _cachedDisplay
    if _cachedDisplay is None:
        _cachedDisplay = display.Display()
    return _cachedDisplay

def getWindowGeometry(windowId: int, d: Optional[display.Display] = None) -> WindowGeometry:
    d = d or getDisplay()
    window = d.create_resource_object("window", windowId)
    geometry = window.get_geometry()
    return WindowGeometry(
        x=geometry.x,
        y=geometry.y,
        width=geometry.width,
        height=geometry.height,
    )

def takeScreenshot(windowId: int, d: Optional[display.Display] = None) -> np.ndarray:
    d = d or getDisplay()
    window = d.create_resource_object("window", windowId)
    geometry = window.get_geometry()

    rawImageBytes = window.get_image(
        0, 0, geometry.width, geometry.height, X.ZPixmap, 0xFFFFFFFF
    )
    img = Image.frombytes(
        "RGB",
        (geometry.width, geometry.height),
        rawImageBytes.data,
        "raw",
        "BGRX",
    )
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def loadTemplateImage(referenceImagePath: str) -> np.ndarray:
    if referenceImagePath not in _templateCache:
        referenceImage = cv2.imread(referenceImagePath)
        if referenceImage is None:
            raise FileNotFoundError(f"Asset {referenceImagePath} does not exist")
        _templateCache[referenceImagePath] = referenceImage
    return _templateCache[referenceImagePath]

def findClickPosition(
    screenshot: np.ndarray,
    referenceImagePath: str,
    matchThreshold: float = DEFAULT_MATCH_THRESHOLD,
) -> Optional[Tuple[int, int]]:
    referenceImage = loadTemplateImage(referenceImagePath)

    if (
        screenshot.shape[0] < referenceImage.shape[0]
        or screenshot.shape[1] < referenceImage.shape[1]
    ):
        return None

    match = cv2.matchTemplate(screenshot, referenceImage, cv2.TM_CCOEFF_NORMED)
    _, maxMatchValue, _, maxLoc = cv2.minMaxLoc(match)

    if maxMatchValue < matchThreshold:
        return None

    height, width = referenceImage.shape[:2]
    return (maxLoc[0] + width // 2, maxLoc[1] + height // 2)

def click(
    windowId: int,
    x: int | float,
    y: int | float,
    button: int = 1,
    holdDelay: float = DEFAULT_CLICK_HOLD_DELAY,
    restoreCursor: bool = True,
    d: Optional[display.Display] = None,
) -> None:
    d = d or getDisplay()
    root = d.screen().root
    window = d.create_resource_object("window", windowId)

    coords = root.translate_coords(window, int(round(x)), int(round(y)))
    rootX = coords.x
    rootY = coords.y

    origPointer = root.query_pointer()
    origX, origY = origPointer.root_x, origPointer.root_y

    xtest.fake_input(d, X.MotionNotify, x=rootX, y=rootY)
    xtest.fake_input(d, X.ButtonPress, detail=button)
    d.sync()

    if holdDelay > 0:
        time.sleep(holdDelay)

    xtest.fake_input(d, X.ButtonRelease, detail=button)
    if restoreCursor:
        xtest.fake_input(d, X.MotionNotify, x=origX, y=origY)
    d.sync()

def scroll(
    windowId: int,
    x: int | float,
    y: int | float,
    clicks: int = 5,
    direction: str = "down",
    delay: float = 0.01,
    restoreCursor: bool = True,
    d: Optional[display.Display] = None,
) -> None:
    button = 5 if direction.lower() == "down" else 4
    for _ in range(clicks):
        click(windowId, x, y, button=button, holdDelay=0, restoreCursor=restoreCursor, d=d)
        if delay > 0:
            time.sleep(delay)

def drag(
    windowId: int,
    startX: int | float,
    startY: int | float,
    endX: int | float,
    endY: int | float,
    steps: int = 10,
    stepDelay: float = 0.01,
    restoreCursor: bool = True,
    d: Optional[display.Display] = None,
) -> None:
    d = d or getDisplay()
    root = d.screen().root
    window = d.create_resource_object("window", windowId)

    origPointer = root.query_pointer()
    origX, origY = origPointer.root_x, origPointer.root_y

    startCoords = root.translate_coords(window, int(round(startX)), int(round(startY)))
    endCoords = root.translate_coords(window, int(round(endX)), int(round(endY)))

    xtest.fake_input(d, X.MotionNotify, x=startCoords.x, y=startCoords.y)
    xtest.fake_input(d, X.ButtonPress, detail=1)
    d.sync()

    for i in range(1, steps + 1):
        currentX = int(round(startCoords.x + (endCoords.x - startCoords.x) * (i / steps)))
        currentY = int(round(startCoords.y + (endCoords.y - startCoords.y) * (i / steps)))
        xtest.fake_input(d, X.MotionNotify, x=currentX, y=currentY)
        d.sync()
        if stepDelay > 0:
            time.sleep(stepDelay)

    xtest.fake_input(d, X.ButtonRelease, detail=1)
    if restoreCursor:
        xtest.fake_input(d, X.MotionNotify, x=origX, y=origY)
    d.sync()


def findGameWindows(targetNames: Optional[list[str]] = None) -> list[Tuple[int, str]]:
    if targetNames is None:
        targetNames = ["Epic Seven", "Wine Desktop"]
    d = getDisplay()
    root = d.screen().root
    results = []
    for window in root.query_tree().children:
        try:
            name = window.get_wm_name()
            if name and any(t.lower() in name.lower() for t in targetNames):
                results.append((window.id, name))
        except Exception:
            pass
    return results
