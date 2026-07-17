from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..translator.engine import DEFAULT_TARGET
from ..translator.languages import AUTO_DETECT, AUTO_DETECT_LABEL, LANGUAGES
from ..translator.worker import TranslationWorker


class PopupWindow(QWidget):
    WIDTH = 420
    HEIGHT = 220
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
        self._ignore_deactivate = False

        self._source_combo = QComboBox(self)
        self._source_combo.addItem(AUTO_DETECT_LABEL, AUTO_DETECT)
        for name, code in LANGUAGES.items():
            self._source_combo.addItem(name, code)
        self._source_combo.currentIndexChanged.connect(self._update_swap_enabled)

        self._swap_button = QPushButton("⇆", self)
        self._swap_button.setFixedWidth(32)
        self._swap_button.clicked.connect(self._on_swap_clicked)

        self._target_combo = QComboBox(self)
        for name, code in LANGUAGES.items():
            self._target_combo.addItem(name, code)
        default_target_index = self._target_combo.findData(DEFAULT_TARGET)
        if default_target_index != -1:
            self._target_combo.setCurrentIndex(default_target_index)

        lang_row = QHBoxLayout()
        lang_row.addWidget(self._source_combo, stretch=1)
        lang_row.addWidget(self._swap_button)
        lang_row.addWidget(self._target_combo, stretch=1)

        self._input = QLineEdit(self)
        self._input.setPlaceholderText("Type text and press Enter...")
        self._input.returnPressed.connect(self._on_translate_requested)

        self._output = QLabel(self)
        self._output.setWordWrap(True)
        self._output.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self._copy_button = QPushButton("Copy", self)
        self._copy_button.setEnabled(False)
        self._copy_button.clicked.connect(self._on_copy_clicked)

        output_row = QHBoxLayout()
        output_row.addWidget(self._output, stretch=1)
        output_row.addWidget(self._copy_button, alignment=Qt.AlignmentFlag.AlignTop)

        layout = QVBoxLayout(self)
        layout.addLayout(lang_row)
        layout.addWidget(self._input)
        layout.addLayout(output_row, 1)

        self._update_swap_enabled()

    def toggle(self) -> None:
        if self.isVisible():
            self.close()
        else:
            self._fill_from_clipboard()
            self._move_to_cursor()
            self._ignore_deactivate = True
            self.show()
            self.activateWindow()
            self.raise_()
            self._input.setFocus()
            QTimer.singleShot(200, self._stop_ignoring_deactivate)

    def _stop_ignoring_deactivate(self) -> None:
        self._ignore_deactivate = False

    def _fill_from_clipboard(self) -> None:
        clipboard_text = QGuiApplication.clipboard().text()
        self._input.setText(clipboard_text)
        if clipboard_text.strip():
            self._on_translate_requested()
        else:
            self._output.setStyleSheet("")
            self._output.clear()
            self._copy_button.setEnabled(False)

    def _move_to_cursor(self) -> None:
        cursor_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(cursor_pos) or QGuiApplication.primaryScreen()
        screen_geo = screen.availableGeometry()

        x = min(cursor_pos.x() + self.CURSOR_OFFSET, screen_geo.right() - self.WIDTH)
        y = min(cursor_pos.y() + self.CURSOR_OFFSET, screen_geo.bottom() - self.HEIGHT)
        x = max(x, screen_geo.left())
        y = max(y, screen_geo.top())

        self.move(x, y)

    def _current_source(self) -> str:
        return self._source_combo.currentData()

    def _current_target(self) -> str:
        return self._target_combo.currentData()

    def _update_swap_enabled(self) -> None:
        self._swap_button.setEnabled(self._current_source() != AUTO_DETECT)

    def _on_swap_clicked(self) -> None:
        source_code = self._current_source()
        target_code = self._current_target()

        new_source_index = self._source_combo.findData(target_code)
        new_target_index = self._target_combo.findData(source_code)

        if new_source_index != -1:
            self._source_combo.setCurrentIndex(new_source_index)
        if new_target_index != -1:
            self._target_combo.setCurrentIndex(new_target_index)

        if self._copy_button.isEnabled():  # there's a real translation result to carry over
            self._input.setText(self._output.text())
            self._on_translate_requested()

    def _on_translate_requested(self) -> None:
        if self._worker is not None:
            return

        text = self._input.text()
        if not text.strip():
            return

        self._output.setStyleSheet("")
        self._output.setText("Translating...")
        self._copy_button.setEnabled(False)

        self._worker = TranslationWorker(text, self._current_source(), self._current_target())
        self._worker.finished_ok.connect(self._on_translated)
        self._worker.finished_error.connect(self._on_translation_failed)
        self._worker.finished.connect(self._on_worker_done)
        self._worker.start()

    def _on_translated(self, result: str) -> None:
        self._output.setText(result)
        self._copy_button.setEnabled(True)

    def _on_translation_failed(self, message: str) -> None:
        self._output.setStyleSheet("color: #ff8080;")
        self._output.setText(f"Error: {message}")

    def _on_worker_done(self) -> None:
        self._worker = None

    def _on_copy_clicked(self) -> None:
        QGuiApplication.clipboard().setText(self._output.text())
        self._copy_button.setText("Copied!")
        QTimer.singleShot(1200, lambda: self._copy_button.setText("Copy"))

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def changeEvent(self, event) -> None:
        if (
            event.type() == QEvent.Type.ActivationChange
            and not self.isActiveWindow()
            and not self._ignore_deactivate
        ):
            self.close()
        super().changeEvent(event)
