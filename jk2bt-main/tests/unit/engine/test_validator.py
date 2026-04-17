"""
test_validator.py
策略验证器单元测试

测试场景覆盖:
1. ValidationStatus 枚举
2. StrategyValidationResult 类
3. validate_strategy_loading 函数
4. validate_strategy_execution 函数 (mocked)
5. determine_final_status 函数
6. validate_single_strategy 函数 (mocked)
7. validate_batch_strategies 函数 (mocked)
8. generate_report 函数
9. 边界情况
"""

import os
import json
import tempfile
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock, mock_open

from jk2bt.engine.validator import (
    ValidationStatus,
    StrategyValidationResult,
    validate_strategy_loading,
    validate_strategy_execution,
    determine_final_status,
    validate_single_strategy,
    validate_batch_strategies,
    generate_report,
)


class TestValidationStatus:
    """测试 ValidationStatus 枚举"""

    def test_all_statuses_exist(self):
        assert ValidationStatus.LOAD_FAILED.value == "load_failed"
        assert ValidationStatus.SYNTAX_ERROR.value == "syntax_error"
        assert ValidationStatus.MISSING_DEPENDENCY.value == "missing_dependency"
        assert ValidationStatus.MISSING_API.value == "missing_api"
        assert ValidationStatus.MISSING_RESOURCE.value == "missing_resource"
        assert ValidationStatus.DATA_MISSING.value == "data_missing"
        assert ValidationStatus.RUN_EXCEPTION.value == "run_exception"
        assert ValidationStatus.ENTERED_BACKTEST_LOOP.value == "entered_backtest_loop"
        assert ValidationStatus.SUCCESS_NO_TRADE.value == "success_no_trade"
        assert ValidationStatus.SUCCESS_WITH_NAV.value == "success_with_nav"
        assert (
            ValidationStatus.SUCCESS_WITH_TRANSACTIONS.value
            == "success_with_transactions"
        )
        assert ValidationStatus.PSEUDO_SUCCESS.value == "pseudo_success"
        assert ValidationStatus.PSEUDO_FAILURE.value == "pseudo_failure"
        assert ValidationStatus.TIMEOUT.value == "timeout"
        assert ValidationStatus.UNKNOWN.value == "unknown"


class TestStrategyValidationResult:
    """测试 StrategyValidationResult 类"""

    def test_init(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        assert result.strategy_file == "/path/to/strategy.py"
        assert result.strategy_name == "strategy.py"
        assert result.timestamp is not None
        assert result.load_success is False
        assert result.run_success is False
        assert result.final_status == ValidationStatus.UNKNOWN.value
        assert result.is_really_running is False

    def test_init_evidence_defaults(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        assert result.evidence["loaded"] is False
        assert result.evidence["has_data"] is True
        assert result.evidence["transaction_count"] == 0

    def test_init_attribution_defaults(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        assert result.attribution["failure_root_cause"] == ""
        assert result.attribution["recoverable"] is False

    def test_to_dict(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = True
        result.trade_occurred = True

        d = result.to_dict()
        assert d["strategy_file"] == "/path/to/strategy.py"
        assert d["load_success"] is True
        assert d["run_success"] is True
        assert d["trade_occurred"] is True
        assert "evidence" in d
        assert "attribution" in d

    def test_to_dict_contains_all_fields(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        d = result.to_dict()
        required_keys = [
            "strategy_file",
            "strategy_name",
            "timestamp",
            "load_success",
            "load_error",
            "functions_found",
            "run_success",
            "run_error",
            "timer_triggered",
            "timer_details",
            "trade_occurred",
            "trade_count",
            "trade_details",
            "nav_curve_exists",
            "nav_curve_valid",
            "nav_details",
            "record_output_exists",
            "record_keys",
            "record_details",
            "semantic_issues",
            "passed_checks",
            "failed_checks",
            "final_status",
            "is_really_running",
            "evidence",
            "attribution",
        ]
        for key in required_keys:
            assert key in d


class TestValidateStrategyLoading:
    """测试策略加载验证"""

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_success_with_functions(self, mock_load):
        mock_load.return_value = (
            {"initialize": MagicMock(), "handle_data": MagicMock()},
            None,
        )
        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_loading("/path/to/strategy.py", result)

        assert result.load_success is True
        assert "initialize" in result.functions_found
        assert "handle_data" in result.functions_found
        assert result.evidence["loaded"] is True

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_success_no_functions(self, mock_load):
        mock_load.return_value = ({}, None)
        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_loading("/path/to/strategy.py", result)

        assert result.load_success is True
        assert result.functions_found == []
        assert len(result.semantic_issues) > 0

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_success_missing_initialize(self, mock_load):
        mock_load.return_value = ({}, None)
        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_loading("/path/to/strategy.py", result)

        assert result.load_success is True
        assert len(result.semantic_issues) > 0

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_success_with_timer(self, mock_load):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        result = StrategyValidationResult("/path/to/strategy.py")

        with patch("builtins.open", mock_open(read_data="run_daily(my_func)")):
            validate_strategy_loading("/path/to/strategy.py", result)

        assert result.load_success is True
        assert "定时器注册检查" in result.passed_checks

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_success_with_handle_timer_funcs(self, mock_load):
        mock_load.return_value = (
            {"initialize": MagicMock(), "handle_data": MagicMock()},
            None,
        )
        result = StrategyValidationResult("/path/to/strategy.py")

        with patch("builtins.open", mock_open(read_data="")):
            validate_strategy_loading("/path/to/strategy.py", result)

        assert result.load_success is True
        assert "策略函数定义检查" in result.passed_checks

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_file_not_found(self, mock_load):
        result = StrategyValidationResult("/nonexistent/strategy.py")
        mock_load.side_effect = FileNotFoundError("File not found")
        validate_strategy_loading("/nonexistent/strategy.py", result)

        assert result.load_success is False
        assert result.load_error is not None
        assert result.attribution["error_type"] == "FileNotFoundError"
        assert result.attribution["recoverable"] is True

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_syntax_error(self, mock_load):
        result = StrategyValidationResult("/path/to/strategy.py")
        syntax_err = SyntaxError("invalid syntax")
        syntax_err.msg = "invalid syntax"
        syntax_err.lineno = 10
        mock_load.side_effect = syntax_err

        validate_strategy_loading("/path/to/strategy.py", result)

        assert result.load_success is False
        assert result.attribution["error_type"] == "SyntaxError"
        assert result.attribution["error_category"] == "syntax_error"

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_import_error(self, mock_load):
        result = StrategyValidationResult("/path/to/strategy.py")
        mock_load.side_effect = ImportError("No module named 'xyz'")

        validate_strategy_loading("/path/to/strategy.py", result)

        assert result.load_success is False
        assert result.attribution["error_type"] == "ImportError"
        assert result.attribution["error_category"] == "dependency_missing"
        assert result.attribution["recoverable"] is True

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_unicode_error(self, mock_load):
        result = StrategyValidationResult("/path/to/strategy.py")
        mock_load.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")

        validate_strategy_loading("/path/to/strategy.py", result)

        assert result.load_success is False
        assert result.attribution["error_type"] == "UnicodeDecodeError"

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_generic_exception(self, mock_load):
        result = StrategyValidationResult("/path/to/strategy.py")
        mock_load.side_effect = RuntimeError("Unexpected error")

        validate_strategy_loading("/path/to/strategy.py", result)

        assert result.load_success is False
        assert result.attribution["error_type"] == "RuntimeError"

    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_load_missing_handle_and_timer(self, mock_load):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        result = StrategyValidationResult("/path/to/strategy.py")

        with patch("builtins.open", mock_open(read_data="")):
            validate_strategy_loading("/path/to/strategy.py", result)

        assert len(result.semantic_issues) > 0
        assert "缺少交易处理函数或定时器注册" in result.semantic_issues[0]


class TestValidateStrategyExecution:
    """测试策略执行验证"""

    @patch("jk2bt.engine.validator.get_record_data")
    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_success_with_trades(
        self, mock_load, mock_run, mock_set_runtime, mock_clear, mock_record
    ):
        mock_load.return_value = (
            {"initialize": MagicMock(), "handle_data": MagicMock()},
            None,
        )

        mock_strategy = MagicMock()
        mock_strategy.orders = [
            {"action": "buy", "symbol": "600519"},
            {"action": "sell", "symbol": "600519"},
        ]
        mock_strategy.navs = [
            1.0,
            1.01,
            1.02,
            1.03,
            1.04,
            1.05,
            1.06,
            1.07,
            1.08,
            1.09,
            1.10,
            1.11,
        ]
        mock_strategy.timer_manager = MagicMock()
        mock_strategy.timer_manager.timers = [MagicMock()]

        mock_run.return_value = {
            "strategy": mock_strategy,
            "cerebro": MagicMock(),
            "final_value": 110000,
            "pnl": 10000,
            "pnl_pct": 0.1,
        }
        mock_record.return_value = {"returns": [0.01, 0.02]}

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.run_success is True
        assert result.trade_occurred is True
        assert result.trade_count == 2
        assert result.nav_curve_exists is True

    @patch("jk2bt.engine.validator.get_record_data")
    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_no_trades(
        self, mock_load, mock_run, mock_set_runtime, mock_clear, mock_record
    ):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        mock_strategy = MagicMock()
        mock_strategy.orders = []
        mock_strategy.navs = []
        mock_strategy.timer_manager = None

        mock_run.return_value = {
            "strategy": mock_strategy,
            "cerebro": MagicMock(),
            "final_value": 100000,
            "pnl": 0,
            "pnl_pct": 0,
        }
        mock_record.return_value = {}

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.run_success is True
        assert result.trade_occurred is False
        assert len(result.semantic_issues) > 0

    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_run_returns_none(
        self, mock_load, mock_run, mock_set_runtime, mock_clear
    ):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        mock_run.return_value = None

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.run_success is False
        assert result.run_error is not None

    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_load_fails(self, mock_load, mock_set_runtime, mock_clear):
        mock_load.return_value = (None, None)

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.run_success is False

    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_exception_data_missing(
        self, mock_load, mock_run, mock_set_runtime, mock_clear
    ):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        mock_run.side_effect = ValueError("无数据")

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.run_success is False
        assert result.attribution["error_category"] == "data_missing"

    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_exception_missing_dependency(
        self, mock_load, mock_run, mock_set_runtime, mock_clear
    ):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        mock_run.side_effect = ImportError("No module named 'pandas'")

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.run_success is False
        assert result.attribution["error_category"] == "dependency_missing"

    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_exception_missing_api(
        self, mock_load, mock_run, mock_set_runtime, mock_clear
    ):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        mock_run.side_effect = AttributeError(
            "'Strategy' object has no attribute 'get_price'"
        )

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.run_success is False
        assert result.attribution["error_category"] == "api_missing"

    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_exception_resource_missing(
        self, mock_load, mock_run, mock_set_runtime, mock_clear
    ):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        mock_run.side_effect = FileNotFoundError("File not found: data.csv")

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.run_success is False
        assert result.attribution["error_category"] == "resource_missing"

    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_exception_generic(
        self, mock_load, mock_run, mock_set_runtime, mock_clear
    ):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        mock_run.side_effect = RuntimeError("Some unknown error")

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.run_success is False
        assert result.attribution["error_category"] == "runtime_exception"

    @patch("jk2bt.engine.validator.get_record_data")
    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_final_value_same_as_initial(
        self, mock_load, mock_run, mock_set_runtime, mock_clear, mock_record
    ):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        mock_strategy = MagicMock()
        mock_strategy.orders = []
        mock_strategy.navs = []
        mock_strategy.timer_manager = None

        mock_run.return_value = {
            "strategy": mock_strategy,
            "cerebro": MagicMock(),
            "final_value": 100000,
            "pnl": 0,
            "pnl_pct": 0,
        }
        mock_record.return_value = {}

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution(
            "/path/to/strategy.py",
            initial_capital=100000,
            result=result,
        )

        assert "最终资金与初始资金相同" in " ".join(result.semantic_issues)

    @patch("jk2bt.engine.validator.get_record_data")
    @patch("jk2bt.engine.validator.clear_runtime_data")
    @patch("jk2bt.engine.validator.set_runtime_dir")
    @patch("jk2bt.engine.validator.run_jq_strategy")
    @patch("jk2bt.engine.validator.load_jq_strategy")
    def test_execution_with_nav_curve_valid(
        self, mock_load, mock_run, mock_set_runtime, mock_clear, mock_record
    ):
        mock_load.return_value = ({"initialize": MagicMock()}, None)
        mock_strategy = MagicMock()
        mock_strategy.orders = [{"action": "buy", "symbol": "600519"}]
        mock_strategy.navs = [1.0 + i * 0.01 for i in range(20)]
        mock_strategy.timer_manager = MagicMock()
        mock_strategy.timer_manager.timers = [MagicMock()]

        mock_run.return_value = {
            "strategy": mock_strategy,
            "cerebro": MagicMock(),
            "final_value": 105000,
            "pnl": 5000,
            "pnl_pct": 0.05,
        }
        mock_record.return_value = {"returns": [0.01]}

        result = StrategyValidationResult("/path/to/strategy.py")
        validate_strategy_execution("/path/to/strategy.py", result=result)

        assert result.nav_curve_exists is True
        assert result.nav_curve_valid is True
        assert result.trade_occurred is True


class TestDetermineFinalStatus:
    """测试最终状态判定"""

    def test_load_failed_syntax_error(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = False
        result.run_success = False
        result.attribution["error_type"] = "SyntaxError"
        determine_final_status(result)
        assert result.final_status == ValidationStatus.SYNTAX_ERROR.value

    def test_load_failed_missing_dependency(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = False
        result.run_success = False
        result.attribution["error_category"] = "dependency_missing"
        determine_final_status(result)
        assert result.final_status == ValidationStatus.MISSING_DEPENDENCY.value

    def test_load_failed_missing_resource(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = False
        result.run_success = False
        result.attribution["error_category"] = "resource_missing"
        determine_final_status(result)
        assert result.final_status == ValidationStatus.MISSING_RESOURCE.value

    def test_load_failed_generic(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = False
        result.run_success = False
        determine_final_status(result)
        assert result.final_status == ValidationStatus.LOAD_FAILED.value

    def test_run_failed_data_missing(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = False
        result.attribution["error_category"] = "data_missing"
        determine_final_status(result)
        assert result.final_status == ValidationStatus.DATA_MISSING.value

    def test_run_failed_missing_api(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = False
        result.attribution["error_category"] = "api_missing"
        determine_final_status(result)
        assert result.final_status == ValidationStatus.MISSING_API.value

    def test_run_failed_missing_dependency(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = False
        result.attribution["error_category"] = "dependency_missing"
        determine_final_status(result)
        assert result.final_status == ValidationStatus.MISSING_DEPENDENCY.value

    def test_run_failed_resource_missing(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = False
        result.attribution["error_category"] = "resource_missing"
        determine_final_status(result)
        assert result.final_status == ValidationStatus.MISSING_RESOURCE.value

    def test_run_failed_generic(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = False
        determine_final_status(result)
        assert result.final_status == ValidationStatus.RUN_EXCEPTION.value

    def test_pseudo_success(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = True
        result.evidence["entered_backtest_loop"] = False
        determine_final_status(result)
        assert result.final_status == ValidationStatus.PSEUDO_SUCCESS.value
        assert result.is_really_running is False

    def test_success_with_transactions(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_transactions"] = True
        result.evidence["has_nav_series"] = True
        result.evidence["nav_series_length"] = 20
        determine_final_status(result)
        assert result.final_status == ValidationStatus.SUCCESS_WITH_TRANSACTIONS.value
        assert result.is_really_running is True

    def test_success_with_nav(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_transactions"] = False
        result.evidence["has_nav_series"] = True
        result.evidence["nav_series_length"] = 20
        result.evidence["pnl_pct"] = 0.05
        determine_final_status(result)
        assert result.final_status == ValidationStatus.SUCCESS_WITH_NAV.value
        assert result.is_really_running is True

    def test_success_no_trade(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["has_transactions"] = False
        result.evidence["has_nav_series"] = True
        result.evidence["nav_series_length"] = 20
        result.evidence["pnl_pct"] = 0
        determine_final_status(result)
        assert result.final_status == ValidationStatus.SUCCESS_NO_TRADE.value
        assert result.is_really_running is True

    def test_pseudo_failure(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = True
        result.evidence["entered_backtest_loop"] = True
        result.evidence["loaded"] = True
        result.evidence["has_transactions"] = False
        result.evidence["has_nav_series"] = False
        result.evidence["nav_series_length"] = 0
        determine_final_status(result)
        assert result.final_status == ValidationStatus.PSEUDO_FAILURE.value

    def test_pseudo_success_when_not_entered_backtest_loop(self):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = True
        result.evidence["entered_backtest_loop"] = False
        determine_final_status(result)
        assert result.final_status == ValidationStatus.PSEUDO_SUCCESS.value
        assert result.is_really_running is False


class TestValidateSingleStrategy:
    """测试单个策略验证"""

    @patch("jk2bt.engine.validator.determine_final_status")
    @patch("jk2bt.engine.validator.validate_strategy_execution")
    @patch("jk2bt.engine.validator.validate_strategy_loading")
    def test_validate_load_failure(self, mock_load, mock_exec, mock_determine):
        def set_load_failure(strategy_file, result):
            result.load_success = False
            result.load_error = "File not found"

        mock_load.side_effect = set_load_failure

        result = validate_single_strategy("/path/to/strategy.py")

        assert result.load_success is False
        mock_exec.assert_not_called()
        mock_determine.assert_called_once()

    @patch("jk2bt.engine.validator.determine_final_status")
    @patch("jk2bt.engine.validator.validate_strategy_execution")
    @patch("jk2bt.engine.validator.validate_strategy_loading")
    def test_validate_execution_failure(self, mock_load, mock_exec, mock_determine):
        def set_load_success(strategy_file, result):
            result.load_success = True
            result.functions_found = ["initialize"]

        def set_exec_failure(*args, **kwargs):
            kwargs["result"].run_success = False
            kwargs["result"].run_error = "Runtime error"

        mock_load.side_effect = set_load_success
        mock_exec.side_effect = set_exec_failure

        result = validate_single_strategy("/path/to/strategy.py")

        assert result.run_success is False
        mock_determine.assert_called_once()

    @patch("jk2bt.engine.validator.determine_final_status")
    @patch("jk2bt.engine.validator.validate_strategy_execution")
    @patch("jk2bt.engine.validator.validate_strategy_loading")
    def test_validate_success_path(self, mock_load, mock_exec, mock_determine):
        def set_load_success(strategy_file, result):
            result.load_success = True
            result.functions_found = ["initialize", "handle_data"]

        def set_exec_success(*args, **kwargs):
            kwargs["result"].run_success = True
            kwargs["result"].timer_triggered = True
            kwargs["result"].trade_occurred = True
            kwargs["result"].nav_curve_valid = True

        mock_load.side_effect = set_load_success
        mock_exec.side_effect = set_exec_success

        result = validate_single_strategy("/path/to/strategy.py")

        assert result.load_success is True
        assert result.run_success is True
        mock_determine.assert_called_once()


class TestValidateBatchStrategies:
    """测试批量策略验证"""

    @patch("jk2bt.engine.validator.validate_single_strategy")
    def test_validate_batch(self, mock_single):
        mock_result = StrategyValidationResult("/path/to/s1.py")
        mock_result.final_status = "success_with_transactions"
        mock_result.is_really_running = True
        mock_single.return_value = mock_result

        results = validate_batch_strategies(
            ["/path/to/s1.py", "/path/to/s2.py"],
            output_file=None,
        )

        assert len(results) == 2
        assert mock_single.call_count == 2

    @patch("jk2bt.engine.validator.validate_single_strategy")
    def test_validate_batch_with_output(self, mock_single, tmp_path):
        mock_result = StrategyValidationResult("/path/to/s1.py")
        mock_result.final_status = "success_with_transactions"
        mock_result.is_really_running = True
        mock_single.return_value = mock_result

        output_file = str(tmp_path / "output.json")
        results = validate_batch_strategies(
            ["/path/to/s1.py"],
            output_file=output_file,
        )

        assert os.path.exists(output_file)
        with open(output_file) as f:
            data = json.load(f)
        assert "results" in data
        assert data["total_strategies"] == 1

    @patch("jk2bt.engine.validator.validate_single_strategy")
    def test_validate_batch_status_counts(self, mock_single):
        r1 = StrategyValidationResult("/path/to/s1.py")
        r1.final_status = "success_with_transactions"
        r1.is_really_running = True
        r2 = StrategyValidationResult("/path/to/s2.py")
        r2.final_status = "load_failed"
        r2.is_really_running = False
        mock_single.side_effect = [r1, r2]

        results = validate_batch_strategies(
            ["/path/to/s1.py", "/path/to/s2.py"],
            output_file=None,
        )

        assert len(results) == 2


class TestGenerateReport:
    """测试报告生成"""

    def test_generate_report_basic(self, tmp_path):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = True
        result.functions_found = ["initialize", "handle_data"]
        result.final_status = "success_with_transactions"
        result.is_really_running = True
        result.timer_triggered = True
        result.trade_occurred = True
        result.nav_curve_valid = True

        output_file = str(tmp_path / "report.md")
        generate_report([result], output_file)

        assert os.path.exists(output_file)
        with open(output_file) as f:
            content = f.read()
        assert "strategy.py" in content
        assert "success_with_transactions" in content

    def test_generate_report_with_issues(self, tmp_path):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = False
        result.final_status = "load_failed"
        result.semantic_issues = ["策略未定义任何函数"]

        output_file = str(tmp_path / "report.md")
        generate_report([result], output_file)

        assert os.path.exists(output_file)
        with open(output_file) as f:
            content = f.read()
        assert "语义异常" in content

    def test_generate_report_no_running_strategies(self, tmp_path):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = False
        result.final_status = "load_failed"
        result.is_really_running = False

        output_file = str(tmp_path / "report.md")
        generate_report([result], output_file)

        with open(output_file) as f:
            content = f.read()
        assert "未发现完全跑通策略" in content

    def test_generate_report_with_trade_details(self, tmp_path):
        result = StrategyValidationResult("/path/to/strategy.py")
        result.load_success = True
        result.run_success = True
        result.functions_found = ["initialize"]
        result.final_status = "success_with_transactions"
        result.is_really_running = True
        result.timer_triggered = True
        result.timer_details = {"timer_count": 1, "timer_types": ["Timer"]}
        result.trade_occurred = True
        result.trade_details = {"total": 5, "buy": 3, "sell": 2}
        result.nav_curve_valid = True
        result.nav_details = {"length": 50, "range_pct": 10.5}

        output_file = str(tmp_path / "report.md")
        generate_report([result], output_file)

        with open(output_file) as f:
            content = f.read()
        assert "5笔" in content
        assert "买入" in content
        assert "卖出" in content

    def test_generate_report_multiple_results(self, tmp_path):
        r1 = StrategyValidationResult("/path/to/s1.py")
        r1.load_success = True
        r1.run_success = True
        r1.final_status = "success_with_transactions"
        r1.is_really_running = True

        r2 = StrategyValidationResult("/path/to/s2.py")
        r2.load_success = False
        r2.final_status = "load_failed"
        r2.is_really_running = False

        output_file = str(tmp_path / "report.md")
        generate_report([r1, r2], output_file)

        with open(output_file) as f:
            content = f.read()
        assert "s1.py" in content
        assert "s2.py" in content
