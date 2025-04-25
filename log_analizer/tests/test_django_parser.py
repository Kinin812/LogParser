import pytest
from core.django_parser import DjangoRequestParser
from core.base import LogRecord


@pytest.fixture
def parser():
    return DjangoRequestParser()


def test_parse_valid_line(parser):
    line = "2024-04-25 12:34:56 INFO django.request: GET /api/v1/items/ HTTP/1.1"
    record = parser.parse_line(line)
    assert isinstance(record, LogRecord)
    assert record.handler == "/api/v1/items/"


def test_parse_invalid_logger(parser):
    line = "2024-04-25 12:34:56 INFO other.logger: Some message"
    assert parser.parse_line(line) is None


def test_parse_malformed_line(parser):
    line = "malformed log line without enough parts"
    assert parser.parse_line(line) is None