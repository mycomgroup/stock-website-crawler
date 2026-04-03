"""
Task 31 测试用例：日线真实跑通样本池验证

测试策略验证器的正确性，确保能区分真跑通、假跑通和加载失败。

测试覆盖:
1. 真跑通策略（定时器机制）
2. 真跑通策略（handle函数机制）
3. 假跑通策略（无交易）
4. 假跑通策略（无净值变化）
5. 加载失败策略（语法错误）
6. 加载失败策略（缺少模块）
7. 加载失败策略（缺少必要函数）
8. Task19已验证的真实策略
"""

import os
import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jk2bt.core.validator import (
    validate_single_strategy,
    StrategyValidationResult,
    ValidationStatus,
)


class TestTrueRunStrategies:
    """真跑通策略测试"""

    def test_timer_strategy_true_run(self):
        """测试使用定时器机制的策略能正确识别为真跑通"""
        strategy_file = os.path.join(
            os.path.dirname(__file__),
            "validator_samples",
            "true_run_timer_strategy.txt",
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success, f"策略加载失败: {result.load_error}"

        assert result.entered_backtest_loop, (
            f"策略未进入回测循环，状态: {result.final_status}"
        )

        assert result.validation_details.get("timer_triggered", False), "定时器未触发"

        assert result.validation_details.get("final_status") in [
            ValidationStatus.FULL_RUNNING.value,
            ValidationStatus.PARTIAL_RUNNING.value,
        ], f"策略状态异常: {result.final_status}"

        assert result.validation_details.get("is_really_running", False), (
            "策略未判定为真跑通"
        )

    def test_handle_strategy_true_run(self):
        """测试使用handle函数的策略能正确识别为真跑通"""
        strategy_file = os.path.join(
            os.path.dirname(__file__),
            "validator_samples",
            "true_run_handle_strategy.txt",
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success, f"策略加载失败: {result.load_error}"

        assert result.entered_backtest_loop, (
            f"策略未进入回测循环，状态: {result.final_status}"
        )

        assert result.validation_details.get("final_status") in [
            ValidationStatus.FULL_RUNNING.value,
            ValidationStatus.PARTIAL_RUNNING.value,
        ], f"策略状态异常: {result.final_status}"

    def test_etf_rotation_strategy_true_run(self):
        """测试ETF轮动策略能正确识别为真跑通"""
        strategy_file = os.path.join(
            os.path.dirname(__file__), "validator_samples", "true_run_etf_rotation.txt"
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success, f"策略加载失败: {result.load_error}"

        assert result.validation_details.get("timer_triggered", False), "定时器未触发"

    def test_task19_verified_strategy(self):
        """测试Task19已验证的真实策略"""
        strategy_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "jkcode",
            "jkcode",
            "03 一个简单而持续稳定的懒人超额收益策略.txt",
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"Task19策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success, f"Task19策略加载失败: {result.load_error}"

        assert result.entered_backtest_loop, (
            f"Task19策略未进入回测循环，状态: {result.final_status}"
        )

        assert result.validation_details.get("trade_count", 0) > 0, (
            f"Task19策略无交易记录，预期应有交易"
        )

        assert result.validation_details.get("is_really_running", False), (
            "Task19策略未判定为真跑通"
        )


class TestFakeRunStrategies:
    """假跑通策略测试"""

    def test_no_trade_fake_run(self):
        """测试无交易策略应判定为假跑通"""
        strategy_file = os.path.join(
            os.path.dirname(__file__), "validator_samples", "fake_run_no_trade.txt"
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success, f"策略加载失败: {result.load_error}"

        assert result.entered_backtest_loop, "策略应进入回测循环"

        assert not result.has_transactions, "策略应无交易发生"

        assert result.final_value == 100000, (
            f"假跑通策略最终资金应为初始资金，实际: {result.final_value}"
        )

        assert result.validation_details.get("final_status") in [
            ValidationStatus.PARTIAL_RUNNING.value,
            ValidationStatus.SEMANTIC_FAILED.value,
        ], f"假跑通策略状态异常: {result.final_status}"

    def test_no_nav_change_fake_run(self):
        """测试无净值变化策略应判定为假跑通"""
        strategy_file = os.path.join(
            os.path.dirname(__file__), "validator_samples", "fake_run_no_nav.txt"
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success, f"策略加载失败: {result.load_error}"

        assert result.final_value == 100000 or result.pnl_pct == 0, (
            f"假跑通策略盈亏应为0，实际: {result.pnl_pct}%"
        )


class TestLoadFailedStrategies:
    """加载失败策略测试"""

    def test_syntax_error_load_failed(self):
        """测试语法错误策略应加载失败"""
        strategy_file = os.path.join(
            os.path.dirname(__file__), "validator_samples", "fail_syntax_error.txt"
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert not result.load_success, "语法错误策略应加载失败"

        assert result.load_error is not None, "应记录加载错误信息"

        assert "语法" in result.load_error or "Syntax" in result.load_error, (
            f"错误信息应包含语法错误，实际: {result.load_error}"
        )

    def test_missing_module_load_failed(self):
        """测试缺少模块策略应加载失败"""
        strategy_file = os.path.join(
            os.path.dirname(__file__), "validator_samples", "fail_missing_module.txt"
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert not result.load_success, "缺少模块策略应加载失败"

    def test_no_initialize_load_failed(self):
        """测试缺少initialize函数策略应标记为缺少必要函数"""
        strategy_file = os.path.join(
            os.path.dirname(__file__), "validator_samples", "fail_no_initialize.txt"
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success, "策略应能加载"

        has_missing_init = any(
            "initialize" in issue.lower() or "initialize" in str(result.semantic_issues)
            for issue in result.semantic_issues
        )

        assert has_missing_init, (
            f"应识别缺少initialize函数，实际问题: {result.semantic_issues}"
        )


class TestValidatorLogic:
    """验证器逻辑测试"""

    def test_timer_mechanism_recognition(self):
        """测试验证器能识别定时器机制"""
        timer_strategy = os.path.join(
            os.path.dirname(__file__),
            "validator_samples",
            "true_run_timer_strategy.txt",
        )

        if not os.path.exists(timer_strategy):
            pytest.skip(f"测试策略文件不存在: {timer_strategy}")

        result = validate_single_strategy(
            timer_strategy,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success, f"策略加载失败: {result.load_error}"

        assert "定时器注册检查" in result.passed_checks, (
            f"验证器应识别定时器机制，通过检查: {result.passed_checks}"
        )

        no_handle_issue = any(
            "handle" in issue.lower() and "定时器" not in issue
            for issue in result.semantic_issues
        )

        assert not no_handle_issue, (
            f"验证器不应仅因为无handle函数就报错，问题: {result.semantic_issues}"
        )

    def test_handle_function_recognition(self):
        """测试验证器能识别handle函数机制"""
        handle_strategy = os.path.join(
            os.path.dirname(__file__),
            "validator_samples",
            "true_run_handle_strategy.txt",
        )

        if not os.path.exists(handle_strategy):
            pytest.skip(f"测试策略文件不存在: {handle_strategy}")

        result = validate_single_strategy(
            handle_strategy,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.load_success, f"策略加载失败: {result.load_error}"

        assert "handle_data" in result.functions_found or "handle_" in str(
            result.functions_found
        ), f"验证器应识别handle函数，函数列表: {result.functions_found}"

    def test_evidence_collection(self):
        """测试验证器能正确收集证据"""
        strategy_file = os.path.join(
            os.path.dirname(__file__),
            "validator_samples",
            "true_run_timer_strategy.txt",
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.evidence is not None, "证据字典不应为空"

        assert result.evidence.get("loaded", False), "加载证据应为True"

        if result.entered_backtest_loop:
            assert result.evidence.get("entered_backtest_loop", False), (
                "进入回测循环证据应为True"
            )


class TestValidationStatus:
    """验证状态测试"""

    def test_full_running_status(self):
        """测试完全跑通状态"""
        strategy_file = os.path.join(
            os.path.dirname(__file__),
            "validator_samples",
            "true_run_timer_strategy.txt",
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.final_status in [
            ValidationStatus.FULL_RUNNING.value,
            ValidationStatus.PARTIAL_RUNNING.value,
        ], (
            f"真跑通策略状态应为FULL_RUNNING或PARTIAL_RUNNING，实际: {result.final_status}"
        )

    def test_load_failed_status(self):
        """测试加载失败状态"""
        strategy_file = os.path.join(
            os.path.dirname(__file__), "validator_samples", "fail_syntax_error.txt"
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.final_status == ValidationStatus.LOAD_FAILED.value, (
            f"加载失败策略状态应为LOAD_FAILED，实际: {result.final_status}"
        )

    def test_partial_running_status(self):
        """测试部分跑通状态"""
        strategy_file = os.path.join(
            os.path.dirname(__file__), "validator_samples", "fake_run_no_trade.txt"
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        assert result.final_status in [
            ValidationStatus.PARTIAL_RUNNING.value,
            ValidationStatus.SEMANTIC_FAILED.value,
        ], (
            f"假跑通策略状态应为PARTIAL_RUNNING或SEMANTIC_FAILED，实际: {result.final_status}"
        )


class TestCoverageVerification:
    """测试覆盖度验证"""

    def test_all_sample_strategies_covered(self):
        """验证所有样本策略都被测试"""
        samples_dir = os.path.join(os.path.dirname(__file__), "validator_samples")

        if not os.path.exists(samples_dir):
            pytest.skip(f"样本目录不存在: {samples_dir}")

        expected_samples = [
            "true_run_timer_strategy.txt",
            "true_run_handle_strategy.txt",
            "true_run_etf_rotation.txt",
            "fake_run_no_trade.txt",
            "fake_run_no_nav.txt",
            "fail_syntax_error.txt",
            "fail_missing_module.txt",
            "fail_no_initialize.txt",
        ]

        existing_samples = os.listdir(samples_dir)

        for sample in expected_samples:
            assert sample in existing_samples, f"缺少测试样本: {sample}"

    def test_validation_dimensions_coverage(self):
        """验证验证维度覆盖"""
        dimensions = [
            "load_success",
            "entered_backtest_loop",
            "has_transactions",
            "has_nav_series",
            "final_value",
            "pnl_pct",
        ]

        strategy_file = os.path.join(
            os.path.dirname(__file__),
            "validator_samples",
            "true_run_timer_strategy.txt",
        )

        if not os.path.exists(strategy_file):
            pytest.skip(f"测试策略文件不存在: {strategy_file}")

        result = validate_single_strategy(
            strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        for dim in dimensions:
            assert hasattr(result, dim), f"缺少验证维度: {dim}"

    def test_true_run_pool_minimum_count(self):
        """测试真跑通样本池达到最小数量"""
        samples_dir = os.path.join(os.path.dirname(__file__), "validator_samples")

        if not os.path.exists(samples_dir):
            pytest.skip(f"样本目录不存在: {samples_dir}")

        true_run_samples = [
            f for f in os.listdir(samples_dir) if f.startswith("true_run_")
        ]

        assert len(true_run_samples) >= 3, (
            f"真跑通样本应至少3个，实际: {len(true_run_samples)}"
        )


def run_tests():
    """运行测试"""
    import subprocess

    test_file = os.path.abspath(__file__)

    result = subprocess.run(
        ["python3", "-m", "pytest", test_file, "-v", "--tb=short"],
        cwd=os.path.dirname(test_file),
        capture_output=True,
        text=True,
    )

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    return result.returncode


if __name__ == "__main__":
    import sys

    sys.exit(run_tests())
