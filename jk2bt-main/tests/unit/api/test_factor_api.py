"""
tests/unit/api/test_factor_api.py
因子 API 单元测试

测试覆盖:
1. get_north_factor - 北向资金因子
2. get_comb_factor - 组合因子
3. get_factor_momentum - 因子动量
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import warnings


class TestNorthFactor:
    """测试北向资金因子"""

    def test_get_north_factor_no_security(self):
        with patch("jk2bt.api.factor.get_north_money_flow") as mock_flow:
            mock_df = pd.DataFrame(
                {
                    "net_inflow": [100, 200, 300, 400, 500],
                    "inflow": [1000, 2000, 3000, 4000, 5000],
                    "outflow": [900, 1800, 2700, 3600, 4500],
                }
            )
            mock_flow.return_value = mock_df

            from jk2bt.api.factor import get_north_factor

            result = get_north_factor(security=None, count=1)
            assert isinstance(result, float)

    def test_get_north_factor_single_security(self):
        with patch("jk2bt.api.factor.get_north_money_stock_flow") as mock_flow:
            mock_df = pd.DataFrame(
                {
                    "net_inflow": [100, 200, 300, 400, 500],
                }
            )
            mock_df.index = pd.date_range("2024-01-01", periods=5)
            mock_flow.return_value = mock_df

            from jk2bt.api.factor import get_north_factor

            result = get_north_factor("600519.XSHG", count=1, factor_type="stock_flow")
            assert isinstance(result, (int, float))

    def test_get_north_factor_multiple_securities(self):
        with patch("jk2bt.api.factor.get_north_money_stock_flow") as mock_flow:
            mock_df = pd.DataFrame(
                {
                    "net_inflow": [100, 200, 300, 400, 500],
                }
            )
            mock_df.index = pd.date_range("2024-01-01", periods=5)
            mock_flow.return_value = mock_df

            from jk2bt.api.factor import get_north_factor

            result = get_north_factor(
                ["600519.XSHG", "000001.XSHE"], count=1, factor_type="stock_flow"
            )
            assert isinstance(result, dict)
            assert len(result) == 2


class TestCombFactor:
    """测试组合因子"""

    def test_get_comb_factor_empty_factors(self):
        from jk2bt.api.factor import get_comb_factor

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = get_comb_factor("600519.XSHG", [], end_date="2024-01-01")
            assert result == 0.0

    @patch("jk2bt.api.factor.get_factor_values_jq")
    def test_get_comb_factor_single_security(self, mock_get_factor):
        mock_get_factor.return_value = {
            "pe_ratio": pd.DataFrame(
                {"600519.XSHG": [10, 11, 12]},
                index=pd.date_range("2024-01-01", periods=3),
            ),
        }

        from jk2bt.api.factor import get_comb_factor

        result = get_comb_factor("600519.XSHG", ["pe_ratio"], end_date="2024-01-01")
        assert isinstance(result, (int, float))


class TestFactorMomentum:
    """测试因子动量"""

    @patch("jk2bt.api.factor.get_factor_values_jq")
    def test_get_factor_momentum_single_security(self, mock_get_factor):
        mock_df1 = pd.DataFrame({"600519.XSHG": [10, 11, 12]})
        mock_df1.index = pd.date_range("2024-01-01", periods=3)
        mock_df2 = pd.DataFrame({"600519.XSHG": [9, 10, 11]})
        mock_df2.index = pd.date_range("2024-01-01", periods=3)

        mock_get_factor.side_effect = [mock_df1, mock_df2]

        from jk2bt.api.factor import get_factor_momentum

        result = get_factor_momentum("600519.XSHG", "pe_ratio", window=1)
        assert isinstance(result, (int, float))


class TestFactorModuleExports:
    """测试模块导出"""

    def test_all_exports_exist(self):
        from jk2bt.api.factor import __all__

        expected = [
            "get_north_factor",
            "get_comb_factor",
            "get_factor_momentum",
        ]

        for name in expected:
            assert name in __all__, f"{name} not in __all__"
