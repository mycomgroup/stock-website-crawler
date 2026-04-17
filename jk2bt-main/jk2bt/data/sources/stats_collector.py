"""
stats_collector.py
兼容层 - 转发到 jk2bt.logging.stats
"""

from jk2bt.logging.stats import (
    StatsCollector,
    get_stats_collector,
    reset_stats_collector,
)

__all__ = ["StatsCollector", "get_stats_collector", "reset_stats_collector"]
