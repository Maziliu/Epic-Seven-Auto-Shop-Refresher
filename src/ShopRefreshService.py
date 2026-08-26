from typing import Callable, Optional
import threading
from E7X11ShopRefresh import E7X11ShopRefresh


class ShopRefreshService:
    def __init__(self, windowId: int):
        self.windowId = windowId
        self.e7ShopRefresh: Optional[E7X11ShopRefresh] = None
        self.onServiceCompletionCallback: Optional[Callable[[], None]] = None
        self.observerCallbacks: list[Callable[[dict], None]] = []

    def setOnServiceCompletionCallback(self, callback: Callable[[], None]) -> None:
        self.onServiceCompletionCallback = callback

    def onServiceCompletion(self) -> None:
        if self.onServiceCompletionCallback:
            self.onServiceCompletionCallback()

    def start(self, skystoneAmount: int) -> None:
        self.e7ShopRefresh = E7X11ShopRefresh(windowId=self.windowId)
        self.e7ShopRefresh.attachObserver(self.onShopRefresh)
        self.e7ShopRefresh.attachOnComplete(self.onServiceCompletion)
        shopRefreshProcess = threading.Thread(
            target=self.e7ShopRefresh.start,
            args=(skystoneAmount,),
            daemon=True,
        )
        shopRefreshProcess.start()

    def stop(self) -> None:
        if self.e7ShopRefresh:
            self.e7ShopRefresh.stop()

    def attachObserver(self, callback: Callable[[dict], None]) -> None:
        self.observerCallbacks.append(callback)

    def notifyObservers(self, data: dict) -> None:
        for callback in self.observerCallbacks:
            callback(data)

    def onShopRefresh(self, data: dict) -> None:
        self.notifyObservers(data)
