import subprocess
import os
import sys
from io import BytesIO
import time

from PIL import Image
import cv2
import numpy as np

# Subprocesses were making windows and this supresses them
if sys.platform == "win32":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE


def getResourcePath(relative_path):
    try:
        # Using the --onefile param to compile so the pyinstaller makes a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class E7Item:
    def __init__(self, image=None, price=0, count=0):
        self.image = image
        self.price = price
        self.count = count

    def __repr__(self):
        return f"ShopItem(image={self.image}, price={self.price}, count={self.count})"


class E7Inventory:
    def __init__(self):
        self.inventory = dict()

    def addItem(self, path: str, name="", price=0, count=0):
        image_path = getResourcePath(os.path.join("adb-assets", path))
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not load image at: {image_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        newItem = E7Item(image, price, count)
        self.inventory[name] = newItem

    def getStatusString(self):
        status_string = ""
        for key, value in self.inventory.items():
            status_string += key[0:4] + ": " + str(value.count) + " "
        return status_string

    def getName(self):
        res = []
        for key in self.inventory.keys():
            res.append(key)
        return res

    def getCount(self):
        res = []
        for value in self.inventory.values():
            res.append(value.count)
        return res

    def getTotalCost(self):
        sum = 0
        for value in self.inventory.values():
            sum += value.price * value.count
        return sum


class E7ADBShopRefresh:
    def __init__(self, tap_sleep: float = 0.5, budget=None, ip_port=None, debug=False):
        self.observerCallbacks = []
        self.onCompletionCallback = None
        self.loop_active = False
        self.end_of_refresh = True
        self.tap_sleep = tap_sleep
        self.budget = budget
        self.ip_port = ip_port
        self.device_args = [] if ip_port is None else ["-s", ip_port]
        self.refresh_count = 0

        self.adb_path = getResourcePath(
            os.path.join("adb-assets", "platform-tools", "adb.exe")
        )
        # if the first fails try again but with no .exe externsion
        if not os.path.exists(self.adb_path):
            self.adb_path = getResourcePath(
                os.path.join("adb-assets", "platform-tools", "adb")
            )

        if not os.path.exists(self.adb_path):
            raise FileNotFoundError(f"ADB executable not found at: {self.adb_path}")

        self.storage = E7Inventory()
        self.screenwidth = 1920
        self.screenheight = 1080
        self.updateScreenDimension()

        self.storage.addItem("cov.jpg", "Covenant bookmark", 184000)
        self.storage.addItem("mys.jpg", "Mystic medal", 280000)
        if debug:
            self.storage.addItem("fb.jpg", "Friendship bookmark", 18000)

    def setOnCompletionCallback(self, callback):
        self.onCompletionCallback = callback

    def attachOnComplete(self, callback):
        self.onCompletionCallback = callback

    def notifyComplete(self):
        if self.onCompletionCallback:
            self.onCompletionCallback()

    def notifyObservers(self):
        data = {key: value.count for key, value in self.storage.inventory.items()}
        data["Refresh Count"] = self.refresh_count

        for callback in self.observerCallbacks:
            callback(data)

    def attachObserver(self, callback):
        self.observerCallbacks.append(callback)

    def start(self):
        self.loop_active = True
        self.end_of_refresh = False
        self.refreshShop()

    def refreshShop(self):
        self.clickShop()
        # time needed for item to drop in after refresh (0.8)
        sliding_time = 1
        # stat track
        milestone = self.budget // 10
        # swipe location
        x1 = str(0.6250 * self.screenwidth)
        y1 = str(0.7481 * self.screenheight)
        y2 = str(0.3629 * self.screenheight)
        # refresh loop
        while self.loop_active:

            time.sleep(sliding_time)
            brought = set()

            if not self.loop_active:
                break
            # look at shop (page 1)
            screenshot = self.takeScreenshot()
            for key, value in self.storage.inventory.items():
                pos = self.findItemPosition(screenshot, value.image)
                if pos is not None:
                    self.clickBuy(pos)
                    value.count += 1
                    brought.add(key)
                    self.notifyObservers()

            if not self.loop_active:
                break
            # swipe
            try:
                adb_process = subprocess.run(
                    [self.adb_path]
                    + self.device_args
                    + ["shell", "input", "swipe", x1, y1, x1, y2],
                    check=True,
                    startupinfo=startupinfo,
                )
            except subprocess.CalledProcessError as e:
                print(f"ADB command failed: {e}")
                break
            # wait for action to complete
            time.sleep(0.75)

            if not self.loop_active:
                break
            # look at shop (page 2)
            screenshot = self.takeScreenshot()
            for key, value in self.storage.inventory.items():
                pos = self.findItemPosition(screenshot, value.image)
                if pos is not None and key not in brought:
                    self.clickBuy(pos)
                    value.count += 1
                    self.notifyObservers()

            if not self.loop_active:
                break
            if self.budget:
                if self.refresh_count >= self.budget // 3:
                    break

            self.clickRefresh()
            self.refresh_count += 1

            self.notifyObservers()

        self.end_of_refresh = True
        self.loop_active = False
        self.notifyComplete()

    def updateScreenDimension(self):
        try:
            adb_process = subprocess.run(
                [self.adb_path] + self.device_args + ["exec-out", "screencap", "-p"],
                stdout=subprocess.PIPE,
                check=True,
                startupinfo=startupinfo,
            )
            byte_image = BytesIO(adb_process.stdout)
            pil_image = Image.open(byte_image)
            pil_image = np.array(pil_image)
            y, x, _ = pil_image.shape
            self.screenwidth = x
            self.screenheight = y
        except subprocess.CalledProcessError as e:
            print(f"Failed to get screen dimensions: {e}")

    def takeScreenshot(self):
        adb_process = subprocess.run(
            [self.adb_path] + self.device_args + ["exec-out", "screencap", "-p"],
            stdout=subprocess.PIPE,
            startupinfo=startupinfo,
        )
        byte_image = BytesIO(adb_process.stdout)
        pil_image = Image.open(byte_image)
        pil_image = np.array(pil_image)
        screenshot = cv2.cvtColor(pil_image, cv2.COLOR_BGR2GRAY)
        return screenshot

    def findItemPosition(self, screen_image, item_image):
        result = cv2.matchTemplate(screen_image, item_image, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.75)

        if loc[0].size > 0:
            x = loc[1][0] + self.screenwidth * 0.4718
            y = loc[0][0] + self.screenheight * 0.1000
            pos = (x, y)
            return pos
        return None

    # macro
    def clickShop(self):
        # newshop
        x = self.screenwidth * 0.0411
        y = self.screenheight * 0.3835
        adb_process = subprocess.run(
            [self.adb_path]
            + self.device_args
            + ["shell", "input", "tap", str(x), str(y)],
            startupinfo=startupinfo,
        )
        time.sleep(self.tap_sleep)

        # oldshop
        x = self.screenwidth * 0.4406
        y = self.screenheight * 0.2462
        adb_process = subprocess.run(
            [self.adb_path]
            + self.device_args
            + ["shell", "input", "tap", str(x), str(y)],
            startupinfo=startupinfo,
        )
        time.sleep(self.tap_sleep)

        # newshop
        x = self.screenwidth * 0.0411
        y = self.screenheight * 0.3835
        adb_process = subprocess.run(
            [self.adb_path]
            + self.device_args
            + ["shell", "input", "tap", str(x), str(y)],
            startupinfo=startupinfo,
        )
        time.sleep(self.tap_sleep)

    def clickBuy(self, pos):
        if pos is None:
            return False

        x, y = pos
        adb_process = subprocess.run(
            [self.adb_path]
            + self.device_args
            + ["shell", "input", "tap", str(x), str(y)],
            startupinfo=startupinfo,
        )
        time.sleep(self.tap_sleep)

        # confirm
        x = self.screenwidth * 0.5677
        y = self.screenheight * 0.7037
        adb_process = subprocess.run(
            [self.adb_path]
            + self.device_args
            + ["shell", "input", "tap", str(x), str(y)],
            startupinfo=startupinfo,
        )
        time.sleep(self.tap_sleep)
        time.sleep(0.5)

    def clickRefresh(self):
        x = self.screenwidth * 0.1698
        y = self.screenheight * 0.9138
        adb_process = subprocess.run(
            [self.adb_path]
            + self.device_args
            + ["shell", "input", "tap", str(x), str(y)],
            startupinfo=startupinfo,
        )
        time.sleep(self.tap_sleep)

        if not self.loop_active:
            return
        # confirm
        x = self.screenwidth * 0.5828
        y = self.screenheight * 0.6411
        adb_process = subprocess.run(
            [self.adb_path]
            + self.device_args
            + ["shell", "input", "tap", str(x), str(y)],
            startupinfo=startupinfo,
        )
        time.sleep(self.tap_sleep)
