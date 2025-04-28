from pathlib import Path

import pytest

from log_analizer.core.base import BaseLineParser, BaseLogRecord
from log_analizer.core.parser import LogParser


class DummyLineParser(BaseLineParser):
    """
    Парсит строку, возвращая LogRecord с фиксированным timestamp и уровнем логирования.
    """

    def parse_line(self, line: str) -> BaseLogRecord | None:
        line = line.strip()
        if not line:
            return None
        return BaseLogRecord(timestamp="2024-01-01 00:00:00", level="INFO")


@pytest.fixture
def sample_log_file(tmp_path: Path) -> Path:
    """
    Создает тестовый лог-файл с несколькими строками.
    """
    log_content = "First log line\n\nSecond log line\nThird log line\n"
    log_file = tmp_path / "test.log"
    log_file.write_text(log_content)
    return log_file


def test_log_parser_parses_non_empty_lines(sample_log_file):
    """
    Проверяет правильность парсинга непустых строк лога.
    """
    parser = LogParser(sample_log_file, DummyLineParser())
    records = parser.parse()

    assert len(records) == 3
    for record in records:
        assert isinstance(record, BaseLogRecord)
        assert record.timestamp == "2024-01-01 00:00:00"
        assert record.level == "INFO"


def test_log_parser_empty_file(tmp_path: Path):
    """
    Проверяет, что парсер возвращает пустой список для пустого файла.
    """
    empty_log = tmp_path / "empty.log"
    empty_log.write_text("")

    parser = LogParser(empty_log, DummyLineParser())
    records = parser.parse()

    assert records == []
