import argparse
import sys
from pathlib import Path

from core.report_factory import get_report
from reports.plugins import ALL_REPORTS, load_plugin_reports

load_plugin_reports()


class LogAnalyzer:
    """
    Класс для анализа логов и генерации отчетов.
    """

    def __init__(self, log_files: list[Path], report_name: str) -> None:
        """
        Инициализирует анализатор логов.
        """
        self.log_files: list[Path] = log_files
        self.report_name: str = report_name

    def validate_files(self) -> None:
        """
        Проверяет существование лог-файлов. Прерывает выполнение при отсутствии файла.
        """
        for file_path in self.log_files:
            if not file_path.exists():
                print(f"File not found: {file_path}", file=sys.stderr)
                sys.exit(1)

    def generate_report(self):
        """
        Генерирует отчет по логам с использованием указанного парсера.
        """
        report = get_report(self.report_name, self.log_files)
        return report


class CLI:
    """
    Класс для обработки аргументов командной строки и выполнения анализа логов.
    """

    def __init__(self) -> None:
        """
        Инициализирует интерфейс командной строки и анализатор.
        """
        self.args = self.parse_args()
        self.analyzer = LogAnalyzer(self.args.log_files, self.args.report)

    @staticmethod
    def parse_args() -> argparse.Namespace:
        """
        Парсит аргументы командной строки.
        """
        parser = argparse.ArgumentParser(description="Analyze log files.")
        parser.add_argument(
            "log_files", nargs="+", type=Path, help="Path(s) to log file(s)"
        )
        parser.add_argument(
            "--report",
            required=True,
            choices=list(ALL_REPORTS.keys()),
            help="Name of the report to generate",
        )
        return parser.parse_args()

    def run(self) -> None:
        """
        Проверяет лог-файлы и генерирует отчет.
        """
        self.analyzer.validate_files()
        report = self.analyzer.generate_report()
        report.print()


def main() -> None:
    """
    Основная функция для запуска анализа логов через CLI.
    """
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
