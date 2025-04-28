import concurrent.futures
from pathlib import Path
from typing import TypeVar, Callable, Any

from reports.plugins import ALL_REPORTS
from .base import BaseStatsCollector
from .parser import LogParser

T = TypeVar("T", bound=BaseStatsCollector)
V = TypeVar("V", bound=LogParser)


class LogProcessor:
    """
    Класс для обработки лог-файлов.
    """

    def __init__(
            self,
            log_files: list[Path],
            parser_cls: Callable[[], V],
            collector_cls: Callable[[], T],
    ):
        self.log_files = log_files
        self.parser_cls = parser_cls
        self.collector_cls = collector_cls

    def parse_log(self, path: Path) -> dict[str, Any]:
        """
        Парсит один лог-файл и собирает статистику.
        """
        parser = self.parser_cls()
        log_parser = LogParser(path, parser)
        try:
            records = log_parser.parse()
            collector = self.collector_cls()
            return collector.collect(records)
        except Exception as e:
            print(f"Error processing {path}: {e}")
            return {}

    def process_logs(self) -> list[dict[str, Any]]:
        """
        Обрабатывает все лог-файлы, парсит их и собирает статистику с использованием параллельной обработки.
        """
        with concurrent.futures.ProcessPoolExecutor() as executor:
            return list(executor.map(self.parse_log, self.log_files))


class ReportGenerator:
    """
    Класс для генерации отчета по лог-файлам.
    """

    def __init__(self, report_name: str, log_files: list[Path]):
        self.report_name = report_name
        self.log_files = log_files

    def generate_report(self) -> BaseStatsCollector:
        """
        Генерирует отчет на основе лог-файлов и выбранного парсера.
        """
        report_cls = ALL_REPORTS.get(self.report_name)
        if not report_cls:
            raise ValueError(f"Unsupported report type: {self.report_name}")

        log_processor = LogProcessor(
            log_files=self.log_files,
            parser_cls=report_cls.PARSER,
            collector_cls=report_cls.COLLECTOR,
        )
        all_stats = log_processor.process_logs()
        collector = report_cls.COLLECTOR()
        merged_stats = collector.merge(stats_list=all_stats)

        return report_cls(merged_stats)


def get_report(name: str, log_files: list[Path]) -> BaseStatsCollector:
    """
    Получает и генерирует отчет по указанным лог-файлам.
    """
    return ReportGenerator(name, log_files).generate_report()
