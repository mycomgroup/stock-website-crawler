"""
tests/unit/api/test_indicators.py
技术指标 API 单元测试（迁移自 tests/test_indicators_api.py）

测试覆盖：
- MA, EMA, MACD, KDJ, RSI, BOLL, ATR 函数导入与基本计算
- 从 src.api 顶层导出验证
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"),
)


class TestIndicatorImports:
    """技术指标函数导入测试"""

    def test_ma_importable(self):
        from jk2bt.api.indicators import MA
        assert callable(MA)

    def test_ema_importable(self):
        from jk2bt.api.indicators import EMA
        assert callable(EMA)

    def test_macd_importable(self):
        from jk2bt.api.indicators import MACD
        assert callable(MACD)

    def test_kdj_importable(self):
        from jk2bt.api.indicators import KDJ
        assert callable(KDJ)

    def test_rsi_importable(self):
        from jk2bt.api.indicators import RSI
        assert callable(RSI)

    def test_boll_importable(self):
        from jk2bt.api.indicators import BOLL
        assert callable(BOLL)

    def test_atr_importable(self):
        from jk2bt.api.indicators import ATR
        assert callable(ATR)


class TestIndicatorsFromApiInit:
    """从 src.api 顶层导入技术指标"""

    def test_all_indicators_from_api(self):
        from jk2bt.api import MA, EMA, MACD, KDJ, RSI, BOLL, ATR
        for fn in [MA, EMA, MACD, KDJ, RSI, BOLL, ATR]:
            assert callable(fn)


class TestMA:
    """MA 均线计算测试"""

    def test_ma_series_input(self):
        from jk2bt.api.indicators import MA
        close = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        result = MA(close, timeperiod=5)
        assert isinstance(result, pd.Series)
        assert len(result) == len(close)
        # 第5个值（index=4）应为前5个数的均值
        assert result.iloc[4] == pytest.approx(12.0, rel=0.01)

    def test_ma_numpy_input(self):
        from jk2bt.api.indicators import MA
        close = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19], dtype=float)
        result = MA(close, timeperiod=5)
        assert isinstance(result, np.ndarray)
        assert len(result) == len(close)

    def test_ma_list_input(self):
        from jk2bt.api.indicators import MA
        close = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        result = MA(close, timeperiod=5)
        assert isinstance(result, list)
        assert len(result) == len(close)


class TestEMA:
    """EMA 指数均线测试"""

    def test_ema_series_input(self):
        from jk2bt.api.indicators import EMA
        close = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
        result = EMA(close, timeperiod=5)
        assert isinstance(result, pd.Series)
        assert len(result) == len(close)


class TestRSI:
    """RSI 相对强弱指数测试"""

    def test_rsi_series_input(self):
        from jk2bt.api.indicators import RSI
        close = pd.Series([100 + i for i in range(30)])
        result = RSI(close, timeperiod=14)
        assert isinstance(result, pd.Series)
        # 持续上涨序列 RSI 应接近 100
        assert result.iloc[-1] > 70

    def test_rsi_numpy_input(self):
        from jk2bt.api.indicators import RSI
        close = np.array([100 + i for i in range(30)], dtype=float)
        result = RSI(close, timeperiod=14)
        assert isinstance(result, np.ndarray)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
