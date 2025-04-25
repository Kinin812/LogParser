from reports import HandlersBaseReport


def test_handlers_report_output():
    stats = {
        "/api/v1/items/": {"INFO": 3, "ERROR": 2},
        "/api/v1/users/": {"INFO": 1}
    }

    report = HandlersBaseReport(stats)
    output = report.generate()

    assert "HANDLER" in output
    assert "/api/v1/items/" in output
    assert "Total requests: 6" in output
    assert "ERROR" in output