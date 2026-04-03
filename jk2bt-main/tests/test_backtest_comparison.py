"""
test_backtest_comparison.py
回测对比方案测试。

验证对比框架的功能正确性。
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os

from tests.backtest_comparison import (
    BacktestResult,
    BacktestComparator,
    BacktestValidator,
    compare_jq_local_backtest,
    safe_divide,
)


class TestBacktestResult:
    """BacktestResult 测试。"""

    def test_create_result(self):
        """创建结果。"""
        result = BacktestResult(
            name="test_strategy",
            total_return=45.6,
            annual_return=18.5,
            max_drawdown=-15.3,
            sharpe_ratio=1.25,
            win_rate=62.5,
            profit_factor=2.1,
            trade_count=156,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

        assert result.name == "test_strategy"
        assert result.total_return == 45.6
        assert result.sharpe_ratio == 1.25

    def test_to_dict(self):
        """转换为字典。"""
        result = BacktestResult(
            name="test",
            total_return=10.0,
            annual_return=5.0,
            max_drawdown=-5.0,
            sharpe_ratio=1.0,
            win_rate=50.0,
            profit_factor=1.0,
            trade_count=10,
            start_date="2020-01-01",
            end_date="2020-12-31",
        )

        d = result.to_dict()
        assert d["name"] == "test"
        assert d["total_return"] == 10.0

    def test_from_dict(self):
        """从字典创建。"""
        data = {
            "name": "test",
            "total_return": 10.0,
            "annual_return": 5.0,
            "max_drawdown": -5.0,
            "sharpe_ratio": 1.0,
            "win_rate": 50.0,
            "profit_factor": 1.0,
            "trade_count": 10,
            "start_date": "2020-01-01",
            "end_date": "2020-12-31",
        }

        result = BacktestResult.from_dict(data)
        assert result.name == "test"
        assert result.total_return == 10.0

    def test_save_and_load(self):
        """保存和加载。"""
        result = BacktestResult(
            name="test",
            total_return=10.0,
            annual_return=5.0,
            max_drawdown=-5.0,
            sharpe_ratio=1.0,
            win_rate=50.0,
            profit_factor=1.0,
            trade_count=10,
            start_date="2020-01-01",
            end_date="2020-12-31",
        )

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            filepath = f.name

        try:
            result.save(filepath)
            loaded = BacktestResult.load(filepath)
            assert loaded.name == result.name
            assert loaded.total_return == result.total_return
        finally:
            os.unlink(filepath)


class TestBacktestComparator:
    """BacktestComparator 测试。"""

    @pytest.fixture
    def sample_results(self):
        """示例结果。"""
        return [
            BacktestResult(
                name="策略A",
                total_return=45.6,
                annual_return=18.5,
                max_drawdown=-15.3,
                sharpe_ratio=1.25,
                win_rate=62.5,
                profit_factor=2.1,
                trade_count=156,
                start_date="2020-01-01",
                end_date="2023-12-31",
            ),
            BacktestResult(
                name="策略B",
                total_return=38.2,
                annual_return=15.5,
                max_drawdown=-12.1,
                sharpe_ratio=1.05,
                win_rate=58.0,
                profit_factor=1.8,
                trade_count=120,
                start_date="2020-01-01",
                end_date="2023-12-31",
            ),
        ]

    def test_compare(self, sample_results):
        """生成对比表格。"""
        comparator = BacktestComparator(sample_results)
        table = comparator.compare()

        assert isinstance(table, pd.DataFrame)
        assert len(table) == 2
        assert "name" in table.columns

    def test_compute_differences(self, sample_results):
        """计算差异。"""
        comparator = BacktestComparator(sample_results)
        diff = comparator.compute_differences("策略A")

        assert isinstance(diff, pd.DataFrame)
        assert len(diff) == 1

    def test_compute_differences_invalid_baseline(self, sample_results):
        """无效基准。"""
        comparator = BacktestComparator(sample_results)

        with pytest.raises(ValueError):
            comparator.compute_differences("不存在")

    def test_generate_report(self, sample_results):
        """生成报告。"""
        comparator = BacktestComparator(sample_results)

        with tempfile.TemporaryDirectory() as tmpdir:
            report_file = comparator.generate_report(tmpdir, baseline="策略A")
            assert os.path.exists(report_file)

            with open(report_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert "策略A" in content
            assert "策略B" in content


class TestBacktestValidator:
    """BacktestValidator 测试。"""

    @pytest.fixture
    def jq_result(self):
        """聚宽结果。"""
        return BacktestResult(
            name="聚宽",
            total_return=45.6,
            annual_return=18.5,
            max_drawdown=-15.3,
            sharpe_ratio=1.25,
            win_rate=62.5,
            profit_factor=2.1,
            trade_count=156,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

    @pytest.fixture
    def local_result(self):
        """本地结果。"""
        return BacktestResult(
            name="本地",
            total_return=44.2,
            annual_return=17.8,
            max_drawdown=-16.1,
            sharpe_ratio=1.18,
            win_rate=61.8,
            profit_factor=2.05,
            trade_count=158,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

    def test_validate_performance_consistency(self, jq_result, local_result):
        """验证绩效一致性。"""
        validator = BacktestValidator(tolerance=0.05)
        result = validator.validate_performance_consistency(jq_result, local_result)

        assert "metrics" in result
        assert "overall_match" in result

    def test_validate_performance_consistency_with_tolerance(self):
        """容差测试。"""
        jq = BacktestResult(
            name="聚宽",
            total_return=100.0,
            annual_return=25.0,
            max_drawdown=-10.0,
            sharpe_ratio=2.0,
            win_rate=70.0,
            profit_factor=3.0,
            trade_count=100,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

        local = BacktestResult(
            name="本地",
            total_return=105.0,
            annual_return=26.0,
            max_drawdown=-11.0,
            sharpe_ratio=2.1,
            win_rate=72.0,
            profit_factor=3.1,
            trade_count=105,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

        validator = BacktestValidator(tolerance=0.10)
        result = validator.validate_performance_consistency(jq, local)

        assert result["overall_match"] == True

    def test_validate_performance_consistency_fail(self):
        """不通过验证。"""
        jq = BacktestResult(
            name="聚宽",
            total_return=100.0,
            annual_return=25.0,
            max_drawdown=-10.0,
            sharpe_ratio=2.0,
            win_rate=70.0,
            profit_factor=3.0,
            trade_count=100,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

        local = BacktestResult(
            name="本地",
            total_return=50.0,
            annual_return=12.0,
            max_drawdown=-25.0,
            sharpe_ratio=0.5,
            win_rate=40.0,
            profit_factor=1.0,
            trade_count=50,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

        validator = BacktestValidator(tolerance=0.05)
        result = validator.validate_performance_consistency(jq, local)

        assert result["overall_match"] == False

    def test_validate_signal_consistency(self):
        """信号一致性验证。"""
        validator = BacktestValidator()

        jq_signals = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
                "signal": [1, 0, 1],
            }
        )
        local_signals = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
                "signal": [1, 0, 0],
            }
        )

        result = validator.validate_signal_consistency(jq_signals, local_signals)

        assert "match_rate" in result
        assert result["match_rate"] == 2 / 3

    def test_validate_trade_consistency(self):
        """交易一致性验证。"""
        validator = BacktestValidator()

        jq_trades = pd.DataFrame(
            {
                "profit": [100, -50, 200, -30],
            }
        )
        local_trades = pd.DataFrame(
            {
                "profit": [100, -50, 200, -30],
            }
        )

        result = validator.validate_trade_consistency(jq_trades, local_trades)

        assert result["trade_count_match"] == True
        assert result["profit_match"] == True

    def test_generate_validation_report(self, jq_result, local_result):
        """生成验证报告。"""
        validator = BacktestValidator()

        with tempfile.TemporaryDirectory() as tmpdir:
            report_file = os.path.join(tmpdir, "validation_report.txt")
            report = validator.generate_validation_report(
                jq_result,
                local_result,
                output_file=report_file,
            )

            assert os.path.exists(report_file)
            assert "聚宽" in report
            assert "本地" in report


class TestCompareJqLocalBacktest:
    """compare_jq_local_backtest 测试。"""

    def test_comparison_result_structure(self):
        """对比结果结构。"""
        jq = BacktestResult(
            name="聚宽",
            total_return=100.0,
            annual_return=25.0,
            max_drawdown=-10.0,
            sharpe_ratio=2.0,
            win_rate=70.0,
            profit_factor=3.0,
            trade_count=100,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

        local = BacktestResult(
            name="本地",
            total_return=95.0,
            annual_return=24.0,
            max_drawdown=-11.0,
            sharpe_ratio=1.9,
            win_rate=68.0,
            profit_factor=2.9,
            trade_count=98,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

        result = compare_jq_local_backtest(jq, local, tolerance=0.10)

        assert "jq_name" in result
        assert "local_name" in result
        assert "metrics" in result
        assert "overall_match" in result
        assert "warnings" in result

    def test_tolerance_threshold(self):
        """容差阈值测试。"""
        jq = BacktestResult(
            name="聚宽",
            total_return=100.0,
            annual_return=25.0,
            max_drawdown=-10.0,
            sharpe_ratio=2.0,
            win_rate=70.0,
            profit_factor=3.0,
            trade_count=100,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

        local = BacktestResult(
            name="本地",
            total_return=100.0,
            annual_return=25.0,
            max_drawdown=-10.0,
            sharpe_ratio=2.0,
            win_rate=70.0,
            profit_factor=3.0,
            trade_count=100,
            start_date="2020-01-01",
            end_date="2023-12-31",
        )

        result = compare_jq_local_backtest(jq, local, tolerance=0.01)

        assert result["overall_match"] == True
        assert len(result["warnings"]) == 0


class TestSafeDivide:
    """safe_divide 测试。"""

    def test_normal_division(self):
        """正常除法。"""
        assert safe_divide(10, 2) == 5.0

    def test_zero_denominator(self):
        """零分母。"""
        assert np.isnan(safe_divide(10, 0))

    def test_nan_denominator(self):
        """NaN 分母。"""
        assert np.isnan(safe_divide(10, np.nan))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
