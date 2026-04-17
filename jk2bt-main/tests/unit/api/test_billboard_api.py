"""
tests/unit/api/test_billboard_api.py
龙虎榜 API 单元测试

测试覆盖:
1. get_billboard_list - 获取龙虎榜数据
2. get_institutional_holdings - 获取机构持仓数据
3. get_billboard_hot_stocks - 获取龙虎榜热门股票
4. get_broker_statistics - 获取营业部买卖统计
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestJqSymbol:
    """测试 _jq_symbol 辅助函数"""

    def test_jq_symbol_shanghai(self):
        from jk2bt.api.billboard import _jq_symbol

        assert _jq_symbol("600519") == "600519.XSHG"
        assert _jq_symbol("600000") == "600000.XSHG"

    def test_jq_symbol_shenzhen(self):
        from jk2bt.api.billboard import _jq_symbol

        assert _jq_symbol("000001") == "000001.XSHE"
        assert _jq_symbol("300750") == "300750.XSHE"

    def test_jq_symbol_none(self):
        from jk2bt.api.billboard import _jq_symbol

        assert _jq_symbol(None) is None


class TestGetBillboardList:
    """测试获取龙虎榜数据"""

    @patch("jk2bt.api.billboard.get_adapter")
    def test_get_billboard_list_success(self, mock_adapter):
        mock_adapter.return_value.get_billboard_list.return_value = pd.DataFrame(
            {
                "代码": ["600519", "000001"],
                "名称": ["贵州茅台", "平安银行"],
                "龙虎榜净买": [1000000, 2000000],
                "龙虎榜买入额": [5000000, 8000000],
                "龙虎榜卖出额": [4000000, 6000000],
                "上榜原因": ["涨幅偏离", "跌幅偏离"],
            }
        )

        from jk2bt.api.billboard import get_billboard_list

        result = get_billboard_list(count=5)

        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    @patch("jk2bt.api.billboard.get_adapter")
    def test_get_billboard_list_empty(self, mock_adapter):
        mock_adapter.return_value.get_billboard_list.return_value = pd.DataFrame()

        from jk2bt.api.billboard import get_billboard_list

        result = get_billboard_list()
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.api.billboard.get_adapter")
    def test_get_billboard_list_with_stock_filter(self, mock_adapter):
        mock_adapter.return_value.get_billboard_list.return_value = pd.DataFrame(
            {
                "代码": ["600519", "000001"],
                "名称": ["贵州茅台", "平安银行"],
                "龙虎榜净买": [1000000, 2000000],
                "龙虎榜买入额": [5000000, 8000000],
                "龙虎榜卖出额": [4000000, 6000000],
            }
        )

        from jk2bt.api.billboard import get_billboard_list

        result = get_billboard_list(stock="600519.XSHG")
        assert isinstance(result, pd.DataFrame)


class TestGetInstitutionalHoldings:
    """测试获取机构持仓数据"""

    @patch("jk2bt.api.billboard.get_adapter")
    def test_get_institutional_holdings_success(self, mock_adapter):
        mock_adapter.return_value.get_top10_holders.return_value = pd.DataFrame(
            {
                "股东名称": ["机构A", "机构B"],
                "持股数量": [1000000, 800000],
                "持股比例": [5.0, 4.0],
                "报告期": ["2024-03-31", "2024-03-31"],
            }
        )

        from jk2bt.api.billboard import get_institutional_holdings

        result = get_institutional_holdings("600519.XSHG")

        assert isinstance(result, pd.DataFrame)
        assert "institution_name" in result.columns

    @patch("jk2bt.api.billboard.get_adapter")
    def test_get_institutional_holdings_empty(self, mock_adapter):
        mock_adapter.return_value.get_top10_holders.return_value = pd.DataFrame()
        mock_adapter.return_value.get_institutional_holders.return_value = (
            pd.DataFrame()
        )
        mock_adapter.return_value.get_fund_hold_stock.return_value = pd.DataFrame()

        from jk2bt.api.billboard import get_institutional_holdings

        result = get_institutional_holdings("600519.XSHG")
        assert isinstance(result, pd.DataFrame)


class TestGetBillboardHotStocks:
    """测试获取龙虎榜热门股票"""

    @patch("jk2bt.api.billboard.get_billboard_list")
    def test_get_billboard_hot_stocks(self, mock_get_list):
        mock_get_list.return_value = pd.DataFrame(
            {
                "code": ["600519.XSHG", "600519.XSHG", "000001.XSHE"],
                "net_value": [1000000, 2000000, 1500000],
                "buy_value": [5000000, 8000000, 6000000],
                "sell_value": [4000000, 6000000, 4500000],
                "date": ["2024-01-01", "2024-01-02", "2024-01-01"],
            }
        )

        from jk2bt.api.billboard import get_billboard_hot_stocks

        result = get_billboard_hot_stocks(top_n=10)

        assert isinstance(result, pd.DataFrame)
        assert "total_net_value" in result.columns


class TestGetBrokerStatistics:
    """测试获取营业部买卖统计"""

    @patch("jk2bt.api.billboard.get_billboard_list")
    def test_get_broker_statistics(self, mock_get_list):
        mock_get_list.return_value = pd.DataFrame(
            {
                "broker_name": ["营业部A", "营业部A", "营业部B"],
                "buy_value": [1000000, 2000000, 1500000],
                "sell_value": [900000, 1800000, 1400000],
                "net_value": [100000, 200000, 100000],
                "code": ["600519.XSHG", "000001.XSHE", "600519.XSHG"],
            }
        )

        from jk2bt.api.billboard import get_broker_statistics

        result = get_broker_statistics(top_n=10)

        assert isinstance(result, pd.DataFrame)
        assert "total_buy" in result.columns


class TestBillboardModuleExports:
    """测试模块导出"""

    def test_all_exports_exist(self):
        from jk2bt.api.billboard import __all__

        expected = [
            "get_billboard_list",
            "get_institutional_holdings",
            "get_billboard_hot_stocks",
            "get_broker_statistics",
        ]

        for name in expected:
            assert name in __all__, f"{name} not in __all__"
