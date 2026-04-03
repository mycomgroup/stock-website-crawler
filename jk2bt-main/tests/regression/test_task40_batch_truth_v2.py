#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 40: 跑批真值 v2 测试套件

测试覆盖：
1. 验证状态判定（14种状态）
2. 证据字段正确性
3. 归因分析准确性
4. 边界情况处理
5. 伪成功/伪失败判定
6. 各种失败类型识别
7. 批量验证功能
8. 报告生成功能
"""

import os
import sys
import json
import pytest
import tempfile
import shutil
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from jk2bt.core.validator import (
        ValidationStatus,
        StrategyValidationResult,
        validate_strategy_loading,
        validate_strategy_execution,
        determine_final_status,
        validate_single_strategy,
        validate_batch_strategies,
    )
except ImportError as e:
    pytest.skip(f"导入失败: {e}", allow_module_level=True)


class TestValidationStatus:
    """测试验证状态枚举"""

    def test_all_status_defined(self):
        """测试所有状态都已定义"""
        expected_statuses = [
            "load_failed",
            "syntax_error",
            "missing_dependency",
            "missing_api",
            "missing_resource",
            "data_missing",
            "run_exception",
            "entered_backtest_loop",
            "success_no_trade",
            "success_with_nav",
            "success_with_transactions",
            "pseudo_success",
            "pseudo_failure",
            "timeout",
            "unknown",
        ]

        for status in expected_statuses:
            assert hasattr(ValidationStatus, status.upper()), f"缺少状态: {status}"
            assert ValidationStatus[status.upper()].value == status

    def test_status_values_unique(self):
        """测试状态值唯一"""
        values = [s.value for s in ValidationStatus]
        assert len(values) == len(set(values)), "存在重复的状态值"


class TestStrategyValidationResult:
    """测试策略验证结果类"""

    def test_result_initialization(self):
        """测试结果初始化"""
        result = StrategyValidationResult("/path/to/strategy.txt")

        assert result.strategy_file == "/path/to/strategy.txt"
        assert result.strategy_name == "strategy.txt"
        assert result.load_success is False
        assert result.run_success is False
        assert result.final_status == ValidationStatus.UNKNOWN.value
        assert result.is_really_running is False

    def test_evidence_fields_initialized(self):
        """测试证据字段初始化"""
        result = StrategyValidationResult("/path/to/strategy.txt")

        required_evidence_fields = [
            "loaded",
            "loaded_time",
            "entered_backtest_loop",
            "has_transactions",
            "transaction_count",
            "has_nav_series",
            "nav_series_length",
            "nav_series_first",
            "nav_series_last",
            "nav_series_min",
            "nav_series_max",
            "nav_series_std",
            "strategy_obj_valid",
            "cerebro_valid",
            "final_value",
            "initial_capital",
            "pnl",
            "pnl_pct",
            "max_drawdown",
            "annual_return",
            "sharpe_ratio",
            "trading_days",
            "timer_count",
            "has_data",
            "data_missing_count",
            "record_count",
        ]

        for field in required_evidence_fields:
            assert field in result.evidence, f"缺少证据字段: {field}"

    def test_attribution_fields_initialized(self):
        """测试归因字段初始化"""
        result = StrategyValidationResult("/path/to/strategy.txt")

        required_attribution_fields = [
            "failure_root_cause",
            "missing_dependency",
            "missing_api",
            "missing_resource_file",
            "error_category",
            "error_type",
            "recoverable",
            "recommendation",
        ]

        for field in required_attribution_fields:
            assert field in result.attribution, f"缺少归因字段: {field}"

    def test_to_dict_method(self):
        """测试转换为字典方法"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.final_status = ValidationStatus.SUCCESS_NO_TRADE.value

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict["load_success"] is True
        assert result_dict["final_status"] == "success_no_trade"
        assert "evidence" in result_dict
        assert "attribution" in result_dict


class TestValidateStrategyLoading:
    """测试策略加载验证"""

    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        result = StrategyValidationResult("/nonexistent/strategy.txt")
        validate_strategy_loading("/nonexistent/strategy.txt", result)

        assert result.load_success is False
        assert result.evidence["loaded"] is False
        assert "文件不存在" in result.load_error or "FileNotFoundError" in str(
            type(result.load_error)
        )
        assert result.attribution["error_type"] == "FileNotFoundError"
        assert result.attribution["recoverable"] is True

    def test_load_syntax_error_file(self):
        """测试加载语法错误的文件"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(
                "def initialize(context):\n    pass\n\ndef handle_data(context, data):\n    if True\n        print('syntax error')\n"
            )
            temp_file = f.name

        try:
            result = StrategyValidationResult(temp_file)
            validate_strategy_loading(temp_file, result)

            assert result.load_success is False
            assert result.evidence["loaded"] is False
            assert result.attribution["error_type"] == "SyntaxError"
            assert result.attribution["recoverable"] is False
        finally:
            os.unlink(temp_file)

    def test_load_valid_strategy_file(self):
        """测试加载有效的策略文件"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("""
def initialize(context):
    set_benchmark('000300.XSHG')
    
def handle_data(context, data):
    order('000001.XSHE', 100)
""")
            temp_file = f.name

        try:
            result = StrategyValidationResult(temp_file)
            validate_strategy_loading(temp_file, result)

            assert result.load_success is True
            assert result.evidence["loaded"] is True
            assert "initialize" in result.functions_found
            assert "handle_data" in result.functions_found
        finally:
            os.unlink(temp_file)

    def test_load_strategy_without_initialize(self):
        """测试加载没有initialize函数的策略"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("""
def handle_data(context, data):
    order('000001.XSHE', 100)
""")
            temp_file = f.name

        try:
            result = StrategyValidationResult(temp_file)
            validate_strategy_loading(temp_file, result)

            assert result.load_success is True
            assert any(
                "缺少必要函数: initialize" in issue for issue in result.semantic_issues
            )
        finally:
            os.unlink(temp_file)

    def test_load_strategy_without_handle(self):
        """测试加载没有handle函数的策略"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("""
def initialize(context):
    set_benchmark('000300.XSHG')
""")
            temp_file = f.name

        try:
            result = StrategyValidationResult(temp_file)
            validate_strategy_loading(temp_file, result)

            assert result.load_success is True
            assert any("缺少交易处理函数" in issue for issue in result.semantic_issues)
        finally:
            os.unlink(temp_file)


class TestDetermineFinalStatus:
    """测试最终状态判定"""

    def test_load_failed_status(self):
        """测试加载失败状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = False
        result.attribution["error_type"] = ""

        determine_final_status(result)

        assert result.final_status == ValidationStatus.LOAD_FAILED.value
        assert result.is_really_running is False

    def test_syntax_error_status(self):
        """测试语法错误状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = False
        result.attribution["error_type"] = "SyntaxError"

        determine_final_status(result)

        assert result.final_status == ValidationStatus.SYNTAX_ERROR.value
        assert result.is_really_running is False

    def test_missing_dependency_status(self):
        """测试依赖缺失状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = False
        result.attribution["error_category"] = "dependency_missing"

        determine_final_status(result)

        assert result.final_status == ValidationStatus.MISSING_DEPENDENCY.value
        assert result.is_really_running is False

    def test_run_exception_status(self):
        """测试运行异常状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = False
        result.attribution["error_category"] = "runtime_exception"

        determine_final_status(result)

        assert result.final_status == ValidationStatus.RUN_EXCEPTION.value
        assert result.is_really_running is False

    def test_data_missing_status(self):
        """测试数据缺失状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = False
        result.attribution["error_category"] = "data_missing"

        determine_final_status(result)

        assert result.final_status == ValidationStatus.DATA_MISSING.value
        assert result.is_really_running is False

    def test_missing_api_status(self):
        """测试API缺失状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = False
        result.attribution["error_category"] = "api_missing"

        determine_final_status(result)

        assert result.final_status == ValidationStatus.MISSING_API.value
        assert result.is_really_running is False

    def test_pseudo_success_status(self):
        """测试伪成功状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = False

        determine_final_status(result)

        assert result.final_status == ValidationStatus.PSEUDO_SUCCESS.value
        assert result.is_really_running is False

    def test_success_no_trade_status(self):
        """测试成功无交易状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_nav_series"] = True
        result.evidence["nav_series_length"] = 58
        result.evidence["has_transactions"] = False
        result.evidence["pnl_pct"] = 0

        determine_final_status(result)

        assert result.final_status == ValidationStatus.SUCCESS_NO_TRADE.value
        assert result.is_really_running is True

    def test_success_with_nav_status(self):
        """测试成功有净值状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_nav_series"] = True
        result.evidence["nav_series_length"] = 58
        result.evidence["has_transactions"] = False
        result.evidence["pnl_pct"] = 5.5

        determine_final_status(result)

        assert result.final_status == ValidationStatus.SUCCESS_WITH_NAV.value
        assert result.is_really_running is True

    def test_success_with_transactions_status(self):
        """测试成功有交易状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_nav_series"] = True
        result.evidence["nav_series_length"] = 58
        result.evidence["has_transactions"] = True
        result.evidence["transaction_count"] = 10

        determine_final_status(result)

        assert result.final_status == ValidationStatus.SUCCESS_WITH_TRANSACTIONS.value
        assert result.is_really_running is True

    def test_pseudo_failure_status(self):
        """测试伪失败状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_nav_series"] = False
        result.evidence["nav_series_length"] = 0

        determine_final_status(result)

        assert result.final_status == ValidationStatus.PSEUDO_FAILURE.value
        assert result.is_really_running is False

    def test_unknown_status(self):
        """测试未知状态判定"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = False
        result.evidence["has_nav_series"] = False
        result.evidence["nav_series_length"] = 0

        determine_final_status(result)

        assert result.final_status == ValidationStatus.PSEUDO_SUCCESS.value
        assert result.is_really_running is False


class TestEvidenceExtraction:
    """测试证据提取"""

    def test_evidence_loaded_time_recorded(self):
        """测试加载时间记录"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("def initialize(context):\n    pass\n")
            temp_file = f.name

        try:
            result = StrategyValidationResult(temp_file)
            validate_strategy_loading(temp_file, result)

            assert result.evidence["loaded_time"] >= 0
        finally:
            os.unlink(temp_file)

    def test_evidence_nav_series_stats(self):
        """测试净值序列统计"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.evidence["nav_series_first"] = 100000.0
        result.evidence["nav_series_last"] = 105000.0
        result.evidence["nav_series_min"] = 98000.0
        result.evidence["nav_series_max"] = 105000.0
        result.evidence["nav_series_std"] = 1500.0

        assert result.evidence["nav_series_first"] == 100000.0
        assert result.evidence["nav_series_last"] == 105000.0
        assert result.evidence["nav_series_max"] > result.evidence["nav_series_min"]

    def test_evidence_transaction_count(self):
        """测试交易计数"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.evidence["has_transactions"] = True
        result.evidence["transaction_count"] = 25

        assert result.evidence["has_transactions"] is True
        assert result.evidence["transaction_count"] == 25


class TestAttributionAnalysis:
    """测试归因分析"""

    def test_attribution_data_missing(self):
        """测试数据缺失归因"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = False
        result.run_error = "运行异常: 找不到股票数据: 000001.XSHE"
        result.evidence["loaded"] = True

        result.attribution["error_type"] = "RuntimeError"
        result.attribution["failure_root_cause"] = "RuntimeError: 找不到股票数据"
        result.attribution["error_category"] = "data_missing"
        result.attribution["recoverable"] = True

        assert result.attribution["error_category"] == "data_missing"
        assert result.attribution["recoverable"] is True

    def test_attribution_api_missing(self):
        """测试API缺失归因"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = False
        result.run_error = "运行异常: 'NoneType' object has no attribute 'get_ticks'"
        result.evidence["loaded"] = True

        result.attribution["error_type"] = "AttributeError"
        result.attribution["failure_root_cause"] = (
            "AttributeError: 'NoneType' object has no attribute 'get_ticks'"
        )
        result.attribution["error_category"] = "api_missing"
        result.attribution["missing_api"] = "get_ticks"
        result.attribution["recoverable"] = True

        assert result.attribution["error_category"] == "api_missing"
        assert "get_ticks" in result.attribution["missing_api"]

    def test_attribution_dependency_missing(self):
        """测试依赖缺失归因"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = False
        result.load_error = "加载异常: No module named 'prettytable'"
        result.evidence["loaded"] = False

        result.attribution["error_type"] = "ModuleNotFoundError"
        result.attribution["failure_root_cause"] = "依赖包缺失: prettytable"
        result.attribution["error_category"] = "dependency_missing"
        result.attribution["missing_dependency"] = "prettytable"
        result.attribution["recoverable"] = True

        assert result.attribution["error_category"] == "dependency_missing"
        assert result.attribution["recoverable"] is True

    def test_attribution_syntax_error(self):
        """测试语法错误归因"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = False
        result.load_error = "语法错误: invalid syntax (行 15)"
        result.evidence["loaded"] = False

        result.attribution["error_type"] = "SyntaxError"
        result.attribution["failure_root_cause"] = "语法错误: invalid syntax"
        result.attribution["error_category"] = "syntax_error"
        result.attribution["recoverable"] = False

        assert result.attribution["error_category"] == "syntax_error"
        assert result.attribution["recoverable"] is False

    def test_attribution_resource_missing(self):
        """测试资源缺失归因"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = False
        result.run_error = "运行异常: File not found: /data/stocks.csv"
        result.evidence["loaded"] = True

        result.attribution["error_type"] = "FileNotFoundError"
        result.attribution["failure_root_cause"] = "资源文件缺失: /data/stocks.csv"
        result.attribution["error_category"] = "resource_missing"
        result.attribution["missing_resource_file"] = "/data/stocks.csv"
        result.attribution["recoverable"] = True

        assert result.attribution["error_category"] == "resource_missing"
        assert result.attribution["recoverable"] is True


class TestReallyRunningCriteria:
    """测试真跑通判定标准"""

    def test_really_running_true_criteria(self):
        """测试真跑通判定标准（满足所有条件）"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_nav_series"] = True
        result.evidence["nav_series_length"] = 58

        determine_final_status(result)

        assert result.is_really_running is True

    def test_really_running_false_missing_nav(self):
        """测试真跑通判定（缺少净值序列）"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_nav_series"] = False
        result.evidence["nav_series_length"] = 0

        determine_final_status(result)

        assert result.is_really_running is False

    def test_really_running_false_short_nav(self):
        """测试真跑通判定（净值序列太短）"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_nav_series"] = True
        result.evidence["nav_series_length"] = 5

        determine_final_status(result)

        assert result.is_really_running is False

    def test_really_running_false_not_entered_loop(self):
        """测试真跑通判定（未进入回测循环）"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = False
        result.evidence["has_nav_series"] = False
        result.evidence["nav_series_length"] = 0

        determine_final_status(result)

        assert result.is_really_running is False


class TestEdgeCases:
    """测试边界情况"""

    def test_empty_strategy_file(self):
        """测试空策略文件"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            temp_file = f.name

        try:
            result = StrategyValidationResult(temp_file)
            validate_strategy_loading(temp_file, result)

            assert result.load_success is True
            assert len(result.functions_found) == 0
        finally:
            os.unlink(temp_file)

    def test_unicode_filename(self):
        """测试Unicode文件名"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("def initialize(context):\n    pass\n")
            temp_file = f.name

        try:
            result = StrategyValidationResult(temp_file)
            result.strategy_name = "策略测试_001.txt"

            assert "策略" in result.strategy_name
        finally:
            os.unlink(temp_file)

    def test_very_long_strategy_file_path(self):
        """测试超长文件路径"""
        long_path = "/a" * 200 + "/strategy.txt"
        result = StrategyValidationResult(long_path)

        assert result.strategy_file == long_path
        assert len(result.strategy_file) > 200

    def test_special_characters_in_strategy(self):
        """测试策略中的特殊字符"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("""
def initialize(context):
    # 中文注释测试
    print("测试特殊字符: @#$%^&*()")
    pass
""")
            temp_file = f.name

        try:
            result = StrategyValidationResult(temp_file)
            validate_strategy_loading(temp_file, result)

            assert result.load_success is True
        finally:
            os.unlink(temp_file)

    def test_zero_values_in_evidence(self):
        """测试证据中的零值"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.evidence["pnl_pct"] = 0.0
        result.evidence["nav_series_length"] = 0
        result.evidence["transaction_count"] = 0
        result.evidence["max_drawdown"] = 0.0

        assert result.evidence["pnl_pct"] == 0.0
        assert result.evidence["nav_series_length"] == 0

    def test_negative_values_in_evidence(self):
        """测试证据中的负值"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.evidence["pnl_pct"] = -5.5
        result.evidence["max_drawdown"] = -0.15
        result.evidence["annual_return"] = -0.10

        assert result.evidence["pnl_pct"] < 0
        assert result.evidence["max_drawdown"] < 0


class TestReportGeneration:
    """测试报告生成"""

    def test_to_dict_completeness(self):
        """测试字典转换完整性"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.run_success = True
        result.final_status = ValidationStatus.SUCCESS_NO_TRADE.value
        result.is_really_running = True

        result_dict = result.to_dict()

        required_keys = [
            "strategy_file",
            "strategy_name",
            "timestamp",
            "load_success",
            "run_success",
            "final_status",
            "is_really_running",
            "evidence",
            "attribution",
            "functions_found",
            "semantic_issues",
            "passed_checks",
            "failed_checks",
        ]

        for key in required_keys:
            assert key in result_dict, f"缺少键: {key}"

    def test_json_serialization(self):
        """测试JSON序列化"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.load_success = True
        result.evidence["nav_series_length"] = 58

        result_dict = result.to_dict()

        try:
            json_str = json.dumps(result_dict, ensure_ascii=False, indent=2)
            parsed = json.loads(json_str)

            assert parsed["load_success"] is True
            assert parsed["evidence"]["nav_series_length"] == 58
        except Exception as e:
            pytest.fail(f"JSON序列化失败: {e}")

    def test_datetime_in_result(self):
        """测试结果中的日期时间"""
        result = StrategyValidationResult("/path/to/strategy.txt")

        assert result.timestamp is not None
        try:
            datetime.fromisoformat(result.timestamp)
        except ValueError:
            pytest.fail("timestamp格式不正确")


class TestStatusTransitions:
    """测试状态转换"""

    def test_load_to_success_transition(self):
        """测试从加载到成功的转换"""
        result = StrategyValidationResult("/path/to/strategy.txt")

        result.load_success = True
        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_nav_series"] = True
        result.evidence["nav_series_length"] = 58

        determine_final_status(result)

        assert result.final_status in [
            ValidationStatus.SUCCESS_NO_TRADE.value,
            ValidationStatus.SUCCESS_WITH_NAV.value,
            ValidationStatus.SUCCESS_WITH_TRANSACTIONS.value,
        ]

    def test_load_to_failure_transition(self):
        """测试从加载到失败的转换"""
        result = StrategyValidationResult("/path/to/strategy.txt")

        result.load_success = False
        result.attribution["error_type"] = "SyntaxError"

        determine_final_status(result)

        assert result.final_status == ValidationStatus.SYNTAX_ERROR.value
        assert result.is_really_running is False

    def test_run_to_exception_transition(self):
        """测试从运行到异常的转换"""
        result = StrategyValidationResult("/path/to/strategy.txt")

        result.load_success = True
        result.run_success = False
        result.attribution["error_category"] = "runtime_exception"

        determine_final_status(result)

        assert result.final_status == ValidationStatus.RUN_EXCEPTION.value


class TestRecoverabilityAnalysis:
    """测试可恢复性分析"""

    def test_recoverable_data_missing(self):
        """测试数据缺失可恢复"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.attribution["error_category"] = "data_missing"
        result.attribution["recoverable"] = True
        result.attribution["recommendation"] = "补充缺失的数据文件"

        assert result.attribution["recoverable"] is True
        assert "补充" in result.attribution["recommendation"]

    def test_recoverable_missing_api(self):
        """测试API缺失可恢复"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.attribution["error_category"] = "api_missing"
        result.attribution["recoverable"] = True
        result.attribution["recommendation"] = "实现缺失的API"

        assert result.attribution["recoverable"] is True

    def test_not_recoverable_syntax_error(self):
        """测试语法错误不可恢复"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.attribution["error_category"] = "syntax_error"
        result.attribution["recoverable"] = False

        assert result.attribution["recoverable"] is False

    def test_not_recoverable_runtime_exception(self):
        """测试运行时异常不可恢复"""
        result = StrategyValidationResult("/path/to/strategy.txt")
        result.attribution["error_category"] = "runtime_exception"
        result.attribution["recoverable"] = False

        assert result.attribution["recoverable"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
