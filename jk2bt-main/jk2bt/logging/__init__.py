"""Logging module for jk2bt.

Provides configurable logging with rotating file handlers,
custom formatters, request/cache statistics, and JoinQuant adapter.
"""

from .adapters import JQLogAdapter, create_jq_log_adapter
from .config import LoggingConfig, apply_config, get_default_config
from .formatters import (
    STANDARD_FORMAT,
    SIMPLE_FORMAT,
    STRATEGY_FORMAT,
    StandardFormatter,
    JSONFormatter,
    get_formatter,
)
from .handlers import (
    create_rotating_file_handler,
    create_timed_rotating_file_handler,
    create_strategy_log_file,
    close_handler_safely,
)
from .stats import (
    RequestStats,
    CacheStats,
    StatsCollector,
    get_stats_collector,
    reset_stats_collector,
)
from .manager import LogManager, setup_logging, get_logger, get_jq_log

__all__ = [
    # adapters
    "JQLogAdapter",
    "create_jq_log_adapter",
    # config
    "LoggingConfig",
    "apply_config",
    "get_default_config",
    # formatters
    "STANDARD_FORMAT",
    "SIMPLE_FORMAT",
    "STRATEGY_FORMAT",
    "StandardFormatter",
    "JSONFormatter",
    "get_formatter",
    # handlers
    "create_rotating_file_handler",
    "create_timed_rotating_file_handler",
    "create_strategy_log_file",
    "close_handler_safely",
    # stats
    "RequestStats",
    "CacheStats",
    "StatsCollector",
    "get_stats_collector",
    "reset_stats_collector",
    # manager
    "LogManager",
    "setup_logging",
    "get_logger",
    "get_jq_log",
]
