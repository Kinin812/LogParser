from collections import defaultdict
from dataclasses import dataclass
from io import StringIO
from typing import TypeVar

from core.base import BaseReport, BaseLineParser, LogRecord, BaseStatsCollector

T = TypeVar("T", bound=LogRecord)


@dataclass
class HandlersLogRecord(LogRecord):
    """
    Расширение базового класса LogRecord для хранения данных о логах,
    специфичных для отчёта.
    """

    logger: str
    message: str
    handler: str | None


class HandlersCollector(BaseStatsCollector):
    """
    Класс для сбора статистики по лог-записям.
    """

    def add_record(self, record: HandlersLogRecord):
        """
        Добавляет запись в статистику, если она подходит по условиям.
        """
        if record.logger != "django.request":
            return
        if not record.handler:
            return
        self.stats[record.handler][record.level] += 1

    def merge(self, stats_list):
        """
        Объединяет список статистик в одну.
        """
        merged = defaultdict(lambda: defaultdict(int))

        for stat in stats_list:
            for handler, level_counts in stat.items():
                for level, count in level_counts.items():
                    merged[handler][level] += count

        return dict(merged)


class HandlersParser(BaseLineParser):
    """
    Парсер для обработки строк логов и преобразования их в объект HandlersLogRecord.
    """

    def parse_line(self, line: str) -> HandlersLogRecord | None:
        """
        Разбирает строку лога и возвращает объект HandlersLogRecord с извлечёнными данными.
        """
        parts = line.split()
        if len(parts) < 5:
            return None

        try:
            timestamp = f"{parts[0]} {parts[1]}"
            level = parts[2]
            logger = parts[3].rstrip(":")

            if logger != "django.request":
                return None

            message = " ".join(parts[4:])
            handler = next((p for p in parts if p.startswith("/")), None)

            return HandlersLogRecord(
                timestamp=timestamp,
                level=level,
                logger=logger,
                message=message,
                handler=handler,
            )
        except ValueError:
            return None
        except Exception as e:
            print(f"Error parsing line: {e}")
            return None


class HandlersReport(BaseReport):
    """
    Отчёт по количеству запросов на каждый хендлер Django-приложения с разбивкой по уровням логов.
    """

    PARSER = HandlersParser
    COLLECTOR = HandlersCollector

    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def generate(self) -> str:
        """
        Генерирует текстовый отчёт о количестве логов по хендлерам и уровням.
        """
        buf = StringIO()

        total_requests = sum(sum(lv.values()) for lv in self.stats.values())
        buf.write(f"Total requests: {total_requests}\n\n")
        buf.write(f"{'HANDLER':<24}\t" + "\t".join(self.LEVELS) + "\n")

        for handler in sorted(self.stats):
            counts = [str(self.stats[handler].get(level, 0)) for level in self.LEVELS]
            buf.write(f"{handler:<24}\t" + "\t".join(counts) + "\n")

        total_by_level = [
            sum(self.stats[h].get(level, 0) for h in self.stats)
            for level in self.LEVELS
        ]
        buf.write(" " * 24 + "\t" + "\t".join(str(c) for c in total_by_level) + "\n")

        return buf.getvalue()

    def print(self):
        """
        Печатает сгенерированный отчёт в консоль.
        """
        print(self.generate())
