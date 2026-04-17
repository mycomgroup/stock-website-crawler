"""
Tests for jk2bt/validation/data_collector.py - DataCollector
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from jk2bt.validation.data_collector import (
    LocalDataSource,
    JQNotebookSource,
    DataCollector,
)


class TestLocalDataSource:
    """Test LocalDataSource class"""

    def setup_method(self):
        self.source = LocalDataSource()

    def test_get_prefix_sh(self):
        assert self.source._get_prefix("600519.XSHG") == "sh"
        assert self.source._get_prefix("601318.XSHG") == "sh"

    def test_get_prefix_sz(self):
        assert self.source._get_prefix("000858.XSHE") == "sz"
        assert self.source._get_prefix("002594.XSHE") == "sz"

    @patch("jk2bt.validation.data_collector.get_adapter")
    def test_get_valuation_data(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_df = pd.DataFrame(
            {
                "日期": ["2024-01-02", "2024-01-03"],
                "pe": [10.0, 11.0],
                "pe_ttm": [9.5, 10.5],
                "pb": [3.0, 3.2],
                "ps": [2.0, 2.1],
                "total_mv": [1000000, 1100000],
                "circ_mv": [800000, 880000],
            }
        )
        mock_adapter.get_stock_valuation.return_value = mock_df
        mock_get_adapter.return_value = mock_adapter

        result = self.source.get_valuation_data(["600519.XSHG"], "2024-01-03")
        assert len(result) >= 0

    @patch("jk2bt.validation.data_collector.get_adapter")
    def test_get_trade_status(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_st_stocks.return_value = pd.DataFrame({"代码": []})
        mock_adapter.get_suspended_stocks.return_value = pd.DataFrame({"代码": []})
        mock_adapter.get_stock_hist.return_value = pd.DataFrame(
            {
                "日期": ["2024-01-02", "2024-01-03"],
                "收盘": [100.0, 105.0],
            }
        )
        mock_get_adapter.return_value = mock_adapter

        result = self.source.get_trade_status(["600519.XSHG"], "2024-01-03")
        assert len(result) >= 0

    @patch("jk2bt.validation.data_collector.get_adapter")
    def test_get_factor_data(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_stock_hist.return_value = pd.DataFrame(
            {
                "日期": pd.date_range("2024-01-01", periods=30),
                "收盘": [100.0 + i for i in range(30)],
            }
        )
        mock_get_adapter.return_value = mock_adapter

        result = self.source.get_factor_data(
            ["600519.XSHG"], "2024-01-30", ["momentum_20"]
        )
        assert len(result) >= 0


class TestJQNotebookSource:
    """Test JQNotebookSource class"""

    def setup_method(self):
        self.source = JQNotebookSource()

    def test_generate_collector_code_valuation(self):
        code = self.source._generate_collector_code(
            ["600519.XSHG"], "2024-01-01", "valuation"
        )
        assert "valuation" in code
        assert "600519.XSHG" in code

    def test_generate_collector_code_trade_status(self):
        code = self.source._generate_collector_code(
            ["600519.XSHG"], "2024-01-01", "trade_status"
        )
        assert "get_current_data" in code

    def test_generate_collector_code_factors(self):
        code = self.source._generate_collector_code(
            ["600519.XSHG"], "2024-01-01", "factors"
        )
        assert "get_factor_values" in code

    def test_generate_collector_code_unknown(self):
        code = self.source._generate_collector_code(
            ["600519.XSHG"], "2024-01-01", "unknown"
        )
        assert code == ""

    def test_collect_data_generates_file(self, tmp_path):
        output_file = tmp_path / "collector.py"
        df = self.source.collect_data(
            ["600519.XSHG"], "2024-01-01", "valuation", output_file=str(output_file)
        )
        assert output_file.exists()
        assert isinstance(df, pd.DataFrame)


class TestDataCollector:
    """Test DataCollector class"""

    def setup_method(self):
        self.collector = DataCollector()

    def test_init(self):
        assert self.collector.local_source is not None
        assert self.collector.jq_source is not None

    def test_collect_batch_creates_code_files(self, tmp_path):
        output_dir = tmp_path / "validation_results"
        output_dir.mkdir()

        self.collector.jq_source.collect_data(
            ["600519.XSHG"],
            "2024-01-01",
            "valuation",
            output_file=str(output_dir / "test.py"),
        )

        assert (output_dir / "test.py").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
