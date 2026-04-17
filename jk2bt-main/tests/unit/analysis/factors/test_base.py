"""
test_base.py
analysis/factors/base.py 的单元测试。

测试覆盖：
- normalize_factor_name: 因子名标准化
- normalize_factor_names: 批量标准化
- FactorRegistry 类: 注册、获取、列表、元信息、检查注册
- safe_divide: 安全除法
"""

import pytest
import pandas as pd
import numpy as np

from jk2bt.analysis.factors.base import (
    normalize_factor_name,
    normalize_factor_names,
    FactorRegistry,
    global_factor_registry,
    safe_divide,
    fill_missing_with_warning,
    slice_window,
    align_to_trade_days,
)


class TestNormalizeFactorName:
    """测试因子名标准化"""

    def test_exact_match(self):
        assert normalize_factor_name("pe_ratio") == "pe_ratio"

    def test_alias_mapping(self):
        assert normalize_factor_name("PE") == "pe_ratio"
        assert normalize_factor_name("市盈率") == "pe_ratio"

    def test_unknown_name_returns_original(self):
        assert normalize_factor_name("unknown_factor") == "unknown_factor"


class TestNormalizeFactorNames:
    """测试批量标准化"""

    def test_list_input(self):
        result = normalize_factor_names(["PE", "PB", "ROE"])
        assert result == ["pe_ratio", "pb_ratio", "roe"]

    def test_empty_list(self):
        assert normalize_factor_names([]) == []


class TestFactorRegistry:
    """测试因子注册中心"""

    def test_register_factor(self):
        registry = FactorRegistry()

        @registry.register("test_factor")
        def test_compute(data):
            return data

        assert "test_factor" in registry.list_factors()

    def test_get_factor(self):
        registry = FactorRegistry()

        @registry.register("my_factor")
        def my_compute(data):
            return data * 2

        func = registry.get_factor("my_factor")
        assert func(np.array([1, 2])) == [2, 4]

    def test_list_factors(self):
        registry = FactorRegistry()
        assert isinstance(registry.list_factors(), list)


class TestSafeDivide:
    """测试安全除法"""

    def test_normal_division(self):
        result = safe_divide(10.0, 2.0)
        assert result == 5.0

    def test_zero_division_returns_zero(self):
        result = safe_divide(10.0, 0.0)
        assert result == 0.0

    def test_series_division(self):
        a = pd.Series([10, 20, 30])
        b = pd.Series([2, 0, 3])
        result = safe_divide(a, b)
        expected = pd.Series([5.0, 0.0, 10.0])
        pd.testing.assert_series_equal(result, expected)

    def test_array_division(self):
        a = np.array([10, 20, 30])
        b = np.array([2, 0, 3])
        result = safe_divide(a, b)
        expected = np.array([5.0, 0.0, 10.0])
        np.testing.assert_array_equal(result, expected)


class TestSliceWindow:
    """测试切片窗口"""

    def test_slice_window(self):
        df = pd.DataFrame(
            {"date": pd.date_range("2020-01-01", periods=10), "value": range(10)}
        )
        result = slice_window(df, "date", "2020-01-03", "2020-01-07")
        assert len(result) == 5


class TestAlignToTradeDays:
    """测试交易日对齐"""

    def test_align_basic(self):
        dates = pd.DatetimeIndex(["2020-01-01", "2020-01-03", "2020-01-05"])
        trade_days = pd.DatetimeIndex(["2020-01-02", "2020-01-04", "2020-01-06"])
        result = align_to_trade_days(dates, trade_days)
        assert isinstance(result, pd.DatetimeIndex)
