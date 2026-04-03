"""
tests/unit/api/test_market.py
行情 API 单元测试（合并自 test_market_api.py、test_market_api_unit.py、test_market_api_enhanced.py）

测试覆盖：
1. 股票代码标准化（normalize_symbol、get_symbol_prefix）
2. 涨跌停价计算（calculate_limit_price）
3. 推导字段（pre_close、paused、high_limit、low_limit）
4. get_price 参数签名与返回结构
5. history / attribute_history / get_bars 参数签名
6. Mock 数据测试（避免网络依赖）
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
import sys
import os

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"),
)


# ---------------------------------------------------------------------------
# 股票代码工具函数测试（来自 test_market_api_unit.py）
# ---------------------------------------------------------------------------

class TestNormalizeSymbol:
    """股票代码标准化测试"""

    def test_sh_prefix(self):
        from jk2bt.api._internal.symbol_utils import normalize_symbol
        assert normalize_symbol("sh600000") == "600000"
        assert normalize_symbol("sh000001") == "000001"

    def test_sz_prefix(self):
        from jk2bt.api._internal.symbol_utils import normalize_symbol
        assert normalize_symbol("sz000001") == "000001"
        assert normalize_symbol("sz300750") == "300750"

    def test_xshg_suffix(self):
        from jk2bt.api._internal.symbol_utils import normalize_symbol
        assert normalize_symbol("600000.XSHG") == "600000"
        assert normalize_symbol("600519.XSHG") == "600519"

    def test_xshe_suffix(self):
        from jk2bt.api._internal.symbol_utils import normalize_symbol
        assert normalize_symbol("000001.XSHE") == "000001"
        assert normalize_symbol("300750.XSHE") == "300750"

    def test_pure_6_digit(self):
        from jk2bt.api._internal.symbol_utils import normalize_symbol
        assert normalize_symbol("600000") == "600000"
        assert normalize_symbol("000001") == "000001"


class TestGetSymbolPrefix:
    """股票代码前缀测试"""

    def test_sh_prefix_for_6(self):
        from jk2bt.api._internal.symbol_utils import get_symbol_prefix
        assert get_symbol_prefix("600000") == "sh"
        assert get_symbol_prefix("601318") == "sh"
        assert get_symbol_prefix("688981") == "sh"

    def test_sz_prefix_for_0(self):
        from jk2bt.api._internal.symbol_utils import get_symbol_prefix
        assert get_symbol_prefix("000001") == "sz"
        assert get_symbol_prefix("000858") == "sz"

    def test_sz_prefix_for_3(self):
        from jk2bt.api._internal.symbol_utils import get_symbol_prefix
        assert get_symbol_prefix("300750") == "sz"
        assert get_symbol_prefix("300001") == "sz"


class TestIsGemOrStar:
    """创业板/科创板判断测试"""

    def test_gem_code(self):
        from jk2bt.api._internal.symbol_utils import is_gem_or_star
        assert is_gem_or_star("300750") is True
        assert is_gem_or_star("300001") is True

    def test_star_code(self):
        from jk2bt.api._internal.symbol_utils import is_gem_or_star
        assert is_gem_or_star("688981") is True
        assert is_gem_or_star("688001") is True

    def test_mainboard_code(self):
        from jk2bt.api._internal.symbol_utils import is_gem_or_star
        assert is_gem_or_star("600000") is False
        assert is_gem_or_star("000001") is False
        assert is_gem_or_star("601318") is False


class TestCalculateLimitPrice:
    """涨跌停价计算测试"""

    def test_mainboard_up(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        assert calculate_limit_price(100.0, "600000", "up") == 110.0

    def test_mainboard_down(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        assert calculate_limit_price(100.0, "600000", "down") == 90.0

    def test_gem_up(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        assert calculate_limit_price(100.0, "300750", "up") == 120.0

    def test_gem_down(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        assert calculate_limit_price(100.0, "300750", "down") == 80.0

    def test_star_up(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        assert calculate_limit_price(100.0, "688981", "up") == 120.0

    def test_star_down(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        assert calculate_limit_price(100.0, "688981", "down") == 80.0

    def test_none_prev_close(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        assert calculate_limit_price(None, "600000", "up") is None

    def test_zero_prev_close(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        assert calculate_limit_price(0, "600000", "up") is None

    def test_negative_prev_close(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        assert calculate_limit_price(-10.0, "600000", "up") is None

    def test_rounding(self):
        from jk2bt.api._internal.symbol_utils import calculate_limit_price
        result = calculate_limit_price(10.123, "600000", "up")
        assert result == round(10.123 * 1.10, 2)


# ---------------------------------------------------------------------------
# get_price 返回结构测试（Mock，不依赖网络）
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_akshare_daily():
    """模拟 AkShare 日线数据"""
    dates = pd.date_range("2023-01-01", periods=10, freq="D")
    return pd.DataFrame({
        "日期": dates,
        "开盘": [100.0 + i for i in range(10)],
        "最高": [105.0 + i for i in range(10)],
        "最低": [95.0 + i for i in range(10)],
        "收盘": [102.0 + i for i in range(10)],
        "成交量": [1000000 + i * 10000 for i in range(10)],
        "成交额": [10000000.0 + i * 100000 for i in range(10)],
    })


class TestGetPriceReturnStructure:
    """get_price 返回结构测试（Mock）"""

    @patch("src.api.market.ak")
    def test_single_security_returns_dataframe(self, mock_ak, mock_akshare_daily):
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_daily
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-10")
        assert isinstance(result, pd.DataFrame)
        assert "datetime" in result.columns

    @patch("src.api.market.ak")
    def test_multiple_securities_panel_true(self, mock_ak, mock_akshare_daily):
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_daily
        from jk2bt.api.market import get_price
        result = get_price(["600519.XSHG", "000001.XSHE"], start_date="2023-01-01",
                           end_date="2023-01-10", panel=True)
        assert isinstance(result, dict)
        assert "600519.XSHG" in result
        assert "000001.XSHE" in result

    @patch("src.api.market.ak")
    def test_multiple_securities_panel_false(self, mock_ak, mock_akshare_daily):
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_daily
        from jk2bt.api.market import get_price
        result = get_price(["600519.XSHG", "000001.XSHE"], start_date="2023-01-01",
                           end_date="2023-01-10", panel=False)
        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    @patch("src.api.market.ak")
    def test_count_parameter(self, mock_ak, mock_akshare_daily):
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_daily
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", end_date="2023-01-10", count=5)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 5

    @patch("src.api.market.ak")
    def test_fields_parameter(self, mock_ak, mock_akshare_daily):
        mock_ak.stock_zh_a_hist.return_value = mock_akshare_daily
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-10",
                           fields=["open", "close"])
        assert isinstance(result, pd.DataFrame)
        assert "open" in result.columns
        assert "close" in result.columns
        assert "high" not in result.columns

    @patch("src.api.market.ak")
    def test_empty_data(self, mock_ak):
        mock_ak.stock_zh_a_hist.return_value = pd.DataFrame()
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-10")
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    @patch("src.api.market.ak")
    def test_none_data(self, mock_ak):
        mock_ak.stock_zh_a_hist.return_value = None
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-10")
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_empty_security_list(self):
        from jk2bt.api.market import get_price
        result = get_price([], start_date="2023-01-01", end_date="2023-01-10")
        assert isinstance(result, dict)
        assert len(result) == 0


# ---------------------------------------------------------------------------
# 高频字段测试（Mock）
# ---------------------------------------------------------------------------

class TestHighFrequencyFieldsWithMock:
    """高频字段 Mock 测试"""

    @pytest.fixture
    def mock_data_with_pause(self):
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        volumes = [1000000, 1100000, 1200000, 0, 1400000, 1500000, 0, 1700000, 1800000, 1900000]
        return pd.DataFrame({
            "日期": dates,
            "开盘": [100.0 + i for i in range(10)],
            "最高": [105.0 + i for i in range(10)],
            "最低": [95.0 + i for i in range(10)],
            "收盘": [102.0 + i for i in range(10)],
            "成交量": volumes,
            "成交额": [v * 10.0 for v in volumes],
        })

    @patch("src.api.market.ak")
    def test_paused_field_from_volume_zero(self, mock_ak, mock_data_with_pause):
        mock_ak.stock_zh_a_hist.return_value = mock_data_with_pause
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-10",
                           fields=["close", "volume", "paused"], skip_paused=False, fill_paused=False)
        assert "paused" in result.columns
        paused_rows = result[result["volume"] == 0]
        if not paused_rows.empty:
            assert (paused_rows["paused"] == 1).all()
        trading_rows = result[result["volume"] > 0]
        if not trading_rows.empty:
            assert (trading_rows["paused"] == 0).all()

    @patch("src.api.market.ak")
    def test_pre_close_is_previous_close(self, mock_ak, mock_data_with_pause):
        mock_ak.stock_zh_a_hist.return_value = mock_data_with_pause
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-10",
                           fields=["close", "pre_close"])
        assert "pre_close" in result.columns
        assert pd.isna(result.iloc[0]["pre_close"])
        assert result.iloc[1]["pre_close"] == result.iloc[0]["close"]

    @patch("src.api.market.ak")
    def test_mainboard_limit_ratio_10pct(self, mock_ak):
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        mock_ak.stock_zh_a_hist.return_value = pd.DataFrame({
            "日期": dates,
            "开盘": [10.0] * 5,
            "最高": [10.5] * 5,
            "最低": [9.5] * 5,
            "收盘": [10.0 + i * 0.1 for i in range(5)],
            "成交量": [1000000] * 5,
            "成交额": [10000000.0] * 5,
        })
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-05",
                           fields=["close", "pre_close", "high_limit", "low_limit", "paused"])
        for i in range(1, len(result)):
            if result.iloc[i]["paused"] == 0 and pd.notna(result.iloc[i]["pre_close"]):
                pre_close = result.iloc[i]["pre_close"]
                assert abs(result.iloc[i]["high_limit"] - round(pre_close * 1.10, 2)) < 0.01
                assert abs(result.iloc[i]["low_limit"] - round(pre_close * 0.90, 2)) < 0.01

    @patch("src.api.market.ak")
    def test_gem_limit_ratio_20pct(self, mock_ak):
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        mock_ak.stock_zh_a_hist.return_value = pd.DataFrame({
            "日期": dates,
            "开盘": [10.0] * 5,
            "最高": [10.5] * 5,
            "最低": [9.5] * 5,
            "收盘": [10.0 + i * 0.1 for i in range(5)],
            "成交量": [1000000] * 5,
            "成交额": [10000000.0] * 5,
        })
        from jk2bt.api.market import get_price
        result = get_price("300750.XSHE", start_date="2023-01-01", end_date="2023-01-05",
                           fields=["close", "pre_close", "high_limit", "low_limit", "paused"])
        for i in range(1, len(result)):
            if result.iloc[i]["paused"] == 0 and pd.notna(result.iloc[i]["pre_close"]):
                pre_close = result.iloc[i]["pre_close"]
                assert abs(result.iloc[i]["high_limit"] - round(pre_close * 1.20, 2)) < 0.01
                assert abs(result.iloc[i]["low_limit"] - round(pre_close * 0.80, 2)) < 0.01


# ---------------------------------------------------------------------------
# 代码格式兼容性测试（Mock）
# ---------------------------------------------------------------------------

class TestCodeFormatCompatibility:
    """代码格式兼容性测试"""

    @pytest.fixture
    def mock_data(self):
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        return pd.DataFrame({
            "日期": dates,
            "开盘": [100.0] * 5,
            "最高": [105.0] * 5,
            "最低": [95.0] * 5,
            "收盘": [102.0] * 5,
            "成交量": [1000000] * 5,
            "成交额": [10000000.0] * 5,
        })

    @patch("src.api.market.ak")
    def test_jq_format(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-05")
        assert isinstance(result, pd.DataFrame)
        assert mock_ak.stock_zh_a_hist.call_args[1]["symbol"] == "600519"

    @patch("src.api.market.ak")
    def test_sh_prefix(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_price
        result = get_price("sh600519", start_date="2023-01-01", end_date="2023-01-05")
        assert isinstance(result, pd.DataFrame)
        assert mock_ak.stock_zh_a_hist.call_args[1]["symbol"] == "600519"

    @patch("src.api.market.ak")
    def test_pure_code(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_price
        result = get_price("600519", start_date="2023-01-01", end_date="2023-01-05")
        assert isinstance(result, pd.DataFrame)
        assert mock_ak.stock_zh_a_hist.call_args[1]["symbol"] == "600519"

    @patch("src.api.market.ak")
    def test_sz_format(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_price
        result = get_price("000001.XSHE", start_date="2023-01-01", end_date="2023-01-05")
        assert isinstance(result, pd.DataFrame)


# ---------------------------------------------------------------------------
# history / attribute_history / get_bars 返回结构测试（Mock）
# ---------------------------------------------------------------------------

class TestHistoryWithMock:
    """history Mock 测试"""

    @pytest.fixture
    def mock_data(self):
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        return pd.DataFrame({
            "日期": dates,
            "开盘": [100.0 + i for i in range(30)],
            "最高": [105.0 + i for i in range(30)],
            "最低": [95.0 + i for i in range(30)],
            "收盘": [102.0 + i for i in range(30)],
            "成交量": [1000000 + i * 10000 for i in range(30)],
            "成交额": [10000000.0 + i * 100000 for i in range(30)],
        })

    @patch("src.api.market.ak")
    def test_history_returns_dataframe(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import history
        result = history(count=10, unit="1d", field="close",
                         security_list=["600519.XSHG", "000001.XSHE"])
        assert isinstance(result, pd.DataFrame)
        assert "600519.XSHG" in result.columns
        assert "000001.XSHE" in result.columns

    @patch("src.api.market.ak")
    def test_history_df_false_returns_dict(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import history
        result = history(count=10, unit="1d", field="close",
                         security_list=["600519.XSHG"], df=False)
        assert isinstance(result, dict)
        assert "600519.XSHG" in result
        assert isinstance(result["600519.XSHG"], np.ndarray)

    def test_history_empty_security_list(self):
        from jk2bt.api.market import history
        result = history(count=10, unit="1d", field="close", security_list=None)
        assert isinstance(result, pd.DataFrame)
        assert result.empty


class TestAttributeHistoryWithMock:
    """attribute_history Mock 测试"""

    @pytest.fixture
    def mock_data(self):
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        return pd.DataFrame({
            "日期": dates,
            "开盘": [100.0 + i for i in range(30)],
            "最高": [105.0 + i for i in range(30)],
            "最低": [95.0 + i for i in range(30)],
            "收盘": [102.0 + i for i in range(30)],
            "成交量": [1000000 + i * 10000 for i in range(30)],
            "成交额": [10000000.0 + i * 100000 for i in range(30)],
        })

    @patch("src.api.market.ak")
    def test_attribute_history_returns_dataframe(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import attribute_history
        result = attribute_history("600519.XSHG", count=10, unit="1d",
                                   fields=["open", "close", "high", "low"])
        assert isinstance(result, pd.DataFrame)
        for col in ["open", "close", "high", "low"]:
            assert col in result.columns

    @patch("src.api.market.ak")
    def test_attribute_history_df_false(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import attribute_history
        result = attribute_history("600519.XSHG", count=10, unit="1d",
                                   fields=["open", "close"], df=False)
        assert isinstance(result, dict)
        assert "open" in result
        assert "close" in result
        assert isinstance(result["open"], np.ndarray)


class TestGetBarsWithMock:
    """get_bars Mock 测试"""

    @pytest.fixture
    def mock_data(self):
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        return pd.DataFrame({
            "日期": dates,
            "开盘": [100.0 + i for i in range(30)],
            "最高": [105.0 + i for i in range(30)],
            "最低": [95.0 + i for i in range(30)],
            "收盘": [102.0 + i for i in range(30)],
            "成交量": [1000000 + i * 10000 for i in range(30)],
            "成交额": [10000000.0 + i * 100000 for i in range(30)],
        })

    @patch("src.api.market.ak")
    def test_get_bars_daily(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_bars
        result = get_bars("600519.XSHG", count=10, unit="1d")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 10
        assert "datetime" in result.columns

    @patch("src.api.market.ak")
    def test_get_bars_multiple_securities(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_bars
        result = get_bars(["600519.XSHG", "000001.XSHE"], count=10, unit="1d")
        assert isinstance(result, dict)
        assert "600519.XSHG" in result
        assert "000001.XSHE" in result

    @patch("src.api.market.ak")
    def test_get_bars_fields(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_bars
        result = get_bars("600519.XSHG", count=10, unit="1d", fields=["open", "close"])
        assert isinstance(result, pd.DataFrame)
        assert "open" in result.columns
        assert "close" in result.columns


# ---------------------------------------------------------------------------
# 数据类型验证（Mock）
# ---------------------------------------------------------------------------

class TestDataTypes:
    """数据类型测试"""

    @pytest.fixture
    def mock_data(self):
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        return pd.DataFrame({
            "日期": dates,
            "开盘": [100.0 + i for i in range(5)],
            "最高": [105.0 + i for i in range(5)],
            "最低": [95.0 + i for i in range(5)],
            "收盘": [102.0 + i for i in range(5)],
            "成交量": [1000000 + i * 10000 for i in range(5)],
            "成交额": [10000000.0 + i * 100000 for i in range(5)],
        })

    @patch("src.api.market.ak")
    def test_datetime_column_is_datetime_type(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-05")
        assert "datetime" in result.columns
        assert pd.api.types.is_datetime64_any_dtype(result["datetime"])

    @patch("src.api.market.ak")
    def test_numeric_fields_are_numeric(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-05",
                           fields=["open", "close", "volume"])
        for col in ["open", "close", "volume"]:
            assert pd.api.types.is_numeric_dtype(result[col])

    @patch("src.api.market.ak")
    def test_paused_field_is_binary(self, mock_ak, mock_data):
        mock_ak.stock_zh_a_hist.return_value = mock_data
        from jk2bt.api.market import get_price
        result = get_price("600519.XSHG", start_date="2023-01-01", end_date="2023-01-05",
                           fields=["paused"])
        assert "paused" in result.columns
        assert result["paused"].isin([0, 1]).all()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
