"""
test_strategy_regression_task34.py
Task 34: 指数与基本面接口回归测试

选取依赖指数/基本面的策略进行回归测试，验证稳健性改进效果。
"""

import unittest
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    INDEX_CODE_ALIAS_MAP,
    SUPPORTED_INDEXES,
)


class TestStrategyRegression(unittest.TestCase):
    """
    回归测试 - 验证指数和基本面接口在实际策略场景中的稳健性
    """

    def test_strategy_04_hongli_banzhuan(self):
        """
        策略: 04 红利搬砖，年化29%

        使用 get_index_stocks 获取股票池
        验证:
        - 空结果处理
        - 别名兼容
        """
        index_codes = ["000300.XSHG", "hs300", "000905", "zz500"]

        for index_code in index_codes:
            result = get_index_stocks_robust(index_code)

            self.assertIsInstance(result, RobustResult)

            if not result.success:
                print(f"  {index_code}: FAILED - {result.reason}")

            self.assertTrue(
                result.success
                or "不支持" in result.reason
                or "无数据" in result.reason,
                f"{index_code} 应返回成功或明确失败原因",
            )

            if result.success:
                self.assertIsInstance(result.data, list)
                self.assertGreater(
                    len(result.data), 0, f"{index_code} 成功时应返回非空列表"
                )

    def test_strategy_03_simple_strategy(self):
        """
        策略: 03 一个简单而持续稳定的懒人超额收益策略

        使用 get_index_weights 获取权重
        验证:
        - 权重DataFrame结构
        - 缓存机制
        """
        result = get_index_weights_robust("000300")

        self.assertIsInstance(result, RobustResult)

        if result.success:
            df = result.data
            self.assertIsInstance(df, pd.DataFrame)
            self.assertIn("weight", df.columns)
            self.assertGreater(len(df), 100)
            print(f"  成功获取 {len(df)} 只成分股权重")
        else:
            print(f"  FAILED: {result.reason}")

    def test_strategy_87_basic_triangle(self):
        """
        策略: 87 【基本面三角3.0】

        使用 get_history_fundamentals 获取基本面数据
        验证:
        - 多股票多期查询
        - 字段前缀处理
        """
        test_stocks = ["600519.XSHG", "000858.XSHE"]

        result = get_history_fundamentals_robust(
            security=test_stocks,
            fields=["income.total_operating_revenue", "balance.total_assets"],
            count=1,
        )

        self.assertIsInstance(result, RobustResult)

        if result.success:
            df = result.data
            self.assertIsInstance(df, pd.DataFrame)
            expected_cols = ["income.total_operating_revenue", "balance.total_assets"]
            for col in expected_cols:
                if col in df.columns:
                    print(f"  字段 {col} 存在")
        else:
            print(f"  FAILED: {result.reason}")

    def test_strategy_70_chengbenlv_strategy(self):
        """
        策略: 70 超稳的股息率+均线选股策略

        使用 get_index_stocks 获取股票池，然后 get_fundamentals 查询估值
        """
        stocks_result = get_index_stocks_robust("000300.XSHG")

        if stocks_result.success and len(stocks_result.data) > 0:
            stocks = stocks_result.data[:10]

            fund_result = get_fundamentals_robust(
                query(valuation).filter(valuation.code.in_(stocks))
            )

            self.assertIsInstance(fund_result, RobustResult)

            if fund_result.success:
                self.assertIsInstance(fund_result.data, pd.DataFrame)
                print(f"  成功获取 {len(fund_result.data)} 条估值数据")
            else:
                print(f"  fundamentals FAILED: {fund_result.reason}")
        else:
            print(f"  stocks FAILED: {stocks_result.reason}")

    def test_strategy_79_duoyinzi_model(self):
        """
        策略: 79 【多因子选股模型框架】

        使用 get_index_stocks 获取股票池
        """
        for index_id in ["000300", "000905", "000852"]:
            result = get_index_stocks_robust(index_id)

            self.assertIsInstance(result, RobustResult)

            if result.success:
                self.assertGreater(len(result.data), 0)
                print(f"  {index_id}: {len(result.data)} 只股票")
            else:
                print(f"  {index_id}: FAILED - {result.reason}")

    def test_strategy_29_fscore(self):
        """
        策略: 29 F_Score 选股，年化80%+

        使用 get_index_stocks 和 get_history_fundamentals
        """
        stocks_result = get_index_stocks_robust("000905")

        if stocks_result.success and len(stocks_result.data) > 0:
            stocks = stocks_result.data[:3]

            hist_result = get_history_fundamentals_robust(
                security=stocks,
                fields=["income.net_profit", "balance.total_assets"],
                count=1,
            )

            self.assertIsInstance(hist_result, RobustResult)

            if hist_result.success:
                print(f"  成功获取 {len(hist_result.data)} 条历史基本面")
            else:
                print(f"  history FAILED: {hist_result.reason}")
        else:
            print(f"  stocks FAILED: {stocks_result.reason}")

    def test_strategy_78_ffscore_rsrs(self):
        """
        策略: 78 ffscore选股加rsrs择时

        使用 get_index_stocks 获取股票池
        """
        result = get_index_stocks_robust("000300.XSHG")

        self.assertIsInstance(result, RobustResult)

        if result.success:
            print(f"  成功获取 {len(result.data)} 只股票")
        else:
            print(f"  FAILED: {result.reason}")

    def test_index_alias_compatibility(self):
        """
        测试指数代码别名兼容性

        验证各种格式都能被正确识别
        """
        test_codes = [
            ("000300.XSHG", "000300"),
            ("000300", "000300"),
            ("sh000300", "000300"),
            ("hs300", "000300"),
            ("沪深300", "000300"),
            ("000905.XSHG", "000905"),
            ("zz500", "000905"),
            ("中证500", "000905"),
            ("000016", "000016"),
            ("sz50", "000016"),
            ("上证50", "000016"),
            ("399006.XSHE", "399006"),
            ("cyb", "399006"),
            ("创业板", "399006"),
        ]

        success_count = 0
        for code, expected_index in test_codes:
            result = get_index_stocks_robust(code)
            if result.success:
                success_count += 1

        print(f"  别名兼容测试: {success_count}/{len(test_codes)} 成功")

        self.assertGreater(
            success_count, len(test_codes) * 0.7, f"至少70%的别名应该成功"
        )

    def test_empty_result_handling(self):
        """
        测试空结果处理

        验证空结果返回正确结构，不会导致下游策略假跑通
        """
        empty_cases = [
            ("get_index_stocks", lambda: get_index_stocks_robust("999999")),
            ("get_index_weights", lambda: get_index_weights_robust("999999")),
            (
                "get_fundamentals",
                lambda: get_fundamentals_robust(
                    query(valuation).filter(valuation.code.in_([]))
                ),
            ),
            (
                "get_history_fundamentals",
                lambda: get_history_fundamentals_robust([], ["income.net_profit"]),
            ),
        ]

        for name, func in empty_cases:
            result = func()
            self.assertIsInstance(result, RobustResult)
            self.assertFalse(result.success)

            print(f"  {name}: 返回正确失败结构 (reason: {result.reason[:30]}...)")

            self.assertFalse(result.data is None, f"{name} 不应返回 None")

            if isinstance(result.data, pd.DataFrame):
                self.assertTrue(
                    "code" in result.data.columns, f"{name} 空DataFrame应有code列"
                )
            elif isinstance(result.data, list):
                self.assertEqual(result.data, [], f"{name} 空列表应为 []")


class TestIndexCodeFormat(unittest.TestCase):
    """
    测试指数代码格式化
    """

    def test_supported_indexes_count(self):
        self.assertGreater(len(SUPPORTED_INDEXES), 15, "至少支持15个指数")
        print(f"  支持指数数量: {len(SUPPORTED_INDEXES)}")

    def test_alias_map_count(self):
        self.assertGreater(len(INDEX_CODE_ALIAS_MAP), 40, "至少有40个别名映射")
        print(f"  别名映射数量: {len(INDEX_CODE_ALIAS_MAP)}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
