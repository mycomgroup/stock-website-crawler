"""
test_finance_query.py
单元测试：finance.run_query 适配
"""

import unittest
import pandas as pd
import datetime as dt
import sys
import os

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src",
    ),
)

from jk2bt.core.strategy_base import finance, query


class TestFinanceQuery(unittest.TestCase):
    def test_finance_module_attributes(self):
        """测试finance模块属性"""
        self.assertTrue(hasattr(finance, "STK_XR_XD"))
        self.assertTrue(hasattr(finance, "STK_MX_RZ_RQ"))
        self.assertTrue(hasattr(finance, "STK_FIN_FORCAST"))
        self.assertTrue(hasattr(finance, "run_query"))

    def test_finance_table_proxy(self):
        """测试finance表代理"""
        table = finance.STK_XR_XD
        self.assertTrue(hasattr(table, "_name"))
        self.assertEqual(table._name, "STK_XR_XD")

        field = finance.STK_XR_XD.code
        self.assertTrue(hasattr(field, "_field"))
        self.assertEqual(field._field, "code")

    def test_finance_field_in_operator(self):
        """测试finance字段in_操作"""
        stocks = ["600519.XSHG", "000001.XSHE"]
        expr = finance.STK_XR_XD.code.in_(stocks)
        self.assertEqual(expr._symbols, stocks)

    def test_finance_field_comparison_operators(self):
        """测试finance字段比较操作"""
        expr_gt = finance.STK_XR_XD.bonus_amount_rmb > 100
        self.assertTrue(expr_gt._gt)
        self.assertEqual(expr_gt._value, 100)

        expr_ge = finance.STK_XR_XD.bonus_amount_rmb >= 100
        self.assertTrue(expr_ge._ge)
        self.assertEqual(expr_ge._value, 100)

        expr_lt = finance.STK_XR_XD.bonus_amount_rmb < 1000
        self.assertTrue(expr_lt._lt)
        self.assertEqual(expr_lt._value, 1000)

        expr_le = finance.STK_XR_XD.bonus_amount_rmb <= 1000
        self.assertTrue(expr_le._le)
        self.assertEqual(expr_le._value, 1000)

    def test_query_builder_with_finance_table(self):
        """测试query builder与finance表"""
        stocks = ["600519.XSHG"]
        q = query(
            finance.STK_XR_XD.code,
            finance.STK_XR_XD.bonus_amount_rmb,
        ).filter(finance.STK_XR_XD.code.in_(stocks))

        self.assertTrue(hasattr(q, "_tables"))
        self.assertTrue(hasattr(q, "_filters"))
        self.assertEqual(q._symbols, stocks)

    def test_query_dividend_basic(self):
        """测试查询分红数据基本功能"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(
                finance.STK_XR_XD.code,
                finance.STK_XR_XD.board_plan_pub_date,
                finance.STK_XR_XD.bonus_amount_rmb,
            ).filter(finance.STK_XR_XD.code.in_(stocks))
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)

    def test_query_dividend_with_date_filter(self):
        """测试带日期过滤的分红查询"""
        stocks = ["600519.XSHG"]
        dt_3y = dt.datetime.now() - dt.timedelta(days=3 * 365)

        df = finance.run_query(
            query(
                finance.STK_XR_XD.code,
                finance.STK_XR_XD.bonus_amount_rmb,
            ).filter(
                finance.STK_XR_XD.code.in_(stocks),
                finance.STK_XR_XD.board_plan_pub_date > dt_3y,
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty and "board_plan_pub_date" in df.columns:
            dates = pd.to_datetime(df["board_plan_pub_date"], errors="coerce")
            valid_dates = dates.dropna()
            if len(valid_dates) > 0:
                self.assertTrue(all(valid_dates > pd.Timestamp(dt_3y)))

    def test_query_dividend_columns(self):
        """测试分红数据列名"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(
                finance.STK_XR_XD.code,
            ).filter(finance.STK_XR_XD.code.in_(stocks))
        )

        self.assertIn("code", df.columns)

    def test_query_margin_not_implemented(self):
        """测试融资融券查询（已实现）"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(
                finance.STK_MX_RZ_RQ.code,
            ).filter(finance.STK_MX_RZ_RQ.code.in_(stocks))
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty or "code" in df.columns)

    def test_query_forecast_not_implemented(self):
        """测试业绩预告查询（已实现）"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(
                finance.STK_FIN_FORCAST.code,
            ).filter(finance.STK_FIN_FORCAST.code.in_(stocks))
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty or "code" in df.columns)

    def test_query_margin_with_filter(self):
        """测试融资融券查询带过滤条件"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(
                finance.STK_MX_RZ_RQ.code,
                finance.STK_MX_RZ_RQ.margin_balance,
            ).filter(
                finance.STK_MX_RZ_RQ.code.in_(stocks),
                finance.STK_MX_RZ_RQ.margin_balance > 0,
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertTrue(all(df["margin_balance"] > 0))

    def test_query_forecast_with_filter(self):
        """测试业绩预告查询带过滤条件"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(
                finance.STK_FIN_FORCAST.code,
                finance.STK_FIN_FORCAST.year,
            )
            .filter(
                finance.STK_FIN_FORCAST.code.in_(stocks),
                finance.STK_FIN_FORCAST.year > 2020,
            )
            .limit(5)
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertTrue(len(df) <= 5)

    def test_query_empty_symbols(self):
        """测试空股票列表"""
        df = finance.run_query(
            query(
                finance.STK_XR_XD.code,
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_dividend_schema_fallback(self):
        """测试分红表schema保底"""
        df = finance.run_query(
            query(finance.STK_XR_XD.code).filter(
                finance.STK_XR_XD.code.in_(["999999.XSHG"])
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)
        self.assertIn("code", df.columns)

    def test_margin_schema_fallback(self):
        """测试融资融券schema保底"""
        df = finance.run_query(
            query(finance.STK_MX_RZ_RQ.code).filter(
                finance.STK_MX_RZ_RQ.code.in_(["999999.XSHG"])
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)
        self.assertIn("code", df.columns)
        self.assertIn("margin_balance", df.columns)

    def test_forecast_schema_fallback(self):
        """测试业绩预告schema保底"""
        df = finance.run_query(
            query(finance.STK_FIN_FORCAST.code).filter(
                finance.STK_FIN_FORCAST.code.in_(["999999.XSHG"])
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)
        self.assertIn("code", df.columns)
        self.assertIn("year", df.columns)
        self.assertIn("type", df.columns)


class TestMarginData(unittest.TestCase):
    """融资融券底层函数测试"""

    def test_get_margin_data_basic(self):
        """测试基本融资融券数据获取"""
        try:
            from finance_data.margin import get_margin_data
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        df = get_margin_data("600519.XSHG")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("margin_balance", df.columns)
            self.assertEqual(df.iloc[0]["code"], "600519.XSHG")

    def test_get_margin_data_different_formats(self):
        """测试不同代码格式"""
        try:
            from finance_data.margin import get_margin_data
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        formats = ["600519.XSHG", "sh600519", "600519"]
        for fmt in formats:
            df = get_margin_data(fmt)
            self.assertIsInstance(df, pd.DataFrame)
            if not df.empty:
                self.assertIn("code", df.columns)
                self.assertTrue(df.iloc[0]["code"].endswith(".XSHG"))

    def test_get_margin_data_sz_market(self):
        """测试深市股票"""
        try:
            from finance_data.margin import get_margin_data
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        df = get_margin_data("000001.XSHE")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertEqual(df.iloc[0]["code"], "000001.XSHE")

    def test_get_margin_data_specific_date(self):
        """测试指定日期查询"""
        try:
            from finance_data.margin import get_margin_data
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        df = get_margin_data("600519.XSHG", date="20240115")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("date", df.columns)

    def test_get_margin_data_invalid_stock(self):
        """测试无效股票代码"""
        try:
            from finance_data.margin import get_margin_data
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        df = get_margin_data("999999.XSHG")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_margin_field_normalization(self):
        """测试字段标准化"""
        try:
            from finance_data.margin import _filter_and_normalize
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        sh_data = {
            "信用交易日期": "20240115",
            "标的证券代码": "600519",
            "融资余额": 10000000000,
            "融资买入额": 100000000,
            "融资偿还额": 50000000,
            "融券余量": 10000,
            "融券卖出量": 5000,
            "融券偿还量": 3000,
        }
        df_sh = pd.DataFrame([sh_data])
        result = _filter_and_normalize(df_sh, "600519", "sh", "600519.XSHG")

        self.assertIn("code", result.columns)
        self.assertIn("date", result.columns)
        self.assertIn("margin_balance", result.columns)
        self.assertEqual(result.iloc[0]["margin_balance"], 10000000000)


class TestForecastData(unittest.TestCase):
    """业绩预告底层函数测试"""

    def test_get_forecast_data_basic(self):
        """测试基本业绩预告数据获取"""
        try:
            from finance_data.forecast import get_forecast_data
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        df = get_forecast_data("600519.XSHG")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("year", df.columns)
            self.assertIn("type", df.columns)
            self.assertEqual(df.iloc[0]["code"], "600519.XSHG")

    def test_get_forecast_data_different_formats(self):
        """测试不同代码格式"""
        try:
            from finance_data.forecast import get_forecast_data
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        formats = ["600519.XSHG", "sh600519", "600519"]
        for fmt in formats:
            df = get_forecast_data(fmt)
            self.assertIsInstance(df, pd.DataFrame)
            if not df.empty:
                self.assertIn("code", df.columns)

    def test_get_forecast_data_sz_market(self):
        """测试深市股票"""
        try:
            from finance_data.forecast import get_forecast_data
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        df = get_forecast_data("000001.XSHE")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertEqual(df.iloc[0]["code"], "000001.XSHE")

    def test_forecast_field_normalization(self):
        """测试字段标准化"""
        try:
            from finance_data.forecast import _normalize_predict_data
        except ImportError:
            self.skipTest("finance_data module not available in test context")

        data = {
            "年度": [2025, 2026],
            "预测机构数": [45, 46],
            "最小值": [71.07, 72.00],
            "均值": [72.52, 73.00],
            "最大值": [75.23, 76.00],
            "行业平均数": [9.86, 10.00],
        }
        df = pd.DataFrame(data)
        result = _normalize_predict_data(df, "600519.XSHG")

        self.assertIn("code", result.columns)
        self.assertIn("year", result.columns)
        self.assertIn("type", result.columns)
        self.assertIn("forecast_mean", result.columns)
        self.assertEqual(len(result), 2)


class TestFinanceQueryAdvanced(unittest.TestCase):
    """高级 finance.run_query 测试"""

    def test_multi_stock_margin_query(self):
        """测试多股票融资融券查询"""
        stocks = ["600519.XSHG", "000001.XSHE", "000002.XSHE"]

        df = finance.run_query(
            query(finance.STK_MX_RZ_RQ.code).filter(
                finance.STK_MX_RZ_RQ.code.in_(stocks)
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            unique_codes = df["code"].unique()
            self.assertTrue(len(unique_codes) <= len(stocks))

    def test_multi_stock_forecast_query(self):
        """测试多股票业绩预告查询"""
        stocks = ["600519.XSHG", "000001.XSHE"]

        df = finance.run_query(
            query(finance.STK_FIN_FORCAST.code).filter(
                finance.STK_FIN_FORCAST.code.in_(stocks)
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            unique_codes = df["code"].unique()
            self.assertTrue(len(unique_codes) <= len(stocks))

    def test_margin_numeric_filter_combinations(self):
        """测试融资融券数值过滤组合"""
        stocks = ["600519.XSHG"]

        # 测试大于
        df_gt = finance.run_query(
            query(finance.STK_MX_RZ_RQ.margin_balance).filter(
                finance.STK_MX_RZ_RQ.code.in_(stocks),
                finance.STK_MX_RZ_RQ.margin_balance > 1000000000,
            )
        )
        self.assertIsInstance(df_gt, pd.DataFrame)

        # 测试小于
        df_lt = finance.run_query(
            query(finance.STK_MX_RZ_RQ.margin_balance).filter(
                finance.STK_MX_RZ_RQ.code.in_(stocks),
                finance.STK_MX_RZ_RQ.margin_balance < 100000000000,
            )
        )
        self.assertIsInstance(df_lt, pd.DataFrame)

    def test_forecast_numeric_filter_combinations(self):
        """测试业绩预告数值过滤组合"""
        stocks = ["600519.XSHG"]

        # 测试大于等于
        df_ge = finance.run_query(
            query(finance.STK_FIN_FORCAST.year).filter(
                finance.STK_FIN_FORCAST.code.in_(stocks),
                finance.STK_FIN_FORCAST.year >= 2025,
            )
        )
        self.assertIsInstance(df_ge, pd.DataFrame)

        # 测试小于等于
        df_le = finance.run_query(
            query(finance.STK_FIN_FORCAST.year).filter(
                finance.STK_FIN_FORCAST.code.in_(stocks),
                finance.STK_FIN_FORCAST.year <= 2030,
            )
        )
        self.assertIsInstance(df_le, pd.DataFrame)

    def test_margin_with_limit(self):
        """测试融资融券limit功能"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(finance.STK_MX_RZ_RQ.code)
            .filter(finance.STK_MX_RZ_RQ.code.in_(stocks))
            .limit(1)
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertTrue(len(df) <= 1)

    def test_empty_result_handling(self):
        """测试空结果处理"""
        # 测试不存在的股票代码
        df = finance.run_query(
            query(finance.STK_MX_RZ_RQ.code).filter(
                finance.STK_MX_RZ_RQ.code.in_(["999999.XSHG"])
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty or "code" in df.columns)

    def test_field_selection(self):
        """测试字段选择"""
        stocks = ["600519.XSHG"]

        # 选择特定字段
        df = finance.run_query(
            query(
                finance.STK_MX_RZ_RQ.code, finance.STK_MX_RZ_RQ.margin_balance
            ).filter(finance.STK_MX_RZ_RQ.code.in_(stocks))
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)


class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def test_empty_stock_list(self):
        """测试空股票列表"""
        df = finance.run_query(
            query(finance.STK_MX_RZ_RQ.code).filter(finance.STK_MX_RZ_RQ.code.in_([]))
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_no_filter_query(self):
        """测试无过滤条件的查询"""
        df = finance.run_query(query(finance.STK_MX_RZ_RQ.code))

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_multiple_filters(self):
        """测试多个过滤条件"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(finance.STK_MX_RZ_RQ.code).filter(
                finance.STK_MX_RZ_RQ.code.in_(stocks),
                finance.STK_MX_RZ_RQ.margin_balance > 0,
                finance.STK_MX_RZ_RQ.margin_buy > 0,
            )
        )

        self.assertIsInstance(df, pd.DataFrame)

    def test_invalid_table_query(self):
        """测试不支持的表查询"""
        from jk2bt.core.strategy_base import _FinanceTableProxy

        invalid_table = _FinanceTableProxy("INVALID_TABLE")
        df = finance.run_query(query(invalid_table.code))

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_chained_filter_operations(self):
        """测试链式过滤操作"""
        stocks = ["600519.XSHG"]

        q = query(finance.STK_MX_RZ_RQ.code)
        q = q.filter(finance.STK_MX_RZ_RQ.code.in_(stocks))
        q = q.limit(10)

        df = finance.run_query(q)

        self.assertIsInstance(df, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
