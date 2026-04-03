"""
test_market_api_enhanced.py
行情 API 兼容层增强测试

测试覆盖：
1. 参数签名验证
2. 返回结构验证
3. 边界条件测试
4. 异常处理测试
5. 数据类型验证
6. 高频字段验证
7. Mock 数据测试（避免网络依赖）
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src",
    ),
)


class TestGetPriceWithMock:
    """get_price 使用 Mock 测试"""

    @pytest.fixture
    def mock_akshare_data(self):
        """模拟 AkShare 返回数据"""
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        data = pd.DataFrame(
            {
                "日期": dates,
                "开盘": [100.0 + i for i in range(10)],
                "最高": [105.0 + i for i in range(10)],
                "最低": [95.0 + i for i in range(10)],
                "收盘": [102.0 + i for i in range(10)],
                "成交量": [1000000 + i * 10000 for i in range(10)],
                "成交额": [10000000.0 + i * 100000 for i in range(10)],
            }
        )
        return data

    @patch("jk2bt.api.market.ak")
    def test_get_price_single_security(self, mock_ak, mock_akshare_data):
        """单标的基础测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)
        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "close" in result.columns
        assert "volume" in result.columns

    @patch("jk2bt.api.market.ak")
    def test_get_price_count_parameter(self, mock_ak, mock_akshare_data):
        """count 参数测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            end_date="2023-01-10",
            count=5,
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 5

    @patch("jk2bt.api.market.ak")
    def test_get_price_fields_parameter(self, mock_ak, mock_akshare_data):
        """fields 参数测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["open", "close"],
        )

        assert isinstance(result, pd.DataFrame)
        assert "open" in result.columns
        assert "close" in result.columns
        assert "high" not in result.columns

    @patch("jk2bt.api.market.ak")
    def test_get_price_multiple_securities_panel_true(self, mock_ak, mock_akshare_data):
        """多标的 panel=True 测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2023-01-01",
            end_date="2023-01-10",
            panel=True,
        )

        assert isinstance(result, dict)
        assert "600519.XSHG" in result
        assert "000001.XSHE" in result
        assert isinstance(result["600519.XSHG"], pd.DataFrame)

    @patch("jk2bt.api.market.ak")
    def test_get_price_multiple_securities_panel_false(
        self, mock_ak, mock_akshare_data
    ):
        """多标的 panel=False 测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security=["600519.XSHG", "000001.XSHE"],
            start_date="2023-01-01",
            end_date="2023-01-10",
            panel=False,
        )

        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns
        assert result["code"].nunique() == 2

    @patch("jk2bt.api.market.ak")
    def test_get_price_frequency_minute(self, mock_ak):
        """分钟线测试"""
        times = pd.date_range("2023-01-01 09:30", periods=10, freq="1min")
        mock_data = pd.DataFrame(
            {
                "时间": times.strftime("%Y-%m-%d %H:%M:%S").tolist(),
                "开盘": [100.0 + i for i in range(10)],
                "最高": [105.0 + i for i in range(10)],
                "最低": [95.0 + i for i in range(10)],
                "收盘": [102.0 + i for i in range(10)],
                "成交量": [1000000 + i * 10000 for i in range(10)],
                "成交额": [10000000.0 + i * 100000 for i in range(10)],
            }
        )
        mock_ak.stock_zh_a_minute.return_value = mock_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-01",
            frequency="1m",
        )

        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "datetime" in result.columns


class TestHighFrequencyFieldsWithMock:
    """高频字段 Mock 测试"""

    @pytest.fixture
    def mock_akshare_data_with_volume(self):
        """模拟包含成交量的数据"""
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        data = pd.DataFrame(
            {
                "日期": dates,
                "开盘": [
                    100.0,
                    101.0,
                    102.0,
                    103.0,
                    104.0,
                    105.0,
                    106.0,
                    107.0,
                    108.0,
                    109.0,
                ],
                "最高": [
                    105.0,
                    106.0,
                    107.0,
                    108.0,
                    109.0,
                    110.0,
                    111.0,
                    112.0,
                    113.0,
                    114.0,
                ],
                "最低": [
                    95.0,
                    96.0,
                    97.0,
                    98.0,
                    99.0,
                    100.0,
                    101.0,
                    102.0,
                    103.0,
                    104.0,
                ],
                "收盘": [
                    102.0,
                    103.0,
                    104.0,
                    105.0,
                    106.0,
                    107.0,
                    108.0,
                    109.0,
                    110.0,
                    111.0,
                ],
                "成交量": [
                    1000000,
                    1100000,
                    1200000,
                    0,
                    1400000,
                    1500000,
                    0,
                    1700000,
                    1800000,
                    1900000,
                ],
                "成交额": [
                    10000000.0,
                    11000000.0,
                    12000000.0,
                    0,
                    14000000.0,
                    15000000.0,
                    0,
                    17000000.0,
                    18000000.0,
                    19000000.0,
                ],
            }
        )
        return data

    @patch("jk2bt.api.market.ak")
    def test_paused_field_calculation(self, mock_ak, mock_akshare_data_with_volume):
        """paused 字段计算测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data_with_volume

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close", "volume", "paused", "pre_close"],
            skip_paused=False,
            fill_paused=False,
        )

        assert "paused" in result.columns
        paused_rows = result[result["volume"] == 0]
        if not paused_rows.empty:
            assert (paused_rows["paused"] == 1).all()
        trading_rows = result[result["volume"] > 0]
        if not trading_rows.empty:
            assert (trading_rows["paused"] == 0).all()

    @patch("jk2bt.api.market.ak")
    def test_pre_close_field_calculation(self, mock_ak, mock_akshare_data_with_volume):
        """pre_close 字段计算测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data_with_volume

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close", "pre_close"],
        )

        assert "pre_close" in result.columns
        assert pd.isna(result.iloc[0]["pre_close"])
        assert result.iloc[1]["pre_close"] == result.iloc[0]["close"]

    @patch("jk2bt.api.market.ak")
    def test_high_limit_calculation(self, mock_ak, mock_akshare_data_with_volume):
        """涨停价计算测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data_with_volume

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close", "pre_close", "high_limit", "paused"],
            skip_paused=False,
        )

        assert "high_limit" in result.columns
        for i in range(1, len(result)):
            if (
                "paused" in result.columns
                and result.iloc[i].get("paused", 0) == 0
                and pd.notna(result.iloc[i]["pre_close"])
            ):
                pre_close = result.iloc[i]["pre_close"]
                expected_high_limit = round(pre_close * 1.10, 2)
                assert abs(result.iloc[i]["high_limit"] - expected_high_limit) < 0.01

    @patch("jk2bt.api.market.ak")
    def test_low_limit_calculation(self, mock_ak, mock_akshare_data_with_volume):
        """跌停价计算测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data_with_volume

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close", "pre_close", "low_limit", "paused"],
            skip_paused=False,
        )

        assert "low_limit" in result.columns
        for i in range(1, len(result)):
            if (
                "paused" in result.columns
                and result.iloc[i].get("paused", 0) == 0
                and pd.notna(result.iloc[i]["pre_close"])
            ):
                pre_close = result.iloc[i]["pre_close"]
                expected_low_limit = round(pre_close * 0.90, 2)
                assert abs(result.iloc[i]["low_limit"] - expected_low_limit) < 0.01


class TestHistoryWithMock:
    """history Mock 测试"""

    @pytest.fixture
    def mock_akshare_data(self):
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        data = pd.DataFrame(
            {
                "日期": dates,
                "开盘": [100.0 + i for i in range(30)],
                "最高": [105.0 + i for i in range(30)],
                "最低": [95.0 + i for i in range(30)],
                "收盘": [102.0 + i for i in range(30)],
                "成交量": [1000000 + i * 10000 for i in range(30)],
                "成交额": [10000000.0 + i * 100000 for i in range(30)],
            }
        )
        return data

    @patch("jk2bt.api.market.ak")
    def test_history_basic(self, mock_ak, mock_akshare_data):
        """history 基础测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG", "000001.XSHE"],
        )

        assert isinstance(result, pd.DataFrame)
        assert "600519.XSHG" in result.columns
        assert "000001.XSHE" in result.columns

    @patch("jk2bt.api.market.ak")
    def test_history_df_false(self, mock_ak, mock_akshare_data):
        """history df=False 测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG", "000001.XSHE"],
            df=False,
        )

        assert isinstance(result, dict)
        assert "600519.XSHG" in result
        assert "000001.XSHE" in result
        assert isinstance(result["600519.XSHG"], np.ndarray)

    @patch("jk2bt.api.market.ak")
    def test_history_single_security(self, mock_ak, mock_akshare_data):
        """history 单标测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG"],
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 1
        assert "600519.XSHG" in result.columns


class TestAttributeHistoryWithMock:
    """attribute_history Mock 测试"""

    @pytest.fixture
    def mock_akshare_data(self):
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        data = pd.DataFrame(
            {
                "日期": dates,
                "开盘": [100.0 + i for i in range(30)],
                "最高": [105.0 + i for i in range(30)],
                "最低": [95.0 + i for i in range(30)],
                "收盘": [102.0 + i for i in range(30)],
                "成交量": [1000000 + i * 10000 for i in range(30)],
                "成交额": [10000000.0 + i * 100000 for i in range(30)],
            }
        )
        return data

    @patch("jk2bt.api.market.ak")
    def test_attribute_history_basic(self, mock_ak, mock_akshare_data):
        """attribute_history 基础测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            unit="1d",
            fields=["open", "close", "high", "low"],
        )

        assert isinstance(result, pd.DataFrame)
        assert "open" in result.columns
        assert "close" in result.columns
        assert "high" in result.columns
        assert "low" in result.columns

    @patch("jk2bt.api.market.ak")
    def test_attribute_history_df_false(self, mock_ak, mock_akshare_data):
        """attribute_history df=False 测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            unit="1d",
            fields=["open", "close"],
            df=False,
        )

        assert isinstance(result, dict)
        assert "open" in result
        assert "close" in result
        assert isinstance(result["open"], np.ndarray)

    @patch("jk2bt.api.market.ak")
    def test_attribute_history_default_fields(self, mock_ak, mock_akshare_data):
        """attribute_history 默认字段测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            unit="1d",
        )

        assert isinstance(result, pd.DataFrame)
        assert "open" in result.columns
        assert "close" in result.columns
        assert "high" in result.columns
        assert "low" in result.columns
        assert "volume" in result.columns
        assert "money" in result.columns


class TestGetBarsWithMock:
    """get_bars Mock 测试"""

    @pytest.fixture
    def mock_akshare_data(self):
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        data = pd.DataFrame(
            {
                "日期": dates,
                "开盘": [100.0 + i for i in range(30)],
                "最高": [105.0 + i for i in range(30)],
                "最低": [95.0 + i for i in range(30)],
                "收盘": [102.0 + i for i in range(30)],
                "成交量": [1000000 + i * 10000 for i in range(30)],
                "成交额": [10000000.0 + i * 100000 for i in range(30)],
            }
        )
        return data

    @patch("jk2bt.api.market.ak")
    def test_get_bars_daily(self, mock_ak, mock_akshare_data):
        """get_bars 日线测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_bars

        result = get_bars(
            security="600519.XSHG",
            count=10,
            unit="1d",
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10
        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "close" in result.columns

    @patch("jk2bt.api.market.ak")
    def test_get_bars_fields(self, mock_ak, mock_akshare_data):
        """get_bars fields 参数测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_bars

        result = get_bars(
            security="600519.XSHG",
            count=10,
            unit="1d",
            fields=["open", "close"],
        )

        assert isinstance(result, pd.DataFrame)
        assert "open" in result.columns
        assert "close" in result.columns

    @patch("jk2bt.api.market.ak")
    def test_get_bars_multiple_securities(self, mock_ak, mock_akshare_data):
        """get_bars 多标测试"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_bars

        result = get_bars(
            security=["600519.XSHG", "000001.XSHE"],
            count=10,
            unit="1d",
        )

        assert isinstance(result, dict)
        assert "600519.XSHG" in result
        assert "000001.XSHE" in result


class TestEdgeCases:
    """边界条件测试"""

    @patch("jk2bt.api.market.ak")
    def test_empty_data(self, mock_ak):
        """空数据测试"""
        mock_ak.stock_zh_a_hist.return_value = pd.DataFrame()

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    @patch("jk2bt.api.market.ak")
    def test_none_data(self, mock_ak):
        """None 数据测试"""
        mock_ak.stock_zh_a_hist.return_value = None

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_history_empty_security_list(self):
        """history 空股票列表测试"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=None,
        )

        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_history_empty_security_list_df_false(self):
        """history 空股票列表 df=False 测试"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=None,
            df=False,
        )

        assert isinstance(result, dict)
        assert len(result) == 0


class TestCodeFormatCompatibility:
    """代码格式兼容性测试"""

    @pytest.fixture
    def mock_akshare_data(self):
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        return pd.DataFrame(
            {
                "日期": dates,
                "开盘": [100.0 + i for i in range(10)],
                "最高": [105.0 + i for i in range(10)],
                "最低": [95.0 + i for i in range(10)],
                "收盘": [102.0 + i for i in range(10)],
                "成交量": [1000000 + i * 10000 for i in range(10)],
                "成交额": [10000000.0 + i * 100000 for i in range(10)],
            }
        )

    @patch("jk2bt.api.market.ak")
    def test_jq_format(self, mock_ak, mock_akshare_data):
        """聚宽格式 600519.XSHG"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)
        mock_ak.stock_zh_a_hist.assert_called_once()
        assert mock_ak.stock_zh_a_hist.call_args[1]["symbol"] == "600519"

    @patch("jk2bt.api.market.ak")
    def test_sh_prefix(self, mock_ak, mock_akshare_data):
        """sh 前缀格式"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="sh600519",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)
        assert mock_ak.stock_zh_a_hist.call_args[1]["symbol"] == "600519"

    @patch("jk2bt.api.market.ak")
    def test_pure_code(self, mock_ak, mock_akshare_data):
        """纯数字格式"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)
        assert mock_ak.stock_zh_a_hist.call_args[1]["symbol"] == "600519"

    @patch("jk2bt.api.market.ak")
    def test_sz_format(self, mock_ak, mock_akshare_data):
        """深市格式"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="000001.XSHE",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert isinstance(result, pd.DataFrame)
        assert mock_ak.stock_zh_a_hist.call_args[1]["symbol"] == "000001"


class TestLimitPriceCalculationWithMock:
    """涨跌停价计算测试"""

    @pytest.fixture
    def mock_mainboard_data(self):
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        return pd.DataFrame(
            {
                "日期": dates,
                "开盘": [10.0] * 10,
                "最高": [10.5] * 10,
                "最低": [9.5] * 10,
                "收盘": [10.0 + i * 0.1 for i in range(10)],
                "成交量": [1000000] * 10,
                "成交额": [10000000.0] * 10,
            }
        )

    @pytest.fixture
    def mock_gem_data(self):
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        return pd.DataFrame(
            {
                "日期": dates,
                "开盘": [10.0] * 10,
                "最高": [10.5] * 10,
                "最低": [9.5] * 10,
                "收盘": [10.0 + i * 0.1 for i in range(10)],
                "成交量": [1000000] * 10,
                "成交额": [10000000.0] * 10,
            }
        )

    @patch("jk2bt.api.market.ak")
    def test_mainboard_limit_ratio(self, mock_ak, mock_mainboard_data):
        """主板涨跌停比例 10%"""
        mock_ak.stock_zh_a_hist.return_value = mock_mainboard_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close", "pre_close", "high_limit", "low_limit", "paused"],
        )

        for i in range(1, len(result)):
            if result.iloc[i]["paused"] == 0 and pd.notna(result.iloc[i]["pre_close"]):
                pre_close = result.iloc[i]["pre_close"]
                expected_high = round(pre_close * 1.10, 2)
                expected_low = round(pre_close * 0.90, 2)
                assert abs(result.iloc[i]["high_limit"] - expected_high) < 0.01
                assert abs(result.iloc[i]["low_limit"] - expected_low) < 0.01

    @patch("jk2bt.api.market.ak")
    def test_gem_limit_ratio(self, mock_ak, mock_gem_data):
        """创业板涨跌停比例 20%"""
        mock_ak.stock_zh_a_hist.return_value = mock_gem_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="300750.XSHE",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close", "pre_close", "high_limit", "low_limit", "paused"],
        )

        for i in range(1, len(result)):
            if result.iloc[i]["paused"] == 0 and pd.notna(result.iloc[i]["pre_close"]):
                pre_close = result.iloc[i]["pre_close"]
                expected_high = round(pre_close * 1.20, 2)
                expected_low = round(pre_close * 0.80, 2)
                assert abs(result.iloc[i]["high_limit"] - expected_high) < 0.01
                assert abs(result.iloc[i]["low_limit"] - expected_low) < 0.01


class TestParameterValidation:
    """参数验证测试"""

    @patch("jk2bt.api.market.ak")
    def test_count_greater_than_data_length(self, mock_ak):
        """count 大于数据长度"""
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        mock_data = pd.DataFrame(
            {
                "日期": dates,
                "开盘": [100.0] * 5,
                "最高": [105.0] * 5,
                "最低": [95.0] * 5,
                "收盘": [102.0] * 5,
                "成交量": [1000000] * 5,
                "成交额": [10000000.0] * 5,
            }
        )
        mock_ak.stock_zh_a_hist.return_value = mock_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            end_date="2023-01-10",
            count=100,
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 100

    @patch("jk2bt.api.market.ak")
    def test_fields_not_exist(self, mock_ak):
        """不存在的字段"""
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        mock_data = pd.DataFrame(
            {
                "日期": dates,
                "开盘": [100.0] * 5,
                "收盘": [102.0] * 5,
            }
        )
        mock_ak.stock_zh_a_hist.return_value = mock_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["close", "nonexistent_field"],
        )

        assert isinstance(result, pd.DataFrame)
        assert "close" in result.columns

    @patch("jk2bt.api.market.ak")
    def test_invalid_frequency(self, mock_ak):
        """无效频率"""
        mock_ak.stock_zh_a_hist.side_effect = ValueError("Invalid frequency")

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            frequency="invalid",
        )

        assert isinstance(result, pd.DataFrame)
        assert result.empty


class TestDataTypes:
    """数据类型测试"""

    @pytest.fixture
    def mock_akshare_data(self):
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        return pd.DataFrame(
            {
                "日期": dates,
                "开盘": [100.0 + i for i in range(10)],
                "最高": [105.0 + i for i in range(10)],
                "最低": [95.0 + i for i in range(10)],
                "收盘": [102.0 + i for i in range(10)],
                "成交量": [1000000 + i * 10000 for i in range(10)],
                "成交额": [10000000.0 + i * 100000 for i in range(10)],
            }
        )

    @patch("jk2bt.api.market.ak")
    def test_datetime_type(self, mock_ak, mock_akshare_data):
        """datetime 列类型"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
        )

        assert "datetime" in result.columns
        assert pd.api.types.is_datetime64_any_dtype(result["datetime"])

    @patch("jk2bt.api.market.ak")
    def test_numeric_fields_type(self, mock_ak, mock_akshare_data):
        """数值字段类型"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["open", "close", "volume"],
        )

        for col in ["open", "close", "volume"]:
            assert pd.api.types.is_numeric_dtype(result[col])

    @patch("jk2bt.api.market.ak")
    def test_paused_field_type(self, mock_ak, mock_akshare_data):
        """paused 字段类型"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["paused"],
        )

        assert "paused" in result.columns
        assert result["paused"].isin([0, 1]).all()


class TestSkipAndFillPaused:
    """skip_paused 和 fill_paused 参数测试"""

    @pytest.fixture
    def mock_data_with_pause(self):
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        return pd.DataFrame(
            {
                "日期": dates,
                "开盘": [
                    100.0,
                    101.0,
                    102.0,
                    103.0,
                    104.0,
                    105.0,
                    106.0,
                    107.0,
                    108.0,
                    109.0,
                ],
                "最高": [
                    105.0,
                    106.0,
                    107.0,
                    108.0,
                    109.0,
                    110.0,
                    111.0,
                    112.0,
                    113.0,
                    114.0,
                ],
                "最低": [
                    95.0,
                    96.0,
                    97.0,
                    98.0,
                    99.0,
                    100.0,
                    101.0,
                    102.0,
                    103.0,
                    104.0,
                ],
                "收盘": [
                    102.0,
                    103.0,
                    104.0,
                    105.0,
                    106.0,
                    107.0,
                    108.0,
                    109.0,
                    110.0,
                    111.0,
                ],
                "成交量": [
                    1000000,
                    1100000,
                    0,
                    1300000,
                    1400000,
                    0,
                    1600000,
                    1700000,
                    1800000,
                    1900000,
                ],
                "成交额": [
                    10000000.0,
                    11000000.0,
                    0,
                    13000000.0,
                    14000000.0,
                    0,
                    16000000.0,
                    17000000.0,
                    18000000.0,
                    19000000.0,
                ],
            }
        )

    @patch("jk2bt.api.market.ak")
    def test_skip_paused_true(self, mock_ak, mock_data_with_pause):
        """skip_paused=True 跳过停牌"""
        mock_ak.stock_zh_a_hist.return_value = mock_data_with_pause

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            skip_paused=True,
        )

        assert (result["paused"] == 0).all()

    @patch("jk2bt.api.market.ak")
    def test_skip_paused_false(self, mock_ak, mock_data_with_pause):
        """skip_paused=False 包含停牌"""
        mock_ak.stock_zh_a_hist.return_value = mock_data_with_pause

        from jk2bt.api.market import get_price

        result = get_price(
            security="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            skip_paused=False,
        )

        assert len(result) == 10


class TestIntegrationWithBacktraderBaseStrategy:
    """与 backtrader_base_strategy 集成测试"""

    @pytest.fixture
    def mock_akshare_data(self):
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        return pd.DataFrame(
            {
                "日期": dates,
                "开盘": [100.0 + i for i in range(10)],
                "最高": [105.0 + i for i in range(10)],
                "最低": [95.0 + i for i in range(10)],
                "收盘": [102.0 + i for i in range(10)],
                "成交量": [1000000 + i * 10000 for i in range(10)],
                "成交额": [10000000.0 + i * 100000 for i in range(10)],
            }
        )

    @patch("jk2bt.api.market.ak")
    def test_get_price_jq_unified(self, mock_ak, mock_akshare_data):
        """get_price_jq 使用统一接口"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.core.strategy_base import get_price_jq

        result = get_price_jq(
            symbols="600519.XSHG",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["open", "close"],
        )

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.api.market.ak")
    def test_history_unified(self, mock_ak, mock_akshare_data):
        """history 使用统一接口"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.core.strategy_base import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["600519.XSHG"],
        )

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.api.market.ak")
    def test_attribute_history_unified(self, mock_ak, mock_akshare_data):
        """attribute_history 使用统一接口"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.core.strategy_base import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=10,
            unit="1d",
            fields=["open", "close"],
        )

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.api.market.ak")
    def test_get_bars_jq_unified(self, mock_ak, mock_akshare_data):
        """get_bars_jq 使用统一接口"""
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_data

        from jk2bt.core.strategy_base import get_bars_jq

        result = get_bars_jq(
            security="600519.XSHG",
            count=10,
            unit="1d",
        )

        assert isinstance(result, pd.DataFrame)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
