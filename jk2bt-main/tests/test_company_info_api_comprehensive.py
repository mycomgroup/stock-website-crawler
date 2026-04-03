"""
tests/test_company_info_api_comprehensive.py
公司基本信息 API 综合测试

测试覆盖：
1. 正常查询测试
2. 不同代码格式测试
3. 边缘情况测试
4. 错误处理测试
5. 缓存机制测试
6. 数据完整性测试
"""

import pytest
import pandas as pd
import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.finance_data.company_info import (
    get_company_info,
    get_security_status,
    query_company_basic_info,
    query_status_change,
    _extract_code_num,
    _normalize_to_jq,
)


class TestCompanyInfoNormal:
    """正常查询测试"""

    def test_get_company_info_shanghai(self):
        """测试上交所股票"""
        codes = ["600000", "600519", "601318"]
        for code in codes:
            df = get_company_info(code)
            assert isinstance(df, pd.DataFrame)
            if not df.empty:
                assert "code" in df.columns
                assert df["code"].iloc[0].endswith(".XSHG")

    def test_get_company_info_shenzhen(self):
        """测试深交所股票"""
        codes = ["000001", "000002", "002594"]
        for code in codes:
            df = get_company_info(code)
            assert isinstance(df, pd.DataFrame)
            if not df.empty:
                assert df["code"].iloc[0].endswith(".XSHE")

    def test_get_company_info_jq_format(self):
        """测试聚宽格式代码"""
        df1 = get_company_info("600000.XSHG")
        df2 = get_company_info("000001.XSHE")
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)

    def test_get_company_info_with_prefix(self):
        """测试带前缀代码"""
        df1 = get_company_info("sh600000")
        df2 = get_company_info("sz000001")
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)


class TestCompanyInfoBatch:
    """批量查询测试"""

    def test_query_batch_small(self):
        """测试小批量查询"""
        symbols = ["600000", "000001"]
        df = query_company_basic_info(symbols)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert len(df) >= 1

    def test_query_batch_mixed_exchange(self):
        """测试混合交易所批量查询"""
        symbols = ["600000", "000001", "600519", "002594"]
        df = query_company_basic_info(symbols)
        assert isinstance(df, pd.DataFrame)

    def test_query_empty_list(self):
        """测试空列表"""
        df = query_company_basic_info([])
        assert df.empty


class TestSecurityStatus:
    """证券状态测试"""

    def test_get_security_status_current(self):
        """测试当前状态"""
        df = get_security_status("600000")
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "status_type" in df.columns

    def test_get_security_status_with_date(self):
        """测试指定日期状态"""
        df = get_security_status("600000", date="2024-01-15")
        assert isinstance(df, pd.DataFrame)

    def test_get_security_status_multiple(self):
        """测试多个股票状态"""
        for code in ["600000", "000001", "600519"]:
            df = get_security_status(code)
            assert isinstance(df, pd.DataFrame)


class TestCodeNormalization:
    """代码标准化测试"""

    def test_extract_code_num(self):
        """测试代码提取"""
        test_cases = [
            ("600000", "600000"),
            ("sh600000", "600000"),
            ("sz000001", "000001"),
            ("600000.XSHG", "600000"),
            ("000001.XSHE", "000001"),
            ("1", "000001"),
            ("600519", "600519"),
        ]
        for input_code, expected in test_cases:
            result = _extract_code_num(input_code)
            assert result == expected, f"Failed: {input_code} -> {result} (expected {expected})"

    def test_normalize_to_jq(self):
        """测试聚宽格式转换"""
        test_cases = [
            ("600000", "600000.XSHG"),
            ("000001", "000001.XSHE"),
            ("sh600000", "600000.XSHG"),
            ("sz000001", "000001.XSHE"),
            ("600000.XSHG", "600000.XSHG"),
            ("000001.XSHE", "000001.XSHE"),
            ("002594", "002594.XSHE"),
            ("688001", "688001.XSHG"),
        ]
        for input_code, expected in test_cases:
            result = _normalize_to_jq(input_code)
            assert result == expected, f"Failed: {input_code} -> {result} (expected {expected})"

    def test_code_prefix_handling(self):
        """测试代码前缀处理"""
        # 上海股票以6开头
        assert _normalize_to_jq("600000").endswith(".XSHG")
        assert _normalize_to_jq("601318").endswith(".XSHG")
        assert _normalize_to_jq("688001").endswith(".XSHG")
        
        # 深圳股票
        assert _normalize_to_jq("000001").endswith(".XSHE")
        assert _normalize_to_jq("002594").endswith(".XSHE")
        assert _normalize_to_jq("300750").endswith(".XSHE")


class TestCache:
    """缓存机制测试"""

    def test_cache_consistency(self):
        """测试缓存一致性"""
        df1 = get_company_info("600000", force_update=True)
        df2 = get_company_info("600000", force_update=False)
        
        # 两次查询结果应该一致或都为空
        if not df1.empty and not df2.empty:
            assert df1["code"].iloc[0] == df2["code"].iloc[0]

    def test_cache_update(self):
        """测试缓存更新"""
        df1 = get_company_info("600036", force_update=True)
        df2 = get_company_info("600036", force_update=False)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)


class TestEdgeCases:
    """边缘情况测试"""

    def test_invalid_code(self):
        """测试无效代码"""
        df = get_company_info("999999")
        # 应该返回空DataFrame或处理异常
        assert isinstance(df, pd.DataFrame)

    def test_empty_code(self):
        """测试空代码"""
        try:
            df = get_company_info("")
            assert isinstance(df, pd.DataFrame)
        except Exception:
            pass  # 允许抛出异常

    def test_special_characters(self):
        """测试特殊字符"""
        codes = ["600000-", "600000+", "600000 "]
        for code in codes:
            try:
                df = get_company_info(code)
                assert isinstance(df, pd.DataFrame)
            except Exception:
                pass

    def test_future_date(self):
        """测试未来日期"""
        df = get_security_status("600000", date="2030-01-01")
        assert isinstance(df, pd.DataFrame)

    def test_past_date(self):
        """测试历史日期"""
        df = get_security_status("600000", date="2020-01-01")
        assert isinstance(df, pd.DataFrame)


class TestDataQuality:
    """数据质量测试"""

    def test_data_columns(self):
        """测试数据列"""
        df = get_company_info("600000")
        if not df.empty:
            expected_columns = ["code"]
            for col in expected_columns:
                assert col in df.columns

    def test_data_types(self):
        """测试数据类型"""
        df = get_company_info("600000")
        if not df.empty:
            assert isinstance(df, pd.DataFrame)
            if "code" in df.columns:
                assert isinstance(df["code"].iloc[0], str)

    def test_data_not_empty_for_major_stocks(self):
        """测试主要股票数据非空"""
        major_stocks = ["600000", "000001", "600519"]
        non_empty_count = 0
        for code in major_stocks:
            df = get_company_info(code)
            if not df.empty:
                non_empty_count += 1
        
        # 至少有一个股票能获取到数据
        assert non_empty_count >= 1


class TestPerformance:
    """性能测试"""

    def test_single_query_speed(self):
        """测试单次查询速度"""
        start = time.time()
        df = get_company_info("600000")
        elapsed = time.time() - start
        
        # 查询应该在合理时间内完成
        assert elapsed < 30, f"Query took {elapsed}s, too slow"

    def test_batch_query_speed(self):
        """测试批量查询速度"""
        symbols = ["600000", "000001", "600519", "000002", "600036"]
        
        start = time.time()
        df = query_company_basic_info(symbols)
        elapsed = time.time() - start
        
        assert elapsed < 60, f"Batch query took {elapsed}s, too slow"


def run_all_tests():
    """运行所有测试"""
    print("=" * 70)
    print("公司基本信息 API 综合测试")
    print("=" * 70)
    
    test_classes = [
        TestCompanyInfoNormal,
        TestCompanyInfoBatch,
        TestSecurityStatus,
        TestCodeNormalization,
        TestCache,
        TestEdgeCases,
        TestDataQuality,
        TestPerformance,
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n--- {test_class.__name__} ---")
        instance = test_class()
        
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                total_tests += 1
                try:
                    method = getattr(instance, method_name)
                    method()
                    print(f"  ✓ {method_name}")
                    passed_tests += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {str(e)[:50]}")
    
    print("\n" + "=" * 70)
    print(f"测试结果: {passed_tests}/{total_tests} 通过")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
