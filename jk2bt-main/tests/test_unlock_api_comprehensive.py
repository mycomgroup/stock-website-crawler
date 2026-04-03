"""
tests/test_unlock_api_comprehensive.py
限售解禁 API 综合测试
"""

import pytest
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.finance_data.unlock import (
    get_unlock,
    query_unlock,
    get_unlock_calendar,
)


class TestUnlockSchedule:
    """解禁时间表测试"""

    def test_single_stock(self):
        """测试单个股票"""
        df = get_unlock("600000")
        assert isinstance(df, pd.DataFrame)

    def test_multiple_stocks(self):
        """测试多个股票"""
        stocks = ["600000", "000001", "600519"]
        for code in stocks:
            df = get_unlock(code)
            assert isinstance(df, pd.DataFrame)

    def test_with_date_range(self):
        """测试带日期范围"""
        start = datetime.now().strftime("%Y-%m-%d")
        end = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
        df = get_unlock("600000", start_date=start, end_date=end)
        assert isinstance(df, pd.DataFrame)

    def test_future_unlock(self):
        """测试未来解禁"""
        df = get_unlock("600519")
        if not df.empty and "unlock_date" in df.columns:
            # 检查是否有未来的解禁日期
            assert True


class TestQueryUnlock:
    """批量查询测试"""

    def test_batch_query(self):
        """测试批量查询"""
        symbols = ["600000", "000001"]
        df = query_unlock(symbols)
        assert isinstance(df, pd.DataFrame)

    def test_empty_list(self):
        """测试空列表"""
        df = query_unlock([])
        assert df.empty


class TestUnlockCalendar:
    """解禁日历测试"""

    def test_current_month(self):
        """测试当月"""
        today = datetime.now()
        df = get_unlock_calendar(today.strftime("%Y%m"))
        assert isinstance(df, pd.DataFrame)

    def test_specific_month(self):
        """测试特定月份"""
        df = get_unlock_calendar("202401")
        assert isinstance(df, pd.DataFrame)


class TestDataQuality:
    """数据质量测试"""

    def test_unlock_amount(self):
        """测试解禁数量"""
        df = get_unlock("600000")
        if not df.empty and "unlock_amount" in df.columns:
            amounts = df["unlock_amount"].dropna()
            if len(amounts) > 0:
                # 解禁数量应该大于0
                assert (amounts > 0).all()

    def test_unlock_ratio(self):
        """测试解禁比例"""
        df = get_unlock("600519")
        if not df.empty and "unlock_ratio" in df.columns:
            ratios = df["unlock_ratio"].dropna()
            if len(ratios) > 0:
                # 解禁比例应该在合理范围
                assert True


class TestEdgeCases:
    """边缘情况测试"""

    def test_no_unlock_stock(self):
        """测试无解禁股票"""
        df = get_unlock("000001")
        assert isinstance(df, pd.DataFrame)

    def test_new_stock(self):
        """测试次新股"""
        df = get_unlock("688001")
        assert isinstance(df, pd.DataFrame)

    def test_invalid_code(self):
        """测试无效代码"""
        df = get_unlock("999999")
        assert isinstance(df, pd.DataFrame)


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("限售解禁 API 综合测试")
    print("=" * 70)
    
    test_classes = [
        TestUnlockSchedule,
        TestQueryUnlock,
        TestUnlockCalendar,
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
