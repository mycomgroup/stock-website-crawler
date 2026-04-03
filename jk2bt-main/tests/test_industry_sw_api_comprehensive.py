"""
tests/test_industry_sw_api_comprehensive.py
申万行业 API 综合测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.market_data.industry_sw import (
    get_stock_industry,
    get_industry_stocks_sw,
    get_sw_level1,
    get_sw_level2,
    get_sw_level3,
)


class TestIndustryClassification:
    """行业分类测试"""

    def test_get_industry_single_stock(self):
        """测试单个股票行业"""
        result = get_stock_industry("600000")
        assert result is not None

    def test_get_industry_bank(self):
        """测试银行股行业"""
        bank_stocks = ["600000", "601398", "601288"]
        for code in bank_stocks:
            result = get_stock_industry(code)
            assert result is not None

    def test_get_industry_tech(self):
        """测试科技股行业"""
        result = get_stock_industry("000063")
        assert result is not None

    def test_get_industry_consumer(self):
        """测试消费股行业"""
        result = get_stock_industry("600519")
        assert result is not None


class TestIndustryLevels:
    """行业级别测试"""

    def test_level1_industries(self):
        """测试一级行业"""
        result = get_sw_level1()
        assert result is not None

    def test_level2_industries(self):
        """测试二级行业"""
        result = get_sw_level2()
        assert result is not None

    def test_level3_industries(self):
        """测试三级行业"""
        result = get_sw_level3()
        assert result is not None


class TestIndustryStocks:
    """行业成分股测试"""

    def test_bank_industry_stocks(self):
        """测试银行业成分股"""
        result = get_industry_stocks_sw("银行")
        assert result is not None

    def test_realestate_industry_stocks(self):
        """测试房地产行业成分股"""
        result = get_industry_stocks_sw("房地产")
        assert result is not None


class TestEdgeCases:
    """边缘情况测试"""

    def test_invalid_stock_code(self):
        """测试无效股票代码"""
        result = get_stock_industry("999999")
        assert result is not None

    def test_invalid_industry_name(self):
        """测试无效行业名称"""
        result = get_industry_stocks_sw("不存在的行业")
        assert result is not None

    def test_new_stock(self):
        """测试次新股"""
        result = get_stock_industry("688001")
        assert result is not None


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("申万行业 API 综合测试")
    print("=" * 70)
    
    test_classes = [
        TestIndustryClassification,
        TestIndustryLevels,
        TestIndustryStocks,
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
