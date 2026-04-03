"""
test_company_info_alignment.py
公司信息严格对齐验证测试

验证:
1. finance.run_query 可用
2. STK_COMPANY_BASIC_INFO, STK_STATUS_CHANGE 表可用
3. 空结果返回稳定 schema
4. 代码格式兼容（600000/sh600000/600000.XSHG）
"""

import unittest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt import finance, query


class TestFinanceRunQuery(unittest.TestCase):
    """测试全局 finance.run_query 可用性"""

    def test_finance_module_exists(self):
        """验证 finance 模块已导出"""
        self.assertIsNotNone(finance)

    def test_finance_has_run_query(self):
        """验证 finance.run_query 方法存在"""
        self.assertTrue(hasattr(finance, "run_query"))
        self.assertTrue(callable(finance.run_query))

    def test_finance_has_stk_company_basic_info(self):
        """验证 finance.STK_COMPANY_BASIC_INFO 表存在"""
        self.assertTrue(hasattr(finance, "STK_COMPANY_BASIC_INFO"))

    def test_finance_has_stk_status_change(self):
        """验证 finance.STK_STATUS_CHANGE 表存在"""
        self.assertTrue(hasattr(finance, "STK_STATUS_CHANGE"))

    def test_finance_has_stk_listing_info(self):
        """验证 finance.STK_LISTING_INFO 表存在（兼容）"""
        self.assertTrue(hasattr(finance, "STK_LISTING_INFO"))

    def test_query_company_basic_info(self):
        """测试 query(finance.STK_COMPANY_BASIC_INFO).filter(...)"""
        q = query(finance.STK_COMPANY_BASIC_INFO)
        self.assertIsNotNone(q)
        self.assertTrue(hasattr(q, "filter"))
        self.assertTrue(hasattr(q, "limit"))

    def test_run_query_company_basic_info(self):
        """测试 finance.run_query 查询公司基本信息"""
        q = query(finance.STK_COMPANY_BASIC_INFO).filter(
            finance.STK_COMPANY_BASIC_INFO.code.in_(["600519.XSHG"])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)
        expected_cols = [
            "code",
            "company_name",
            "establish_date",
            "list_date",
            "main_business",
            "industry",
            "registered_address",
            "company_status",
            "status_change_date",
            "change_type",
        ]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_run_query_status_change(self):
        """测试 finance.run_query 查询状态变动"""
        q = query(finance.STK_STATUS_CHANGE).filter(
            finance.STK_STATUS_CHANGE.code.in_(["600519.XSHG"])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)
        expected_cols = ["code", "status_date", "status_type", "reason"]
        for col in expected_cols:
            self.assertIn(col, df.columns)


class TestStableSchema(unittest.TestCase):
    """测试空结果返回稳定 schema"""

    def test_empty_symbols_company_basic_info(self):
        """测试空股票代码返回稳定 schema"""
        q = query(finance.STK_COMPANY_BASIC_INFO).filter(
            finance.STK_COMPANY_BASIC_INFO.code.in_([])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)
        expected_cols = [
            "code",
            "company_name",
            "establish_date",
            "list_date",
            "main_business",
            "industry",
            "registered_address",
            "company_status",
            "status_change_date",
            "change_type",
        ]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_invalid_symbols_company_basic_info(self):
        """测试无效股票代码返回稳定 schema"""
        q = query(finance.STK_COMPANY_BASIC_INFO).filter(
            finance.STK_COMPANY_BASIC_INFO.code.in_(["999999.XSHG"])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)
        expected_cols = [
            "code",
            "company_name",
            "establish_date",
            "list_date",
            "main_business",
            "industry",
            "registered_address",
            "company_status",
            "status_change_date",
            "change_type",
        ]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_empty_symbols_status_change(self):
        """测试空股票代码返回稳定 schema"""
        q = query(finance.STK_STATUS_CHANGE).filter(
            finance.STK_STATUS_CHANGE.code.in_([])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)
        expected_cols = ["code", "status_date", "status_type", "reason"]
        for col in expected_cols:
            self.assertIn(col, df.columns)


class TestCodeFormatCompatibility(unittest.TestCase):
    """测试代码格式兼容性"""

    def test_pure_code_format(self):
        """测试纯代码格式: 600000"""
        q = query(finance.STK_COMPANY_BASIC_INFO).filter(
            finance.STK_COMPANY_BASIC_INFO.code.in_(["600000"])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)

    def test_jq_format_sh(self):
        """测试聚宽格式: 600000.XSHG"""
        q = query(finance.STK_COMPANY_BASIC_INFO).filter(
            finance.STK_COMPANY_BASIC_INFO.code.in_(["600000.XSHG"])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)

    def test_jq_format_sz(self):
        """测试聚宽格式: 000001.XSHE"""
        q = query(finance.STK_COMPANY_BASIC_INFO).filter(
            finance.STK_COMPANY_BASIC_INFO.code.in_(["000001.XSHE"])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)

    def test_prefix_format_sh(self):
        """测试前缀格式: sh600000"""
        q = query(finance.STK_COMPANY_BASIC_INFO).filter(
            finance.STK_COMPANY_BASIC_INFO.code.in_(["sh600000"])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)

    def test_prefix_format_sz(self):
        """测试前缀格式: sz000001"""
        q = query(finance.STK_COMPANY_BASIC_INFO).filter(
            finance.STK_COMPANY_BASIC_INFO.code.in_(["sz000001"])
        )
        df = finance.run_query(q)
        self.assertIsInstance(df, pd.DataFrame)


class TestModuleDirectCall(unittest.TestCase):
    """测试模块直接调用"""

    def test_get_company_info_direct(self):
        """测试直接调用 get_company_info"""
        from jk2bt.finance_data.company_info import (
            get_company_info,
        )

        df = get_company_info("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)
        expected_cols = [
            "code",
            "company_name",
            "establish_date",
            "list_date",
            "main_business",
            "industry",
            "registered_address",
            "company_status",
            "status_change_date",
            "change_type",
        ]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_get_security_status_direct(self):
        """测试直接调用 get_security_status"""
        from jk2bt.finance_data.company_info import (
            get_security_status,
        )

        df = get_security_status("600519", force_update=False, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)
        expected_cols = ["code", "status_date", "status_type", "reason"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_get_listing_info_direct(self):
        """测试直接调用 get_listing_info"""
        from jk2bt.finance_data.company_info import (
            get_listing_info,
        )

        df = get_listing_info(symbol="600519", force_update=False)
        self.assertIsInstance(df, pd.DataFrame)
        expected_cols = ["code", "name", "start_date", "state_id", "state"]
        for col in expected_cols:
            self.assertIn(col, df.columns)


if __name__ == "__main__":
    unittest.main(verbosity=2)
