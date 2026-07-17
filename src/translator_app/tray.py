from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from .config import APP_NAME, ICON_PATH


class TrayIcon(QSystemTrayIcon):
    def __init__(self, app: QApplication):
        super().__init__(QIcon(str(ICON_PATH)))
        self.setToolTip(APP_NAME)

        menu = QMenu()
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(app.quit)

        self.setContextMenu(menu)
