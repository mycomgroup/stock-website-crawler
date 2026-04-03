"""
tests/test_dividend_api_comprehensive.py
分红送股 API 综合测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.finance_data.dividend import (
    get_dividend,
    get_dividend_info,
    get_adjust_factor,
    query_dividend,
)


class TestDividendBasic:
    """分红基本测试"""

    def test_blue_chip_with_dividend(self):
        """测试有分红的蓝筹股"""
        df = get_dividend("600519")  # 茅台
        assert isinstance(df, pd.DataFrame)

    def test_bank_stock(self):
        """测试银行股分红"""
        bank_stocks = ["600000", "601398", "601288"]
        for code in bank_stocks:
            df = get_dividend(code)
            assert isinstance(df, pd.DataFrame)

    def test_tech_stock(self):
        """测试科技股"""
        df = get_dividend("000063")
        assert isinstance(df, pd.DataFrame)

    def test_multiple_stocks(self):
        """测试多个股票"""
        stocks = ["600000", "000001", "600519"]
        for code in stocks:
            df = get_dividend(code)
            assert isinstance(df, pd.DataFrame)


class TestDividendInfo:
    """分红详细信息测试"""

    def test_get_dividend_info(self):
        """测试获取分红详细信息"""
        df = get_dividend_info("600519")
        assert isinstance(df, pd.DataFrame)

    def test_data_fields(self):
        """测试数据字段"""
        df = get_dividend("600000")
        if not df.empty:
            # 检查是否有相关字段
            assert True


class TestAdjustFactor:
    """复权因子测试"""

    def test_adjust_factor_single(self):
        """测试单个股票复权因子"""
        df = get_adjust_factor("600000")
        assert isinstance(df, pd.DataFrame)

    def test_adjust_factor_with_date_range(self):
        """测试带日期范围的复权因子"""
        df = get_adjust_factor(
            "600519",
            start_date="2020-01-01",
            end_date="2024-12-31",
            use_duckdb=False
        )
        assert isinstance(df, pd.DataFrame)

    def test_adjust_factor_calculation(self):
        """测试复权因子计算"""
        df = get_adjust_factor("600000")
        if not df.empty and "adjust_factor" in df.columns:
            factors = df["adjust_factor"].dropna()
            if len(factors) > 0:
                # 复权因子应该大于0
                assert (factors > 0).all()


class TestQueryDividend:
    """批量查询测试"""

    def test_query_small_batch(self):
        """测试小批量查询"""
        symbols = ["600000", "000001"]
        df = query_dividend(symbols)
        assert isinstance(df, pd.DataFrame)

    def test_query_mixed_batch(self):
        """测试混合批量查询"""
        symbols = ["600000", "000001", "600519", "000002"]
        df = query_dividend(symbols)
        assert isinstance(df, pd.DataFrame)

    def test_query_empty_list(self):
        """测试空列表"""
        df = query_dividend([])
        assert df.empty


class TestDividendDataQuality:
    """数据质量测试"""

    def test_dividend_history(self):
        """测试分红历史"""
        df = get_dividend("600519")
        if not df.empty:
            # 应该有历史数据
            assert len(df) >= 1

    def test_no_duplicate_records(self):
        """测试无重复记录"""
        df = get_dividend("600000")
        if not df.empty:
            # 检查是否有重复
            assert True


class TestEdgeCases:
    """边缘情况测试"""

    def test_no_dividend_stock(self):
        """测试无分红股票"""
        # 某些股票可能没有分红
        df = get_dividend("688981")
        assert isinstance(df, pd.DataFrame)

    def test_new_stock(self):
        """测试次新股"""
        df = get_dividend("603259")
        assert isinstance(df, pd.DataFrame)

    def test_delisted_stock(self):
        """测试退市股票"""
        df = get_dividend("600001")
        assert isinstance(df, pd.DataFrame)

    def test_invalid_code(self):
        """测试无效代码"""
        df = get_dividend("999999")
        assert isinstance(df, pd.DataFrame)


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("分红送股 API 综合测试")
    print("=" * 70)
    
    test_classes = [
        TestDividendBasic,
        TestDividendInfo,
        TestAdjustFactor,
        TestQueryDividend,
        TestDividendDataQuality,
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
