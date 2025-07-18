import E7ADBShopRefresh
import threading

class ShopRefreshService:
    def __init__(self):
        self.e7ADBShopRefresh = None
    
    def start(self, skystoneAmount: int) -> None:
        self.e7ADBShopRefresh = E7ADBShopRefresh.E7ADBShopRefresh(budget=skystoneAmount)
        shopRefreshProcess = threading.Thread(target=self.e7ADBShopRefresh.start, daemon=True)
        shopRefreshProcess.start()

    def stop(self) -> None:
        if self.e7ADBShopRefresh:
            self.e7ADBShopRefresh.end_of_refresh = True
            self.e7ADBShopRefresh.loop_active = False

