"""
tests/unit/api/test_margin_api.py
融资融券 API 单元测试

测试覆盖:
1. get_mtss - 获取融资融券数据
2. get_margincash_stocks - 获取可融资标的列表
3. get_marginsec_stocks - 获取可融券标的列表
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestGetMtss:
    """测试获取融资融券数据"""

    @patch("jk2bt.api.margin.get_margin_data")
    @patch("jk2bt.api.margin.get_margin_history")
    def test_get_mtss_single_security(self, mock_history, mock_data):
        mock_data.return_value = pd.DataFrame(
            {
                "code": ["600519.XSHG"],
                "date": ["2024-01-01"],
                "margin_balance": [100000000],
                "margin_buy": [5000000],
            }
        )

        from jk2bt.api.margin import get_mtss

        result = get_mtss("600519.XSHG", end_date="2024-01-01")

        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns
        assert "margin_balance" in result.columns

    @patch("jk2bt.api.margin.get_margin_data")
    @patch("jk2bt.api.margin.get_margin_history")
    def test_get_mtss_multiple_securities(self, mock_history, mock_data):
        mock_data.side_effect = [
            pd.DataFrame(
                {
                    "code": ["600519.XSHG"],
                    "date": ["2024-01-01"],
                    "margin_balance": [100000000],
                }
            ),
            pd.DataFrame(
                {
                    "code": ["000001.XSHE"],
                    "date": ["2024-01-01"],
                    "margin_balance": [50000000],
                }
            ),
        ]

        from jk2bt.api.margin import get_mtss

        result = get_mtss(["600519.XSHG", "000001.XSHE"], end_date="2024-01-01")

        assert isinstance(result, pd.DataFrame)

    def test_get_mtss_count_parameter_error(self):
        from jk2bt.api.margin import get_mtss

        with pytest.raises(ValueError, match="start_date 和 count 不能同时使用"):
            get_mtss("600519.XSHG", start_date="2024-01-01", count=5)


class TestGetMtssMarket:
    """测试全市场融资融券数据"""

    @patch("jk2bt.api.margin.get_adapter")
    def test_get_market_mtss(self, mock_adapter):
        mock_adapter.return_value.get_margin_detail.side_effect = [
            pd.DataFrame(
                {
                    "标的证券代码": ["600519", "600000"],
                    "融资余额": [100000000, 50000000],
                    "融资买入额": [5000000, 2000000],
                }
            ),
            pd.DataFrame(
                {
                    "证券代码": ["000001", "000002"],
                    "融资余额": [80000000, 30000000],
                    "融资买入额": [3000000, 1000000],
                }
            ),
        ]

        from jk2bt.api.margin import _get_market_mtss

        result = _get_market_mtss(end_date="2024-01-01")

        assert isinstance(result, pd.DataFrame)


class TestNormalizeMargin:
    """测试融资融券数据标准化"""

    def test_normalize_sse_margin(self):
        from jk2bt.api.margin import _normalize_sse_margin

        df = pd.DataFrame(
            {
                "标的证券代码": ["600519", "600000"],
                "信用交易日期": ["2024-01-01", "2024-01-01"],
                "融资余额": [100000000, 50000000],
                "融资买入额": [5000000, 2000000],
                "融资偿还额": [1000000, 500000],
                "融券余量": [100000, 50000],
                "融券卖出量": [10000, 5000],
                "融券偿还量": [5000, 2000],
            }
        )

        result = _normalize_sse_margin(df)

        assert "code" in result.columns
        assert result["code"].iloc[0] == "600519.XSHG"

    def test_normalize_szse_margin(self):
        from jk2bt.api.margin import _normalize_szse_margin

        df = pd.DataFrame(
            {
                "证券代码": ["000001", "000002"],
                "融资余额": [100000000, 50000000],
                "融资买入额": [5000000, 2000000],
                "融券余量": [100000, 50000],
                "融券卖出量": [10000, 5000],
            }
        )

        result = _normalize_szse_margin(df)

        assert "code" in result.columns
        assert result["code"].iloc[0] == "000001.XSHE"


class TestGetMarginCashStocks:
    """测试获取可融资标的列表"""

    @patch("jk2bt.api.margin.get_adapter")
    def test_get_margincash_stocks(self, mock_adapter):
        mock_adapter.return_value.get_margin_underlying.side_effect = [
            pd.DataFrame({"证券代码": ["600519", "600000"]}),
            pd.DataFrame({"证券代码": ["000001", "000002"]}),
        ]

        from jk2bt.api.margin import get_margincash_stocks

        result = get_margincash_stocks()

        assert isinstance(result, list)

    @patch("jk2bt.api.margin.get_adapter")
    def test_get_margincash_stocks_empty(self, mock_adapter):
        mock_adapter.return_value.get_margin_underlying.side_effect = [
            pd.DataFrame(),
            pd.DataFrame(),
        ]

        from jk2bt.api.margin import get_margincash_stocks

        result = get_margincash_stocks()
        assert isinstance(result, list)


class TestGetMarginSecStocks:
    """测试获取可融券标的列表"""

    @patch("jk2bt.api.margin.get_margincash_stocks")
    def test_get_marginsec_stocks(self, mock_cash):
        mock_cash.return_value = ["600519.XSHG", "000001.XSHE"]

        from jk2bt.api.margin import get_marginsec_stocks

        result = get_marginsec_stocks()

        assert isinstance(result, list)


class TestEmptyMtssFrame:
    """测试空融资融券数据框"""

    def test_get_empty_mtss_frame(self):
        from jk2bt.api.margin import _get_empty_mtss_frame

        result = _get_empty_mtss_frame()

        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert "code" in result.columns
        assert "margin_balance" in result.columns


class TestMarginModuleExports:
    """测试模块导出"""

    def test_all_exports_exist(self):
        from jk2bt.api.margin import __all__

        expected = [
            "get_mtss",
            "get_margincash_stocks",
            "get_marginsec_stocks",
            "get_mtss_jq",
        ]

        for name in expected:
            assert name in __all__, f"{name} not in __all__"
