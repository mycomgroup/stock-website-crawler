"""Logging configuration module for jk2bt project.

Provides unified logging configuration via dataclass, environment variables,
and dict-based loading.
"""

import logging
import os
from dataclasses import dataclass

from .formatters import get_formatter
from .handlers import create_rotating_file_handler

__all__ = [
    "LoggingConfig",
    "apply_config",
    "get_default_config",
]


@dataclass
class LoggingConfig:
    """Logging configuration dataclass."""

    level: str = "INFO"
    log_file: str = "logs/jk2bt.log"
    format: str = "standard"
    max_bytes: int = 10 * 1024 * 1024
    backup_count: int = 5
    suppress_third_party: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "LoggingConfig":
        """Create LoggingConfig from a dictionary."""
        valid_fields = {
            "level",
            "log_file",
            "format",
            "max_bytes",
            "backup_count",
            "suppress_third_party",
        }
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)


def apply_config(config: LoggingConfig) -> logging.Logger:
    """Apply logging configuration to the root logger.

    Args:
        config: LoggingConfig instance.

    Returns:
        The configured root logger.
    """
    log_level = getattr(logging, config.level.upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if not root_logger.handlers:
        formatter = get_formatter(config.format)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        if config.log_file:
            file_handler = create_rotating_file_handler(
                config.log_file,
                max_bytes=config.max_bytes,
                backup_count=config.backup_count,
                level=config.level,
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

    if config.suppress_third_party:
        for logger_name in ("matplotlib", "PIL", "urllib3", "requests"):
            logging.getLogger(logger_name).setLevel(logging.WARNING)

    return root_logger


def get_default_config() -> LoggingConfig:
    """Get default logging configuration, optionally overridden by environment variables.

    Reads JK2BT_LOG_LEVEL and JK2BT_LOG_FILE environment variables.

    Returns:
        LoggingConfig with defaults or env overrides.
    """
    return LoggingConfig(
        level=os.environ.get("JK2BT_LOG_LEVEL", "INFO"),
        log_file=os.environ.get("JK2BT_LOG_FILE", "logs/jk2bt.log"),
    )
