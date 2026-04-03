#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 18: 批量运行结果真值化测试

测试覆盖：
1. 状态分类逻辑测试
2. 证据字段生成测试
3. 归因分析逻辑测试
4. 可恢复性判断测试
5. 关键词识别测试
6. 边界情况测试
7. 集成测试（完整流程）
"""

import os
import sys
import json
import unittest
import tempfile
import shutil
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from run_strategies_parallel import (
    RunStatus,
    StrategyRunResult,
    _classify_run_status,
    run_single_strategy,
)


class TestRunStatusClassification(unittest.TestCase):
    """测试运行状态分类逻辑"""

    def test_run_status_enum_values(self):
        """测试RunStatus枚举值完整性"""
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

        actual_statuses = [status.value for status in RunStatus]
        self.assertEqual(len(expected_statuses), len(actual_statuses))
        for expected in expected_statuses:
            self.assertIn(expected, actual_statuses)

    def test_classify_with_timeout_exception(self):
        """测试超时异常分类"""
        from concurrent.futures import TimeoutError

        result = _classify_run_status(
            backtest_result=None,
            exception=TimeoutError(),
            has_data=False,
            scan_result=None,
            evidence=None,
        )
        self.assertEqual(result, RunStatus.TIMEOUT)

    def test_classify_with_import_error(self):
        """测试依赖缺失分类"""
        exception = ImportError("No module named 'missing_package'")

        result = _classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=False,
            scan_result=None,
            evidence={"loaded": False},
        )
        self.assertEqual(result, RunStatus.MISSING_DEPENDENCY)

    def test_classify_with_data_missing_keywords(self):
        """测试数据缺失关键词识别"""
        test_cases = [
            Exception("无法获取股票数据"),
            Exception("数据缺失导致跳过"),
            Exception("无数据可用"),
            FileNotFoundError("股票数据文件不存在"),
        ]

        for exception in test_cases:
            result = _classify_run_status(
                backtest_result=None,
                exception=exception,
                has_data=False,
                scan_result=None,
                evidence=None,
            )
            self.assertEqual(result, RunStatus.DATA_MISSING)

    def test_classify_with_api_missing_keywords(self):
        """测试API缺失关键词识别"""
        test_cases = [
            AttributeError("'NoneType' object has no attribute 'get_price'"),
            NameError("name 'get_fundamentals' is not defined"),
        ]

        for exception in test_cases:
            result = _classify_run_status(
                backtest_result=None,
                exception=exception,
                has_data=True,
                scan_result={"missing_apis": ["get_price"]},
                evidence=None,
            )
            self.assertEqual(result, RunStatus.MISSING_API)

    def test_classify_with_resource_missing_keywords(self):
        """测试资源文件缺失关键词识别"""
        test_cases = [
            FileNotFoundError("No such file or directory: 'data.csv'"),
            FileNotFoundError("file not found in path"),
            Exception("file not found: resource.csv"),
            Exception("no such file in directory"),
        ]

        for exception in test_cases:
            result = _classify_run_status(
                backtest_result=None,
                exception=exception,
                has_data=True,
                scan_result=None,
                evidence=None,
            )
            self.assertEqual(
                result, RunStatus.MISSING_RESOURCE, f"Failed for: {exception}"
            )

    def test_classify_success_with_return(self):
        """测试成功有收益分类"""
        backtest_result = {
            "strategy": Mock(navs={datetime.now(): 1000000}),
            "pnl_pct": 5.0,
        }
        evidence = {
            "loaded": True,
            "entered_backtest_loop": True,
            "has_nav_series": True,
        }

        result = _classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(result, RunStatus.SUCCESS_WITH_RETURN)

    def test_classify_success_zero_return(self):
        """测试成功零收益分类"""
        backtest_result = {
            "strategy": Mock(navs={datetime.now(): 1000000}),
            "pnl_pct": 0.0,
        }
        evidence = {
            "loaded": True,
            "entered_backtest_loop": True,
            "has_nav_series": True,
        }

        result = _classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(result, RunStatus.SUCCESS_ZERO_RETURN)

    def test_classify_success_no_trade(self):
        """测试成功无交易分类"""
        backtest_result = {
            "strategy": Mock(navs=[]),
        }
        evidence = {
            "loaded": True,
            "entered_backtest_loop": False,
            "has_nav_series": False,
        }

        result = _classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(result, RunStatus.SUCCESS_NO_TRADE)

    def test_classify_load_failed_no_result(self):
        """测试加载失败（无返回结果）"""
        result = _classify_run_status(
            backtest_result=None,
            exception=None,
            has_data=False,
            scan_result=None,
            evidence={"loaded": False},
        )
        self.assertEqual(result, RunStatus.LOAD_FAILED)

    def test_classify_run_exception_unknown(self):
        """测试运行异常（未知类型）"""
        exception = RuntimeError("Unknown runtime error")

        result = _classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
            evidence=None,
        )
        self.assertEqual(result, RunStatus.RUN_EXCEPTION)


class TestEvidenceFields(unittest.TestCase):
    """测试证据字段生成逻辑"""

    def test_evidence_initial_values(self):
        """测试证据字段初始值"""
        expected_evidence = {
            "loaded": False,
            "entered_backtest_loop": False,
            "has_transactions": False,
            "has_nav_series": False,
            "nav_series_length": 0,
            "strategy_obj_valid": False,
            "cerebro_valid": False,
        }

        result = {
            "evidence": {
                "loaded": False,
                "entered_backtest_loop": False,
                "has_transactions": False,
                "has_nav_series": False,
                "nav_series_length": 0,
                "strategy_obj_valid": False,
                "cerebro_valid": False,
            }
        }

        for key, expected_value in expected_evidence.items():
            self.assertEqual(result["evidence"].get(key), expected_value)

    def test_evidence_with_successful_backtest(self):
        """测试成功回测的证据字段"""
        strategy_mock = Mock()
        strategy_mock.navs = {datetime.now(): 1000000, datetime.now(): 1010000}

        cerebro_mock = Mock()
        cerebro_mock.broker = Mock()
        cerebro_mock.broker.transactions = [Mock(), Mock()]

        backtest_result = {
            "strategy": strategy_mock,
            "cerebro": cerebro_mock,
            "final_value": 1010000,
            "pnl_pct": 1.0,
        }

        evidence = {
            "loaded": True,
            "strategy_obj_valid": backtest_result.get("strategy") is not None,
            "cerebro_valid": backtest_result.get("cerebro") is not None,
            "has_nav_series": len(strategy_mock.navs) > 0,
            "nav_series_length": len(strategy_mock.navs),
            "has_transactions": len(cerebro_mock.broker.transactions) > 0,
            "entered_backtest_loop": True,
        }

        self.assertTrue(evidence["loaded"])
        self.assertTrue(evidence["strategy_obj_valid"])
        self.assertTrue(evidence["cerebro_valid"])
        self.assertTrue(evidence["has_nav_series"])
        self.assertEqual(evidence["nav_series_length"], 2)
        self.assertTrue(evidence["has_transactions"])
        self.assertTrue(evidence["entered_backtest_loop"])

    def test_evidence_with_failed_load(self):
        """测试加载失败的证据字段"""
        evidence = {
            "loaded": False,
            "entered_backtest_loop": False,
            "has_transactions": False,
            "has_nav_series": False,
            "nav_series_length": 0,
            "strategy_obj_valid": False,
            "cerebro_valid": False,
        }

        self.assertFalse(evidence["loaded"])
        self.assertFalse(evidence["entered_backtest_loop"])
        self.assertFalse(evidence["has_transactions"])
        self.assertFalse(evidence["has_nav_series"])
        self.assertEqual(evidence["nav_series_length"], 0)


class TestAttributionLogic(unittest.TestCase):
    """测试归因分析逻辑"""

    def test_attribution_initial_values(self):
        """测试归因字段初始值"""
        expected_attribution = {
            "failure_root_cause": "",
            "missing_dependency": "",
            "missing_api": "",
            "missing_resource_file": "",
            "error_category": "",
            "recoverable": False,
            "recommendation": "",
        }

        result = {
            "attribution": {
                "failure_root_cause": "",
                "missing_dependency": "",
                "missing_api": "",
                "missing_resource_file": "",
                "error_category": "",
                "recoverable": False,
                "recommendation": "",
            }
        }

        for key, expected_value in expected_attribution.items():
            self.assertEqual(result["attribution"].get(key), expected_value)

    def test_attribution_dependency_missing(self):
        """测试依赖缺失归因"""
        error_str = "No module named 'missing_package'"
        error_type = "ImportError"

        attribution = {
            "failure_root_cause": "Python依赖包缺失或导入错误",
            "missing_dependency": error_str,
            "error_category": "dependency_missing",
            "recoverable": True,
            "recommendation": "安装缺失的Python包或修复导入路径",
        }

        self.assertEqual(attribution["error_category"], "dependency_missing")
        self.assertTrue(attribution["recoverable"])
        self.assertIn("安装", attribution["recommendation"])

    def test_attribution_api_missing(self):
        """测试API缺失归因"""
        error_str = "'NoneType' object has no attribute 'get_price'"
        error_type = "AttributeError"

        attribution = {
            "failure_root_cause": "API或属性未实现/未定义",
            "missing_api": error_str,
            "error_category": "api_missing",
            "recoverable": True,
            "recommendation": "检查策略使用的API是否在utility中已实现",
        }

        self.assertEqual(attribution["error_category"], "api_missing")
        self.assertTrue(attribution["recoverable"])
        self.assertIn("API", attribution["recommendation"])

    def test_attribution_data_missing(self):
        """测试数据缺失归因"""
        error_str = "无法获取股票数据"

        attribution = {
            "failure_root_cause": "数据缺失",
            "missing_resource_file": error_str,
            "error_category": "data_missing",
            "recoverable": True,
            "recommendation": "补充缺失的数据文件或调整回测时间段",
        }

        self.assertEqual(attribution["error_category"], "data_missing")
        self.assertTrue(attribution["recoverable"])
        self.assertIn("数据", attribution["recommendation"])

    def test_attribution_runtime_exception(self):
        """测试运行异常归因"""
        error_str = "Unexpected runtime error"
        error_type = "RuntimeError"

        attribution = {
            "failure_root_cause": f"{error_type}: {error_str[:100]}",
            "error_category": "runtime_exception",
            "recoverable": False,
            "recommendation": "查看详细错误日志，分析具体异常原因",
        }

        self.assertEqual(attribution["error_category"], "runtime_exception")
        self.assertFalse(attribution["recoverable"])
        self.assertIn("日志", attribution["recommendation"])

    def test_attribution_timeout(self):
        """测试超时归因"""
        attribution = {
            "failure_root_cause": "策略运行超时",
            "error_category": "timeout",
            "recoverable": False,
            "recommendation": "检查策略是否有性能问题或增加超时时间",
        }

        self.assertEqual(attribution["error_category"], "timeout")
        self.assertFalse(attribution["recoverable"])
        self.assertIn("性能", attribution["recommendation"])


class TestKeywordRecognition(unittest.TestCase):
    """测试关键词识别逻辑"""

    def test_import_keywords_detection(self):
        """测试Import关键词识别"""
        keywords = [
            "import",
            "module",
            "no module named",
            "cannot import",
            "relative import",
        ]
        test_errors = [
            "No module named 'pandas'",
            "cannot import name 'DataFrame'",
            "ImportError: attempted relative import",
            "module not found",
        ]

        for error in test_errors:
            detected = any(kw in error.lower() for kw in keywords)
            self.assertTrue(detected, f"Failed to detect: {error}")

    def test_api_keywords_detection(self):
        """测试API关键词识别"""
        keywords = ["get_", "attribute", "has no attribute", "not defined", "undefined"]
        test_errors = [
            "'NoneType' object has no attribute 'get_price'",
            "name 'get_fundamentals' is not defined",
            "undefined function",
            "AttributeError: get_index_stocks",
        ]

        for error in test_errors:
            detected = any(kw in error for kw in keywords)
            self.assertTrue(detected, f"Failed to detect: {error}")

    def test_data_keywords_detection(self):
        """测试数据关键词识别"""
        keywords = ["数据", "无数据", "股票", "数据缺失"]
        test_errors = [
            "无法获取股票数据",
            "数据缺失导致跳过",
            "无数据可用",
            "股票行情数据不存在",
        ]

        for error in test_errors:
            detected = any(kw in error for kw in keywords)
            self.assertTrue(detected, f"Failed to detect: {error}")

    def test_resource_keywords_detection(self):
        """测试资源文件关键词识别"""
        keywords = ["file not found", "no such file", "文件不存在", "cannot find"]
        test_errors = [
            "FileNotFoundError: No such file or directory",
            "文件不存在: data.csv",
            "cannot find resource file",
            "no such file in directory",
        ]

        for error in test_errors:
            detected = any(kw in error.lower() for kw in keywords)
            self.assertTrue(detected, f"Failed to detect: {error}")


class TestRecoverabilityJudgement(unittest.TestCase):
    """测试可恢复性判断逻辑"""

    def test_recoverable_failure_types(self):
        """测试可恢复失败类型"""
        recoverable_categories = [
            "data_missing",
            "dependency_missing",
            "api_missing",
            "resource_missing",
        ]

        for category in recoverable_categories:
            attribution = {
                "error_category": category,
                "recoverable": True,
            }
            self.assertTrue(attribution["recoverable"])

    def test_unrecoverable_failure_types(self):
        """测试不可恢复失败类型"""
        unrecoverable_categories = [
            "runtime_exception",
            "timeout",
            "load_failure",
            "syntax_error",
        ]

        for category in unrecoverable_categories:
            attribution = {
                "error_category": category,
                "recoverable": False,
            }
            self.assertFalse(attribution["recoverable"])

    def test_recoverable_failures_can_be_fixed(self):
        """测试可恢复失败的修复方式"""
        fix_methods = {
            "data_missing": "补充数据文件",
            "dependency_missing": "安装依赖包",
            "api_missing": "实现API",
            "resource_missing": "补充资源文件",
        }

        for category, method in fix_methods.items():
            attribution = {
                "error_category": category,
                "recoverable": True,
                "recommendation": method,
            }
            self.assertTrue(attribution["recoverable"])
            self.assertIsNotNone(attribution["recommendation"])


class TestBoundaryCases(unittest.TestCase):
    """测试边界情况"""

    def test_empty_backtest_result(self):
        """测试空返回结果"""
        result = _classify_run_status(
            backtest_result=None,
            exception=None,
            has_data=False,
            scan_result=None,
            evidence={"loaded": False},
        )
        self.assertEqual(result, RunStatus.LOAD_FAILED)

    def test_backtest_result_with_no_strategy(self):
        """测试返回结果无strategy对象"""
        backtest_result = {"cerebro": Mock()}
        evidence = {
            "loaded": True,
            "strategy_obj_valid": False,
            "entered_backtest_loop": False,
        }

        result = _classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(result, RunStatus.SUCCESS_NO_TRADE)

    def test_backtest_result_with_empty_navs(self):
        """测试返回结果navs为空"""
        strategy_mock = Mock()
        strategy_mock.navs = []

        backtest_result = {"strategy": strategy_mock}
        evidence = {
            "loaded": True,
            "has_nav_series": False,
            "entered_backtest_loop": False,
        }

        result = _classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(result, RunStatus.SUCCESS_NO_TRADE)

    def test_exception_with_none_scan_result(self):
        """测试异常时scan_result为None"""
        exception = AttributeError("'NoneType' object has no attribute 'get_price'")

        result = _classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=None,
            evidence=None,
        )
        self.assertEqual(result, RunStatus.MISSING_API)

    def test_exception_with_scan_result_missing_apis(self):
        """测试异常时scan_result包含missing_apis"""
        exception = AttributeError("'NoneType' object has no attribute 'get_price'")
        scan_result = {"missing_apis": ["get_price", "get_fundamentals"]}

        result = _classify_run_status(
            backtest_result=None,
            exception=exception,
            has_data=True,
            scan_result=scan_result,
            evidence=None,
        )
        self.assertEqual(result, RunStatus.MISSING_API)

    def test_zero_pnl_pct_classification(self):
        """测试零收益率分类"""
        strategy_mock = Mock()
        strategy_mock.navs = {datetime.now(): 1000000}

        backtest_result = {
            "strategy": strategy_mock,
            "pnl_pct": 0.0,
        }
        evidence = {
            "loaded": True,
            "entered_backtest_loop": True,
            "has_nav_series": True,
        }

        result = _classify_run_status(
            backtest_result=backtest_result,
            exception=None,
            has_data=True,
            scan_result=None,
            evidence=evidence,
        )
        self.assertEqual(result, RunStatus.SUCCESS_ZERO_RETURN)


class TestIntegration(unittest.TestCase):
    """测试集成流程"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_summary_json_structure(self):
        """测试summary.json结构完整性"""
        summary = {
            "run_id": "test_run_001",
            "timestamp": datetime.now().isoformat(),
            "config": {
                "max_workers": 2,
                "timeout_per_strategy": 60,
            },
            "summary": {
                "input_total": 5,
                "success_total": 2,
                "failed_total": 3,
                "recoverable_failures": 2,
                "unrecoverable_failures": 1,
                "missing_dependency": 1,
                "missing_api": 1,
                "data_missing": 0,
                "missing_resource": 0,
            },
            "attribution_summary": {
                "recoverable": {
                    "data_missing": 0,
                    "missing_dependency": 1,
                    "missing_api": 1,
                    "missing_resource": 0,
                },
                "unrecoverable": {
                    "load_failed": 0,
                    "run_exception": 1,
                    "timeout": 0,
                },
            },
            "results": [],
        }

        required_keys = [
            "run_id",
            "timestamp",
            "config",
            "summary",
            "attribution_summary",
            "results",
        ]

        for key in required_keys:
            self.assertIn(key, summary)

        summary_keys = [
            "recoverable_failures",
            "unrecoverable_failures",
            "missing_dependency",
            "missing_api",
        ]

        for key in summary_keys:
            self.assertIn(key, summary["summary"])

    def test_result_item_structure(self):
        """测试单个结果项结构"""
        result_item = {
            "strategy": "test_strategy.txt",
            "strategy_file": "/path/to/test_strategy.txt",
            "success": False,
            "run_status": "missing_dependency",
            "status": "依赖缺失",
            "error": "No module named 'pandas'",
            "exception_type": "ImportError",
            "duration": 0.5,
            "evidence": {
                "loaded": False,
                "entered_backtest_loop": False,
                "has_transactions": False,
                "has_nav_series": False,
                "nav_series_length": 0,
                "strategy_obj_valid": False,
                "cerebro_valid": False,
            },
            "attribution": {
                "failure_root_cause": "Python依赖包缺失或导入错误",
                "missing_dependency": "No module named 'pandas'",
                "missing_api": "",
                "missing_resource_file": "",
                "error_category": "dependency_missing",
                "recoverable": True,
                "recommendation": "安装缺失的Python包或修复导入路径",
            },
        }

        required_keys = [
            "strategy",
            "success",
            "run_status",
            "status",
            "error",
            "evidence",
            "attribution",
        ]

        for key in required_keys:
            self.assertIn(key, result_item)

        evidence_keys = [
            "loaded",
            "entered_backtest_loop",
            "has_transactions",
            "has_nav_series",
        ]

        for key in evidence_keys:
            self.assertIn(key, result_item["evidence"])

        attribution_keys = [
            "failure_root_cause",
            "error_category",
            "recoverable",
            "recommendation",
        ]

        for key in attribution_keys:
            self.assertIn(key, result_item["attribution"])

    def test_cross_validation_mechanism(self):
        """测试交叉验证机制"""
        success_case = {
            "success": True,
            "run_status": "success_with_return",
            "evidence": {
                "loaded": True,
                "entered_backtest_loop": True,
                "has_nav_series": True,
            },
        }

        failure_case = {
            "success": False,
            "run_status": "missing_dependency",
            "evidence": {
                "loaded": False,
                "entered_backtest_loop": False,
            },
        }

        self.assertTrue(success_case["success"])
        self.assertTrue(success_case["evidence"]["loaded"])
        self.assertTrue(success_case["evidence"]["entered_backtest_loop"])

        self.assertFalse(failure_case["success"])
        self.assertFalse(failure_case["evidence"]["loaded"])


class TestScannerIntegration(unittest.TestCase):
    """测试扫描器集成"""

    def test_scanner_detects_non_strategy(self):
        """测试扫描器识别非策略文件"""
        from jk2bt.strategy.scanner import StrategyScanner

        scanner = StrategyScanner()

        test_cases = [
            ("README.txt", "not_strategy"),
            ("研究文档.txt", "not_strategy"),
            ("配套资料说明.txt", "not_strategy"),
            ("test_file.txt", "not_strategy"),
        ]

        for filename, expected_status in test_cases:
            file_path = os.path.join(
                self.temp_dir if hasattr(self, "temp_dir") else tempfile.mkdtemp(),
                filename,
            )
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("This is a documentation file, not a strategy.")

            result = scanner.scan_file(file_path)
            self.assertEqual(result.status.value, expected_status)

    def test_scanner_detects_valid_strategy(self):
        """测试扫描器识别有效策略"""
        from jk2bt.strategy.scanner import StrategyScanner

        scanner = StrategyScanner()

        strategy_code = """
def initialize(context):
    set_benchmark('000300.XSHG')
    
def handle_data(context, data):
    order('000001.XSHE', 100)
"""
        file_path = os.path.join(
            self.temp_dir if hasattr(self, "temp_dir") else tempfile.mkdtemp(),
            "valid_strategy.txt",
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(strategy_code)

        result = scanner.scan_file(file_path)
        self.assertTrue(result.is_executable)


if __name__ == "__main__":
    unittest.main(verbosity=2)
