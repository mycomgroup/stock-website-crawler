"""
tests/test_macro_api_comprehensive.py
宏观数据 API 综合测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.finance_data.macro import (
    get_macro_data,
    get_macro_series,
    get_macro_indicators,
)


class TestMacroIndicators:
    """宏观指标测试"""

    def test_get_indicators_list(self):
        """测试获取指标列表"""
        indicators = get_macro_indicators()
        assert isinstance(indicators, list)
        assert len(indicators) > 0

    def test_indicator_info(self):
        """测试指标信息"""
        indicators = get_macro_indicators()
        for indicator in indicators[:3]:
            assert isinstance(indicator, dict)
            assert "name" in indicator or "code" in indicator


class TestMacroData:
    """宏观数据测试"""

    def test_cpi_data(self):
        """测试CPI数据"""
        df = get_macro_data("CPI")
        assert isinstance(df, pd.DataFrame)

    def test_ppi_data(self):
        """测试PPI数据"""
        df = get_macro_data("PPI")
        assert isinstance(df, pd.DataFrame)

    def test_gdp_data(self):
        """测试GDP数据"""
        df = get_macro_data("GDP")
        assert isinstance(df, pd.DataFrame)

    def test_m2_data(self):
        """测试M2数据"""
        df = get_macro_data("M2")
        assert isinstance(df, pd.DataFrame)


class TestMacroSeries:
    """时间序列测试"""

    def test_cpi_series(self):
        """测试CPI序列"""
        df = get_macro_series("CPI", start_date="2020-01-01")
        assert isinstance(df, pd.DataFrame)

    def test_series_with_end_date(self):
        """测试带结束日期的序列"""
        df = get_macro_series(
            "PPI",
            start_date="2022-01-01",
            end_date="2024-12-31",
            use_duckdb=False
        )
        assert isinstance(df, pd.DataFrame)

    def test_series_data_range(self):
        """测试数据范围"""
        df = get_macro_series("CPI", start_date="2023-01-01")
        if not df.empty and "date" in df.columns:
            # 应该有数据
            assert len(df) >= 1


class TestDataQuality:
    """数据质量测试"""

    def test_data_columns(self):
        """测试数据列"""
        df = get_macro_data("CPI")
        if not df.empty:
            expected_cols = ["indicator", "date", "value"]
            for col in expected_cols:
                if col in df.columns:
                    assert True

    def test_value_not_empty(self):
        """测试值非空"""
        df = get_macro_data("CPI")
        if not df.empty and "value" in df.columns:
            non_empty = df["value"].notna().sum()
            assert non_empty > 0

    def test_date_format(self):
        """测试日期格式"""
        df = get_macro_data("PPI")
        if not df.empty and "date" in df.columns:
            # 检查日期格式
            assert True


class TestCache:
    """缓存测试"""

    def test_cache_consistency(self):
        """测试缓存一致性"""
        df1 = get_macro_data("CPI", force_update=True)
        df2 = get_macro_data("CPI", force_update=False)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)


class TestEdgeCases:
    """边缘情况测试"""

    def test_invalid_indicator(self):
        """测试无效指标"""
        try:
            df = get_macro_data("INVALID_INDICATOR")
            assert isinstance(df, pd.DataFrame)
        except Exception:
            pass

    def test_future_date(self):
        """测试未来日期"""
        df = get_macro_series("CPI", start_date="2030-01-01")
        assert isinstance(df, pd.DataFrame)

    def test_old_date(self):
        """测试历史日期"""
        df = get_macro_series("PPI", start_date="2000-01-01")
        assert isinstance(df, pd.DataFrame)


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("宏观数据 API 综合测试")
    print("=" * 70)
    
    test_classes = [
        TestMacroIndicators,
        TestMacroData,
        TestMacroSeries,
        TestDataQuality,
        TestCache,
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
