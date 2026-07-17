from PySide6.QtCore import QThread, Signal

from .engine import TranslationError, translate


class TranslationWorker(QThread):
    finished_ok = Signal(str)
    finished_error = Signal(str)

    def __init__(self, text: str):
        super().__init__()
        self._text = text

    def run(self) -> None:
        try:
            result = translate(self._text)
        except TranslationError as e:
            self.finished_error.emit(str(e))
        else:
            self.finished_ok.emit(result)
