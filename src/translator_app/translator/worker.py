from PySide6.QtCore import QThread, Signal

from .engine import DEFAULT_SOURCE, DEFAULT_TARGET, TranslationError, translate


class TranslationWorker(QThread):
    finished_ok = Signal(str)
    finished_error = Signal(str)

    def __init__(self, text: str, source: str = DEFAULT_SOURCE, target: str = DEFAULT_TARGET):
        super().__init__()
        self._text = text
        self._source = source
        self._target = target

    def run(self) -> None:
        try:
            result = translate(self._text, self._source, self._target)
        except TranslationError as e:
            self.finished_error.emit(str(e))
        else:
            self.finished_ok.emit(result)
