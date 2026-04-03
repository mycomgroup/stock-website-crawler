"""
test_finance_data_modules.py
单元测试：finance_data 底层模块测试
"""

import unittest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from finance_data.margin import (
    get_margin_data,
    get_margin_history,
    _extract_code_num,
    _get_market,
    _normalize_date,
    _filter_and_normalize,
    _normalize_to_jq,
)
from finance_data.forecast import (
    get_forecast_data,
    _extract_code_num as _extract_code_num_forecast,
    _normalize_to_jq as _normalize_to_jq_forecast,
    _normalize_predict_data,
    _normalize_forecast_data,
    _normalize_quick_data,
)


class TestMarginData(unittest.TestCase):
    """融资融券底层函数测试"""

    def test_extract_code_num(self):
        """测试代码提取"""
        self.assertEqual(_extract_code_num("600519.XSHG"), "600519")
        self.assertEqual(_extract_code_num("sh600519"), "600519")
        self.assertEqual(_extract_code_num("600519"), "600519")
        self.assertEqual(_extract_code_num("000001.XSHE"), "000001")
        self.assertEqual(_extract_code_num("sz000001"), "000001")

    def test_get_market(self):
        """测试市场判断"""
        self.assertEqual(_get_market("600519.XSHG"), "sh")
        self.assertEqual(_get_market("sh600519"), "sh")
        self.assertEqual(_get_market("600519"), "sh")
        self.assertEqual(_get_market("000001.XSHE"), "sz")
        self.assertEqual(_get_market("sz000001"), "sz")
        self.assertEqual(_get_market("000001"), "sz")

    def test_normalize_date(self):
        """测试日期标准化"""
        self.assertEqual(_normalize_date("2024-01-15"), "20240115")
        self.assertEqual(_normalize_date("20240115"), "20240115")

    def test_normalize_to_jq(self):
        """测试聚宽格式转换"""
        self.assertEqual(_normalize_to_jq("600519.XSHG"), "600519.XSHG")
        self.assertEqual(_normalize_to_jq("sh600519"), "600519.XSHG")
        self.assertEqual(_normalize_to_jq("600519"), "600519.XSHG")
        self.assertEqual(_normalize_to_jq("sz000001"), "000001.XSHE")
        self.assertEqual(_normalize_to_jq("000001"), "000001.XSHE")

    def test_filter_and_normalize_sh(self):
        """测试沪市数据标准化"""
        sh_data = {
            "信用交易日期": "20240115",
            "标的证券代码": "600519",
            "标的证券简称": "贵州茅台",
            "融资余额": 17212887165,
            "融资买入额": 284428113,
            "融资偿还额": 326217208,
            "融券余量": 68965,
            "融券卖出量": 4400,
            "融券偿还量": 1500,
        }
        df_sh = pd.DataFrame([sh_data])
        result = _filter_and_normalize(df_sh, "600519", "sh", "600519.XSHG")

        self.assertEqual(len(result), 1)
        self.assertIn("code", result.columns)
        self.assertIn("date", result.columns)
        self.assertIn("margin_balance", result.columns)
        self.assertEqual(result.iloc[0]["code"], "600519.XSHG")
        self.assertEqual(result.iloc[0]["date"], "20240115")
        self.assertEqual(result.iloc[0]["margin_balance"], 17212887165)

    def test_filter_and_normalize_sz(self):
        """测试深市数据标准化"""
        sz_data = {
            "证券代码": "000001",
            "证券简称": "平安银行",
            "融资买入额": 59261725,
            "融资余额": 5465405837,
            "融券卖出量": 131200,
            "融券余量": 1538900,
            "融券余额": 16958678,
            "融资融券余额": 5482365015,
        }
        df_sz = pd.DataFrame([sz_data])
        result = _filter_and_normalize(df_sz, "000001", "sz", "000001.XSHE")

        self.assertEqual(len(result), 1)
        self.assertIn("code", result.columns)
        self.assertIn("margin_balance", result.columns)
        self.assertIn("total_balance", result.columns)
        self.assertEqual(result.iloc[0]["code"], "000001.XSHE")
        self.assertEqual(result.iloc[0]["margin_balance"], 5465405837)

    def test_get_margin_data_basic(self):
        """测试基本融资融券数据获取"""
        df = get_margin_data("600519.XSHG")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("margin_balance", df.columns)

    def test_get_margin_data_different_formats(self):
        """测试不同代码格式"""
        formats = ["600519.XSHG", "sh600519", "600519"]
        for fmt in formats:
            df = get_margin_data(fmt)
            self.assertIsInstance(df, pd.DataFrame)

    def test_get_margin_data_sz_market(self):
        """测试深市股票"""
        df = get_margin_data("000001.XSHE")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertEqual(df.iloc[0]["code"], "000001.XSHE")

    def test_get_margin_data_specific_date(self):
        """测试指定日期查询"""
        df = get_margin_data("600519.XSHG", date="20240115")
        self.assertIsInstance(df, pd.DataFrame)

    def test_get_margin_data_invalid_stock(self):
        """测试无效股票代码"""
        df = get_margin_data("999999.XSHG")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_get_margin_history(self):
        """测试历史数据获取"""
        df = get_margin_history(
            "600519.XSHG", "2024-01-10", "2024-01-15", force_update=True
        )
        self.assertIsInstance(df, pd.DataFrame)


class TestForecastData(unittest.TestCase):
    """业绩预告底层函数测试"""

    def test_extract_code_num_forecast(self):
        """测试代码提取"""
        self.assertEqual(_extract_code_num_forecast("600519.XSHG"), "600519")
        self.assertEqual(_extract_code_num_forecast("sh600519"), "600519")
        self.assertEqual(_extract_code_num_forecast("600519"), "600519")

    def test_normalize_to_jq_forecast(self):
        """测试聚宽格式转换"""
        self.assertEqual(_normalize_to_jq_forecast("600519.XSHG"), "600519.XSHG")
        self.assertEqual(_normalize_to_jq_forecast("sh600519"), "600519.XSHG")
        self.assertEqual(_normalize_to_jq_forecast("600519"), "600519.XSHG")

    def test_normalize_predict_data(self):
        """测试预测数据标准化"""
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

        self.assertEqual(len(result), 2)
        self.assertIn("code", result.columns)
        self.assertIn("year", result.columns)
        self.assertIn("type", result.columns)
        self.assertIn("forecast_mean", result.columns)
        self.assertTrue(all(result["type"] == "预测年报每股收益"))

    def test_normalize_forecast_data(self):
        """测试业绩预告数据标准化"""
        data = {
            "年度": [2024],
            "预告类型": ["预增"],
            "公告日期": ["2024-01-15"],
        }
        df = pd.DataFrame(data)
        result = _normalize_forecast_data(df, "600519.XSHG")

        self.assertGreaterEqual(len(result), 1)
        self.assertIn("code", result.columns)
        self.assertIn("type", result.columns)
        self.assertTrue(all(result["type"] == "业绩预告"))

    def test_normalize_quick_data(self):
        """测试业绩快报数据标准化"""
        data = {
            "年度": [2024],
            "营业总收入": [1000000],
            "净利润": [500000],
        }
        df = pd.DataFrame(data)
        result = _normalize_quick_data(df, "600519.XSHG")

        self.assertGreaterEqual(len(result), 1)
        self.assertIn("code", result.columns)
        self.assertIn("type", result.columns)
        self.assertTrue(all(result["type"] == "业绩快报"))

    def test_get_forecast_data_basic(self):
        """测试基本业绩预告数据获取"""
        df = get_forecast_data("600519.XSHG")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("year", df.columns)
            self.assertIn("type", df.columns)

    def test_get_forecast_data_different_formats(self):
        """测试不同代码格式"""
        formats = ["600519.XSHG", "sh600519", "600519"]
        for fmt in formats:
            df = get_forecast_data(fmt)
            self.assertIsInstance(df, pd.DataFrame)

    def test_get_forecast_data_sz_market(self):
        """测试深市股票"""
        df = get_forecast_data("000001.XSHE")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertEqual(df.iloc[0]["code"], "000001.XSHE")


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_margin_and_forecast_together(self):
        """测试同时获取融资融券和业绩预告数据"""
        margin_df = get_margin_data("600519.XSHG")
        forecast_df = get_forecast_data("600519.XSHG")

        self.assertIsInstance(margin_df, pd.DataFrame)
        self.assertIsInstance(forecast_df, pd.DataFrame)

        if not margin_df.empty:
            self.assertIn("code", margin_df.columns)
            self.assertEqual(margin_df.iloc[0]["code"], "600519.XSHG")

        if not forecast_df.empty:
            self.assertIn("code", forecast_df.columns)
            self.assertEqual(forecast_df.iloc[0]["code"], "600519.XSHG")

    def test_multiple_stocks(self):
        """测试多股票查询"""
        stocks = ["600519.XSHG", "000001.XSHE"]

        results = []
        for stock in stocks:
            df = get_margin_data(stock)
            results.append(df)

        self.assertEqual(len(results), 2)
        for df in results:
            self.assertIsInstance(df, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
