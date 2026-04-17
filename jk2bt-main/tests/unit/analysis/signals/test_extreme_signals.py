"""
test_extreme.py
extreme.py 模块核心函数单元测试。

测试目标：
- detect_rsi_extreme: RSI 超买超卖信号
- detect_cci_extreme: CCI 极端信号
- detect_bias_extreme: BIAS 极端偏离信号
- detect_kdj_extreme: KDJ 极端信号
- detect_all_extreme_signals: 批量检测极值信号
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))

from jk2bt.analysis.signals.extreme import (
    detect_rsi_extreme,
    detect_cci_extreme,
    detect_bias_extreme,
    detect_kdj_extreme,
    detect_all_extreme_signals,
)


# =====================================================================
# Fixtures
# =====================================================================


@pytest.fixture
def sample_ohlcv_df():
    """生成模拟OHLCV数据。"""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    close = 100 + np.cumsum(np.random.randn(100) * 0.5)
    close = np.abs(close)

    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "open": close * 0.99,
            "high": close * 1.02,
            "low": close * 0.98,
            "close": close,
            "volume": np.random.randint(1e6, 1e7, 100),
            "amount": np.random.randint(1e8, 1e9, 100),
        }
    )
    return df


@pytest.fixture
def rising_ohlcv_df():
    """生成持续上涨的OHLCV数据（用于触发超买信号）。"""
    dates = pd.date_range("2023-01-01", periods=50, freq="B")
    close = np.linspace(90, 120, 50)

    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "open": close * 0.99,
            "high": close * 1.01,
            "low": close * 0.98,
            "close": close,
            "volume": np.random.randint(1e6, 1e7, 50),
            "amount": np.random.randint(1e8, 1e9, 50),
        }
    )
    return df


@pytest.fixture
def falling_ohlcv_df():
    """生成持续下跌的OHLCV数据（用于触发超卖信号）。"""
    dates = pd.date_range("2023-01-01", periods=50, freq="B")
    close = np.linspace(120, 80, 50)

    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "open": close * 1.01,
            "high": close * 1.02,
            "low": close * 0.99,
            "close": close,
            "volume": np.random.randint(1e6, 1e7, 50),
            "amount": np.random.randint(1e8, 1e9, 50),
        }
    )
    return df


@pytest.fixture
def constant_ohlcv_df():
    """生成价格不变的OHLCV数据。"""
    dates = pd.date_range("2023-01-01", periods=50, freq="B")
    close = np.array([100.0] * 50)

    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "open": close,
            "high": close,
            "low": close,
            "close": close,
            "volume": np.array([1e6] * 50),
            "amount": np.array([1e8] * 50),
        }
    )
    return df


# =====================================================================
# detect_rsi_extreme Tests
# =====================================================================


class TestDetectRSIExtreme:
    """测试 RSI 超买超卖信号检测。"""

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_normal(self, mock_fetch, sample_ohlcv_df):
        """验证RSI极值检测基本功能。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_rsi_extreme("sh600519", window=14)

        assert isinstance(result, pd.DataFrame)
        assert "date" in result.columns
        assert "signal" in result.columns
        assert "type" in result.columns
        assert "rsi_value" in result.columns

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_overbought(self, mock_fetch, rising_ohlcv_df):
        """测试超买信号检测。"""
        mock_fetch.return_value = rising_ohlcv_df

        result = detect_rsi_extreme("sh600519", window=14, upper=70, lower=30)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert all(result["signal"].isin([1, -1]))
            overbought = result[result["signal"] == 1]
            if not overbought.empty:
                assert all(overbought["type"] == "rsi_overbought")

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_oversold(self, mock_fetch, falling_ohlcv_df):
        """测试超卖信号检测。"""
        mock_fetch.return_value = falling_ohlcv_df

        result = detect_rsi_extreme("sh600519", window=14, upper=70, lower=30)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert all(result["signal"].isin([1, -1]))
            oversold = result[result["signal"] == -1]
            if not oversold.empty:
                assert all(oversold["type"] == "rsi_oversold")

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_empty_data(self, mock_fetch):
        """测试空数据返回空DataFrame。"""
        mock_fetch.return_value = pd.DataFrame()

        result = detect_rsi_extreme("sh600519", window=14)

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_no_close_column(self, mock_fetch):
        """测试缺少close列返回空DataFrame。"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "open": [100],
                "high": [102],
                "low": [98],
                "volume": [1e6],
            }
        )
        mock_fetch.return_value = df

        result = detect_rsi_extreme("sh600519", window=14)

        assert result.empty

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_constant_price(self, mock_fetch, constant_ohlcv_df):
        """测试常量价格场景。"""
        mock_fetch.return_value = constant_ohlcv_df

        result = detect_rsi_extreme("sh600519", window=14)

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_custom_thresholds(self, mock_fetch, sample_ohlcv_df):
        """测试自定义阈值。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_rsi_extreme("sh600519", window=14, upper=80, lower=20)

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_with_end_date(self, mock_fetch, sample_ohlcv_df):
        """测试指定截止日期。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_rsi_extreme("sh600519", window=14, end_date="2023-06-01")

        assert isinstance(result, pd.DataFrame)
        mock_fetch.assert_called_once()
        call_kwargs = mock_fetch.call_args[1]
        assert call_kwargs["end_date"] == "2023-06-01"

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_signal_values(self, mock_fetch, sample_ohlcv_df):
        """验证信号值只包含1或-1。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_rsi_extreme("sh600519", window=14)

        if not result.empty:
            assert all(result["signal"].isin([1, -1]))

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_rsi_extreme_short_data(self, mock_fetch):
        """测试数据量不足场景。"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "close": [100, 101],
                "high": [102, 103],
                "low": [98, 99],
                "volume": [1e6, 1e6],
                "amount": [1e8, 1e8],
            }
        )
        mock_fetch.return_value = df

        result = detect_rsi_extreme("sh600519", window=14)

        assert isinstance(result, pd.DataFrame)


# =====================================================================
# detect_cci_extreme Tests
# =====================================================================


class TestDetectCCIExtreme:
    """测试 CCI 极端信号检测。"""

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_cci_extreme_normal(self, mock_fetch, sample_ohlcv_df):
        """验证CCI极值检测基本功能。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_cci_extreme("sh600519", window=10)

        assert isinstance(result, pd.DataFrame)
        assert "date" in result.columns
        assert "signal" in result.columns
        assert "type" in result.columns
        assert "cci_value" in result.columns

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_cci_extreme_overbought(self, mock_fetch):
        """测试CCI超买信号。"""
        dates = pd.date_range("2023-01-01", periods=50, freq="B")
        close = np.linspace(90, 130, 50)
        high = close * 1.02
        low = close * 0.98

        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "open": close,
                "high": high,
                "low": low,
                "close": close,
                "volume": np.random.randint(1e6, 1e7, 50),
                "amount": np.random.randint(1e8, 1e9, 50),
            }
        )
        mock_fetch.return_value = df

        result = detect_cci_extreme("sh600519", window=10, upper=100, lower=-100)

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert all(result["signal"].isin([1, -1]))

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_cci_extreme_oversold(self, mock_fetch):
        """测试CCI超卖信号。"""
        dates = pd.date_range("2023-01-01", periods=50, freq="B")
        close = np.linspace(130, 80, 50)
        high = close * 1.02
        low = close * 0.98

        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "open": close,
                "high": high,
                "low": low,
                "close": close,
                "volume": np.random.randint(1e6, 1e7, 50),
                "amount": np.random.randint(1e8, 1e9, 50),
            }
        )
        mock_fetch.return_value = df

        result = detect_cci_extreme("sh600519", window=10, upper=100, lower=-100)

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_cci_extreme_empty_data(self, mock_fetch):
        """测试空数据返回空DataFrame。"""
        mock_fetch.return_value = pd.DataFrame()

        result = detect_cci_extreme("sh600519", window=10)

        assert result.empty

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_cci_extreme_no_close_column(self, mock_fetch):
        """测试缺少close列返回空DataFrame。"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "open": [100],
                "volume": [1e6],
            }
        )
        mock_fetch.return_value = df

        result = detect_cci_extreme("sh600519", window=10)

        assert result.empty

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_cci_extreme_custom_window(self, mock_fetch, sample_ohlcv_df):
        """测试不同计算窗口。"""
        mock_fetch.return_value = sample_ohlcv_df

        result_10 = detect_cci_extreme("sh600519", window=10)
        result_20 = detect_cci_extreme("sh600519", window=20)

        assert isinstance(result_10, pd.DataFrame)
        assert isinstance(result_20, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_cci_extreme_type_values(self, mock_fetch, sample_ohlcv_df):
        """验证type列值正确。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_cci_extreme("sh600519", window=10)

        if not result.empty:
            valid_types = {"cci_extreme_overbought", "cci_extreme_oversold"}
            assert all(t in valid_types for t in result["type"])


# =====================================================================
# detect_bias_extreme Tests
# =====================================================================


class TestDetectBIASExtreme:
    """测试 BIAS 极端偏离信号检测。"""

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_bias_extreme_normal(self, mock_fetch, sample_ohlcv_df):
        """验证BIAS极值检测基本功能。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_bias_extreme("sh600519", window=10)

        assert isinstance(result, pd.DataFrame)
        assert "date" in result.columns
        assert "signal" in result.columns
        assert "type" in result.columns
        assert "bias_value" in result.columns

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_bias_extreme_overbought(self, mock_fetch):
        """测试BIAS超买信号。"""
        dates = pd.date_range("2023-01-01", periods=50, freq="B")
        close = np.linspace(90, 130, 50)

        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "open": close,
                "high": close * 1.02,
                "low": close * 0.98,
                "close": close,
                "volume": np.random.randint(1e6, 1e7, 50),
                "amount": np.random.randint(1e8, 1e9, 50),
            }
        )
        mock_fetch.return_value = df

        result = detect_bias_extreme("sh600519", window=10, upper=5, lower=-5)

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_bias_extreme_oversold(self, mock_fetch):
        """测试BIAS超卖信号。"""
        dates = pd.date_range("2023-01-01", periods=50, freq="B")
        close = np.linspace(130, 80, 50)

        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "open": close,
                "high": close * 1.02,
                "low": close * 0.98,
                "close": close,
                "volume": np.random.randint(1e6, 1e7, 50),
                "amount": np.random.randint(1e8, 1e9, 50),
            }
        )
        mock_fetch.return_value = df

        result = detect_bias_extreme("sh600519", window=10, upper=5, lower=-5)

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_bias_extreme_empty_data(self, mock_fetch):
        """测试空数据返回空DataFrame。"""
        mock_fetch.return_value = pd.DataFrame()

        result = detect_bias_extreme("sh600519", window=10)

        assert result.empty

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_bias_extreme_custom_window(self, mock_fetch, sample_ohlcv_df):
        """测试不同窗口期。"""
        mock_fetch.return_value = sample_ohlcv_df

        result_5 = detect_bias_extreme("sh600519", window=5)
        result_20 = detect_bias_extreme("sh600519", window=20)

        assert isinstance(result_5, pd.DataFrame)
        assert isinstance(result_20, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_bias_extreme_type_contains_window(self, mock_fetch, sample_ohlcv_df):
        """验证type列包含窗口期信息。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_bias_extreme("sh600519", window=15)

        if not result.empty:
            assert all("bias_15" in t for t in result["type"])

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_bias_extreme_constant_price(self, mock_fetch, constant_ohlcv_df):
        """测试常量价格场景。"""
        mock_fetch.return_value = constant_ohlcv_df

        result = detect_bias_extreme("sh600519", window=10)

        assert isinstance(result, pd.DataFrame)


# =====================================================================
# detect_kdj_extreme Tests
# =====================================================================


class TestDetectKDJExtreme:
    """测试 KDJ 极端信号检测。"""

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_kdj_extreme_normal(self, mock_fetch, sample_ohlcv_df):
        """验证KDJ极值检测基本功能。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_kdj_extreme("sh600519", n=9, m1=3, m2=3)

        assert isinstance(result, pd.DataFrame)
        assert "date" in result.columns
        assert "signal" in result.columns
        assert "type" in result.columns
        assert "k_value" in result.columns
        assert "d_value" in result.columns

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_kdj_extreme_overbought(self, mock_fetch):
        """测试KDJ超买信号。"""
        dates = pd.date_range("2023-01-01", periods=50, freq="B")
        close = np.linspace(90, 130, 50)
        high = close * 1.02
        low = close * 0.98

        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "open": close,
                "high": high,
                "low": low,
                "close": close,
                "volume": np.random.randint(1e6, 1e7, 50),
                "amount": np.random.randint(1e8, 1e9, 50),
            }
        )
        mock_fetch.return_value = df

        result = detect_kdj_extreme("sh600519", n=9, upper=80, lower=20)

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_kdj_extreme_oversold(self, mock_fetch):
        """测试KDJ超卖信号。"""
        dates = pd.date_range("2023-01-01", periods=50, freq="B")
        close = np.linspace(130, 80, 50)
        high = close * 1.02
        low = close * 0.98

        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "open": close,
                "high": high,
                "low": low,
                "close": close,
                "volume": np.random.randint(1e6, 1e7, 50),
                "amount": np.random.randint(1e8, 1e9, 50),
            }
        )
        mock_fetch.return_value = df

        result = detect_kdj_extreme("sh600519", n=9, upper=80, lower=20)

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_kdj_extreme_empty_data(self, mock_fetch):
        """测试空数据返回空DataFrame。"""
        mock_fetch.return_value = pd.DataFrame()

        result = detect_kdj_extreme("sh600519", n=9)

        assert result.empty

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_kdj_extreme_no_close_column(self, mock_fetch):
        """测试缺少close列返回空DataFrame。"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "open": [100],
                "volume": [1e6],
            }
        )
        mock_fetch.return_value = df

        result = detect_kdj_extreme("sh600519", n=9)

        assert result.empty

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_kdj_extreme_custom_params(self, mock_fetch, sample_ohlcv_df):
        """测试自定义参数。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_kdj_extreme("sh600519", n=14, m1=5, m2=5, upper=85, lower=15)

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.signals.extreme_signals._fetch_ohlcv")
    def test_kdj_extreme_type_values(self, mock_fetch, sample_ohlcv_df):
        """验证type列值正确。"""
        mock_fetch.return_value = sample_ohlcv_df

        result = detect_kdj_extreme("sh600519", n=9)

        if not result.empty:
            valid_types = {"kdj_overbought", "kdj_oversold"}
            assert all(t in valid_types for t in result["type"])


# =====================================================================
# detect_all_extreme_signals Tests
# =====================================================================


class TestDetectAllExtremeSignals:
    """测试批量检测极值信号。"""

    @patch("jk2bt.signals.extreme_signals.detect_kdj_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_bias_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_cci_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_rsi_extreme")
    def test_detect_all_normal(
        self,
        mock_rsi,
        mock_cci,
        mock_bias,
        mock_kdj,
    ):
        """验证批量检测基本功能。"""
        rsi_df = pd.DataFrame(
            {
                "date": ["2023-01-10"],
                "signal": [1],
                "type": ["rsi_overbought"],
                "rsi_value": [75.0],
            }
        )
        cci_df = pd.DataFrame(
            {
                "date": ["2023-01-15"],
                "signal": [-1],
                "type": ["cci_extreme_oversold"],
                "cci_value": [-110.0],
            }
        )
        bias_df = pd.DataFrame()
        kdj_df = pd.DataFrame()

        mock_rsi.return_value = rsi_df
        mock_cci.return_value = cci_df
        mock_bias.return_value = bias_df
        mock_kdj.return_value = kdj_df

        result = detect_all_extreme_signals("sh600519")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "date" in result.columns
        assert "signal" in result.columns
        assert "type" in result.columns

    @patch("jk2bt.signals.extreme_signals.detect_kdj_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_bias_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_cci_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_rsi_extreme")
    def test_detect_all_empty(
        self,
        mock_rsi,
        mock_cci,
        mock_bias,
        mock_kdj,
    ):
        """测试所有检测都返回空时。"""
        mock_rsi.return_value = pd.DataFrame()
        mock_cci.return_value = pd.DataFrame()
        mock_bias.return_value = pd.DataFrame()
        mock_kdj.return_value = pd.DataFrame()

        result = detect_all_extreme_signals("sh600519")

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    @patch("jk2bt.signals.extreme_signals.detect_kdj_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_bias_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_cci_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_rsi_extreme")
    def test_detect_all_rsi_exception(
        self,
        mock_rsi,
        mock_cci,
        mock_bias,
        mock_kdj,
    ):
        """测试RSI检测异常时其他检测仍正常执行。"""
        mock_rsi.side_effect = Exception("RSI error")
        mock_cci.return_value = pd.DataFrame(
            {
                "date": ["2023-01-15"],
                "signal": [1],
                "type": ["cci_extreme_overbought"],
                "cci_value": [110.0],
            }
        )
        mock_bias.return_value = pd.DataFrame()
        mock_kdj.return_value = pd.DataFrame()

        result = detect_all_extreme_signals("sh600519")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    @patch("jk2bt.signals.extreme_signals.detect_kdj_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_bias_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_cci_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_rsi_extreme")
    def test_detect_all_multiple_exceptions(
        self,
        mock_rsi,
        mock_cci,
        mock_bias,
        mock_kdj,
    ):
        """测试多个检测异常时仍能返回有效结果。"""
        mock_rsi.side_effect = Exception("RSI error")
        mock_cci.side_effect = Exception("CCI error")
        mock_bias.return_value = pd.DataFrame(
            {
                "date": ["2023-01-20"],
                "signal": [-1],
                "type": ["bias_10_extreme_oversold"],
                "bias_value": [-6.0],
            }
        )
        mock_kdj.return_value = pd.DataFrame()

        result = detect_all_extreme_signals("sh600519")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    @patch("jk2bt.signals.extreme_signals.detect_kdj_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_bias_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_cci_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_rsi_extreme")
    def test_detect_all_with_end_date(
        self,
        mock_rsi,
        mock_cci,
        mock_bias,
        mock_kdj,
    ):
        """测试截止日期参数传递。"""
        mock_rsi.return_value = pd.DataFrame()
        mock_cci.return_value = pd.DataFrame()
        mock_bias.return_value = pd.DataFrame()
        mock_kdj.return_value = pd.DataFrame()

        detect_all_extreme_signals("sh600519", end_date="2023-12-31")

        mock_rsi.assert_called_once()
        assert mock_rsi.call_args[1]["end_date"] == "2023-12-31"

    @patch("jk2bt.signals.extreme_signals.detect_kdj_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_bias_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_cci_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_rsi_extreme")
    def test_detect_all_result_sorted(
        self,
        mock_rsi,
        mock_cci,
        mock_bias,
        mock_kdj,
    ):
        """验证结果按日期排序。"""
        rsi_df = pd.DataFrame(
            {
                "date": ["2023-01-20"],
                "signal": [1],
                "type": ["rsi_overbought"],
                "rsi_value": [75.0],
            }
        )
        cci_df = pd.DataFrame(
            {
                "date": ["2023-01-10"],
                "signal": [-1],
                "type": ["cci_extreme_oversold"],
                "cci_value": [-110.0],
            }
        )
        bias_df = pd.DataFrame(
            {
                "date": ["2023-01-15"],
                "signal": [1],
                "type": ["bias_10_extreme_overbought"],
                "bias_value": [6.0],
            }
        )
        kdj_df = pd.DataFrame()

        mock_rsi.return_value = rsi_df
        mock_cci.return_value = cci_df
        mock_bias.return_value = bias_df
        mock_kdj.return_value = kdj_df

        result = detect_all_extreme_signals("sh600519")

        assert len(result) == 3
        dates = result["date"].tolist()
        assert dates == sorted(dates)

    @patch("jk2bt.signals.extreme_signals.detect_kdj_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_bias_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_cci_extreme")
    @patch("jk2bt.signals.extreme_signals.detect_rsi_extreme")
    def test_detect_all_signal_values(
        self,
        mock_rsi,
        mock_cci,
        mock_bias,
        mock_kdj,
    ):
        """验证信号值只包含1或-1。"""
        rsi_df = pd.DataFrame(
            {
                "date": ["2023-01-10"],
                "signal": [1],
                "type": ["rsi_overbought"],
                "rsi_value": [75.0],
            }
        )
        cci_df = pd.DataFrame(
            {
                "date": ["2023-01-15"],
                "signal": [-1],
                "type": ["cci_extreme_oversold"],
                "cci_value": [-110.0],
            }
        )
        bias_df = pd.DataFrame()
        kdj_df = pd.DataFrame()

        mock_rsi.return_value = rsi_df
        mock_cci.return_value = cci_df
        mock_bias.return_value = bias_df
        mock_kdj.return_value = kdj_df

        result = detect_all_extreme_signals("sh600519")

        assert all(result["signal"].isin([1, -1]))
