"""LogManager module for jk2bt project.

Provides a unified LogManager singleton as the single entry point for all
logging operations, tying together config, handlers, formatters, adapters,
and stats modules.
"""

import logging
import threading

from .adapters import JQLogAdapter
from .config import LoggingConfig, apply_config, get_default_config
from .stats import StatsCollector, get_stats_collector

__all__ = [
    "LogManager",
    "setup_logging",
    "get_logger",
    "get_jq_log",
    "get_default_logger",
]


class LogManager:
    """Unified logging manager (singleton).

    Serves as the single entry point for all logging operations in jk2bt.
    """

    _instance = None
    _init_lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._init_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._config = None
        self._stats_collector = None
        self._initialized = True

    @classmethod
    def get_instance(cls) -> "LogManager":
        return cls()

    def initialize(self, config: LoggingConfig = None):
        """Initialize the logging system.

        Args:
            config: LoggingConfig instance. Uses default config if None.
        """
        if config is None:
            config = get_default_config()
        apply_config(config)
        self._config = config
        self._stats_collector = get_stats_collector()

    def get_jq_adapter(self, strategy=None, logger_name="jk2bt") -> JQLogAdapter:
        """Create and return a JQLogAdapter.

        Args:
            strategy: optional strategy instance for log forwarding
            logger_name: name for the underlying Python logger

        Returns:
            JQLogAdapter instance
        """
        return JQLogAdapter(strategy=strategy, logger_name=logger_name)

    def get_logger(self, name=None) -> logging.Logger:
        """Return a standard Python logger.

        Args:
            name: logger name. Defaults to "jk2bt".

        Returns:
            logging.Logger instance
        """
        return logging.getLogger(name or "jk2bt")

    def get_stats_collector(self) -> StatsCollector:
        """Return the StatsCollector instance.

        Returns:
            StatsCollector instance
        """
        return self._stats_collector

    def shutdown(self):
        """Shut down the logging system.

        Logs stats summary and closes all handlers on the root logger.
        """
        if self._stats_collector:
            self._stats_collector.log_summary()
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            try:
                handler.close()
                root_logger.removeHandler(handler)
            except Exception:
                pass

    def reset(self):
        """Reset the logging manager to initial state."""
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        if self._stats_collector:
            self._stats_collector.reset()
        self._config = None


def setup_logging(
    level: str = "INFO",
    log_file: str = None,
    format: str = "standard",
    force: bool = False,
) -> LogManager:
    """Convenience function to set up logging.

    Args:
        level: log level string (e.g. "INFO", "DEBUG")
        log_file: path to log file. None to disable file logging.
        format: format style ("standard", "detailed", etc.)
        force: if True, clear existing handlers first

    Returns:
        LogManager instance
    """
    if force:
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

    config = LoggingConfig(level=level, log_file=log_file, format=format)
    manager = LogManager.get_instance()
    manager.initialize(config)
    return manager


def get_logger(name: str = None) -> logging.Logger:
    """Convenience function to get a logger.

    Args:
        name: logger name. Defaults to "jk2bt".

    Returns:
        logging.Logger instance
    """
    return LogManager.get_instance().get_logger(name)


def get_jq_log(strategy=None, logger_name: str = "jk2bt") -> JQLogAdapter:
    """Convenience function to get a JQLogAdapter.

    Args:
        strategy: optional strategy instance for log forwarding
        logger_name: name for the underlying Python logger

    Returns:
        JQLogAdapter instance
    """
    return LogManager.get_instance().get_jq_adapter(
        strategy=strategy, logger_name=logger_name
    )


def get_default_logger() -> logging.Logger:
    """Convenience function to get the default logger.

    Returns:
        logging.Logger instance (named 'jk2bt')
    """
    return LogManager.get_instance().get_logger("jk2bt")
