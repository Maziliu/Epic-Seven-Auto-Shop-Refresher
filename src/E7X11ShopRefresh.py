import sys
import os
import time
from typing import Callable, Optional, Tuple
import numpy as np
import random

from EpicSeven import Inventory
from X11Utilities import (
    WindowGeometry,
    click,
    findClickPosition,
    getWindowGeometry,
    scroll,
    takeScreenshot,
)

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    ASSETS_DIRECTORY = os.path.join(sys._MEIPASS, "assets")
else:
    ASSETS_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

CONFIRM_BUTTON_X_RATIO: float = 0.58
CONFIRM_BUTTON_Y_RATIO: float = 0.65
CONFIRM_BUY_BUTTON_X_RATIO: float = 0.55
CONFIRM_BUY_BUTTON_Y_RATIO: float = 0.70
BUY_BUTTON_X_OFFSET_RATIO: float = 0.4318
BUY_BUTTON_Y_OFFSET_RATIO: float = 0.025
REFRESH_BUTTON_X_RATIO: float = 0.1625
REFRESH_BUTTON_Y_RATIO: float = 0.9148
BOTTOM_ITEM_SEARCH_START_Y_RATIO: float = 0.60

DEFAULT_ACTION_DELAY: float = 1

SKYSTONES_PER_REFRESH = 3

def delay(customDelayInSeconds: Optional[float] = None) -> None:
    if customDelayInSeconds:
        time.sleep(customDelayInSeconds)
    else:
        time.sleep(DEFAULT_ACTION_DELAY + random.randint(0, 100) / 1000)

class E7X11ShopRefresh:
    def __init__(self, windowId: int):
        self.windowId: int = windowId
        self.inventory: Inventory = Inventory()
        self.refreshCount: int = 0
        self.loopActive: bool = False
        self.observerCallbacks: list[Callable[[dict], None]] = []
        self.onCompletionCallbacks: list[Callable[[], None]] = []

    def attachObserver(self, callback: Callable[[dict], None]) -> None:
        self.observerCallbacks.append(callback)

    def attachOnComplete(self, callback: Callable[[], None]) -> None:
        self.onCompletionCallbacks.append(callback)

    def notifyObservers(self) -> None:
        data = {
            "Refresh Count": self.refreshCount,
            **self.inventory.getItems(),
        }
        for callback in self.observerCallbacks:
            callback(data)

    def notifyCompletion(self) -> None:
        for callback in self.onCompletionCallbacks:
            callback()

    def stop(self) -> None:
        self.loopActive = False

    def clickConfirmBuyItem(self) -> None:
        geometry: WindowGeometry = getWindowGeometry(self.windowId)
        confirmX = geometry.width * CONFIRM_BUY_BUTTON_X_RATIO
        confirmY = geometry.height * CONFIRM_BUY_BUTTON_Y_RATIO
        click(self.windowId, confirmX, confirmY)

    def clickConfirmRefresh(self) -> None:
        geometry: WindowGeometry = getWindowGeometry(self.windowId)
        confirmX = geometry.width * CONFIRM_BUTTON_X_RATIO
        confirmY = geometry.height * CONFIRM_BUTTON_Y_RATIO
        click(self.windowId, confirmX, confirmY)

    def buyItem(self, key: str, itemPosition: Tuple[int, int]) -> None:
        x, y = itemPosition
        geometry: WindowGeometry = getWindowGeometry(self.windowId)

        correctedX = x + geometry.width * BUY_BUTTON_X_OFFSET_RATIO
        correctedY = y + geometry.height * BUY_BUTTON_Y_OFFSET_RATIO

        click(self.windowId, correctedX, correctedY)
        delay(0.5)
        self.clickConfirmBuyItem()
        self.inventory.incrementItem(key)
        self.notifyObservers()

    def searchBuyItems(self, screenshot: np.ndarray, startYRatio: float = 0.0) -> None:
        height = screenshot.shape[0]
        startY = int(round(height * startYRatio))
        searchRegion = screenshot[startY:, :] if startY > 0 else screenshot

        for key in self.inventory.getKeys():
            imagePath = os.path.join(ASSETS_DIRECTORY, f"{key.lower()}.png")
            if not os.path.exists(imagePath):
                raise FileNotFoundError()

            itemPosition = findClickPosition(searchRegion, imagePath)
            # print(f"Checking {key}, Position: {itemPosition}")
            if itemPosition is None:
                continue

            adjustedPosition = (itemPosition[0], itemPosition[1] + startY)
            self.buyItem(key, adjustedPosition)
            delay()

    def refreshShop(self) -> None:
        geometry: WindowGeometry = getWindowGeometry(self.windowId)
        refreshX = geometry.width * REFRESH_BUTTON_X_RATIO
        refreshY = geometry.height * REFRESH_BUTTON_Y_RATIO

        click(self.windowId, refreshX, refreshY)
        delay(0.5)
        self.clickConfirmRefresh()
        self.refreshCount += 1
        self.notifyObservers()

    def scrollShop(self, clicks: int = 5) -> None:
        geometry: WindowGeometry = getWindowGeometry(self.windowId)
        centerX = geometry.width * 0.6
        centerY = geometry.height * 0.5
        scroll(self.windowId, centerX, centerY, clicks=clicks, direction="down")

    def performRefreshCycle(self) -> None:
        screenshotTop = takeScreenshot(self.windowId)
        self.searchBuyItems(screenshotTop)

        self.scrollShop()
        delay()

        screenshotBottom = takeScreenshot(self.windowId)
        self.searchBuyItems(screenshotBottom, startYRatio=BOTTOM_ITEM_SEARCH_START_Y_RATIO)

        delay()
        self.refreshShop()

    def start(self, skystones) -> None:
        self.loopActive = True
        cycles: int = skystones // SKYSTONES_PER_REFRESH

        while self.loopActive and cycles is not None and cycles > 0:
            self.performRefreshCycle()

            if self.refreshCount >= cycles:
                self.loopActive = False
                break

            delay()
        self.notifyCompletion()


if __name__ == "__main__":
    windowId = 18874377
    refresher = E7X11ShopRefresh(windowId)
    refresher.start(9492)

