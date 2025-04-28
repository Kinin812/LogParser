import pytest

from log_analizer.reports.plugins.django_handlers import (
    HandlersCollector,
    HandlersBaseLogRecord,
    Handlers,
    HandlersParser,
)


@pytest.fixture
def parser():
    """
    Возвращает экземпляр парсера для обработки строк логов.
    """
    return HandlersParser()


def test_parse_valid_django_request(parser):
    """
    Тестирует парсинг корректной строки с запросом.
    """
    line = "2024-04-28 10:00:00 INFO django.request: GET /api/v1/items/ HTTP/1.1"
    record = parser.parse_line(line)

    assert isinstance(record, HandlersBaseLogRecord)
    assert record.timestamp == "2024-04-28 10:00:00"
    assert record.level == "INFO"
    assert record.logger == "django.request"
    assert record.handler == "/api/v1/items/"


def test_parse_other_logger_returns_none(parser):
    """
    Проверяет, что строка с неверным логгером возвращает None.
    """
    line = "2024-04-28 10:00:00 ERROR other.logger: Something went wrong"
    record = parser.parse_line(line)

    assert record is None


def test_parse_incomplete_line_returns_none(parser):
    """
    Проверяет, что неполная строка возвращает None.
    """
    line = "Too short"
    record = parser.parse_line(line)

    assert record is None


@pytest.fixture
def collector():
    """
    Возвращает экземпляр коллектора для статистики обработанных записей.
    """
    return HandlersCollector()


def test_add_valid_record(collector):
    """
    Проверяет, что запись с правильными данными добавляется в статистику.
    """
    record = HandlersBaseLogRecord(
        timestamp="2024-04-28 10:00:00",
        level="INFO",
        logger="django.request",
        message="GET /api/v1/products/ HTTP/1.1",
        handler="/api/v1/products/",
    )
    collector.add_record(record)

    assert collector.stats["/api/v1/products/"]["INFO"] == 1


def test_ignore_record_with_wrong_logger(collector):
    """
    Проверяет, что запись с логгером "django.security" не добавляется в статистику.
    """
    record = HandlersBaseLogRecord(
        timestamp="2024-04-28 10:00:00",
        level="ERROR",
        logger="django.security",
        message="Permission denied",
        handler="/api/v1/login/",
    )
    collector.add_record(record)

    assert collector.stats == {}


def test_ignore_record_without_handler(collector):
    """
    Проверяет, что запись без значения handler не добавляется в статистику.
    """
    record = HandlersBaseLogRecord(
        timestamp="2024-04-28 10:00:00",
        level="WARNING",
        logger="django.request",
        message="Some message",
        handler=None,
    )
    collector.add_record(record)

    assert collector.stats == {}


def test_merge_multiple_stats():
    """
    Проверяет, что несколько наборов статистик сливаются правильно.
    """
    collector = HandlersCollector()

    stats_list = [
        {"/api/v1/products/": {"INFO": 2, "ERROR": 1}},
        {"/api/v1/products/": {"INFO": 3}, "/api/v1/orders/": {"WARNING": 1}},
    ]

    merged = collector.merge(stats_list)

    assert merged["/api/v1/products/"]["INFO"] == 5
    assert merged["/api/v1/products/"]["ERROR"] == 1
    assert merged["/api/v1/orders/"]["WARNING"] == 1


def test_generate_report_output():
    """
    Проверяет, что отчет правильно генерирует информацию о запросах и уровнях логирования.
    """
    stats = {
        "/api/v1/products/": {"INFO": 5, "ERROR": 2},
        "/api/v1/orders/": {"WARNING": 1},
    }
    report = Handlers(stats)
    text = report.generate()

    assert "Total requests: 8" in text
    assert "/api/v1/products/" in text
    assert "/api/v1/orders/" in text
    assert "INFO" in text
    assert "ERROR" in text
    assert "WARNING" in text
