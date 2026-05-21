import subprocess
import sys
from io import BytesIO

from PIL import Image
import cv2
import numpy as np
import easyocr

if sys.platform == "win32":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE


class CurrencyService:
    def __init__(self, device_id=None):
        self.adb_path = "adb"
        self.device_args = [] if device_id is None else ["-s", device_id]
        self.reader = easyocr.Reader(["en"], gpu=False)

    def takeScreenshot(self):
        result = subprocess.run(
            [self.adb_path] + self.device_args + ["exec-out", "screencap", "-p"],
            stdout=subprocess.PIPE,
            startupinfo=startupinfo,
        )
        pil_image = Image.open(BytesIO(result.stdout))
        arr = np.array(pil_image)
        image = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        return image, arr.shape[1], arr.shape[0]

    def extractCurrencies(self):
        image, screenwidth, screenheight = self.takeScreenshot()

        x = int(0.40 * screenwidth)
        y = int(0.00 * screenheight)
        w = int(0.40 * screenwidth)
        h = int(0.07 * screenheight)
        cropped = image[y : y + h, x : x + w]

        cropped = cv2.resize(cropped, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        _, cropped = cv2.threshold(cropped, 150, 255, cv2.THRESH_BINARY)

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
