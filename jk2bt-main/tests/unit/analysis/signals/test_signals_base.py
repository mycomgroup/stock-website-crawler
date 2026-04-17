"""
tests/unit/analysis/signals/test_signals_base.py
单元测试：信号检测模块基础工具函数 (base.py)

覆盖函数：
- safe_divide

测试场景：
- 正常除法
- 除零场景（返回 fill_value）
- pd.Series 输入
- numpy 数组输入
- 无穷大/NaN 处理
"""

import pytest
import pandas as pd
import numpy as np

from jk2bt.analysis.signals.base import safe_divide


class TestSafeDivide:
    """safe_divide 函数测试"""

    def test_normal_division(self):
        """测试正常除法"""
        result = safe_divide(10, 2)
        assert result == 5.0

    def test_divide_by_zero_scalar(self):
        """测试标量除零，返回 fill_value"""
        result = safe_divide(10, 0)
        assert np.isnan(result)

    def test_divide_by_zero_with_fill_value(self):
        """测试除零时使用自定义 fill_value"""
        result = safe_divide(10, 0, fill_value=-1.0)
        assert result == -1.0

    def test_zero_dividend(self):
        """测试被除数为零"""
        result = safe_divide(0, 5)
        assert result == 0.0

    def test_negative_division(self):
        """测试负数除法"""
        result = safe_divide(-10, 2)
        assert result == -5.0

    def test_both_negative(self):
        """测试两个负数相除"""
        result = safe_divide(-10, -2)
        assert result == 5.0

    def test_float_division(self):
        """测试浮点数除法"""
        result = safe_divide(10.5, 2.5)
        assert result == pytest.approx(4.2, rel=1e-6)

    def test_series_input(self):
        """测试 pd.Series 输入"""
        a = pd.Series([10, 20, 30])
        b = pd.Series([2, 0, 3])
        result = safe_divide(a, b)

        assert isinstance(result, pd.Series)
        assert len(result) == 3
        assert result.iloc[0] == 5.0
        assert np.isnan(result.iloc[1])
        assert result.iloc[2] == 10.0

    def test_series_with_fill_value(self):
        """测试 pd.Series 除零时使用 fill_value"""
        a = pd.Series([10, 20, 30])
        b = pd.Series([2, 0, 3])
        result = safe_divide(a, b, fill_value=0.0)

        assert result.iloc[1] == 0.0

    def test_series_division_by_zero(self):
        """测试 Series 中部分元素除零"""
        a = pd.Series([10.0])
        b = pd.Series([0.0])
        result = safe_divide(a, b, fill_value=-999.0)
        assert result.iloc[0] == -999.0

    def test_numpy_array_input(self):
        """测试 numpy 数组输入"""
        a = np.array([10.0, 20.0, 30.0])
        b = np.array([2.0, 0.0, 5.0])
        result = safe_divide(a, b)

        assert isinstance(result, np.ndarray)
        assert result[0] == 5.0
        assert np.isnan(result[1])
        assert result[2] == 6.0

    def test_inf_handling(self):
        """测试无穷大处理"""
        result = safe_divide(np.inf, 2)
        assert np.isinf(result)

    def test_nan_in_dividend(self):
        """测试被除数包含 NaN"""
        result = safe_divide(np.nan, 5)
        assert np.isnan(result)

    def test_nan_in_divisor(self):
        """测试除数包含 NaN"""
        result = safe_divide(10, np.nan)
        assert np.isnan(result)

    def test_all_zeros(self):
        """测试分子分母都为零"""
        result = safe_divide(0, 0)
        assert np.isnan(result)

    def test_large_numbers(self):
        """测试大数相除"""
        result = safe_divide(1e10, 1e5)
        assert result == pytest.approx(1e5, rel=1e-6)

    def test_small_numbers(self):
        """测试小数相除"""
        result = safe_divide(1e-10, 1e-5)
        assert result == pytest.approx(1e-5, rel=1e-6)

    def test_zero_fill_value(self):
        """测试 fill_value 为零"""
        result = safe_divide(10, 0, fill_value=0)
        assert result == 0
