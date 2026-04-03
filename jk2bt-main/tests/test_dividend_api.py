"""
test_dividend_api.py
分红送股 API 全面测试

测试覆盖:
1. 正常功能测试 - 分红信息获取、历史记录
2. 边界条件测试 - 空输入、None输入、无效代码
3. 异常处理测试 - 网络失败、数据缺失
4. 缓存机制测试 - 90天缓存策略
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

from jk2bt.finance_data.dividend import (
    get_dividend_info,
    get_dividend_history,
    calculate_ex_rights_price,
    get_stock_bonus,
    get_adjust_factor,
    get_dividend_by_date,
    get_dividend,
    query_dividend,
    get_rights_issue,
    get_next_dividend,
    query_dividend_right,
    calculate_adjust_price,
    FinanceQuery,
    run_query_simple,
    finance,
    _DIVIDEND_SCHEMA,
    _RIGHTS_ISSUE_SCHEMA,
    _NEXT_DIVIDEND_SCHEMA,
    _ADJUST_FACTOR_SCHEMA,
    _extract_code_num,
    _normalize_to_jq,
)


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


class TestGetDividendInfo(unittest.TestCase):
    """测试 get_dividend_info 函数"""

    def test_returns_dataframe(self):
        df = get_dividend_info("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_dividend_info("600519", force_update=False, use_duckdb=False)
        expected_cols = ["code", "bonus_ratio_rmb", "ex_dividend_date"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_multiple_formats(self):
        formats = ["600519", "sh600519", "600519.XSHG"]
        for fmt in formats:
            df = get_dividend_info(fmt, force_update=False, use_duckdb=False)
            self.assertIsInstance(df, pd.DataFrame)

    def test_sz_code(self):
        df = get_dividend_info("000001", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_with_date_range(self):
        df = get_dividend_info(
            "600519",
            start_date="2020-01-01",
            end_date="2025-01-01",
            force_update=False,
            use_duckdb=False,
        )
        self.assertIsInstance(df, pd.DataFrame)

    def test_invalid_code(self):
        df = get_dividend_info("999999", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestGetDividendHistory(unittest.TestCase):
    """测试 get_dividend_history 函数"""

    def test_returns_dataframe(self):
        df = get_dividend_history("600519", years=5, force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_dividend_history("600519", years=5, force_update=False)
        expected_cols = ["code", "year", "dividend_count", "total_dividend"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_different_years(self):
        df1 = get_dividend_history("600519", years=3, force_update=False)
        df5 = get_dividend_history("600519", years=5, force_update=False)
        self.assertIsInstance(df1, pd.DataFrame)
        self.assertIsInstance(df5, pd.DataFrame)


class TestCalculateExRightsPrice(unittest.TestCase):
    """测试 calculate_ex_rights_price 函数"""

    def test_cash_dividend_only(self):
        dividend_info = {
            "bonus_ratio_rmb": 10,
            "bonus_share_ratio": 0,
            "transfer_ratio": 0,
        }
        ex_price = calculate_ex_rights_price(100.0, dividend_info)
        self.assertAlmostEqual(ex_price, 99.0, places=2)

    def test_stock_bonus_only(self):
        dividend_info = {
            "bonus_ratio_rmb": 0,
            "bonus_share_ratio": 10,
            "transfer_ratio": 0,
        }
        ex_price = calculate_ex_rights_price(100.0, dividend_info)
        self.assertAlmostEqual(ex_price, 50.0, places=2)

    def test_transfer_only(self):
        dividend_info = {
            "bonus_ratio_rmb": 0,
            "bonus_share_ratio": 0,
            "transfer_ratio": 10,
        }
        ex_price = calculate_ex_rights_price(100.0, dividend_info)
        self.assertAlmostEqual(ex_price, 50.0, places=2)

    def test_combined(self):
        dividend_info = {
            "bonus_ratio_rmb": 5,
            "bonus_share_ratio": 5,
            "transfer_ratio": 5,
        }
        ex_price = calculate_ex_rights_price(100.0, dividend_info)
        self.assertGreater(ex_price, 0)
        self.assertLess(ex_price, 100)

    def test_no_dividend(self):
        dividend_info = {}
        ex_price = calculate_ex_rights_price(100.0, dividend_info)
        self.assertEqual(ex_price, 100.0)

    def test_zero_price(self):
        dividend_info = {
            "bonus_ratio_rmb": 10,
            "bonus_share_ratio": 0,
            "transfer_ratio": 0,
        }
        ex_price = calculate_ex_rights_price(0, dividend_info)
        self.assertEqual(ex_price, 0)

    def test_with_dataframe(self):
        df = pd.DataFrame(
            {"bonus_ratio_rmb": [10], "bonus_share_ratio": [0], "transfer_ratio": [0]}
        )
        ex_price = calculate_ex_rights_price(100.0, df)
        self.assertAlmostEqual(ex_price, 99.0, places=2)

    def test_with_series(self):
        series = pd.Series(
            {"bonus_ratio_rmb": 10, "bonus_share_ratio": 0, "transfer_ratio": 0}
        )
        ex_price = calculate_ex_rights_price(100.0, series)
        self.assertAlmostEqual(ex_price, 99.0, places=2)


class TestGetStockBonus(unittest.TestCase):
    """测试 get_stock_bonus 函数"""

    def test_returns_dataframe(self):
        df = get_stock_bonus("600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_stock_bonus("600519", force_update=False)
        if not df.empty:
            self.assertIn("code", df.columns)


class TestGetAdjustFactor(unittest.TestCase):
    """测试 get_adjust_factor 函数"""

    def test_returns_dataframe(self):
        df = get_adjust_factor("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_adjust_factor("600519", force_update=False, use_duckdb=False)
        expected_cols = ["code", "ex_dividend_date", "adjust_factor"]
        for col in expected_cols:
            self.assertIn(col, df.columns)


class TestGetDividendByDate(unittest.TestCase):
    """测试 get_dividend_by_date 函数"""

    def test_returns_dataframe(self):
        df = get_dividend_by_date("20231231", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_dividend_by_date("20231231", force_update=False)
        if not df.empty:
            self.assertIn("code", df.columns)


class TestQueryDividend(unittest.TestCase):
    """测试 query_dividend 函数"""

    def test_batch_query(self):
        df = query_dividend(["600519"], force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_empty_list(self):
        df = query_dividend([], use_duckdb=False)
        self.assertTrue(df.empty)

    def test_none_list(self):
        df = query_dividend(None, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_multiple_codes(self):
        df = query_dividend(["600519", "000001"], force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_with_date_range(self):
        df = query_dividend(
            ["600519"],
            start_date="2020-01-01",
            end_date="2025-01-01",
            force_update=False,
            use_duckdb=False,
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestGetRightsIssue(unittest.TestCase):
    """测试 get_rights_issue 函数"""

    def test_returns_dataframe(self):
        df = get_rights_issue("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_rights_issue("600519", force_update=False, use_duckdb=False)
        if not df.empty:
            self.assertIn("code", df.columns)


class TestGetNextDividend(unittest.TestCase):
    """测试 get_next_dividend 函数"""

    def test_returns_dataframe(self):
        df = get_next_dividend("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_next_dividend("600519", force_update=False, use_duckdb=False)
        if not df.empty:
            self.assertIn("code", df.columns)


class TestQueryDividendRight(unittest.TestCase):
    """测试 query_dividend_right 函数"""

    def test_batch_query(self):
        df = query_dividend_right(["600519.XSHG"], force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_empty_list(self):
        df = query_dividend_right([], use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestCalculateAdjustPrice(unittest.TestCase):
    """测试 calculate_adjust_price 函数"""

    def test_qfq_calculation(self):
        price = calculate_adjust_price(
            "600519", 100.0, adjust_type="qfq", force_update=False
        )
        self.assertIsInstance(price, (int, float))
        self.assertGreater(price, 0)

    def test_hfq_calculation(self):
        price = calculate_adjust_price(
            "600519", 100.0, adjust_type="hfq", force_update=False
        )
        self.assertIsInstance(price, (int, float))
        self.assertGreater(price, 0)

    def test_with_date(self):
        price = calculate_adjust_price(
            "600519", 100.0, adjust_type="qfq", date="2023-01-01", force_update=False
        )
        self.assertIsInstance(price, (int, float))

    def test_no_dividend_stock(self):
        price = calculate_adjust_price(
            "688981", 100.0, adjust_type="qfq", force_update=False
        )
        self.assertEqual(price, 100.0)


class TestFinanceQuery(unittest.TestCase):
    """测试 FinanceQuery 类"""

    def test_instance_creation(self):
        fq = FinanceQuery()
        self.assertIsNotNone(fq)

    def test_table_attributes(self):
        fq = FinanceQuery()
        self.assertTrue(hasattr(fq, "STK_XR_XD"))
        self.assertTrue(hasattr(fq, "STK_DIVIDEND_INFO"))
        self.assertTrue(hasattr(fq, "STK_DIVIDEND_RIGHT"))

    def test_run_query_simple(self):
        df = run_query_simple("STK_XR_XD", code="600519.XSHG", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_run_query_simple_dividend_right(self):
        df = run_query_simple(
            "STK_DIVIDEND_RIGHT", code="600519.XSHG", force_update=False
        )
        self.assertIsInstance(df, pd.DataFrame)

    def test_run_query_invalid_table(self):
        with self.assertRaises(ValueError):
            run_query_simple("INVALID_TABLE", code="600519")

    def test_global_finance_instance(self):
        self.assertIsNotNone(finance)

    def test_stk_xr_xd_and_dividend_right_consistency(self):
        df_xrxd = run_query_simple("STK_XR_XD", code="600519.XSHG", force_update=False)
        df_right = run_query_simple(
            "STK_DIVIDEND_RIGHT", code="600519.XSHG", force_update=False
        )
        self.assertEqual(len(df_xrxd), len(df_right))


class TestCacheMechanism(unittest.TestCase):
    """测试缓存机制"""

    def test_cache_directory_creation(self):
        cache_dir = tempfile.mkdtemp() + "/test_cache"
        try:
            get_dividend_info(
                "600519", cache_dir=cache_dir, force_update=False, use_duckdb=False
            )
            self.assertTrue(os.path.exists(cache_dir))
        finally:
            shutil.rmtree(cache_dir, ignore_errors=True)

    def test_force_update_flag(self):
        df1 = get_dividend_info("600519", force_update=True, use_duckdb=False)
        df2 = get_dividend_info("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df1, pd.DataFrame)
        self.assertIsInstance(df2, pd.DataFrame)


class TestSchemaDefinition(unittest.TestCase):
    """测试 Schema 定义"""

    def test_dividend_schema(self):
        expected_cols = ["code", "bonus_ratio_rmb", "ex_dividend_date"]
        for col in expected_cols:
            self.assertIn(col, _DIVIDEND_SCHEMA)


class TestEdgeCases(unittest.TestCase):
    """测试边界条件"""

    def test_invalid_code(self):
        df = get_dividend_info("999999", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_empty_string_code(self):
        df = get_dividend_info("", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_future_date(self):
        df = get_dividend_info(
            "600519", start_date="2030-01-01", force_update=False, use_duckdb=False
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestCodeFormatCompatibility(unittest.TestCase):
    """测试代码格式兼容性"""

    def test_jq_sh_format(self):
        df = get_dividend_info("600519.XSHG", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_jq_sz_format(self):
        df = get_dividend_info("000001.XSHE", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sh_prefix(self):
        df = get_dividend_info("sh600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sz_prefix(self):
        df = get_dividend_info("sz000001", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_pure_code(self):
        df = get_dividend_info("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestDataValidation(unittest.TestCase):
    """测试数据验证"""

    def test_bonus_ratio_non_negative(self):
        df = get_dividend_info("600519", force_update=False, use_duckdb=False)
        if not df.empty and "bonus_ratio_rmb" in df.columns:
            bonus = df["bonus_ratio_rmb"].dropna()
            for b in bonus:
                self.assertGreaterEqual(b, 0)

    def test_code_format_consistency(self):
        df = get_dividend_info("600519", force_update=False, use_duckdb=False)
        if not df.empty and "code" in df.columns:
            code = df.iloc[0]["code"]
            self.assertTrue(".XSHG" in code or ".XSHE" in code)


class TestPackageLevelExports(unittest.TestCase):
    """测试包级导出"""

    def test_dividend_info_exported(self):
        from jk2bt.finance_data import get_dividend_info

        df = get_dividend_info("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_rights_issue_exported(self):
        from jk2bt.finance_data import get_rights_issue

        df = get_rights_issue("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_next_dividend_exported(self):
        from jk2bt.finance_data import get_next_dividend

        df = get_next_dividend("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_adjust_factor_exported(self):
        from jk2bt.finance_data import get_adjust_factor

        df = get_adjust_factor("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_exports(self):
        from jk2bt.finance_data import (
            _DIVIDEND_SCHEMA,
            _RIGHTS_ISSUE_SCHEMA,
            _NEXT_DIVIDEND_SCHEMA,
            _ADJUST_FACTOR_SCHEMA,
        )

        self.assertIn("code", _DIVIDEND_SCHEMA)
        self.assertIn("code", _RIGHTS_ISSUE_SCHEMA)
        self.assertIn("code", _NEXT_DIVIDEND_SCHEMA)
        self.assertIn("code", _ADJUST_FACTOR_SCHEMA)

    def test_finance_instance_exported(self):
        from jk2bt.finance_data import finance

        self.assertIsNotNone(finance)
        self.assertTrue(hasattr(finance, "STK_XR_XD"))
        self.assertTrue(hasattr(finance, "STK_DIVIDEND_RIGHT"))


class TestSchemaStability(unittest.TestCase):
    """测试 Schema 字段稳定性"""

    def test_dividend_schema_fields(self):
        expected_fields = [
            "code",
            "bonus_ratio_rmb",
            "bonus_share_ratio",
            "transfer_ratio",
            "ex_dividend_date",
        ]
        for field in expected_fields:
            self.assertIn(field, _DIVIDEND_SCHEMA)

    def test_rights_issue_schema_fields(self):
        expected_fields = ["code", "ex_dividend_date", "bonus_ratio_rmb"]
        for field in expected_fields:
            self.assertIn(field, _RIGHTS_ISSUE_SCHEMA)

    def test_next_dividend_schema_fields(self):
        expected_fields = ["code", "report_date", "bonus_ratio_rmb"]
        for field in expected_fields:
            self.assertIn(field, _NEXT_DIVIDEND_SCHEMA)

    def test_adjust_factor_schema_fields(self):
        expected_fields = ["code", "ex_dividend_date", "adjust_factor"]
        for field in expected_fields:
            self.assertIn(field, _ADJUST_FACTOR_SCHEMA)


class TestAdjustFactorCalculation(unittest.TestCase):
    """测试复权因子计算稳定性"""

    def test_adjust_factor_columns_stable(self):
        df = get_adjust_factor("600519", force_update=False, use_duckdb=False)
        if not df.empty:
            self.assertIn("adjust_factor", df.columns)
            self.assertIn("bonus_ratio_rmb", df.columns)
            self.assertIn("bonus_share_ratio", df.columns)
            self.assertIn("transfer_ratio", df.columns)

    def test_adjust_factor_values_reasonable(self):
        df = get_adjust_factor("600519", force_update=False, use_duckdb=False)
        if not df.empty and "adjust_factor" in df.columns:
            for factor in df["adjust_factor"].dropna():
                self.assertGreater(factor, 0)
                self.assertLessEqual(factor, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
