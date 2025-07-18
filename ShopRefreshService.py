from E7ADBShopRefresh import E7ADBShopRefresh
import threading

class ShopRefreshService:
    def __init__(self):
        self.e7ADBShopRefresh = None
        self.observers = []
    
    def start(self, skystoneAmount: int) -> None:
        self.e7ADBShopRefresh = E7ADBShopRefresh(budget=skystoneAmount)
        self.e7ADBShopRefresh.attachObserver(self.onShopRefresh)
        shopRefreshProcess = threading.Thread(target=self.e7ADBShopRefresh.start, daemon=True)
        shopRefreshProcess.start()

    def stop(self) -> None:
        if self.e7ADBShopRefresh:
            self.e7ADBShopRefresh.end_of_refresh = True
            self.e7ADBShopRefresh.loop_active = False

    def attachObserver(self, callback) -> None:
        self.observers.append(callback)
    
    def notifyObservers(self, data: dict) -> None:
        for callback in self.observers:
            callback(data)
            
    def onShopRefresh(self, data: dict) -> None:
        self.notifyObservers(data)