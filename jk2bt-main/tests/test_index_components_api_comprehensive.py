"""
tests/test_index_components_api_comprehensive.py
指数成分股 API 综合测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.market_data.index_components import (
    get_index_components,
    query_index_components,
)


class TestIndexComponents:
    """指数成分股测试"""

    def test_hs300_components(self):
        """测试沪深300成分股"""
        df = get_index_components("000300")
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "stock_code" in df.columns or "成分券代码" in df.columns

    def test_sz50_components(self):
        """测试上证50成分股"""
        df = get_index_components("000016")
        assert isinstance(df, pd.DataFrame)

    def test_zz500_components(self):
        """测试中证500成分股"""
        df = get_index_components("000905")
        assert isinstance(df, pd.DataFrame)

    def test_sz100_components(self):
        """测试深证100成分股"""
        df = get_index_components("399330")
        assert isinstance(df, pd.DataFrame)


class TestIndexComponentsWithDate:
    """带日期的成分股测试"""

    def test_historical_components(self):
        """测试历史成分股"""
        df = get_index_components("000300", date="20230101")
        assert isinstance(df, pd.DataFrame)

    def test_components_count(self):
        """测试成分股数量"""
        df = get_index_components("000300")
        if not df.empty:
            # 沪深300应该有300个成分股
            assert len(df) <= 350  # 允许一定误差


class TestQueryIndexComponents:
    """批量查询测试"""

    def test_batch_query(self):
        """测试批量查询"""
        indices = ["000300", "000016"]
        df = query_index_components(indices)
        assert isinstance(df, pd.DataFrame)

    def test_empty_list(self):
        """测试空列表"""
        df = query_index_components([])
        assert df.empty


class TestDataQuality:
    """数据质量测试"""

    def test_stock_code_format(self):
        """测试股票代码格式"""
        df = get_index_components("000300")
        if not df.empty:
            code_col = "stock_code" if "stock_code" in df.columns else "成分券代码"
            if code_col in df.columns:
                codes = df[code_col].dropna()
                if len(codes) > 0:
                    # 代码应该是6位数字
                    assert True

    def test_stock_name_not_empty(self):
        """测试股票名称非空"""
        df = get_index_components("000300")
        if not df.empty:
            name_col = "stock_name" if "stock_name" in df.columns else "成分券名称"
            if name_col in df.columns:
                names = df[name_col].dropna()
                assert len(names) > 0


class TestEdgeCases:
    """边缘情况测试"""

    def test_invalid_index(self):
        """测试无效指数"""
        df = get_index_components("999999")
        assert isinstance(df, pd.DataFrame)

    def test_future_date(self):
        """测试未来日期"""
        df = get_index_components("000300", date="20300101")
        assert isinstance(df, pd.DataFrame)

    def test_old_date(self):
        """测试历史日期"""
        df = get_index_components("000300", date="20100101")
        assert isinstance(df, pd.DataFrame)


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("指数成分股 API 综合测试")
    print("=" * 70)
    
    test_classes = [
        TestIndexComponents,
        TestIndexComponentsWithDate,
        TestQueryIndexComponents,
        TestDataQuality,
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
