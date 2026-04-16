"""
tests/test_signals_breakthrough_signals.py
突破类信号检测模块单元测试。

覆盖：
- detect_price_breakout
- detect_volume_breakout
- detect_boll_breakout
- detect_ma_breakout
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from jk2bt.signals.breakthrough_signals import (
    detect_price_breakout,
    detect_volume_breakout,
    detect_boll_breakout,
    detect_ma_breakout,
    detect_all_breakthrough_signals,
)


def _make_ohlcv(
    dates,
    opens,
    highs,
    lows,
    closes,
    volumes,
):
    """构造 OHLCV DataFrame，包含 date 列（与 _fetch_ohlcv 输出一致）。"""
    return pd.DataFrame(
        {
            "datetime": pd.to_datetime(dates),
            "date": dates,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
            "amount": [o * v for o, v in zip(opens, volumes)],
        }
    )


def _mock_fetch(ohlcv_df):
    """返回一个 mock，让 _fetch_ohlcv 返回指定 DataFrame。"""
    return patch(
        "jk2bt.signals.breakthrough_signals._fetch_ohlcv",
        return_value=ohlcv_df,
    )


# =====================================================================
# detect_price_breakout
# =====================================================================


class TestDetectPriceBreakout:
    def test_breakout_high_signal(self):
        """构造最后一天收盘价突破过去 20 日最高价的场景。"""
        window = 20
        n = window + 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n
        # 最后一天大幅上涨突破
        closes[-1] = 11.0
        highs[-1] = 11.2

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_price_breakout("sh600000", window=window)

        assert not result.empty
        assert (result["signal"] == 1).any()
        assert "price_breakout_high_20d" in result["type"].values

    def test_breakout_low_signal(self):
        """构造最后一天收盘价跌破过去 20 日最低价的场景。"""
        window = 20
        n = window + 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n
        # 最后一天大幅下跌跌破
        closes[-1] = 9.0
        lows[-1] = 8.8

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_price_breakout("sh600000", window=window)

        assert not result.empty
        assert (result["signal"] == -1).any()
        assert "price_breakout_low_20d" in result["type"].values

    def test_no_signal(self):
        """价格在区间内波动，不突破任何高低点。"""
        window = 20
        n = window + 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0 + i * 0.01 for i in range(n)]
        highs = [10.5 + i * 0.01 for i in range(n)]
        lows = [9.5 + i * 0.01 for i in range(n)]
        opens = [10.0 + i * 0.01 for i in range(n)]
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_price_breakout("sh600000", window=window)

        assert result.empty

    def test_insufficient_data(self):
        """数据长度不足 window + 1 天。"""
        window = 20
        n = 5  # 远小于 window
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_price_breakout("sh600000", window=window)

        assert result.empty

    def test_empty_dataframe(self):
        """输入空 DataFrame。"""
        df = pd.DataFrame()
        with _mock_fetch(df):
            result = detect_price_breakout("sh600000", window=20)
        assert result.empty

    def test_missing_close_column(self):
        """DataFrame 缺少 close 列。"""
        df = pd.DataFrame(
            {"open": [10.0], "high": [10.5], "low": [9.5], "volume": [1_000_000]}
        )
        with _mock_fetch(df):
            result = detect_price_breakout("sh600000", window=20)
        assert result.empty

    def test_result_columns(self):
        """验证返回结果包含预期列。"""
        window = 20
        n = window + 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        closes[-1] = 15.0
        highs = [10.5] * n
        highs[-1] = 15.2
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_price_breakout("sh600000", window=window)

        expected_cols = {"date", "signal", "type", "close", "high_n", "low_n"}
        assert expected_cols.issubset(set(result.columns))


# =====================================================================
# detect_volume_breakout
# =====================================================================


class TestDetectVolumeBreakout:
    def test_volume_breakout_high(self):
        """构造成交量异常放大的场景。"""
        window = 20
        n = window + 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n
        # 最后一天成交量放大 5 倍
        volumes[-1] = 10_000_000

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_volume_breakout("sh600000", window=window, multiplier=2.0)

        assert not result.empty
        assert (result["signal"] == 1).any()
        assert "volume_breakout_high_2.0x" in result["type"].values

    def test_volume_breakout_low(self):
        """构造成交量异常缩小的场景。"""
        window = 20
        n = window + 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        # 前 window 天成交量很大，最后一天极度缩量
        volumes = [5_000_000] * n
        volumes[-1] = 100_000  # 远小于均量的 1/2

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_volume_breakout("sh600000", window=window, multiplier=2.0)

        assert not result.empty
        assert (result["signal"] == -1).any()
        assert "volume_breakout_low_2.0x" in result["type"].values

    def test_no_signal(self):
        """成交量正常波动，不触发信号。"""
        window = 20
        n = window + 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_volume_breakout("sh600000", window=window, multiplier=2.0)

        assert result.empty

    def test_insufficient_data(self):
        """数据长度不足。"""
        window = 20
        n = 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_volume_breakout("sh600000", window=window)

        assert result.empty

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        with _mock_fetch(df):
            result = detect_volume_breakout("sh600000", window=20)
        assert result.empty

    def test_missing_volume_column(self):
        df = pd.DataFrame(
            {
                "datetime": pd.to_datetime(["2024-01-01"]),
                "close": [10.0],
                "open": [10.0],
                "high": [10.5],
                "low": [9.5],
            }
        )
        with _mock_fetch(df):
            result = detect_volume_breakout("sh600000", window=20)
        assert result.empty

    def test_result_columns(self):
        window = 20
        n = window + 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n
        volumes[-1] = 10_000_000

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_volume_breakout("sh600000", window=window, multiplier=2.0)

        expected_cols = {
            "date",
            "signal",
            "type",
            "volume",
            "avg_volume",
            "volume_ratio",
        }
        assert expected_cols.issubset(set(result.columns))


# =====================================================================
# detect_boll_breakout
# =====================================================================


class TestDetectBollBreakout:
    def test_boll_breakout_up(self):
        """构造价格上穿布林上轨的场景。"""
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        # 前 window 天价格稳定在 10 附近
        closes = [10.0] * n
        highs = [10.3] * n
        lows = [9.7] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        # 倒数第二天还在布林带内
        closes[-2] = 10.0
        # 最后一天大幅上涨突破上轨
        closes[-1] = 15.0
        highs[-1] = 15.5

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_boll_breakout("sh600000", window=window, num_std=2.0)

        assert not result.empty
        assert (result["signal"] == 1).any()
        assert "boll_breakout_up" in result["type"].values

    def test_boll_breakout_down(self):
        """构造价格下穿布林下轨的场景。"""
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.3] * n
        lows = [9.7] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        # 倒数第二天还在布林带内
        closes[-2] = 10.0
        # 最后一天大幅下跌突破下轨
        closes[-1] = 5.0
        lows[-1] = 4.5

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_boll_breakout("sh600000", window=window, num_std=2.0)

        assert not result.empty
        assert (result["signal"] == -1).any()
        assert "boll_breakout_down" in result["type"].values

    def test_no_signal(self):
        """价格在布林带内波动，不触发突破。"""
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        # 价格恒定在 10，布林带会收敛到极窄范围，但仍不会突破
        closes = [10.0] * n
        highs = [10.01] * n
        lows = [9.99] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_boll_breakout("sh600000", window=window, num_std=2.0)

        assert result.empty

    def test_insufficient_data(self):
        window = 20
        n = 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_boll_breakout("sh600000", window=window)

        assert result.empty

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        with _mock_fetch(df):
            result = detect_boll_breakout("sh600000", window=20)
        assert result.empty

    def test_missing_close_column(self):
        df = pd.DataFrame(
            {"open": [10.0], "high": [10.5], "low": [9.5], "volume": [1_000_000]}
        )
        with _mock_fetch(df):
            result = detect_boll_breakout("sh600000", window=20)
        assert result.empty

    def test_result_columns(self):
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        closes[-1] = 15.0
        highs = [10.3] * n
        highs[-1] = 15.5
        lows = [9.7] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_boll_breakout("sh600000", window=window, num_std=2.0)

        expected_cols = {
            "date",
            "signal",
            "type",
            "close",
            "boll_up",
            "boll_down",
            "boll_ma",
        }
        assert expected_cols.issubset(set(result.columns))


# =====================================================================
# detect_ma_breakout
# =====================================================================


class TestDetectMABreakout:
    def test_ma_breakout_up(self):
        """构造价格上穿均线的场景。"""
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        # 前 window 天价格逐步下跌到均线下方
        closes = [12.0 - i * 0.1 for i in range(n)]
        highs = [c + 0.1 for c in closes]
        lows = [c - 0.1 for c in closes]
        opens = list(closes)
        volumes = [1_000_000] * n

        # 最后一天大幅上涨穿越均线
        closes[-1] = 20.0
        highs[-1] = 20.5
        lows[-1] = 19.5

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_ma_breakout("sh600000", window=window)

        assert not result.empty
        assert (result["signal"] == 1).any()
        assert "ma_20_breakout_up" in result["type"].values

    def test_ma_breakout_down(self):
        """构造价格下穿均线的场景。"""
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        # 前 window 天价格逐步上涨到均线上方
        closes = [8.0 + i * 0.1 for i in range(n)]
        highs = [c + 0.1 for c in closes]
        lows = [c - 0.1 for c in closes]
        opens = list(closes)
        volumes = [1_000_000] * n

        # 最后一天大幅下跌穿越均线
        closes[-1] = 2.0
        highs[-1] = 2.5
        lows[-1] = 1.5

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_ma_breakout("sh600000", window=window)

        assert not result.empty
        assert (result["signal"] == -1).any()
        assert "ma_20_breakout_down" in result["type"].values

    def test_no_signal(self):
        """价格一直在均线上方，不触发穿越。"""
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [15.0 + i * 0.1 for i in range(n)]
        highs = [c + 0.1 for c in closes]
        lows = [c - 0.1 for c in closes]
        opens = list(closes)
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_ma_breakout("sh600000", window=window)

        assert result.empty

    def test_insufficient_data(self):
        window = 20
        n = 5
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        highs = [10.5] * n
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_ma_breakout("sh600000", window=window)

        assert result.empty

    def test_empty_dataframe(self):
        df = pd.DataFrame()
        with _mock_fetch(df):
            result = detect_ma_breakout("sh600000", window=20)
        assert result.empty

    def test_missing_close_column(self):
        df = pd.DataFrame(
            {"open": [10.0], "high": [10.5], "low": [9.5], "volume": [1_000_000]}
        )
        with _mock_fetch(df):
            result = detect_ma_breakout("sh600000", window=20)
        assert result.empty

    def test_result_columns(self):
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [12.0 - i * 0.1 for i in range(n)]
        closes[-1] = 20.0
        highs = [c + 0.1 for c in closes]
        lows = [c - 0.1 for c in closes]
        opens = list(closes)
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_ma_breakout("sh600000", window=window)

        expected_cols = {"date", "signal", "type", "close", "ma_20"}
        assert expected_cols.issubset(set(result.columns))


# =====================================================================
# detect_all_breakthrough_signals
# =====================================================================


class TestDetectAllBreakthroughSignals:
    def test_returns_combined_signals(self):
        """测试多个信号同时触发的场景。"""
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        closes[-1] = 15.0  # 价格突破
        highs = [10.5] * n
        highs[-1] = 15.5
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n
        volumes[-1] = 10_000_000  # 成交量突破

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_all_breakthrough_signals("sh600000")

        assert not result.empty
        assert "date" in result.columns
        assert "signal" in result.columns
        assert "type" in result.columns

    def test_empty_when_no_signals(self):
        """无信号时返回空 DataFrame。"""
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0 + i * 0.01 for i in range(n)]
        highs = [10.5 + i * 0.01 for i in range(n)]
        lows = [9.5 + i * 0.01 for i in range(n)]
        opens = [10.0 + i * 0.01 for i in range(n)]
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)
        with _mock_fetch(df):
            result = detect_all_breakthrough_signals("sh600000")

        assert result.empty

    def test_handles_individual_failure_gracefully(self):
        """某个信号检测失败时不影响其他信号。"""
        window = 20
        n = window + 10
        dates = pd.date_range("2024-01-01", periods=n, freq="B").strftime("%Y-%m-%d")
        closes = [10.0] * n
        closes[-1] = 15.0
        highs = [10.5] * n
        highs[-1] = 15.5
        lows = [9.5] * n
        opens = [10.0] * n
        volumes = [1_000_000] * n

        df = _make_ohlcv(dates, opens, highs, lows, closes, volumes)

        def mock_fetch_side_effect(symbol, end_date=None, count=None):
            return df

        with patch(
            "jk2bt.signals.breakthrough_signals._fetch_ohlcv",
            side_effect=mock_fetch_side_effect,
        ):
            with patch(
                "jk2bt.signals.breakthrough_signals.detect_volume_breakout",
                side_effect=Exception("mock error"),
            ):
                result = detect_all_breakthrough_signals("sh600000")

        # 价格突破应该仍然有效
        assert not result.empty
