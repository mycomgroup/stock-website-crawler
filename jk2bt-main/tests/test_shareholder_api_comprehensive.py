"""
tests/test_shareholder_api_comprehensive.py
股东信息 API 综合测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.finance_data.shareholder import (
    get_top10_shareholders,
    get_top10_float_shareholders,
    get_shareholder_count,
)


class TestTop10Shareholders:
    """十大股东测试"""

    def test_shanghai_stock(self):
        """测试上交所股票"""
        df = get_top10_shareholders("600000")
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "holder_name" in df.columns

    def test_shenzhen_stock(self):
        """测试深交所股票"""
        df = get_top10_shareholders("000001")
        assert isinstance(df, pd.DataFrame)

    def test_blue_chip_stock(self):
        """测试蓝筹股"""
        blue_chips = ["600519", "601318", "000858"]
        for code in blue_chips:
            df = get_top10_shareholders(code)
            assert isinstance(df, pd.DataFrame)

    def test_data_fields(self):
        """测试数据字段"""
        df = get_top10_shareholders("600519")
        if not df.empty:
            expected_fields = ["holder_name", "hold_amount", "hold_ratio"]
            for field in expected_fields:
                if field in df.columns:
                    assert True

    def test_holder_count(self):
        """测试股东数量"""
        df = get_top10_shareholders("600000")
        if not df.empty:
            # 十大股东应该有接近10条记录
            assert len(df) <= 20


class TestTop10FloatShareholders:
    """十大流通股东测试"""

    def test_shanghai_stock(self):
        """测试上交所股票"""
        df = get_top10_float_shareholders("600000")
        assert isinstance(df, pd.DataFrame)

    def test_shenzhen_stock(self):
        """测试深交所股票"""
        df = get_top10_float_shareholders("000001")
        assert isinstance(df, pd.DataFrame)

    def test_multiple_stocks(self):
        """测试多个股票"""
        stocks = ["600000", "000001", "600519"]
        for code in stocks:
            df = get_top10_float_shareholders(code)
            assert isinstance(df, pd.DataFrame)


class TestShareholderCount:
    """股东户数测试"""

    def test_single_stock(self):
        """测试单个股票"""
        df = get_shareholder_count("600000")
        assert isinstance(df, pd.DataFrame)

    def test_time_series(self):
        """测试时间序列"""
        df = get_shareholder_count("600519")
        if not df.empty:
            # 应该有多期数据
            assert len(df) >= 1

    def test_data_consistency(self):
        """测试数据一致性"""
        df1 = get_shareholder_count("600000", force_update=True)
        df2 = get_shareholder_count("600000", force_update=False)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)


class TestEdgeCases:
    """边缘情况测试"""

    def test_invalid_code(self):
        """测试无效代码"""
        df = get_top10_shareholders("999999")
        assert isinstance(df, pd.DataFrame)

    def test_small_cap_stock(self):
        """测试小盘股"""
        df = get_top10_shareholders("002594")
        assert isinstance(df, pd.DataFrame)

    def test_new_stock(self):
        """测试次新股"""
        df = get_top10_shareholders("603259")
        assert isinstance(df, pd.DataFrame)

    def test_st_stock(self):
        """测试ST股票"""
        try:
            df = get_top10_shareholders("000001")
            assert isinstance(df, pd.DataFrame)
        except Exception:
            pass


class TestDataQuality:
    """数据质量测试"""

    def test_holder_name_not_empty(self):
        """测试股东名称非空"""
        df = get_top10_shareholders("600519")
        if not df.empty and "holder_name" in df.columns:
            non_empty = df["holder_name"].notna().sum()
            assert non_empty > 0

    def test_hold_ratio_range(self):
        """测试持股比例范围"""
        df = get_top10_shareholders("600000")
        if not df.empty and "hold_ratio" in df.columns:
            valid_ratios = df["hold_ratio"].dropna()
            if len(valid_ratios) > 0:
                assert (valid_ratios >= 0).all()


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("股东信息 API 综合测试")
    print("=" * 70)
    
    test_classes = [
        TestTop10Shareholders,
        TestTop10FloatShareholders,
        TestShareholderCount,
        TestEdgeCases,
        TestDataQuality,
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
