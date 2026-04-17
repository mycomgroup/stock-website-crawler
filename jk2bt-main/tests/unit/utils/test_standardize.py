"""
test_standardize.py
OHLCV 数据标准化模块测试
"""

import pytest
import pandas as pd
import numpy as np
from jk2bt.utils.standardize import (
    normalize_columns,
    normalize_datetime,
    validate_required_columns,
    convert_numeric_columns,
    standardize_ohlcv,
    standardize_minute_ohlcv,
    standardize_financial,
    COLUMN_MAP_COMMON,
    COLUMN_MAP_DAILY,
)


class TestNormalizeColumns:
    """测试列名标准化"""

    def test_chinese_to_english_mapping(self):
        """测试中文列名转英文"""
        df = pd.DataFrame(
            {
                "日期": ["2023-01-01", "2023-01-02"],
                "开盘": [100.0, 101.0],
                "收盘": [105.0, 106.0],
            }
        )
        result = normalize_columns(df)
        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "close" in result.columns
        assert result["datetime"].tolist() == ["2023-01-01", "2023-01-02"]

    def test_custom_column_map(self):
        """测试自定义列名映射"""
        df = pd.DataFrame(
            {
                "old_col": [1, 2, 3],
                "other": [4, 5, 6],
            }
        )
        custom_map = {"old_col": "new_col"}
        result = normalize_columns(df, column_map=custom_map)
        assert "new_col" in result.columns
        assert "old_col" not in result.columns

    def test_no_matching_columns(self):
        """测试无匹配列名时返回原数据"""
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        result = normalize_columns(df)
        assert result.equals(df)

    def test_preserve_existing_columns(self):
        """测试保留已有列"""
        df = pd.DataFrame(
            {
                "datetime": ["2023-01-01"],
                "open": [100.0],
                "日期": ["2023-01-01"],
            }
        )
        result = normalize_columns(df)
        assert "datetime" in result.columns
        assert "open" in result.columns


class TestNormalizeDatetime:
    """测试时间戳标准化"""

    def test_normalize_datetime_column(self):
        """测试 datetime 列转换"""
        df = pd.DataFrame(
            {
                "datetime": ["2023-01-01", "2023-01-02", "2023-01-03"],
                "value": [1, 2, 3],
            }
        )
        result = normalize_datetime(df)
        assert isinstance(result["datetime"].iloc[0], pd.Timestamp)

    def test_sort_by_datetime(self):
        """测试按时间排序"""
        df = pd.DataFrame(
            {
                "datetime": ["2023-01-03", "2023-01-01", "2023-01-02"],
                "value": [3, 1, 2],
            }
        )
        result = normalize_datetime(df)
        assert result["datetime"].iloc[0] == pd.Timestamp("2023-01-01")

    def test_missing_datetime_column(self):
        """测试缺少 datetime 列"""
        df = pd.DataFrame({"value": [1, 2, 3]})
        result = normalize_datetime(df)
        assert result.equals(df)

    def test_drop_na_datetime(self):
        """测试移除 NA 时间"""
        df = pd.DataFrame(
            {
                "datetime": ["2023-01-01", "invalid", "2023-01-02"],
                "value": [1, 2, 3],
            }
        )
        result = normalize_datetime(df)
        assert len(result) == 2


class TestValidateRequiredColumns:
    """测试必要列验证"""

    def test_all_columns_present(self):
        """测试所有列存在时不抛异常"""
        df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
        validate_required_columns(df, ["a", "b"])

    def test_missing_columns_raises(self):
        """测试缺少列时抛 ValueError"""
        df = pd.DataFrame({"a": [1], "b": [2]})
        with pytest.raises(ValueError, match="数据缺少必要列"):
            validate_required_columns(df, ["a", "b", "c"])


class TestConvertNumericColumns:
    """测试数值列转换"""

    def test_convert_to_float64(self):
        """测试转换为 float64"""
        df = pd.DataFrame(
            {
                "col1": ["1.0", "2.0", "3.0"],
                "col2": [4, 5, 6],
            }
        )
        result = convert_numeric_columns(df, ["col1", "col2"])
        assert result["col1"].dtype == np.float64
        assert result["col2"].dtype == np.float64

    def test_coerce_errors(self):
        """测试错误值被设为 NaN"""
        df = pd.DataFrame(
            {
                "col1": ["1.0", "invalid", "3.0"],
            }
        )
        result = convert_numeric_columns(df, ["col1"])
        assert pd.isna(result["col1"].iloc[1])

    def test_missing_column_skipped(self):
        """测试不存在的列被跳过"""
        df = pd.DataFrame({"a": [1, 2, 3]})
        result = convert_numeric_columns(df, ["a", "nonexistent"])
        assert "nonexistent" not in result.columns


class TestStandardizeOhlcv:
    """测试日线 OHLCV 标准化"""

    def test_basic_ohlcv_standardize(self):
        """测试基本日线标准化"""
        df = pd.DataFrame(
            {
                "日期": ["2023-01-01", "2023-01-02"],
                "开盘": ["100.0", "101.0"],
                "最高": ["105.0", "106.0"],
                "最低": ["99.0", "100.0"],
                "收盘": ["103.0", "104.0"],
                "成交量": ["1000000", "1100000"],
            }
        )
        result = standardize_ohlcv(df)
        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "high" in result.columns
        assert "low" in result.columns
        assert "close" in result.columns
        assert "volume" in result.columns
        assert "openinterest" in result.columns

    def test_ohlcv_missing_volume(self):
        """测试缺少成交量时补充为0"""
        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=2),
                "open": [100.0, 101.0],
                "high": [105.0, 106.0],
                "low": [99.0, 100.0],
                "close": [103.0, 104.0],
            }
        )
        result = standardize_ohlcv(df)
        assert "volume" in result.columns
        assert result["volume"].iloc[0] == 0.0

    def test_ohlcv_empty_dataframe(self):
        """测试空 DataFrame"""
        df = pd.DataFrame()
        result = standardize_ohlcv(df)
        assert result.empty


class TestStandardizeMinuteOhlcv:
    """测试分钟 OHLCV 标准化"""

    def test_basic_minute_standardize(self):
        """测试基本分钟线标准化"""
        df = pd.DataFrame(
            {
                "时间": ["2023-01-01 09:30", "2023-01-01 09:31"],
                "开盘": [100.0, 101.0],
                "最高": [105.0, 106.0],
                "最低": [99.0, 100.0],
                "收盘": [103.0, 104.0],
                "成交量": [1000, 1100],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert "datetime" in result.columns
        assert "money" in result.columns

    def test_minute_amount_to_money(self):
        """测试 amount 列转为 money"""
        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01 09:30", periods=2, freq="min"),
                "open": [100.0, 101.0],
                "high": [105.0, 106.0],
                "low": [99.0, 100.0],
                "close": [103.0, 104.0],
                "volume": [1000, 1100],
                "amount": [100000, 110000],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert "money" in result.columns


class TestStandardizeFinancial:
    """测试财务数据标准化"""

    def test_financial_basic(self):
        """测试财务数据基本清洗"""
        df = pd.DataFrame(
            {
                "指标": ["营收", "利润"],
                "2023Q1": [100, 50],
                "2023Q2": [120, 60],
            }
        )
        result = standardize_financial(df)
        assert len(result) == 2

    def test_financial_drop_all_na_rows(self):
        """测试移除全空行"""
        df = pd.DataFrame(
            {
                "a": [1, np.nan, np.nan],
                "b": [2, np.nan, np.nan],
            }
        )
        result = standardize_financial(df)
        assert len(result) == 1
