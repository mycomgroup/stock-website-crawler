"""
test_all_apis.py
测试所有新增 API 模块的基本功能
"""

import unittest
import pandas as pd
from jk2bt.core.strategy_base import finance, query


class TestAllAPIs(unittest.TestCase):
    """测试所有 API 模块"""

    def test_shareholder_api(self):
        """测试股东信息 API"""
        from jk2bt.finance_data import get_top10_shareholders
        
        df = get_top10_shareholders("600519")
        self.assertIsInstance(df, pd.DataFrame)

    def test_dividend_api(self):
        """测试分红 API"""
        from jk2bt.finance_data import get_dividend_info
        
        df = get_dividend_info("600519.XSHG")
        self.assertIsInstance(df, pd.DataFrame)

    def test_unlock_api(self):
        """测试限售解禁 API"""
        from jk2bt.finance_data import get_unlock_info
        
        df = get_unlock_info("600519.XSHG")
        self.assertIsInstance(df, pd.DataFrame)

    def test_share_change_api(self):
        """测试股东变动 API"""
        from jk2bt.finance_data import get_share_change
        
        df = get_share_change("600519.XSHG")
        self.assertIsInstance(df, pd.DataFrame)

    def test_macro_api(self):
        """测试宏观数据 API"""
        from jk2bt.finance_data import get_macro_indicator
        
        df = get_macro_indicator("gdp")
        self.assertIsInstance(df, pd.DataFrame)

    def test_conversion_bond_api(self):
        """测试可转债 API"""
        from jk2bt.market_data.conversion_bond import get_conversion_bond_list
        
        df = get_conversion_bond_list()
        self.assertIsInstance(df, pd.DataFrame)

    def test_option_api(self):
        """测试期权 API"""
        from jk2bt.market_data.option import get_option_current_em
        
        df = get_option_current_em()
        self.assertIsInstance(df, pd.DataFrame)

    def test_index_components_api(self):
        """测试指数成分股 API"""
        from jk2bt.market_data.index_components import get_index_stocks
        
        df = get_index_stocks("000300.XSHG")
        self.assertIsInstance(df, pd.DataFrame)

    def test_industry_sw_api(self):
        """测试申万行业 API"""
        from jk2bt.market_data.industry_sw import get_industry_list
        
        df = get_industry_list()
        self.assertIsInstance(df, pd.DataFrame)

    def test_finance_module_tables(self):
        """测试 finance 模块新增表"""
        self.assertTrue(hasattr(finance, "STK_SHAREHOLDER_TOP10"))
        self.assertTrue(hasattr(finance, "STK_SHAREHOLDER_NUM"))
        self.assertTrue(hasattr(finance, "STK_XR_XD"))
        self.assertTrue(hasattr(finance, "STK_UNLOCK"))


if __name__ == "__main__":
    unittest.main()
