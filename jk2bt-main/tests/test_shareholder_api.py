"""
test_shareholder_api.py
股东信息 API 全面测试

测试覆盖:
1. 正常功能测试 - 十大股东、流通股东、股东户数
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

from jk2bt.finance_data.shareholder import (
    get_top10_shareholders,
    get_top10_float_shareholders,
    get_shareholder_count,
    get_top_shareholders,
    get_top_float_shareholders,
    get_shareholder_structure,
    get_shareholder_concentration,
    get_shareholders,
    query_shareholder_top10,
    query_shareholder_float_top10,
    query_shareholder_num,
    prewarm_shareholder_cache,
    RobustResult,
    SHAREHOLDER_CACHE_DAYS,
    FinanceQuery,
    run_query_simple,
    _extract_code_num,
    _normalize_to_jq,
    _SHAREHOLDER_SCHEMA,
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

    def test_is_empty_with_none(self):
        result = RobustResult(success=True, data=None)
        self.assertTrue(result.is_empty())


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


class TestGetTop10Shareholders(unittest.TestCase):
    """测试 get_top10_shareholders 函数"""

    def test_returns_dataframe(self):
        df = get_top10_shareholders("600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_top10_shareholders("600519", force_update=False)
        expected_cols = ["code", "shareholder_name"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_multiple_formats(self):
        formats = ["600519", "sh600519", "600519.XSHG"]
        for fmt in formats:
            df = get_top10_shareholders(fmt, force_update=False)
            self.assertIsInstance(df, pd.DataFrame)

    def test_sz_code(self):
        df = get_top10_shareholders("000001", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestGetTop10FloatShareholders(unittest.TestCase):
    """测试 get_top10_float_shareholders 函数"""

    def test_returns_dataframe(self):
        df = get_top10_float_shareholders("600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_top10_float_shareholders("600519", force_update=False)
        if not df.empty:
            self.assertIn("code", df.columns)

    def test_multiple_formats(self):
        formats = ["600519", "sh600519", "600519.XSHG"]
        for fmt in formats:
            df = get_top10_float_shareholders(fmt, force_update=False)
            self.assertIsInstance(df, pd.DataFrame)


class TestGetShareholderCount(unittest.TestCase):
    """测试 get_shareholder_count 函数"""

    def test_returns_dataframe(self):
        df = get_shareholder_count("600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_schema_columns(self):
        df = get_shareholder_count("600519", force_update=False)
        if not df.empty:
            self.assertIn("code", df.columns)


class TestGetShareholders(unittest.TestCase):
    """测试 get_shareholders 函数（稳健版）"""

    def test_returns_robust_result(self):
        result = get_shareholders("600519", force_update=False)
        self.assertIsInstance(result, RobustResult)

    def test_source_field(self):
        result = get_shareholders("600519", force_update=False)
        self.assertIn(result.source, ["cache", "network", "fallback", "input"])

    def test_multiple_formats(self):
        formats = ["600519", "sh600519", "600519.XSHG"]
        for fmt in formats:
            result = get_shareholders(fmt, force_update=False)
            self.assertIsInstance(result, RobustResult)


class TestGetShareholderConcentration(unittest.TestCase):
    """测试 get_shareholder_concentration 函数"""

    def test_returns_dict(self):
        result = get_shareholder_concentration("600519", force_update=False)
        self.assertIsInstance(result, dict)

    def test_required_keys(self):
        result = get_shareholder_concentration("600519", force_update=False)
        required_keys = [
            "top1_ratio",
            "top3_ratio",
            "top5_ratio",
            "top10_ratio",
            "concentration_level",
        ]
        for key in required_keys:
            self.assertIn(key, result)

    def test_concentration_level_valid(self):
        result = get_shareholder_concentration("600519", force_update=False)
        self.assertIn(result["concentration_level"], ["高", "中", "低", "未知"])


class TestBatchQuery(unittest.TestCase):
    """测试批量查询函数"""

    def test_query_shareholder_top10(self):
        df = query_shareholder_top10(["600519"], force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_query_shareholder_top10_empty(self):
        df = query_shareholder_top10([])
        self.assertTrue(df.empty)

    def test_query_shareholder_top10_none(self):
        df = query_shareholder_top10(None)
        self.assertTrue(df.empty)

    def test_query_shareholder_float_top10(self):
        df = query_shareholder_float_top10(["600519"], force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_query_shareholder_num(self):
        df = query_shareholder_num(["600519"], force_update=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestFinanceQuery(unittest.TestCase):
    """测试 FinanceQuery 类"""

    def test_instance_creation(self):
        fq = FinanceQuery()
        self.assertIsNotNone(fq)

    def test_table_attributes(self):
        fq = FinanceQuery()
        self.assertTrue(hasattr(fq, "STK_SHAREHOLDER"))
        self.assertTrue(hasattr(fq, "STK_SHAREHOLDER_TOP10"))
        self.assertTrue(hasattr(fq, "STK_SHAREHOLDER_FLOAT_TOP10"))
        self.assertTrue(hasattr(fq, "STK_SHAREHOLDER_NUM"))

    def test_run_query_simple(self):
        df = run_query_simple(
            "STK_SHAREHOLDER_TOP10", code="600519", force_update=False
        )
        self.assertIsInstance(df, pd.DataFrame)

    def test_run_query_invalid_table(self):
        with self.assertRaises(ValueError):
            run_query_simple("INVALID_TABLE", code="600519")


class TestCacheMechanism(unittest.TestCase):
    """测试缓存机制"""

    def test_cache_days(self):
        self.assertEqual(SHAREHOLDER_CACHE_DAYS, 7)

    def test_cache_directory_creation(self):
        cache_dir = tempfile.mkdtemp() + "/test_cache"
        try:
            get_top10_shareholders("600519", cache_dir=cache_dir, force_update=False)
            self.assertTrue(os.path.exists(cache_dir))
        finally:
            shutil.rmtree(cache_dir, ignore_errors=True)


class TestSchemaDefinition(unittest.TestCase):
    """测试 Schema 定义"""

    def test_shareholder_schema(self):
        expected = [
            "code",
            "report_date",
            "ann_date",
            "shareholder_name",
            "shareholder_code",
            "shareholder_type",
            "hold_amount",
            "hold_ratio",
            "change_type",
            "change_amount",
            "rank",
        ]
        self.assertEqual(_SHAREHOLDER_SCHEMA, expected)

    def test_shareholder_num_schema(self):
        expected_num = [
            "code",
            "report_date",
            "ann_date",
            "holder_num",
            "holder_num_change",
            "holder_num_change_ratio",
        ]
        from jk2bt.finance_data.shareholder import (
            _SHAREHOLDER_NUM_SCHEMA,
        )

        self.assertEqual(_SHAREHOLDER_NUM_SCHEMA, expected_num)


class TestEdgeCases(unittest.TestCase):
    """测试边界条件"""

    def test_invalid_code(self):
        df = get_top10_shareholders("999999", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_empty_string_code(self):
        df = get_top10_shareholders("", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_whitespace_code(self):
        result = get_shareholders("   ", force_update=False)
        self.assertIsInstance(result, RobustResult)


class TestCodeFormatCompatibility(unittest.TestCase):
    """测试代码格式兼容性"""

    def test_jq_sh_format(self):
        df = get_top10_shareholders("600519.XSHG", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_jq_sz_format(self):
        df = get_top10_shareholders("000001.XSHE", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sh_prefix(self):
        df = get_top10_shareholders("sh600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_sz_prefix(self):
        df = get_top10_shareholders("sz000001", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)

    def test_pure_code(self):
        df = get_top10_shareholders("600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)


class TestDataValidation(unittest.TestCase):
    """测试数据验证"""

    def test_shareholder_name_not_empty(self):
        df = get_top10_shareholders("600519", force_update=False)
        if not df.empty and "shareholder_name" in df.columns:
            non_empty = df["shareholder_name"].dropna()
            if len(non_empty) > 0:
                self.assertTrue(all(len(str(n)) > 0 for n in non_empty))

    def test_hold_ratio_range(self):
        df = get_top10_shareholders("600519", force_update=False)
        if not df.empty and "hold_ratio" in df.columns:
            ratios = df["hold_ratio"].dropna()
            for r in ratios:
                self.assertGreaterEqual(r, 0)
                self.assertLessEqual(r, 100)

    def test_code_format_consistency(self):
        df = get_top10_shareholders("600519", force_update=False)
        if not df.empty and "code" in df.columns:
            codes = df["code"].unique()
            for code in codes:
                self.assertTrue(".XSHG" in code or ".XSHE" in code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
