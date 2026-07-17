import json
import logging
import os
from logging.handlers import RotatingFileHandler

from .config import LOGS_DIR


class Logger:
    def __init__(self, app, log_name):
        self.app_name = app
        self.logger = logging.getLogger(app)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(message)s]')

        if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        log_dir = os.path.join(LOGS_DIR, log_name)
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f'{log_name}.log')

        if not any(isinstance(h, RotatingFileHandler) for h in self.logger.handlers):
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,  # 5 MB
                backupCount=5,  # Quantidade de arquivos de backup antes de sobrescrever os antigos
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self.nivel_info = 'INFO'
        self.nivel_erro = 'ERRO'

    def _log(self, tipo, nivel, log):
        if isinstance(log, dict):
            log = json.dumps(log, ensure_ascii=False)
        elif isinstance(log, list):
            log = json.dumps(log, ensure_ascii=False)

        msg = f"{tipo} | {log}"

        if nivel == 'INFO':
            self.logger.info(msg)
        elif nivel == 'ERRO':
            self.logger.error(msg)
        else:
            self.logger.warning(msg)

    def info(self, tipo, log):
        self._log(tipo, self.nivel_info, log)

    def erro(self, tipo, log):
        self._log(tipo, self.nivel_erro, log)
