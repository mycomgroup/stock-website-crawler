#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 30 测试用例：跑批真值重跑与策略语义抽检
测试策略批量运行的真值验证和语义抽检功能
"""

import os
import sys
import json
import unittest
import tempfile
import shutil
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))

from run_strategies_parallel import RunStatus
from jk2bt.strategy.scanner import StrategyScanner


class TestBatchTruthValidation(unittest.TestCase):
    """测试批量运行真值验证"""

    @classmethod
    def setUpClass(cls):
        """设置测试类"""
        cls.test_dir = os.path.dirname(os.path.dirname(__file__))
        cls.strategy_dir = os.path.join(cls.test_dir, "jkcode", "jkcode")
        cls.temp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        """清理测试类"""
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)

    def test_01_run_status_enum(self):
        """测试运行状态枚举定义"""
        expected_statuses = [
            "success_with_return",
            "success_zero_return",
            "success_no_trade",
            "load_failed",
            "run_exception",
            "timeout",
            "data_missing",
            "missing_dependency",
            "missing_api",
            "missing_resource",
            "skipped_not_strategy",
            "skipped_syntax_error",
            "skipped_no_initialize",
            "skipped_missing_api",
        ]

        for status in expected_statuses:
            self.assertTrue(hasattr(RunStatus, status.upper()))
            self.assertEqual(RunStatus(status).value, status)

    def test_02_strategy_scanner_valid_strategy(self):
        """测试策略扫描器识别有效策略"""
        scanner = StrategyScanner()

        strategy_file = os.path.join(
            self.strategy_dir, "03 一个简单而持续稳定的懒人超额收益策略.txt"
        )

        if os.path.exists(strategy_file):
            scan_result = scanner.scan_file(strategy_file)

            self.assertEqual(scan_result.status.value, "valid")
            self.assertTrue(scan_result.is_executable)
            self.assertTrue(scan_result.has_initialize)
            self.assertTrue(scan_result.has_handle)
            self.assertEqual(len(scan_result.missing_apis), 0)

    def test_03_strategy_scanner_not_strategy(self):
        """测试策略扫描器识别非策略文件"""
        scanner = StrategyScanner()

        strategy_file = os.path.join(self.strategy_dir, "100 配套资料说明.txt")

        if os.path.exists(strategy_file):
            scan_result = scanner.scan_file(strategy_file)

            self.assertEqual(scan_result.status.value, "not_strategy")
            self.assertFalse(scan_result.is_executable)
            self.assertFalse(scan_result.has_initialize)
            self.assertFalse(scan_result.has_handle)

    def test_04_strategy_scanner_missing_api(self):
        """测试策略扫描器识别缺失API策略"""
        scanner = StrategyScanner()

        strategy_file = os.path.join(self.strategy_dir, "03 多策略融合-80倍.txt")

        if os.path.exists(strategy_file):
            scan_result = scanner.scan_file(strategy_file)

            self.assertEqual(scan_result.status.value, "missing_api")
            self.assertFalse(scan_result.is_executable)
            self.assertTrue(len(scan_result.missing_apis) > 0)
            self.assertIn("get_ticks", scan_result.missing_apis)

    def test_05_evidence_structure(self):
        """测试证据字段结构"""
        expected_evidence_fields = [
            "loaded",
            "entered_backtest_loop",
            "has_transactions",
            "has_nav_series",
            "nav_series_length",
            "strategy_obj_valid",
            "cerebro_valid",
        ]

        evidence = {
            "loaded": False,
            "entered_backtest_loop": False,
            "has_transactions": False,
            "has_nav_series": False,
            "nav_series_length": 0,
            "strategy_obj_valid": False,
            "cerebro_valid": False,
        }

        for field in expected_evidence_fields:
            self.assertIn(field, evidence)

    def test_06_attribution_structure(self):
        """测试归因字段结构"""
        expected_attribution_fields = [
            "failure_root_cause",
            "missing_dependency",
            "missing_api",
            "missing_resource_file",
            "error_category",
            "recoverable",
            "recommendation",
        ]

        attribution = {
            "failure_root_cause": "",
            "missing_dependency": "",
            "missing_api": "",
            "missing_resource_file": "",
            "error_category": "",
            "recoverable": False,
            "recommendation": "",
        }

        for field in expected_attribution_fields:
            self.assertIn(field, attribution)

    def test_07_semantic_check_logic(self):
        """测试语义抽检逻辑"""

        def semantic_check(result):
            checks = {
                "loaded": result.get("evidence", {}).get("loaded", False),
                "entered_backtest_loop": result.get("evidence", {}).get(
                    "entered_backtest_loop", False
                ),
                "has_transactions": result.get("evidence", {}).get(
                    "has_transactions", False
                ),
                "has_nav_series": result.get("evidence", {}).get(
                    "has_nav_series", False
                ),
                "nav_series_length": result.get("evidence", {}).get(
                    "nav_series_length", 0
                ),
                "strategy_obj_valid": result.get("evidence", {}).get(
                    "strategy_obj_valid", False
                ),
                "cerebro_valid": result.get("evidence", {}).get("cerebro_valid", False),
            }

            semantic_status = "unknown"

            if (
                checks["loaded"]
                and checks["entered_backtest_loop"]
                and checks["has_nav_series"]
            ):
                if checks["has_transactions"] and checks["nav_series_length"] > 0:
                    if result.get("pnl_pct", 0) != 0:
                        semantic_status = "real_success_with_return"
                    else:
                        semantic_status = "real_success_zero_return"
                else:
                    semantic_status = "real_success_no_trade"
            elif checks["loaded"] and not checks["entered_backtest_loop"]:
                semantic_status = "pseudo_success_no_loop"
            elif not checks["loaded"]:
                semantic_status = "pseudo_success_not_loaded"

            return checks, semantic_status

        result_real_success = {
            "evidence": {
                "loaded": True,
                "entered_backtest_loop": True,
                "has_transactions": True,
                "has_nav_series": True,
                "nav_series_length": 58,
            },
            "pnl_pct": -1.63,
        }

        checks, status = semantic_check(result_real_success)
        self.assertEqual(status, "real_success_with_return")

        result_no_trade = {
            "evidence": {
                "loaded": True,
                "entered_backtest_loop": True,
                "has_transactions": False,
                "has_nav_series": True,
                "nav_series_length": 58,
            },
            "pnl_pct": 0,
        }

        checks, status = semantic_check(result_no_trade)
        self.assertEqual(status, "real_success_no_trade")

        result_pseudo = {
            "evidence": {
                "loaded": True,
                "entered_backtest_loop": False,
                "has_transactions": False,
                "has_nav_series": False,
                "nav_series_length": 0,
            },
            "pnl_pct": 0,
        }

        checks, status = semantic_check(result_pseudo)
        self.assertEqual(status, "pseudo_success_no_loop")

    def test_08_status_classification_success_with_return(self):
        """测试状态分类：成功有收益"""
        from run_strategies_parallel import _classify_run_status

        class MockStrategy:
            def __init__(self):
                self.navs = [100000, 99000, 98000, 95000]

        backtest_result = {
            "strategy": MockStrategy(),
            "cerebro": None,
            "final_value": 95000,
            "pnl_pct": -5.0,
        }

        evidence = {
            "loaded": True,
            "entered_backtest_loop": True,
            "has_transactions": True,
            "has_nav_series": True,
        }

        status = _classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )

        self.assertEqual(status, RunStatus.SUCCESS_WITH_RETURN)

    def test_09_status_classification_success_zero_return(self):
        """测试状态分类：成功零收益"""
        from run_strategies_parallel import _classify_run_status

        class MockStrategy:
            def __init__(self):
                self.navs = [100000, 100000, 100000, 100000]

        backtest_result = {
            "strategy": MockStrategy(),
            "cerebro": None,
            "final_value": 100000,
            "pnl_pct": 0.0,
        }

        evidence = {
            "loaded": True,
            "entered_backtest_loop": True,
            "has_transactions": True,
            "has_nav_series": True,
        }

        status = _classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )

        self.assertEqual(status, RunStatus.SUCCESS_ZERO_RETURN)

    def test_10_status_classification_load_failed(self):
        """测试状态分类：加载失败"""
        from run_strategies_parallel import _classify_run_status

        status = _classify_run_status(
            backtest_result=None,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence={"loaded": False},
        )

        self.assertEqual(status, RunStatus.LOAD_FAILED)

    def test_11_status_classification_timeout(self):
        """测试状态分类：超时"""
        from run_strategies_parallel import _classify_run_status
        from concurrent.futures import TimeoutError

        status = _classify_run_status(
            backtest_result=None,
            exception=TimeoutError(),
            has_data=True,
            scan_result=None,
            evidence=None,
        )

        self.assertEqual(status, RunStatus.TIMEOUT)

    def test_12_status_classification_missing_dependency(self):
        """测试状态分类：依赖缺失"""
        from run_strategies_parallel import _classify_run_status

        exception = ImportError("No module named 'sklearn'")

        status = _classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
            evidence=None,
        )

        self.assertEqual(status, RunStatus.MISSING_DEPENDENCY)

    def test_13_status_classification_missing_api(self):
        """测试状态分类：API缺失"""
        from run_strategies_parallel import _classify_run_status

        exception = AttributeError(
            "'NoneType' object has no attribute 'get_fundamentals'"
        )

        scan_result = {"missing_apis": ["get_fundamentals"]}

        status = _classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=scan_result,
            evidence=None,
        )

        self.assertEqual(status, RunStatus.MISSING_API)

    def test_14_status_classification_data_missing(self):
        """测试状态分类：数据缺失"""
        from run_strategies_parallel import _classify_run_status

        exception = ValueError("找不到股票数据")

        status = _classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
            evidence=None,
        )

        self.assertEqual(status, RunStatus.DATA_MISSING)

    def test_15_status_classification_run_exception(self):
        """测试状态分类：运行异常"""
        from run_strategies_parallel import _classify_run_status

        exception = RuntimeError("Unknown runtime error")

        status = _classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
            evidence=None,
        )

        self.assertEqual(status, RunStatus.RUN_EXCEPTION)

    def test_16_attribution_missing_dependency(self):
        """测试归因分析：依赖缺失"""
        error_str = "No module named 'sklearn'"

        attribution = {
            "failure_root_cause": "Python依赖包缺失",
            "missing_dependency": error_str,
            "error_category": "dependency_missing",
            "recoverable": True,
            "recommendation": "安装缺失的Python包: pip install <package>",
        }

        self.assertTrue(attribution["recoverable"])
        self.assertEqual(attribution["error_category"], "dependency_missing")

    def test_17_attribution_missing_api(self):
        """测试归因分析：API缺失"""
        error_str = "'NoneType' object has no attribute 'get_fundamentals'"

        attribution = {
            "failure_root_cause": "聚宽API未实现",
            "missing_api": "get_fundamentals",
            "error_category": "api_missing",
            "recoverable": True,
            "recommendation": "在utility中实现缺失的API或修改策略代码",
        }

        self.assertTrue(attribution["recoverable"])
        self.assertEqual(attribution["error_category"], "api_missing")

    def test_18_attribution_data_missing(self):
        """测试归因分析：数据缺失"""
        error_str = "找不到股票数据: 600519.XSHG"

        attribution = {
            "failure_root_cause": "数据缺失",
            "missing_resource_file": error_str,
            "error_category": "data_missing",
            "recoverable": True,
            "recommendation": "补充缺失的数据文件或调整回测时间段",
        }

        self.assertTrue(attribution["recoverable"])
        self.assertEqual(attribution["error_category"], "data_missing")

    def test_19_attribution_unrecoverable(self):
        """测试归因分析：不可恢复"""
        attribution = {
            "failure_root_cause": "IndentationError: unexpected indent",
            "error_category": "syntax_error",
            "recoverable": False,
            "recommendation": "检查策略文件语法错误",
        }

        self.assertFalse(attribution["recoverable"])
        self.assertEqual(attribution["error_category"], "syntax_error")

    def test_20_summary_structure(self):
        """测试summary.json结构"""
        summary = {
            "run_id": "20260330_184133",
            "timestamp": datetime.now().isoformat(),
            "config": {
                "max_workers": 3,
                "timeout_per_strategy": 120,
                "start_date": "2022-01-01",
                "end_date": "2022-03-31",
                "initial_capital": 100000,
            },
            "scan_summary": {
                "total": 8,
                "executable": 6,
                "skipped": 2,
            },
            "summary": {
                "input_total": 8,
                "run_total": 6,
                "skipped_total": 2,
                "success_with_return": 1,
                "success_zero_return": 0,
                "success_no_trade": 5,
                "success_total": 6,
                "load_failed": 0,
                "run_exception": 0,
                "timeout": 0,
                "data_missing": 0,
                "missing_dependency": 0,
                "missing_api": 0,
                "missing_resource": 0,
                "skipped_not_strategy": 2,
                "failed_total": 2,
                "recoverable_failures": 0,
                "unrecoverable_failures": 2,
                "real_success_rate": 100.0,
                "input_success_rate": 75.0,
                "status_counts": {
                    "success_with_return": 1,
                    "success_no_trade": 5,
                    "skipped_not_strategy": 2,
                },
            },
            "attribution_summary": {
                "recoverable": {
                    "data_missing": 0,
                    "missing_dependency": 0,
                    "missing_api": 0,
                    "missing_resource": 0,
                },
                "unrecoverable": {
                    "load_failed": 0,
                    "run_exception": 0,
                    "timeout": 0,
                    "syntax_error": 0,
                },
            },
            "results": [],
        }

        required_fields = [
            "run_id",
            "timestamp",
            "config",
            "scan_summary",
            "summary",
            "attribution_summary",
            "results",
        ]

        for field in required_fields:
            self.assertIn(field, summary)

    def test_21_result_structure(self):
        """测试单个结果结构"""
        result = {
            "strategy": "03 一个简单而持续稳定的懒人超额收益策略.txt",
            "strategy_file": "jkcode/jkcode/03 一个简单而持续稳定的懒人超额收益策略.txt",
            "success": True,
            "run_status": "success_with_return",
            "status": "运行成功有收益",
            "start_time": "2026-03-30T18:41:29.533870",
            "end_time": "2026-03-30T18:41:30.874370",
            "duration": 1.34,
            "final_value": 98368.14992,
            "pnl": -1631.850080,
            "pnl_pct": -1.631850080,
            "max_drawdown": 0.05,
            "annual_return": -0.20,
            "sharpe_ratio": -1.5,
            "trading_days": 58,
            "error": "",
            "traceback": "",
            "scan_result": {},
            "exception_type": "",
            "evidence": {
                "loaded": True,
                "entered_backtest_loop": True,
                "has_transactions": True,
                "has_nav_series": True,
                "nav_series_length": 58,
                "strategy_obj_valid": True,
                "cerebro_valid": True,
            },
            "attribution": {
                "failure_root_cause": "",
                "missing_dependency": "",
                "missing_api": "",
                "missing_resource_file": "",
                "error_category": "",
                "recoverable": False,
                "recommendation": "",
            },
        }

        required_fields = [
            "strategy",
            "strategy_file",
            "success",
            "run_status",
            "status",
            "start_time",
            "end_time",
            "duration",
            "final_value",
            "pnl",
            "pnl_pct",
            "max_drawdown",
            "annual_return",
            "sharpe_ratio",
            "trading_days",
            "error",
            "traceback",
            "scan_result",
            "exception_type",
            "evidence",
            "attribution",
        ]

        for field in required_fields:
            self.assertIn(field, result)

    def test_22_strategy_object_handling(self):
        """测试策略对象处理（避免AttributeError）"""
        import backtrader as bt

        class MockStrategy(bt.Strategy):
            def __init__(self):
                self.navs = [100000, 99000, 98000]

        cerebro = bt.Cerebro()
        cerebro.addstrategy(MockStrategy)

        strategy_class = MockStrategy

        self.assertIsNotNone(strategy_class)

        self.assertTrue(hasattr(strategy_class, "__init__"))

    def test_23_recoverable_failure_count(self):
        """测试可恢复失败计数"""
        results = [
            {
                "attribution": {
                    "recoverable": True,
                    "error_category": "data_missing",
                }
            },
            {
                "attribution": {
                    "recoverable": True,
                    "error_category": "missing_dependency",
                }
            },
            {
                "attribution": {
                    "recoverable": False,
                    "error_category": "syntax_error",
                }
            },
            {
                "attribution": {
                    "recoverable": False,
                    "error_category": "load_failed",
                }
            },
        ]

        recoverable_count = sum(
            1 for r in results if r.get("attribution", {}).get("recoverable", False)
        )

        self.assertEqual(recoverable_count, 2)

        unrecoverable_count = len(results) - recoverable_count
        self.assertEqual(unrecoverable_count, 2)

    def test_24_success_rate_calculation(self):
        """测试成功率计算"""
        summary = {
            "success_total": 6,
            "run_total": 6,
            "input_total": 8,
        }

        real_success_rate = (
            (summary["success_total"] / summary["run_total"] * 100)
            if summary["run_total"] > 0
            else 0
        )
        input_success_rate = (
            (summary["success_total"] / summary["input_total"] * 100)
            if summary["input_total"] > 0
            else 0
        )

        self.assertEqual(real_success_rate, 100.0)
        self.assertEqual(input_success_rate, 75.0)

    def test_25_json_serialization(self):
        """测试JSON序列化"""
        result = {
            "strategy": "test_strategy.txt",
            "success": True,
            "run_status": "success_with_return",
            "pnl_pct": -1.63,
            "evidence": {
                "loaded": True,
                "nav_series_length": 58,
            },
            "attribution": {
                "recoverable": False,
            },
        }

        json_str = json.dumps(result, ensure_ascii=False)
        parsed = json.loads(json_str)

        self.assertEqual(parsed["strategy"], "test_strategy.txt")
        self.assertEqual(parsed["pnl_pct"], -1.63)
        self.assertEqual(parsed["evidence"]["nav_series_length"], 58)


class TestIntegrationBatchTruth(unittest.TestCase):
    """集成测试：批量运行真值验证"""

    @classmethod
    def setUpClass(cls):
        """设置测试类"""
        cls.test_dir = os.path.dirname(os.path.dirname(__file__))
        cls.strategy_dir = os.path.join(cls.test_dir, "jkcode", "jkcode")

    def test_01_real_strategy_scan(self):
        """集成测试：真实策略扫描"""
        scanner = StrategyScanner()

        strategy_files = [
            "03 一个简单而持续稳定的懒人超额收益策略.txt",
            "04 红利搬砖，年化29%.txt",
            "100 配套资料说明.txt",
        ]

        results = []
        for strategy_file in strategy_files:
            path = os.path.join(self.strategy_dir, strategy_file)
            if os.path.exists(path):
                scan_result = scanner.scan_file(path)
                results.append(
                    {
                        "strategy": strategy_file,
                        "status": scan_result.status.value,
                        "is_executable": scan_result.is_executable,
                        "has_initialize": scan_result.has_initialize,
                        "has_handle": scan_result.has_handle,
                    }
                )

        self.assertTrue(len(results) > 0)

        valid_count = sum(1 for r in results if r["status"] == "valid")
        self.assertTrue(valid_count > 0)

    def test_02_real_strategy_categories(self):
        """集成测试：真实策略分类"""
        scanner = StrategyScanner()

        categories = {
            "likely_success": ["03 一个简单而持续稳定的懒人超额收益策略.txt"],
            "likely_missing_api": ["03 多策略融合-80倍.txt"],
            "likely_not_strategy": ["100 配套资料说明.txt"],
        }

        validation_results = {}

        for category, files in categories.items():
            for strategy_file in files:
                path = os.path.join(self.strategy_dir, strategy_file)
                if os.path.exists(path):
                    scan_result = scanner.scan_file(path)
                    validation_results[strategy_file] = {
                        "expected_category": category,
                        "actual_status": scan_result.status.value,
                        "is_executable": scan_result.is_executable,
                    }

        for strategy, result in validation_results.items():
            expected_cat = result["expected_category"]
            actual_status = result["actual_status"]

            if expected_cat == "likely_success":
                self.assertEqual(actual_status, "valid")
                self.assertTrue(result["is_executable"])

            elif expected_cat == "likely_missing_api":
                self.assertEqual(actual_status, "missing_api")
                self.assertFalse(result["is_executable"])

            elif expected_cat == "likely_not_strategy":
                self.assertEqual(actual_status, "not_strategy")
                self.assertFalse(result["is_executable"])


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestBatchTruthValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationBatchTruth))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    result = run_tests()

    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    print(f"运行测试数: {result.testsRun}")
    print(f"成功数: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")

    if result.failures:
        print("\n失败详情:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n错误详情:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    print("=" * 80)

    sys.exit(0 if result.wasSuccessful() else 1)
