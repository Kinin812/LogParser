from pathlib import Path
from unittest.mock import MagicMock

import pytest

from log_analizer.core.base import BaseStatsCollector
from log_analizer.core.parser import LogParser
from log_analizer.core.report_factory import LogProcessor, ReportGenerator


class MockParser(LogParser):
    """
    Моковый парсер для тестирования. Симулирует парсинг строки лога.
    """

    def parse_line(self, line: str):
        return MagicMock(timestamp="2025-01-01 00:00:00", level="INFO")


class MockCollector(BaseStatsCollector):
    """
    Моковый коллектор для тестирования. Собирает статистику по числу записей.
    """

    def __init__(self):
        super().__init__()
        self.stats = {"count": 0}

    def collect(self, records):
        """
        Считает количество записей.
        """
        self.stats["count"] = len(records)
        return self.stats

    def merge(self, stats_list):
        """
        Объединяет статистику из нескольких коллекций.
        """
        merged = {"count": sum(stat["count"] for stat in stats_list)}
        return merged

    def add_record(self, record):
        """
        Добавляет запись в статистику.
        """
        self.stats["count"] += 1


def create_mock_parser():
    """
    Создает экземпляр мокового парсера.
    """
    return MockParser(Path("dummy.log"), MagicMock())


def create_mock_collector():
    """
    Создает экземпляр мокового коллектора.
    """
    return MockCollector()


@pytest.fixture
def log_files(tmp_path: Path):
    """
    Создает тестовые лог-файлы.
    """
    log_file1 = tmp_path / "test1.log"
    log_file2 = tmp_path / "test2.log"
    log_file1.write_text("Line 1\nLine 2\n")
    log_file2.write_text("Line 3\n")
    return [log_file1, log_file2]


def test_log_processor(log_files: list[Path]):
    """
    Проверяет обработку лог-файлов с использованием мокового парсера и коллектора.
    """
    log_processor = LogProcessor(
        log_files=log_files,
        parser_cls=create_mock_parser,
        collector_cls=create_mock_collector,
    )

    result = log_processor.process_logs()

    assert len(result) == 2
    assert result[0]["count"] == 2
    assert result[1]["count"] == 1


def test_report_generator(log_files: list[Path]):
    """
    Проверяет создание отчета с использованием мокового коллектора.
    """
    mock_collector = MagicMock(spec=BaseStatsCollector)
    mock_collector.merge.return_value = {"count": 6}

    report_generator = ReportGenerator("dummy", log_files)
    report_generator.generate_report = MagicMock(return_value=mock_collector)

    report = report_generator.generate_report()

    assert isinstance(report, MagicMock)
    report_generator.generate_report.assert_called()
    assert report.merge.return_value == {"count": 6}
