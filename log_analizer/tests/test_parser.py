from pathlib import Path

import pytest

from log_analizer.core.base import BaseLineParser, LogRecord
from log_analizer.core.parser import LogParser


# Фейковый парсер для теста
class DummyLineParser(BaseLineParser):
    def parse_line(self, line: str) -> LogRecord | None:
        line = line.strip()
        if not line:
            return None
        return LogRecord(timestamp="2024-01-01 00:00:00", level="INFO")


@pytest.fixture
def sample_log_file(tmp_path: Path) -> Path:
    log_content = "First log line\n\nSecond log line\nThird log line\n"
    log_file = tmp_path / "test.log"
    log_file.write_text(log_content)
    return log_file


def test_log_parser_parses_non_empty_lines(sample_log_file):
    parser = LogParser(sample_log_file, DummyLineParser())
    records = parser.parse()

    assert len(records) == 3
    for record in records:
        assert isinstance(record, LogRecord)
        assert record.timestamp == "2024-01-01 00:00:00"
        assert record.level == "INFO"


def test_log_parser_empty_file(tmp_path: Path):
    empty_log = tmp_path / "empty.log"
    empty_log.write_text("")  # Создаем пустой файл

    parser = LogParser(empty_log, DummyLineParser())
    records = parser.parse()

    assert records == []
