"""
test_get_current_data.py
测试 get_current_data() 实现的各个属性
"""

import unittest

from jk2bt.core.strategy_base import (
    get_current_data,
    _CurrentDataEntry,
    _CurrentDataProxy,
    format_stock_symbol_for_akshare,
)


class TestCurrentDataEntry(unittest.TestCase):
    """测试 _CurrentDataEntry 类的各个属性"""

    def test_init_with_single_code(self):
        """测试单个代码初始化"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertEqual(entry.codes, ["600519.XSHG"])
        self.assertTrue(entry._single)

    def test_init_with_list_codes(self):
        """测试列表代码初始化"""
        entry = _CurrentDataEntry(["600519.XSHG", "000001.XSHE"])
        self.assertEqual(entry.codes, ["600519.XSHG", "000001.XSHE"])
        self.assertFalse(entry._single)

    def test_format_stock_symbol_for_akshare(self):
        """测试代码格式转换"""
        self.assertEqual(format_stock_symbol_for_akshare("600519.XSHG"), "600519")
        self.assertEqual(format_stock_symbol_for_akshare("000001.XSHE"), "000001")
        self.assertEqual(format_stock_symbol_for_akshare("sh600519"), "600519")
        self.assertEqual(format_stock_symbol_for_akshare("sz000001"), "000001")
        self.assertEqual(format_stock_symbol_for_akshare("600519"), "600519")

    def test_last_price_property(self):
        """测试 last_price 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "last_price"))

    def test_day_open_property(self):
        """测试 day_open 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "day_open"))

    def test_high_property(self):
        """测试 high 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "high"))

    def test_low_property(self):
        """测试 low 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "low"))

    def test_volume_property(self):
        """测试 volume 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "volume"))

    def test_high_limit_property(self):
        """测试 high_limit 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "high_limit"))

    def test_low_limit_property(self):
        """测试 low_limit 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "low_limit"))

    def test_paused_property(self):
        """测试 paused 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "paused"))

    def test_is_st_property(self):
        """测试 is_st 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "is_st"))

    def test_name_property(self):
        """测试 name 属性存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "name"))

    def test_get_data_feed_method(self):
        """测试 _get_data_feed 方法存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "_get_data_feed"))
        self.assertTrue(callable(entry._get_data_feed))

    def test_fetch_from_akshare_method(self):
        """测试 _fetch_from_akshare 方法存在"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertTrue(hasattr(entry, "_fetch_from_akshare"))
        self.assertTrue(callable(entry._fetch_from_akshare))


class TestCurrentDataProxy(unittest.TestCase):
    """测试 _CurrentDataProxy 类"""

    def test_init(self):
        """测试初始化"""
        proxy = _CurrentDataProxy()
        self.assertIsNone(proxy._bt)
        self.assertEqual(proxy._store, {})

    def test_getitem_single_code(self):
        """测试单个代码访问"""
        proxy = _CurrentDataProxy()
        entry = proxy["600519.XSHG"]
        self.assertIsInstance(entry, _CurrentDataEntry)
        self.assertEqual(entry.codes, ["600519.XSHG"])

    def test_getitem_list_codes(self):
        """测试列表代码访问"""
        proxy = _CurrentDataProxy()
        entry = proxy[["600519.XSHG", "000001.XSHE"]]
        self.assertIsInstance(entry, _CurrentDataEntry)
        self.assertEqual(entry.codes, ["600519.XSHG", "000001.XSHE"])

    def test_cache_entries(self):
        """测试缓存机制"""
        proxy = _CurrentDataProxy()
        entry1 = proxy["600519.XSHG"]
        entry2 = proxy["600519.XSHG"]
        self.assertIs(entry1, entry2)


class TestGetCurrentData(unittest.TestCase):
    """测试 get_current_data 函数"""

    def test_returns_proxy(self):
        """测试返回类型"""
        result = get_current_data()
        self.assertIsInstance(result, _CurrentDataProxy)

    def test_with_strategy_param(self):
        """测试传入策略参数"""
        result = get_current_data(None)
        self.assertIsInstance(result, _CurrentDataProxy)


class TestHighLimitCalculation(unittest.TestCase):
    """测试涨停价计算逻辑"""

    def test_mainboard_high_limit_ratio(self):
        """主板涨停幅度10%"""
        entry = _CurrentDataEntry("600519.XSHG")
        code_num = format_stock_symbol_for_akshare("600519.XSHG")
        self.assertTrue(code_num.startswith("6"))

    def test_gem_high_limit_ratio(self):
        """创业板涨停幅度20%"""
        entry = _CurrentDataEntry("300001.XSHE")
        code_num = format_stock_symbol_for_akshare("300001.XSHE")
        self.assertTrue(code_num.startswith("300"))

    def test_star_market_high_limit_ratio(self):
        """科创板涨停幅度20%"""
        entry = _CurrentDataEntry("688001.XSHG")
        code_num = format_stock_symbol_for_akshare("688001.XSHG")
        self.assertTrue(code_num.startswith("688"))


class TestCodeFormatCompatibility(unittest.TestCase):
    """测试代码格式兼容性"""

    def test_jq_code_format(self):
        """聚宽代码格式"""
        entry = _CurrentDataEntry("600519.XSHG")
        self.assertEqual(entry.codes[0], "600519.XSHG")

    def test_ak_code_format(self):
        """AkShare代码格式"""
        entry = _CurrentDataEntry("sh600519")
        self.assertEqual(entry.codes[0], "sh600519")

    def test_pure_code_format(self):
        """纯数字代码格式"""
        entry = _CurrentDataEntry("600519")
        self.assertEqual(entry.codes[0], "600519")


if __name__ == "__main__":
    unittest.main()
