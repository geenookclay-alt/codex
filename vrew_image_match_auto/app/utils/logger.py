from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal


class QtLogEmitter(QObject):
    log_message = Signal(str)


class QtLogHandler(logging.Handler):
    def __init__(self, emitter: QtLogEmitter) -> None:
        super().__init__()
        self.emitter = emitter

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.emitter.log_message.emit(msg)


def setup_logger(name: str = "vrew_image_match_auto") -> tuple[logging.Logger, QtLogEmitter]:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    emitter = QtLogEmitter()

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        qt_handler = QtLogHandler(emitter)
        qt_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(qt_handler)

    return logger, emitter
