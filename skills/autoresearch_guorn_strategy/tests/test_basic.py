"""
基础功能测试
"""

import sys
from pathlib import Path

# 添加父目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scorer import ParsedMetrics, calculate_score, decide_keep_rollback, validate_result
from guorn_mutator import mutate, validate_config, COMMON_INDICATORS


def test_scorer_basic():
    """测试评分器基础功能"""
    metrics = ParsedMetrics(
        status="ok",
        backtest_id="test_001",
        total_return=0.75,
        annual_return=0.15,
        max_drawdown=0.12,
        sharpe=1.5,
        sortino=2.0,
        information_ratio=0.8,
        win_rate=0.65,
        avg_holding_days=25,
        sell_count=120,
    )

    # 测试验证
    is_valid, msg = validate_result(metrics)
    assert is_valid, f"Validation failed: {msg}"

    # 测试评分
    score = calculate_score(metrics)
    assert score > 0, "Score should be positive"
    print(f"✓ Score calculated: {score:.6f}")

    # 测试决策
    decision, reason = decide_keep_rollback(
        new_score=score,
        champion_score=-1e308,
        new_metrics=metrics,
        champion_metrics=None,
    )
    assert decision == "keep", "First version should be kept"
    print(f"✓ Decision: {decision} - {reason}")


def test_mutator_basic():
    """测试变异器基础功能"""
    config = {
        "name": "测试策略",
        "filters": [
            {"factor": "pe_ttm", "operator": "<", "value": 20},
        ],
        "rankings": [
            {"factor": "dividend_yield", "ascending": False, "weight": 1.0},
        ],
        "pool": "hs300",
        "exclude_st": True,
        "holding_num": 15,
        "rebalance_interval": 10,
    }

    # 测试配置验证
    assert validate_config(config), "Config should be valid"
    print("✓ Config validation passed")

    # 测试变异
    new_config, mutation_desc = mutate(config, mutation_type="add_filter")
    assert len(new_config["filters"]) == 2, "Should have 2 filters after add_filter"
    print(f"✓ Mutation: {mutation_desc}")

    # 测试变异后配置仍然合法
    assert validate_config(new_config), "Mutated config should be valid"
    print("✓ Mutated config validation passed")


def test_factor_library():
    """测试因子库"""
    assert len(COMMON_INDICATORS) > 0, "Factor library should not be empty"
    print(f"✓ Factor library loaded: {len(COMMON_INDICATORS)} indicators")

    # 检查关键因子
    key_factors = ["pe_ttm", "pb", "roe", "dividend_yield"]
    for factor in key_factors:
        assert factor in COMMON_INDICATORS, f"Factor {factor} should be in library"
    print(f"✓ Key factors present: {', '.join(key_factors)}")


if __name__ == "__main__":
    print("=" * 70)
    print("Running basic tests...")
    print("=" * 70)

    try:
        test_scorer_basic()
        print()
        test_mutator_basic()
        print()
        test_factor_library()
        print()
        print("=" * 70)
        print("All tests passed!")
        print("=" * 70)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
