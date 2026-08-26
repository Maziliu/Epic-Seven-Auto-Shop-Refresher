import os
from PyQt6.QtGui import QIcon

SRC_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIRECTORY = os.path.join(SRC_DIRECTORY, "..", "assets")

APP_TITLE = "Epic Seven Auto Shop Refresher"

COLOR_SKYSTONES = "rgba(56, 189, 248, 0.9)"
COLOR_GOLD = "rgba(251, 191, 36, 0.9)"
COLOR_COVENANTS = "rgba(96, 165, 250, 0.9)"
COLOR_MYSTICS = "rgba(251, 146, 60, 0.9)"
COLOR_SUCCESS = "rgba(52, 211, 153, 0.9)"
COLOR_DANGER = "rgba(248, 113, 113, 0.9)"
COLOR_MUTED = "rgba(161, 161, 170, 0.9)"


def get_app_icon() -> QIcon:
    icon_path_png = os.path.join(ASSETS_DIRECTORY, "icon.png")
    icon_path_ico = os.path.join(ASSETS_DIRECTORY, "icon.ico")
    if os.path.exists(icon_path_png):
        return QIcon(icon_path_png)
    elif os.path.exists(icon_path_ico):
        return QIcon(icon_path_ico)
    return QIcon()


def get_app_stylesheet() -> str:
    return """
    QMainWindow, QDialog, QWidget {
        background-color: #18181b;
        color: rgba(250, 250, 250, 0.9);
        font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif;
        font-size: 14px;
    }

    QLabel {
        background-color: transparent;
        background: transparent;
        color: rgba(250, 250, 250, 0.9);
    }

    QFrame#cardFrame {
        background-color: #27272a;
        border: 1px solid #3f3f46;
        border-radius: 10px;
    }

    QLabel#appTitleLabel {
        background: transparent;
        font-size: 20px;
        font-weight: bold;
        color: rgba(255, 255, 255, 0.9);
    }

    QLabel#cardTitleLabel {
        background: transparent;
        font-size: 15px;
        font-weight: bold;
        color: rgba(255, 255, 255, 0.9);
    }

    QLabel#statTitleLabel {
        background: transparent;
        font-size: 13px;
        color: rgba(161, 161, 170, 0.9);
    }

    QLabel#statValueLabel {
        background: transparent;
        font-size: 16px;
        font-weight: bold;
    }

    QLabel#summaryBadgeLabel {
        background: transparent;
        font-size: 13px;
        font-weight: bold;
        color: rgba(56, 189, 248, 0.9);
    }

    QLabel#statusLabel {
        background: transparent;
        font-size: 14px;
        font-weight: bold;
        color: rgba(52, 211, 153, 0.9);
    }

    QLabel#hintLabel {
        background: transparent;
        font-size: 12px;
        color: rgba(113, 113, 122, 0.9);
    }

    QLineEdit {
        background-color: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 16px;
        font-weight: bold;
        color: rgba(255, 255, 255, 0.9);
        selection-background-color: #3b82f6;
    }
    QLineEdit:focus {
        border: 1px solid #38bdf8;
    }
    QLineEdit:disabled {
        background-color: #27272a;
        color: rgba(113, 113, 122, 0.9);
    }

    QPushButton {
        background-color: #3f3f46;
        color: rgba(250, 250, 250, 0.9);
        border: 1px solid #52525b;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #52525b;
    }
    QPushButton:pressed {
        background-color: #27272a;
    }
    QPushButton:disabled {
        background-color: #27272a;
        border-color: #3f3f46;
        color: rgba(113, 113, 122, 0.9);
    }

    QPushButton#startBtn {
        background-color: #059669;
        border: none;
        color: rgba(255, 255, 255, 0.9);
        font-size: 15px;
        padding: 10px;
        border-radius: 8px;
    }
    QPushButton#startBtn:hover {
        background-color: #047857;
    }
    QPushButton#startBtn:pressed {
        background-color: #065f46;
    }
    QPushButton#startBtn:disabled {
        background-color: #064e3b;
        color: rgba(110, 231, 183, 0.9);
        opacity: 0.5;
    }

    QPushButton#stopBtn {
        background-color: #ef4444;
        border: none;
        color: rgba(255, 255, 255, 0.9);
        font-size: 15px;
        padding: 10px;
        border-radius: 8px;
    }
    QPushButton#stopBtn:hover {
        background-color: #dc2626;
    }
    QPushButton#stopBtn:pressed {
        background-color: #b91c1c;
    }
    QPushButton#stopBtn:disabled {
        background-color: #450a0a;
        color: rgba(252, 165, 165, 0.9);
        opacity: 0.5;
    }

    QProgressBar {
        background-color: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 5px;
        height: 10px;
        text-align: center;
        font-size: 11px;
    }
    QProgressBar::chunk {
        background-color: #10b981;
        border-radius: 4px;
    }

    QComboBox {
        background-color: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 14px;
        color: rgba(255, 255, 255, 0.9);
    }
    QComboBox:focus {
        border-color: #38bdf8;
    }
    QComboBox::drop-down {
        border: none;
        width: 24px;
    }
    QComboBox QAbstractItemView {
        background-color: #27272a;
        border: 1px solid #3f3f46;
        selection-background-color: #3b82f6;
        color: rgba(255, 255, 255, 0.9);
        padding: 4px;
    }
    """
