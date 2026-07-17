from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from .config import APP_NAME, ICON_PATH


class TrayIcon(QSystemTrayIcon):
    def __init__(self, app: QApplication, popup, settings_window):
        super().__init__(QIcon(str(ICON_PATH)))
        self.setToolTip(APP_NAME)

        menu = QMenu()

        open_action = menu.addAction("Open")
        open_action.triggered.connect(popup.toggle)

        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(settings_window.open)

        menu.addSeparator()

        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(app.quit)

        self.setContextMenu(menu)
