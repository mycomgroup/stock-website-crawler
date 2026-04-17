"""
tests/unit/data/market/test_lof.py
单元测试 for jk2bt/data/market/lof.py

覆盖场景:
- get_lof_daily: 正常获取、重试逻辑、数据源失败、空数据、日期过滤
- get_lof_spot: 正常获取、异常处理
- get_lof_min: 正常获取、分钟数据标准化
- get_lof_nav: 正常获取、净值数据标准化
- get_lof_daily_with_fallback: 优先行情、优先净值、回退逻辑
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def _make_lof_daily_df(start="2024-01-02", rows=5):
    """生成 LOF 日线数据（中文列名）"""
    dates = pd.date_range(start, periods=rows, freq="B")
    return pd.DataFrame(
        {
            "日期": dates,
            "开盘": [10.0 + i for i in range(rows)],
            "最高": [11.0 + i for i in range(rows)],
            "最低": [9.0 + i for i in range(rows)],
            "收盘": [10.5 + i for i in range(rows)],
            "成交量": [1000 + i * 100 for i in range(rows)],
            "成交额": [10000.0 + i * 1000 for i in range(rows)],
        }
    )


def _make_lof_min_df(start="2024-01-02 09:30:00", rows=10):
    """生成 LOF 分钟数据（中文列名）"""
    dates = pd.to_datetime([start]) + pd.to_timedelta([f"{i}min" for i in range(rows)])
    return pd.DataFrame(
        {
            "时间": dates,
            "开盘": [10.0 + i * 0.1 for i in range(rows)],
            "最高": [10.5 + i * 0.1 for i in range(rows)],
            "最低": [9.5 + i * 0.1 for i in range(rows)],
            "收盘": [10.2 + i * 0.1 for i in range(rows)],
            "成交量": [100 + i * 10 for i in range(rows)],
            "成交额": [1000.0 + i * 100 for i in range(rows)],
        }
    )


def _make_lof_nav_df(start="2024-01-02", rows=5):
    """生成 LOF 净值数据（中文列名）"""
    dates = pd.date_range(start, periods=rows, freq="D")
    return pd.DataFrame(
        {
            "净值日期": dates,
            "单位净值": [1.0 + i * 0.05 for i in range(rows)],
            "累计净值": [1.1 + i * 0.05 for i in range(rows)],
            "日增长率": [1.0 + i * 0.2 for i in range(rows)],
            "申购状态": ["开放" for _ in range(rows)],
            "赎回状态": ["开放" for _ in range(rows)],
        }
    )


def _make_sample_df(start="2024-01-02", rows=5):
    """生成标准化 OHLCV 测试数据"""
    dates = pd.date_range(start, periods=rows, freq="B")
    return pd.DataFrame(
        {
            "datetime": dates,
            "open": [10.0 + i for i in range(rows)],
            "high": [11.0 + i for i in range(rows)],
            "low": [9.0 + i for i in range(rows)],
            "close": [10.5 + i for i in range(rows)],
            "volume": [1000 + i * 100 for i in range(rows)],
            "amount": [10000.0 + i * 1000 for i in range(rows)],
        }
    )


class TestGetLofDaily:
    """测试 get_lof_daily 函数"""

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_first_attempt_success(self, mock_get_adapter):
        """第一次尝试成功获取数据"""
        raw_df = _make_lof_daily_df()

        adapter_mock = MagicMock()
        adapter_mock.get_lof_hist.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_daily

        result = get_lof_daily("161725", "2024-01-01", "2024-01-31", retry_count=3)

        adapter_mock.get_lof_hist.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_retry_success_on_second_attempt(self, mock_get_adapter):
        """第二次重试成功"""
        raw_df = _make_lof_daily_df()

        adapter_mock = MagicMock()
        adapter_mock.get_lof_hist.side_effect = [
            pd.DataFrame(),
            raw_df,
        ]
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_daily

        result = get_lof_daily("161725", "2024-01-01", "2024-01-31", retry_count=3)

        assert adapter_mock.get_lof_hist.call_count == 2
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_all_retries_fail_raises(self, mock_get_adapter):
        """所有重试失败时抛出 ValueError"""
        adapter_mock = MagicMock()
        adapter_mock.get_lof_hist.side_effect = Exception("Network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_daily

        with pytest.raises(ValueError, match="LOF 数据获取失败"):
            get_lof_daily("161725", "2024-01-01", "2024-01-31", retry_count=2)

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_adapter_returns_empty(self, mock_get_adapter):
        """adapter 返回空数据时抛出 ValueError"""
        adapter_mock = MagicMock()
        adapter_mock.get_lof_hist.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_daily

        with pytest.raises(ValueError, match="LOF 数据获取失败"):
            get_lof_daily("161725", "2024-01-01", "2024-01-31")

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_date_filtering(self, mock_get_adapter):
        """日期过滤功能"""
        raw_df = _make_lof_daily_df(rows=15)

        adapter_mock = MagicMock()
        adapter_mock.get_lof_hist.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_daily

        result = get_lof_daily("161725", "2024-01-05", "2024-01-10")

        assert result["datetime"].min() >= pd.to_datetime("2024-01-05")
        assert result["datetime"].max() <= pd.to_datetime("2024-01-10")

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_column_mapping(self, mock_get_adapter):
        """列名应正确映射"""
        raw_df = _make_lof_daily_df()

        adapter_mock = MagicMock()
        adapter_mock.get_lof_hist.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_daily

        result = get_lof_daily("161725", "2024-01-01", "2024-01-10")

        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "high" in result.columns
        assert "low" in result.columns
        assert "close" in result.columns
        assert "volume" in result.columns


class TestGetLofSpot:
    """测试 get_lof_spot 函数"""

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """正常获取 LOF 实时行情"""
        mock_df = pd.DataFrame(
            {
                "代码": ["161725", "160632"],
                "名称": ["白酒指数LOF", "军工指数LOF"],
                "最新价": [1.5, 2.0],
            }
        )

        adapter_mock = MagicMock()
        adapter_mock.get_lof_spot.return_value = mock_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_spot

        result = get_lof_spot()

        adapter_mock.get_lof_spot.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_adapter_raises(self, mock_get_adapter):
        """adapter 抛出异常时应向上传播"""
        adapter_mock = MagicMock()
        adapter_mock.get_lof_spot.side_effect = Exception("Network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_spot

        with pytest.raises(Exception, match="Network error"):
            get_lof_spot()


class TestGetLofMin:
    """测试 get_lof_min 函数"""

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """正常获取 LOF 分钟数据"""
        raw_df = _make_lof_min_df()

        adapter_mock = MagicMock()
        adapter_mock.get_lof_hist_min.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_min

        result = get_lof_min("161725", period="5")

        adapter_mock.get_lof_hist_min.assert_called_once()
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_retry_success(self, mock_get_adapter):
        """重试后成功"""
        raw_df = _make_lof_min_df()

        adapter_mock = MagicMock()
        adapter_mock.get_lof_hist_min.side_effect = [
            pd.DataFrame(),
            raw_df,
        ]
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_min

        result = get_lof_min("161725", retry_count=2)

        assert adapter_mock.get_lof_hist_min.call_count == 2
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_all_retries_fail_raises(self, mock_get_adapter):
        """所有重试失败时抛出 ValueError"""
        adapter_mock = MagicMock()
        adapter_mock.get_lof_hist_min.side_effect = Exception("Network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_min

        with pytest.raises(ValueError, match="LOF 分钟数据获取失败"):
            get_lof_min("161725", retry_count=2)


class TestGetLofNav:
    """测试 get_lof_nav 函数"""

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """正常获取 LOF 净值数据"""
        raw_df = _make_lof_nav_df()

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_nav

        result = get_lof_nav("161725", "2024-01-01", "2024-01-31")

        adapter_mock.get_fund_of_nav.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_adapter_returns_empty_raises(self, mock_get_adapter):
        """adapter 返回空数据时抛出 ValueError"""
        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_nav

        with pytest.raises(ValueError, match="LOF 净值数据为空"):
            get_lof_nav("161725")

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_date_filtering(self, mock_get_adapter):
        """日期过滤功能"""
        raw_df = _make_lof_nav_df(rows=15)

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_nav

        result = get_lof_nav("161725", "2024-01-05", "2024-01-10")

        assert result["datetime"].min() >= pd.to_datetime("2024-01-05")
        assert result["datetime"].max() <= pd.to_datetime("2024-01-10")

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_column_mapping(self, mock_get_adapter):
        """列名应正确映射"""
        raw_df = _make_lof_nav_df()

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_nav

        result = get_lof_nav("161725")

        assert "datetime" in result.columns
        assert "unit_nav" in result.columns
        assert "acc_nav" in result.columns
        assert "daily_growth_rate" in result.columns

    @patch("jk2bt.data.market.lof.get_adapter")
    def test_sort_by_datetime(self, mock_get_adapter):
        """结果应按日期排序"""
        raw_df = _make_lof_nav_df()
        raw_df = raw_df.sample(frac=1).reset_index(drop=True)

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.lof import get_lof_nav

        result = get_lof_nav("161725")

        assert result["datetime"].is_monotonic_increasing


class TestGetLofDailyWithFallback:
    """测试 get_lof_daily_with_fallback 函数"""

    @patch("jk2bt.data.market.lof.get_lof_nav")
    @patch("jk2bt.data.market.lof.get_lof_daily")
    def test_prefer_nav_first(self, mock_daily, mock_nav):
        """prefer_nav=True 时优先使用净值数据"""
        nav_df = _make_lof_nav_df()
        mock_nav.return_value = nav_df

        from jk2bt.data.market.lof import get_lof_daily_with_fallback

        result = get_lof_daily_with_fallback(
            "161725", "2024-01-01", "2024-01-31", prefer_nav=True
        )

        mock_nav.assert_called_once()
        mock_daily.assert_not_called()
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.lof.get_lof_nav")
    @patch("jk2bt.data.market.lof.get_lof_daily")
    def test_prefer_nav_fallback_to_daily(self, mock_daily, mock_nav):
        """prefer_nav=True 但净值失败时回退到行情"""
        daily_df = _make_lof_daily_df()
        mock_nav.side_effect = Exception("NAV error")
        mock_daily.return_value = daily_df

        from jk2bt.data.market.lof import get_lof_daily_with_fallback

        result = get_lof_daily_with_fallback(
            "161725", "2024-01-01", "2024-01-31", prefer_nav=True
        )

        mock_nav.assert_called_once()
        mock_daily.assert_called_once()
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.lof.get_lof_nav")
    @patch("jk2bt.data.market.lof.get_lof_daily")
    def test_prefer_daily_first(self, mock_daily, mock_nav):
        """prefer_nav=False 时优先使用行情数据"""
        daily_df = _make_lof_daily_df()
        mock_daily.return_value = daily_df

        from jk2bt.data.market.lof import get_lof_daily_with_fallback

        result = get_lof_daily_with_fallback(
            "161725", "2024-01-01", "2024-01-31", prefer_nav=False
        )

        mock_daily.assert_called_once()
        mock_nav.assert_not_called()
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.lof.get_lof_nav")
    @patch("jk2bt.data.market.lof.get_lof_daily")
    def test_daily_fails_fallback_to_nav(self, mock_daily, mock_nav):
        """行情失败时回退到净值"""
        nav_df = _make_lof_nav_df()
        mock_daily.side_effect = Exception("Daily error")
        mock_nav.return_value = nav_df

        from jk2bt.data.market.lof import get_lof_daily_with_fallback

        result = get_lof_daily_with_fallback(
            "161725", "2024-01-01", "2024-01-31", prefer_nav=False
        )

        mock_daily.assert_called_once()
        mock_nav.assert_called_once()
        assert isinstance(result, pd.DataFrame)
