#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 19: 策略回放正确性验证测试

测试目标：
1. 验证前置条件满足情况
2. 验证结果文档存在性
3. 验证真跑通策略样本池状态
4. 验证任务定位正确性

覆盖问题：
- P3: Task 19缺结果文档
- 当前没有task19_strategy_replay_validation_result.md
- "抽样验证策略是真的跑对了"这一步还不能算完成
"""

import os
import sys
import unittest

try:
    from jk2bt.strategy.scanner import StrategyScanner
except ImportError:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    try:
        from jk2bt.strategy.scanner import StrategyScanner
    except ImportError:
        StrategyScanner = None


class TestTask19ResultDocumentExists(unittest.TestCase):
    """测试Task 19结果文档存在性"""

    def test_result_document_exists(self):
        """Task 19结果文档应存在"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task19_strategy_replay_validation_result.md",
        )

        self.assertTrue(
            os.path.exists(result_doc_path),
            "Task 19结果文档应存在: task19_strategy_replay_validation_result.md",
        )

        if os.path.exists(result_doc_path):
            print(f"验证通过: 结果文档存在 {result_doc_path}")

    def test_result_document_has_content(self):
        """结果文档应有内容"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task19_strategy_replay_validation_result.md",
        )

        if not os.path.exists(result_doc_path):
            self.skipTest("结果文档不存在")

        with open(result_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertGreater(len(content), 100, "结果文档应有内容")

        required_sections = ["修改文件", "完成内容", "已知边界"]
        found_sections = [s for s in required_sections if s in content]

        self.assertGreater(len(found_sections), 0, "结果文档应包含至少一个必要章节")

        print(f"验证通过: 结果文档包含章节 {found_sections}")


class TestPreconditionsSatisfied(unittest.TestCase):
    """测试前置条件满足情况"""

    def test_task13_result_exists(self):
        """Task 13结果应存在"""
        task13_result = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task13_daily_equity_baseline_result.md",
        )

        self.assertTrue(
            os.path.exists(task13_result), "Task 13结果应存在（Task 19前置条件）"
        )

        print("验证通过: Task 13结果存在")

    def test_task18_result_exists(self):
        """Task 18结果应存在"""
        task18_result = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task18_batch_runner_truth_result.md",
        )

        self.assertTrue(
            os.path.exists(task18_result), "Task 18结果应存在（Task 19前置条件）"
        )

        print("验证通过: Task 18结果存在")

    def test_task13_has_zero_success(self):
        """Task 13应记录首批测试成功0个"""
        task13_result = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task13_daily_equity_baseline_result.md",
        )

        if not os.path.exists(task13_result):
            self.skipTest("Task 13结果不存在")

        with open(task13_result, "r", encoding="utf-8") as f:
            content = f.read()

        has_zero_success = "成功: 0个" in content or "成功总数: 0" in content

        self.assertTrue(has_zero_success, "Task 13应记录首批测试成功0个")

        print("验证通过: Task 13记录首批测试成功0个")

    def test_task18_has_indentation_error(self):
        """Task 18应记录IndentationError"""
        task18_result = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task18_batch_runner_truth_result.md",
        )

        if not os.path.exists(task18_result):
            self.skipTest("Task 18结果不存在")

        with open(task18_result, "r", encoding="utf-8") as f:
            content = f.read()

        has_indentation_error = "IndentationError" in content

        self.assertTrue(has_indentation_error, "Task 18应记录IndentationError")

        print("验证通过: Task 18记录IndentationError")


class TestVerifiedStrategyPoolStatus(unittest.TestCase):
    """测试真跑通策略样本池状态"""

    def test_pool_is_empty(self):
        """样本池应为空（因前置条件不满足）"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task19_strategy_replay_validation_result.md",
        )

        if not os.path.exists(result_doc_path):
            self.skipTest("结果文档不存在")

        with open(result_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        empty_pool_indicators = [
            "空池",
            "无真实成功运行的策略样本",
            "样本池为空",
            "无法完成",
            "前置阻塞",
        ]

        has_empty_indicator = any(p in content for p in empty_pool_indicators)

        self.assertTrue(has_empty_indicator, "文档应说明样本池为空或无法完成")

        if has_empty_indicator:
            found_indicator = [p for p in empty_pool_indicators if p in content][0]
            print(f"验证通过: 样本池状态 '{found_indicator}'")

    def test_cannot_claim_verification_complete(self):
        """不能声称验证完成"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task19_strategy_replay_validation_result.md",
        )

        if not os.path.exists(result_doc_path):
            self.skipTest("结果文档不存在")

        with open(result_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        cannot_claim_patterns = ["不能说", "不能给出", "无法执行", "未完成", "前置阻塞"]

        has_cannot_claim = any(p in content for p in cannot_claim_patterns)

        self.assertTrue(has_cannot_claim, "文档应说明不能声称验证完成")

        if has_cannot_claim:
            found_pattern = [p for p in cannot_claim_patterns if p in content][0]
            print(f"验证通过: '{found_pattern}'")


class TestTask19Positioning(unittest.TestCase):
    """测试Task 19任务定位"""

    def test_task_positioning_is_quality_assurance(self):
        """任务定位应为质量保证"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task19_strategy_replay_validation_result.md",
        )

        if not os.path.exists(result_doc_path):
            self.skipTest("结果文档不存在")

        with open(result_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        quality_assurance_keywords = ["质量保证", "验证任务", "抽检", "正确性验证"]

        has_qa_keyword = any(kw in content for kw in quality_assurance_keywords)

        self.assertTrue(has_qa_keyword, "文档应明确任务定位为质量保证")

        if has_qa_keyword:
            found_keyword = [kw for kw in quality_assurance_keywords if kw in content][
                0
            ]
            print(f"验证通过: 任务定位为'{found_keyword}'")

    def test_prerequisites_documented(self):
        """前置条件应记录"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task19_strategy_replay_validation_result.md",
        )

        if not os.path.exists(result_doc_path):
            self.skipTest("结果文档不存在")

        with open(result_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        prerequisite_patterns = [
            "前置条件",
            "前置阻塞",
            "依赖",
            "IndentationError",
            "导入错误",
        ]

        has_prerequisite = any(p in content for p in prerequisite_patterns)

        self.assertTrue(has_prerequisite, "文档应记录前置条件或阻塞原因")

        if has_prerequisite:
            found_pattern = [p for p in prerequisite_patterns if p in content][0]
            print(f"验证通过: 前置条件 '{found_pattern}'")


class TestStrategyReplayCorrectnessChecks(unittest.TestCase):
    """测试策略回放正确性检查项"""

    def test_timer_trigger_check_defined(self):
        """定时器触发检查应定义"""
        prompt_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "subagent_tasks_phase2",
            "task19_strategy_replay_validation_prompt.md",
        )

        if not os.path.exists(prompt_doc_path):
            self.skipTest("prompt文档不存在")

        with open(prompt_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("定时器", content, "prompt应定义定时器触发检查")

        print("验证通过: 定时器触发检查已定义")

    def test_transaction_check_defined(self):
        """交易检查应定义"""
        prompt_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "subagent_tasks_phase2",
            "task19_strategy_replay_validation_prompt.md",
        )

        if not os.path.exists(prompt_doc_path):
            self.skipTest("prompt文档不存在")

        with open(prompt_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("交易", content, "prompt应定义交易检查")

        print("验证通过: 交易检查已定义")

    def test_nav_curve_check_defined(self):
        """净值曲线检查应定义"""
        prompt_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "subagent_tasks_phase2",
            "task19_strategy_replay_validation_prompt.md",
        )

        if not os.path.exists(prompt_doc_path):
            self.skipTest("prompt文档不存在")

        with open(prompt_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("净值曲线", content, "prompt应定义净值曲线检查")

        print("验证通过: 净值曲线检查已定义")

    def test_record_output_check_defined(self):
        """record输出检查应定义"""
        prompt_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "subagent_tasks_phase2",
            "task19_strategy_replay_validation_prompt.md",
        )

        if not os.path.exists(prompt_doc_path):
            self.skipTest("prompt文档不存在")

        with open(prompt_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("record", content, "prompt应定义record输出检查")

        print("验证通过: record输出检查已定义")


class TestSampleStrategyFiles(unittest.TestCase):
    """测试样本策略文件"""

    def test_sample_strategies_directory_exists(self):
        """样本策略目录应存在"""
        sample_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "tests", "sample_strategies"
        )

        self.assertTrue(
            os.path.exists(sample_dir), "样本策略目录应存在: tests/sample_strategies"
        )

        if os.path.exists(sample_dir):
            files = os.listdir(sample_dir)
            print(f"验证通过: 样本策略目录存在，包含 {len(files)} 个文件")

    def test_valid_strategy_sample_exists(self):
        """有效策略样本应存在"""
        sample_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "tests", "sample_strategies"
        )

        if not os.path.exists(sample_dir):
            self.skipTest("样本策略目录不存在")

        valid_strategy = os.path.join(sample_dir, "01_valid_strategy.txt")

        self.assertTrue(
            os.path.exists(valid_strategy), "有效策略样本应存在: 01_valid_strategy.txt"
        )

        if os.path.exists(valid_strategy):
            print("验证通过: 有效策略样本存在")


if __name__ == "__main__":
    unittest.main(verbosity=2)
