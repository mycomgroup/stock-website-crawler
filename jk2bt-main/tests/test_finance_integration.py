"""
test_finance_integration.py
Finance模块集成测试 - 测试所有finance表的联合使用
"""

import unittest
import pandas as pd

from jk2bt.core.strategy_base import finance, query


class TestFinanceIntegration(unittest.TestCase):
    """Finance模块集成测试"""

    def test_all_finance_tables_exist(self):
        """测试所有finance表都存在"""
        tables = [
            "STK_XR_XD",
            "STK_MX_RZ_RQ",
            "STK_FIN_FORCAST",
            "STK_COMPANY_BASIC_INFO",
            "STK_STATUS_CHANGE",
            "STK_LISTING_INFO",
            "STK_SHAREHOLDER_TOP10",
            "STK_SHAREHOLDER_FLOAT_TOP10",
            "STK_SHAREHOLDER_NUM",
            "STK_DIVIDEND",
            "STK_UNLOCK",
            "STK_SHARE_CHANGE",
        ]
        
        for table in tables:
            self.assertTrue(hasattr(finance, table), f"缺少表: {table}")

    def test_multiple_tables_query(self):
        """测试多表联合查询"""
        stocks = ["600519.XSHG"]
        
        # 查询公司信息
        df1 = finance.run_query(
            query(finance.STK_COMPANY_BASIC_INFO.code).filter(
                finance.STK_COMPANY_BASIC_INFO.code.in_(stocks)
            )
        )
        
        # 查询股东信息
        df2 = finance.run_query(
            query(finance.STK_SHAREHOLDER_TOP10.code).filter(
                finance.STK_SHAREHOLDER_TOP10.code.in_(stocks)
            )
        )
        
        # 查询分红信息
        df3 = finance.run_query(
            query(finance.STK_XR_XD.code).filter(
                finance.STK_XR_XD.code.in_(stocks)
            )
        )
        
        self.assertIsInstance(df1, pd.DataFrame)
        self.assertIsInstance(df2, pd.DataFrame)
        self.assertIsInstance(df3, pd.DataFrame)

    def test_cross_table_filter(self):
        """测试跨表过滤"""
        stocks = ["600519.XSHG", "000001.XSHE"]
        
        # 查询公司信息
        df_company = finance.run_query(
            query(
                finance.STK_COMPANY_BASIC_INFO.code,
                finance.STK_COMPANY_BASIC_INFO.company_name,
            ).filter(finance.STK_COMPANY_BASIC_INFO.code.in_(stocks))
        )
        
        if not df_company.empty:
            # 使用公司信息结果查询股东
            codes = df_company["code"].tolist()
            df_holder = finance.run_query(
                query(finance.STK_SHAREHOLDER_TOP10.code).filter(
                    finance.STK_SHAREHOLDER_TOP10.code.in_(codes)
                )
            )
            
            self.assertIsInstance(df_holder, pd.DataFrame)

    def test_query_with_multiple_filters(self):
        """测试多条件过滤"""
        stocks = ["600519.XSHG"]
        
        df = finance.run_query(
            query(
                finance.STK_XR_XD.code,
                finance.STK_XR_XD.bonus_amount_rmb,
            ).filter(
                finance.STK_XR_XD.code.in_(stocks),
                finance.STK_XR_XD.bonus_amount_rmb > 0,
            )
        )
        
        self.assertIsInstance(df, pd.DataFrame)

    def test_query_with_limit_offset(self):
        """测试limit功能"""
        stocks = ["600519.XSHG"]
        
        df = finance.run_query(
            query(finance.STK_SHAREHOLDER_TOP10.code)
            .filter(finance.STK_SHAREHOLDER_TOP10.code.in_(stocks))
            .limit(3)
        )
        
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertLessEqual(len(df), 3)

    def test_table_proxy_functionality(self):
        """测试表代理功能"""
        # 测试表属性
        table = finance.STK_COMPANY_BASIC_INFO
        self.assertTrue(hasattr(table, "_name"))
        
        # 测试字段代理
        field = finance.STK_COMPANY_BASIC_INFO.code
        self.assertTrue(hasattr(field, "_field"))
        self.assertEqual(field._field, "code")
        
        # 测试字段操作
        expr = finance.STK_COMPANY_BASIC_INFO.code.in_(["600519.XSHG"])
        self.assertTrue(hasattr(expr, "_symbols"))

    def test_run_query_error_handling(self):
        """测试错误处理"""
        # 空查询
        df1 = finance.run_query(query())
        self.assertIsInstance(df1, pd.DataFrame)
        
        # 无效表名（应该返回空DataFrame）
        df2 = finance.run_query(
            query(finance.STK_COMPANY_BASIC_INFO.code).filter(
                finance.STK_COMPANY_BASIC_INFO.code.in_(["999999.XSHG"])
            )
        )
        self.assertIsInstance(df2, pd.DataFrame)

    def test_performance_multiple_queries(self):
        """测试批量查询性能"""
        stocks = ["600519.XSHG", "000001.XSHE", "000858.XSHE"]
        
        # 批量查询多个表
        results = {}
        for table_name, table in [
            ("company", finance.STK_COMPANY_BASIC_INFO),
            ("shareholder", finance.STK_SHAREHOLDER_TOP10),
        ]:
            df = finance.run_query(
                query(table.code).filter(table.code.in_(stocks))
            )
            results[table_name] = df
        
        self.assertEqual(len(results), 2)
        for df in results.values():
            self.assertIsInstance(df, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
