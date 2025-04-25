from core.base import BaseReport
from io import StringIO

class HandlersBaseReport(BaseReport):
    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def generate(self) -> str:
        buf = StringIO()

        total_requests = sum(sum(lv.values()) for lv in self.stats.values())
        buf.write(f"Total requests: {total_requests}\n\n")
        buf.write(f"{'HANDLER':<24}\t" + "\t".join(self.LEVELS) + "\n")

        for handler in sorted(self.stats):
            counts = [str(self.stats[handler].get(level, 0)) for level in self.LEVELS]
            buf.write(f"{handler:<24}\t" + "\t".join(counts) + "\n")

        total_by_level = [sum(self.stats[h].get(level, 0) for h in self.stats) for level in self.LEVELS]
        buf.write(" " * 24 + "\t" + "\t".join(str(c) for c in total_by_level) + "\n")

        return buf.getvalue()

    def print(self):
        print(self.generate())