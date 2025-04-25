from core.base import LogRecord


def test_log_record_creation():
    record = LogRecord(
        timestamp="2024-04-25 12:34:56",
        level="INFO",
        logger="django.request",
        message="GET /api/v1/items/ HTTP/1.1",
        handler="/api/v1/items/"
    )
    assert record.timestamp == "2024-04-25 12:34:56"
    assert record.level == "INFO"
    assert record.logger == "django.request"
    assert record.message == "GET /api/v1/items/ HTTP/1.1"
    assert record.handler == "/api/v1/items/"