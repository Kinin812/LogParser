from core.base import BaseReport

class HandlersBaseReport(BaseReport):
    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def print(self):
        print("Total requests:", sum(sum(lv.values()) for lv in self.stats.values()))
        print("\nHANDLER                \t" + "\t".join(self.LEVELS))

        for handler in sorted(self.stats):
            counts = [str(self.stats[handler].get(level, 0)) for level in self.LEVELS]
            print(f"{handler:<24}\t" + "\t".join(counts))

        total_by_level = [sum(self.stats[h].get(level, 0) for h in self.stats) for level in self.LEVELS]
        print(" " * 24 + "\t" + "\t".join(str(c) for c in total_by_level))