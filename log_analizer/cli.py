import argparse
import sys
from pathlib import Path
from core.report_factory import get_report


class LogAnalyzer:
    def __init__(self, log_files, report_name):
        self.log_files = log_files
        self.report_name = report_name

    def validate_files(self):
        for file_path in self.log_files:
            if not file_path.exists():
                print(f"File not found: {file_path}", file=sys.stderr)
                sys.exit(1)

    def generate_report(self):
        report = get_report(self.report_name, self.log_files)
        return report


class CLI:
    def __init__(self):
        self.args = self.parse_args()
        self.analyzer = LogAnalyzer(self.args.log_files, self.args.report)

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="Analyze Django log files.")
        parser.add_argument("log_files", nargs="+", type=Path, help="Path(s) to log file(s)")
        parser.add_argument("--report", required=True, choices=["handlers"], help="Name of the report to generate")
        return parser.parse_args()

    def run(self):
        self.analyzer.validate_files()
        report = self.analyzer.generate_report()
        report.print()


def main():
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()