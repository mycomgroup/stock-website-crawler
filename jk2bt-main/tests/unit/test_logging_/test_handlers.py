"""
Tests for jk2bt/logging/handlers.py - Log Handlers
"""

import pytest
import logging
import tempfile
import os
from jk2bt.logging.handlers import (
    create_rotating_file_handler,
    create_timed_rotating_file_handler,
    create_strategy_log_file,
    close_handler_safely,
)


class TestCreateRotatingFileHandler:
    """Test create_rotating_file_handler function"""

    def test_create_with_defaults(self, tmp_path):
        log_file = tmp_path / "test.log"
        handler = create_rotating_file_handler(str(log_file))

        assert handler is not None
        assert isinstance(handler, logging.handlers.RotatingFileHandler)
        assert handler.maxBytes == 10 * 1024 * 1024
        assert handler.backupCount == 5
        handler.close()

    def test_create_with_custom_params(self, tmp_path):
        log_file = tmp_path / "test.log"
        handler = create_rotating_file_handler(
            str(log_file),
            max_bytes=1024,
            backup_count=3,
            level="DEBUG",
        )

        assert handler.maxBytes == 1024
        assert handler.backupCount == 3
        assert handler.level == logging.DEBUG
        handler.close()

    def test_handler_writes_log(self, tmp_path):
        log_file = tmp_path / "test.log"
        handler = create_rotating_file_handler(str(log_file))
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)

        logger = logging.getLogger("test_rotating")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        logger.info("test message")

        handler.close()
        logger.removeHandler(handler)

        with open(log_file, "r") as f:
            assert "test message" in f.read()


class TestCreateTimedRotatingFileHandler:
    """Test create_timed_rotating_file_handler function"""

    def test_create_with_defaults(self, tmp_path):
        log_file = tmp_path / "test.log"
        handler = create_timed_rotating_file_handler(str(log_file))

        assert handler is not None
        assert isinstance(handler, logging.handlers.TimedRotatingFileHandler)
        assert handler.when == "midnight"
        assert handler.backupCount == 7
        handler.close()

    def test_create_with_custom_params(self, tmp_path):
        log_file = tmp_path / "test.log"
        handler = create_timed_rotating_file_handler(
            str(log_file),
            when="H",
            backup_count=10,
            level="WARNING",
        )

        assert handler.when == "H"
        assert handler.backupCount == 10
        assert handler.level == logging.WARNING
        handler.close()


class TestCreateStrategyLogFile:
    """Test create_strategy_log_file function"""

    def test_create_with_defaults(self, tmp_path):
        log_file = tmp_path / "strategy.log"
        handler = create_strategy_log_file(str(log_file))

        assert handler is not None
        assert isinstance(handler, logging.FileHandler)
        assert handler.level == logging.INFO
        handler.close()

    def test_create_append_mode(self, tmp_path):
        log_file = tmp_path / "strategy.log"

        handler1 = create_strategy_log_file(str(log_file), mode="w")
        handler1.setFormatter(logging.Formatter("%(message)s"))
        logging.getLogger("test_strategy").addHandler(handler1)
        logging.getLogger("test_strategy").info("first")
        handler1.close()

        handler2 = create_strategy_log_file(str(log_file), mode="a")
        handler2.setFormatter(logging.Formatter("%(message)s"))
        logging.getLogger("test_strategy").addHandler(handler2)
        logging.getLogger("test_strategy").info("second")
        handler2.close()

        with open(log_file, "r") as f:
            content = f.read()
            assert "first" in content
            assert "second" in content


class TestCloseHandlerSafely:
    """Test close_handler_safely function"""

    def test_close_none(self):
        close_handler_safely(None)

    def test_close_handler_with_close_method(self):
        handler = logging.StreamHandler()
        close_handler_safely(handler)

    def test_close_object_without_close_method(self):
        class NoClose:
            pass

        obj = NoClose()
        close_handler_safely(obj)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
