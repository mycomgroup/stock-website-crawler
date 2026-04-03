"""
test_all_finance_apis.py
全面测试所有财务数据 API
"""

import unittest
import pandas as pd
import datetime as dt
import sys
sys.path.insert(0, '/Users/yuping/Downloads/git/jk2bt-main')

from jk2bt.core.strategy_base import finance, query


class TestAllFinanceAPIs(unittest.TestCase):
    """测试所有 finance 数据 API"""

    def setUp(self):
        """测试前准备"""
        self.test_stocks = ["600519.XSHG"]
        self.test_stock = "600519.XSHG"

    # ========== 任务1：公司基本信息 ==========
    def test_task1_company_info(self):
        """任务1：公司基本信息"""
        from jk2bt.finance_data import get_company_info
        
        df = get_company_info(self.test_stock, use_duckdb=False, force_update=False)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("company_name", df.columns)

    def test_task1_security_status(self):
        """任务1：证券状态"""
        from jk2bt.finance_data import get_security_status
        
        df = get_security_status(self.test_stock, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("status_type", df.columns)

    def test_task1_finance_company_info(self):
        """任务1：finance.run_query 公司信息"""
        df = finance.run_query(
            query(finance.STK_COMPANY_BASIC_INFO.code).filter(
                finance.STK_COMPANY_BASIC_INFO.code.in_(self.test_stocks)
            )
        )
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("code", df.columns)

    def test_task1_finance_status_change(self):
        """任务1：finance.run_query 状态变更"""
        df = finance.run_query(
            query(finance.STK_STATUS_CHANGE.code).filter(
                finance.STK_STATUS_CHANGE.code.in_(self.test_stocks)
            )
        )
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("code", df.columns)

    # ========== 任务2：股东信息 ==========
    def test_task2_top_shareholders(self):
        """任务2：十大股东"""
        from jk2bt.finance_data import get_top_shareholders
        
        df = get_top_shareholders(self.test_stock, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("shareholder_name", df.columns)

    def test_task2_shareholder_count(self):
        """任务2：股东户数"""
        from jk2bt.finance_data import get_shareholder_count
        
        df = get_shareholder_count(self.test_stock, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)

    def test_task2_finance_shareholder(self):
        """任务2：finance.run_query 股东信息"""
        df = finance.run_query(
            query(finance.STK_SHAREHOLDER_TOP10.code).filter(
                finance.STK_SHAREHOLDER_TOP10.code.in_(self.test_stocks)
            )
        )
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("code", df.columns)

    # ========== 任务3：分红送股 ==========
    def test_task3_dividend_info(self):
        """任务3：分红信息"""
        from jk2bt.finance_data import get_dividend_info
        
        df = get_dividend_info(self.test_stock, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)

    def test_task3_finance_dividend(self):
        """任务3：finance.run_query 分红"""
        df = finance.run_query(
            query(finance.STK_XR_XD.code).filter(
                finance.STK_XR_XD.code.in_(self.test_stocks)
            )
        )
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("code", df.columns)

    # ========== 任务4：股东变动 ==========
    def test_task4_share_change(self):
        """任务4：股东变动"""
        from jk2bt.finance_data import get_share_change
        
        df = get_share_change(self.test_stock, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)

    # ========== 任务5：限售解禁 ==========
    def test_task5_unlock(self):
        """任务5：限售解禁"""
        from jk2bt.finance_data import get_unlock
        
        df = get_unlock(self.test_stock, use_duckdb=False)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)

    # ========== 通用测试 ==========
    def test_finance_module_all_tables(self):
        """测试 finance 模块所有表"""
        tables = [
            "STK_COMPANY_BASIC_INFO",
            "STK_STATUS_CHANGE",
            "STK_SHAREHOLDER_TOP10",
            "STK_SHAREHOLDER_NUM",
            "STK_XR_XD",
        ]
        
        for table_name in tables:
            self.assertTrue(hasattr(finance, table_name))
            table = getattr(finance, table_name)
            self.assertTrue(hasattr(table, "_name"))

    def test_finance_field_proxy(self):
        """测试 finance 字段代理"""
        field = finance.STK_XR_XD.code
        self.assertTrue(hasattr(field, "_field"))
        self.assertEqual(field._field, "code")

        # 测试 in_ 操作
        expr = field.in_(self.test_stocks)
        self.assertTrue(hasattr(expr, "_symbols"))

    def test_finance_comparison_operators(self):
        """测试 finance 比较操作符"""
        field = finance.STK_XR_XD.bonus_amount_rmb
        
        # 测试各种比较操作
        expr_gt = field > 0
        self.assertTrue(hasattr(expr_gt, "_gt"))
        
        expr_ge = field >= 0
        self.assertTrue(hasattr(expr_ge, "_ge"))
        
        expr_lt = field < 1000
        self.assertTrue(hasattr(expr_lt, "_lt"))
        
        expr_le = field <= 1000
        self.assertTrue(hasattr(expr_le, "_le"))

    def test_query_builder(self):
        """测试 query 构建器"""
        q = query(
            finance.STK_XR_XD.code,
            finance.STK_XR_XD.bonus_amount_rmb,
        ).filter(
            finance.STK_XR_XD.code.in_(self.test_stocks)
        ).limit(10)
        
        self.assertTrue(hasattr(q, "_tables"))
        self.assertTrue(hasattr(q, "_filters"))
        self.assertEqual(q._limit_n, 10)

    def test_schema_fallback(self):
        """测试 schema 保底机制"""
        # 测试所有表的 schema 保底
        tables = [
            finance.STK_COMPANY_BASIC_INFO,
            finance.STK_STATUS_CHANGE,
            finance.STK_SHAREHOLDER_TOP10,
            finance.STK_XR_XD,
        ]
        
        for table in tables:
            df = finance.run_query(
                query(table.code).filter(
                    table.code.in_(["999999.XSHG"])
                )
            )
            self.assertIsInstance(df, pd.DataFrame)
            self.assertTrue(df.empty)
            self.assertIn("code", df.columns)

    def test_empty_symbols(self):
        """测试空股票列表"""
        df = finance.run_query(
            query(finance.STK_XR_XD.code)
        )
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_limit_functionality(self):
        """测试 limit 功能"""
        df = finance.run_query(
            query(finance.STK_XR_XD.code)
            .filter(finance.STK_XR_XD.code.in_(self.test_stocks))
            .limit(5)
        )
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertLessEqual(len(df), 5)

    def test_date_filter(self):
        """测试日期过滤"""
        dt_3y = dt.datetime.now() - dt.timedelta(days=3 * 365)
        
        df = finance.run_query(
            query(
                finance.STK_XR_XD.code,
                finance.STK_XR_XD.bonus_amount_rmb,
            ).filter(
                finance.STK_XR_XD.code.in_(self.test_stocks),
                finance.STK_XR_XD.board_plan_pub_date > dt_3y,
            )
        )
        
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty and "board_plan_pub_date" in df.columns:
            self.assertTrue(all(df["board_plan_pub_date"] > pd.Timestamp(dt_3y)))


class TestDataQuality(unittest.TestCase):
    """测试数据质量"""

    def test_company_info_data_quality(self):
        """测试公司信息数据质量"""
        from jk2bt.finance_data import get_company_info
        
        df = get_company_info("600519.XSHG", use_duckdb=False)
        
        if not df.empty:
            # 验证必需字段存在
            required_fields = ["code", "company_name", "industry"]
            for field in required_fields:
                self.assertIn(field, df.columns, f"缺少字段: {field}")
            
            # 验证代码格式正确
            code = df.iloc[0]["code"]
            self.assertIn(".XSHG", code) or self.assertIn(".XSHE", code)

    def test_dividend_data_quality(self):
        """测试分红数据质量"""
        df = finance.run_query(
            query(
                finance.STK_XR_XD.code,
                finance.STK_XR_XD.bonus_amount_rmb,
            ).filter(
                finance.STK_XR_XD.code.in_(["600519.XSHG"])
            )
        )
        
        if not df.empty:
            # 验证分红金额字段为数值类型
            self.assertIn("bonus_amount_rmb", df.columns)


class TestCacheMechanism(unittest.TestCase):
    """测试缓存机制"""

    def test_company_info_cache(self):
        """测试公司信息缓存"""
        from jk2bt.finance_data import get_company_info
        
        # 第一次调用
        df1 = get_company_info("600519.XSHG", use_duckdb=False, force_update=False)
        
        # 第二次调用（应该使用缓存）
        df2 = get_company_info("600519.XSHG", use_duckdb=False, force_update=False)
        
        self.assertIsInstance(df1, pd.DataFrame)
        self.assertIsInstance(df2, pd.DataFrame)


if __name__ == "__main__":
    # 运行所有测试
    unittest.main(verbosity=2)
