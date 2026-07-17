import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from . import single_instance
from .config import APP_NAME
from .hotkey_listener import DEFAULT_HOTKEY, HotkeyListener
from .logger import Logger
from .tray import TrayIcon
from .ui.popup import PopupWindow

logger = Logger(APP_NAME, "app")


def main() -> None:
    app = QApplication(sys.argv)
    # No window is ever the "main" window here (just a tray icon + popup), so Qt
    # must be told explicitly not to quit when the popup window is closed —
    # otherwise dismissing it would kill the whole app.
    app.setQuitOnLastWindowClosed(False)

    if not single_instance.acquire():
        logger.erro("Startup", "Another instance is already running.")
        QMessageBox.warning(None, APP_NAME, f"{APP_NAME} is already running.")
        sys.exit(1)

    logger.info("Startup", "Application starting.")

    tray = TrayIcon(app)
    tray.show()

    popup = PopupWindow()

    hotkey_listener = HotkeyListener()
    hotkey_listener.triggered.connect(popup.toggle)
    hotkey_listener.start()
    logger.info("Hotkey", f"Global hotkey listener started ({DEFAULT_HOTKEY}).")

    exit_code = app.exec()

    hotkey_listener.stop()
    logger.info("Shutdown", "Application exiting.")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
