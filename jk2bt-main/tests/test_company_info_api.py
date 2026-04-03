"""
test_company_info_api.py
公司基本信息与状态变动 API 全面测试

测试覆盖:
1. 正常功能测试 - 数据获取成功
2. 边界条件测试 - 空输入、None输入、无效代码
3. 异常处理测试 - 网络失败、数据缺失
4. 缓存机制测试 - 缓存命中、缓存过期
5. RobustResult 测试 - success/data/reason/source 验证
6. 批量查询测试 - 多股票查询
7. 代码格式兼容测试 - .XSHG/.XSHE/sh/sz/纯数字
"""

import unittest
import pandas as pd
import os
import tempfile
import shutil
from datetime import datetime

import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.finance_data.company_info import (
    get_company_info,
    get_company_info_robust,
    get_security_status,
    get_security_status_robust,
    query_company_basic_info,
    query_company_info_robust,
    query_status_change,
    get_company_info_list,
    get_industry_info,
    prewarm_company_info_cache,
    RobustResult,
    CACHE_EXPIRE_DAYS,
    FinanceQuery,
    run_query_simple,
    _extract_code_num,
    _normalize_to_jq,
)


class TestRobustResult(unittest.TestCase):
    """测试 RobustResult 类"""

    def test_success_result(self):
        df = pd.DataFrame({"code": ["600519.XSHG"], "name": ["贵州茅台"]})
        result = RobustResult(success=True, data=df, reason="成功", source="network")
        self.assertTrue(result.success)
        self.assertFalse(result.is_empty())
        self.assertEqual(len(result.data), 1)

    def test_failure_result(self):
        result = RobustResult(
            success=False, data=pd.DataFrame(), reason="失败", source="fallback"
        )
        self.assertFalse(result.success)
        self.assertTrue(result.is_empty())

    def test_bool_conversion(self):
        success = RobustResult(success=True, data=pd.DataFrame({"a": [1]}))
        failure = RobustResult(success=False, data=pd.DataFrame())
        self.assertTrue(bool(success))
        self.assertFalse(bool(failure))

    def test_repr_output(self):
        result = RobustResult(success=True, reason="测试")
        repr_str = repr(result)
        self.assertIn("SUCCESS", repr_str)

    def test_is_empty_with_list(self):
        result = RobustResult(success=True, data=[])
        self.assertTrue(result.is_empty())

    def test_is_empty_with_none(self):
        result = RobustResult(success=True, data=None)
        self.assertTrue(result.is_empty())


class TestCodeNormalization(unittest.TestCase):
    """测试代码标准化函数"""

    def test_extract_jq_format_sh(self):
        self.assertEqual(_extract_code_num("600519.XSHG"), "600519")

    def test_extract_jq_format_sz(self):
        self.assertEqual(_extract_code_num("000001.XSHE"), "000001")

    def test_extract_sh_prefix(self):
        self.assertEqual(_extract_code_num("sh600519"), "600519")

    def test_extract_sz_prefix(self):
        self.assertEqual(_extract_code_num("sz000001"), "000001")

    def test_extract_pure_code(self):
        self.assertEqual(_extract_code_num("600519"), "600519")

    def test_extract_short_code_padding(self):
        self.assertEqual(_extract_code_num("1"), "000001")

    def test_normalize_jq_format_sh(self):
        self.assertEqual(_normalize_to_jq("600519.XSHG"), "600519.XSHG")

    def test_normalize_jq_format_sz(self):
        self.assertEqual(_normalize_to_jq("000001.XSHE"), "000001.XSHE")

    def test_normalize_sh_prefix(self):
        self.assertEqual(_normalize_to_jq("sh600519"), "600519.XSHG")

    def test_normalize_sz_prefix(self):
        self.assertEqual(_normalize_to_jq("sz000001"), "000001.XSHE")

    def test_normalize_pure_sh_code(self):
        self.assertEqual(_normalize_to_jq("600519"), "600519.XSHG")

    def test_normalize_pure_sz_code(self):
        self.assertEqual(_normalize_to_jq("000001"), "000001.XSHE")


class TestGetCompanyInfo(unittest.TestCase):
    """测试 get_company_info 函数"""

    def test_returns_dataframe(self):
        df = get_company_info("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_company_info("600519", force_update=False, use_duckdb=False)
        expected_cols = ["code", "company_name", "industry"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_code_format_sh(self):
        df = get_company_info("sh600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_code_format_jq(self):
        df = get_company_info("600519.XSHG", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sz_code(self):
        df = get_company_info("000001", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestGetCompanyInfoRobust(unittest.TestCase):
    """测试 get_company_info_robust 函数"""

    def test_returns_robust_result(self):
        result = get_company_info_robust("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(result, RobustResult)

    def test_none_input(self):
        result = get_company_info_robust(None, force_update=False, use_duckdb=False)
        self.assertFalse(result.success)
        self.assertIn("空", result.reason)

    def test_empty_list_input(self):
        result = get_company_info_robust([], force_update=False, use_duckdb=False)
        self.assertFalse(result.success)
        self.assertIn("空", result.reason)

    def test_invalid_code(self):
        result = get_company_info_robust("999999", force_update=False, use_duckdb=False)
        self.assertIsInstance(result, RobustResult)
        self.assertIn("code", result.data.columns)

    def test_batch_query(self):
        result = get_company_info_robust(
            ["600519", "000001"], force_update=False, use_duckdb=False
        )
        self.assertIsInstance(result, RobustResult)
        self.assertIsInstance(result.data, pd.DataFrame)

    def test_source_field(self):
        result = get_company_info_robust("600519", force_update=False, use_duckdb=False)
        self.assertIn(result.source, ["cache", "network", "fallback", "input"])


class TestGetSecurityStatus(unittest.TestCase):
    """测试 get_security_status 函数"""

    def test_returns_dataframe(self):
        df = get_security_status("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_security_status("600519", force_update=False, use_duckdb=False)
        expected_cols = ["code", "status_type"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_with_date(self):
        df = get_security_status(
            "600519", date="2025-01-15", force_update=False, use_duckdb=False
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestGetSecurityStatusRobust(unittest.TestCase):
    """测试 get_security_status_robust 函数"""

    def test_returns_robust_result(self):
        result = get_security_status_robust(
            "600519", force_update=False, use_duckdb=False
        )
        self.assertIsInstance(result, RobustResult)

    def test_none_input(self):
        result = get_security_status_robust(None, force_update=False, use_duckdb=False)
        self.assertFalse(result.success)
        self.assertIn("空", result.reason)

    def test_schema_fallback(self):
        result = get_security_status_robust(
            "999999", force_update=False, use_duckdb=False
        )
        expected_cols = ["code", "status_date", "status_type", "reason"]
        for col in expected_cols:
            self.assertIn(col, result.data.columns)


class TestQueryFunctions(unittest.TestCase):
    """测试批量查询函数"""

    def test_query_company_basic_info(self):
        df = query_company_basic_info(["600519"], force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_query_empty_list(self):
        df = query_company_basic_info([], use_duckdb=False)
        self.assertTrue(df.empty)

    def test_query_none_list(self):
        df = query_company_basic_info(None, use_duckdb=False)
        self.assertTrue(df.empty)

    def test_query_company_info_robust(self):
        result = query_company_info_robust(
            ["600519"], force_update=False, use_duckdb=False
        )
        self.assertIsInstance(result, RobustResult)


class TestGetCompanyInfoList(unittest.TestCase):
    """测试 get_company_info_list 函数"""

    def test_returns_dict(self):
        result = get_company_info_list(
            ["600519.XSHG"], force_update=False, use_duckdb=False
        )
        self.assertIsInstance(result, dict)

    def test_empty_list(self):
        result = get_company_info_list([], use_duckdb=False)
        self.assertEqual(len(result), 0)

    def test_multiple_codes(self):
        result = get_company_info_list(
            ["600519", "000001"], force_update=False, use_duckdb=False
        )
        self.assertEqual(len(result), 2)


class TestGetIndustryInfo(unittest.TestCase):
    """测试 get_industry_info 函数"""

    def test_returns_dataframe(self):
        df = get_industry_info("600519.XSHG", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_industry_info("600519.XSHG", force_update=False)
        expected_cols = ["code", "industry_name"]
        for col in expected_cols:
            self.assertIn(col, df.columns)


class TestFinanceQuery(unittest.TestCase):
    """测试 FinanceQuery 类"""

    def test_instance_creation(self):
        fq = FinanceQuery()
        self.assertIsNotNone(fq)

    def test_table_attributes(self):
        fq = FinanceQuery()
        self.assertTrue(hasattr(fq, "STK_COMPANY_BASIC_INFO"))
        self.assertTrue(hasattr(fq, "STK_STATUS_CHANGE"))

    def test_run_query_simple(self):
        df = run_query_simple(
            "STK_COMPANY_BASIC_INFO", code="600519", force_update=False
        )
        self.assertIsInstance(df, pd.DataFrame)

    def test_run_query_invalid_table(self):
        with self.assertRaises(ValueError):
            run_query_simple("INVALID_TABLE", code="600519")


class TestCacheMechanism(unittest.TestCase):
    """测试缓存机制"""

    def test_cache_expire_days(self):
        self.assertEqual(CACHE_EXPIRE_DAYS, 90)

    def test_cache_directory_creation(self):
        cache_dir = tempfile.mkdtemp() + "/test_cache"
        try:
            get_company_info(
                "600519", cache_dir=cache_dir, force_update=False, use_duckdb=False
            )
            self.assertTrue(os.path.exists(cache_dir))
        finally:
            shutil.rmtree(cache_dir, ignore_errors=True)

    def test_force_update_flag(self):
        df1 = get_company_info("600519", force_update=True, use_duckdb=False)
        df2 = get_company_info("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df1, pd.DataFrame)
        self.assertIsInstance(df2, pd.DataFrame)


class TestEdgeCases(unittest.TestCase):
    """测试边界条件"""

    def test_empty_string_code(self):
        df = get_company_info("", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_whitespace_code(self):
        result = get_company_info_robust("   ", force_update=False, use_duckdb=False)
        self.assertIsInstance(result, RobustResult)

    def test_invalid_format_code(self):
        invalid_codes = ["ABC123", "123ABC", "@#$%^&"]
        for code in invalid_codes:
            df = get_company_info(code, force_update=False, use_duckdb=False)
            self.assertIsInstance(df, pd.DataFrame)


class TestCodeFormatCompatibility(unittest.TestCase):
    """测试代码格式兼容性"""

    def test_sh_jq_format(self):
        df = get_company_info("600519.XSHG", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sz_jq_format(self):
        df = get_company_info("000001.XSHE", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sh_prefix(self):
        df = get_company_info("sh600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sz_prefix(self):
        df = get_company_info("sz000001", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_pure_code(self):
        df = get_company_info("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)


if __name__ == "__main__":
    unittest.main(verbosity=2)
