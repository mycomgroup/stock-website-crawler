"""
Tests for jk2bt/logging/formatters.py - Formatters
"""

import pytest
import logging
import json
import sys
from datetime import datetime, timezone
from jk2bt.logging.formatters import (
    STANDARD_FORMAT,
    SIMPLE_FORMAT,
    STRATEGY_FORMAT,
    StandardFormatter,
    JSONFormatter,
    get_formatter,
)


class TestFormatConstants:
    """Test format constant strings"""

    def test_standard_format(self):
        assert "%(asctime)s" in STANDARD_FORMAT
        assert "%(levelname)-8s" in STANDARD_FORMAT

    def test_simple_format(self):
        assert "%(asctime)s" in SIMPLE_FORMAT
        assert "%(message)s" in SIMPLE_FORMAT

    def test_strategy_format(self):
        assert "%(asctime)s" in STRATEGY_FORMAT
        assert "%(message)s" in STRATEGY_FORMAT


class TestStandardFormatter:
    """Test StandardFormatter class"""

    def test_init(self):
        formatter = StandardFormatter()
        assert formatter._fmt == STANDARD_FORMAT

    def test_init_custom_format(self):
        formatter = StandardFormatter("%(message)s")
        assert formatter._fmt == "%(message)s"

    def test_format_record(self, caplog):
        logger = logging.getLogger("test_standard")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(StandardFormatter())
        logger.addHandler(handler)

        logger.info("test message")
        assert "test message" in caplog.text


class TestJSONFormatter:
    """Test JSONFormatter class"""

    def test_format_simple_message(self):
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="test message",
            args=(),
            exc_info=None,
        )

        output = formatter.format(record)
        data = json.loads(output)

        assert data["level"] == "INFO"
        assert data["logger"] == "test"
        assert data["message"] == "test message"
        assert "timestamp" in data

    def test_format_with_exception(self):
        formatter = JSONFormatter()
        try:
            raise ValueError("test error")
        except ValueError:
            exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="error occurred",
            args=(),
            exc_info=exc_info,
        )

        output = formatter.format(record)
        data = json.loads(output)

        assert data["level"] == "ERROR"
        assert "exception" in data


class TestGetFormatter:
    """Test get_formatter function"""

    def test_get_standard_formatter(self):
        formatter = get_formatter("standard")
        assert isinstance(formatter, StandardFormatter)

    def test_get_simple_formatter(self):
        formatter = get_formatter("simple")
        assert isinstance(formatter, logging.Formatter)

    def test_get_json_formatter(self):
        formatter = get_formatter("json")
        assert isinstance(formatter, JSONFormatter)

    def test_get_strategy_formatter(self):
        formatter = get_formatter("strategy")
        assert isinstance(formatter, logging.Formatter)

    def test_get_formatter_invalid_type(self):
        with pytest.raises(ValueError) as excinfo:
            get_formatter("invalid")
        assert "Unsupported format type" in str(excinfo.value)


if __name__ == "__main__":
    import sys

    sys.path.insert(0, "/Users/fengzhi/Downloads/git/testlixingren/jk2bt-main")
    pytest.main([__file__, "-v"])
