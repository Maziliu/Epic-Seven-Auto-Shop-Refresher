import customtkinter
import tkinter
from ShopRefreshService import ShopRefreshService
from functools import partial

ESTIMATED_GOLD_COST_PER_SKYSTONE = 3382.09072
ESTIMATED_COVENANT_YIELD_PER_SKYSTONE = 0.013207018
ESTIMATED_MYSTIC_YIELD_PER_SKYSTONE = 0.003401292

def convertToGoldCost(skystoneAmount: int) -> int:
    return int(round(skystoneAmount * ESTIMATED_GOLD_COST_PER_SKYSTONE))

def convertToEstimatedCovenents(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * ESTIMATED_COVENANT_YIELD_PER_SKYSTONE))

def convertToEstimatedMystics(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * ESTIMATED_MYSTIC_YIELD_PER_SKYSTONE))

class ShopRefreshViewModel:
    def __init__(self, shopRefreshService: ShopRefreshService):
        self.shopRefreshService = shopRefreshService

        self.skystoneInputVariable = tkinter.StringVar()
        self.estimatedGold = tkinter.StringVar(value="0")
        self.estimatedCovenants = tkinter.StringVar(value="0")
        self.estimatedMystics = tkinter.StringVar(value="0")

        self.skystoneInputVariable.trace_add("write", partial(self.onInputChange, self.skystoneInputVariable, self.estimatedGold, convertToGoldCost))
        self.skystoneInputVariable.trace_add("write", partial(self.onInputChange, self.skystoneInputVariable, self.estimatedCovenants, convertToEstimatedCovenents))
        self.skystoneInputVariable.trace_add("write", partial(self.onInputChange, self.skystoneInputVariable, self.estimatedMystics, convertToEstimatedMystics))
    
    def startRefresh(self) -> None:
        currentSkystoneValue = self.skystoneInputVariable.get()

        if(currentSkystoneValue.isdigit()):
            self.shopRefreshService.start(int(currentSkystoneValue))

    def stopRefresh(self) -> None:
        self.shopRefreshService.stop()

    def onInputChange(self, inputStringVar: tkinter.StringVar, mirrorStringVar: tkinter.StringVar, convertCurrency: tkinter.StringVar, *args) -> None:
        currentValue = inputStringVar.get()
        if currentValue.isdigit():
            skystones = int(currentValue)
            result = convertCurrency(skystones)
            mirrorStringVar.set(f"{result:,}")
        else:
            mirrorStringVar.set("0")


    