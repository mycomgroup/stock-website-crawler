import unittest

from jk2bt.core.strategy_base import (
    get_index_weights,
    get_index_stocks,
    SUPPORTED_INDEXES,
)


class TestIndexAPIs(unittest.TestCase):
    def test_get_index_weights_hs300(self):
        """测试获取沪深300权重"""
        weights = get_index_weights("000300.XSHG")
        self.assertFalse(weights.empty, "权重数据不应为空")
        self.assertIn("weight", weights.columns, "应包含weight列")
        self.assertGreater(len(weights), 100, "沪深300应至少有100只成分股")

    def test_get_index_stocks_hs300(self):
        """测试获取沪深300成分股"""
        stocks = get_index_stocks("000300.XSHG")
        self.assertGreater(len(stocks), 100, "沪深300应至少有100只成分股")
        self.assertTrue(
            all(".XSHG" in s or ".XSHE" in s for s in stocks),
            "所有股票代码应为聚宽格式",
        )

    def test_get_index_weights_format(self):
        """测试不同代码格式"""
        weights1 = get_index_weights("000300")
        weights2 = get_index_weights("000300.XSHG")
        self.assertEqual(
            len(weights1), len(weights2), "不同格式的指数代码应返回相同数量的成分股"
        )

    def test_cache_mechanism(self):
        """测试缓存机制"""
        weights1 = get_index_weights("000300.XSHG")
        weights2 = get_index_stocks("000300.XSHG")
        self.assertEqual(len(weights1), len(weights2), "权重表和成分股列表应一致")

    def test_supported_indexes(self):
        """测试支持的指数列表"""
        self.assertIn("000300", SUPPORTED_INDEXES)
        self.assertIn("000016", SUPPORTED_INDEXES)
        self.assertIn("000905", SUPPORTED_INDEXES)
        self.assertIn("000852", SUPPORTED_INDEXES)

    def test_unsupported_index(self):
        """测试不支持的指数"""
        weights = get_index_weights("999999")
        self.assertTrue(weights.empty, "不支持的指数应返回空DataFrame")


if __name__ == "__main__":
    unittest.main(verbosity=2)
