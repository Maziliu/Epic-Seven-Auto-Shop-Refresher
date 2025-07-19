from tkinter import StringVar
from E7ADBShopRefresh import E7Item
from ShopRefreshService import ShopRefreshService
from functools import partial
from typing import Callable

EXPECTED_GOLD_COST_PER_SKYSTONE = 3382.09072
EXPECTED_COVENANT_YIELD_PER_SKYSTONE = 0.013207018
EXPECTED_MYSTIC_YIELD_PER_SKYSTONE = 0.003401292
SKYSTONES_PER_REFRESH = 3


def convertToGoldCost(skystoneAmount: int) -> int:
    return int(round(skystoneAmount * EXPECTED_GOLD_COST_PER_SKYSTONE))


def convertToExpectedCovenents(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * EXPECTED_COVENANT_YIELD_PER_SKYSTONE))


def convertToExpectedMystics(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * EXPECTED_MYSTIC_YIELD_PER_SKYSTONE))


class ShopRefreshViewModel:
    def __init__(self, shopRefreshService: ShopRefreshService):
        self.shopRefreshService = shopRefreshService
        self.shopRefreshService.attachObserver(self.onShopRefresh)
        self.shopRefreshService.setOnServiceCompletionCallback(self.onServiceCompletion)

        self.onServiceCompletionCallback = None

        self.skystoneInputVariable = StringVar()
        self.expectedGold = StringVar(value="0")
        self.expectedCovenants = StringVar(value="0")
        self.expectedMystics = StringVar(value="0")

        self.skystonesSpent = StringVar(value="0")
        self.goldSpent = StringVar(value="0")
        self.covanentsPurchased = StringVar(value="0")
        self.mysticsPurchased = StringVar(value="0")

        self.skystoneInputVariable.trace_add(
            "write",
            partial(
                self.onInputChange,
                self.skystoneInputVariable,
                self.expectedGold,
                convertToGoldCost,
            ),
        )
        self.skystoneInputVariable.trace_add(
            "write",
            partial(
                self.onInputChange,
                self.skystoneInputVariable,
                self.expectedCovenants,
                convertToExpectedCovenents,
            ),
        )
        self.skystoneInputVariable.trace_add(
            "write",
            partial(
                self.onInputChange,
                self.skystoneInputVariable,
                self.expectedMystics,
                convertToExpectedMystics,
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
        convertCurrency: Callable[[int], float],
        *args,
    ) -> None:
        currentValue = inputStringVar.get()
        if currentValue.isdigit():
            skystones = int(currentValue)
            result = convertCurrency(skystones)
            mirrorStringVar.set(f"{result:,}")
        else:
            mirrorStringVar.set("0")

    def onShopRefresh(self, data: dict[str, E7Item | int]) -> None:
        goldSpent = 0
        for _, value in data.items():
            if type(value) == E7Item:
                goldSpent = goldSpent + value.count * value.price

        self.skystonesSpent.set(f'{data["Refresh Count"] * SKYSTONES_PER_REFRESH:,}')
        self.goldSpent.set(f"{goldSpent:,}")
        self.covanentsPurchased.set(f'{data["Covenant bookmark"].count:,}')
        self.mysticsPurchased.set(f'{data["Mystic medal"].count:,}')
