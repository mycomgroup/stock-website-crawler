"""
test_date_utils.py
日期工具模块测试
"""

import pytest
import pandas as pd
from datetime import datetime
from jk2bt.utils.date_utils import (
    find_date_column,
    is_trade_date,
    get_previous_trade_date,
    get_next_trade_date,
    count_trade_days_between,
    parse_date,
    filter_by_date_range,
    standardize_datetime,
    parse_ratio,
    parse_num,
    parse_int,
)


class TestFindDateColumn:
    """测试日期列查找"""

    def test_market_date_column(self):
        """测试市场数据日期列检测"""
        df = pd.DataFrame({"日期": [1, 2, 3]})
        assert find_date_column(df, "market") == "日期"

    def test_financial_date_column(self):
        """测试财务数据日期列检测"""
        df = pd.DataFrame({"报告期": [1, 2, 3]})
        assert find_date_column(df, "financial") == "报告期"

    def test_english_date_column(self):
        """测试英文日期列"""
        df = pd.DataFrame({"date": [1, 2, 3]})
        assert find_date_column(df, "market") == "date"

    def test_no_date_column(self):
        """测试无日期列"""
        df = pd.DataFrame({"value": [1, 2, 3]})
        assert find_date_column(df, "market") is None


class TestParseDate:
    """测试日期解析"""

    def test_parse_ymd_format(self):
        """测试 YYYY-MM-DD 格式"""
        assert parse_date("2023-01-15") == "2023-01-15"

    def test_parse_yyyymmdd_format(self):
        """测试 YYYYMMDD 格式"""
        assert parse_date("20230115") == "2023-01-15"

    def test_parse_slash_format(self):
        """测试斜杠分隔格式"""
        assert parse_date("2023/01/15") == "2023-01-15"

    def test_parse_chinese_format(self):
        """测试中文年月格式"""
        assert parse_date("2023年01月") == "2023-01-01"

    def test_parse_chinese_full_format(self):
        """测试中文完整日期格式"""
        assert parse_date("2023年01月15日") == "2023-01-15"

    def test_parse_as_datetime(self):
        """测试返回 datetime 对象"""
        result = parse_date("2023-01-15", as_datetime=True)
        assert isinstance(result, datetime)

    def test_parse_invalid_returns_none(self):
        """测试无效日期返回 None"""
        assert parse_date("invalid") is None
        assert parse_date(None) is None
        assert parse_date("") is None

    def test_parse_na_returns_none(self):
        """测试 NA 值返回 None"""
        assert parse_date(pd.NA) is None


class TestFilterByDateRange:
    """测试日期范围过滤"""

    def test_filter_no_bounds(self):
        """测试无边界时返回原数据"""
        df = pd.DataFrame({"datetime": pd.date_range("2023-01-01", periods=5)})
        result = filter_by_date_range(df)
        assert len(result) == 5

    def test_filter_start_only(self):
        """测试只有起始日期"""
        df = pd.DataFrame({"datetime": pd.date_range("2023-01-01", periods=5)})
        result = filter_by_date_range(df, start_date="2023-01-03")
        assert len(result) == 3

    def test_filter_end_only(self):
        """测试只有结束日期"""
        df = pd.DataFrame({"datetime": pd.date_range("2023-01-01", periods=5)})
        result = filter_by_date_range(df, end_date="2023-01-03")
        assert len(result) == 3

    def test_filter_both_bounds(self):
        """测试同时有起止日期"""
        df = pd.DataFrame({"datetime": pd.date_range("2023-01-01", periods=5)})
        result = filter_by_date_range(
            df, start_date="2023-01-02", end_date="2023-01-04"
        )
        assert len(result) == 3

    def test_filter_no_datetime_column(self):
        """测试无日期列"""
        df = pd.DataFrame({"value": [1, 2, 3]})
        result = filter_by_date_range(df, start_date="2023-01-01")
        assert len(result) == 3


class TestStandardizeDatetime:
    """测试日期列标准化"""

    def test_standardize_basic(self):
        """测试基本标准化"""
        df = pd.DataFrame(
            {
                "datetime": ["2023-01-03", "2023-01-01", "2023-01-02"],
            }
        )
        result = standardize_datetime(df)
        assert result["datetime"].iloc[0] == pd.Timestamp("2023-01-01")

    def test_standardize_no_datetime_column(self):
        """测试无日期列"""
        df = pd.DataFrame({"value": [1, 2, 3]})
        result = standardize_datetime(df)
        assert result.equals(df)


class TestParseRatio:
    """测试百分比解析"""

    def test_parse_percent_string(self):
        """测试百分比字符串"""
        assert parse_ratio("50%") == 0.5

    def test_parse_decimal_string(self):
        """测试小数格式"""
        assert parse_ratio("0.5") == 0.5

    def test_parse_small_percent(self):
        """测试小于1的百分比"""
        assert parse_ratio("5%") == 0.05

    def test_parse_none_returns_none(self):
        """测试 None 返回 None"""
        assert parse_ratio(None) is None

    def test_parse_empty_returns_none(self):
        """测试空字符串返回 None"""
        assert parse_ratio("") is None
        assert parse_ratio("-") is None


class TestParseNum:
    """测试数值解析"""

    def test_parse_basic(self):
        """测试基本解析"""
        assert parse_num("123.45") == 123.45
        assert parse_num(123.45) == 123.45

    def test_parse_with_comma(self):
        """测试带逗号"""
        assert parse_num("1,234.56") == 1234.56

    def test_parse_percent(self):
        """测试百分比"""
        assert parse_num("50%") == 0.5

    def test_parse_none_returns_none(self):
        """测试 None 返回 None"""
        assert parse_num(None) is None
        assert parse_num("") is None
        assert parse_num("-") is None


class TestParseInt:
    """测试整数解析"""

    def test_parse_basic(self):
        """测试基本解析"""
        assert parse_int("123") == 123
        assert parse_int(123) == 123
        assert parse_int(123.7) == 123

    def test_parse_with_comma(self):
        """测试带逗号"""
        assert parse_int("1,234") == 1234

    def test_parse_none_returns_none(self):
        """测试 None 返回 None"""
        assert parse_int(None) is None
        assert parse_int("") is None
        assert parse_int("-") is None


class TestTradeDateFunctions:
    """测试交易日相关函数（使用 mock）"""

    def test_is_trade_date_mock(self, mocker):
        """测试交易日判断（mock）"""
        mocker.patch(
            "jk2bt.utils.date_utils.get_all_trade_days",
            return_value=pd.DatetimeIndex(["2023-01-03"]),
        )
        assert is_trade_date("2023-01-03") is True
        assert is_trade_date("2023-01-01") is False

    def test_get_previous_trade_date_mock(self, mocker):
        """测试获取前一个交易日（mock）"""
        mocker.patch(
            "jk2bt.utils.date_utils.get_all_trade_days",
            return_value=pd.DatetimeIndex(["2023-01-03", "2023-01-04", "2023-01-05"]),
        )
        result = get_previous_trade_date("2023-01-05", n=1)
        assert result == pd.Timestamp("2023-01-04")

    def test_get_next_trade_date_mock(self, mocker):
        """测试获取下一个交易日（mock）"""
        mocker.patch(
            "jk2bt.utils.date_utils.get_all_trade_days",
            return_value=pd.DatetimeIndex(["2023-01-03", "2023-01-04", "2023-01-05"]),
        )
        result = get_next_trade_date("2023-01-03", n=1)
        assert result == pd.Timestamp("2023-01-04")

    def test_count_trade_days_between_mock(self, mocker):
        """测试计算交易日数量（mock）"""
        mocker.patch(
            "jk2bt.utils.date_utils.get_trade_days",
            return_value=pd.DatetimeIndex(["2023-01-03", "2023-01-04", "2023-01-05"]),
        )
        result = count_trade_days_between("2023-01-03", "2023-01-05")
        assert result == 3
