"""
logging_config.py - DEPRECATED

This module is deprecated. Please import from jk2bt.logging directly.

Usage:
    from jk2bt.logging import setup_logging, get_logger
"""

import warnings

warnings.warn(
    "jk2bt.utils.logging_config is deprecated, use jk2bt.logging instead",
    DeprecationWarning,
    stacklevel=2,
)

from jk2bt.logging import (
    setup_logging,
    get_logger,
    get_jq_log,
    get_default_logger,
    JQLogAdapter,
    LogAdapter,
    create_jq_log_adapter,
)

__all__ = [
    "setup_logging",
    "get_logger",
    "get_jq_log",
    "get_default_logger",
    "JQLogAdapter",
    "LogAdapter",
    "create_jq_log_adapter",
]
