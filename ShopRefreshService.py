from E7ADBShopRefresh import E7ADBShopRefresh
from typing import Callable
import threading


class ShopRefreshService:
    def __init__(self):
        self.e7ADBShopRefresh = None
        self.onServiceCompletionCallback: Callable[[None], None] = None
        self.observerCallbacks: list[Callable[[dict], None]] = []

    def setOnServiceCompletionCallback(self, callback: Callable[[None], None]) -> None:
        self.onServiceCompletionCallback = callback

    def onServiceCompletion(self):
        if self.onServiceCompletionCallback:
            self.onServiceCompletionCallback()

    def start(self, skystoneAmount: int) -> None:
        self.e7ADBShopRefresh = E7ADBShopRefresh(budget=skystoneAmount)
        self.e7ADBShopRefresh.attachObserver(self.onShopRefresh)
        self.e7ADBShopRefresh.attachOnComplete(self.onServiceCompletion)
        shopRefreshProcess = threading.Thread(
            target=self.e7ADBShopRefresh.start, daemon=True
        )
        shopRefreshProcess.start()

    def stop(self) -> None:
        if self.e7ADBShopRefresh:
            self.e7ADBShopRefresh.end_of_refresh = True
            self.e7ADBShopRefresh.loop_active = False

    def attachObserver(self, callback: Callable[[dict], None]) -> None:
        self.observerCallbacks.append(callback)

    def notifyObservers(self, data: dict) -> None:
        for callback in self.observerCallbacks:
            callback(data)

    def onShopRefresh(self, data: dict) -> None:
        self.notifyObservers(data)
