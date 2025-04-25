from collections import defaultdict
from core.base import LogRecord

def collect_stats(records: list[LogRecord]) -> dict[str, dict[str, int]]:
    stats = defaultdict(lambda: defaultdict(int))

    for record in records:
        if record.logger != "django.request":
            continue
        if not record.handler:
            continue
        stats[record.handler][record.level] += 1

    return dict(stats)