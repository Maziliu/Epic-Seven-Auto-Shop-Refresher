from typing import Optional, Tuple
from PIL import Image
import cv2
import easyocr
import numpy as np
import torch
from X11Utilities import takeScreenshot


class CurrencyService:
    def __init__(self, windowId: int):
        self.windowId = windowId
        self.reader = easyocr.Reader(["en"], gpu=torch.cuda.is_available())

    def extractCurrencies(self) -> Optional[Tuple[int, int]]:
        screenshot = takeScreenshot(self.windowId)
        screenheight, screenwidth = screenshot.shape[:2]

        x = int(0.55 * screenwidth)
        y = int(0.02 * screenheight)
        w = int(0.21 * screenwidth)
        h = int(0.08 * screenheight)
        cropped = screenshot[y : y + h, x : x + w]

        results = self.reader.readtext(cropped, allowlist="0123456789,", detail=1)

        valid = []
        for bbox, text, conf in results:
            cleaned = text.strip().replace(",", "")
            if cleaned.isdigit():
                x_pos = bbox[0][0]
                valid.append((x_pos, int(cleaned), text, conf))

        if len(valid) < 2:
            return None

        valid.sort(key=lambda item: item[0])
        gold = valid[0][1]
        skystones = valid[1][1]
        return gold, skystones
