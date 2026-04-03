"""
test_share_change_api.py
股东变动 API 全面测试

测试覆盖:
1. 正常功能测试 - 股东变动数据获取
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
from datetime import datetime

import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.finance_data.share_change import (
    get_share_change,
    get_pledge_info,
    get_major_holder_trade,
    get_insider_trading,
    get_major_shareholder_change,
    analyze_share_change_trend,
    get_shareholder_changes,
    get_freeze_info,
    get_capital_change,
    query_share_change,
    query_pledge_data,
    query_freeze_data,
    query_capital_change,
    run_query_simple,
    RobustResult,
    SHARE_CHANGE_CACHE_DAYS,
    FinanceQuery,
    FinanceQueryEnhanced,
    FinanceQueryV2,
    FinanceQueryV3,
    _extract_code_num,
    _normalize_to_jq,
    _parse_date,
    _parse_num,
    _parse_ratio,
    _SHARE_CHANGE_SCHEMA,
    _PLEDGE_SCHEMA,
    _FREEZE_SCHEMA,
)


class TestRobustResult(unittest.TestCase):
    """测试 RobustResult 类"""

    def test_success_result(self):
        df = pd.DataFrame({"code": ["600519.XSHG"], "shareholder_name": ["股东A"]})
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


class TestGetShareChange(unittest.TestCase):
    """测试 get_share_change 函数"""

    def test_returns_dataframe(self):
        df = get_share_change("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_share_change("600519", force_update=False, use_duckdb=False)
        expected_cols = ["code", "shareholder_name"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_multiple_formats(self):
        formats = ["600519", "sh600519", "600519.XSHG"]
        for fmt in formats:
            df = get_share_change(fmt, force_update=False, use_duckdb=False)
            self.assertIsInstance(df, pd.DataFrame)

    def test_with_date_range(self):
        df = get_share_change(
            "600519",
            start_date="2024-01-01",
            end_date="2024-12-31",
            force_update=False,
            use_duckdb=False,
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestGetShareholderChanges(unittest.TestCase):
    """测试 get_shareholder_changes 函数"""

    def test_returns_robust_result(self):
        result = get_shareholder_changes(
            "600519.XSHG", force_update=False, use_duckdb=False
        )
        self.assertIsInstance(result, RobustResult)

    def test_empty_code(self):
        result = get_shareholder_changes("", force_update=False, use_duckdb=False)
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "股票代码不能为空")

    def test_none_code(self):
        result = get_shareholder_changes(None, force_update=False, use_duckdb=False)
        self.assertFalse(result.success)

    def test_source_field(self):
        result = get_shareholder_changes(
            "600519.XSHG", force_update=False, use_duckdb=False
        )
        self.assertIn(result.source, ["cache", "network", "fallback", "input"])


class TestGetPledgeInfo(unittest.TestCase):
    """测试 get_pledge_info 函数"""

    def test_returns_dataframe(self):
        df = get_pledge_info("600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_pledge_info("600519", force_update=False)
        if not df.empty:
            self.assertIn("code", df.columns)

    def test_multiple_formats(self):
        formats = ["600519", "sh600519", "600519.XSHG"]
        for fmt in formats:
            df = get_pledge_info(fmt, force_update=False)
            self.assertIsInstance(df, pd.DataFrame)


class TestGetFreezeInfo(unittest.TestCase):
    """测试 get_freeze_info 函数"""

    def test_returns_dataframe(self):
        df = get_freeze_info("600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_freeze_info("600519", force_update=False)
        if not df.empty:
            self.assertIn("code", df.columns)


class TestGetCapitalChange(unittest.TestCase):
    """测试 get_capital_change 函数"""

    def test_returns_dataframe(self):
        df = get_capital_change("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_capital_change("600519", force_update=False, use_duckdb=False)
        if not df.empty:
            self.assertIn("code", df.columns)

    def test_with_date_range(self):
        df = get_capital_change(
            "600519",
            start_date="2023-01-01",
            end_date="2024-12-31",
            force_update=False,
            use_duckdb=False,
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestGetInsiderTrading(unittest.TestCase):
    """测试 get_insider_trading 函数"""

    def test_returns_dataframe(self):
        df = get_insider_trading("600519.XSHG", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_insider_trading("600519.XSHG", force_update=False)
        if not df.empty:
            self.assertIn("code", df.columns)


class TestAnalyzeShareChangeTrend(unittest.TestCase):
    """测试 analyze_share_change_trend 函数"""

    def test_returns_dict(self):
        result = analyze_share_change_trend("600519.XSHG", force_update=False)
        self.assertIsInstance(result, dict)

    def test_required_keys(self):
        result = analyze_share_change_trend("600519.XSHG", force_update=False)
        required_keys = [
            "net_change_type",
            "total_increase_count",
            "total_decrease_count",
            "trend_signal",
            "recent_activity",
        ]
        for key in required_keys:
            self.assertIn(key, result)

    def test_net_change_type_valid(self):
        result = analyze_share_change_trend("600519.XSHG", force_update=False)
        self.assertIn(result["net_change_type"], ["增持", "减持", "持平"])

    def test_trend_signal_valid(self):
        result = analyze_share_change_trend("600519.XSHG", force_update=False)
        self.assertIn(
            result["trend_signal"], ["积极", "偏积极", "中性", "偏消极", "消极"]
        )

    def test_recent_activity_valid(self):
        result = analyze_share_change_trend("600519.XSHG", force_update=False)
        self.assertIn(result["recent_activity"], ["高", "中", "低"])

    def test_custom_period_days(self):
        result = analyze_share_change_trend(
            "600519.XSHG", period_days=180, force_update=False
        )
        self.assertEqual(result["period_days"], 180)


class TestBatchQuery(unittest.TestCase):
    """测试批量查询函数"""

    def test_query_share_change(self):
        df = query_share_change(["600519.XSHG"], force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_query_share_change_empty(self):
        df = query_share_change([], use_duckdb=False)
        self.assertTrue(df.empty)

    def test_query_share_change_none(self):
        df = query_share_change(None, use_duckdb=False)
        self.assertTrue(df.empty)

    def test_query_pledge_data(self):
        df = query_pledge_data(["600519.XSHG"], force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_query_pledge_data_empty(self):
        df = query_pledge_data([])
        self.assertTrue(df.empty)

    def test_query_freeze_data(self):
        df = query_freeze_data(["600519.XSHG"], force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_query_capital_change(self):
        df = query_capital_change(["600519.XSHG"], force_update=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestFinanceQuery(unittest.TestCase):
    """测试 FinanceQuery 类"""

    def test_instance_creation(self):
        fq = FinanceQuery()
        self.assertIsNotNone(fq)

    def test_table_attributes(self):
        fq = FinanceQuery()
        self.assertTrue(hasattr(fq, "STK_SHAREHOLDER_CHANGE"))

    def test_run_query_simple(self):
        df = run_query_simple(
            "STK_SHAREHOLDER_CHANGE", code="600519.XSHG", force_update=False
        )
        self.assertIsInstance(df, pd.DataFrame)

    def test_run_query_invalid_table(self):
        with self.assertRaises(ValueError):
            run_query_simple("INVALID_TABLE", code="600519")


class TestFinanceQueryEnhanced(unittest.TestCase):
    """测试 FinanceQueryEnhanced 类"""

    def test_instance_creation(self):
        fq = FinanceQueryEnhanced()
        self.assertIsNotNone(fq)

    def test_table_attributes(self):
        fq = FinanceQueryEnhanced()
        self.assertTrue(hasattr(fq, "STK_SHAREHOLDER_CHANGE"))


class TestFinanceQueryV2(unittest.TestCase):
    """测试 FinanceQueryV2 类"""

    def test_instance_creation(self):
        fq = FinanceQueryV2()
        self.assertIsNotNone(fq)

    def test_table_attributes(self):
        fq = FinanceQueryV2()
        self.assertTrue(hasattr(fq, "STK_SHARE_CHANGE"))
        self.assertTrue(hasattr(fq, "STK_SHAREHOLDER_CHANGE"))


class TestFinanceQueryV3(unittest.TestCase):
    """测试 FinanceQueryV3 类"""

    def test_instance_creation(self):
        fq = FinanceQueryV3()
        self.assertIsNotNone(fq)


class TestCacheMechanism(unittest.TestCase):
    """测试缓存机制"""

    def test_cache_days(self):
        self.assertEqual(SHARE_CHANGE_CACHE_DAYS, 7)

    def test_cache_directory_creation(self):
        cache_dir = tempfile.mkdtemp() + "/test_cache"
        try:
            get_share_change(
                "600519", cache_dir=cache_dir, force_update=False, use_duckdb=False
            )
            self.assertTrue(os.path.exists(cache_dir))
        finally:
            shutil.rmtree(cache_dir, ignore_errors=True)


class TestSchemaDefinitions(unittest.TestCase):
    """测试 Schema 定义"""

    def test_share_change_schema(self):
        expected = [
            "code",
            "shareholder_name",
            "change_date",
            "change_type",
            "change_amount",
            "change_ratio",
            "hold_amount_after",
            "hold_ratio_after",
        ]
        self.assertEqual(_SHARE_CHANGE_SCHEMA, expected)

    def test_pledge_schema(self):
        expected = [
            "code",
            "pledge_date",
            "pledgor",
            "pledgee",
            "pledge_amount",
            "pledge_ratio",
        ]
        self.assertEqual(_PLEDGE_SCHEMA, expected)

    def test_freeze_schema(self):
        expected = [
            "code",
            "shareholder_name",
            "freeze_amount",
            "freeze_ratio",
            "freeze_date",
            "freeze_reason",
            "freeze_type",
            "unfreeze_date",
        ]
        self.assertEqual(_FREEZE_SCHEMA, expected)


class TestEdgeCases(unittest.TestCase):
    """测试边界条件"""

    def test_invalid_code(self):
        df = get_share_change("999999", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_empty_string_code(self):
        result = get_shareholder_changes("", force_update=False, use_duckdb=False)
        self.assertFalse(result.success)

    def test_whitespace_code(self):
        df = get_share_change("   ", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestCodeFormatCompatibility(unittest.TestCase):
    """测试代码格式兼容性"""

    def test_jq_sh_format(self):
        df = get_share_change("600519.XSHG", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_jq_sz_format(self):
        df = get_share_change("000001.XSHE", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sh_prefix(self):
        df = get_share_change("sh600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sz_prefix(self):
        df = get_share_change("sz000001", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_pure_code(self):
        df = get_share_change("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestDataValidation(unittest.TestCase):
    """测试数据验证"""

    def test_change_amount_numeric(self):
        df = get_share_change("600519.XSHG", force_update=False, use_duckdb=False)
        if not df.empty and "change_amount" in df.columns:
            amounts = df["change_amount"].dropna()
            for amt in amounts:
                self.assertTrue(isinstance(amt, (int, float)) or pd.isna(amt))

    def test_code_format_consistency(self):
        df = get_share_change("600519", force_update=False, use_duckdb=False)
        if not df.empty and "code" in df.columns:
            codes = df["code"].unique()
            for code in codes:
                self.assertTrue(".XSHG" in code or ".XSHE" in code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
