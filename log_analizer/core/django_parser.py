from core.base import LogLineParser, LogRecord


class DjangoRequestParser(LogLineParser):
    def parse_line(self, line: str) -> LogRecord | None:
        parts = line.split()
        if len(parts) < 5:
            return None

        try:
            timestamp = f"{parts[0]} {parts[1]}"
            level = parts[2]
            logger = parts[3].rstrip(":")

            if logger != "django.request":
                return None

            message = " ".join(parts[4:])
            handler = next((p for p in parts if p.startswith("/")), None)

            return LogRecord(
                timestamp=timestamp,
                level=level,
                logger=logger,
                message=message,
                handler=handler,
            )
        except Exception:
            return None