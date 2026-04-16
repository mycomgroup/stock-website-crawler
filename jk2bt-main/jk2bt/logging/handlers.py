"""Log handler factory functions for the jk2bt project."""

import logging
import logging.handlers

__all__ = [
    "create_rotating_file_handler",
    "create_timed_rotating_file_handler",
    "create_strategy_log_file",
    "close_handler_safely",
]


def create_rotating_file_handler(
    log_file, max_bytes=10 * 1024 * 1024, backup_count=5, level="INFO"
):
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    handler.setLevel(getattr(logging, level.upper()))
    return handler


def create_timed_rotating_file_handler(
    log_file, when="midnight", backup_count=7, level="INFO"
):
    handler = logging.handlers.TimedRotatingFileHandler(
        log_file, when=when, backupCount=backup_count, encoding="utf-8"
    )
    handler.setLevel(getattr(logging, level.upper()))
    return handler


def create_strategy_log_file(filepath, mode="a"):
    handler = logging.FileHandler(filepath, mode=mode, encoding="utf-8")
    handler.setLevel(logging.INFO)
    return handler


def close_handler_safely(handler):
    if handler is not None and hasattr(handler, "close"):
        handler.close()
