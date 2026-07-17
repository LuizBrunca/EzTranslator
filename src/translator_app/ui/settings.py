from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QComboBox, QFormLayout, QLineEdit, QVBoxLayout, QWidget

from ..config import APP_NAME, load_config, save_config
from ..hotkey_listener import qt_event_to_hotkey_string
from ..translator.languages import AUTO_DETECT, AUTO_DETECT_LABEL, LANGUAGES


def _prettify_hotkey(hotkey: str) -> str:
    return "+".join(part.strip("<>").capitalize() for part in hotkey.split("+"))


class HotkeyCaptureField(QLineEdit):
    hotkey_captured = Signal(str)

    def __init__(self, current_hotkey: str, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._current_hotkey = current_hotkey
        self.set_current(current_hotkey)

    def set_current(self, hotkey: str) -> None:
        self._current_hotkey = hotkey
        self.setText(_prettify_hotkey(hotkey))

    def focusInEvent(self, event) -> None:
        super().focusInEvent(event)
        self.setText("Press new combination... (Esc to cancel)")

    def focusOutEvent(self, event) -> None:
        super().focusOutEvent(event)
        self.setText(_prettify_hotkey(self._current_hotkey))

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.clearFocus()
            return

        hotkey = qt_event_to_hotkey_string(event)
        if hotkey is not None:
            self.hotkey_captured.emit(hotkey)
            self.clearFocus()


class SettingsWindow(QWidget):
    def __init__(self, hotkey_listener):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} — Settings")
        self.resize(360, 160)

        self._hotkey_listener = hotkey_listener
        config = load_config()

        self._source_combo = QComboBox(self)
        self._source_combo.addItem(AUTO_DETECT_LABEL, AUTO_DETECT)
        for name, code in LANGUAGES.items():
            self._source_combo.addItem(name, code)
        self._set_combo_value(self._source_combo, config["source_lang"])
        self._source_combo.currentIndexChanged.connect(self._on_source_changed)

        self._target_combo = QComboBox(self)
        for name, code in LANGUAGES.items():
            self._target_combo.addItem(name, code)
        self._set_combo_value(self._target_combo, config["target_lang"])
        self._target_combo.currentIndexChanged.connect(self._on_target_changed)

        self._hotkey_field = HotkeyCaptureField(config["hotkey"], self)
        self._hotkey_field.hotkey_captured.connect(self._on_hotkey_captured)

        form = QFormLayout()
        form.addRow("Source language", self._source_combo)
        form.addRow("Target language", self._target_combo)
        form.addRow("Global hotkey", self._hotkey_field)

        layout = QVBoxLayout(self)
        layout.addLayout(form)

    @staticmethod
    def _set_combo_value(combo: QComboBox, code: str) -> None:
        index = combo.findData(code)
        if index != -1:
            combo.setCurrentIndex(index)

    def _on_source_changed(self) -> None:
        config = load_config()
        config["source_lang"] = self._source_combo.currentData()
        save_config(config)

    def _on_target_changed(self) -> None:
        config = load_config()
        config["target_lang"] = self._target_combo.currentData()
        save_config(config)

    def _on_hotkey_captured(self, hotkey: str) -> None:
        self._hotkey_field.set_current(hotkey)
        config = load_config()
        config["hotkey"] = hotkey
        save_config(config)
        self._hotkey_listener.set_hotkey(hotkey)

    def open(self) -> None:
        config = load_config()
        self._set_combo_value(self._source_combo, config["source_lang"])
        self._set_combo_value(self._target_combo, config["target_lang"])
        self._hotkey_field.set_current(config["hotkey"])

        self.show()
        self.activateWindow()
        self.raise_()
