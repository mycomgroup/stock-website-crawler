"""
测试文件 - 使用模拟数据测试框架
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import AnalyzerConfig
from market_classifier import MarketStateClassifier
from risk_metrics import RiskMetrics


def test_config():
    """测试配置类"""
    print("测试 AnalyzerConfig...")

    config = AnalyzerConfig(
        start="2020-01-01",
        end="2026-03-28",
        freq="quarterly",
        cost=0.003,
    )

    assert config.start == "2020-01-01"
    assert config.freq == "quarterly"
    assert config.cost == 0.003

    thresholds = config.get_thresholds()
    assert "bull" in thresholds
    assert "mild_down" in thresholds

    print("  ✓ AnalyzerConfig 测试通过")


def test_market_classifier():
    """测试市场状态分类器"""
    print("测试 MarketStateClassifier...")

    classifier = MarketStateClassifier(
        {
            "bull": 0.05,
            "mild_down": -0.05,
        }
    )

    # 测试单个分类
    assert classifier.classify_single(0.10) == "bull"
    assert classifier.classify_single(0.03) == "mild_up"
    assert classifier.classify_single(-0.03) == "mild_down"
    assert classifier.classify_single(-0.10) == "bear"
    assert classifier.classify_single(np.nan) == "unknown"

    # 测试批量分类
    series = pd.Series([0.10, 0.03, -0.03, -0.10, np.nan])
    classified = classifier.classify_series(series)
    assert classified.tolist() == ["bull", "mild_up", "mild_down", "bear", "unknown"]

    # 测试标签
    label = classifier.get_state_label("bull")
    assert "牛市" in label

    print("  ✓ MarketStateClassifier 测试通过")


def test_risk_metrics():
    """测试风险指标计算"""
    print("测试 RiskMetrics...")

    risk_calc = RiskMetrics(risk_free_rate=0.02, periods_per_year=4)

    # 创建模拟数据
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0.02, 0.05, 24))  # 24个季度

    # 测试各项指标
    ann_ret = risk_calc.annualized_return(returns)
    assert isinstance(ann_ret, float)

    ann_vol = risk_calc.annualized_volatility(returns)
    assert ann_vol > 0

    sharpe = risk_calc.sharpe_ratio(returns)
    assert isinstance(sharpe, float)

    max_dd, _, _ = risk_calc.max_drawdown(returns)
    assert max_dd >= 0

    calmar = risk_calc.calmar_ratio(returns)
    assert isinstance(calmar, float)

    win_rate = risk_calc.win_rate(returns)
    assert 0 <= win_rate <= 1

    # 测试全部指标
    all_metrics = risk_calc.calculate_all(returns)
    assert "cumulative_return" in all_metrics
    assert "sharpe_ratio" in all_metrics
    assert "max_drawdown" in all_metrics

    # 测试相对指标
    benchmark_returns = pd.Series(np.random.normal(0.01, 0.04, 24))
    rel_metrics = risk_calc.calculate_relative(returns, benchmark_returns)
    assert "beta" in rel_metrics
    assert "alpha" in rel_metrics
    assert "information_ratio" in rel_metrics

    print("  ✓ RiskMetrics 测试通过")


def test_integration():
    """集成测试"""
    print("测试集成...")

    # 创建模拟数据
    dates = pd.date_range("2020-01-01", "2025-12-31", freq="QS")
    np.random.seed(42)

    data = pd.DataFrame(
        {
            "date": dates,
            "strategy1": np.random.normal(0.03, 0.08, len(dates)),
            "strategy2": np.random.normal(0.02, 0.10, len(dates)),
            "benchmark": np.random.normal(0.01, 0.06, len(dates)),
        }
    )

    # 测试年度分析
    data["year"] = data["date"].dt.year
    yearly = data.groupby("year").agg(
        {
            col: lambda x: (1 + x).prod() - 1
            for col in ["strategy1", "strategy2", "benchmark"]
        }
    )
    assert len(yearly) > 0

    # 测试市场状态分类
    classifier = MarketStateClassifier()
    data["regime"] = classifier.classify_series(data["benchmark"])
    assert "regime" in data.columns

    # 测试风险指标
    risk_calc = RiskMetrics()
    for col in ["strategy1", "strategy2", "benchmark"]:
        metrics = risk_calc.calculate_all(data[col])
        assert len(metrics) > 0

    print("  ✓ 集成测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("运行测试...")
    print("=" * 60)
    print()

    test_config()
    test_market_classifier()
    test_risk_metrics()
    test_integration()

    print()
    print("=" * 60)
    print("所有测试通过!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
