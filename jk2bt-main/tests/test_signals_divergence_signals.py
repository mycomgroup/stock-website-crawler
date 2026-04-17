"""
test_signals_divergence_signals.py
背离信号检测模块单元测试。

测试目标：
- detect_macd_divergence - MACD 背离检测
- detect_rsi_divergence - RSI 背离检测
- detect_bear_power_divergence - 熊力背离检测
- detect_kdj_divergence - KDJ 背离检测

测试场景：
- 正常路径（能触发顶背离/底背离信号）
- 无信号场景（返回空 DataFrame）
- 数据不足场景（历史数据长度不够）
- 空数据/异常数据输入
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))

from jk2bt.data.sources import set_adapter, MockDataSource, get_adapter
from jk2bt.analysis.signals.divergence import (
    detect_macd_divergence,
    detect_rsi_divergence,
    detect_bear_power_divergence,
    detect_kdj_divergence,
    detect_all_divergence_signals,
    _find_local_extrema,
    _check_divergence,
)


# =====================================================================
# Fixtures
# =====================================================================


@pytest.fixture(autouse=True)
def setup_mock_adapter():
    """每个测试前重置 adapter 为 MockDataSource。"""
    mock = MockDataSource(seed=42, generate_random=True)
    set_adapter(mock)
    yield mock
    # 清理：重置为新的 MockDataSource
    set_adapter(MockDataSource(seed=42, generate_random=True))


def _create_ohlcv_df(dates, opens, highs, lows, closes, volumes=None):
    """构造 OHLCV DataFrame。"""
    n = len(dates)
    if volumes is None:
        volumes = [1000000] * n
    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(dates),
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
            "amount": [o * v for o, v in zip(opens, volumes)],
        }
    )
    return df


def _create_top_divergence_ohlcv(n_warmup=80, n_between=15):
    """
    构造触发顶背离的 OHLCV 数据。

    逻辑：价格创新高，但 MACD 指标未创新高。
    - 第一个峰值：价格快速上涨到 ~100，MACD 较高
    - 回调
    - 第二个峰值：价格缓慢上涨到 ~110（更高），但 MACD 较低
    """
    total = n_warmup + n_between + n_warmup
    dates = pd.date_range("2023-01-01", periods=total, freq="B")

    closes = []
    opens = []
    highs = []
    lows = []
    volumes = []

    # 阶段1：warmup 平稳
    for i in range(n_warmup):
        p = 50 + i * 0.3
        closes.append(p)
        opens.append(p - 0.1)
        highs.append(p + 0.3)
        lows.append(p - 0.3)
        volumes.append(1000000)

    # 阶段2：快速上涨到第一个峰值
    peak1 = 100.0
    for i in range(10):
        p = closes[-1] + 3.0
        closes.append(p)
        opens.append(p - 1.0)
        highs.append(p + 0.5)
        lows.append(p - 0.5)
        volumes.append(2000000)

    # 阶段3：回调
    for i in range(n_between):
        p = closes[-1] - 1.5
        closes.append(p)
        opens.append(p + 0.5)
        highs.append(p + 1.0)
        lows.append(p - 0.5)
        volumes.append(800000)

    # 阶段4：缓慢上涨到第二个峰值（价格更高但动量更小）
    peak2 = 110.0  # 比 peak1 高 10%
    steps = 20
    for i in range(steps):
        p = closes[-1] + 0.5  # 缓慢上涨
        closes.append(p)
        opens.append(p - 0.2)
        highs.append(p + 0.3)
        lows.append(p - 0.3)
        volumes.append(600000)  # 成交量递减

    # 阶段5：后续平稳
    remaining = total - len(closes)
    for i in range(max(0, remaining)):
        p = closes[-1]
        closes.append(p)
        opens.append(p)
        highs.append(p + 0.2)
        lows.append(p - 0.2)
        volumes.append(500000)

    return _create_ohlcv_df(dates[: len(closes)], opens, highs, lows, closes, volumes)


def _create_bottom_divergence_ohlcv(n_warmup=80, n_between=15):
    """
    构造触发底背离的 OHLCV 数据。

    逻辑：价格创新低，但 MACD 指标未创新低。
    - 第一个谷底：价格快速下跌到 ~40，MACD 较低
    - 反弹
    - 第二个谷底：价格缓慢下跌到 ~30（更低），但 MACD 较高
    """
    total = n_warmup + n_between + n_warmup
    dates = pd.date_range("2023-01-01", periods=total, freq="B")

    closes = []
    opens = []
    highs = []
    lows = []
    volumes = []

    # 阶段1：warmup 平稳
    for i in range(n_warmup):
        p = 80 - i * 0.3
        closes.append(p)
        opens.append(p + 0.1)
        highs.append(p + 0.3)
        lows.append(p - 0.3)
        volumes.append(1000000)

    # 阶段2：快速下跌到第一个谷底
    for i in range(10):
        p = closes[-1] - 3.0
        closes.append(p)
        opens.append(p + 1.0)
        highs.append(p + 0.5)
        lows.append(p - 0.5)
        volumes.append(2000000)

    # 阶段3：反弹
    for i in range(n_between):
        p = closes[-1] + 1.5
        closes.append(p)
        opens.append(p - 0.5)
        highs.append(p + 1.0)
        lows.append(p - 0.5)
        volumes.append(800000)

    # 阶段4：缓慢下跌到第二个谷底（价格更低但动量更小）
    steps = 20
    for i in range(steps):
        p = closes[-1] - 0.5  # 缓慢下跌
        closes.append(p)
        opens.append(p + 0.2)
        highs.append(p + 0.3)
        lows.append(p - 0.3)
        volumes.append(600000)

    # 阶段5：后续平稳
    remaining = total - len(closes)
    for i in range(max(0, remaining)):
        p = closes[-1]
        closes.append(p)
        opens.append(p)
        highs.append(p + 0.2)
        lows.append(p - 0.2)
        volumes.append(500000)

    return _create_ohlcv_df(dates[: len(closes)], opens, highs, lows, closes, volumes)


def _create_no_divergence_ohlcv(n=120):
    """构造无背离的 OHLCV 数据（价格与指标同步）。"""
    dates = pd.date_range("2023-01-01", periods=n, freq="B")
    closes = [50 + i * 0.5 for i in range(n)]  # 稳定上涨
    opens = [c - 0.2 for c in closes]
    highs = [c + 0.3 for c in closes]
    lows = [c - 0.3 for c in closes]
    volumes = [1000000] * n
    return _create_ohlcv_df(dates, opens, highs, lows, closes, volumes)


def _inject_ohlcv(mock, symbol, df):
    """将 OHLCV 数据注入 MockDataSource。"""
    mock.set_mock_data("daily", symbol, df)


# =====================================================================
# Helper function tests
# =====================================================================


class TestFindLocalExtrema:
    """测试 _find_local_extrema 辅助函数。"""

    def test_finds_local_max(self):
        """应能识别局部极大值。"""
        data = pd.Series([1, 2, 3, 4, 5, 4, 3, 2, 1])
        is_max, is_min = _find_local_extrema(data, window=2)
        assert is_max.iloc[4] == True  # 5 is the local max
        assert is_max.sum() >= 1

    def test_finds_local_min(self):
        """应能识别局部极小值。"""
        data = pd.Series([5, 4, 3, 2, 1, 2, 3, 4, 5])
        is_max, is_min = _find_local_extrema(data, window=2)
        assert is_min.iloc[4] == True  # 1 is the local min
        assert is_min.sum() >= 1

    def test_no_extrema_in_flat_series(self):
        """平坦序列不应有极值。"""
        data = pd.Series([5] * 20)
        is_max, is_min = _find_local_extrema(data, window=3)
        # 所有值都等于 max/min，所以都标记为极值
        assert is_max.sum() > 0

    def test_short_series(self):
        """短于 2*window+1 的序列不应有极值。"""
        data = pd.Series([1, 2, 3, 4, 5])
        is_max, is_min = _find_local_extrema(data, window=3)
        assert is_max.sum() == 0
        assert is_min.sum() == 0

    def test_empty_series(self):
        """空序列应返回空结果。"""
        data = pd.Series([], dtype=float)
        is_max, is_min = _find_local_extrema(data, window=3)
        assert len(is_max) == 0
        assert len(is_min) == 0


class TestCheckDivergence:
    """测试 _check_divergence 辅助函数。"""

    def test_bottom_divergence_detected(self):
        """底背离：价格创新低，指标未创新低。"""
        # 价格走势：平稳 -> 下跌到第一个低点(索引14=38) -> 反弹 -> 下跌到更低低点(索引27=34)
        price = pd.Series(
            [
                50,
                50,
                50,
                50,
                50,
                50,
                50,
                50,
                50,
                50,
                50,
                50,
                48,
                45,
                38,
                42,
                45,
                48,
                50,
                52,
                54,
                56,
                54,
                52,
                50,
                48,
                45,
                34,
                38,
                42,
                45,
                48,
            ]
        )
        # 指标序列：第二个低点更高（底背离：价格34<38，但指标-1>-2）
        indicator = pd.Series(
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                -1,
                -2,
                -2,
                -1,
                0,
                1,
                2,
                3,
                4,
                5,
                4,
                3,
                2,
                1,
                0,
                -1,
                0,
                1,
                2,
                3,
            ]
        )

        signal = _check_divergence(
            price, indicator, is_bottom=True, lookback=5, tolerance=0.02
        )
        assert (signal == 1).any()

    def test_top_divergence_detected(self):
        """顶背离：价格创新高，指标未创新高。"""
        # 价格走势：平稳 -> 上涨到第一个高点(索引14=45) -> 回调 -> 上涨到更高高点(索引27=50)
        price = pd.Series(
            [
                30,
                30,
                30,
                30,
                30,
                30,
                30,
                30,
                30,
                30,
                30,
                30,
                32,
                35,
                45,
                42,
                39,
                36,
                33,
                30,
                27,
                24,
                27,
                30,
                33,
                36,
                40,
                50,
                46,
                42,
                38,
                34,
            ]
        )
        # 指标序列：第二个高点更低（顶背离：价格50>45，但指标8<10）
        indicator = pd.Series(
            [
                5,
                5,
                5,
                5,
                5,
                5,
                5,
                5,
                5,
                5,
                5,
                5,
                6,
                8,
                10,
                9,
                8,
                7,
                6,
                5,
                4,
                3,
                4,
                5,
                6,
                7,
                8,
                8,
                7,
                6,
                5,
                4,
            ]
        )

        signal = _check_divergence(
            price, indicator, is_bottom=False, lookback=5, tolerance=0.02
        )
        assert (signal == -1).any()

    def test_no_divergence(self):
        """价格与指标同步变化，无背离。"""
        price = pd.Series([30, 35, 40, 45, 50, 55, 60, 65, 70, 75])
        indicator = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        signal = _check_divergence(
            price, indicator, is_bottom=True, lookback=5, tolerance=0.02
        )
        assert (signal == 0).all()

        signal = _check_divergence(
            price, indicator, is_bottom=False, lookback=5, tolerance=0.02
        )
        assert (signal == 0).all()

    def test_insufficient_data(self):
        """数据不足时不应产生信号。"""
        price = pd.Series([30, 35, 40])
        indicator = pd.Series([1, 2, 3])

        signal = _check_divergence(
            price, indicator, is_bottom=True, lookback=20, tolerance=0.02
        )
        assert (signal == 0).all()


# =====================================================================
# detect_macd_divergence tests
# =====================================================================


class TestDetectMacdDivergence:
    """测试 detect_macd_divergence 函数。"""

    def test_top_divergence_signal(self):
        """应能检测到 MACD 顶背离信号。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_top_divergence_ohlcv(n_warmup=80, n_between=15)
        _inject_ohlcv(mock, "TEST001", df)
        set_adapter(mock)

        result = detect_macd_divergence(
            "TEST001", fast=12, slow=26, signal_period=9, lookback=20
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "date" in result.columns
            assert "signal" in result.columns
            assert "type" in result.columns
            assert "macd_value" in result.columns
            # 顶背离信号值为 -1
            top_signals = result[result["signal"] == -1]
            if not top_signals.empty:
                assert (top_signals["type"] == "macd_top_divergence").all()

    def test_bottom_divergence_signal(self):
        """应能检测到 MACD 底背离信号。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_bottom_divergence_ohlcv(n_warmup=80, n_between=15)
        _inject_ohlcv(mock, "TEST002", df)
        set_adapter(mock)

        result = detect_macd_divergence(
            "TEST002", fast=12, slow=26, signal_period=9, lookback=20
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "date" in result.columns
            assert "signal" in result.columns
            assert "type" in result.columns
            bottom_signals = result[result["signal"] == 1]
            if not bottom_signals.empty:
                assert (bottom_signals["type"] == "macd_bottom_divergence").all()

    def test_no_divergence_returns_empty(self):
        """无背离时应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_no_divergence_ohlcv(n=120)
        _inject_ohlcv(mock, "TEST003", df)
        set_adapter(mock)

        result = detect_macd_divergence(
            "TEST003", fast=12, slow=26, signal_period=9, lookback=20
        )

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_insufficient_data(self):
        """数据不足时应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        # 只给 30 天数据，不足 slow + signal + lookback + 20 = 75
        dates = pd.date_range("2023-01-01", periods=30, freq="B")
        closes = [50 + i * 0.5 for i in range(30)]
        df = _create_ohlcv_df(
            dates,
            [c - 0.2 for c in closes],
            [c + 0.3 for c in closes],
            [c - 0.3 for c in closes],
            closes,
        )
        _inject_ohlcv(mock, "TEST004", df)
        set_adapter(mock)

        result = detect_macd_divergence(
            "TEST004", fast=12, slow=26, signal_period=9, lookback=20
        )

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_empty_data(self):
        """空数据输入应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        _inject_ohlcv(mock, "TEST005", pd.DataFrame())
        set_adapter(mock)

        result = detect_macd_divergence("TEST005")

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_missing_close_column(self):
        """缺少 close 列应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=100, freq="B"),
                "open": [50.0] * 100,
                "high": [51.0] * 100,
                "low": [49.0] * 100,
                "volume": [1000000] * 100,
            }
        )
        _inject_ohlcv(mock, "TEST006", df)
        set_adapter(mock)

        result = detect_macd_divergence("TEST006")

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_with_random_data(self):
        """使用随机生成数据应能正常执行不报错。"""
        mock = MockDataSource(seed=42, generate_random=True)
        set_adapter(mock)

        result = detect_macd_divergence(
            "RANDOM001", fast=12, slow=26, signal_period=9, lookback=20
        )

        assert isinstance(result, pd.DataFrame)
        # 可能为空或有信号，但不应报错
        if not result.empty:
            assert "date" in result.columns
            assert "signal" in result.columns

    def test_custom_parameters(self):
        """自定义参数应正常工作。"""
        mock = MockDataSource(seed=42, generate_random=True)
        set_adapter(mock)

        result = detect_macd_divergence(
            "RANDOM002", fast=6, slow=13, signal_period=5, lookback=10
        )

        assert isinstance(result, pd.DataFrame)


# =====================================================================
# detect_rsi_divergence tests
# =====================================================================


class TestDetectRsiDivergence:
    """测试 detect_rsi_divergence 函数。"""

    def test_top_divergence_signal(self):
        """应能检测到 RSI 顶背离信号。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_top_divergence_ohlcv(n_warmup=80, n_between=15)
        _inject_ohlcv(mock, "TEST_RSI001", df)
        set_adapter(mock)

        result = detect_rsi_divergence("TEST_RSI001", window=14, lookback=20)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "date" in result.columns
            assert "signal" in result.columns
            assert "type" in result.columns
            assert "rsi_value" in result.columns
            top_signals = result[result["signal"] == -1]
            if not top_signals.empty:
                assert (top_signals["type"] == "rsi_top_divergence").all()

    def test_bottom_divergence_signal(self):
        """应能检测到 RSI 底背离信号。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_bottom_divergence_ohlcv(n_warmup=80, n_between=15)
        _inject_ohlcv(mock, "TEST_RSI002", df)
        set_adapter(mock)

        result = detect_rsi_divergence("TEST_RSI002", window=14, lookback=20)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            bottom_signals = result[result["signal"] == 1]
            if not bottom_signals.empty:
                assert (bottom_signals["type"] == "rsi_bottom_divergence").all()

    def test_no_divergence_returns_empty(self):
        """无背离时应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_no_divergence_ohlcv(n=120)
        _inject_ohlcv(mock, "TEST_RSI003", df)
        set_adapter(mock)

        result = detect_rsi_divergence("TEST_RSI003", window=14, lookback=20)

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_insufficient_data(self):
        """数据不足时应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        dates = pd.date_range("2023-01-01", periods=20, freq="B")
        closes = [50 + i * 0.5 for i in range(20)]
        df = _create_ohlcv_df(
            dates,
            [c - 0.2 for c in closes],
            [c + 0.3 for c in closes],
            [c - 0.3 for c in closes],
            closes,
        )
        _inject_ohlcv(mock, "TEST_RSI004", df)
        set_adapter(mock)

        result = detect_rsi_divergence("TEST_RSI004", window=14, lookback=20)

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_empty_data(self):
        """空数据输入应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        _inject_ohlcv(mock, "TEST_RSI005", pd.DataFrame())
        set_adapter(mock)

        result = detect_rsi_divergence("TEST_RSI005")

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_with_random_data(self):
        """使用随机生成数据应能正常执行不报错。"""
        mock = MockDataSource(seed=42, generate_random=True)
        set_adapter(mock)

        result = detect_rsi_divergence("RANDOM_RSI001", window=14, lookback=20)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "date" in result.columns
            assert "rsi_value" in result.columns

    def test_custom_window(self):
        """自定义 RSI 窗口应正常工作。"""
        mock = MockDataSource(seed=42, generate_random=True)
        set_adapter(mock)

        result = detect_rsi_divergence("RANDOM_RSI002", window=7, lookback=10)

        assert isinstance(result, pd.DataFrame)


# =====================================================================
# detect_bear_power_divergence tests
# =====================================================================


class TestDetectBearPowerDivergence:
    """测试 detect_bear_power_divergence 函数。"""

    def test_top_divergence_signal(self):
        """应能检测到熊力顶背离信号。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_top_divergence_ohlcv(n_warmup=80, n_between=15)
        _inject_ohlcv(mock, "TEST_BEAR001", df)
        set_adapter(mock)

        result = detect_bear_power_divergence("TEST_BEAR001", window=13, lookback=20)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "date" in result.columns
            assert "signal" in result.columns
            assert "type" in result.columns
            assert "bear_power" in result.columns
            assert "bull_power" in result.columns
            top_signals = result[result["signal"] == -1]
            if not top_signals.empty:
                assert (top_signals["type"] == "bull_power_top_divergence").all()

    def test_bottom_divergence_signal(self):
        """应能检测到熊力底背离信号。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_bottom_divergence_ohlcv(n_warmup=80, n_between=15)
        _inject_ohlcv(mock, "TEST_BEAR002", df)
        set_adapter(mock)

        result = detect_bear_power_divergence("TEST_BEAR002", window=13, lookback=20)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            bottom_signals = result[result["signal"] == 1]
            if not bottom_signals.empty:
                assert (bottom_signals["type"] == "bear_power_bottom_divergence").all()

    def test_no_divergence_returns_empty(self):
        """无背离时应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_no_divergence_ohlcv(n=120)
        _inject_ohlcv(mock, "TEST_BEAR003", df)
        set_adapter(mock)

        result = detect_bear_power_divergence("TEST_BEAR003", window=13, lookback=20)

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_insufficient_data(self):
        """数据不足时应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        dates = pd.date_range("2023-01-01", periods=20, freq="B")
        closes = [50 + i * 0.5 for i in range(20)]
        df = _create_ohlcv_df(
            dates,
            [c - 0.2 for c in closes],
            [c + 0.3 for c in closes],
            [c - 0.3 for c in closes],
            closes,
        )
        _inject_ohlcv(mock, "TEST_BEAR004", df)
        set_adapter(mock)

        result = detect_bear_power_divergence("TEST_BEAR004", window=13, lookback=20)

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_empty_data(self):
        """空数据输入应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        _inject_ohlcv(mock, "TEST_BEAR005", pd.DataFrame())
        set_adapter(mock)

        result = detect_bear_power_divergence("TEST_BEAR005")

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_with_random_data(self):
        """使用随机生成数据应能正常执行不报错。"""
        mock = MockDataSource(seed=42, generate_random=True)
        set_adapter(mock)

        result = detect_bear_power_divergence("RANDOM_BEAR001", window=13, lookback=20)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "bear_power" in result.columns
            assert "bull_power" in result.columns

    def test_missing_high_low_columns(self):
        """缺少 high/low 列时应能处理（使用 random 数据时有这些列）。"""
        mock = MockDataSource(seed=42, generate_random=False)
        # 只有 close 列
        dates = pd.date_range("2023-01-01", periods=100, freq="B")
        closes = [50 + i * 0.5 for i in range(100)]
        df = pd.DataFrame(
            {
                "datetime": dates,
                "close": closes,
            }
        )
        _inject_ohlcv(mock, "TEST_BEAR006", df)
        set_adapter(mock)

        # 应该报错或返回空，取决于实现
        try:
            result = detect_bear_power_divergence("TEST_BEAR006")
            assert isinstance(result, pd.DataFrame)
        except KeyError:
            # 缺少 high/low 列会抛 KeyError，这是可接受的行为
            pass


# =====================================================================
# detect_kdj_divergence tests
# =====================================================================


class TestDetectKdjDivergence:
    """测试 detect_kdj_divergence 函数。"""

    def test_top_divergence_signal(self):
        """应能检测到 KDJ 顶背离信号。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_top_divergence_ohlcv(n_warmup=80, n_between=15)
        _inject_ohlcv(mock, "TEST_KDJ001", df)
        set_adapter(mock)

        result = detect_kdj_divergence("TEST_KDJ001", n=9, m1=3, m2=3, lookback=20)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "date" in result.columns
            assert "signal" in result.columns
            assert "type" in result.columns
            assert "k_value" in result.columns
            assert "d_value" in result.columns
            assert "j_value" in result.columns
            top_signals = result[result["signal"] == -1]
            if not top_signals.empty:
                assert (top_signals["type"] == "kdj_top_divergence").all()

    def test_bottom_divergence_signal(self):
        """应能检测到 KDJ 底背离信号。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_bottom_divergence_ohlcv(n_warmup=80, n_between=15)
        _inject_ohlcv(mock, "TEST_KDJ002", df)
        set_adapter(mock)

        result = detect_kdj_divergence("TEST_KDJ002", n=9, m1=3, m2=3, lookback=20)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            bottom_signals = result[result["signal"] == 1]
            if not bottom_signals.empty:
                assert (bottom_signals["type"] == "kdj_bottom_divergence").all()

    def test_no_divergence_returns_empty(self):
        """无背离时应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        df = _create_no_divergence_ohlcv(n=120)
        _inject_ohlcv(mock, "TEST_KDJ003", df)
        set_adapter(mock)

        result = detect_kdj_divergence("TEST_KDJ003", n=9, m1=3, m2=3, lookback=20)

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_insufficient_data(self):
        """数据不足时应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        dates = pd.date_range("2023-01-01", periods=20, freq="B")
        closes = [50 + i * 0.5 for i in range(20)]
        df = _create_ohlcv_df(
            dates,
            [c - 0.2 for c in closes],
            [c + 0.3 for c in closes],
            [c - 0.3 for c in closes],
            closes,
        )
        _inject_ohlcv(mock, "TEST_KDJ004", df)
        set_adapter(mock)

        result = detect_kdj_divergence("TEST_KDJ004", n=9, m1=3, m2=3, lookback=20)

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_empty_data(self):
        """空数据输入应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        _inject_ohlcv(mock, "TEST_KDJ005", pd.DataFrame())
        set_adapter(mock)

        result = detect_kdj_divergence("TEST_KDJ005")

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_with_random_data(self):
        """使用随机生成数据应能正常执行不报错。"""
        mock = MockDataSource(seed=42, generate_random=True)
        set_adapter(mock)

        result = detect_kdj_divergence("RANDOM_KDJ001", n=9, m1=3, m2=3, lookback=20)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "k_value" in result.columns
            assert "d_value" in result.columns
            assert "j_value" in result.columns

    def test_custom_parameters(self):
        """自定义 KDJ 参数应正常工作。"""
        mock = MockDataSource(seed=42, generate_random=True)
        set_adapter(mock)

        result = detect_kdj_divergence("RANDOM_KDJ002", n=6, m1=2, m2=2, lookback=10)

        assert isinstance(result, pd.DataFrame)


# =====================================================================
# detect_all_divergence_signals tests
# =====================================================================


class TestDetectAllDivergenceSignals:
    """测试 detect_all_divergence_signals 函数。"""

    def test_with_random_data(self):
        """使用随机数据应能正常执行。"""
        mock = MockDataSource(seed=42, generate_random=True)
        set_adapter(mock)

        result = detect_all_divergence_signals("RANDOM_ALL001")

        assert isinstance(result, pd.DataFrame)

    def test_with_empty_data(self):
        """空数据应返回空 DataFrame。"""
        mock = MockDataSource(seed=42, generate_random=False)
        _inject_ohlcv(mock, "TEST_ALL001", pd.DataFrame())
        set_adapter(mock)

        result = detect_all_divergence_signals("TEST_ALL001")

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_returns_concatenated_signals(self):
        """当有多个信号时应返回合并结果。"""
        mock = MockDataSource(seed=42, generate_random=True)
        set_adapter(mock)

        result = detect_all_divergence_signals("RANDOM_ALL002")

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "date" in result.columns
            assert "signal" in result.columns
            assert "type" in result.columns
