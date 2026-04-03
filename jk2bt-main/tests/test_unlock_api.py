"""
test_unlock_api.py
限售解禁 API 全面测试

测试覆盖:
1. 正常功能测试 - 解禁信息获取
2. 边界条件测试 - 空输入、None输入、无效代码
3. 异常处理测试 - 网络失败、数据缺失
4. 缓存机制测试 - 7天缓存策略
5. RobustResult 测试 - success/data/reason/source 验证
6. 批量查询测试 - 多股票查询
7. 代码格式兼容测试 - .XSHG/.XSHE/sh/sz/纯数字
"""

import unittest
import pandas as pd
import os
import tempfile
import shutil
from datetime import datetime, timedelta

import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.finance_data.unlock import (
    get_unlock,
    get_unlock_info,
    get_unlock_info_batch,
    get_unlock_schedule,
    get_unlock_pressure,
    get_unlock_calendar,
    get_upcoming_unlocks,
    get_unlock_history,
    analyze_unlock_impact,
    query_unlock,
    query_lock_share,
    RobustResult,
    UNLOCK_CACHE_DAYS,
    FinanceQuery,
    run_query_simple,
    finance,
    _UNLOCK_SCHEMA,
    _LOCK_SHARE_SCHEMA,
    _extract_code_num,
    _normalize_to_jq,
    _parse_date,
    _parse_num,
    _parse_ratio,
    _filter_by_date_range,
)


class TestRobustResult(unittest.TestCase):
    """测试 RobustResult 类"""

    def test_success_result(self):
        df = pd.DataFrame({"code": ["600519.XSHG"], "unlock_date": ["2024-01-01"]})
        result = RobustResult(success=True, data=df, reason="成功", source="network")
        self.assertTrue(result.success)
        self.assertFalse(result.is_empty())

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


class TestCodeNormalization(unittest.TestCase):
    """测试代码标准化函数"""

    def test_extract_jq_sh(self):
        self.assertEqual(_extract_code_num("600519.XSHG"), "600519")

    def test_extract_jq_sz(self):
        self.assertEqual(_extract_code_num("000001.XSHE"), "000001")

    def test_extract_sh_prefix(self):
        self.assertEqual(_extract_code_num("sh600519"), "600519")

    def test_extract_sz_prefix(self):
        self.assertEqual(_extract_code_num("sz000001"), "000001")

    def test_extract_pure_code(self):
        self.assertEqual(_extract_code_num("600519"), "600519")

    def test_normalize_jq_sh(self):
        self.assertEqual(_normalize_to_jq("600519.XSHG"), "600519.XSHG")

    def test_normalize_jq_sz(self):
        self.assertEqual(_normalize_to_jq("000001.XSHE"), "000001.XSHE")

    def test_normalize_sh_prefix(self):
        self.assertEqual(_normalize_to_jq("sh600519"), "600519.XSHG")

    def test_normalize_sz_prefix(self):
        self.assertEqual(_normalize_to_jq("sz000001"), "000001.XSHE")

    def test_normalize_pure_sh(self):
        self.assertEqual(_normalize_to_jq("600519"), "600519.XSHG")

    def test_normalize_pure_sz(self):
        self.assertEqual(_normalize_to_jq("000001"), "000001.XSHE")


class TestParseFunctions(unittest.TestCase):
    """测试解析函数"""

    def test_parse_date_standard(self):
        result = _parse_date("2024-01-15")
        self.assertEqual(result, "2024-01-15")

    def test_parse_date_compact(self):
        result = _parse_date("20240115")
        self.assertEqual(result, "2024-01-15")

    def test_parse_date_slash(self):
        result = _parse_date("2024/01/15")
        self.assertEqual(result, "2024-01-15")

    def test_parse_date_invalid(self):
        result = _parse_date("invalid")
        self.assertIsNone(result)

    def test_parse_date_empty(self):
        result = _parse_date("")
        self.assertIsNone(result)

    def test_parse_date_none(self):
        result = _parse_date(None)
        self.assertIsNone(result)

    def test_parse_num_integer(self):
        result = _parse_num(12345)
        self.assertEqual(result, 12345)

    def test_parse_num_string(self):
        result = _parse_num("12345")
        self.assertEqual(result, 12345)

    def test_parse_num_with_comma(self):
        result = _parse_num("12,345")
        self.assertEqual(result, 12345)

    def test_parse_num_empty(self):
        result = _parse_num("")
        self.assertIsNone(result)

    def test_parse_ratio_decimal(self):
        result = _parse_ratio(0.05)
        self.assertEqual(result, 0.05)

    def test_parse_ratio_percentage(self):
        result = _parse_ratio("5%")
        self.assertEqual(result, 0.05)


class TestGetUnlock(unittest.TestCase):
    """测试 get_unlock 函数"""

    def test_returns_dataframe(self):
        df = get_unlock("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_unlock("600519", force_update=False, use_duckdb=False)
        expected_cols = ["code", "unlock_date"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_multiple_formats(self):
        formats = ["600519", "sh600519", "600519.XSHG"]
        for fmt in formats:
            df = get_unlock(fmt, force_update=False, use_duckdb=False)
            self.assertIsInstance(df, pd.DataFrame)

    def test_with_date_range(self):
        df = get_unlock(
            "600519",
            start_date="2020-01-01",
            end_date="2025-12-31",
            force_update=False,
            use_duckdb=False,
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestGetUnlockInfo(unittest.TestCase):
    """测试 get_unlock_info 函数"""

    def test_returns_robust_result(self):
        result = get_unlock_info("600519", force_update=False)
        self.assertIsInstance(result, RobustResult)

    def test_source_field(self):
        result = get_unlock_info("600519", force_update=False)
        self.assertIn(result.source, ["cache", "network", "fallback", "input"])

    def test_multiple_formats(self):
        formats = ["600519", "sh600519", "600519.XSHG"]
        for fmt in formats:
            result = get_unlock_info(fmt, force_update=False)
            self.assertIsInstance(result, RobustResult)

    def test_with_date_range(self):
        result = get_unlock_info(
            "600519", start_date="2020-01-01", end_date="2025-12-31", force_update=False
        )
        self.assertIsInstance(result, RobustResult)


class TestGetUnlockInfoBatch(unittest.TestCase):
    """测试 get_unlock_info_batch 函数"""

    def test_returns_robust_result(self):
        result = get_unlock_info_batch(["600519"], force_update=False)
        self.assertIsInstance(result, RobustResult)

    def test_empty_codes(self):
        result = get_unlock_info_batch([])
        self.assertFalse(result.success)
        self.assertIn("空", result.reason)

    def test_multiple_codes(self):
        result = get_unlock_info_batch(["600519", "000001"], force_update=False)
        self.assertIsInstance(result, RobustResult)

    def test_with_date_range(self):
        result = get_unlock_info_batch(
            ["600519"],
            start_date="2024-01-01",
            end_date="2025-12-31",
            force_update=False,
        )
        self.assertIsInstance(result, RobustResult)


class TestGetUnlockSchedule(unittest.TestCase):
    """测试 get_unlock_schedule 函数"""

    def test_returns_dataframe(self):
        df = get_unlock_schedule("600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_with_date_range(self):
        df = get_unlock_schedule(
            "600519", start_date="2020-01-01", end_date="2025-12-31", force_update=False
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestGetUnlockPressure(unittest.TestCase):
    """测试 get_unlock_pressure 函数"""

    def test_returns_dict(self):
        result = get_unlock_pressure("600519", days_ahead=365, force_update=False)
        self.assertIsInstance(result, dict)

    def test_required_keys(self):
        result = get_unlock_pressure("600519", days_ahead=365, force_update=False)
        required_keys = [
            "code",
            "total_unlock_amount",
            "total_unlock_value",
            "pressure_level",
        ]
        for key in required_keys:
            self.assertIn(key, result)

    def test_pressure_level_valid(self):
        result = get_unlock_pressure("600519", days_ahead=365, force_update=False)
        self.assertIn(result["pressure_level"], ["none", "low", "medium", "high"])

    def test_different_days_ahead(self):
        result_30 = get_unlock_pressure("600519", days_ahead=30, force_update=False)
        result_90 = get_unlock_pressure("600519", days_ahead=90, force_update=False)
        self.assertIsInstance(result_30, dict)
        self.assertIsInstance(result_90, dict)


class TestGetUnlockCalendar(unittest.TestCase):
    """测试 get_unlock_calendar 函数"""

    def test_returns_dataframe(self):
        df = get_unlock_calendar(date="2025-01-15", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_different_dates(self):
        dates = ["2025-01-15", "2025-02-20", "2025-03-15"]
        for date in dates:
            df = get_unlock_calendar(date=date, force_update=False)
            self.assertIsInstance(df, pd.DataFrame)


class TestGetUpcomingUnlocks(unittest.TestCase):
    """测试 get_upcoming_unlocks 函数"""

    def test_returns_dataframe(self):
        df = get_upcoming_unlocks(days=30, force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_different_days(self):
        df_7 = get_upcoming_unlocks(days=7, force_update=False)
        df_60 = get_upcoming_unlocks(days=60, force_update=False)
        self.assertIsInstance(df_7, pd.DataFrame)
        self.assertIsInstance(df_60, pd.DataFrame)

    def test_schema_columns(self):
        df = get_upcoming_unlocks(days=30, force_update=False)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("unlock_date", df.columns)


class TestGetUnlockHistory(unittest.TestCase):
    """测试 get_unlock_history 函数"""

    def test_returns_dataframe(self):
        df = get_unlock_history("600519", years=3, force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_different_years(self):
        df_1 = get_unlock_history("600519", years=1, force_update=False)
        df_5 = get_unlock_history("600519", years=5, force_update=False)
        self.assertIsInstance(df_1, pd.DataFrame)
        self.assertIsInstance(df_5, pd.DataFrame)


class TestAnalyzeUnlockImpact(unittest.TestCase):
    """测试 analyze_unlock_impact 函数"""

    def test_returns_dict(self):
        result = analyze_unlock_impact("600519", force_update=False)
        self.assertIsInstance(result, dict)

    def test_required_keys(self):
        result = analyze_unlock_impact("600519", force_update=False)
        required_keys = [
            "code",
            "upcoming_unlocks",
            "total_unlock_amount",
            "avg_unlock_ratio",
            "impact_level",
            "risk_factors",
        ]
        for key in required_keys:
            self.assertIn(key, result)

    def test_impact_level_valid(self):
        result = analyze_unlock_impact("600519", force_update=False)
        self.assertIn(result["impact_level"], ["high", "medium", "low", "none"])

    def test_risk_factors_is_list(self):
        result = analyze_unlock_impact("600519", force_update=False)
        self.assertIsInstance(result["risk_factors"], list)


class TestQueryUnlock(unittest.TestCase):
    """测试 query_unlock 函数"""

    def test_batch_query(self):
        df = query_unlock(["600519"], force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_empty_list(self):
        df = query_unlock([], use_duckdb=False)
        self.assertTrue(df.empty)

    def test_none_list(self):
        df = query_unlock(None, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_multiple_codes(self):
        df = query_unlock(["600519", "000001"], force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_with_date_range(self):
        df = query_unlock(
            ["600519"],
            start_date="2020-01-01",
            end_date="2025-12-31",
            force_update=False,
            use_duckdb=False,
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestFinanceQuery(unittest.TestCase):
    """测试 FinanceQuery 类"""

    def test_instance_creation(self):
        fq = FinanceQuery()
        self.assertIsNotNone(fq)

    def test_table_attributes(self):
        fq = FinanceQuery()
        self.assertTrue(hasattr(fq, "STK_RESTRICTED_RELEASE"))
        self.assertTrue(hasattr(fq, "STK_UNLOCK_INFO"))
        self.assertTrue(hasattr(fq, "STK_LOCK_UNLOCK"))
        self.assertTrue(hasattr(fq, "STK_UNLOCK_DATE"))
        self.assertTrue(hasattr(fq, "STK_LOCK_SHARE"))

    def test_run_query_simple(self):
        df = run_query_simple(
            "STK_RESTRICTED_RELEASE", code="600519", force_update=False
        )
        self.assertIsInstance(df, pd.DataFrame)

    def test_run_query_invalid_table(self):
        with self.assertRaises(ValueError):
            run_query_simple("INVALID_TABLE", code="600519")

    def test_global_finance_instance(self):
        self.assertIsNotNone(finance)

    def test_stk_unlock_date_alias(self):
        fq = FinanceQuery()
        self.assertTrue(hasattr(fq, "STK_UNLOCK_DATE"))
        self.assertTrue(hasattr(fq.STK_UNLOCK_DATE, "code"))

    def test_stk_lock_share_table(self):
        fq = FinanceQuery()
        self.assertTrue(hasattr(fq, "STK_LOCK_SHARE"))
        self.assertTrue(hasattr(fq.STK_LOCK_SHARE, "lock_amount"))


class TestQueryLockShare(unittest.TestCase):
    """测试 query_lock_share 函数"""

    def test_returns_dataframe(self):
        df = query_lock_share("600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = query_lock_share("600519", force_update=False)
        expected_cols = ["code", "unlock_date", "lock_amount"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_multiple_formats(self):
        formats = ["600519", "sh600519", "600519.XSHG"]
        for fmt in formats:
            df = query_lock_share(fmt, force_update=False)
            self.assertIsInstance(df, pd.DataFrame)

    def test_empty_result_schema(self):
        df = query_lock_share("999999", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)
        if df.empty:
            self.assertEqual(list(df.columns), _LOCK_SHARE_SCHEMA)


class TestCacheMechanism(unittest.TestCase):
    """测试缓存机制"""

    def test_cache_days(self):
        self.assertEqual(UNLOCK_CACHE_DAYS, 7)

    def test_cache_directory_creation(self):
        cache_dir = tempfile.mkdtemp() + "/test_cache"
        try:
            get_unlock(
                "600519", cache_dir=cache_dir, force_update=False, use_duckdb=False
            )
            self.assertTrue(os.path.exists(cache_dir))
        finally:
            shutil.rmtree(cache_dir, ignore_errors=True)


class TestFilterByDateRange(unittest.TestCase):
    """测试日期范围筛选函数"""

    def test_filter_empty_df(self):
        df = pd.DataFrame()
        result = _filter_by_date_range(df, "2024-01-01", "2024-12-31")
        self.assertTrue(result.empty)

    def test_filter_with_dates(self):
        df = pd.DataFrame(
            {
                "code": ["600519.XSHG", "600519.XSHG"],
                "unlock_date": ["2024-01-01", "2024-06-01"],
                "unlock_amount": [1000000, 2000000],
            }
        )
        filtered = _filter_by_date_range(df, "2024-03-01", "2024-12-31")
        self.assertEqual(len(filtered), 1)


class TestSchemaDefinition(unittest.TestCase):
    """测试 Schema 定义"""

    def test_unlock_schema(self):
        expected = [
            "code",
            "unlock_date",
            "unlock_amount",
            "unlock_ratio",
            "unlock_type",
            "holder_type",
        ]
        self.assertEqual(_UNLOCK_SCHEMA, expected)

    def test_lock_share_schema(self):
        expected = [
            "code",
            "unlock_date",
            "lock_amount",
            "lock_type",
            "shareholder_name",
            "shareholder_type",
        ]
        self.assertEqual(_LOCK_SHARE_SCHEMA, expected)


class TestEdgeCases(unittest.TestCase):
    """测试边界条件"""

    def test_invalid_code(self):
        df = get_unlock("999999", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_empty_string_code(self):
        df = get_unlock("", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_future_date_range(self):
        df = get_unlock(
            "600519",
            start_date="2030-01-01",
            end_date="2030-12-31",
            force_update=False,
            use_duckdb=False,
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestCodeFormatCompatibility(unittest.TestCase):
    """测试代码格式兼容性"""

    def test_jq_sh_format(self):
        df = get_unlock("600519.XSHG", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_jq_sz_format(self):
        df = get_unlock("000001.XSHE", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sh_prefix(self):
        df = get_unlock("sh600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sz_prefix(self):
        df = get_unlock("sz000001", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_pure_code(self):
        df = get_unlock("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestDataValidation(unittest.TestCase):
    """测试数据验证"""

    def test_unlock_amount_non_negative(self):
        df = get_unlock("600519", force_update=False, use_duckdb=False)
        if not df.empty and "unlock_amount" in df.columns:
            amounts = df["unlock_amount"].dropna()
            for amt in amounts:
                self.assertGreaterEqual(amt, 0)

    def test_unlock_ratio_range(self):
        df = get_unlock("600519", force_update=False, use_duckdb=False)
        if not df.empty and "unlock_ratio" in df.columns:
            ratios = df["unlock_ratio"].dropna()
            for r in ratios:
                self.assertGreaterEqual(r, 0)

    def test_code_format_consistency(self):
        df = get_unlock("600519", force_update=False, use_duckdb=False)
        if not df.empty and "code" in df.columns:
            codes = df["code"].unique()
            for code in codes:
                self.assertTrue(".XSHG" in code or ".XSHE" in code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
