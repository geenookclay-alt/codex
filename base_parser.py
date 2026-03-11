from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable

from models import Strategy


class BaseStrategyParser(ABC):
    def __init__(self, logger: Callable[[str], None]) -> None:
        self.logger = logger

    @abstractmethod
    def parse(self, file_path: Path) -> list[Strategy]:
        raise NotImplementedError
