"""
tests/unit/data/market/test_north_money.py
单元测试 for jk2bt/data/market/north_money.py

覆盖场景:
- get_north_money_flow: 正常获取、日期过滤、异常处理
- get_north_money_daily: 正常获取、空数据处理
- get_north_money_holdings: 正常获取、排序验证
- get_north_money_stock_flow: 股票代码标准化、正常获取、日期过滤
- get_north_money_stock_detail: 正常获取、空数据处理
- compute_north_money_signal: 流入信号、流出信号、中性信号、数据不足
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def _make_north_flow_df(start="2024-01-02", rows=10):
    """生成北向资金流入数据"""
    dates = pd.date_range(start, periods=rows, freq="B")
    return pd.DataFrame(
        {
            "日期": dates,
            "当日净流入": [10.0 + i * 2 for i in range(rows)],
            "当日资金流入": [100.0 + i * 5 for i in range(rows)],
            "当日资金流出": [90.0 + i * 3 for i in range(rows)],
        }
    )


def _make_north_holdings_df(rows=5):
    """生成北向资金持股数据"""
    return pd.DataFrame(
        {
            "股票代码": [f"60000{i}" for i in range(rows)],
            "股票名称": [f"股票{i}" for i in range(rows)],
            "持股数量": [1000000 + i * 100000 for i in range(rows)],
            "持股市值": [10000000 + i * 500000 for i in range(rows)],
            "持股数量占A股百分比": [1.0 + i * 0.1 for i in range(rows)],
            "持股市值占A股百分比": [1.5 + i * 0.2 for i in range(rows)],
            "持股数量变化": [10000 + i * 1000 for i in range(rows)],
            "持股市值变化": [50000 + i * 5000 for i in range(rows)],
        }
    )


def _make_north_stock_flow_df(symbol="600000", start="2024-01-02", rows=5):
    """生成个股北向资金流入数据"""
    dates = pd.date_range(start, periods=rows, freq="B")
    return pd.DataFrame(
        {
            "日期": dates,
            "当日净流入": [5.0 + i for i in range(rows)],
            "当日资金流入": [50.0 + i * 2 for i in range(rows)],
            "当日资金流出": [45.0 + i * 1.5 for i in range(rows)],
        }
    )


class TestGetNorthMoneyFlow:
    """测试 get_north_money_flow 函数"""

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """正常获取北向资金流入数据"""
        raw_df = _make_north_flow_df()

        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_north_net_flow.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_flow

        result = get_north_money_flow("2024-01-01", "2024-01-31")

        adapter_mock.get_hsgt_north_net_flow.assert_called_once_with(symbol="北上")
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert "date" in result.columns
        assert "net_inflow" in result.columns

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_date_filtering(self, mock_get_adapter):
        """日期过滤功能"""
        raw_df = _make_north_flow_df(rows=20)

        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_north_net_flow.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_flow

        result = get_north_money_flow("2024-01-10", "2024-01-20")

        assert result["date"].min() >= pd.to_datetime("2024-01-10")
        assert result["date"].max() <= pd.to_datetime("2024-01-20")

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_adapter_returns_empty(self, mock_get_adapter):
        """adapter 返回空数据时返回空 DataFrame"""
        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_north_net_flow.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_flow

        result = get_north_money_flow()

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_adapter_raises_exception(self, mock_get_adapter):
        """adapter 抛出异常时返回空 DataFrame"""
        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_north_net_flow.side_effect = Exception("Network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_flow

        result = get_north_money_flow()

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_no_date_filter(self, mock_get_adapter):
        """不提供日期时不过滤"""
        raw_df = _make_north_flow_df(rows=10)

        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_north_net_flow.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_flow

        result = get_north_money_flow()

        assert len(result) == 10


class TestGetNorthMoneyDaily:
    """测试 get_north_money_daily 函数"""

    @patch("jk2bt.data.market.north_money.get_north_money_flow")
    def test_normal_case(self, mock_flow):
        """正常获取某日北向资金数据"""
        raw_df = _make_north_flow_df(rows=5)
        mock_flow.return_value = raw_df

        from jk2bt.data.market.north_money import get_north_money_daily

        result = get_north_money_daily("2024-01-05")

        assert isinstance(result, dict)
        assert "net_inflow" in result
        assert "inflow" in result
        assert "outflow" in result
        assert result["net_inflow"] > 0

    @patch("jk2bt.data.market.north_money.get_north_money_flow")
    def test_empty_dataframe(self, mock_flow):
        """空数据时返回零值"""
        mock_flow.return_value = pd.DataFrame()

        from jk2bt.data.market.north_money import get_north_money_daily

        result = get_north_money_daily()

        assert result["net_inflow"] == 0.0
        assert result["inflow"] == 0.0
        assert result["outflow"] == 0.0


class TestGetNorthMoneyHoldings:
    """测试 get_north_money_holdings 函数"""

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """正常获取北向资金持股数据"""
        raw_df = _make_north_holdings_df()

        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_hold_stock.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_holdings

        result = get_north_money_holdings(top_n=3)

        adapter_mock.get_hsgt_hold_stock.assert_called_once_with(
            symbol="北向", indicator="今日"
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert "code" in result.columns
        assert "holding_value" in result.columns

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_sorted_by_holding_value(self, mock_get_adapter):
        """结果应按持股市值降序排列"""
        raw_df = _make_north_holdings_df()

        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_hold_stock.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_holdings

        result = get_north_money_holdings()

        values = result["holding_value"].values
        assert all(values[i] >= values[i + 1] for i in range(len(values) - 1))

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_adapter_returns_empty(self, mock_get_adapter):
        """adapter 返回空时返回空 DataFrame"""
        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_hold_stock.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_holdings

        result = get_north_money_holdings()

        assert isinstance(result, pd.DataFrame)
        assert result.empty


class TestGetNorthMoneyStockFlow:
    """测试 get_north_money_stock_flow 函数"""

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """正常获取个股北向资金流入"""
        raw_df = _make_north_stock_flow_df()

        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_individual_stock_flow.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_stock_flow

        result = get_north_money_stock_flow("sh600000", "2024-01-01", "2024-01-10")

        adapter_mock.get_hsgt_individual_stock_flow.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert "date" in result.columns
        assert "net_inflow" in result.columns

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_symbol_normalization(self, mock_get_adapter):
        """股票代码应被标准化处理"""
        raw_df = _make_north_stock_flow_df()

        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_individual_stock_flow.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_stock_flow

        get_north_money_stock_flow("sz000001", "2024-01-01", "2024-01-10")

        call_args = adapter_mock.get_hsgt_individual_stock_flow.call_args
        assert call_args.kwargs["stock"] == "000001"

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_date_filtering(self, mock_get_adapter):
        """日期过滤功能"""
        raw_df = _make_north_stock_flow_df(rows=10)

        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_individual_stock_flow.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_stock_flow

        result = get_north_money_stock_flow("600000", "2024-01-05", "2024-01-08")

        assert result["date"].min() >= pd.to_datetime("2024-01-05")
        assert result["date"].max() <= pd.to_datetime("2024-01-08")

    @patch("jk2bt.data.market.north_money.get_adapter")
    def test_adapter_returns_empty(self, mock_get_adapter):
        """adapter 返回空时返回空 DataFrame"""
        adapter_mock = MagicMock()
        adapter_mock.get_hsgt_individual_stock_flow.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.north_money import get_north_money_stock_flow

        result = get_north_money_stock_flow("600000")

        assert isinstance(result, pd.DataFrame)
        assert result.empty


class TestGetNorthMoneyStockDetail:
    """测试 get_north_money_stock_detail 函数"""

    @patch("jk2bt.data.market.north_money.get_north_money_stock_flow")
    def test_normal_case(self, mock_flow):
        """正常获取个股北向资金详情"""
        raw_df = _make_north_stock_flow_df(rows=3)
        mock_flow.return_value = raw_df

        from jk2bt.data.market.north_money import get_north_money_stock_detail

        result = get_north_money_stock_detail("600000", "2024-01-05")

        assert isinstance(result, dict)
        assert "net_inflow" in result
        assert "holdings" in result
        assert "holding_change" in result

    @patch("jk2bt.data.market.north_money.get_north_money_stock_flow")
    def test_empty_dataframe(self, mock_flow):
        """空数据时返回零值"""
        mock_flow.return_value = pd.DataFrame()

        from jk2bt.data.market.north_money import get_north_money_stock_detail

        result = get_north_money_stock_detail("600000")

        assert result["net_inflow"] == 0.0
        assert result["holdings"] == 0.0
        assert result["holding_change"] == 0.0


class TestComputeNorthMoneySignal:
    """测试 compute_north_money_signal 函数"""

    @patch("jk2bt.data.market.north_money.get_north_money_flow")
    def test_inflow_signal(self, mock_flow):
        """持续流入信号（avg > threshold）"""
        raw_df = _make_north_flow_df(rows=25)
        mock_flow.return_value = raw_df

        from jk2bt.data.market.north_money import compute_north_money_signal

        result = compute_north_money_signal(window=20, threshold=30.0)

        assert result["signal"] == 1
        assert "net_inflow" in result
        assert "avg_inflow" in result
        assert "description" in result

    @patch("jk2bt.data.market.north_money.get_north_money_flow")
    def test_outflow_signal(self, mock_flow):
        """持续流出信号（avg < -threshold）"""
        dates = pd.date_range("2024-01-02", periods=25, freq="B")
        raw_df = pd.DataFrame(
            {
                "日期": dates,
                "当日净流入": [-50.0 - i * 2 for i in range(25)],
                "当日资金流入": [100.0 + i * 5 for i in range(25)],
                "当日资金流出": [150.0 + i * 7 for i in range(25)],
            }
        )
        mock_flow.return_value = raw_df

        from jk2bt.data.market.north_money import compute_north_money_signal

        result = compute_north_money_signal(window=20, threshold=30.0)

        assert result["signal"] == -1

    @patch("jk2bt.data.market.north_money.get_north_money_flow")
    def test_neutral_signal(self, mock_flow):
        """中性信号（-threshold <= avg <= threshold）"""
        dates = pd.date_range("2024-01-02", periods=25, freq="B")
        raw_df = pd.DataFrame(
            {
                "日期": dates,
                "当日净流入": [10.0 + i * 0.5 for i in range(25)],
                "当日资金流入": [100.0 + i * 5 for i in range(25)],
                "当日资金流出": [90.0 + i * 4.5 for i in range(25)],
            }
        )
        mock_flow.return_value = raw_df

        from jk2bt.data.market.north_money import compute_north_money_signal

        result = compute_north_money_signal(window=20, threshold=30.0)

        assert result["signal"] == 0

    @patch("jk2bt.data.market.north_money.get_north_money_flow")
    def test_insufficient_data(self, mock_flow):
        """数据不足时返回中性信号"""
        raw_df = _make_north_flow_df(rows=5)
        mock_flow.return_value = raw_df

        from jk2bt.data.market.north_money import compute_north_money_signal

        result = compute_north_money_signal(window=20)

        assert result["signal"] == 0
        assert result["description"] == "数据不足"

    @patch("jk2bt.data.market.north_money.get_north_money_flow")
    def test_empty_dataframe(self, mock_flow):
        """空数据时返回默认值"""
        mock_flow.return_value = pd.DataFrame()

        from jk2bt.data.market.north_money import compute_north_money_signal

        result = compute_north_money_signal(window=20)

        assert result["signal"] == 0
        assert result["net_inflow"] == 0.0
        assert result["avg_inflow"] == 0.0
