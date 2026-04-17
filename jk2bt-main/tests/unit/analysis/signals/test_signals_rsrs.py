"""
tests/unit/analysis/signals/test_signals_rsrs.py
单元测试：RSRS择时指标 (rsrs.py)

覆盖函数：
- compute_rsrs
- compute_rsrs_signal
- get_rsrs_for_index
- get_current_rsrs_signal
- compute_rsrs钝化
- compute_rsrs_weighted

测试场景：
- 正常 RSRS 计算
- 不同方法 (basic/right_bias/weighted)
- 信号生成（买入/卖出/观望）
- 数据不足警告
- 钝化处理
- 指数数据获取
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import patch, MagicMock
import warnings

from jk2bt.analysis.signals.rsrs import (
    compute_rsrs,
    compute_rsrs_signal,
    get_rsrs_for_index,
    get_current_rsrs_signal,
    compute_rsrs钝化,
    compute_rsrs_weighted,
)


class TestComputeRsrs:
    """compute_rsrs 函数测试"""

    def _make_price_data(self, n: int, trend: str = "sideways") -> tuple:
        """生成测试用高价低价数据"""
        np.random.seed(42)
        if trend == "sideways":
            high_base = 100
            low_base = 98
            highs = [high_base + np.random.randn() * 0.5 for _ in range(n)]
            lows = [low_base + np.random.randn() * 0.5 for _ in range(n)]
        elif trend == "up":
            highs = [100 + i * 0.1 + np.random.randn() * 0.3 for i in range(n)]
            lows = [98 + i * 0.1 + np.random.randn() * 0.3 for i in range(n)]
        elif trend == "down":
            highs = [100 - i * 0.1 + np.random.randn() * 0.3 for i in range(n)]
            lows = [98 - i * 0.1 + np.random.randn() * 0.3 for i in range(n)]
        else:
            highs = [100] * n
            lows = [98] * n

        dates = pd.date_range("2022-01-01", periods=n, freq="B")
        return pd.Series(highs, index=dates), pd.Series(lows, index=dates)

    def test_insufficient_data(self):
        """测试数据不足场景"""
        high, low = self._make_price_data(50)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = compute_rsrs(high, low, N=18, M=800)
            assert len(w) == 1
            assert "数据长度不足" in str(w[0].message)
            assert result.isna().all()

    def test_basic_method(self):
        """测试基础 RSRS 方法（仅返回斜率）"""
        high, low = self._make_price_data(1000)
        result = compute_rsrs(high, low, N=18, M=800, method="basic")
        assert isinstance(result, pd.Series)
        assert len(result) == len(high)

    def test_right_bias_method(self):
        """测试右偏修正 RSRS 方法"""
        high, low = self._make_price_data(1000)
        result = compute_rsrs(high, low, N=18, M=800, method="right_bias")
        assert isinstance(result, pd.Series)
        assert not result.isna().all()

    def test_weighted_method(self):
        """测试加权 RSRS 方法"""
        high, low = self._make_price_data(1000)
        result = compute_rsrs(high, low, N=18, M=800, method="weighted")
        assert isinstance(result, pd.Series)

    def test_invalid_method(self):
        """测试无效方法，降级为 z_score"""
        high, low = self._make_price_data(1000)
        result = compute_rsrs(high, low, N=18, M=800, method="invalid_method")
        assert isinstance(result, pd.Series)

    def test_custom_N_M_parameters(self):
        """测试自定义 N, M 参数"""
        high, low = self._make_price_data(500)
        result = compute_rsrs(high, low, N=10, M=200, method="right_bias")
        assert isinstance(result, pd.Series)

    def test_result_index_preserved(self):
        """测试返回结果索引与输入一致"""
        high, low = self._make_price_data(1000)
        result = compute_rsrs(high, low, N=18, M=800)
        assert result.index.equals(high.index)

    def test_nan_propagation_in_result(self):
        """测试结果前 N+M 个值应为 NaN"""
        high, low = self._make_price_data(1000)
        result = compute_rsrs(high, low, N=18, M=800)
        assert result.iloc[: 18 + 800].isna().all()


class TestComputeRsrsSignal:
    """compute_rsrs_signal 函数测试"""

    def test_buy_signal(self):
        """测试买入信号（RSRS > 0.8）"""
        rsrs = pd.Series([0.9, 0.85, 1.0, 0.95])
        result = compute_rsrs_signal(rsrs)
        assert all(result == 1)

    def test_sell_signal(self):
        """测试卖出信号（RSRS < -0.8）"""
        rsrs = pd.Series([-0.9, -0.85, -1.0, -0.95])
        result = compute_rsrs_signal(rsrs)
        assert all(result == -1)

    def test_neutral_signal(self):
        """测试观望信号（-0.8 <= RSRS <= 0.8）"""
        rsrs = pd.Series([0.5, 0.0, -0.5, 0.3])
        result = compute_rsrs_signal(rsrs)
        assert all(result == 0)

    def test_mixed_signals(self):
        """测试混合信号"""
        rsrs = pd.Series([1.0, 0.5, -0.9, 0.0, -0.5, 0.8])
        result = compute_rsrs_signal(rsrs)
        expected = pd.Series([1, 0, -1, 0, 0, 1])
        assert result.equals(expected)

    def test_custom_thresholds(self):
        """测试自定义阈值"""
        rsrs = pd.Series([0.5, 0.6, 0.7, 0.8, 0.9])
        result = compute_rsrs_signal(rsrs, buy_threshold=0.7, sell_threshold=-0.7)
        expected = pd.Series([0, 0, 1, 1, 1])
        assert result.equals(expected)

    def test_empty_series(self):
        """测试空序列"""
        rsrs = pd.Series(dtype=float)
        result = compute_rsrs_signal(rsrs)
        assert result.empty

    def test_index_preserved(self):
        """测试索引保留"""
        idx = pd.date_range("2024-01-01", periods=5)
        rsrs = pd.Series([0.9, 0.5, -0.9, 0.0, 0.5], index=idx)
        result = compute_rsrs_signal(rsrs)
        assert result.index.equals(idx)


class TestGetRsrsForIndex:
    """get_rsrs_for_index 函数测试"""

    @patch("jk2bt.analysis.signals.rsrs.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """测试正常获取指数 RSRS"""
        dates = pd.date_range("2022-01-01", periods=1000, freq="B")
        df = pd.DataFrame(
            {
                "date": dates,
                "open": [100.0] * len(dates),
                "high": [101.0] * len(dates),
                "low": [99.0] * len(dates),
                "close": [100.0 + i * 0.01 for i in range(len(dates))],
                "volume": [1000000] * len(dates),
            }
        )

        mock_adapter = MagicMock()
        mock_adapter.get_index_daily_raw.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = get_rsrs_for_index(
            index_code="000300", start_date="2022-01-01", end_date="2024-06-30"
        )

        assert isinstance(result, pd.DataFrame)
        assert "rsrs" in result.columns
        assert "rsrs_signal" in result.columns
        assert "date" in result.columns
        assert "close" in result.columns

    @patch("jk2bt.analysis.signals.rsrs.get_adapter")
    def test_empty_data(self, mock_get_adapter):
        """测试返回空 DataFrame"""
        mock_adapter = MagicMock()
        mock_adapter.get_index_daily_raw.return_value = None
        mock_get_adapter.return_value = mock_adapter

        result = get_rsrs_for_index(index_code="000300")

        assert result.empty

    @patch("jk2bt.analysis.signals.rsrs.get_adapter")
    def test_dataframe_empty(self, mock_get_adapter):
        """测试返回空 DataFrame（数据框为空）"""
        mock_adapter = MagicMock()
        mock_adapter.get_index_daily_raw.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        result = get_rsrs_for_index(index_code="000300")

        assert result.empty

    @patch("jk2bt.analysis.signals.rsrs.get_adapter")
    def test_date_filtering(self, mock_get_adapter):
        """测试日期过滤"""
        dates = pd.date_range("2022-01-01", periods=1000, freq="B")
        df = pd.DataFrame(
            {
                "date": dates,
                "open": [100.0] * len(dates),
                "high": [101.0] * len(dates),
                "low": [99.0] * len(dates),
                "close": [100.0] * len(dates),
                "volume": [1000000] * len(dates),
            }
        )

        mock_adapter = MagicMock()
        mock_adapter.get_index_daily_raw.return_value = df
        mock_get_adapter.return_value = mock_adapter

        result = get_rsrs_for_index(
            index_code="000300",
            start_date="2024-01-01",
            end_date="2024-06-30",
        )

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.analysis.signals.rsrs.get_adapter")
    def test_sh_prefix_added(self, mock_get_adapter):
        """测试指数代码添加 sh 前缀"""
        mock_adapter = MagicMock()
        mock_adapter.get_index_daily_raw.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        get_rsrs_for_index(index_code="000300")

        call_args = mock_adapter.get_index_daily_raw.call_args
        assert "sh000300" in str(call_args)


class TestGetCurrentRsrsSignal:
    """get_current_rsrs_signal 函数测试"""

    @patch("jk2bt.analysis.signals.rsrs.get_rsrs_for_index")
    def test_buy_signal_description(self, mock_get_rsrs):
        """测试买入信号描述"""
        dates = pd.date_range("2024-01-01", periods=20, freq="B")
        df = pd.DataFrame(
            {
                "date": dates,
                "close": [100.0] * 20,
                "rsrs": [0.9] * 19 + [0.85],
                "rsrs_signal": [1] * 20,
            }
        )
        mock_get_rsrs.return_value = df

        result = get_current_rsrs_signal(index_code="000300")

        assert result["signal"] == 1
        assert "看多" in result["description"]
        assert "rsrs_value" in result

    @patch("jk2bt.analysis.signals.rsrs.get_rsrs_for_index")
    def test_sell_signal_description(self, mock_get_rsrs):
        """测试卖出信号描述"""
        dates = pd.date_range("2024-01-01", periods=20, freq="B")
        df = pd.DataFrame(
            {
                "date": dates,
                "close": [100.0] * 20,
                "rsrs": [-0.9] * 19 + [-0.85],
                "rsrs_signal": [-1] * 20,
            }
        )
        mock_get_rsrs.return_value = df

        result = get_current_rsrs_signal(index_code="000300")

        assert result["signal"] == -1
        assert "看空" in result["description"]

    @patch("jk2bt.analysis.signals.rsrs.get_rsrs_for_index")
    def test_neutral_signal_description(self, mock_get_rsrs):
        """测试观望信号描述"""
        dates = pd.date_range("2024-01-01", periods=20, freq="B")
        df = pd.DataFrame(
            {
                "date": dates,
                "close": [100.0] * 20,
                "rsrs": [0.5] * 19 + [0.3],
                "rsrs_signal": [0] * 20,
            }
        )
        mock_get_rsrs.return_value = df

        result = get_current_rsrs_signal(index_code="000300")

        assert result["signal"] == 0
        assert "观望" in result["description"]

    @patch("jk2bt.analysis.signals.rsrs.get_rsrs_for_index")
    def test_empty_data_return(self, mock_get_rsrs):
        """测试数据获取失败"""
        mock_get_rsrs.return_value = pd.DataFrame()

        result = get_current_rsrs_signal(index_code="000300")

        assert result["signal"] == 0
        assert result["rsrs_value"] == 0.0
        assert "数据获取失败" in result["description"]

    @patch("jk2bt.analysis.signals.rsrs.get_rsrs_for_index")
    def test_rsrs_series_returned(self, mock_get_rsrs):
        """测试返回最近 20 期 RSRS 序列"""
        dates = pd.date_range("2024-01-01", periods=30, freq="B")
        df = pd.DataFrame(
            {
                "date": dates,
                "close": [100.0] * 30,
                "rsrs": list(range(30)),
                "rsrs_signal": [0] * 30,
            }
        )
        mock_get_rsrs.return_value = df

        result = get_current_rsrs_signal(index_code="000300")

        assert result["rsrs_series"] is not None
        assert len(result["rsrs_series"]) == 20


class TestComputeRsrs钝化:
    """compute_rsrs钝化 函数测试"""

    def _make_price_data(self, n: int) -> tuple:
        """生成测试用高价低价数据"""
        np.random.seed(42)
        highs = [100 + np.random.randn() * 0.5 for _ in range(n)]
        lows = [98 + np.random.randn() * 0.5 for _ in range(n)]
        dates = pd.date_range("2022-01-01", periods=n, freq="B")
        return pd.Series(highs, index=dates), pd.Series(lows, index=dates)

    def test_default_s_parameter(self):
        """测试默认 S=5 钝化窗口"""
        high, low = self._make_price_data(1000)
        result = compute_rsrs钝化(high, low, N=18, M=800, S=5)
        assert isinstance(result, pd.Series)

    def test_custom_s_parameter(self):
        """测试自定义 S 参数"""
        high, low = self._make_price_data(1000)
        result = compute_rsrs钝化(high, low, N=18, M=800, S=10)
        assert isinstance(result, pd.Series)

    def test_signal_requires_confirmation(self):
        """测试信号需要连续 S 日确认"""
        high, low = self._make_price_data(1000)
        result = compute_rsrs钝化(high, low, N=18, M=800, S=5)
        signal_changes = result.diff().abs().sum()
        raw_signal_changes = (
            compute_rsrs_signal(compute_rsrs(high, low, N=18, M=800)).diff().abs().sum()
        )
        assert signal_changes <= raw_signal_changes


class TestComputeRsrsWeighted:
    """compute_rsrs_weighted 函数测试"""

    def _make_price_data_with_volume(self, n: int) -> tuple:
        """生成测试用高价低价和成交量数据"""
        np.random.seed(42)
        highs = [100 + np.random.randn() * 0.5 + i * 0.01 for i in range(n)]
        lows = [98 + np.random.randn() * 0.5 + i * 0.01 for i in range(n)]
        volumes = [1000000 + np.random.randn() * 10000 for _ in range(n)]
        dates = pd.date_range("2022-01-01", periods=n, freq="B")
        return (
            pd.Series(highs, index=dates),
            pd.Series(lows, index=dates),
            pd.Series(volumes, index=dates),
        )

    def test_weighted_calculation(self):
        """测试成交量加权 RSRS 计算"""
        high, low, volume = self._make_price_data_with_volume(1000)
        result = compute_rsrs_weighted(high, low, volume, N=18, M=800)
        assert isinstance(result, pd.Series)
        assert len(result) == len(high)

    def test_nan_in_early_period(self):
        """测试早期数据为 NaN"""
        high, low, volume = self._make_price_data_with_volume(1000)
        result = compute_rsrs_weighted(high, low, volume, N=18, M=800)
        assert result.iloc[:18].isna().all()

    def test_different_from_basic(self):
        """测试加权结果与基础结果不同（成交量影响）"""
        high, low, volume = self._make_price_data_with_volume(1000)
        weighted_result = compute_rsrs_weighted(high, low, volume, N=18, M=800)
        basic_result = compute_rsrs(high, low, N=18, M=800, method="basic")
        assert not weighted_result.equals(basic_result)
