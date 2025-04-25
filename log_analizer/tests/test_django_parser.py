import pytest
from core.django_parser import DjangoRequestParser
from core.base import LogRecord


def test_parse_line_valid():
    line = "2024-04-24 12:00:00 INFO django.request /api/v1/test HTTP 200"
    parser = DjangoRequestParser()
    record = parser.parse_line(line)

    assert isinstance(record, LogRecord)
    assert record.level == "INFO"
    assert record.logger == "django.request"
    assert record.handler == "/api/v1/test"


def test_parse_line_invalid():
    line = "invalid line without enough parts"
    parser = DjangoRequestParser()
    record = parser.parse_line(line)

    assert record is None