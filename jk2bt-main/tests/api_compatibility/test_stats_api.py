"""
test_stats_api.py
测试统计相关API: get_ols, get_zscore, get_rank 等
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pytest
import pandas as pd
import numpy as np


class TestStatsAPIExistence:
    """统计API存在性测试"""

    def test_get_beta_exists(self):
        """测试get_beta函数存在"""
        from jk2bt.api.missing_apis import get_beta
        assert callable(get_beta)

    def test_get_beta_single_security(self):
        """测试单标的Beta计算"""
        from jk2bt.api.missing_apis import get_beta

        # 测试单只股票
        result = get_beta("sh600000")

        # 应返回浮点数
        assert isinstance(result, (float, int))

    def test_get_beta_multiple_securities(self):
        """测试多标的Beta计算"""
        from jk2bt.api.missing_apis import get_beta

        result = get_beta(["sh600000", "sz000001"])

        # 应返回dict
        assert isinstance(result, dict)

        for symbol, beta in result.items():
            assert isinstance(beta, (float, int))

    def test_get_beta_with_benchmark(self):
        """测试指定基准指数"""
        from jk2bt.api.missing_apis import get_beta

        result = get_beta("sh600000", benchmark="000300.XSHG")

        assert isinstance(result, (float, int))

    def test_get_beta_with_window(self):
        """测试指定计算窗口"""
        from jk2bt.api.missing_apis import get_beta

        result = get_beta("sh600000", window=60)

        assert isinstance(result, (float, int))


class TestFactorStatsAPI:
    """因子统计API测试"""

    def test_get_factor_momentum_exists(self):
        """测试get_factor_momentum函数存在"""
        from jk2bt.api.factor_api import get_factor_momentum
        assert callable(get_factor_momentum)

    def test_get_factor_momentum_basic(self):
        """测试因子动量计算"""
        from jk2bt.api.factor_api import get_factor_momentum

        result = get_factor_momentum(
            securities="sh600000",
            factor="PE_ratio",
            window=20
        )

        # 应返回浮点数
        assert isinstance(result, (float, int))

    def test_get_factor_momentum_multiple(self):
        """测试多标的因子动量"""
        from jk2bt.api.factor_api import get_factor_momentum

        result = get_factor_momentum(
            securities=["sh600000", "sz000001"],
            factor="PE_ratio",
            window=20
        )

        # 应返回dict
        assert isinstance(result, dict)


class TestCombFactorAPI:
    """组合因子API测试"""

    def test_get_comb_factor_exists(self):
        """测试get_comb_factor函数存在"""
        from jk2bt.api.factor_api import get_comb_factor
        assert callable(get_comb_factor)

    def test_get_comb_factor_equal_weight(self):
        """测试等权组合"""
        from jk2bt.api.factor_api import get_comb_factor

        result = get_comb_factor(
            securities=["sh600000", "sz000001"],
            factors=["PE_ratio", "PB_ratio"],
            method="equal"
        )

        # 应返回dict
        assert isinstance(result, dict)

    def test_get_comb_factor_weighted(self):
        """测试加权组合"""
        from jk2bt.api.factor_api import get_comb_factor

        result = get_comb_factor(
            securities="sh600000",
            factors=["PE_ratio", "ROE"],
            method="weighted",
            weights={"PE_ratio": 0.3, "ROE": 0.7}
        )

        # 应返回浮点数
        assert isinstance(result, (float, dict))

    def test_get_comb_factor_rank(self):
        """测试排名加权"""
        from jk2bt.api.factor_api import get_comb_factor

        result = get_comb_factor(
            securities=["sh600000", "sz000001"],
            factors=["PE_ratio", "PB_ratio"],
            method="rank"
        )

        assert isinstance(result, dict)


class TestNorthFactorAPI:
    """北向资金因子API测试"""

    def test_get_north_factor_exists(self):
        """测试get_north_factor函数存在"""
        from jk2bt.api.factor_api import get_north_factor
        assert callable(get_north_factor)

    def test_get_north_factor_overall(self):
        """测试整体北向资金因子"""
        from jk2bt.api.factor_api import get_north_factor

        result = get_north_factor(security=None)

        # 应返回浮点数
        assert isinstance(result, (float, int, pd.Series))

    def test_get_north_factor_by_type(self):
        """测试不同因子类型"""
        from jk2bt.api.factor_api import get_north_factor

        factor_types = ["net_inflow", "flow_ratio", "momentum"]

        for ft in factor_types:
            result = get_north_factor(security=None, factor_type=ft)
            assert isinstance(result, (float, int, pd.Series))

    def test_get_north_factor_single_stock(self):
        """测试单股北向资金因子"""
        from jk2bt.api.factor_api import get_north_factor

        result = get_north_factor(
            security="sh600000",
            factor_type="stock_flow"
        )

        assert isinstance(result, (float, int))


class TestIndicatorStats:
    """技术指标统计测试"""

    def test_ma_calculation(self):
        """测试MA计算"""
        from jk2bt.api.indicators import MA

        # 使用模拟数据
        close_prices = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])

        ma5 = MA(close_prices, timeperiod=5)

        # 验证返回Series
        assert isinstance(ma5, pd.Series)

        # 验证计算结果
        if len(ma5) > 5:
            # MA5[5]应为(10+11+12+13+14)/5 = 12
            expected = close_prices.iloc[:5].mean()
            assert ma5.iloc[4] == expected

    def test_ema_calculation(self):
        """测试EMA计算"""
        from jk2bt.api.indicators import EMA

        close_prices = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])

        ema5 = EMA(close_prices, timeperiod=5)

        assert isinstance(ema5, pd.Series)

    def test_rsi_calculation(self):
        """测试RSI计算"""
        from jk2bt.api.indicators import RSI

        close_prices = pd.Series([10, 11, 10, 12, 11, 13, 12, 14, 13, 15])

        rsi14 = RSI(close_prices, timeperiod=14)

        assert isinstance(rsi14, pd.Series)

        # RSI应在0-100之间
        valid_rsi = rsi14.dropna()
        if len(valid_rsi) > 0:
            assert all(valid_rsi >= 0)
            assert all(valid_rsi <= 100)

    def test_macd_structure(self):
        """测试MACD返回结构"""
        from jk2bt.api.indicators import MACD

        result = MACD("sh600000")

        # 应返回dict
        assert isinstance(result, dict)

        # 应包含MACD, DIFF, DEA键
        assert "MACD" in result
        assert "DIFF" in result
        assert "DEA" in result

    def test_kdj_structure(self):
        """测试KDJ返回结构"""
        from jk2bt.api.indicators import KDJ

        result = KDJ("sh600000")

        assert isinstance(result, dict)

        assert "K" in result
        assert "D" in result
        assert "J" in result

    def test_boll_structure(self):
        """测试BOLL返回结构"""
        from jk2bt.api.indicators import BOLL

        result = BOLL("sh600000")

        assert isinstance(result, dict)

        assert "UPPER" in result
        assert "MIDDLE" in result
        assert "LOWER" in result

    def test_atr_structure(self):
        """测试ATR返回结构"""
        from jk2bt.api.indicators import ATR

        result = ATR("sh600000")

        assert isinstance(result, dict)


class TestZScoreNormalization:
    """Z-Score标准化测试"""

    def test_comb_factor_zscore(self):
        """测试组合因子zscore标准化"""
        from jk2bt.api.factor_api import get_comb_factor

        # 使用zscore标准化
        result = get_comb_factor(
            securities=["sh600000", "sz000001"],
            factors=["PE_ratio", "PB_ratio"],
            method="equal",
            normalize=True
        )

        assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])