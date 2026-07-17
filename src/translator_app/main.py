import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from . import single_instance
from .config import APP_NAME
from .logger import Logger
from .tray import TrayIcon

logger = Logger(APP_NAME, "app")


def main() -> None:
    app = QApplication(sys.argv)
    # No window is ever the "main" window here (just a tray icon), so Qt must be
    # told explicitly not to quit when a popup window (added in a later milestone)
    # is closed — otherwise closing that window would kill the whole app.
    app.setQuitOnLastWindowClosed(False)

    if not single_instance.acquire():
        logger.erro("Startup", "Another instance is already running.")
        QMessageBox.warning(None, APP_NAME, f"{APP_NAME} is already running.")
        sys.exit(1)

    logger.info("Startup", "Application starting.")

    tray = TrayIcon(app)
    tray.show()

    exit_code = app.exec()

    logger.info("Shutdown", "Application exiting.")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
