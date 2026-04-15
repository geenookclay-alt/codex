from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from app.utils.logger import setup_logger


def main() -> int:
    app = QApplication(sys.argv)
    logger, emitter = setup_logger()

    window = MainWindow(logger=logger)
    emitter.log_message.connect(window.log_panel.append_log)

    logger.info("Application started.")
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
