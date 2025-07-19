from tkinter import StringVar
from ShopRefreshService import ShopRefreshService
from functools import partial
from typing import Callable

ESTIMATED_GOLD_COST_PER_SKYSTONE = 3382.09072
ESTIMATED_COVENANT_YIELD_PER_SKYSTONE = 0.013207018
ESTIMATED_MYSTIC_YIELD_PER_SKYSTONE = 0.003401292
SKYSTONES_PER_REFRESH = 3


def convertToGoldCost(skystoneAmount: int) -> int:
    return int(round(skystoneAmount * ESTIMATED_GOLD_COST_PER_SKYSTONE))


def convertToEstimatedCovenents(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * ESTIMATED_COVENANT_YIELD_PER_SKYSTONE))


def convertToEstimatedMystics(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * ESTIMATED_MYSTIC_YIELD_PER_SKYSTONE))


class ShopRefreshViewModel:
    def __init__(self, shopRefreshService: ShopRefreshService):
        self.shopRefreshService = shopRefreshService
        self.shopRefreshService.attachObserver(self.onShopRefresh)
        self.shopRefreshService.setOnServiceCompletionCallback(self.onServiceCompletion)

        self.onServiceCompletionCallback = None

        self.skystoneInputVariable = StringVar()
        self.estimatedGold = StringVar(value="0")
        self.estimatedCovenants = StringVar(value="0")
        self.estimatedMystics = StringVar(value="0")

        self.skystonesSpent = StringVar(value="0")
        self.covanentsPurchased = StringVar(value="0")
        self.mysticsPurchased = StringVar(value="0")

        self.skystoneInputVariable.trace_add(
            "write",
            partial(
                self.onInputChange,
                self.skystoneInputVariable,
                self.estimatedGold,
                convertToGoldCost,
            ),
        )
        self.skystoneInputVariable.trace_add(
            "write",
            partial(
                self.onInputChange,
                self.skystoneInputVariable,
                self.estimatedCovenants,
                convertToEstimatedCovenents,
            ),
        )
        self.skystoneInputVariable.trace_add(
            "write",
            partial(
                self.onInputChange,
                self.skystoneInputVariable,
                self.estimatedMystics,
                convertToEstimatedMystics,
            ),
        )

    def setServiceCompletionCallback(self, callback: Callable[[None], None]) -> None:
        self.onServiceCompletionCallback = callback

    def onServiceCompletion(self):
        if self.onServiceCompletionCallback:
            self.onServiceCompletionCallback()
            self.skystoneInputVariable.set("")

    def isValidSkystoneAmount(self) -> bool:
        currentSkystoneValue = self.skystoneInputVariable.get()
        return (
            currentSkystoneValue.isdigit()
            and int(currentSkystoneValue) >= SKYSTONES_PER_REFRESH
        )

    def startRefresh(self) -> None:
        currentSkystoneValue = self.skystoneInputVariable.get()
        self.skystonesSpent.set("0")
        self.covanentsPurchased.set("0")
        self.mysticsPurchased.set("0")
        self.shopRefreshService.start(int(currentSkystoneValue))

    def stopRefresh(self) -> None:
        self.shopRefreshService.stop()
        self.skystoneInputVariable.set("")

    def onInputChange(
        self,
        inputStringVar: StringVar,
        mirrorStringVar: StringVar,
        convertCurrency: StringVar,
        *args,
    ) -> None:
        currentValue = inputStringVar.get()
        if currentValue.isdigit():
            skystones = int(currentValue)
            result = convertCurrency(skystones)
            mirrorStringVar.set(f"{result:,}")
        else:
            mirrorStringVar.set("0")

    def onShopRefresh(self, data: dict) -> None:
        self.skystonesSpent.set(str(data["Refresh Count"] * SKYSTONES_PER_REFRESH))
        self.covanentsPurchased.set(str(data["Covenant bookmark"]))
        self.mysticsPurchased.set(str(data["Mystic medal"]))
