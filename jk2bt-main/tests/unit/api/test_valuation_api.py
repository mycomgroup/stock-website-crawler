"""
tests/unit/api/test_valuation_api.py
估值 API 单元测试

测试覆盖:
1. get_index_valuation - 指数估值数据
2. get_valuation - 股票/指数估值数据
3. get_index_valuation_jq - 聚宽风格别名
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestGetIndexValuation:
    """测试获取指数估值数据"""

    def test_normalize_index_code(self):
        from jk2bt.api.valuation import _normalize_index_code

        assert _normalize_index_code("000300.XSHG") == "000300"
        assert _normalize_index_code("000300") == "000300"
        assert _normalize_index_code("sh000300") == "000300"

    @patch("jk2bt.api.valuation.get_adapter")
    def test_get_index_valuation_success(self, mock_adapter):
        mock_adapter.return_value.get_index_valuation.return_value = pd.DataFrame(
            {
                "日期": ["2024-01-01", "2024-01-02"],
                "市盈率": [12.0, 12.5],
                "市净率": [1.5, 1.6],
                "股息率": [2.5, 2.4],
            }
        )

        from jk2bt.api.valuation import get_index_valuation

        result = get_index_valuation(
            "000300.XSHG", start_date="2024-01-01", end_date="2024-01-02"
        )

        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns
        assert "date" in result.columns

    @patch("jk2bt.api.valuation.get_adapter")
    def test_get_index_valuation_empty(self, mock_adapter):
        mock_adapter.return_value.get_index_valuation.return_value = pd.DataFrame()

        from jk2bt.api.valuation import get_index_valuation

        result = get_index_valuation("000300.XSHG")
        assert isinstance(result, pd.DataFrame)

    def test_get_index_valuation_with_count(self):
        with patch("jk2bt.api.valuation.get_adapter") as mock_adapter:
            mock_adapter.return_value.get_index_valuation.return_value = pd.DataFrame(
                {
                    "日期": pd.date_range("2024-01-01", periods=10),
                    "市盈率": np.random.randn(10) * 2 + 12,
                    "市净率": np.random.randn(10) * 0.2 + 1.5,
                }
            )

            from jk2bt.api.valuation import get_index_valuation

            result = get_index_valuation("000300.XSHG", count=5)
            assert len(result) <= 5


class TestGetValuation:
    """测试获取股票/指数估值数据"""

    @patch("jk2bt.api.valuation.get_adapter")
    def test_get_valuation_index(self, mock_adapter):
        mock_adapter.return_value.get_index_valuation.return_value = pd.DataFrame(
            {
                "日期": ["2024-01-01"],
                "市盈率": [12.0],
            }
        )

        from jk2bt.api.valuation import get_valuation

        result = get_valuation("000300.XSHG")
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.api.valuation.get_adapter")
    def test_get_valuation_stock(self, mock_adapter):
        mock_adapter.return_value.get_stock_valuation.return_value = pd.DataFrame(
            {
                "市盈率": [15.0],
                "市净率": [2.0],
            }
        )

        from jk2bt.api.valuation import get_valuation

        result = get_valuation("600519.XSHG")
        assert isinstance(result, pd.DataFrame)

    def test_is_index(self):
        from jk2bt.api.valuation import _is_index

        assert _is_index("000300.XSHG") is True
        assert _is_index("399001.XSHE") is True
        assert _is_index("600519.XSHG") is False
        assert _is_index("000001.XSHE") is False


class TestGetEmptyValuationFrame:
    """测试空估值数据框"""

    def test_get_empty_valuation_frame(self):
        from jk2bt.api.valuation import _get_empty_valuation_frame

        result = _get_empty_valuation_frame()
        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert "code" in result.columns
        assert "date" in result.columns


class TestValuationModuleExports:
    """测试模块导出"""

    def test_all_exports_exist(self):
        from jk2bt.api.valuation import __all__

        expected = [
            "get_index_valuation",
            "get_valuation",
            "get_index_valuation_jq",
        ]

        for name in expected:
            assert name in __all__, f"{name} not in __all__"
