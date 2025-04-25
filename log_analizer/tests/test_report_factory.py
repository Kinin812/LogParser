from core.report_factory import get_report

def test_generate_handlers_report(tmp_path):
    log_content = "2024-04-25 12:34:56 INFO django.request: GET /test HTTP/1.1\n"
    log_file = tmp_path / "app.log"
    log_file.write_text(log_content)

    report = get_report("handlers", [log_file])
    output = report.generate()

    assert "HANDLER" in output
    assert "/test" in output
    assert "Total requests: 1" in output