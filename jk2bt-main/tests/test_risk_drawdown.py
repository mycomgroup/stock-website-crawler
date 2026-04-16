"""Tests for jk2bt.risk.drawdown module."""

import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from jk2bt.risk.drawdown import (
    compute_max_drawdown,
    compute_drawdown,
    check_drawdown_alert,
    compute_recovery_time,
    monitor_stock_drawdown,
    compute_drawdown_statistics,
)


# =====================================================================
# compute_max_drawdown
# =====================================================================


class TestComputeMaxDrawdown:
    def test_empty_series(self):
        assert np.isnan(compute_max_drawdown(pd.Series(dtype=float)))

    def test_none_input(self):
        assert np.isnan(compute_max_drawdown(None))

    def test_single_value(self):
        result = compute_max_drawdown(pd.Series([100.0]))
        assert result == 0.0

    def test_constant_prices(self):
        result = compute_max_drawdown(pd.Series([100.0, 100.0, 100.0]))
        assert result == 0.0

    def test_monotonic_increasing(self):
        prices = pd.Series([100.0, 110.0, 120.0, 130.0])
        result = compute_max_drawdown(prices)
        assert result == 0.0

    def test_simple_drawdown(self):
        prices = pd.Series([100.0, 110.0, 99.0])
        result = compute_max_drawdown(prices)
        assert result == pytest.approx(11.0 / 110.0, rel=1e-6)

    def test_multiple_peaks(self):
        prices = pd.Series([100.0, 120.0, 90.0, 130.0, 100.0])
        result = compute_max_drawdown(prices)
        expected = max((120 - 90) / 120, (130 - 100) / 130)
        assert result == pytest.approx(expected, rel=1e-6)

    def test_large_drawdown(self):
        prices = pd.Series([100.0, 200.0, 50.0])
        result = compute_max_drawdown(prices)
        assert result == pytest.approx(0.75, rel=1e-6)

    def test_with_nan_values(self):
        prices = pd.Series([100.0, np.nan, 110.0, 99.0])
        result = compute_max_drawdown(prices)
        assert not np.isnan(result)

    def test_extreme_values(self):
        prices = pd.Series([1e-10, 1e10, 1e-10])
        result = compute_max_drawdown(prices)
        assert result == pytest.approx(1.0, rel=1e-6)


# =====================================================================
# compute_drawdown
# =====================================================================


class TestComputeDrawdown:
    def test_empty_series(self):
        result = compute_drawdown(pd.Series(dtype=float))
        assert len(result) == 0

    def test_none_input(self):
        result = compute_drawdown(None)
        assert len(result) == 0

    def test_single_value(self):
        result = compute_drawdown(pd.Series([100.0]))
        assert len(result) == 1
        assert result.iloc[0] == 0.0

    def test_monotonic_increasing(self):
        prices = pd.Series([100.0, 110.0, 120.0])
        result = compute_drawdown(prices)
        assert all(result == 0.0)

    def test_drawdown_sequence(self):
        prices = pd.Series([100.0, 110.0, 99.0, 105.0])
        result = compute_drawdown(prices)
        assert result.iloc[0] == 0.0
        assert result.iloc[1] == 0.0
        assert result.iloc[2] == pytest.approx(11.0 / 110.0, rel=1e-6)
        assert result.iloc[3] == pytest.approx(5.0 / 110.0, rel=1e-6)

    def test_volatile_prices(self):
        prices = pd.Series([100.0, 120.0, 90.0, 130.0, 100.0, 140.0, 110.0])
        result = compute_drawdown(prices)
        assert len(result) == len(prices)
        assert result.iloc[0] == 0.0
        assert result.iloc[1] == 0.0
        assert result.iloc[3] == 0.0
        assert result.iloc[5] == 0.0

    def test_with_nan_values(self):
        prices = pd.Series([100.0, np.nan, 110.0, 99.0])
        result = compute_drawdown(prices)
        assert len(result) == len(prices)


# =====================================================================
# check_drawdown_alert
# =====================================================================


class TestCheckDrawdownAlert:
    def test_empty_series(self):
        result = check_drawdown_alert(pd.Series(dtype=float))
        assert np.isnan(result["current_drawdown"])
        assert np.isnan(result["max_drawdown"])
        assert result["status"] == "normal"
        assert result["action"] == "无数据"

    def test_none_input(self):
        result = check_drawdown_alert(None)
        assert result["status"] == "normal"
        assert result["action"] == "无数据"

    def test_normal_status(self):
        prices = pd.Series([100.0, 105.0, 102.0])
        result = check_drawdown_alert(prices, warning_level=0.10, critical_level=0.20)
        assert result["status"] == "normal"
        assert result["action"] == "继续持有"

    def test_warning_status(self):
        prices = pd.Series([100.0, 110.0, 98.0])
        result = check_drawdown_alert(prices, warning_level=0.10, critical_level=0.20)
        assert result["status"] == "warning"

    def test_critical_status(self):
        prices = pd.Series([100.0, 120.0, 90.0])
        result = check_drawdown_alert(prices, warning_level=0.10, critical_level=0.20)
        assert result["status"] == "critical"

    def test_exact_warning_boundary(self):
        prices = pd.Series([100.0, 100.0 / 0.9, 100.0])
        result = check_drawdown_alert(prices, warning_level=0.10, critical_level=0.20)
        dd = result["current_drawdown"]
        if dd >= 0.20:
            assert result["status"] == "critical"
        elif dd >= 0.10:
            assert result["status"] == "warning"
        else:
            assert result["status"] == "normal"

    def test_returns_dict_keys(self):
        prices = pd.Series([100.0, 110.0, 105.0])
        result = check_drawdown_alert(prices)
        assert "current_drawdown" in result
        assert "max_drawdown" in result
        assert "status" in result
        assert "action" in result


# =====================================================================
# compute_recovery_time
# =====================================================================


class TestComputeRecoveryTime:
    def test_empty_series(self):
        result = compute_recovery_time(pd.Series(dtype=float))
        assert np.isnan(result["max_recovery_days"])
        assert result["current_recovery_days"] == 0
        assert result["in_drawdown"] is False

    def test_none_input(self):
        result = compute_recovery_time(None)
        assert result["current_recovery_days"] == 0
        assert result["in_drawdown"] is False

    def test_monotonic_increasing(self):
        prices = pd.Series([100.0, 110.0, 120.0])
        result = compute_recovery_time(prices)
        assert result["max_recovery_days"] == 0
        assert result["in_drawdown"] == False

    def test_single_drawdown_recovered(self):
        prices = pd.Series([100.0, 110.0, 105.0, 100.0, 115.0])
        result = compute_recovery_time(prices)
        assert result["max_recovery_days"] == 2
        assert result["in_drawdown"] == False

    def test_currently_in_drawdown(self):
        prices = pd.Series([100.0, 120.0, 110.0, 105.0])
        result = compute_recovery_time(prices)
        assert result["in_drawdown"] == True
        assert result["current_recovery_days"] == 2

    def test_multiple_drawdowns(self):
        prices = pd.Series([100.0, 120.0, 100.0, 130.0, 110.0, 140.0, 120.0])
        result = compute_recovery_time(prices)
        assert result["max_recovery_days"] > 0
        assert result["in_drawdown"] == True

    def test_returns_dict_keys(self):
        prices = pd.Series([100.0, 110.0, 105.0])
        result = compute_recovery_time(prices)
        assert "max_recovery_days" in result
        assert "current_recovery_days" in result
        assert "in_drawdown" in result


# =====================================================================
# monitor_stock_drawdown (mocked _get_daily_ohlcv)
# =====================================================================


class TestMonitorStockDrawdown:
    def _make_df(self, prices, dates=None):
        if dates is None:
            dates = pd.date_range("2024-01-01", periods=len(prices), freq="B")
        return pd.DataFrame(
            {
                "date": dates,
                "close": prices,
                "open": prices,
                "high": prices,
                "low": prices,
            }
        )

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_normal_data(self, mock_get):
        prices = [100.0, 105.0, 110.0, 108.0, 112.0]
        mock_get.return_value = self._make_df(prices)

        result = monitor_stock_drawdown("000001.XSHE", window=60)

        assert result["symbol"] == "000001.XSHE"
        assert result["status"] == "normal"
        assert not np.isnan(result["current_drawdown"])
        mock_get.assert_called_once()

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_empty_dataframe(self, mock_get):
        mock_get.return_value = pd.DataFrame()

        result = monitor_stock_drawdown("000001.XSHE")

        assert result["status"] == "normal"
        assert result["action"] == "无数据"
        assert np.isnan(result["current_drawdown"])

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_missing_close_column(self, mock_get):
        df = pd.DataFrame(
            {"date": pd.date_range("2024-01-01", periods=10), "open": [100.0] * 10}
        )
        mock_get.return_value = df

        result = monitor_stock_drawdown("000001.XSHE")

        assert result["action"] == "无数据"
        assert np.isnan(result["current_drawdown"])

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_warning_level_triggered(self, mock_get):
        prices = [100.0, 120.0, 105.0]
        mock_get.return_value = self._make_df(prices)

        result = monitor_stock_drawdown(
            "000001.XSHE", warning_level=0.10, critical_level=0.20
        )

        assert result["status"] == "warning"

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_critical_level_triggered(self, mock_get):
        prices = [100.0, 120.0, 90.0]
        mock_get.return_value = self._make_df(prices)

        result = monitor_stock_drawdown(
            "000001.XSHE", warning_level=0.10, critical_level=0.20
        )

        assert result["status"] == "critical"

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_window_truncation(self, mock_get):
        prices = list(range(100, 200))
        mock_get.return_value = self._make_df(prices)

        result = monitor_stock_drawdown("000001.XSHE", window=30)

        assert result["window"] == 30

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_with_end_date(self, mock_get):
        mock_get.return_value = self._make_df([100.0, 105.0, 110.0])

        monitor_stock_drawdown("000001.XSHE", end_date="2024-06-01")

        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["end_date"] == "2024-06-01"


# =====================================================================
# compute_drawdown_statistics (mocked _get_daily_ohlcv)
# =====================================================================


class TestComputeDrawdownStatistics:
    def _make_df(self, prices, dates=None):
        if dates is None:
            dates = pd.date_range("2024-01-01", periods=len(prices), freq="B")
        return pd.DataFrame(
            {
                "date": dates,
                "close": prices,
                "open": prices,
                "high": prices,
                "low": prices,
            }
        )

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_normal_data(self, mock_get):
        prices = [100.0, 105.0, 110.0, 108.0, 112.0, 107.0, 115.0]
        mock_get.return_value = self._make_df(prices)

        result = compute_drawdown_statistics("000001.XSHE", window=252)

        assert result["symbol"] == "000001.XSHE"
        assert not np.isnan(result["max_drawdown"])
        assert not np.isnan(result["avg_drawdown"])
        assert not np.isnan(result["current_drawdown"])
        assert "drawdown_days" in result
        assert "window" in result

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_empty_dataframe(self, mock_get):
        mock_get.return_value = pd.DataFrame()

        result = compute_drawdown_statistics("000001.XSHE")

        assert np.isnan(result["max_drawdown"])
        assert np.isnan(result["avg_drawdown"])
        assert result["drawdown_days"] == 0

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_missing_close_column(self, mock_get):
        df = pd.DataFrame(
            {"date": pd.date_range("2024-01-01", periods=10), "open": [100.0] * 10}
        )
        mock_get.return_value = df

        result = compute_drawdown_statistics("000001.XSHE")

        assert np.isnan(result["max_drawdown"])
        assert result["drawdown_days"] == 0

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_no_drawdown(self, mock_get):
        prices = [100.0, 101.0, 102.0, 103.0, 104.0]
        mock_get.return_value = self._make_df(prices)

        result = compute_drawdown_statistics("000001.XSHE")

        assert result["max_drawdown"] == 0.0
        assert result["drawdown_days"] == 0

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_with_drawdown_days(self, mock_get):
        prices = [100.0, 120.0, 110.0, 105.0, 115.0, 130.0, 120.0]
        mock_get.return_value = self._make_df(prices)

        result = compute_drawdown_statistics("000001.XSHE")

        assert result["drawdown_days"] > 0
        assert result["max_drawdown"] > 0

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_window_truncation(self, mock_get):
        prices = list(range(100, 400))
        mock_get.return_value = self._make_df(prices)

        result = compute_drawdown_statistics("000001.XSHE", window=60)

        assert result["window"] == 60

    @patch("jk2bt.risk.drawdown._get_daily_ohlcv")
    def test_returns_dict_keys(self, mock_get):
        mock_get.return_value = self._make_df([100.0, 105.0, 110.0])

        result = compute_drawdown_statistics("000001.XSHE")

        expected_keys = {
            "symbol",
            "max_drawdown",
            "avg_drawdown",
            "current_drawdown",
            "drawdown_days",
            "window",
        }
        assert set(result.keys()) == expected_keys
