"""
Tests for jk2bt/logging/adapters.py - JQLogAdapter
"""

import pytest
import io
import sys
import pandas as pd
from unittest.mock import MagicMock
from jk2bt.logging.adapters import JQLogAdapter, create_jq_log_adapter


class TestJQLogAdapter:
    """Test JQLogAdapter class"""

    def test_init_default(self):
        adapter = JQLogAdapter()
        assert adapter._strategy is None
        assert adapter._logger is not None

    def test_init_with_strategy(self):
        mock_strategy = MagicMock()
        adapter = JQLogAdapter(strategy=mock_strategy)
        assert adapter._strategy is mock_strategy

    def test_info_output(self):
        adapter = JQLogAdapter()
        captured = io.StringIO()
        sys.stdout = captured
        adapter.info("test message")
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "test message" in output

    def test_warn_output(self):
        adapter = JQLogAdapter()
        captured = io.StringIO()
        sys.stdout = captured
        adapter.warn("warning message")
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "[WARN]" in output
        assert "warning message" in output

    def test_error_output(self):
        adapter = JQLogAdapter()
        captured = io.StringIO()
        sys.stdout = captured
        adapter.error("error message")
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "[ERROR]" in output
        assert "error message" in output

    def test_debug_with_debug_level(self):
        adapter = JQLogAdapter()
        adapter.set_level("debug", "debug")

        captured = io.StringIO()
        sys.stdout = captured
        adapter.debug("debug message")
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "debug message" in output

    def test_debug_without_debug_level(self):
        adapter = JQLogAdapter()
        adapter.set_level("debug", "off")

        captured = io.StringIO()
        sys.stdout = captured
        adapter.debug("debug message")
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "debug message" not in output

    def test_warning_alias(self):
        adapter = JQLogAdapter()
        captured = io.StringIO()
        sys.stdout = captured
        adapter.warning("warning alias test")
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "[WARN]" in output

    def test_critical(self):
        adapter = JQLogAdapter()
        captured = io.StringIO()
        sys.stdout = captured
        adapter.critical("critical message")
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "[CRITICAL]" in output
        assert "critical message" in output

    def test_multiple_args(self):
        adapter = JQLogAdapter()
        captured = io.StringIO()
        sys.stdout = captured
        adapter.info("arg1", "arg2", "arg3")
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "arg1" in output
        assert "arg2" in output
        assert "arg3" in output

    def test_dataframe_formatting(self):
        adapter = JQLogAdapter()
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

        captured = io.StringIO()
        sys.stdout = captured
        adapter.info("Data:", df)
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "Data:" in output
        assert "a" in output
        assert "b" in output

    def test_series_formatting(self):
        adapter = JQLogAdapter()
        s = pd.Series([1, 2, 3], name="test")

        captured = io.StringIO()
        sys.stdout = captured
        adapter.info("Series:", s)
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "Series:" in output
        assert "test" in output

    def test_kwargs_formatting(self):
        adapter = JQLogAdapter()
        captured = io.StringIO()
        sys.stdout = captured
        adapter.info("message", key="value", num=123)
        sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "key=value" in output
        assert "num=123" in output

    def test_set_level(self):
        adapter = JQLogAdapter()
        adapter.set_level("order", "warning")
        assert adapter._log_levels["order"] == "warning"

        adapter.set_level("trade", "error")
        assert adapter._log_levels["trade"] == "error"

    def test_forward_to_strategy(self):
        mock_strategy = MagicMock()
        adapter = JQLogAdapter(strategy=mock_strategy)

        adapter.info("test message")

        mock_strategy.log.assert_called_once()
        call_args = mock_strategy.log.call_args[0][0]
        assert "test message" in call_args

    def test_forward_with_warn_prefix(self):
        mock_strategy = MagicMock()
        adapter = JQLogAdapter(strategy=mock_strategy)

        adapter.warn("warning message")

        call_args = mock_strategy.log.call_args[0][0]
        assert "[WARN]" in call_args

    def test_forward_with_error_prefix(self):
        mock_strategy = MagicMock()
        adapter = JQLogAdapter(strategy=mock_strategy)

        adapter.error("error message")

        call_args = mock_strategy.log.call_args[0][0]
        assert "[ERROR]" in call_args


class TestCreateJQLogAdapter:
    """Test create_jq_log_adapter function"""

    def test_create_without_strategy(self):
        adapter = create_jq_log_adapter()
        assert isinstance(adapter, JQLogAdapter)
        assert adapter._strategy is None

    def test_create_with_strategy(self):
        mock_strategy = MagicMock()
        adapter = create_jq_log_adapter(strategy=mock_strategy)
        assert adapter._strategy is mock_strategy

    def test_create_with_custom_logger_name(self):
        adapter = create_jq_log_adapter(logger_name="custom_logger")
        assert adapter._logger.name == "custom_logger"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
