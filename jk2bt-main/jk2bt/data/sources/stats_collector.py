"""
stats_collector.py - 数据源统计收集器 (stub)

Minimal stub to satisfy imports. Full implementation can be added later.
"""


class StatsCollector:
    """Minimal stats collector stub."""

    def record_call(self, *args, **kwargs):
        pass

    def record_request(self, *args, **kwargs):
        pass

    def record_cache_hit(self, *args, **kwargs):
        pass

    def record_cache_miss(self, *args, **kwargs):
        pass

    def get_stats(self):
        return {}


_instance = None


def get_stats_collector():
    global _instance
    if _instance is None:
        _instance = StatsCollector()
    return _instance
