"""
Tests for jk2bt/validation/comparison_engine.py - ComparisonEngine
"""

import pytest
import pandas as pd
import numpy as np
from jk2bt.validation.comparison_engine import (
    ComparisonEngine,
    ComparisonResult,
    StockComparisonResult,
    ComparisonSummary,
)


class TestComparisonResult:
    """Test ComparisonResult dataclass"""

    def test_to_dict(self):
        result = ComparisonResult(
            field_name="pe",
            local_value=10.5,
            jq_value=10.6,
            tolerance=0.01,
            is_match=True,
            diff_pct=0.95,
            diff_abs=0.1,
        )
        d = result.to_dict()
        assert d["field_name"] == "pe"
        assert d["is_match"] is True


class TestComparisonEngine:
    """Test ComparisonEngine class"""

    def setup_method(self):
        self.engine = ComparisonEngine()

    def test_get_tolerance_default(self):
        assert self.engine.get_tolerance("pe") == 0.01
        assert self.engine.get_tolerance("unknown") == 0.01

    def test_get_tolerance_custom(self):
        engine = ComparisonEngine({"pe": 0.05})
        assert engine.get_tolerance("pe") == 0.05

    def test_compare_value_both_none(self):
        result = self.engine.compare_value(None, None, "pe")
        assert result.is_match is True
        assert "均为 None" in result.note

    def test_compare_value_one_none(self):
        result = self.engine.compare_value(None, 10.0, "pe")
        assert result.is_match is False

    def test_compare_value_bool_match(self):
        result = self.engine.compare_value(True, True, "is_st")
        assert result.is_match is True

    def test_compare_value_bool_mismatch(self):
        result = self.engine.compare_value(True, False, "is_st")
        assert result.is_match is False

    def test_compare_value_numeric_match(self):
        result = self.engine.compare_value(10.0, 10.0, "pe")
        assert result.is_match is True

    def test_compare_value_numeric_within_tolerance(self):
        result = self.engine.compare_value(10.0, 10.005, "pe")
        assert result.is_match is True

    def test_compare_value_numeric_outside_tolerance(self):
        result = self.engine.compare_value(10.0, 11.0, "pe")
        assert result.is_match is False
        assert result.diff_pct > 0

    def test_compare_value_string_match(self):
        result = self.engine.compare_value("test", "test", "name")
        assert result.is_match is True

    def test_compare_value_string_mismatch(self):
        result = self.engine.compare_value("test", "Test", "name")
        assert result.is_match is False

    def test_compare_value_zero_division(self):
        result = self.engine.compare_value(0.0, 0.0, "pe")
        assert result.is_match is True
        assert result.diff_pct == 0.0

    def test_compare_row(self):
        local_row = pd.Series(
            {"code": "600519.XSHG", "date": "2024-01-01", "pe": 10.0, "pb": 3.0}
        )
        jq_row = pd.Series(
            {"code": "600519.XSHG", "date": "2024-01-01", "pe": 10.1, "pb": 3.0}
        )

        result = self.engine.compare_row(local_row, jq_row, ["pe", "pb"])

        assert result.code == "600519.XSHG"
        assert len(result.field_results) == 2

    def test_compare_dataframe(self):
        local_df = pd.DataFrame(
            {
                "code": ["600519.XSHG", "000858.XSHE"],
                "date": ["2024-01-01", "2024-01-01"],
                "pe": [10.0, 20.0],
                "pb": [3.0, 5.0],
            }
        )

        jq_df = pd.DataFrame(
            {
                "code": ["600519.XSHG", "000858.XSHE"],
                "date": ["2024-01-01", "2024-01-01"],
                "pe": [10.0, 20.1],
                "pb": [3.0, 5.0],
            }
        )

        summary = self.engine.compare_dataframe(local_df, jq_df)

        assert summary.total_stocks == 2
        assert summary.match_rate == 50.0
        assert "pe" in summary.field_stats

    def test_compare_dataframe_empty(self):
        local_df = pd.DataFrame({"code": [], "date": [], "pe": []})
        jq_df = pd.DataFrame({"code": [], "date": [], "pe": []})

        summary = self.engine.compare_dataframe(local_df, jq_df)
        assert summary.total_stocks == 0

    def test_compare_valuation(self):
        local_df = pd.DataFrame(
            {
                "code": ["600519.XSHG"],
                "date": ["2024-01-01"],
                "pe": [10.0],
                "pe_ttm": [9.5],
                "pb": [3.0],
                "ps": [2.0],
                "market_cap": [1000000],
                "circulating_market_cap": [800000],
            }
        )

        jq_df = pd.DataFrame(
            {
                "code": ["600519.XSHG"],
                "date": ["2024-01-01"],
                "pe": [10.0],
                "pe_ttm": [9.5],
                "pb": [3.0],
                "ps": [2.0],
                "market_cap": [1000000],
                "circulating_market_cap": [800000],
            }
        )

        summary = self.engine.compare_valuation(local_df, jq_df)
        assert summary.match_rate == 100.0

    def test_compare_trade_status(self):
        local_df = pd.DataFrame(
            {
                "code": ["600519.XSHG"],
                "date": ["2024-01-01"],
                "high_limit": [1000.0],
                "low_limit": [800.0],
                "is_st": [False],
                "paused": [False],
            }
        )

        jq_df = pd.DataFrame(
            {
                "code": ["600519.XSHG"],
                "date": ["2024-01-01"],
                "high_limit": [1000.0],
                "low_limit": [800.0],
                "is_st": [False],
                "paused": [False],
            }
        )

        summary = self.engine.compare_trade_status(local_df, jq_df)
        assert summary.match_rate == 100.0

    def test_compare_factors(self):
        local_df = pd.DataFrame(
            {
                "code": ["600519.XSHG"],
                "date": ["2024-01-01"],
                "momentum_20": [5.0],
                "volatility_20": [20.0],
            }
        )

        jq_df = pd.DataFrame(
            {
                "code": ["600519.XSHG"],
                "date": ["2024-01-01"],
                "momentum_20": [5.1],
                "volatility_20": [20.0],
            }
        )

        summary = self.engine.compare_factors(local_df, jq_df)
        assert summary.total_stocks == 1


class TestComparisonSummary:
    """Test ComparisonSummary dataclass"""

    def test_to_dict(self):
        summary = ComparisonSummary(
            data_type="valuation",
            total_stocks=10,
            total_fields=5,
            matched_stocks=8,
            matched_fields=45,
            match_rate=80.0,
        )
        d = summary.to_dict()
        assert d["data_type"] == "valuation"
        assert d["match_rate"] == 80.0


class TestStockComparisonResult:
    """Test StockComparisonResult dataclass"""

    def test_to_dict(self):
        result = StockComparisonResult(
            code="600519.XSHG",
            date="2024-01-01",
            data_type="valuation",
            is_match=True,
            match_rate=100.0,
        )
        d = result.to_dict()
        assert d["code"] == "600519.XSHG"
        assert d["is_match"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
