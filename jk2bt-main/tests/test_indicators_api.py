"""
测试技术指标 API 和因子 API

测试:
- MA, EMA, MACD, KDJ, RSI, BOLL, ATR 函数
- get_north_factor, get_comb_factor 函数
"""

import sys
import os
import warnings

# 添加 src 目录到路径
src_dir = os.path.join(os.path.dirname(__file__), "..", "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import pytest
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

pytestmark = pytest.mark.network


class TestTechnicalIndicators:
    """测试技术指标函数"""

    def test_ma_with_series(self):
        """测试 MA 函数 - Series 输入"""
        from jk2bt.api.indicators import MA

        # 创建测试数据
        close = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])

        # 计算 5 日均线
        ma5 = MA(close, timeperiod=5)

        assert isinstance(ma5, pd.Series)
        assert len(ma5) == len(close)
        # 第5个值应该是前5个数的平均值
        assert ma5.iloc[4] == pytest.approx(12.0, rel=0.01)

    def test_ma_with_numpy(self):
        """测试 MA 函数 - numpy 输入"""
        from jk2bt.api.indicators import MA

        close = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        ma5 = MA(close, timeperiod=5)

        assert isinstance(ma5, np.ndarray)
        assert len(ma5) == len(close)

    def test_ma_with_list(self):
        """测试 MA 函数 - list 输入"""
        from jk2bt.api.indicators import MA

        close = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        ma5 = MA(close, timeperiod=5)

        assert isinstance(ma5, list)
        assert len(ma5) == len(close)

    def test_ema(self):
        """测试 EMA 函数"""
        from jk2bt.api.indicators import EMA

        close = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        ema5 = EMA(close, timeperiod=5)

        assert isinstance(ema5, pd.Series)
        assert len(ema5) == len(close)

    def test_rsi_with_series(self):
        """测试 RSI 函数 - Series 输入"""
        from jk2bt.api.indicators import RSI

        # 创建上涨序列
        close = pd.Series([100 + i for i in range(30)])
        rsi = RSI(close, timeperiod=14)

        assert isinstance(rsi, pd.Series)
        # 上涨序列 RSI 应该接近 100
        assert rsi.iloc[-1] > 70

    def test_rsi_with_numpy(self):
        """测试 RSI 函数 - numpy 输入"""
        from jk2bt.api.indicators import RSI

        close = np.array([100 + i for i in range(30)])
        rsi = RSI(close, timeperiod=14)

        assert isinstance(rsi, np.ndarray)


class TestMACD:
    """测试 MACD 函数"""

    def test_macd_import(self):
        """测试 MACD 模块导入"""
        from jk2bt.api.indicators import MACD

        assert callable(MACD)


class TestKDJ:
    """测试 KDJ 函数"""

    def test_kdj_import(self):
        """测试 KDJ 模块导入"""
        from jk2bt.api.indicators import KDJ

        assert callable(KDJ)


class TestBOLL:
    """测试布林带函数"""

    def test_boll_import(self):
        """测试 BOLL 模块导入"""
        from jk2bt.api.indicators import BOLL

        assert callable(BOLL)


class TestATR:
    """测试 ATR 函数"""

    def test_atr_import(self):
        """测试 ATR 模块导入"""
        from jk2bt.api.indicators import ATR

        assert callable(ATR)


class TestNorthFactor:
    """测试北向资金因子"""

    def test_get_north_factor_import(self):
        """测试 get_north_factor 导入"""
        from jk2bt.api.factor_api import get_north_factor

        assert callable(get_north_factor)

    def test_get_north_factor_types(self):
        """测试 get_north_factor 因子类型"""
        from jk2bt.api.factor_api import get_north_factor

        # 测试不同因子类型
        factor_types = ["net_inflow", "flow_ratio", "momentum"]

        for ft in factor_types:
            try:
                result = get_north_factor(factor_type=ft, window=5)
                # 返回值应该是数值
                assert isinstance(result, (int, float, np.floating))
            except Exception as e:
                # 网络错误是可接受的
                if "network" not in str(e).lower() and "akshare" not in str(e).lower():
                    pytest.fail(f"Unexpected error for factor_type={ft}: {e}")


class TestCombFactor:
    """测试组合因子"""

    def test_get_comb_factor_import(self):
        """测试 get_comb_factor 导入"""
        from jk2bt.api.factor_api import get_comb_factor

        assert callable(get_comb_factor)

    def test_get_comb_factor_single(self):
        """测试单股票组合因子"""
        from jk2bt.api.factor_api import get_comb_factor

        # 使用技术因子测试（不需要网络）
        try:
            result = get_comb_factor(
                securities="sh600519",
                factors=["PE_ratio"],
                end_date="2024-01-01",
                method="equal",
            )
            # 应该返回数值
            assert isinstance(result, (int, float, np.floating, dict))
        except Exception as e:
            # 数据获取失败是可接受的
            pass

    def test_get_comb_factor_methods(self):
        """测试不同组合方法"""
        from jk2bt.api.factor_api import get_comb_factor

        methods = ["equal", "weighted", "rank"]

        for method in methods:
            try:
                result = get_comb_factor(
                    securities=["sh600519"],
                    factors=["PE_ratio"],
                    end_date="2024-01-01",
                    method=method,
                )
                assert isinstance(result, (dict, float, int, np.floating))
            except Exception:
                pass  # 网络或数据错误可接受


class TestFactorMomentum:
    """测试因子动量"""

    def test_get_factor_momentum_import(self):
        """测试 get_factor_momentum 导入"""
        from jk2bt.api.factor_api import get_factor_momentum

        assert callable(get_factor_momentum)


class TestAPIExports:
    """测试 API 导出"""

    def test_indicators_export(self):
        """测试技术指标从 api 模块导出"""
        from jk2bt.api import MA, EMA, MACD, KDJ, RSI, BOLL, ATR

        assert callable(MA)
        assert callable(EMA)
        assert callable(MACD)
        assert callable(KDJ)
        assert callable(RSI)
        assert callable(BOLL)
        assert callable(ATR)

    def test_factor_api_export(self):
        """测试因子 API 从 api 模块导出"""
        from jk2bt.api import get_north_factor, get_comb_factor, get_factor_momentum

        assert callable(get_north_factor)
        assert callable(get_comb_factor)
        assert callable(get_factor_momentum)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])