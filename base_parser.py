from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

from models import Strategy

LogFn = Callable[[str], None]


class BaseStrategyParser(ABC):
    def __init__(self, log: LogFn):
        self.log = log

    @abstractmethod
    def parse(self, file_path: str) -> list[Strategy]:
        raise NotImplementedError
