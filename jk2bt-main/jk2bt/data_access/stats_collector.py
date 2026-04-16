"""
stats_collector.py - DEPRECATED

This module has been moved to jk2bt.logging.stats.
This file exists for backward compatibility only and will be removed in a future release.
"""

import warnings

warnings.warn(
    "jk2bt.data_access.stats_collector is deprecated, use jk2bt.logging.stats instead",
    DeprecationWarning,
    stacklevel=2,
)

from jk2bt.logging.stats import (
    RequestStats,
    CacheStats,
    StatsCollector,
    get_stats_collector,
    reset_stats_collector,
)

__all__ = [
    "RequestStats",
    "CacheStats",
    "StatsCollector",
    "get_stats_collector",
    "reset_stats_collector",
]
