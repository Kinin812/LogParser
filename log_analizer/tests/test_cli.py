import sys
import pytest
from pathlib import Path
from log_analizer.cli import LogAnalyzer, CLI


class DummyReport:
    def print(self):
        print("Dummy report")


@pytest.fixture
def mock_report(monkeypatch):
    monkeypatch.setattr("log_analizer.cli.get_report", lambda name, files: DummyReport())


def test_validate_files_exists(tmp_path):
    log_file = tmp_path / "log.log"
    log_file.write_text("2024-04-25 INFO django.request: GET /api HTTP/1.1")
    analyzer = LogAnalyzer([log_file], "handlers")
    analyzer.validate_files()  # Не должен упасть


def test_validate_files_not_found():
    analyzer = LogAnalyzer([Path("nonexistent.log")], "handlers")
    with pytest.raises(SystemExit):
        analyzer.validate_files()


def test_generate_report(mock_report, tmp_path):
    log_file = tmp_path / "log.log"
    log_file.write_text("log content")
    analyzer = LogAnalyzer([log_file], "handlers")
    report = analyzer.generate_report()
    assert isinstance(report, DummyReport)


def test_cli_run(monkeypatch, tmp_path, capsys, mock_report):
    log_file = tmp_path / "log.log"
    log_file.write_text("log")
    monkeypatch.setattr(sys, "argv", ["prog", str(log_file), "--report", "handlers"])
    cli = CLI()
    cli.run()
    captured = capsys.readouterr()
    assert "Dummy report" in captured.out


def test_parse_args(monkeypatch, tmp_path):
    log_file = tmp_path / "log.log"
    log_file.write_text("log")
    monkeypatch.setattr(sys, "argv", ["prog", str(log_file), "--report", "handlers"])
    cli = CLI()
    assert cli.args.report == "handlers"
    assert cli.args.log_files == [log_file]