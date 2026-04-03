import unittest

from jk2bt.core.strategy_base import GlobalState


class TestGlobalState(unittest.TestCase):
    def test_set_and_get(self):
        """测试设置和获取属性"""
        g = GlobalState()
        g.index = "000300.XSHG"
        self.assertEqual(g.index, "000300.XSHG")

    def test_list_value(self):
        """测试列表值存储"""
        g = GlobalState()
        g.stocks = ["600519.XSHG", "000001.XSHE"]
        self.assertEqual(len(g.stocks), 2)

    def test_dict_value(self):
        """测试字典值存储"""
        g = GlobalState()
        g.params = {"num": 10, "days": 20}
        self.assertEqual(g.params["num"], 10)

    def test_contains(self):
        """测试in语法"""
        g = GlobalState()
        g.value = 100
        self.assertTrue("value" in g)
        self.assertFalse("missing" in g)

    def test_get_with_default(self):
        """测试get方法带默认值"""
        g = GlobalState()
        self.assertEqual(g.get("missing", 42), 42)

    def test_delete(self):
        """测试删除属性"""
        g = GlobalState()
        g.temp = "value"
        del g.temp
        self.assertIsNone(g.temp)

    def test_clear(self):
        """测试清空"""
        g = GlobalState()
        g.a = 1
        g.b = 2
        g.clear()
        self.assertIsNone(g.a)
        self.assertIsNone(g.b)

    def test_none_value(self):
        """测试访问不存在属性返回None"""
        g = GlobalState()
        self.assertIsNone(g.nonexistent)

    def test_set_method(self):
        """测试set方法"""
        g = GlobalState()
        g.set("num", 10)
        self.assertEqual(g.num, 10)

    def test_items(self):
        """测试items方法"""
        g = GlobalState()
        g.a = 1
        g.b = 2
        items = dict(g.items())
        self.assertEqual(items["a"], 1)
        self.assertEqual(items["b"], 2)

    def test_numeric_value(self):
        """测试数值存储"""
        g = GlobalState()
        g.num = 10
        g.factor_score = 0.5
        self.assertEqual(g.num, 10)
        self.assertEqual(g.factor_score, 0.5)

    def test_update_value(self):
        """测试更新已存在的属性"""
        g = GlobalState()
        g.stocks = []
        g.stocks = ["600519.XSHG"]
        self.assertEqual(g.stocks, ["600519.XSHG"])

    def test_private_attribute(self):
        """测试私有属性不受影响"""
        g = GlobalState()
        g._private = "should not be stored in _state"
        self.assertEqual(g._private, "should not be stored in _state")


if __name__ == "__main__":
    unittest.main()
