"""
tests/unit/analysis/signals/test_signals_data_fetcher.py
单元测试：信号检测模块数据获取器 (data_fetcher.py)

覆盖函数：
- _fetch_ohlcv

测试场景：
- 正常数据获取
- 空数据处理
- datetime 列转换
- amount/money 列处理
- 数据适配器交互
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from jk2bt.data.sources import set_adapter, MockDataSource


def _make_dates(count: int, end_date: str = "2024-06-30") -> list:
    """生成 count 个交易日（跳过周末）"""
    end = pd.Timestamp(end_date)
    dates = []
    current = end
    while len(dates) < count:
        if current.weekday() < 5:
            dates.append(current)
        current -= timedelta(days=1)
    dates.reverse()
    return dates


def _make_ohlcv(closes: list, end_date: str = "2024-06-30") -> pd.DataFrame:
    """根据收盘价序列构造 OHLCV DataFrame"""
    n = len(closes)
    dates = _make_dates(n, end_date)
    opens = [c * 0.99 for c in closes]
    highs = [c * 1.01 for c in closes]
    lows = [c * 0.98 for c in closes]
    volumes = [1000000 + i * 1000 for i in range(n)]

    return pd.DataFrame(
        {
            "datetime": dates,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
            "amount": [o * v for o, v in zip(opens, volumes)],
        }
    )


class TestFetchOhlcv:
    """_fetch_ohlcv 函数测试"""

    def _setup_mock_with_data(self, df: pd.DataFrame, symbol: str = "TEST001"):
        """设置 Mock 数据源并注入数据"""
        mock = MockDataSource(seed=42, generate_random=False)
        mock.set_mock_data("daily", symbol, df)
        set_adapter(mock)
        return mock

    @patch("jk2bt.analysis.signals.data_fetcher.get_adapter")
    def test_normal_fetch(self, mock_get_adapter):
        """测试正常数据获取"""
        closes = [100.0 + i for i in range(100)]
        df = _make_ohlcv(closes)
        df["date"] = df["datetime"].dt.strftime("%Y-%m-%d")

        mock_adapter = MagicMock()
        mock_adapter.get_daily_data.return_value = df
        mock_get_adapter.return_value = mock_adapter

        from jk2bt.analysis.signals.data_fetcher import _fetch_ohlcv

        result = _fetch_ohlcv("TEST001", "2024-06-30", 100)

        mock_adapter.get_daily_data.assert_called_once()
        assert not result.empty
        assert "date" in result.columns

    @patch("jk2bt.analysis.signals.data_fetcher.get_adapter")
    def test_empty_dataframe(self, mock_get_adapter):
        """测试空数据框处理"""
        mock_adapter = MagicMock()
        mock_adapter.get_daily_data.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        from jk2bt.analysis.signals.data_fetcher import _fetch_ohlcv

        result = _fetch_ohlcv("TEST001", "2024-06-30", 100)

        assert result.empty

    @patch("jk2bt.analysis.signals.data_fetcher.get_adapter")
    def test_datetime_column_conversion(self, mock_get_adapter):
        """测试 datetime 列转换为 date 列"""
        dates = pd.date_range("2024-01-01", periods=50, freq="B")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [100.0] * 50,
                "high": [101.0] * 50,
                "low": [99.0] * 50,
                "close": [100.0] * 50,
                "volume": [1000000] * 50,
            }
        )

        mock_adapter = MagicMock()
        mock_adapter.get_daily_data.return_value = df
        mock_get_adapter.return_value = mock_adapter

        from jk2bt.analysis.signals.data_fetcher import _fetch_ohlcv

        result = _fetch_ohlcv("TEST001", "2024-06-30", 50)

        assert "date" in result.columns
        assert result["date"].iloc[0] == "2024-01-01"

    @patch("jk2bt.analysis.signals.data_fetcher.get_adapter")
    def test_amount_to_money_conversion(self, mock_get_adapter):
        """测试 amount 列转换为 money 列"""
        df = _make_ohlcv([100.0] * 50)
        if "datetime" in df.columns:
            df["date"] = df["datetime"].dt.strftime("%Y-%m-%d")
        if "money" in df.columns:
            del df["money"]

        mock_adapter = MagicMock()
        mock_adapter.get_daily_data.return_value = df
        mock_get_adapter.return_value = mock_adapter

        from jk2bt.analysis.signals.data_fetcher import _fetch_ohlcv

        result = _fetch_ohlcv("TEST001", "2024-06-30", 50)

        assert "money" in result.columns

    @patch("jk2bt.analysis.signals.data_fetcher.get_adapter")
    def test_end_date_none_uses_current(self, mock_get_adapter):
        """测试 end_date 为 None 时使用当前日期"""
        mock_adapter = MagicMock()
        mock_adapter.get_daily_data.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        from jk2bt.analysis.signals.data_fetcher import _fetch_ohlcv

        result = _fetch_ohlcv("TEST001", None, 100)

        mock_adapter.get_daily_data.assert_called_once()
        call_args = mock_adapter.get_daily_data.call_args
        assert call_args[0][0] == "TEST001"
        start_date_arg = call_args[0][1]
        assert start_date_arg is not None

    @patch("jk2bt.analysis.signals.data_fetcher.get_adapter")
    def test_count_multiplier_for_start_date(self, mock_get_adapter):
        """测试 start_date 计算使用 count * 1.5 倍数"""
        mock_adapter = MagicMock()
        mock_adapter.get_daily_data.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        from jk2bt.analysis.signals.data_fetcher import _fetch_ohlcv

        _fetch_ohlcv("TEST001", "2024-06-30", 100)

        call_args = mock_adapter.get_daily_data.call_args
        start_date = call_args[0][1]
        end_date = call_args[0][2]
        assert end_date == "2024-06-30"
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        days_diff = (end_dt - start_dt).days
        assert days_diff >= 100 * 1.5 - 5

    @patch("jk2bt.analysis.signals.data_fetcher.get_adapter")
    def test_result_preserves_columns(self, mock_get_adapter):
        """测试返回结果保留原始列"""
        closes = [100.0 + i for i in range(50)]
        df = _make_ohlcv(closes)
        df["date"] = df["datetime"].dt.strftime("%Y-%m-%d")

        mock_adapter = MagicMock()
        mock_adapter.get_daily_data.return_value = df
        mock_get_adapter.return_value = mock_adapter

        from jk2bt.analysis.signals.data_fetcher import _fetch_ohlcv

        result = _fetch_ohlcv("TEST001", "2024-06-30", 50)

        assert "close" in result.columns
        assert "open" in result.columns
        assert "high" in result.columns
        assert "low" in result.columns
        assert "volume" in result.columns

    @patch("jk2bt.analysis.signals.data_fetcher.get_adapter")
    def test_no_datetime_column(self, mock_get_adapter):
        """测试数据中没有 datetime 列的情况"""
        df = pd.DataFrame(
            {
                "date": pd.date_range("2024-01-01", periods=50, freq="B").strftime(
                    "%Y-%m-%d"
                ),
                "open": [100.0] * 50,
                "high": [101.0] * 50,
                "low": [99.0] * 50,
                "close": [100.0] * 50,
                "volume": [1000000] * 50,
            }
        )

        mock_adapter = MagicMock()
        mock_adapter.get_daily_data.return_value = df
        mock_get_adapter.return_value = mock_adapter

        from jk2bt.analysis.signals.data_fetcher import _fetch_ohlcv

        result = _fetch_ohlcv("TEST001", "2024-06-30", 50)

        assert "date" in result.columns

    @patch("jk2bt.analysis.signals.data_fetcher.get_adapter")
    def test_data_copy(self, mock_get_adapter):
        """测试返回的是数据副本而非原始引用"""
        closes = [100.0 + i for i in range(50)]
        df = _make_ohlcv(closes)
        df["date"] = df["datetime"].dt.strftime("%Y-%m-%d")

        mock_adapter = MagicMock()
        mock_adapter.get_daily_data.return_value = df
        mock_get_adapter.return_value = mock_adapter

        from jk2bt.analysis.signals.data_fetcher import _fetch_ohlcv

        result = _fetch_ohlcv("TEST001", "2024-06-30", 50)

        assert result is not df
