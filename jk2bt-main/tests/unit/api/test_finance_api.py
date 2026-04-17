"""
tests/unit/api/test_finance_api.py
财务 API 单元测试

测试覆盖:
1. get_locked_shares - 获取限售股解禁数据
2. get_fund_info - 获取基金信息
3. get_fundamentals_continuously - 连续获取财务数据
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestGetLockedShares:
    """测试获取限售股解禁数据"""

    @patch("jk2bt.api.finance.get_adapter")
    def test_get_locked_shares_success(self, mock_adapter):
        mock_adapter.return_value.get_unlock_summary.return_value = pd.DataFrame(
            {
                "股票代码": ["600519", "000001"],
                "解禁日期": ["2024-01-15", "2024-01-20"],
                "解禁股数": [1000000, 2000000],
                "解禁市值": [100000000, 200000000],
                "占流通股比例": [0.05, 0.08],
            }
        )

        from jk2bt.api.finance import get_locked_shares

        result = get_locked_shares()

        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns
        assert "unlock_date" in result.columns

    @patch("jk2bt.api.finance.get_adapter")
    def test_get_locked_shares_with_date_filter(self, mock_adapter):
        mock_adapter.return_value.get_unlock_summary.return_value = pd.DataFrame(
            {
                "股票代码": ["600519", "000001"],
                "解禁日期": ["2024-01-15", "2024-02-20"],
                "解禁股数": [1000000, 2000000],
                "解禁市值": [100000000, 200000000],
                "占流通股比例": [0.05, 0.08],
            }
        )

        from jk2bt.api.finance import get_locked_shares

        result = get_locked_shares(start_date="2024-01-16", end_date="2024-02-01")
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.api.finance.get_adapter")
    def test_get_locked_shares_empty(self, mock_adapter):
        mock_adapter.return_value.get_unlock_summary.return_value = pd.DataFrame()

        from jk2bt.api.finance import get_locked_shares

        result = get_locked_shares()
        assert isinstance(result, pd.DataFrame)
        assert result.empty


class TestGetFundInfo:
    """测试获取基金信息"""

    @patch("jk2bt.api.finance.get_adapter")
    def test_get_fund_info_success(self, mock_adapter):
        mock_adapter.return_value.get_fund_name_list.return_value = pd.DataFrame(
            {
                "基金代码": ["000001", "000002"],
                "基金简称": ["基金A", "基金B"],
                "基金类型": ["股票型", "债券型"],
                "成立日期": ["2010-01-01", "2012-06-15"],
            }
        )

        from jk2bt.api.finance import get_fund_info

        result = get_fund_info("000001")
        assert isinstance(result, dict)
        assert result.get("fund_code") == "000001"
        assert "fund_name" in result

    @patch("jk2bt.api.finance.get_adapter")
    def test_get_fund_info_not_found(self, mock_adapter):
        mock_adapter.return_value.get_fund_name_list.return_value = pd.DataFrame(
            {
                "基金代码": ["000001"],
                "基金简称": ["基金A"],
            }
        )

        from jk2bt.api.finance import get_fund_info

        result = get_fund_info("999999")
        assert isinstance(result, dict)
        assert result == {}

    @patch("jk2bt.api.finance.get_adapter")
    def test_get_fund_info_with_fields(self, mock_adapter):
        mock_adapter.return_value.get_fund_name_list.return_value = pd.DataFrame(
            {
                "基金代码": ["000001"],
                "基金简称": ["基金A"],
                "基金类型": ["股票型"],
                "成立日期": ["2010-01-01"],
            }
        )

        from jk2bt.api.finance import get_fund_info

        result = get_fund_info("000001", fields=["fund_code", "fund_name"])
        assert isinstance(result, dict)
        assert "fund_code" in result
        assert "fund_name" in result
        assert "fund_type" not in result


class TestGetFundamentalsContinuously:
    """测试连续获取财务数据"""

    def test_get_fundamentals_continuously_empty_query(self):
        from jk2bt.api.finance import get_fundamentals_continuously

        class MockQuery:
            pass

        result = get_fundamentals_continuously(MockQuery(), start_date="2024-01-01")
        assert isinstance(result, pd.DataFrame)


class TestFinanceModuleExports:
    """测试模块导出"""

    def test_all_exports_exist(self):
        from jk2bt.api.finance import __all__

        expected = [
            "get_locked_shares",
            "get_fund_info",
            "get_fundamentals_continuously",
        ]

        for name in expected:
            assert name in __all__, f"{name} not in __all__"
