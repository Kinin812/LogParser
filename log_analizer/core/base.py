from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LogRecord:
    timestamp: str
    level: str
    logger: str
    message: str
    handler: str | None


class LogLineParser(ABC):
    @abstractmethod
    def parse_line(self, line: str) -> LogRecord | None:
        pass


class BaseReport(ABC):
    def __init__(self, stats):
        self.stats = stats

    @abstractmethod
    def print(self):
        pass
