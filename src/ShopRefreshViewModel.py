from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal
from ShopRefreshService import ShopRefreshService

GOLD_COST_PER_COVENANT = 184000
GOLD_COST_PER_MYSTIC = 280000
EXPECTED_COVENANT_YIELD_PER_SKYSTONE = 0.013207018
EXPECTED_MYSTIC_YIELD_PER_SKYSTONE = 0.003401292
SKYSTONES_PER_REFRESH = 3


def convertToGoldCost(skystoneAmount: int) -> int:
    return (
        convertToExpectedCovenants(skystoneAmount) * GOLD_COST_PER_COVENANT
        + convertToExpectedMystics(skystoneAmount) * GOLD_COST_PER_MYSTIC
    )


def convertToExpectedCovenants(skystoneAmount: int) -> int:
    return int(round(skystoneAmount * EXPECTED_COVENANT_YIELD_PER_SKYSTONE))


def convertToExpectedMystics(skystoneAmount: int) -> int:
    return int(round(skystoneAmount * EXPECTED_MYSTIC_YIELD_PER_SKYSTONE))


class ShopRefreshViewModel(QObject):
    statsUpdated = pyqtSignal()
    statusChanged = pyqtSignal(str, str)
    progressChanged = pyqtSignal(int)
    runningStateChanged = pyqtSignal(bool)

    def __init__(self, shopRefreshService: ShopRefreshService):
        super().__init__()
        self.shopRefreshService = shopRefreshService
        self.shopRefreshService.attachObserver(self.onShopRefresh)
        self.shopRefreshService.setOnServiceCompletionCallback(self.onServiceCompletion)

        self.skystonesInput: int = 0
        self.targetCycles: int = 0
        self.currentRefreshCount: int = 0
        self.isRunning: bool = False

        self.expectedGold: int = 0
        self.expectedCovenants: int = 0
        self.expectedMystics: int = 0

        self.skystonesSpent: int = 0
        self.goldSpent: int = 0
        self.covenantsPurchased: int = 0
        self.mysticsPurchased: int = 0

    def setSkystones(self, amount: int) -> None:
        self.skystonesInput = max(0, amount)
        self.targetCycles = self.skystonesInput // SKYSTONES_PER_REFRESH
        self.expectedGold = convertToGoldCost(self.skystonesInput)
        self.expectedCovenants = convertToExpectedCovenants(self.skystonesInput)
        self.expectedMystics = convertToExpectedMystics(self.skystonesInput)
        self.statsUpdated.emit()

    def addSkystones(self, amount: int) -> None:
        self.setSkystones(self.skystonesInput + amount)

    def clearSkystones(self) -> None:
        self.setSkystones(0)

    def getPlannedRefreshesText(self) -> str:
        if self.skystonesInput >= SKYSTONES_PER_REFRESH:
            cycles = self.skystonesInput // SKYSTONES_PER_REFRESH
            return f"{cycles:,} refreshes"
        return "0 refreshes"

    def isValidSkystoneAmount(self) -> bool:
        return self.skystonesInput >= SKYSTONES_PER_REFRESH

    def startRefresh(self) -> None:
        if not self.isValidSkystoneAmount() or self.isRunning:
            return

        self.isRunning = True
        self.targetCycles = self.skystonesInput // SKYSTONES_PER_REFRESH
        self.currentRefreshCount = 0

        self.skystonesSpent = 0
        self.goldSpent = 0
        self.covenantsPurchased = 0
        self.mysticsPurchased = 0

        self.statsUpdated.emit()
        self.progressChanged.emit(0)
        self.runningStateChanged.emit(True)
        self.statusChanged.emit(
            f"Running: Refresh 0 / {self.targetCycles:,} (0%)",
            "running",
        )

        self.shopRefreshService.start(self.skystonesInput)

    def stopRefresh(self) -> None:
        if not self.isRunning:
            return
        self.isRunning = False
        self.shopRefreshService.stop()
        self.runningStateChanged.emit(False)
        self.statusChanged.emit(
            f"Stopped at {self.currentRefreshCount:,} / {self.targetCycles:,} refreshes",
            "stopped",
        )

    def onServiceCompletion(self) -> None:
        if self.isRunning:
            self.isRunning = False
            self.runningStateChanged.emit(False)
            self.progressChanged.emit(100)
            self.statusChanged.emit(
                f"Completed {self.currentRefreshCount:,} refreshes! ({self.currentRefreshCount * SKYSTONES_PER_REFRESH:,} SS spent)",
                "completed",
            )

    def onShopRefresh(self, data: dict) -> None:
        covenants = data.get("Covenant", 0)
        mystics = data.get("Mystic", 0)
        refreshCount = data.get("Refresh Count", 0)
        self.currentRefreshCount = refreshCount

        self.covenantsPurchased = covenants
        self.mysticsPurchased = mystics
        self.goldSpent = covenants * GOLD_COST_PER_COVENANT + mystics * GOLD_COST_PER_MYSTIC
        self.skystonesSpent = refreshCount * SKYSTONES_PER_REFRESH

        if self.targetCycles > 0:
            percent = min(100, int((refreshCount / self.targetCycles) * 100))
            self.progressChanged.emit(percent)
            self.statusChanged.emit(
                f"Running: Refresh {refreshCount:,} / {self.targetCycles:,} ({percent}%)",
                "running",
            )
        else:
            self.statusChanged.emit(f"Running: Refresh {refreshCount:,}", "running")

        self.statsUpdated.emit()
