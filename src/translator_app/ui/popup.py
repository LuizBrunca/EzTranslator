from PySide6.QtCore import QEvent, QRectF, Qt, QTimer
from PySide6.QtGui import QCursor, QGuiApplication, QPainterPath, QRegion
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..config import load_config, save_config
from ..translator.languages import AUTO_DETECT, AUTO_DETECT_LABEL, LANGUAGES
from ..translator.worker import TranslationWorker


class PopupWindow(QWidget):
    WIDTH = 420
    HEIGHT = 220
    CURSOR_OFFSET = 16
    DEBOUNCE_MS = 500
    CORNER_RADIUS = 12

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self._apply_rounded_mask()
        self.setStyleSheet(
            """
            QWidget {
                background-color: #1e1e1e;
                color: #f2f2f2;
                font-family: "Segoe UI Variable Text", "Segoe UI Semibold", "Segoe UI";
                font-size: 13px;
                font-weight: 500;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 6px 8px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #5b8def;
            }
            QLineEdit::placeholder {
                color: #8a8a8a;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                selection-background-color: #5b8def;
                outline: none;
            }
            QPushButton {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 6px 10px;
            }
            QPushButton:hover:enabled {
                background-color: #333333;
                border: 1px solid #5b8def;
            }
            QPushButton:disabled {
                color: #666666;
            }
            QPushButton#swapButton {
                border-radius: 16px;
                font-size: 15px;
                font-weight: 600;
                padding: 0px;
            }
            QPushButton#swapButton:enabled {
                color: #5b8def;
            }
            QTextEdit#outputText {
                font-size: 15px;
                font-weight: 500;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a4a;
                border-radius: 4px;
                min-height: 24px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5b8def;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            """
        )

        self._worker: TranslationWorker | None = None
        self._ignore_deactivate = False
        self._drag_offset = None

        config = load_config()

        self._source_combo = QComboBox(self)
        self._source_combo.addItem(AUTO_DETECT_LABEL, AUTO_DETECT)
        for name, code in LANGUAGES.items():
            self._source_combo.addItem(name, code)
        self._set_combo_value(self._source_combo, config["source_lang"])
        self._source_combo.currentIndexChanged.connect(self._on_source_changed)

        self._swap_button = QPushButton("↔", self)
        self._swap_button.setObjectName("swapButton")
        self._swap_button.setFixedSize(32, 32)
        self._swap_button.clicked.connect(self._on_swap_clicked)

        self._target_combo = QComboBox(self)
        for name, code in LANGUAGES.items():
            self._target_combo.addItem(name, code)
        self._set_combo_value(self._target_combo, config["target_lang"])
        self._target_combo.currentIndexChanged.connect(self._on_target_changed)

        lang_row = QHBoxLayout()
        lang_row.addWidget(self._source_combo, stretch=1)
        lang_row.addWidget(self._swap_button)
        lang_row.addWidget(self._target_combo, stretch=1)

        self._debounce_timer = QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(self.DEBOUNCE_MS)
        self._debounce_timer.timeout.connect(self._on_translate_requested)

        self._input = QLineEdit(self)
        self._input.setPlaceholderText("Type to translate...")
        self._input.returnPressed.connect(self._on_translate_requested)
        self._input.textChanged.connect(lambda: self._debounce_timer.start())

        self._output = QTextEdit(self)
        self._output.setObjectName("outputText")
        self._output.setReadOnly(True)
        self._output.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        self._copy_button = QPushButton("Copy", self)
        self._copy_button.setEnabled(False)
        self._copy_button.clicked.connect(self._on_copy_clicked)

        output_row = QHBoxLayout()
        output_row.addWidget(self._output, stretch=1)
        output_row.addWidget(self._copy_button, alignment=Qt.AlignmentFlag.AlignTop)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        layout.addLayout(lang_row)
        layout.addWidget(self._input)
        layout.addLayout(output_row, 1)

        self._update_swap_enabled()

    def toggle(self) -> None:
        if self.isVisible():
            self.close()
        else:
            self._sync_language_combos_from_config()
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

    def _sync_language_combos_from_config(self) -> None:
        config = load_config()
        self._source_combo.blockSignals(True)
        self._target_combo.blockSignals(True)
        self._set_combo_value(self._source_combo, config["source_lang"])
        self._set_combo_value(self._target_combo, config["target_lang"])
        self._source_combo.blockSignals(False)
        self._target_combo.blockSignals(False)
        self._update_swap_enabled()

    @staticmethod
    def _set_combo_value(combo: QComboBox, code: str) -> None:
        index = combo.findData(code)
        if index != -1:
            combo.setCurrentIndex(index)

    def _fill_from_clipboard(self) -> None:
        clipboard_text = QGuiApplication.clipboard().text()
        self._input.blockSignals(True)
        self._input.setText(clipboard_text)
        self._input.blockSignals(False)
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

    def _on_source_changed(self) -> None:
        self._update_swap_enabled()
        self._save_language_prefs()
        self._on_translate_requested()

    def _on_target_changed(self) -> None:
        self._save_language_prefs()
        self._on_translate_requested()

    def _save_language_prefs(self) -> None:
        config = load_config()
        config["source_lang"] = self._current_source()
        config["target_lang"] = self._current_target()
        save_config(config)

    def _on_swap_clicked(self) -> None:
        source_code = self._current_source()
        target_code = self._current_target()

        new_source_index = self._source_combo.findData(target_code)
        new_target_index = self._target_combo.findData(source_code)

        self._source_combo.blockSignals(True)
        self._target_combo.blockSignals(True)
        if new_source_index != -1:
            self._source_combo.setCurrentIndex(new_source_index)
        if new_target_index != -1:
            self._target_combo.setCurrentIndex(new_target_index)
        self._source_combo.blockSignals(False)
        self._target_combo.blockSignals(False)

        self._update_swap_enabled()
        self._save_language_prefs()

        if self._copy_button.isEnabled():  # there's a real translation result to carry over
            self._input.blockSignals(True)
            self._input.setText(self._output.toPlainText())
            self._input.blockSignals(False)
            self._on_translate_requested()

    def _on_translate_requested(self) -> None:
        if self._worker is not None:
            return

        text = self._input.text()
        if not text.strip():
            return

        self._output.setStyleSheet("")
        self._output.setPlainText("Translating...")
        self._copy_button.setEnabled(False)

        self._worker = TranslationWorker(text, self._current_source(), self._current_target())
        self._worker.finished_ok.connect(self._on_translated)
        self._worker.finished_error.connect(self._on_translation_failed)
        self._worker.finished.connect(self._on_worker_done)
        self._worker.start()

    def _on_translated(self, result: str) -> None:
        self._output.setPlainText(result)
        self._copy_button.setEnabled(True)

    def _on_translation_failed(self, message: str) -> None:
        self._output.setStyleSheet("color: #ff8080;")
        self._output.setPlainText(f"Error: {message}")

    def _on_worker_done(self) -> None:
        self._worker = None

    def _on_copy_clicked(self) -> None:
        QGuiApplication.clipboard().setText(self._output.toPlainText())
        self._copy_button.setText("Copied!")
        QTimer.singleShot(1200, lambda: self._copy_button.setText("Copy"))

    def _apply_rounded_mask(self) -> None:
        # Called once, right after setFixedSize — the window can never resize
        # again, so there's no need (and no risk of the resizeEvent-driven
        # layout-growth bug we hit) in recomputing this on every resize.
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, self.WIDTH, self.HEIGHT), self.CORNER_RADIUS, self.CORNER_RADIUS)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_offset = event.globalPosition().toPoint() - self.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() & Qt.MouseButton.LeftButton and self._drag_offset is not None:
            self.move(event.globalPosition().toPoint() - self._drag_offset)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_offset = None
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif (
            event.key() == Qt.Key.Key_S
            and event.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            if self._swap_button.isEnabled():
                self._on_swap_clicked()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event) -> None:
        self._debounce_timer.stop()
        super().closeEvent(event)

    def changeEvent(self, event) -> None:
        if (
            event.type() == QEvent.Type.ActivationChange
            and not self.isActiveWindow()
            and not self._ignore_deactivate
        ):
            self.close()
        super().changeEvent(event)
