from collections import defaultdict

class StatsMerger:
    @staticmethod
    def merge(stats_list):
        merged = defaultdict(lambda: defaultdict(int))

        for stat in stats_list:
            for handler, level_counts in stat.items():
                for level, count in level_counts.items():
                    merged[handler][level] += count

        return dict(merged)