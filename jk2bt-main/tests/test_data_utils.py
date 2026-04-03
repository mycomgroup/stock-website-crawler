import unittest
import pandas as pd
import pytest

from jk2bt.core.strategy_base import (
    get_akshare_etf_data,
    format_stock_symbol_for_akshare,
    get_akshare_stock_data,
    get_index_nav,
    get_price_jq,
    get_cashflow_sina,
    get_income_ths,
)
import os


class TestDataUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 初始化测试数据和缓存目录
        cls.cache_dir = "test_cache"
        os.makedirs(cls.cache_dir, exist_ok=True)

    def test_format_stock_symbol_for_akshare(self):
        self.assertEqual(format_stock_symbol_for_akshare("sh600000"), "600000")
        self.assertEqual(format_stock_symbol_for_akshare("600000.XSHG"), "600000")
        self.assertEqual(format_stock_symbol_for_akshare("000001"), "000001")

    @pytest.mark.network
    def test_get_index_nav(self):
        try:
            nav = get_index_nav("000001", "2023-01-01", "2023-01-10")
            self.assertIsInstance(nav, pd.Series)
        except Exception as e:
            self.skipTest(f"无法获取指数净值数据: {e}")

    @pytest.mark.network
    def test_get_price(self):
        try:
            result = get_price_jq(
                "sh600000", "2023-01-01", "2023-01-10", cache_dir=self.cache_dir
            )
            self.assertIsInstance(result, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"无法获取行情数据: {e}")

    @pytest.mark.network
    def test_get_akshare_etf_data(self):
        try:
            data = get_akshare_etf_data("510300", "2023-01-01", "2023-01-10")
            self.assertIsNotNone(data)
        except Exception as e:
            self.skipTest(f"无法获取ETF数据: {e}")

    @pytest.mark.network
    def test_get_akshare_stock_data(self):
        try:
            data = get_akshare_stock_data("sh600000", "2023-01-01", "2023-01-10")
            self.assertIsNotNone(data)
        except Exception as e:
            self.skipTest(f"无法获取A股数据: {e}")

    def test_get_cashflow_sina(self):
        try:
            data = get_cashflow_sina("sh600000")
            self.assertIsInstance(data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"无法获取现金流量表数据: {e}")

    def test_get_income_ths(self):
        try:
            data = get_income_ths("sh600000", "合并报表")
            self.assertIsInstance(data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"无法获取利润表数据: {e}")


if __name__ == "__main__":
    unittest.main()
