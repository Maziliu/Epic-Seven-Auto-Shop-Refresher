import E7ADBShopRefresh

class ShopRefreshService:
    def __init__(self):
        self.e7ADBShopRefresh = None
    
    def start(self, skystoneAmount):
        self.e7ADBShopRefresh = E7ADBShopRefresh.E7ADBShopRefresh(budget=skystoneAmount)
        self.e7ADBShopRefresh.start()


