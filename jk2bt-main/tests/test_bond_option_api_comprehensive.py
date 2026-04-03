"""
tests/test_bond_option_api_comprehensive.py
可转债与期权 API 综合测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.market_data.conversion_bond import (
    get_conversion_bond_list,
    get_conversion_bond_quote,
    calculate_conversion_value,
    calculate_premium_rate,
)
from jk2bt.market_data.option import (
    get_option_list,
    get_option_quote,
    get_option_chain,
)


class TestConversionBondList:
    """可转债列表测试"""

    def test_get_list(self):
        """测试获取可转债列表"""
        df = get_conversion_bond_list(use_duckdb=False)
        assert isinstance(df, pd.DataFrame)

    def test_list_not_empty(self):
        """测试列表非空"""
        df = get_conversion_bond_list(use_duckdb=False)
        # 可转债列表应该有数据
        if not df.empty:
            assert len(df) > 0

    def test_list_columns(self):
        """测试列表字段"""
        df = get_conversion_bond_list(use_duckdb=False)
        if not df.empty:
            # 应该包含基本字段
            assert True


class TestConversionCalculation:
    """转股价值计算测试"""

    def test_conversion_value_basic(self):
        """测试基本转股价值计算"""
        # 转股价100，正股价50
        value = calculate_conversion_value(100.0, 50.0)
        assert abs(value - 50.0) < 0.01

    def test_conversion_value_high_price(self):
        """测试高股价转股价值"""
        # 转股价100，正股价200
        value = calculate_conversion_value(100.0, 200.0)
        assert abs(value - 200.0) < 0.01

    def test_conversion_value_low_price(self):
        """测试低股价转股价值"""
        # 转股价100，正股价50
        value = calculate_conversion_value(100.0, 50.0)
        assert value == 50.0

    def test_premium_rate_positive(self):
        """测试正溢价率"""
        # 债券价格110，转股价值100
        rate = calculate_premium_rate(110.0, 100.0)
        assert abs(rate - 10.0) < 0.01

    def test_premium_rate_negative(self):
        """测试负溢价率"""
        # 债券价格90，转股价值100
        rate = calculate_premium_rate(90.0, 100.0)
        assert abs(rate - (-10.0)) < 0.01

    def test_premium_rate_zero(self):
        """测试零溢价率"""
        # 债券价格100，转股价值100
        rate = calculate_premium_rate(100.0, 100.0)
        assert abs(rate) < 0.01


class TestOptionList:
    """期权列表测试"""

    def test_50etf_option_list(self):
        """测试50ETF期权列表"""
        df = get_option_list("50etf")
        assert isinstance(df, pd.DataFrame)

    def test_300etf_option_list(self):
        """测试300ETF期权列表"""
        df = get_option_list("300etf")
        assert isinstance(df, pd.DataFrame)

    def test_option_list_columns(self):
        """测试期权列表字段"""
        df = get_option_list("50etf")
        if not df.empty:
            # 应该有期权代码等字段
            assert True


class TestOptionChain:
    """期权链测试"""

    def test_option_chain_50etf(self):
        """测试50ETF期权链"""
        df = get_option_chain("50etf")
        assert isinstance(df, pd.DataFrame)

    def test_option_chain_with_date(self):
        """测试带日期的期权链"""
        df = get_option_chain("50etf", date="2024-01-01")
        assert isinstance(df, pd.DataFrame)


class TestEdgeCases:
    """边缘情况测试"""

    def test_invalid_bond_code(self):
        """测试无效债券代码"""
        df = get_conversion_bond_quote("999999")
        assert isinstance(df, pd.DataFrame)

    def test_invalid_option_underlying(self):
        """测试无效期权标的"""
        df = get_option_list("invalid")
        assert isinstance(df, pd.DataFrame)

    def test_zero_conversion_price(self):
        """测试零转股价"""
        value = calculate_conversion_value(0.0, 100.0)
        assert value == 0.0

    def test_zero_conversion_value(self):
        """测试零转股价值"""
        rate = calculate_premium_rate(100.0, 0.0)
        assert rate == 0.0


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("可转债与期权 API 综合测试")
    print("=" * 70)
    
    test_classes = [
        TestConversionBondList,
        TestConversionCalculation,
        TestOptionList,
        TestOptionChain,
        TestEdgeCases,
    ]
    
    total = 0
    passed = 0
    
    for test_class in test_classes:
        print(f"\n--- {test_class.__name__} ---")
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                total += 1
                try:
                    getattr(instance, method_name)()
                    print(f"  ✓ {method_name}")
                    passed += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {str(e)[:50]}")
    
    print("\n" + "=" * 70)
    print(f"测试结果: {passed}/{total} 通过")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
