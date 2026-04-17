"""
tests/unit/data/market/test_fund_of.py
单元测试 for jk2bt/data/market/fund_of.py

覆盖场景:
- standardize_fund_nav: 列名映射、日期处理、数值类型转换、字段选择
- get_fund_of_nav: 正常获取、日期过滤、空数据处理
- get_fund_of_daily_list: 正常获取、异常处理
- get_fund_of_info: 正常获取基本信息、返回空字典
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def _make_fund_nav_df(start="2024-01-02", rows=5):
    """生成场外基金净值数据（中文列名）"""
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


def _make_fund_info_df():
    """生成场外基金基本信息数据"""
    return pd.DataFrame(
        {
            "基金简称": ["华夏成长混合"],
            "基金类型": ["混合型"],
            "基金管理人": ["华夏基金"],
        }
    )


class TestStandardizeFundNav:
    """测试 standardize_fund_nav 函数"""

    def test_column_mapping(self):
        """列名应正确映射"""
        from jk2bt.data.market.fund_of import standardize_fund_nav

        raw_df = _make_fund_nav_df()
        result = standardize_fund_nav(raw_df)

        assert "datetime" in result.columns
        assert "unit_nav" in result.columns
        assert "acc_nav" in result.columns
        assert "daily_growth_rate" in result.columns
        assert "purchase_status" in result.columns
        assert "redeem_status" in result.columns

    def test_datetime_conversion(self):
        """日期列应转换为 datetime 类型"""
        from jk2bt.data.market.fund_of import standardize_fund_nav

        raw_df = _make_fund_nav_df()
        result = standardize_fund_nav(raw_df)

        assert pd.api.types.is_datetime64_any_dtype(result["datetime"])

    def test_sort_by_datetime(self):
        """结果应按日期排序"""
        from jk2bt.data.market.fund_of import standardize_fund_nav

        raw_df = _make_fund_nav_df()
        raw_df = raw_df.sample(frac=1).reset_index(drop=True)
        result = standardize_fund_nav(raw_df)

        assert result["datetime"].is_monotonic_increasing

    def test_drop_na_datetime(self):
        """日期为空时应该删除该行"""
        from jk2bt.data.market.fund_of import standardize_fund_nav

        raw_df = _make_fund_nav_df()
        raw_df.loc[2, "净值日期"] = pd.NaT
        result = standardize_fund_nav(raw_df)

        assert len(result) == len(raw_df) - 1

    def test_numeric_conversion(self):
        """数值列应转换为数值类型"""
        from jk2bt.data.market.fund_of import standardize_fund_nav

        raw_df = _make_fund_nav_df()
        result = standardize_fund_nav(raw_df)

        assert pd.api.types.is_numeric_dtype(result["unit_nav"])
        assert pd.api.types.is_numeric_dtype(result["acc_nav"])
        assert pd.api.types.is_numeric_dtype(result["daily_growth_rate"])

    def test_select_required_columns(self):
        """结果只应包含必要字段"""
        from jk2bt.data.market.fund_of import standardize_fund_nav

        raw_df = _make_fund_nav_df()
        result = standardize_fund_nav(raw_df)

        expected_cols = [
            "datetime",
            "unit_nav",
            "acc_nav",
            "daily_growth_rate",
            "purchase_status",
            "redeem_status",
        ]
        assert list(result.columns) == expected_cols

    def test_partial_columns(self):
        """只有部分列时也應正常處理"""
        from jk2bt.data.market.fund_of import standardize_fund_nav

        raw_df = pd.DataFrame(
            {
                "净值日期": pd.date_range("2024-01-01", periods=3),
                "单位净值": [1.0, 1.1, 1.2],
            }
        )
        result = standardize_fund_nav(raw_df)

        assert "datetime" in result.columns
        assert "unit_nav" in result.columns
        assert "acc_nav" not in result.columns


class TestGetFundOfNav:
    """测试 get_fund_of_nav 函数"""

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """正常获取场外基金净值数据"""
        raw_df = _make_fund_nav_df()

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_nav

        result = get_fund_of_nav("000001", "2024-01-01", "2024-01-31")

        adapter_mock.get_fund_of_nav.assert_called_once_with(symbol="000001")
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_adapter_returns_empty_raises(self, mock_get_adapter):
        """adapter 返回空数据时抛出 ValueError"""
        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_nav

        with pytest.raises(ValueError, match="基金净值数据为空"):
            get_fund_of_nav("000001")

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_adapter_raises(self, mock_get_adapter):
        """adapter 抛出异常时向上传播"""
        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.side_effect = Exception("Network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_nav

        with pytest.raises(ValueError, match="场外基金净值获取失败"):
            get_fund_of_nav("000001")

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_date_filtering_start(self, mock_get_adapter):
        """开始日期过滤功能"""
        raw_df = _make_fund_nav_df(rows=15)

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_nav

        result = get_fund_of_nav("000001", start="2024-01-10")

        assert result["datetime"].min() >= pd.to_datetime("2024-01-10")

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_date_filtering_end(self, mock_get_adapter):
        """结束日期过滤功能"""
        raw_df = _make_fund_nav_df(rows=15)

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_nav

        result = get_fund_of_nav("000001", end="2024-01-10")

        assert result["datetime"].max() <= pd.to_datetime("2024-01-10")

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_no_date_filter(self, mock_get_adapter):
        """不指定日期时返回全部数据"""
        raw_df = _make_fund_nav_df(rows=10)

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_nav

        result = get_fund_of_nav("000001")

        assert len(result) == 10

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_empty_after_date_filter(self, mock_get_adapter):
        """日期过滤后为空时应记录警告"""
        raw_df = _make_fund_nav_df()
        raw_df = raw_df[raw_df["净值日期"] < pd.to_datetime("2023-01-01")]

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_nav

        result = get_fund_of_nav("000001", start="2024-01-01")

        assert result.empty

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_force_update_no_effect(self, mock_get_adapter):
        """force_update 参数暂无实现（无缓存机制）"""
        raw_df = _make_fund_nav_df()

        adapter_mock = MagicMock()
        adapter_mock.get_fund_of_nav.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_nav

        result = get_fund_of_nav("000001", force_update=True)

        assert isinstance(result, pd.DataFrame)
        assert not result.empty


class TestGetFundOfDailyList:
    """测试 get_fund_of_daily_list 函数"""

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """正常获取场外基金当日净值列表"""
        mock_df = pd.DataFrame(
            {
                "基金代码": ["000001", "000002"],
                "基金简称": ["华夏成长", "易基科翔"],
                "单位净值": [1.5, 2.0],
            }
        )

        adapter_mock = MagicMock()
        adapter_mock.get_fund_open_daily.return_value = mock_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_daily_list

        result = get_fund_of_daily_list()

        adapter_mock.get_fund_open_daily.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_adapter_raises(self, mock_get_adapter):
        """adapter 抛出异常时应向上传播"""
        adapter_mock = MagicMock()
        adapter_mock.get_fund_open_daily.side_effect = Exception("Network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_daily_list

        with pytest.raises(Exception, match="Network error"):
            get_fund_of_daily_list()


class TestGetFundOfInfo:
    """测试 get_fund_of_info 函数"""

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_normal_case(self, mock_get_adapter):
        """正常获取场外基金基本信息"""
        raw_df = _make_fund_info_df()

        adapter_mock = MagicMock()
        adapter_mock.get_fund_open_info.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_info

        result = get_fund_of_info("000001")

        adapter_mock.get_fund_open_info.assert_called_once_with(symbol="000001")
        assert isinstance(result, dict)
        assert result["name"] == "华夏成长混合"
        assert result["type"] == "混合型"

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_adapter_returns_empty(self, mock_get_adapter):
        """adapter 返回空数据时返回空字典"""
        adapter_mock = MagicMock()
        adapter_mock.get_fund_open_info.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_info

        result = get_fund_of_info("000001")

        assert isinstance(result, dict)
        assert result == {}

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_adapter_raises(self, mock_get_adapter):
        """adapter 抛出异常时返回空字典"""
        adapter_mock = MagicMock()
        adapter_mock.get_fund_open_info.side_effect = Exception("Network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_info

        result = get_fund_of_info("000001")

        assert isinstance(result, dict)
        assert result == {}

    @patch("jk2bt.data.market.fund_of.get_adapter")
    def test_partial_info(self, mock_get_adapter):
        """只有部分信息时只返回有的字段"""
        raw_df = pd.DataFrame(
            {
                "基金简称": ["华夏成长混合"],
            }
        )

        adapter_mock = MagicMock()
        adapter_mock.get_fund_open_info.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.fund_of import get_fund_of_info

        result = get_fund_of_info("000001")

        assert result["name"] == "华夏成长混合"
        assert "type" not in result
