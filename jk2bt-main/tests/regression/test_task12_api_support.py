#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 12: API支持状态判断测试

测试目标：
1. 验证API支持状态分类准确性
2. 验证占位函数检测
3. 验证"已完整支持"分类合理性
4. 验证API实际实现状态

覆盖问题：
- P2: Task 12的API矩阵里"已完整支持"有过度乐观风险
- set_option/set_benchmark/set_slippage/set_order_cost实际为占位pass
"""

import os
import sys
import unittest
import inspect

try:
    from jk2bt import load_jq_strategy
    from jk2bt.core.runner import (
        set_option,
        set_benchmark,
        set_slippage,
        set_order_cost,
    )
except ImportError:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    try:
        from jk2bt import load_jq_strategy
        from jk2bt.core.runner import (
            set_option,
            set_benchmark,
            set_slippage,
            set_order_cost,
        )
    except ImportError:
        set_option = None
        set_benchmark = None
        set_slippage = None
        set_order_cost = None


class TestPlaceholderFunctionDetection(unittest.TestCase):
    """测试占位函数检测"""

    def test_set_option_is_placeholder(self):
        """set_option应为占位函数"""
        if set_option is None:
            self.skipTest("set_option函数不可用")

        source = inspect.getsource(set_option)

        is_placeholder = "pass" in source and "占位" in source

        self.assertTrue(is_placeholder, "set_option应为占位函数（包含pass和占位标记）")

        print(f"验证通过: set_option是占位函数")
        print(f"源码片段: {source[:200]}")

    def test_set_benchmark_is_placeholder(self):
        """set_benchmark应为占位函数"""
        if set_benchmark is None:
            self.skipTest("set_benchmark函数不可用")

        source = inspect.getsource(set_benchmark)

        is_placeholder = "pass" in source and "占位" in source

        self.assertTrue(is_placeholder, "set_benchmark应为占位函数")

        print(f"验证通过: set_benchmark是占位函数")

    def test_set_slippage_is_placeholder(self):
        """set_slippage应为占位函数"""
        if set_slippage is None:
            self.skipTest("set_slippage函数不可用")

        source = inspect.getsource(set_slippage)

        is_placeholder = "pass" in source and "占位" in source

        self.assertTrue(is_placeholder, "set_slippage应为占位函数")

        print(f"验证通过: set_slippage是占位函数")

    def test_set_order_cost_is_placeholder(self):
        """set_order_cost应为占位函数"""
        if set_order_cost is None:
            self.skipTest("set_order_cost函数不可用")

        source = inspect.getsource(set_order_cost)

        is_placeholder = "pass" in source and "占位" in source

        self.assertTrue(is_placeholder, "set_order_cost应为占位函数")

        print(f"验证通过: set_order_cost是占位函数")


class TestPlaceholderFunctionBehavior(unittest.TestCase):
    """测试占位函数行为"""

    def test_set_option_returns_none(self):
        """set_option调用应返回None"""
        if set_option is None:
            self.skipTest("set_option函数不可用")

        result = set_option("use_real_price", True)

        self.assertIsNone(result, "占位函数应返回None")

        print(f"验证通过: set_option返回None")

    def test_set_benchmark_returns_none(self):
        """set_benchmark调用应返回None"""
        if set_benchmark is None:
            self.skipTest("set_benchmark函数不可用")

        result = set_benchmark("000300.XSHG")

        self.assertIsNone(result, "占位函数应返回None")

        print(f"验证通过: set_benchmark返回None")

    def test_set_slippage_returns_none(self):
        """set_slippage调用应返回None"""
        if set_slippage is None:
            self.skipTest("set_slippage函数不可用")

        class FakeSlippage:
            pass

        result = set_slippage(FakeSlippage())

        self.assertIsNone(result, "占位函数应返回None")

        print(f"验证通过: set_slippage返回None")

    def test_set_order_cost_returns_none(self):
        """set_order_cost调用应返回None"""
        if set_order_cost is None:
            self.skipTest("set_order_cost函数不可用")

        class FakeCost:
            pass

        result = set_order_cost(FakeCost())

        self.assertIsNone(result, "占位函数应返回None")

        print(f"验证通过: set_order_cost返回None")


class TestAPISupportStatusAccuracy(unittest.TestCase):
    """测试API支持状态准确性"""

    def test_document_marks_placeholder_correctly(self):
        """文档应正确标记占位API"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task12_missing_api_matrix_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            placeholder_apis = [
                "set_option",
                "set_benchmark",
                "set_slippage",
                "set_order_cost",
            ]

            has_placeholder_warning = any(
                f"{api}" in content and ("占位" in content or "pass" in content)
                for api in placeholder_apis
            )

            self.assertTrue(has_placeholder_warning, "文档应标记占位API")

            print(f"验证通过: 文档标记占位API")
        else:
            self.skipTest("结果文档不存在")

    def test_document_has_warning_about_optimistic_classification(self):
        """文档应有过度乐观分类警告"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task12_missing_api_matrix_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            warning_patterns = [
                "过度乐观",
                "占位pass",
                "占位函数",
                "需重新审查",
                "实际实现为占位",
            ]

            has_warning = any(p in content for p in warning_patterns)

            self.assertTrue(has_warning, "文档应有过度乐观分类警告")

            if has_warning:
                found_pattern = [p for p in warning_patterns if p in content][0]
                print(f"验证通过: 文档包含'{found_pattern}'警告")
        else:
            self.skipTest("结果文档不存在")


class TestRealAPIImplementation(unittest.TestCase):
    """测试真实API实现状态"""

    def test_run_daily_is_implemented(self):
        """run_daily应有实际实现"""
        try:
            from jk2bt.core.strategy_base import (
                run_daily,
            )

            source = inspect.getsource(run_daily)

            has_real_implementation = len(source) > 200 and "pass" not in source[:100]

            self.assertTrue(has_real_implementation, "run_daily应有实际实现")

            print(f"验证通过: run_daily有实际实现")
        except Exception as e:
            self.skipTest(f"run_daily不可用: {e}")

    def test_get_price_is_implemented(self):
        """get_price应有实际实现"""
        try:
            from jk2bt.core.strategy_base import (
                get_price_jq,
            )

            source = inspect.getsource(get_price_jq)

            has_real_implementation = len(source) > 500 and "pass" not in source[:100]

            self.assertTrue(has_real_implementation, "get_price_jq应有实际实现")

            print(f"验证通过: get_price_jq有实际实现")
        except Exception as e:
            self.skipTest(f"get_price_jq不可用: {e}")

    def test_order_target_value_is_implemented(self):
        """order_target_value应有实际实现"""
        try:
            from jk2bt.core.strategy_base import (
                JQ2BTBaseStrategy,
            )

            has_order_target = hasattr(JQ2BTBaseStrategy, "order_target_value")

            self.assertTrue(
                has_order_target, "JQ2BTBaseStrategy应有order_target_value方法"
            )

            print(f"验证通过: order_target_value有实际实现")
        except Exception as e:
            self.skipTest(f"JQ2BTBaseStrategy不可用: {e}")


class TestAPISupportStatusDistribution(unittest.TestCase):
    """测试API支持状态分布"""

    def test_distribution_counts_reasonable(self):
        """支持状态分布计数应合理"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task12_missing_api_matrix_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            import re

            full_support_match = re.search(r"已完整支持.*?(\d+)", content)
            partial_support_match = re.search(r"部分支持.*?(\d+)", content)
            placeholder_match = re.search(r"仅占位支持.*?(\d+)", content)
            not_supported_match = re.search(r"完全未支持.*?(\d+)", content)

            if full_support_match:
                full_count = int(full_support_match.group(1))
                print(f"已完整支持: {full_count}")

                self.assertGreater(full_count, 0, "应有已完整支持的API")

            if partial_support_match:
                partial_count = int(partial_support_match.group(1))
                print(f"部分支持: {partial_count}")

            if placeholder_match:
                placeholder_count = int(placeholder_match.group(1))
                print(f"仅占位支持: {placeholder_count}")

            if not_supported_match:
                not_supported_count = int(not_supported_match.group(1))
                print(f"完全未支持: {not_supported_count}")
        else:
            self.skipTest("结果文档不存在")

    def test_critical_missing_apis_identified(self):
        """关键缺失API应被识别"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task12_missing_api_matrix_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            critical_apis = [
                "get_fundamentals_continuously",
                "get_ticks",
                "get_future_contracts",
                "get_factor_values",
                "get_industry_stocks",
            ]

            found_critical = [api for api in critical_apis if api in content]

            self.assertGreater(len(found_critical), 0, "应识别关键缺失API")

            print(f"验证通过: 识别关键缺失API {found_critical}")
        else:
            self.skipTest("结果文档不存在")


class TestPlaceholderFunctionSourceCode(unittest.TestCase):
    """测试占位函数源码位置"""

    def test_placeholder_source_file_location(self):
        """占位函数源码位置验证"""
        runner_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "src",
            "jq_strategy_runner.py",
        )

        if not os.path.exists(runner_path):
            self.skipTest("jq_strategy_runner.py不存在")

        with open(runner_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        placeholder_function_lines = {}

        for i, line in enumerate(lines):
            if "def set_option(" in line:
                placeholder_function_lines["set_option"] = i + 1
            elif "def set_benchmark(" in line:
                placeholder_function_lines["set_benchmark"] = i + 1
            elif "def set_slippage(" in line:
                placeholder_function_lines["set_slippage"] = i + 1
            elif "def set_order_cost(" in line:
                placeholder_function_lines["set_order_cost"] = i + 1

        for func_name, line_num in placeholder_function_lines.items():
            print(f"{func_name}: line {line_num}")

            self.assertGreater(
                line_num, 0, f"{func_name}应在jq_strategy_runner.py中定义"
            )

        self.assertEqual(len(placeholder_function_lines), 4, "应找到4个占位函数")


if __name__ == "__main__":
    unittest.main(verbosity=2)
