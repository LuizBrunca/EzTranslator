from pynput import mouse
from PySide6.QtCore import QObject, Signal


class GlobalClickListener(QObject):
    """Watches mouse presses anywhere on screen and re-emits them as a Qt
    signal (same thread hop as HotkeyListener). Only meant to run while the
    popup is open, so the global mouse hook isn't installed the rest of the time.
    """

    pressed = Signal()

    def __init__(self):
        super().__init__()
        self._listener: mouse.Listener | None = None

    def start(self) -> None:
        if self._listener is not None:
            return
        self._listener = mouse.Listener(on_click=self._on_click)
        self._listener.daemon = True
        self._listener.start()

    def stop(self) -> None:
        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    def _on_click(self, x, y, button, is_pressed) -> None:
        if is_pressed:
            self.pressed.emit()
