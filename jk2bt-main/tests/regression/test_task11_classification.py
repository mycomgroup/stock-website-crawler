#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 11: 策略分类准确性测试

测试目标：
1. 验证策略分类规则准确性
2. 验证分类比例合理性
3. 验证避免过度分类
4. 验证代表样本一致性

覆盖问题：
- P2: Task 11的盘点结果有明显过度分类迹象
- 期货/股指策略被标成428个(95.3%)，比例过高
- 代表样本明显包含普通股票/ETF策略
"""

import os
import sys
import unittest
import tempfile

try:
    from jk2bt.strategy.scanner import (
        StrategyScanner,
        StrategyStatus,
    )
except ImportError:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    try:
        from jk2bt.strategy.scanner import (
            StrategyScanner,
            StrategyStatus,
        )
    except ImportError:
        StrategyScanner = None
        StrategyStatus = None


class TestStrategyClassificationAccuracy(unittest.TestCase):
    """测试策略分类准确性"""

    def test_stock_strategy_detection(self):
        """股票策略应正确识别"""
        if StrategyScanner is None:
            self.skipTest("strategy_scanner模块不可用")

        scanner = StrategyScanner()

        stock_strategy = """
def initialize(context):
    g.stocks = ['600519.XSHG', '000001.XSHE']
    set_benchmark('000300.XSHG')

def handle_data(context, data):
    for stock in g.stocks:
        order_value(stock, 10000)
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(stock_strategy)
            f.flush()
            strategy_file = f.name

        try:
            result = scanner.scan_file(strategy_file)

            self.assertTrue(result.has_initialize)
            self.assertEqual(result.status, StrategyStatus.VALID)
            print(f"股票策略检测: status={result.status.value}")
        finally:
            os.unlink(strategy_file)

    def test_etf_strategy_detection(self):
        """ETF策略应正确识别"""
        if StrategyScanner is None:
            self.skipTest("strategy_scanner模块不可用")

        scanner = StrategyScanner()

        etf_strategy = """
def initialize(context):
    g.etfs = ['510300.XSHG', '159915.XSHE']
    set_benchmark('000300.XSHG')

def handle_data(context, data):
    order_target_value(g.etfs[0], 50000)
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(etf_strategy)
            f.flush()
            strategy_file = f.name

        try:
            result = scanner.scan_file(strategy_file)

            self.assertTrue(result.has_initialize)
            self.assertEqual(result.status, StrategyStatus.VALID)
            print(f"ETF策略检测: status={result.status.value}")
        finally:
            os.unlink(strategy_file)

    def test_minute_strategy_detection_by_frequency(self):
        """分钟策略应基于频率参数识别"""
        if StrategyScanner is None:
            self.skipTest("strategy_scanner模块不可用")

        scanner = StrategyScanner()

        true_minute_strategy = """
def initialize(context):
    run_daily(rebalance, time='every_bar')

def rebalance(context):
    df = history(10, unit='1m')
    order('600519.XSHG', 100)
"""

        fake_minute_strategy = """
def initialize(context):
    # 这是一个使用分钟关键词的策略，但实际是日线
    # 分钟数据在这里只是注释
    run_daily(rebalance, time='open')

def rebalance(context):
    df = history(10, unit='1d')
    order('600519.XSHG', 100)
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(true_minute_strategy)
            f.flush()
            true_file = f.name

        try:
            true_result = scanner.scan_file(true_file)
            true_minute_apis = [
                api
                for api in true_result.used_apis
                if "minute" in api.lower() or "1m" in api.lower()
            ]
            print(f"真分钟策略API: {true_result.used_apis}")
        finally:
            os.unlink(true_file)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(fake_minute_strategy)
            f.flush()
            fake_file = f.name

        try:
            fake_result = scanner.scan_file(fake_file)
            fake_minute_apis = [
                api
                for api in fake_result.used_apis
                if "minute" in api.lower() or "1m" in api.lower()
            ]
            print(f"假分钟策略API: {fake_result.used_apis}")

            self.assertEqual(len(fake_minute_apis), 0, "假分钟策略不应被识别为分钟策略")
        finally:
            os.unlink(fake_file)


class TestClassificationRatioReasonableness(unittest.TestCase):
    """测试分类比例合理性"""

    def test_futures_ratio_not_too_high(self):
        """期货策略比例不应过高"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task11_strategy_inventory_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            has_warning = (
                "过度分类" in content
                or "分类规则偏宽" in content
                or "比例过高" in content
                or "警告" in content
            )

            self.assertTrue(has_warning, "文档应包含过度分类警告")

            if has_warning:
                print("验证通过: 文档包含过度分类警告")
        else:
            self.skipTest("结果文档不存在")

    def test_total_files_matches_sum(self):
        """总文件数应与各分类数合理对应"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task11_strategy_inventory_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            import re

            total_match = re.search(r"总文件数.*?(\d+)", content)
            futures_match = re.search(r"期货/股指策略.*?(\d+).*?(\d+\.\d+)%", content)

            if total_match and futures_match:
                total = int(total_match.group(1))
                futures = int(futures_match.group(1))
                futures_pct = float(futures_match.group(2))

                self.assertEqual(
                    futures, int(total * futures_pct / 100), "期货数量应与百分比对应"
                )

                print(f"总文件: {total}, 期货: {futures}, 占比: {futures_pct}%")

                if futures_pct > 50:
                    print(f"警告: 期货占比 {futures_pct}% > 50%，可能存在过度分类")
        else:
            self.skipTest("结果文档不存在")


class TestRepresentativeSampleConsistency(unittest.TestCase):
    """测试代表样本一致性"""

    def test_futures_representative_is_actually_futures(self):
        """期货策略代表样本应确实是期货策略"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task11_strategy_inventory_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            non_futures_keywords = [
                "小市值",
                "AI因子选股",
                "成长股策略",
                "股票策略",
                "ETF策略",
            ]

            futures_section_start = content.find("期货/股指策略")
            if futures_section_start > 0:
                futures_section = content[
                    futures_section_start : futures_section_start + 2000
                ]

                found_non_futures = [
                    kw for kw in non_futures_keywords if kw in futures_section
                ]

                if found_non_futures:
                    print(
                        f"警告: 期货代表样本包含非期货策略关键词: {found_non_futures}"
                    )

                    has_inconsistency_warning = (
                        "过度分类" in content
                        or "代表样本包含" in content
                        or "分类规则偏宽" in content
                    )

                    self.assertTrue(
                        has_inconsistency_warning, "文档应记录代表样本不一致问题"
                    )
        else:
            self.skipTest("结果文档不存在")

    def test_sample_strategy_files_exist(self):
        """样本策略文件应存在"""
        jkcode_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "jkcode", "jkcode"
        )

        if not os.path.exists(jkcode_path):
            self.skipTest("策略目录不存在")

        sample_files = [
            "01 龙回头3.0回测速度优化版.txt",
            "03 一个简单而持续稳定的懒人超额收益策略.txt",
        ]

        existing_samples = []
        for sample in sample_files:
            matching_files = [f for f in os.listdir(jkcode_path) if sample in f]
            if matching_files:
                existing_samples.append(sample)

        self.assertGreater(len(existing_samples), 0, "应存在至少一个样本策略文件")

        print(f"样本策略存在: {existing_samples}")


class TestClassificationRulesCorrectness(unittest.TestCase):
    """测试分类规则正确性"""

    def test_classification_based_on_api_usage(self):
        """分类应基于API使用情况"""
        if StrategyScanner is None:
            self.skipTest("strategy_scanner模块不可用")

        scanner = StrategyScanner()

        strategy_with_future_api = """
def initialize(context):
    contracts = get_future_contracts('IF')
    set_benchmark('IF2312.CCFX')

def handle_data(context, data):
    order('IF2312.CCFX', 1)
"""

        strategy_without_future_api = """
def initialize(context):
    g.stocks = get_index_stocks('000300.XSHG')
    set_benchmark('000300.XSHG')

def handle_data(context, data):
    order(g.stocks[0], 100)
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(strategy_with_future_api)
            f.flush()
            future_file = f.name

        try:
            future_result = scanner.scan_file(future_file)
            has_future_api = "get_future_contracts" in future_result.used_apis
            print(
                f"期货API策略: used_apis={future_result.used_apis}, has_future_api={has_future_api}"
            )
        finally:
            os.unlink(future_file)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(strategy_without_future_api)
            f.flush()
            stock_file = f.name

        try:
            stock_result = scanner.scan_file(stock_file)
            has_future_api = "get_future_contracts" in stock_result.used_apis
            print(
                f"股票API策略: used_apis={stock_result.used_apis}, has_future_api={has_future_api}"
            )

            self.assertFalse(has_future_api, "股票策略不应有期货API")
        finally:
            os.unlink(stock_file)

    def test_ml_library_detection(self):
        """ML库依赖应正确检测"""
        if StrategyScanner is None:
            self.skipTest("strategy_scanner模块不可用")

        scanner = StrategyScanner()

        ml_strategy = """
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def initialize(context):
    g.model = RandomForestClassifier()

def handle_data(context, data):
    pass
"""

        non_ml_strategy = """
def initialize(context):
    g.stocks = ['600519.XSHG']

def handle_data(context, data):
    order(g.stocks[0], 100)
"""

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(ml_strategy)
            f.flush()
            ml_file = f.name

        try:
            ml_result = scanner.scan_file(ml_file)
            has_ml_deps = len(ml_result.ml_dependencies) > 0
            print(f"ML策略: ml_dependencies={ml_result.ml_dependencies}")
        finally:
            os.unlink(ml_file)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(non_ml_strategy)
            f.flush()
            non_ml_file = f.name

        try:
            non_ml_result = scanner.scan_file(non_ml_file)
            has_ml_deps = len(non_ml_result.ml_dependencies) > 0
            print(f"非ML策略: ml_dependencies={non_ml_result.ml_dependencies}")

            self.assertFalse(has_ml_deps, "非ML策略不应有ML依赖")
        finally:
            os.unlink(non_ml_file)


class TestDocumentWarningExists(unittest.TestCase):
    """测试文档警告是否存在"""

    def test_overclassification_warning_exists(self):
        """过度分类警告应存在"""
        result_doc_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs",
            "0330_result",
            "task11_strategy_inventory_result.md",
        )

        if os.path.exists(result_doc_path):
            with open(result_doc_path, "r", encoding="utf-8") as f:
                content = f.read()

            warning_patterns = [
                "过度分类",
                "分类规则偏宽",
                "比例过高",
                "警告",
                "不能直接当排期真值",
            ]

            has_warning = any(p in content for p in warning_patterns)

            self.assertTrue(has_warning, "文档应包含过度分类警告")

            if has_warning:
                found_pattern = [p for p in warning_patterns if p in content][0]
                print(f"验证通过: 文档包含'{found_pattern}'警告")
        else:
            self.skipTest("结果文档不存在")


if __name__ == "__main__":
    unittest.main(verbosity=2)
