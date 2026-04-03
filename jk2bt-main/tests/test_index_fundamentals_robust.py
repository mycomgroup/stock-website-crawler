"""
test_index_fundamentals_robust.py

Task 34: 测试指数与基本面接口稳健性增强。

覆盖场景：
- 空结果
- 不支持的指数
- 缓存命中
- 各种参数格式
- entity 参数兼容
"""

import unittest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.core.strategy_base import (
    get_index_weights,
    get_index_stocks,
    get_fundamentals,
    get_history_fundamentals,
    query,
    valuation,
    balance,
    income,
    cash_flow,
    indicator,
    RobustResult,
    SUPPORTED_INDEXES,
    INDEX_CODE_ALIAS_MAP,
)


class TestRobustResult(unittest.TestCase):
    """测试 RobustResult 类"""

    def test_robust_result_success(self):
        """测试成功结果"""
        df = pd.DataFrame({"code": ["600519.XSHG"], "pe_ratio": [30.0]})
        result = RobustResult(
            success=True, data=df, reason="成功获取1条记录", source="network"
        )

        self.assertTrue(result.success)
        self.assertFalse(result.is_empty())
        self.assertEqual(len(result.data), 1)
        self.assertIn("成功", result.reason)

    def test_robust_result_failure(self):
        """测试失败结果"""
        result = RobustResult(
            success=False, data=pd.DataFrame(), reason="网络错误", source="fallback"
        )

        self.assertFalse(result.success)
        self.assertTrue(result.is_empty())
        self.assertIn("网络错误", result.reason)

    def test_robust_result_bool(self):
        """测试布尔转换"""
        success_result = RobustResult(success=True)
        fail_result = RobustResult(success=False)

        self.assertTrue(bool(success_result))
        self.assertFalse(bool(fail_result))

    def test_robust_result_repr(self):
        """测试字符串表示"""
        result = RobustResult(success=True, reason="test")
        repr_str = repr(result)
        self.assertIn("SUCCESS", repr_str)
        self.assertIn("test", repr_str)

    def test_robust_result_with_list_data(self):
        """测试列表数据"""
        result = RobustResult(
            success=True, data=["600519.XSHG", "000858.XSHE"], reason="success"
        )
        self.assertFalse(result.is_empty())
        self.assertEqual(len(result.data), 2)


class TestIndexCodeNormalization(unittest.TestCase):
    """测试指数代码标准化"""

    def test_supported_indexes_coverage(self):
        """测试支持的主要指数覆盖"""
        required_indexes = ["000300", "000016", "000905", "000852", "399006"]
        for idx in required_indexes:
            self.assertIn(idx, SUPPORTED_INDEXES, f"缺少主要指数 '{idx}'")

    def test_index_alias_map(self):
        """测试指数别名映射"""
        self.assertEqual(INDEX_CODE_ALIAS_MAP.get("hs300"), "000300")
        self.assertEqual(INDEX_CODE_ALIAS_MAP.get("沪深300"), "000300")
        self.assertEqual(INDEX_CODE_ALIAS_MAP.get("上证50"), "000016")
        self.assertEqual(INDEX_CODE_ALIAS_MAP.get("中证500"), "000905")
        self.assertEqual(INDEX_CODE_ALIAS_MAP.get("创业板"), "399006")


class TestGetIndexWeightsRobust(unittest.TestCase):
    """测试稳健版指数权重获取"""

    def test_get_index_weights_robust_returns_robust_result(self):
        """测试稳健模式返回 RobustResult"""
        result = get_index_weights("000300.XSHG", robust=True)
        self.assertIsInstance(result, RobustResult)
        self.assertTrue(hasattr(result, "success"))
        self.assertTrue(hasattr(result, "reason"))
        self.assertTrue(hasattr(result, "source"))

    def test_get_index_weights_unsupported_index(self):
        """测试不支持的指数"""
        result = get_index_weights("999999", robust=True)
        self.assertFalse(result.success)
        self.assertIn("支持列表", result.reason)

    def test_get_index_weights_alias(self):
        """测试指数别名"""
        result = get_index_weights("hs300", robust=True)
        self.assertIsInstance(result, RobustResult)

    def test_get_index_weights_non_robust(self):
        """测试非稳健模式返回 DataFrame"""
        result = get_index_weights("000300.XSHG", robust=False)
        self.assertIsInstance(result, pd.DataFrame)


class TestGetIndexStocksRobust(unittest.TestCase):
    """测试稳健版指数成分股获取"""

    def test_get_index_stocks_robust_returns_robust_result(self):
        """测试稳健模式返回 RobustResult"""
        result = get_index_stocks("000300.XSHG", robust=True)
        self.assertIsInstance(result, RobustResult)
        self.assertIsInstance(result.data, list)

    def test_get_index_stocks_unsupported(self):
        """测试不支持的指数"""
        result = get_index_stocks("999999", robust=True)
        self.assertFalse(result.success)
        self.assertIsInstance(result.data, list)
        self.assertEqual(len(result.data), 0)

    def test_get_index_stocks_non_robust(self):
        """测试非稳健模式返回列表"""
        result = get_index_stocks("000300.XSHG", robust=False)
        self.assertIsInstance(result, list)


class TestGetFundamentalsRobust(unittest.TestCase):
    """测试稳健版基本面查询"""

    def test_get_fundamentals_empty_symbols(self):
        """测试空股票列表"""
        result = get_fundamentals(query(valuation), robust=True)
        self.assertFalse(result.success)
        self.assertIn("空", result.reason.lower() + result.reason)

    def test_get_fundamentals_robust_returns_robust_result(self):
        """测试稳健模式返回 RobustResult"""
        stocks = ["600519.XSHG", "000858.XSHE"]
        q = query(valuation).filter(valuation.code.in_(stocks))
        result = get_fundamentals(q, robust=True)
        self.assertIsInstance(result, RobustResult)
        self.assertIsInstance(result.data, pd.DataFrame)

    def test_get_fundamentals_dict_input(self):
        """测试字典格式输入"""
        result = get_fundamentals(
            {"table": "valuation", "symbols": ["600519.XSHG"]}, robust=True
        )
        self.assertIsInstance(result, RobustResult)

    def test_get_fundamentals_schema_fallback(self):
        """测试 schema 保底"""
        result = get_fundamentals(query(valuation), robust=True)
        self.assertIn("code", result.data.columns)

    def test_get_fundamentals_non_robust(self):
        """测试非稳健模式返回 DataFrame"""
        result = get_fundamentals(query(valuation), robust=False)
        self.assertIsInstance(result, pd.DataFrame)


class TestGetHistoryFundamentalsRobust(unittest.TestCase):
    """测试稳健版历史基本面查询"""

    def test_get_history_fundamentals_empty_security(self):
        """测试空股票列表"""
        result = get_history_fundamentals(
            security=None, fields=["balance.total_assets"], robust=True
        )
        self.assertFalse(result.success)
        self.assertIn("空", result.reason.lower() + result.reason)

    def test_get_history_fundamentals_empty_fields(self):
        """测试空字段列表"""
        result = get_history_fundamentals(
            security=["600519.XSHG"], fields=None, robust=True
        )
        self.assertFalse(result.success)

    def test_get_history_fundamentals_entity_parameter(self):
        """测试 entity 参数"""
        result = get_history_fundamentals(
            entity=["600519.XSHG"], fields=["balance.total_assets"], robust=True
        )
        self.assertIsInstance(result, RobustResult)

    def test_get_history_fundamentals_non_robust(self):
        """测试非稳健模式返回 DataFrame"""
        result = get_history_fundamentals(
            security=["600519.XSHG"], fields=["balance.total_assets"], robust=False
        )
        self.assertIsInstance(result, pd.DataFrame)


class TestEmptyResultHandling(unittest.TestCase):
    """测试空结果处理"""

    def test_empty_result_has_schema(self):
        """测试空结果有 schema"""
        result = get_fundamentals(query(valuation), robust=True)
        self.assertFalse(result.data.columns.empty)
        self.assertIn("code", result.data.columns)

    def test_empty_result_for_unsupported_index(self):
        """测试不支持指数返回空结果"""
        result = get_index_stocks("999999", robust=True)
        self.assertFalse(result.success)
        self.assertEqual(len(result.data), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
