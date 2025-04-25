from pathlib import Path
from core.base import LogLineParser, LogRecord

class LogParser:
    def __init__(self, path: Path, line_parser: LogLineParser):
        self.path = path
        self.line_parser = line_parser

    def parse(self) -> list[LogRecord]:
        records = []

        with open(self.path, 'r') as file:
            for line in file:
                record = self.line_parser.parse_line(line)
                if record:
                    records.append(record)

        return records