"""Log formatters for jk2bt project.

Provides unified formatting classes and constants for consistent log output.
"""

import json
import logging
from datetime import datetime, timezone

__all__ = [
    "STANDARD_FORMAT",
    "SIMPLE_FORMAT",
    "STRATEGY_FORMAT",
    "StandardFormatter",
    "JSONFormatter",
    "get_formatter",
]

STANDARD_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
SIMPLE_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
STRATEGY_FORMAT = "%(asctime)s - %(message)s"


class StandardFormatter(logging.Formatter):
    """Standard log formatter using predefined format constants."""

    def __init__(self, fmt=None):
        super().__init__(fmt or STANDARD_FORMAT)


class JSONFormatter(logging.Formatter):
    """JSON log formatter outputting structured log records."""

    def format(self, record):
        log_data = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0] is not None:
            log_data["exception"] = self.formatException(record.exc_info)
        try:
            return json.dumps(log_data)
        except (TypeError, ValueError):
            log_data["message"] = str(log_data["message"])
            return json.dumps(log_data)


def get_formatter(format_type="standard"):
    """Return a formatter based on the specified format type.

    Args:
        format_type: One of "standard", "simple", "json", "strategy".

    Returns:
        A logging.Formatter instance.

    Raises:
        ValueError: If format_type is not supported.
    """
    formatters = {
        "standard": lambda: StandardFormatter(),
        "simple": lambda: logging.Formatter(SIMPLE_FORMAT),
        "json": lambda: JSONFormatter(),
        "strategy": lambda: logging.Formatter(STRATEGY_FORMAT),
    }
    if format_type not in formatters:
        raise ValueError(
            f"Unsupported format type: {format_type}. Choose from {list(formatters.keys())}"
        )
    return formatters[format_type]()
