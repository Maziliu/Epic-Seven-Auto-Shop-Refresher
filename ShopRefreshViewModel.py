import customtkinter
import tkinter
from functools import partial


def convertToGoldCost(skystoneAmount: int) -> int:
    return int(round(skystoneAmount * 1691.04536 * 2))

def convertToEstimatedCovenents(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * 0.006603509 * 2))

def convertToEstimatedMystics(skystoneAmount: int) -> float:
    return int(round(skystoneAmount * 0.001700646 * 2))

class ShopRefreshViewModel:
    def __init__(self, shopRefreshService):
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

    def onInputChange(self, inputStringVar, mirrorStringVar, convertCurrency, *args):
        currentValue = inputStringVar.get()
        if currentValue.isdigit():
            skystones = int(currentValue)
            result = convertCurrency(skystones)
            mirrorStringVar.set(f"{result:,}")
        else:
            mirrorStringVar.set("0")


    