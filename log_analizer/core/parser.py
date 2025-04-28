from pathlib import Path
from typing import TypeVar

from .base import BaseLineParser, LogRecord

T = TypeVar("T", bound=LogRecord)


class LogParser:
    """
    Класс для парсинга лог-файлов.
    """

    def __init__(self, path: Path, line_parser: BaseLineParser):
        self.path = path
        self.line_parser = line_parser

    def parse(self) -> list[T]:
        """
        Парсит лог-файл, возвращая список объектов LogRecord.
        """
        records = []

        with open(self.path, "r") as file:
            for line in file:
                record = self.line_parser.parse_line(line)
                if record:
                    records.append(record)

        return records
