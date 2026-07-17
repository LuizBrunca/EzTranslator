from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QWidget

from ..translator.worker import TranslationWorker


class PopupWindow(QWidget):
    WIDTH = 420
    HEIGHT = 160
    CURSOR_OFFSET = 16

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setFocusPolicy(Qt.StrongFocus)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setStyleSheet(
            "background-color: #2b2b2b; border: 1px solid #555; color: white;"
        )

        self._worker: TranslationWorker | None = None

        self._input = QLineEdit(self)
        self._input.setPlaceholderText("Type text in English and press Enter...")
        self._input.returnPressed.connect(self._on_translate_requested)

        self._output = QLabel(self)
        self._output.setWordWrap(True)
        self._output.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout = QVBoxLayout(self)
        layout.addWidget(self._input)
        layout.addWidget(self._output, stretch=1)

    def toggle(self) -> None:
        if self.isVisible():
            self.close()
        else:
            self._input.clear()
            self._output.clear()
            self._output.setStyleSheet("")
            self._move_to_cursor()
            self.show()
            self.activateWindow()
            self.raise_()
            self._input.setFocus()

    def _move_to_cursor(self) -> None:
        cursor_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(cursor_pos) or QGuiApplication.primaryScreen()
        screen_geo = screen.availableGeometry()

        x = min(cursor_pos.x() + self.CURSOR_OFFSET, screen_geo.right() - self.WIDTH)
        y = min(cursor_pos.y() + self.CURSOR_OFFSET, screen_geo.bottom() - self.HEIGHT)
        x = max(x, screen_geo.left())
        y = max(y, screen_geo.top())

        self.move(x, y)

    def _on_translate_requested(self) -> None:
        if self._worker is not None:
            return

        text = self._input.text()
        if not text.strip():
            return

        self._output.setStyleSheet("")
        self._output.setText("Translating...")

        self._worker = TranslationWorker(text)
        self._worker.finished_ok.connect(self._on_translated)
        self._worker.finished_error.connect(self._on_translation_failed)
        self._worker.finished.connect(self._on_worker_done)
        self._worker.start()

    def _on_translated(self, result: str) -> None:
        self._output.setText(result)

    def _on_translation_failed(self, message: str) -> None:
        self._output.setStyleSheet("color: #ff8080;")
        self._output.setText(f"Error: {message}")

    def _on_worker_done(self) -> None:
        self._worker = None

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
