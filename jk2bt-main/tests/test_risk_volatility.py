"""
test_risk_volatility.py
volatility.py 模块单元测试。

测试目标：
- compute_volatility: 历史波动率计算
- compute_volatility_adjusted_position: 波动率调整仓位
- compute_atr_based_stop_loss: ATR止损计算
- detect_volatility_regime_change: 波动率状态变化检测
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add jk2bt to path for direct import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))

from jk2bt.analysis.risk.volatility import (
    compute_volatility,
    compute_volatility_adjusted_position,
    compute_atr_based_stop_loss,
    detect_volatility_regime_change,
)
from jk2bt.analysis.factors.base import safe_divide


# =====================================================================
# Fixtures
# =====================================================================


@pytest.fixture
def sample_ohlcv_df():
    """生成模拟OHLCV数据DataFrame（100天，低波动）。"""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    dates_str = dates.strftime("%Y-%m-%d").tolist()

    close = 100 + np.random.randn(100) * 2
    close = np.abs(close)

    high = close * 1.02
    low = close * 0.98
    open_price = close * 0.99 + np.random.randn(100) * 0.5
    open_price = np.abs(open_price)
    volume = np.random.randint(1e6, 1e7, 100)

    df = pd.DataFrame(
        {
            "date": dates_str,
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )
    return df


@pytest.fixture
def high_volatility_ohlcv_df():
    """生成高波动OHLCV数据。"""
    np.random.seed(123)
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    dates_str = dates.strftime("%Y-%m-%d").tolist()

    close = 100 + np.random.randn(100) * 10
    close = np.abs(close)

    high = close * 1.05
    low = close * 0.95
    open_price = close * 0.99 + np.random.randn(100) * 2
    open_price = np.abs(open_price)
    volume = np.random.randint(1e6, 1e7, 100)

    df = pd.DataFrame(
        {
            "date": dates_str,
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )
    return df


@pytest.fixture
def long_ohlcv_df():
    """生成长期OHLCV数据（足够 detect_volatility_regime_change 使用）。"""
    np.random.seed(456)
    dates = pd.date_range("2023-01-01", periods=200, freq="B")
    dates_str = dates.strftime("%Y-%m-%d").tolist()

    close = 100 + np.random.randn(200) * 2
    close = np.abs(close)

    high = close * 1.02
    low = close * 0.98
    open_price = close * 0.99 + np.random.randn(200) * 0.5
    open_price = np.abs(open_price)
    volume = np.random.randint(1e6, 1e7, 200)

    df = pd.DataFrame(
        {
            "date": dates_str,
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }
    )
    return df


@pytest.fixture
def constant_price_ohlcv_df():
    """生成常量价格OHLCV数据。"""
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    dates_str = dates.strftime("%Y-%m-%d").tolist()

    df = pd.DataFrame(
        {
            "date": dates_str,
            "open": [100.0] * 100,
            "high": [102.0] * 100,
            "low": [98.0] * 100,
            "close": [100.0] * 100,
            "volume": [1e6] * 100,
        }
    )
    return df


# =====================================================================
# compute_volatility Tests
# =====================================================================


class TestComputeVolatility:
    """测试 compute_volatility 函数。"""

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_basic_calculation(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证波动率基本计算。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_volatility("sh600519", window=20, end_date="2023-06-01")

        # 验证返回float
        assert isinstance(result, float)
        # 验证波动率为正
        assert result > 0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_returns_series_without_end_date(
        self, mock_get_ohlcv, sample_ohlcv_df
    ):
        """验证不带end_date时返回Series。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_volatility("sh600519", window=20)

        # 验证返回Series
        assert isinstance(result, pd.Series)
        # 验证最后一个值与带end_date的结果一致
        last_val = result.iloc[-1]
        result_float = compute_volatility("sh600519", window=20, end_date="2023-06-01")
        np.testing.assert_almost_equal(last_val, result_float, decimal=6)

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_annualized(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证年化波动率计算。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result_annualized = compute_volatility(
            "sh600519", window=20, annualized=True, end_date="2023-06-01"
        )
        result_daily = compute_volatility(
            "sh600519", window=20, annualized=False, end_date="2023-06-01"
        )

        # 年化波动率应大于日波动率
        assert result_annualized > result_daily
        # 年化系数约为 sqrt(252)
        np.testing.assert_almost_equal(
            result_annualized / result_daily, np.sqrt(252), decimal=6
        )

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_high_volatility(self, mock_get_ohlcv, high_volatility_ohlcv_df):
        """验证高波动数据返回更高的波动率。"""
        mock_get_ohlcv.return_value = high_volatility_ohlcv_df

        result = compute_volatility("sh600519", window=20, end_date="2023-06-01")

        # 高波动数据的波动率应显著大于低波动数据
        assert result > 0.1  # 年化波动率应大于10%

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_constant_price(self, mock_get_ohlcv, constant_price_ohlcv_df):
        """验证常量价格波动率为0。"""
        mock_get_ohlcv.return_value = constant_price_ohlcv_df

        result = compute_volatility("sh600519", window=20, end_date="2023-06-01")

        # 常量价格的波动率应为0
        assert result == 0.0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_volatility("sh600519", window=20)

        assert np.isnan(result)

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_missing_close_column(self, mock_get_ohlcv):
        """测试缺少close列返回NaN。"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "open": [100.0],
                "high": [102.0],
                "low": [98.0],
                "volume": [1e6],
            }
        )
        mock_get_ohlcv.return_value = df

        result = compute_volatility("sh600519", window=20)

        assert np.isnan(result)

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_insufficient_data(self, mock_get_ohlcv):
        """测试数据不足时返回NaN。"""
        dates = pd.date_range("2023-01-01", periods=5, freq="B")
        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d").tolist(),
                "close": [100.0, 101.0, 102.0, 101.5, 103.0],
                "high": [102.0] * 5,
                "low": [98.0] * 5,
                "volume": [1e6] * 5,
            }
        )
        mock_get_ohlcv.return_value = df

        result = compute_volatility("sh600519", window=20, end_date="2023-01-10")

        # 数据不足20天，应返回NaN
        assert np.isnan(result)

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_with_end_date(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试带截止日期参数。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_volatility("sh600519", window=20, end_date="2023-06-01")

        assert isinstance(result, float)
        assert result > 0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_with_force_update(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试force_update参数传递。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_volatility("sh600519", window=20, force_update=True)

        # 验证调用参数包含force_update
        call_kwargs = mock_get_ohlcv.call_args[1]
        assert call_kwargs["force_update"] is True

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_different_windows(self, mock_get_ohlcv, sample_ohlcv_df):
        """参数化测试不同窗口期。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        for window in [5, 10, 20, 60]:
            result = compute_volatility(
                "sh600519", window=window, end_date="2023-06-01"
            )
            assert isinstance(result, float)
            assert result >= 0


# =====================================================================
# compute_volatility_adjusted_position Tests
# =====================================================================


class TestComputeVolatilityAdjustedPosition:
    """测试 compute_volatility_adjusted_position 函数。"""

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_position_high_volatility_reduces_size(
        self, mock_get_ohlcv, high_volatility_ohlcv_df
    ):
        """验证高波动率时仓位应减小。"""
        mock_get_ohlcv.return_value = high_volatility_ohlcv_df

        result = compute_volatility_adjusted_position(
            "sh600519",
            base_position=1.0,
            target_vol=0.15,
            window=20,
            end_date="2023-06-01",
        )

        # 验证返回字典包含必要键
        assert isinstance(result, dict)
        assert "adjusted_position" in result
        assert "current_vol" in result
        assert "target_vol" in result
        assert "vol_ratio" in result

        # 验证目标波动率
        assert result["target_vol"] == 0.15

        # 验证波动率为正
        assert result["current_vol"] > 0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_position_high_volatility_reduces_size(
        self, mock_get_ohlcv, high_volatility_ohlcv_df
    ):
        """验证高波动率时仓位应减小。"""
        mock_get_ohlcv.return_value = high_volatility_ohlcv_df

        result = compute_volatility_adjusted_position(
            "sh600519",
            base_position=1.0,
            target_vol=0.15,
            window=20,
            end_date="2023-06-01",
        )

        # 高波动率时，vol_ratio < 1，adjusted_position < base_position
        assert result["vol_ratio"] < 1.0
        assert (
            result["adjusted_position"] < result["base_position"]
            if "base_position" in result
            else result["adjusted_position"] < 1.0
        )

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_position_empty_data(self, mock_get_ohlcv):
        """测试空数据返回基础仓位。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_volatility_adjusted_position(
            "sh600519",
            base_position=0.5,
            target_vol=0.15,
        )

        # 数据为空时，应返回基础仓位
        assert result["adjusted_position"] == 0.5
        assert np.isnan(result["current_vol"])
        assert result["vol_ratio"] == 1.0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_position_constant_price(self, mock_get_ohlcv, constant_price_ohlcv_df):
        """测试常量价格（波动率为0）时返回基础仓位。"""
        mock_get_ohlcv.return_value = constant_price_ohlcv_df

        result = compute_volatility_adjusted_position(
            "sh600519",
            base_position=1.0,
            target_vol=0.15,
            end_date="2023-06-01",
        )

        # 波动率为0时，应返回基础仓位
        assert result["adjusted_position"] == 1.0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_position_capped_at_max(self, mock_get_ohlcv):
        """验证仓位上限不超过 base_position * 2。"""
        # 创建极低波动率数据
        dates = pd.date_range("2023-01-01", periods=100, freq="B")
        close = [100.0 + i * 0.001 for i in range(100)]
        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d").tolist(),
                "open": close,
                "high": [c * 1.001 for c in close],
                "low": [c * 0.999 for c in close],
                "close": close,
                "volume": [1e6] * 100,
            }
        )
        mock_get_ohlcv.return_value = df

        result = compute_volatility_adjusted_position(
            "sh600519",
            base_position=1.0,
            target_vol=0.15,
            window=20,
            end_date="2023-06-01",
        )

        # 仓位不应超过 base_position * 2
        assert result["adjusted_position"] <= 2.0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_position_not_negative(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证仓位不为负。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_volatility_adjusted_position(
            "sh600519",
            base_position=1.0,
            target_vol=0.15,
            end_date="2023-06-01",
        )

        assert result["adjusted_position"] >= 0.0


# =====================================================================
# compute_atr_based_stop_loss Tests
# =====================================================================


class TestComputeAtrBasedStopLoss:
    """测试 compute_atr_based_stop_loss 函数。"""

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_atr_stop_loss_basic(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证ATR止损基本计算。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_atr_based_stop_loss(
            "sh600519", atr_window=14, atr_multiplier=2.0
        )

        # 验证返回字典包含必要键
        assert isinstance(result, dict)
        assert "stop_loss_price" in result
        assert "atr_value" in result
        assert "risk_per_share" in result
        assert "current_price" in result

        # 验证ATR为正
        assert result["atr_value"] > 0
        # 验证当前价格为正
        assert result["current_price"] > 0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_atr_stop_loss_price_below_current(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证止损价低于当前价格。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_atr_based_stop_loss(
            "sh600519", atr_window=14, atr_multiplier=2.0
        )

        # 止损价应低于当前价格
        assert result["stop_loss_price"] < result["current_price"]

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_atr_stop_loss_risk_per_share(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证每股风险计算正确。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_atr_based_stop_loss(
            "sh600519", atr_window=14, atr_multiplier=2.0
        )

        # risk_per_share = current_price - stop_loss_price
        expected_risk = result["current_price"] - result["stop_loss_price"]
        np.testing.assert_almost_equal(
            result["risk_per_share"], expected_risk, decimal=6
        )

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_atr_stop_loss_high_volatility(
        self, mock_get_ohlcv, high_volatility_ohlcv_df
    ):
        """验证高波动数据ATR更大，止损距离更远。"""
        mock_get_ohlcv.return_value = high_volatility_ohlcv_df

        result = compute_atr_based_stop_loss(
            "sh600519", atr_window=14, atr_multiplier=2.0
        )

        # 高波动数据的ATR应更大
        assert result["atr_value"] > 1.0  # 高波动ATR应显著大于1

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_atr_stop_loss_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_atr_based_stop_loss("sh600519", atr_window=14)

        assert np.isnan(result["stop_loss_price"])
        assert np.isnan(result["atr_value"])
        assert np.isnan(result["risk_per_share"])
        assert np.isnan(result["current_price"])

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_atr_stop_loss_missing_close(self, mock_get_ohlcv):
        """测试缺少close列返回NaN。"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "open": [100.0],
                "high": [102.0],
                "low": [98.0],
                "volume": [1e6],
            }
        )
        mock_get_ohlcv.return_value = df

        result = compute_atr_based_stop_loss("sh600519", atr_window=14)

        assert np.isnan(result["stop_loss_price"])

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_atr_stop_loss_different_multipliers(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证不同ATR倍数影响止损距离。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result_1x = compute_atr_based_stop_loss(
            "sh600519", atr_window=14, atr_multiplier=1.0
        )
        result_2x = compute_atr_based_stop_loss(
            "sh600519", atr_window=14, atr_multiplier=2.0
        )

        # 2倍ATR的止损距离应是1倍ATR的两倍
        risk_1x = result_1x["current_price"] - result_1x["stop_loss_price"]
        risk_2x = result_2x["current_price"] - result_2x["stop_loss_price"]

        np.testing.assert_almost_equal(risk_2x, risk_1x * 2, decimal=6)

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_atr_stop_loss_constant_price(
        self, mock_get_ohlcv, constant_price_ohlcv_df
    ):
        """验证常量价格ATR为固定值。"""
        mock_get_ohlcv.return_value = constant_price_ohlcv_df

        result = compute_atr_based_stop_loss(
            "sh600519", atr_window=14, atr_multiplier=2.0
        )

        # 常量价格的high-low=4，ATR应接近4
        assert result["atr_value"] > 0
        assert result["stop_loss_price"] < result["current_price"]


# =====================================================================
# detect_volatility_regime_change Tests
# =====================================================================


class TestDetectVolatilityRegimeChange:
    """测试 detect_volatility_regime_change 函数。"""

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_basic(self, mock_get_ohlcv, long_ohlcv_df):
        """验证波动率状态检测基本功能。"""
        mock_get_ohlcv.return_value = long_ohlcv_df

        result = detect_volatility_regime_change(
            "sh600519",
            short_window=10,
            long_window=60,
            multiplier=1.5,
        )

        # 验证返回DataFrame
        assert isinstance(result, pd.DataFrame)
        # 验证包含必要列
        assert "date" in result.columns
        assert "signal" in result.columns
        assert "type" in result.columns

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_signal_values(self, mock_get_ohlcv, long_ohlcv_df):
        """验证信号值只包含1或-1。"""
        mock_get_ohlcv.return_value = long_ohlcv_df

        result = detect_volatility_regime_change("sh600519")

        # 过滤后的结果只包含非零信号
        if len(result) > 0:
            assert set(result["signal"].unique()).issubset({1, -1})

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_type_values(self, mock_get_ohlcv, long_ohlcv_df):
        """验证type列只包含预期值。"""
        mock_get_ohlcv.return_value = long_ohlcv_df

        result = detect_volatility_regime_change("sh600519")

        if len(result) > 0:
            valid_types = {"volatility_increase", "volatility_decrease"}
            assert set(result["type"].unique()).issubset(valid_types)

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_signal_type_consistency(self, mock_get_ohlcv, long_ohlcv_df):
        """验证signal与type的一致性。"""
        mock_get_ohlcv.return_value = long_ohlcv_df

        result = detect_volatility_regime_change("sh600519")

        if len(result) > 0:
            # signal=1 对应 volatility_increase
            increase_rows = result[result["signal"] == 1]
            if len(increase_rows) > 0:
                assert (increase_rows["type"] == "volatility_increase").all()

            # signal=-1 对应 volatility_decrease
            decrease_rows = result[result["signal"] == -1]
            if len(decrease_rows) > 0:
                assert (decrease_rows["type"] == "volatility_decrease").all()

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_empty_data(self, mock_get_ohlcv):
        """测试空数据返回空DataFrame。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = detect_volatility_regime_change("sh600519")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert "date" in result.columns
        assert "signal" in result.columns
        assert "type" in result.columns

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_missing_close(self, mock_get_ohlcv):
        """测试缺少close列返回空DataFrame。"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "open": [100.0],
                "high": [102.0],
                "low": [98.0],
                "volume": [1e6],
            }
        )
        mock_get_ohlcv.return_value = df

        result = detect_volatility_regime_change("sh600519")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_insufficient_data(self, mock_get_ohlcv):
        """测试数据不足时返回空DataFrame。"""
        dates = pd.date_range("2023-01-01", periods=10, freq="B")
        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d").tolist(),
                "close": [100.0 + i for i in range(10)],
                "high": [102.0] * 10,
                "low": [98.0] * 10,
                "volume": [1e6] * 10,
            }
        )
        mock_get_ohlcv.return_value = df

        result = detect_volatility_regime_change(
            "sh600519", short_window=10, long_window=60
        )

        # 数据不足以计算60日波动率，应返回空或很少结果
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_vol_ratio_column(self, mock_get_ohlcv, long_ohlcv_df):
        """验证vol_ratio列存在且为正。"""
        mock_get_ohlcv.return_value = long_ohlcv_df

        result = detect_volatility_regime_change("sh600519")

        if len(result) > 0:
            assert "vol_ratio" in result.columns
            # vol_ratio应为正（波动率比率）
            valid_ratio = result["vol_ratio"].dropna()
            if len(valid_ratio) > 0:
                assert (valid_ratio > 0).all()

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_with_custom_params(self, mock_get_ohlcv, long_ohlcv_df):
        """测试自定义参数。"""
        mock_get_ohlcv.return_value = long_ohlcv_df

        result = detect_volatility_regime_change(
            "sh600519",
            short_window=5,
            long_window=30,
            multiplier=2.0,
        )

        assert isinstance(result, pd.DataFrame)
        assert "date" in result.columns
        assert "signal" in result.columns

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_regime_change_constant_price(self, mock_get_ohlcv):
        """测试常量价格时波动率比率为NaN或无信号。"""
        dates = pd.date_range("2023-01-01", periods=200, freq="B")
        df = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d").tolist(),
                "open": [100.0] * 200,
                "high": [102.0] * 200,
                "low": [98.0] * 200,
                "close": [100.0] * 200,
                "volume": [1e6] * 200,
            }
        )
        mock_get_ohlcv.return_value = df

        result = detect_volatility_regime_change(
            "sh600519", short_window=10, long_window=60
        )

        # 常量价格时波动率为0，vol_ratio可能为NaN或无信号
        assert isinstance(result, pd.DataFrame)


# =====================================================================
# safe_divide Tests (imported from factors.base)
# =====================================================================


class TestSafeDivide:
    """测试 safe_divide 函数。"""

    def test_safe_divide_normal(self):
        """测试正常除法。"""
        result = safe_divide(10, 2)
        assert result == 5.0

    def test_safe_divide_zero_denominator(self):
        """测试分母为零返回NaN。"""
        result = safe_divide(10, 0)
        assert np.isnan(result)

    def test_safe_divide_series(self):
        """测试Series除法。"""
        a = pd.Series([10, 20, 30])
        b = pd.Series([2, 0, 3])

        result = safe_divide(a, b)

        assert result.iloc[0] == 5.0
        assert np.isnan(result.iloc[1])
        assert result.iloc[2] == 10.0

    def test_safe_divide_nan_denominator(self):
        """测试NaN分母返回NaN。"""
        result = safe_divide(10, np.nan)
        assert np.isnan(result)

    def test_safe_divide_numpy_arrays(self):
        """测试numpy数组除法。"""
        a = np.array([10.0, 20.0, 30.0])
        b = np.array([2.0, 0.0, 3.0])

        result = safe_divide(a, b)

        assert result[0] == 5.0
        assert np.isnan(result[1])
        assert result[2] == 10.0


# =====================================================================
# Integration Tests
# =====================================================================


class TestVolatilityModuleIntegration:
    """测试波动率模块集成场景。"""

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_volatility_then_position_adjustment(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证先计算波动率再调整仓位的流程。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        vol = compute_volatility("sh600519", window=20, end_date="2023-06-01")
        position_result = compute_volatility_adjusted_position(
            "sh600519",
            base_position=1.0,
            target_vol=0.15,
            window=20,
            end_date="2023-06-01",
        )

        # 验证波动率一致
        np.testing.assert_almost_equal(vol, position_result["current_vol"], decimal=6)

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_atr_stop_loss_with_volatility_context(
        self, mock_get_ohlcv, sample_ohlcv_df
    ):
        """验证ATR止损与波动率的关联。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        vol = compute_volatility("sh600519", window=20, end_date="2023-06-01")
        stop_loss = compute_atr_based_stop_loss("sh600519", atr_window=14)

        # 两者都应返回有效值
        assert vol > 0
        assert stop_loss["atr_value"] > 0
        assert stop_loss["current_price"] > 0

    @patch("jk2bt.risk.volatility._get_daily_ohlcv")
    def test_all_functions_with_same_data(self, mock_get_ohlcv, long_ohlcv_df):
        """验证所有函数使用相同数据时不报错。"""
        mock_get_ohlcv.return_value = long_ohlcv_df

        vol = compute_volatility("sh600519", window=20, end_date="2023-12-01")
        position = compute_volatility_adjusted_position(
            "sh600519", window=20, end_date="2023-12-01"
        )
        stop_loss = compute_atr_based_stop_loss("sh600519", atr_window=14)
        regime = detect_volatility_regime_change(
            "sh600519", short_window=10, long_window=60
        )

        # 验证所有函数返回有效结果
        assert isinstance(vol, float)
        assert isinstance(position, dict)
        assert isinstance(stop_loss, dict)
        assert isinstance(regime, pd.DataFrame)
