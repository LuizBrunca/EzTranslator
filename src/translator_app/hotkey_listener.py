from pynput import keyboard
from PySide6.QtCore import QObject, Signal

DEFAULT_HOTKEY = '<ctrl>+<alt>+t'


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
