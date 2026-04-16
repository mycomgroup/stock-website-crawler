"""
adapters.py
Unified JQLogAdapter for jk2bt project.

Merges the two existing implementations:
- jk2bt/utils/logging_config.py (standard Python logging)
- jk2bt/core/global_state.py (strategy-aware forwarding)

Supports both modes:
- With strategy: forwards to strategy.log()
- Without strategy: uses standard Python logging
"""

import logging
import pandas as pd


class JQLogAdapter:
    """Unified JoinQuant-style log adapter.

    Supports multi-argument logging, DataFrame/Series pretty-printing,
    kwargs as key=value pairs, and optional strategy forwarding.
    """

    def __init__(self, strategy=None, logger_name="jk2bt"):
        self._strategy = strategy
        self._logger = logging.getLogger(logger_name)
        self._log_levels = {
            "order": "info",
            "trade": "info",
            "debug": "info",
        }

    def info(self, *args, **kwargs):
        msg = self._format_message(args, kwargs)
        self._dispatch("info", msg)

    def warn(self, *args, **kwargs):
        msg = self._format_message(args, kwargs)
        self._dispatch("warn", msg)

    def warning(self, *args, **kwargs):
        msg = self._format_message(args, kwargs)
        self._dispatch("warn", msg)

    def error(self, *args, **kwargs):
        msg = self._format_message(args, kwargs)
        self._dispatch("error", msg)

    def debug(self, *args, **kwargs):
        level = self._log_levels.get("debug", "info")
        if level == "debug":
            msg = self._format_message(args, kwargs)
            self._dispatch("debug", msg)

    def critical(self, *args, **kwargs):
        msg = self._format_message(args, kwargs)
        self._dispatch("critical", msg)

    def set_level(self, module, level):
        """Set per-module log level.

        Args:
            module: one of "order", "trade", "debug"
            level: log level string
        """
        self._log_levels[module] = level

    def _dispatch(self, method, msg):
        if self._strategy is not None:
            prefix = ""
            if method == "warn":
                prefix = "[WARN] "
            elif method == "error":
                prefix = "[ERROR] "
            elif method == "debug":
                prefix = "[DEBUG] "
            self._strategy.log(f"{prefix}{msg}")
        else:
            log_method = getattr(
                self._logger, method if method != "warn" else "warning", None
            )
            if log_method is None:
                log_method = self._logger.info
            log_method(msg)

    def _format_message(self, args, kwargs):
        parts = []
        for arg in args:
            if isinstance(arg, (pd.DataFrame, pd.Series)):
                parts.append("\n" + str(arg))
            else:
                parts.append(str(arg))
        msg = " ".join(parts)
        if kwargs:
            kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
            msg = f"{msg} {kwargs_str}" if msg else kwargs_str
        return msg


def create_jq_log_adapter(strategy=None, logger_name="jk2bt") -> JQLogAdapter:
    """Create a JQLogAdapter instance.

    Args:
        strategy: optional strategy instance for log forwarding
        logger_name: name for the underlying Python logger

    Returns:
        JQLogAdapter instance
    """
    return JQLogAdapter(strategy=strategy, logger_name=logger_name)


__all__ = [
    "JQLogAdapter",
    "create_jq_log_adapter",
]
