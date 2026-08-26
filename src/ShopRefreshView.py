import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QPixmap
from Style import (
    COLOR_SKYSTONES,
    COLOR_GOLD,
    COLOR_COVENANTS,
    COLOR_MYSTICS,
    COLOR_SUCCESS,
    COLOR_DANGER,
    COLOR_MUTED,
    ASSETS_DIRECTORY,
)
from ShopRefreshViewModel import ShopRefreshViewModel


class ShopRefreshView(QWidget):
    def __init__(self, viewModel: ShopRefreshViewModel, parent: QWidget):
        super().__init__(parent)
        self.viewModel = viewModel

        self.initUI()
        self.connectViewModel()
        self.updateStatsDisplay()

    def initUI(self) -> None:
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(14)

        headerLayout = QHBoxLayout()
        headerLayout.setSpacing(12)

        iconLabel = QLabel(self)
        iconPathPng = os.path.join(ASSETS_DIRECTORY, "icon.png")
        if os.path.exists(iconPathPng):
            pixmap = QPixmap(iconPathPng).scaled(
                36,
                36,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            iconLabel.setPixmap(pixmap)
        headerLayout.addWidget(iconLabel)

        titleLayout = QVBoxLayout()
        titleLayout.setSpacing(2)

        appTitle = QLabel("Epic Seven Shop Refresher", self)
        appTitle.setObjectName("appTitleLabel")
        titleLayout.addWidget(appTitle)

        subTitle = QLabel("Automated X11 / Wine Secret Shop", self)
        subTitle.setObjectName("hintLabel")
        titleLayout.addWidget(subTitle)

        headerLayout.addLayout(titleLayout)
        headerLayout.addStretch()
        mainLayout.addLayout(headerLayout)

        inputCard = QFrame(self)
        inputCard.setObjectName("cardFrame")
        inputCardLayout = QVBoxLayout(inputCard)
        inputCardLayout.setContentsMargins(16, 14, 16, 14)
        inputCardLayout.setSpacing(10)

        cardTitleRow = QHBoxLayout()
        cardTitle = QLabel("Target Skystones", inputCard)
        cardTitle.setObjectName("cardTitleLabel")
        cardTitleRow.addWidget(cardTitle)

        self.summaryBadge = QLabel("0 refreshes planned", inputCard)
        self.summaryBadge.setObjectName("summaryBadgeLabel")
        self.summaryBadge.setAlignment(Qt.AlignmentFlag.AlignRight)
        cardTitleRow.addWidget(self.summaryBadge)
        inputCardLayout.addLayout(cardTitleRow)

        self.skystoneInput = QLineEdit(inputCard)
        self.skystoneInput.setValidator(QIntValidator(0, 999999, self))
        self.skystoneInput.textChanged.connect(self.onInputTextChanged)
        inputCardLayout.addWidget(self.skystoneInput)

        mainLayout.addWidget(inputCard)

        
        statsContainer = QHBoxLayout()
        statsContainer.setSpacing(14)

        leftCard = QFrame(self)
        leftCard.setObjectName("cardFrame")
        leftLayout = QVBoxLayout(leftCard)
        leftLayout.setContentsMargins(16, 14, 16, 14)
        leftLayout.setSpacing(12)

        leftTitle = QLabel("Expected", leftCard)
        leftTitle.setObjectName("cardTitleLabel")
        leftLayout.addWidget(leftTitle)

        self.expRefreshesLabel = self.createStatItem(leftLayout, "Refreshes", COLOR_SKYSTONES)
        self.expGoldLabel = self.createStatItem(leftLayout, "Gold", COLOR_GOLD)
        self.expCovLabel = self.createStatItem(leftLayout, "Covenants", COLOR_COVENANTS)
        self.expMysLabel = self.createStatItem(leftLayout, "Mystics", COLOR_MYSTICS)

        statsContainer.addWidget(leftCard, 1)

        rightCard = QFrame(self)
        rightCard.setObjectName("cardFrame")
        rightLayout = QVBoxLayout(rightCard)
        rightLayout.setContentsMargins(16, 14, 16, 14)
        rightLayout.setSpacing(12)

        rightTitle = QLabel("Results", rightCard)
        rightTitle.setObjectName("cardTitleLabel")
        rightLayout.addWidget(rightTitle)

        self.liveRefreshesLabel = self.createStatItem(rightLayout, "Refreshes Done", COLOR_SKYSTONES)
        self.liveGoldLabel = self.createStatItem(rightLayout, "Gold", COLOR_GOLD)
        self.liveCovLabel = self.createStatItem(rightLayout, "Covenants", COLOR_COVENANTS)
        self.liveMysLabel = self.createStatItem(rightLayout, "Mystics", COLOR_MYSTICS)

        statsContainer.addWidget(rightCard, 1)
        mainLayout.addLayout(statsContainer)

        actionsLayout = QHBoxLayout()
        actionsLayout.setSpacing(12)

        self.startBtn = QPushButton("Start", self)
        self.startBtn.setObjectName("startBtn")
        self.startBtn.setFixedHeight(46)
        self.startBtn.clicked.connect(self.viewModel.startRefresh)
        actionsLayout.addWidget(self.startBtn)

        self.stopBtn = QPushButton("Stop", self)
        self.stopBtn.setObjectName("stopBtn")
        self.stopBtn.setFixedHeight(46)
        self.stopBtn.setEnabled(False)
        self.stopBtn.clicked.connect(self.viewModel.stopRefresh)
        actionsLayout.addWidget(self.stopBtn)

        mainLayout.addLayout(actionsLayout)

    def createStatItem(
        self,
        parentLayout: QVBoxLayout,
        title: str,
        valueColor: str,
    ) -> QLabel:
        rowLayout = QHBoxLayout()
        rowLayout.setContentsMargins(0, 2, 0, 2)
        rowLayout.setSpacing(8)

        titleLabel = QLabel(title)
        titleLabel.setObjectName("statTitleLabel")
        rowLayout.addWidget(titleLabel)

        rowLayout.addStretch()

        valueLabel = QLabel("0")
        valueLabel.setObjectName("statValueLabel")
        valueLabel.setStyleSheet(f"color: {valueColor}; background: transparent;")
        valueLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        rowLayout.addWidget(valueLabel)

        parentLayout.addLayout(rowLayout)
        return valueLabel

    def connectViewModel(self) -> None:
        self.viewModel.statsUpdated.connect(self.updateStatsDisplay)
        self.viewModel.runningStateChanged.connect(self.setRunningState)

    def onInputTextChanged(self, text: str) -> None:
        val = int(text) if text.strip().isdigit() else 0
        if val != self.viewModel.skystonesInput:
            self.viewModel.setSkystones(val)

    def updateStatsDisplay(self) -> None:
        strVal = str(self.viewModel.skystonesInput) if self.viewModel.skystonesInput > 0 else ""
        if self.skystoneInput.text() != strVal:
            self.skystoneInput.blockSignals(True)
            self.skystoneInput.setText(strVal)
            self.skystoneInput.blockSignals(False)

        self.summaryBadge.setText(self.viewModel.getPlannedRefreshesText())

        self.expRefreshesLabel.setText(f"{self.viewModel.targetCycles:,}")
        self.expGoldLabel.setText(f"{self.viewModel.expectedGold:,}")
        self.expCovLabel.setText(f"{self.viewModel.expectedCovenants:,}")
        self.expMysLabel.setText(f"{self.viewModel.expectedMystics:,}")

        self.liveRefreshesLabel.setText(f"{self.viewModel.currentRefreshCount:,}")
        self.liveGoldLabel.setText(f"{self.viewModel.goldSpent:,}")
        self.liveCovLabel.setText(f"{self.viewModel.covenantsPurchased:,}")
        self.liveMysLabel.setText(f"{self.viewModel.mysticsPurchased:,}")

    def setRunningState(self, isRunning: bool) -> None:
        self.skystoneInput.setEnabled(not isRunning)
        self.startBtn.setEnabled(not isRunning)
        self.stopBtn.setEnabled(isRunning)
