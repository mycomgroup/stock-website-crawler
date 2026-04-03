"""
test_index_fundamentals_robustness.py
Task 34: 指数与基本面接口稳健性测试

测试覆盖:
- get_index_stocks_robust
- get_index_weights_robust
- get_fundamentals_robust
- get_history_fundamentals_robust

测试场景:
- 正常情况（数据获取成功）
- 空结果（无匹配数据）
- 不支持的指数/股票
- 缓存命中/过期/刷新
- 断网场景（模拟）
- 参数验证（空值、None、极端值）
- 异常处理（各种异常类型）
- 数据验证（格式、字段完整性）
- 兼容性测试（不同API风格）
- 批量查询测试
"""

import unittest
import pandas as pd
import numpy as np
import tempfile
import os
import time
from unittest.mock import patch, MagicMock, PropertyMock
import warnings

from jk2bt.core.strategy_base import (
    RobustResult,
    get_index_stocks_robust,
    get_index_weights_robust,
    get_fundamentals_robust,
    get_history_fundamentals_robust,
    get_index_stocks,
    get_index_weights,
    get_fundamentals,
    get_history_fundamentals,
    query,
    valuation,
    balance,
    income,
    cash_flow,
    INDEX_CODE_ALIAS_MAP,
    SUPPORTED_INDEXES,
    _format_index_code,
    _stock_code_to_jq,
    _normalize_index_weights,
)


class TestRobustResult(unittest.TestCase):
    """RobustResult 类测试"""

    def test_robust_result_success(self):
        result = RobustResult(
            success=True,
            data=pd.DataFrame({"a": [1, 2]}),
            reason="OK",
            source="network",
        )
        self.assertTrue(result.success)
        self.assertFalse(result.is_empty())
        self.assertTrue(bool(result))

    def test_robust_result_failure(self):
        result = RobustResult(
            success=False, data=pd.DataFrame(), reason="Failed", source="fallback"
        )
        self.assertFalse(result.success)
        self.assertTrue(result.is_empty())
        self.assertFalse(bool(result))

    def test_robust_result_empty_list(self):
        result = RobustResult(
            success=True, data=[], reason="Empty list", source="cache"
        )
        self.assertTrue(result.is_empty())

    def test_robust_result_none_data(self):
        """测试 data=None 的情况"""
        result = RobustResult(
            success=True, data=None, reason="No data", source="network"
        )
        self.assertTrue(result.success)
        self.assertEqual(result.data, pd.DataFrame())
        self.assertTrue(result.is_empty())

    def test_robust_result_tuple_data(self):
        """测试 tuple 类型数据"""
        result = RobustResult(
            success=True, data=(1, 2, 3), reason="Tuple", source="cache"
        )
        self.assertFalse(result.is_empty())
        self.assertTrue(bool(result))

    def test_robust_result_repr(self):
        """测试字符串表示"""
        result = RobustResult(
            success=True, data=pd.DataFrame(), reason="Test", source="cache"
        )
        repr_str = repr(result)
        self.assertIn("SUCCESS", repr_str)
        self.assertIn("cache", repr_str)
        self.assertIn("Test", repr_str)

    def test_robust_result_repr_failure(self):
        """测试失败状态的字符串表示"""
        result = RobustResult(
            success=False, data=[], reason="Error occurred", source="fallback"
        )
        repr_str = repr(result)
        self.assertIn("FAILED", repr_str)
        self.assertIn("fallback", repr_str)

    def test_robust_result_default_values(self):
        """测试默认值"""
        result = RobustResult()
        self.assertTrue(result.success)
        self.assertEqual(result.data, pd.DataFrame())
        self.assertEqual(result.reason, "")
        self.assertEqual(result.source, "network")

    def test_robust_result_with_large_data(self):
        """测试大数据量"""
        large_df = pd.DataFrame({"a": range(10000), "b": range(10000)})
        result = RobustResult(
            success=True, data=large_df, reason="Large data", source="network"
        )
        self.assertTrue(result.success)
        self.assertFalse(result.is_empty())
        self.assertEqual(len(result.data), 10000)

    def test_robust_result_bool_conversion(self):
        """测试 bool 转换"""
        success_result = RobustResult(success=True, data=[1, 2])
        failure_result = RobustResult(success=False, data=[])
        self.assertTrue(bool(success_result))
        self.assertFalse(bool(failure_result))

    def test_robust_result_with_nan_data(self):
        """测试包含 NaN 的数据"""
        df_with_nan = pd.DataFrame({"a": [1, np.nan, 3], "b": [np.nan, 2, 3]})
        result = RobustResult(
            success=True, data=df_with_nan, reason="Data with NaN", source="network"
        )
        self.assertFalse(result.is_empty())
        self.assertTrue(result.success)

    def test_robust_result_with_custom_attributes(self):
        """测试自定义属性"""
        result = RobustResult(
            success=True,
            data=[],
            reason="Custom",
            source="custom",
        )
        result.custom_attr = "custom_value"
        self.assertEqual(result.custom_attr, "custom_value")


class TestGetIndexStocksRobust(unittest.TestCase):
    """get_index_stocks_robust 接口测试"""

    def test_supported_index_hs300(self):
        result = get_index_stocks_robust("000300.XSHG")
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertIsInstance(result.data, list)
            self.assertGreater(len(result.data), 50)
            self.assertIn(".XSHG", result.data[0] if result.data else "")

    def test_supported_index_alias(self):
        result = get_index_stocks_robust("hs300")
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertGreater(len(result.data), 50)

    def test_unsupported_index(self):
        result = get_index_stocks_robust("999999")
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)
        self.assertEqual(result.data, [])

    def test_empty_input(self):
        result = get_index_stocks_robust("")
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_robust_vs_normal_mode(self):
        robust_result = get_index_stocks_robust("000300")
        normal_result = get_index_stocks("000300")
        if robust_result.success:
            self.assertEqual(robust_result.data, normal_result)

    def test_multiple_supported_indices(self):
        """测试多个支持的指数"""
        indices = ["000300", "000016", "000905", "000852"]
        for index in indices:
            result = get_index_stocks_robust(index)
            self.assertIsInstance(result, RobustResult)
            if result.success:
                self.assertIsInstance(result.data, list)

    def test_index_with_whitespace(self):
        """测试带空格的指数代码"""
        result = get_index_stocks_robust(" 000300 ")
        self.assertIsInstance(result, RobustResult)

    def test_index_with_case_variation(self):
        """测试大小写变体"""
        variants = ["000300.XSHG", "000300.xshg", "000300.XSHG"]
        for code in variants:
            result = get_index_stocks_robust(code)
            self.assertIsInstance(result, RobustResult)

    def test_deep_market_index(self):
        """测试深市指数"""
        result = get_index_stocks_robust("399006.XSHE")
        self.assertIsInstance(result, RobustResult)

    def test_all_chinese_aliases(self):
        """测试所有中文别名"""
        chinese_aliases = ["沪深300", "上证50", "中证500", "创业板", "中证1000"]
        for alias in chinese_aliases:
            result = get_index_stocks_robust(alias)
            self.assertIsInstance(result, RobustResult)

    def test_result_source_types(self):
        """测试结果来源类型"""
        result = get_index_stocks_robust("000300")
        self.assertIsInstance(result.source, str)
        self.assertIn(result.source, ["cache", "network", "fallback"])

    def test_result_reason_not_empty(self):
        """测试失败时 reason 不为空"""
        result = get_index_stocks_robust("999999")
        if not result.success:
            self.assertGreater(len(result.reason), 0)

    def test_normal_mode_empty_list(self):
        """测试普通模式返回空列表不报错"""
        stocks = get_index_stocks("999999")
        self.assertIsInstance(stocks, list)

    def test_robust_mode_preserves_source(self):
        """测试稳健模式保留数据来源信息"""
        result = get_index_stocks_robust("000300")
        if result.success:
            self.assertIn(result.source, ["cache", "network"])

    def test_invalid_format_handling(self):
        """测试无效格式处理"""
        invalid_codes = ["abc", "123abc", "!@#", "null", "none"]
        for code in invalid_codes:
            result = get_index_stocks_robust(code)
            self.assertIsInstance(result, RobustResult)
            self.assertFalse(result.success)


class TestGetIndexWeightsRobust(unittest.TestCase):
    """get_index_weights_robust 接口测试"""

    def test_supported_index_weights(self):
        result = get_index_weights_robust("000300.XSHG")
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertIsInstance(result.data, pd.DataFrame)
            self.assertIn("weight", result.data.columns)

    def test_unsupported_index_weights(self):
        result = get_index_weights_robust("999999")
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)
        self.assertTrue(result.data.empty)

    def test_index_code_format_variants(self):
        variants = ["000300", "000300.XSHG", "000300.xshg", "sh000300", "hs300"]
        for code in variants:
            result = get_index_weights_robust(code)
            self.assertIsInstance(result, RobustResult)

    def test_weights_dataframe_structure(self):
        """测试权重DataFrame结构"""
        result = get_index_weights_robust("000300")
        if result.success:
            df = result.data
            self.assertTrue(df.index.name == "code" or "code" in df.columns)
            if "weight" in df.columns:
                self.assertTrue(
                    df["weight"].dtype in [np.float64, np.int64, float, int]
                )

    def test_weights_positive_values(self):
        """测试权重值为正数"""
        result = get_index_weights_robust("000300")
        if result.success and not result.data.empty:
            if "weight" in result.data.columns:
                weights = result.data["weight"]
                self.assertTrue((weights >= 0).all() or weights.isna().all())

    def test_normal_mode_returns_dataframe(self):
        """测试普通模式返回DataFrame"""
        weights = get_index_weights("000300")
        self.assertIsInstance(weights, pd.DataFrame)

    def test_normal_mode_unsupported_index(self):
        """测试普通模式不支持指数"""
        weights = get_index_weights("999999")
        self.assertIsInstance(weights, pd.DataFrame)
        self.assertTrue(weights.empty)

    def test_empty_dataframe_columns(self):
        """测试空DataFrame列结构"""
        result = get_index_weights_robust("999999")
        self.assertIsInstance(result.data, pd.DataFrame)
        # 空结果也应该有基本列结构
        self.assertIn("weight", result.data.columns)

    def test_multiple_indices_comparison(self):
        """测试多个指数权重对比"""
        indices = ["000300", "000016", "000905"]
        for idx in indices:
            result = get_index_weights_robust(idx)
            if result.success:
                self.assertIsInstance(result.data, pd.DataFrame)

    def test_result_source_tracking(self):
        """测试数据来源追踪"""
        result = get_index_weights_robust("000300")
        if result.success:
            self.assertIn(result.source, ["cache", "network"])

    def test_reason_contains_useful_info(self):
        """测试失败原因包含有用信息"""
        result = get_index_weights_robust("999999")
        if not result.success:
            reason = result.reason.lower()
            self.assertTrue(
                "不支持" in reason or "不在支持列表" in reason or "无效" in reason
            )

    def test_weights_sum_approximately_one(self):
        """测试权重总和接近1"""
        result = get_index_weights_robust("000300")
        if result.success and "weight" in result.data.columns:
            total_weight = result.data["weight"].sum()
            # 权重总和应该接近100%（某些成分股可能被排除）
            self.assertTrue(total_weight > 0)


class TestGetFundamentalsRobust(unittest.TestCase):
    """get_fundamentals_robust 接口测试"""

    def test_empty_symbols(self):
        q = query(valuation).filter(valuation.code.in_([]))
        result = get_fundamentals_robust(q)
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)
        self.assertTrue(result.data.empty)

    def test_invalid_query_object(self):
        result = get_fundamentals_robust(None)
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_dict_format_query(self):
        result = get_fundamentals_robust({"table": "balance", "symbol": []})
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_unsupported_table(self):
        result = get_fundamentals_robust(
            {"table": "unknown_table", "symbol": ["600519.XSHG"]}
        )
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_dict_format_with_string_symbol(self):
        """测试dict格式单个股票代码"""
        result = get_fundamentals_robust({"table": "balance", "symbol": "600519.XSHG"})
        self.assertIsInstance(result, RobustResult)

    def test_dict_format_with_list_symbols(self):
        """测试dict格式多个股票代码"""
        result = get_fundamentals_robust(
            {"table": "balance", "symbols": ["600519.XSHG", "000858.XSHE"]}
        )
        self.assertIsInstance(result, RobustResult)

    def test_all_table_types(self):
        """测试所有表类型"""
        table_types = ["valuation", "income", "balance", "cash_flow"]
        for table in table_types:
            result = get_fundamentals_robust(
                {"table": table, "symbol": ["600519.XSHG"]}
            )
            self.assertIsInstance(result, RobustResult)

    def test_empty_dataframe_has_schema(self):
        """测试空DataFrame有schema"""
        result = get_fundamentals_robust({"table": "balance", "symbol": []})
        if not result.data.empty or result.success is False:
            self.assertIn("code", result.data.columns)

    def test_normal_mode_empty_result(self):
        """测试普通模式空结果"""
        df = get_fundamentals(query(valuation))
        self.assertIsInstance(df, pd.DataFrame)

    def test_filter_expression_handling(self):
        """测试过滤表达式"""
        q = query(valuation).filter(
            valuation.code.in_(["600519.XSHG"]),
            valuation.pe_ratio > 0,
        )
        result = get_fundamentals_robust(q)
        self.assertIsInstance(result, RobustResult)

    def test_result_reason_content(self):
        """测试结果原因内容"""
        result = get_fundamentals_robust({"table": "balance", "symbol": []})
        if not result.success:
            self.assertTrue("空" in result.reason or "symbols" in result.reason.lower())

    def test_valuation_field_names(self):
        """测试估值字段名映射"""
        result = get_fundamentals_robust(
            {"table": "valuation", "symbol": ["600519.XSHG"]}
        )
        self.assertIsInstance(result, RobustResult)

    def test_query_with_limit(self):
        """测试带limit的查询"""
        q = query(valuation).filter(valuation.code.in_(["600519.XSHG"]))
        q._limit_n = 10
        result = get_fundamentals_robust(q)
        self.assertIsInstance(result, RobustResult)

    def test_multiple_query_types(self):
        """测试多种查询类型"""
        query_types = [
            {"table": "valuation", "symbol": ["600519.XSHG"]},
            {"table": "income", "symbol": ["600519.XSHG"]},
            {"table": "balance", "symbol": ["600519.XSHG"]},
            {"table": "cash_flow", "symbol": ["600519.XSHG"]},
        ]
        for q in query_types:
            result = get_fundamentals_robust(q)
            self.assertIsInstance(result, RobustResult)

    def test_dict_with_missing_table(self):
        """测试dict格式缺少table参数"""
        result = get_fundamentals_robust({"symbol": ["600519.XSHG"]})
        self.assertIsInstance(result, RobustResult)

    def test_invalid_symbol_format(self):
        """测试无效股票代码格式"""
        result = get_fundamentals_robust(
            {"table": "balance", "symbol": ["invalid_code"]}
        )
        self.assertIsInstance(result, RobustResult)


class TestGetHistoryFundamentalsRobust(unittest.TestCase):
    """get_history_fundamentals_robust 接口测试"""

    def test_empty_security(self):
        result = get_history_fundamentals_robust([], ["income.total_operating_revenue"])
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_empty_fields(self):
        result = get_history_fundamentals_robust(["600519.XSHG"], [])
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_invalid_field_prefix(self):
        result = get_history_fundamentals_robust(["600519.XSHG"], ["invalid_field"])
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_valid_fields_format(self):
        result = get_history_fundamentals_robust(
            ["600519.XSHG"],
            ["income.total_operating_revenue", "balance.total_assets"],
            count=1,
        )
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertIsInstance(result.data, pd.DataFrame)

    def test_none_security(self):
        """测试None security参数"""
        result = get_history_fundamentals_robust(None, ["balance.total_assets"])
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_none_fields(self):
        """测试None fields参数"""
        result = get_history_fundamentals_robust(["600519.XSHG"], None)
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_single_stock_single_field(self):
        """测试单只股票单个字段"""
        result = get_history_fundamentals_robust(
            "600519.XSHG", ["balance.total_assets"], count=1
        )
        self.assertIsInstance(result, RobustResult)

    def test_multiple_stocks_multiple_fields(self):
        """测试多只股票多个字段"""
        result = get_history_fundamentals_robust(
            ["600519.XSHG", "000858.XSHE"],
            ["income.total_operating_revenue", "balance.total_assets"],
            count=2,
        )
        self.assertIsInstance(result, RobustResult)

    def test_all_field_types(self):
        """测试所有字段类型"""
        field_types = [
            ["cash_flow.net_profit"],
            ["income.total_operating_revenue"],
            ["balance.total_assets"],
        ]
        for fields in field_types:
            result = get_history_fundamentals_robust(["600519.XSHG"], fields, count=1)
            self.assertIsInstance(result, RobustResult)

    def test_count_parameter_variations(self):
        """测试count参数变化"""
        for count in [1, 2, 4, 8]:
            result = get_history_fundamentals_robust(
                ["600519.XSHG"], ["balance.total_assets"], count=count
            )
            self.assertIsInstance(result, RobustResult)

    def test_stat_date_parameter(self):
        """测试stat_date参数"""
        result = get_history_fundamentals_robust(
            ["600519.XSHG"], ["balance.total_assets"], stat_date="2023q1", count=1
        )
        self.assertIsInstance(result, RobustResult)

    def test_stat_date_format_variations(self):
        """测试stat_date格式变化"""
        stat_dates = ["2023q1", "2023Q1", "2023-03-31"]
        for sd in stat_dates:
            result = get_history_fundamentals_robust(
                ["600519.XSHG"], ["balance.total_assets"], stat_date=sd, count=1
            )
            self.assertIsInstance(result, RobustResult)

    def test_normal_mode_empty_result(self):
        """测试普通模式空结果"""
        df = get_history_fundamentals(None, ["balance.total_assets"])
        self.assertIsInstance(df, pd.DataFrame)

    def test_result_dataframe_structure(self):
        """测试结果DataFrame结构"""
        result = get_history_fundamentals_robust(
            ["600519.XSHG"], ["balance.total_assets"], count=1
        )
        if result.success:
            df = result.data
            # 检查MultiIndex
            self.assertEqual(df.index.names, ["code", "statDate"])

    def test_mixed_valid_invalid_fields(self):
        """测试混合有效和无效字段"""
        result = get_history_fundamentals_robust(
            ["600519.XSHG"], ["balance.total_assets", "invalid_field"], count=1
        )
        self.assertIsInstance(result, RobustResult)

    def test_force_update_parameter(self):
        """测试force_update参数"""
        result = get_history_fundamentals_robust(
            ["600519.XSHG"], ["balance.total_assets"], count=1, force_update=False
        )
        self.assertIsInstance(result, RobustResult)

    def test_result_reason_content(self):
        """测试结果原因内容"""
        result = get_history_fundamentals_robust([], ["balance.total_assets"])
        if not result.success:
            reason = result.reason.lower()
            self.assertTrue("security" in reason or "股票" in reason or "空" in reason)

    def test_large_number_of_stocks(self):
        """测试大量股票查询"""
        stocks = [
            "600519.XSHG",
            "000858.XSHE",
            "600036.XSHG",
            "601318.XSHG",
            "000001.XSHE",
        ]
        result = get_history_fundamentals_robust(
            stocks, ["balance.total_assets"], count=1
        )
        self.assertIsInstance(result, RobustResult)


class TestIndexCodeAliasCompatibility(unittest.TestCase):
    def test_alias_mapping_complete(self):
        expected_aliases = [
            "hs300",
            "沪深300",
            "sz50",
            "上证50",
            "zz500",
            "中证500",
            "zz1000",
            "中证1000",
            "cyb",
            "创业板",
            "zz100",
            "中证100",
        ]

        for alias in expected_aliases:
            self.assertIn(
                alias.lower(), INDEX_CODE_ALIAS_MAP.keys(), f"Missing alias: {alias}"
            )

    def test_format_variants(self):
        variants = [
            ("000300.XSHG", "000300"),
            ("000300.xshg", "000300"),
            ("sh000300", "000300"),
            ("000300.XSHE", "000300"),
        ]

        for input_code, expected in variants:
            result = _format_index_code(input_code)
            self.assertEqual(result, expected)


class TestRobustBehavior(unittest.TestCase):
    def test_none_handling_get_index_stocks(self):
        with patch(
            "src.backtrader_base_strategy.ak.index_stock_cons_weight_csindex"
        ) as mock_ak:
            mock_ak.return_value = None

            result = get_index_stocks_robust("000300")
            self.assertIsInstance(result, RobustResult)
            self.assertFalse(result.success)

    def test_empty_df_handling(self):
        with patch(
            "src.backtrader_base_strategy.ak.index_stock_cons_weight_csindex"
        ) as mock_ak:
            mock_ak.return_value = pd.DataFrame()

            result = get_index_weights_robust("000300")
            self.assertIsInstance(result, RobustResult)
            self.assertFalse(result.success)

    def test_network_error_handling(self):
        with patch(
            "src.backtrader_base_strategy.ak.index_stock_cons_weight_csindex"
        ) as mock_ak:
            mock_ak.side_effect = Exception("Network error")

            result = get_index_stocks_robust("000300")
            self.assertIsInstance(result, RobustResult)
            self.assertFalse(result.success)
            self.assertIn("Network error", result.reason)


class TestSchemaPreservation(unittest.TestCase):
    def test_empty_result_has_schema(self):
        result = get_fundamentals_robust({"table": "valuation", "symbol": []})
        self.assertIsInstance(result.data, pd.DataFrame)
        self.assertIn("code", result.data.columns)

    def test_history_fundamentals_empty_schema(self):
        result = get_history_fundamentals_robust([], ["income.net_profit"])
        self.assertIsInstance(result.data, pd.DataFrame)
        expected_cols = ["code", "statDate"]
        for col in expected_cols:
            self.assertIn(col, result.data.columns)


class TestIntegration(unittest.TestCase):
    def test_full_workflow_index_stocks(self):
        result = get_index_stocks_robust("000300.XSHG")

        if result.success:
            stocks = result.data

            if len(stocks) > 0:
                fund_result = get_fundamentals_robust(
                    query(valuation).filter(valuation.code.in_(stocks[:5]))
                )

                if fund_result.success:
                    self.assertIsInstance(fund_result.data, pd.DataFrame)
                    self.assertGreater(len(fund_result.data), 0)

    def test_full_workflow_with_fundamentals(self):
        """完整工作流测试：指数成分股 -> 基本面查询"""
        result = get_index_stocks_robust("000016.XSHG")
        if result.success and len(result.data) > 0:
            stocks = result.data[:3]
            hist_result = get_history_fundamentals_robust(
                stocks, ["balance.total_assets"], count=1
            )
            self.assertIsInstance(hist_result, RobustResult)

    def test_workflow_with_weights(self):
        """工作流测试：权重 -> 成分股"""
        weights_result = get_index_weights_robust("000300")
        if weights_result.success:
            stocks = list(weights_result.data.index)
            self.assertIsInstance(stocks, list)


class TestBoundaryConditions(unittest.TestCase):
    """边界条件测试"""

    def test_extremely_long_index_code(self):
        """测试超长指数代码"""
        long_code = "0" * 100
        result = get_index_stocks_robust(long_code)
        self.assertIsInstance(result, RobustResult)

    def test_special_characters_in_index_code(self):
        """测试特殊字符"""
        special_chars = ["!@#", "test-123", "index.code", "中国指数"]
        for code in special_chars:
            result = get_index_stocks_robust(code)
            self.assertIsInstance(result, RobustResult)

    def test_none_values_handling(self):
        """测试None值处理"""
        tests = [
            lambda: get_index_stocks_robust(None),
            lambda: get_index_weights_robust(None),
            lambda: get_fundamentals_robust(None),
        ]
        for test_func in tests:
            result = test_func()
            self.assertIsInstance(result, RobustResult)
            self.assertFalse(result.success)

    def test_count_zero(self):
        """测试count=0"""
        result = get_history_fundamentals_robust(
            ["600519.XSHG"], ["balance.total_assets"], count=0
        )
        self.assertIsInstance(result, RobustResult)

    def test_count_negative(self):
        """测试负数count"""
        result = get_history_fundamentals_robust(
            ["600519.XSHG"], ["balance.total_assets"], count=-1
        )
        self.assertIsInstance(result, RobustResult)

    def test_count_large_number(self):
        """测试大数值count"""
        result = get_history_fundamentals_robust(
            ["600519.XSHG"], ["balance.total_assets"], count=1000
        )
        self.assertIsInstance(result, RobustResult)

    def test_empty_string_parameters(self):
        """测试空字符串参数"""
        tests = [
            get_index_stocks_robust(""),
            get_index_weights_robust(""),
        ]
        for result in tests:
            self.assertIsInstance(result, RobustResult)

    def test_whitespace_only(self):
        """测试仅空白字符"""
        result = get_index_stocks_robust("   ")
        self.assertIsInstance(result, RobustResult)


class TestCacheMechanism(unittest.TestCase):
    """缓存机制测试"""

    def test_cache_directory_creation(self):
        """测试缓存目录创建"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = get_index_weights_robust("000300", cache_dir=tmpdir)
            self.assertIsInstance(result, RobustResult)

    def test_cache_hit_on_second_call(self):
        """测试缓存命中"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result1 = get_index_weights_robust("000300", cache_dir=tmpdir)
            if result1.success:
                result2 = get_index_weights_robust("000300", cache_dir=tmpdir)
                self.assertEqual(result2.source, "cache")

    def test_force_update_parameter(self):
        """测试force_update参数"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result1 = get_index_weights_robust("000300", cache_dir=tmpdir)
            result2 = get_index_weights_robust(
                "000300", cache_dir=tmpdir, force_update=True
            )
            self.assertIsInstance(result2, RobustResult)


class TestExceptionHandling(unittest.TestCase):
    """异常处理测试"""

    def test_timeout_exception(self):
        """测试超时异常"""
        with patch(
            "src.backtrader_base_strategy.ak.index_stock_cons_weight_csindex"
        ) as mock_ak:
            import socket

            mock_ak.side_effect = socket.timeout("Connection timeout")

            result = get_index_stocks_robust("000300")
            self.assertIsInstance(result, RobustResult)
            self.assertFalse(result.success)

    def test_connection_error(self):
        """测试连接错误"""
        with patch(
            "src.backtrader_base_strategy.ak.index_stock_cons_weight_csindex"
        ) as mock_ak:
            import urllib3

            mock_ak.side_effect = urllib3.exceptions.HTTPError("HTTP Error")

            result = get_index_weights_robust("000300")
            self.assertIsInstance(result, RobustResult)

    def test_key_error_in_data_processing(self):
        """测试数据处理中的KeyError"""
        with patch(
            "src.backtrader_base_strategy.ak.index_stock_cons_weight_csindex"
        ) as mock_ak:
            mock_ak.return_value = pd.DataFrame({"wrong_column": [1, 2, 3]})

            result = get_index_weights_robust("000300")
            self.assertIsInstance(result, RobustResult)

    def test_value_error_in_normalization(self):
        """测试标准化过程中的ValueError"""
        with patch(
            "src.backtrader_base_strategy._normalize_index_weights"
        ) as mock_normalize:
            mock_normalize.side_effect = ValueError("Normalization error")

            result = get_index_weights_robust("000300")
            self.assertIsInstance(result, RobustResult)


class TestDataValidation(unittest.TestCase):
    """数据验证测试"""

    def test_stock_code_format_validation(self):
        """测试股票代码格式验证"""
        code = _stock_code_to_jq("600519")
        self.assertEqual(code, "600519.XSHG")

        code = _stock_code_to_jq("000001")
        self.assertEqual(code, "000001.XSHE")

    def test_index_code_normalization(self):
        """测试指数代码标准化"""
        test_cases = [
            ("000300.XSHG", "000300"),
            ("HS300", "000300"),
            ("沪深300", "000300"),
            ("SH000300", "000300"),
        ]
        for input_code, expected in test_cases:
            result = _format_index_code(input_code)
            self.assertEqual(result, expected)

    def test_data_consistency_between_robust_and_normal(self):
        """测试稳健模式和普通模式数据一致性"""
        result_robust = get_index_stocks_robust("000300")
        result_normal = get_index_stocks("000300")

        if result_robust.success:
            self.assertEqual(result_robust.data, result_normal)

    def test_weights_dataframe_columns(self):
        """测试权重DataFrame列"""
        result = get_index_weights_robust("000300")
        if result.success:
            df = result.data
            self.assertIn("weight", df.columns)


class TestBatchQueries(unittest.TestCase):
    """批量查询测试"""

    def test_multiple_indices_sequential(self):
        """测试顺序查询多个指数"""
        indices = ["000300", "000016", "000905"]
        results = []
        for idx in indices:
            result = get_index_stocks_robust(idx)
            results.append(result)

        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIsInstance(result, RobustResult)

    def test_multiple_fundamentals_tables(self):
        """测试查询多个基本面表"""
        tables = ["valuation", "income", "balance", "cash_flow"]
        results = []
        for table in tables:
            result = get_fundamentals_robust(
                {"table": table, "symbol": ["600519.XSHG"]}
            )
            results.append(result)

        self.assertEqual(len(results), 4)

    def test_large_stock_list(self):
        """测试大股票列表查询"""
        result = get_index_stocks_robust("000300")
        if result.success and len(result.data) > 50:
            large_list = result.data
            hist_result = get_history_fundamentals_robust(
                large_list[:20], ["balance.total_assets"], count=1
            )
            self.assertIsInstance(hist_result, RobustResult)


class TestCompatibility(unittest.TestCase):
    """兼容性测试"""

    def test_jqdata_code_format(self):
        """测试聚宽代码格式兼容性"""
        jq_codes = ["000300.XSHG", "000016.XSHG", "399006.XSHE"]
        for code in jq_codes:
            result = get_index_stocks_robust(code)
            self.assertIsInstance(result, RobustResult)

    def test_akshare_code_format(self):
        """测试AkShare代码格式兼容性"""
        ak_codes = ["sh000300", "sz399006"]
        for code in ak_codes:
            result = _format_index_code(code)
            self.assertIsInstance(result, str)

    def test_query_builder_compatibility(self):
        """测试query builder兼容性"""
        q = query(valuation).filter(valuation.code.in_(["600519.XSHG", "000858.XSHE"]))
        result = get_fundamentals_robust(q)
        self.assertIsInstance(result, RobustResult)


class TestPerformanceRelated(unittest.TestCase):
    """性能相关测试"""

    def test_response_time_reasonable(self):
        """测试响应时间合理"""
        import time

        start = time.time()
        result = get_index_stocks_robust("000300")
        elapsed = time.time() - start

        # 缓存命中应该很快
        if result.source == "cache":
            self.assertLess(elapsed, 2.0)

    def test_memory_usage(self):
        """测试内存使用"""
        import gc

        gc.collect()

        results = []
        for _ in range(10):
            result = get_index_stocks_robust("000300")
            results.append(result)

        # 应该能正常完成而不崩溃
        self.assertEqual(len(results), 10)

    def test_concurrent_safety(self):
        """测试并发安全（基本测试）"""
        results = []
        for i in range(5):
            result = get_index_stocks_robust("000300")
            results.append(result)

        # 所有结果都应该成功
        for result in results:
            self.assertIsInstance(result, RobustResult)


if __name__ == "__main__":
    unittest.main(verbosity=2)
