from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtWidgets import QWidget


class PopupWindow(QWidget):
    WIDTH = 420
    HEIGHT = 160

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setFocusPolicy(Qt.StrongFocus)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setStyleSheet(
            "background-color: #2b2b2b; border: 1px solid #555;"
        )

    def toggle(self) -> None:
        if self.isVisible():
            self.close()
        else:
            self._move_to_cursor()
            self.show()
            self.activateWindow()
            self.raise_()
            self.setFocus()

    def _move_to_cursor(self) -> None:
        cursor_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(cursor_pos) or QGuiApplication.primaryScreen()
        screen_geo = screen.availableGeometry()

        x = min(cursor_pos.x(), screen_geo.right() - self.WIDTH)
        y = min(cursor_pos.y(), screen_geo.bottom() - self.HEIGHT)
        x = max(x, screen_geo.left())
        y = max(y, screen_geo.top())

        self.move(x, y)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
