"""
test_valuation_query.py
TASK_07 valuation表查询单元测试
"""

import unittest
import pandas as pd

from jk2bt.core.strategy_base import (
    get_fundamentals,
    query,
    valuation,
    _QueryBuilder,
    _FieldProxy,
    _apply_filter,
)


class TestQueryBuilder(unittest.TestCase):
    def test_query_builder_init(self):
        """测试 _QueryBuilder 初始化"""
        qb = query(valuation)
        self.assertIsInstance(qb, _QueryBuilder)
        self.assertEqual(qb._tables, [valuation])
        self.assertEqual(qb._limit_n, None)
        self.assertEqual(qb._symbols, None)
        self.assertEqual(qb._filter_expressions, [])

    def test_query_builder_filter_in(self):
        """测试 filter in_ 操作"""
        stocks = ["600519.XSHG", "000858.XSHE"]
        qb = query(valuation).filter(valuation.code.in_(stocks))
        self.assertEqual(qb._symbols, stocks)

    def test_query_builder_filter_comparison(self):
        """测试 filter 比较操作"""
        qb = query(valuation).filter(
            valuation.pb_ratio > 0,
            valuation.pe_ratio > 0,
        )
        self.assertEqual(len(qb._filter_expressions), 2)

    def test_query_builder_limit(self):
        """测试 limit 操作"""
        qb = query(valuation).limit(10)
        self.assertEqual(qb._limit_n, 10)

    def test_query_builder_order_by(self):
        """测试 order_by 操作"""
        qb = query(valuation).order_by(valuation.pb_ratio, ascending=False)
        self.assertEqual(qb._order_field, valuation.pb_ratio)
        self.assertFalse(qb._order_ascending)


class TestFieldProxy(unittest.TestCase):
    def test_field_proxy_init(self):
        """测试 _FieldProxy 初始化"""
        fp = valuation.pe_ratio
        self.assertEqual(fp._table, "valuation")
        self.assertEqual(fp._field, "pe_ratio")
        self.assertIsNone(fp._operator)
        self.assertIsNone(fp._value)

    def test_field_proxy_in(self):
        """测试 in_ 操作"""
        stocks = ["600519.XSHG", "000858.XSHE"]
        result = valuation.code.in_(stocks)
        self.assertEqual(result._symbols, stocks)

    def test_field_proxy_comparison_operators(self):
        """测试比较操作符"""
        fp = valuation.pb_ratio

        fp_gt = valuation.pb_ratio > 0
        self.assertEqual(fp_gt._operator, ">")
        self.assertEqual(fp_gt._value, 0)

        fp_ge = valuation.pb_ratio >= 0
        self.assertEqual(fp_ge._operator, ">=")
        self.assertEqual(fp_ge._value, 0)

        fp_lt = valuation.pb_ratio < 1
        self.assertEqual(fp_lt._operator, "<")
        self.assertEqual(fp_lt._value, 1)

        fp_le = valuation.pb_ratio <= 1
        self.assertEqual(fp_le._operator, "<=")
        self.assertEqual(fp_le._value, 1)

        fp_eq = valuation.pb_ratio == 0.5
        self.assertEqual(fp_eq._operator, "==")
        self.assertEqual(fp_eq._value, 0.5)


class TestApplyFilter(unittest.TestCase):
    def test_apply_filter_greater_than(self):
        """测试 > 过滤"""
        df = pd.DataFrame({"pe_ratio": [10, 20, 30, 40], "pb_ratio": [1, 2, 3, 4]})

        class MockFilter:
            _field = "pe_ratio"
            _operator = ">"
            _value = 25

        result = _apply_filter(df, MockFilter())
        self.assertEqual(len(result), 2)
        self.assertTrue(all(result["pe_ratio"] > 25))

    def test_apply_filter_less_than(self):
        """测试 < 过滤"""
        df = pd.DataFrame({"pe_ratio": [10, 20, 30, 40], "pb_ratio": [1, 2, 3, 4]})

        class MockFilter:
            _field = "pe_ratio"
            _operator = "<"
            _value = 25

        result = _apply_filter(df, MockFilter())
        self.assertEqual(len(result), 2)
        self.assertTrue(all(result["pe_ratio"] < 25))

    def test_apply_filter_equal(self):
        """测试 == 过滤"""
        df = pd.DataFrame({"pe_ratio": [10, 20, 30, 40], "pb_ratio": [1, 2, 3, 4]})

        class MockFilter:
            _field = "pe_ratio"
            _operator = "=="
            _value = 20

        result = _apply_filter(df, MockFilter())
        self.assertEqual(len(result), 1)
        self.assertEqual(result["pe_ratio"].iloc[0], 20)

    def test_apply_filter_missing_field(self):
        """测试字段不存在时的过滤"""
        df = pd.DataFrame({"pe_ratio": [10, 20, 30, 40]})

        class MockFilter:
            _field = "missing_field"
            _operator = ">"
            _value = 25

        result = _apply_filter(df, MockFilter())
        self.assertEqual(len(result), 4)


class TestValuationQuery(unittest.TestCase):
    def test_query_valuation_basic(self):
        """测试基本 valuation 查询"""
        stocks = ["600519.XSHG", "000858.XSHE"]
        qb = query(valuation).filter(valuation.code.in_(stocks))

        self.assertEqual(qb._symbols, stocks)
        self.assertEqual(len(qb._filter_expressions), 0)

    def test_query_valuation_with_filters(self):
        """测试带过滤条件的 valuation 查询"""
        stocks = ["600519.XSHG", "000858.XSHE"]
        qb = query(valuation).filter(
            valuation.code.in_(stocks),
            valuation.pb_ratio > 0,
            valuation.pe_ratio > 0,
        )

        self.assertEqual(qb._symbols, stocks)
        self.assertEqual(len(qb._filter_expressions), 2)

    def test_query_valuation_with_limit(self):
        """测试带 limit 的 valuation 查询"""
        stocks = ["600519.XSHG", "000858.XSHE", "000568.XSHE"]
        qb = query(valuation).filter(valuation.code.in_(stocks)).limit(2)

        self.assertEqual(qb._symbols, stocks)
        self.assertEqual(qb._limit_n, 2)

    def test_get_fundamentals_empty_symbols(self):
        """测试 symbols 为空时返回空 DataFrame"""
        result = get_fundamentals(query(valuation))
        self.assertTrue(result.empty)

    def test_get_fundamentals_dict_input(self):
        """测试 dict 格式输入"""
        result = get_fundamentals({"table": "valuation", "symbols": ["600519.XSHG"]})
        self.assertIsInstance(result, pd.DataFrame)


class TestSupportedFields(unittest.TestCase):
    def test_supported_fields_exist(self):
        """测试支持的字段都存在"""
        supported_fields = [
            "pe_ratio",
            "pb_ratio",
            "ps_ratio",
            "market_cap",
            "dividend_ratio",
        ]

        for field in supported_fields:
            fp = getattr(valuation, field)
            self.assertIsInstance(fp, _FieldProxy)
            self.assertEqual(fp._field, field)


if __name__ == "__main__":
    unittest.main(verbosity=2)
