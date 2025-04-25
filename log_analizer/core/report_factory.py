from pathlib import Path
import concurrent.futures

from core.parser import LogParser
from core.django_parser import DjangoRequestParser
from core.stats_collector import collect_stats
from core.stats_merger import StatsMerger
from reports.handlers import HandlersBaseReport


class LogProcessor:
    def __init__(self, log_files: list[Path]):
        self.log_files = log_files
        self.parser = DjangoRequestParser()

    def parse_log(self, path: Path):
        log_parser = LogParser(path, self.parser)
        records = log_parser.parse()
        return collect_stats(records)

    def process_logs(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            return list(executor.map(self.parse_log, self.log_files))


class ReportGenerator:
    def __init__(self, report_name: str, log_files: list[Path]):
        self.report_name = report_name
        self.log_files = log_files

    def generate_report(self):
        log_processor = LogProcessor(self.log_files)
        all_stats = log_processor.process_logs()
        merged_stats = StatsMerger.merge(all_stats)

        if self.report_name == "handlers":
            return HandlersBaseReport(merged_stats)

        raise ValueError(f"Unsupported report type: {self.report_name}")


def get_report(name: str, log_files: list[Path]) -> HandlersBaseReport:
    return ReportGenerator(name, log_files).generate_report()