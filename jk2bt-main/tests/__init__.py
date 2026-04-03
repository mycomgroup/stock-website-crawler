"""
tests 包初始化文件。

包含测试验证体系：
- test_factor_formula.py: 因子计算公式单元测试
- test_api_compatibility.py: 接口兼容性测试
- backtest_comparison.py: 回测结果对比框架
- test_backtest_comparison.py: 回测对比测试
"""

from tests.backtest_comparison import (
    BacktestResult,
    BacktestComparator,
    BacktestValidator,
    compare_jq_local_backtest,
)

__all__ = [
    "BacktestResult",
    "BacktestComparator",
    "BacktestValidator",
    "compare_jq_local_backtest",
]
