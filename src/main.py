import sys
from typing import Optional
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication

from Style import APP_TITLE, get_app_icon, get_app_stylesheet
from ShopRefreshService import ShopRefreshService
from CurrencyService import CurrencyService
from ShopRefreshViewModel import ShopRefreshViewModel
from ShopRefreshView import ShopRefreshView
from WindowSelectorView import WindowSelectorView
from X11Utilities import findGameWindows


class MainWindow(QMainWindow):
    def __init__(self, viewModel: ShopRefreshViewModel, parent=None):
        super().__init__(parent)
        self.viewModel = viewModel

        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(get_app_icon())
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.view = ShopRefreshView(self.viewModel, self)
        self.setCentralWidget(self.view)

        self.setFixedSize(540, 470)
        self.centerOnScreen()

    def centerOnScreen(self) -> None:
        screen = QGuiApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            x = (geo.width() - self.width()) // 2
            y = (geo.height() - self.height()) // 2
            self.move(x, y)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(get_app_stylesheet())
    app.setWindowIcon(get_app_icon())

    detectedWindows = findGameWindows()
    selectedWindowId: Optional[int] = None

    if len(detectedWindows) == 1:
        selectedWindowId = detectedWindows[0][0]
    else:
        dialog = WindowSelectorView()
        if dialog.exec():
            selectedWindowId = dialog.selectedWindowId

    if not selectedWindowId:
        sys.exit(0)

    refreshService = ShopRefreshService(selectedWindowId)
    currencyService = CurrencyService(selectedWindowId)
    viewModel = ShopRefreshViewModel(refreshService, currencyService)

    mainWindow = MainWindow(viewModel)
    mainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
