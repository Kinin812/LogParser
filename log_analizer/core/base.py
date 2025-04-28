from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import TypeVar


@dataclass
class LogRecord:
    """
    Класс для представления записи лога.
    """

    timestamp: str
    level: str


class BaseLineParser(ABC):
    """
    Абстрактный класс для парсера строк лога.
    """

    T = TypeVar("T", bound=LogRecord)

    @abstractmethod
    def parse_line(self, line: str) -> T | None:
        """
        Абстрактный метод для парсинга строки лога.
        """
        pass


class BaseParser(ABC):
    """
    Абстрактный класс для парсера логов.
    """

    @abstractmethod
    def parse(self, log_file):
        """
        Абстрактный метод для парсинга лог-файла.
        """
        raise NotImplementedError


class BaseReport(ABC):
    """
    Абстрактный класс для отчетов.
    """

    def __init__(self, stats):
        """
        Инициализирует отчет.
        """
        self.stats = stats

    @abstractmethod
    def generate(self):
        """
        Генерирует отчет.
        """
        pass

    @abstractmethod
    def print(self):
        """
        Печатает отчет.
        """
        pass


class BaseStatsCollector(ABC):
    """
    Абстрактный класс для сбора статистики по лог-записям.
    """

    T = TypeVar("T", bound=LogRecord)

    def __init__(self):
        self.stats = defaultdict(lambda: defaultdict(int))

    @abstractmethod
    def add_record(self, record: T):
        """
        Добавляет запись в статистику, если она подходит по условиям.
        """
        pass

    def collect(self, records: list[T]) -> dict[str, dict[str, int]]:
        """
        Обрабатывает список лог-записей и возвращает готовую статистику.
        """
        for record in records:
            self.add_record(record)
        return dict(self.stats)

    @abstractmethod
    def merge(self, stats_list: list):
        """
        Объединяет список статистик в одну.
        """
        pass
