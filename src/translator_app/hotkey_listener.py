from pynput import keyboard
from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QKeySequence

DEFAULT_HOTKEY = '<ctrl>+<alt>+t'

_MODIFIER_MAP = [
    (Qt.KeyboardModifier.ControlModifier, "<ctrl>"),
    (Qt.KeyboardModifier.AltModifier, "<alt>"),
    (Qt.KeyboardModifier.ShiftModifier, "<shift>"),
    (Qt.KeyboardModifier.MetaModifier, "<cmd>"),
]

_MODIFIER_ONLY_KEYS = {
    Qt.Key.Key_Control,
    Qt.Key.Key_Alt,
    Qt.Key.Key_AltGr,
    Qt.Key.Key_Shift,
    Qt.Key.Key_Meta,
}


def qt_event_to_hotkey_string(event) -> str | None:
    """Converts a captured QKeyEvent into pynput's '<ctrl>+<alt>+t' format.

    Returns None if the event is just a modifier being held on its own (not
    a complete combination yet) or has no modifier at all — global hotkeys
    without a modifier would collide with normal typing everywhere.
    """
    key = event.key()
    if key in _MODIFIER_ONLY_KEYS:
        return None

    modifiers = event.modifiers()
    parts = [label for mod, label in _MODIFIER_MAP if modifiers & mod]
    if not parts:
        return None

    key_text = QKeySequence(key).toString().lower()
    if not key_text:
        return None

    parts.append(key_text)
    return "+".join(parts)


class HotkeyListener(QObject):
    """Runs pynput's global hook on its own thread and re-emits it as a Qt
    signal, since GlobalHotKeys fires its callback off the Qt main thread and
    touching widgets from there directly is not safe.
    """

    triggered = Signal()

    def __init__(self, hotkey: str = DEFAULT_HOTKEY):
        super().__init__()
        self._hotkey = hotkey
        self._listener: keyboard.GlobalHotKeys | None = None

    def start(self) -> None:
        self._listener = keyboard.GlobalHotKeys({self._hotkey: self.triggered.emit})
        self._listener.daemon = True
        self._listener.start()

    def stop(self) -> None:
        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    def set_hotkey(self, hotkey: str) -> None:
        self.stop()
        self._hotkey = hotkey
        self.start()
