import os
from typing import Optional, List, Tuple
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from Style import get_app_icon, ASSETS_DIRECTORY, COLOR_DANGER
from X11Utilities import findGameWindows


class WindowSelectorView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selectedWindowId: Optional[int] = None
        self.windowMap = {}

        self.setWindowTitle("Select Game Window")
        self.setWindowIcon(get_app_icon())
        self.setFixedWidth(500)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.initUI()
        self.scanWindows()
        self.adjustSize()

    def initUI(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        headerLayout = QHBoxLayout()
        headerLayout.setSpacing(12)

        iconLabel = QLabel(self)
        iconPathPng = os.path.join(ASSETS_DIRECTORY, "icon.png")
        if os.path.exists(iconPathPng):
            pixmap = QPixmap(iconPathPng).scaled(
                32,
                32,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            iconLabel.setPixmap(pixmap)
        headerLayout.addWidget(iconLabel)

        titleLayout = QVBoxLayout()
        titleLayout.setSpacing(2)

        title = QLabel("Connect Game Window", self)
        title.setObjectName("cardTitleLabel")
        titleLayout.addWidget(title)

        subTitle = QLabel("Select your Epic Seven / Wine emulator window", self)
        subTitle.setObjectName("hintLabel")
        titleLayout.addWidget(subTitle)

        headerLayout.addLayout(titleLayout)
        headerLayout.addStretch()
        layout.addLayout(headerLayout)

        self.cardFrame = QFrame(self)
        self.cardFrame.setObjectName("cardFrame")
        self.cardLayout = QVBoxLayout(self.cardFrame)
        self.cardLayout.setContentsMargins(14, 14, 14, 14)
        self.cardLayout.setSpacing(10)

        self.statusLabel = QLabel("Detected Windows:", self.cardFrame)
        self.statusLabel.setObjectName("statTitleLabel")
        self.cardLayout.addWidget(self.statusLabel)

        selectRow = QHBoxLayout()
        selectRow.setSpacing(8)

        self.comboBox = QComboBox(self.cardFrame)
        selectRow.addWidget(self.comboBox, 1)

        self.rescanBtn = QPushButton("🔄 Rescan", self.cardFrame)
        self.rescanBtn.clicked.connect(self.scanWindows)
        selectRow.addWidget(self.rescanBtn)

        self.cardLayout.addLayout(selectRow)

        self.warnLabel = QLabel("", self.cardFrame)
        self.warnLabel.setStyleSheet(f"color: {COLOR_DANGER}; font-size: 13px;")
        self.warnLabel.setVisible(False)
        self.cardLayout.addWidget(self.warnLabel)

        layout.addWidget(self.cardFrame)

        btnRow = QHBoxLayout()
        btnRow.setSpacing(10)

        self.cancelBtn = QPushButton("Cancel", self)
        self.cancelBtn.clicked.connect(self.reject)
        btnRow.addWidget(self.cancelBtn)

        self.connectBtn = QPushButton("Connect Window", self)
        self.connectBtn.setObjectName("startBtn")
        self.connectBtn.clicked.connect(self.onConnect)
        btnRow.addWidget(self.connectBtn)

        layout.addLayout(btnRow)

    def scanWindows(self) -> None:
        self.comboBox.clear()
        self.windowMap.clear()

        windows: List[Tuple[int, str]] = findGameWindows()
        if windows:
            self.warnLabel.setVisible(False)
            self.connectBtn.setEnabled(True)
            self.statusLabel.setText(f"Detected Windows ({len(windows)}):")
            for winId, name in windows:
                key = f"{name} (ID: {winId})"
                self.windowMap[key] = winId
                self.comboBox.addItem(key)
        else:
            self.statusLabel.setText("Detected Windows (0):")
            self.warnLabel.setText("No game window found. Make sure Epic Seven is running.")
            self.warnLabel.setVisible(True)
            self.connectBtn.setEnabled(False)

    def onConnect(self) -> None:
        selectedText = self.comboBox.currentText()
        winId = self.windowMap.get(selectedText)
        if winId:
            self.selectedWindowId = winId
            self.accept()
