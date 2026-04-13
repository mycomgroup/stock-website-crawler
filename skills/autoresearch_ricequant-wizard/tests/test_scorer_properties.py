"""
属性测试：scorer.py
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hypothesis import given, settings
from hypothesis import strategies as st

from scorer import ParsedMetrics, calculate_score, decide_keep_rollback


# ── Property 1: 评分公式正确性 ────────────────────────────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 1: 评分公式正确性
@settings(max_examples=100)
@given(
    annual_return=st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False),
    max_drawdown=st.floats(min_value=-1, max_value=1, allow_nan=False, allow_infinity=False),
    sortino=st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False),
    information_ratio=st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False),
)
def test_score_formula_correctness(annual_return, max_drawdown, sortino, information_ratio):
    """Property 1: calculate_score() 应严格等于 calmar*0.55 + sortino*0.25 + ir*0.20"""
    metrics = ParsedMetrics(
        status="finished",
        backtest_id="12345",
        total_return=0.0,
        annual_return=annual_return,
        max_drawdown=max_drawdown,
        sharpe=0.0,
        sortino=sortino,
        information_ratio=information_ratio,
        alpha=0.0,
        beta=1.0,
    )
    result = calculate_score(metrics)
    expected = (annual_return / max(abs(max_drawdown), 0.01)) * 0.55 + sortino * 0.25 + information_ratio * 0.20
    assert math.isclose(result, expected, rel_tol=1e-9), (
        f"score={result} != expected={expected} "
        f"(annual_return={annual_return}, max_drawdown={max_drawdown}, "
        f"sortino={sortino}, ir={information_ratio})"
    )


# ── Property 2: keep 决策条件 ─────────────────────────────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 2: keep 决策条件
@settings(max_examples=100)
@given(
    champion_score=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
    delta=st.floats(min_value=1e-9, max_value=10, allow_nan=False, allow_infinity=False),
    max_drawdown=st.floats(min_value=0, max_value=0.3, allow_nan=False, allow_infinity=False),
)
def test_keep_when_score_better(champion_score, delta, max_drawdown):
    """Property 2: new_score > champion_score 且状态合法且 max_drawdown 未超限时应返回 keep"""
    new_score = champion_score + delta

    new_metrics = ParsedMetrics(
        status="finished",
        backtest_id="99999",
        total_return=0.1,
        annual_return=0.15,
        max_drawdown=max_drawdown,
        sharpe=1.0,
        sortino=1.2,
        information_ratio=0.8,
        alpha=0.05,
        beta=0.9,
    )
    champion_metrics = ParsedMetrics(
        status="finished",
        backtest_id="88888",
        total_return=0.05,
        annual_return=0.10,
        max_drawdown=0.1,
        sharpe=0.8,
        sortino=1.0,
        information_ratio=0.6,
        alpha=0.03,
        beta=0.95,
    )

    decision, reason = decide_keep_rollback(
        new_score=new_score,
        champion_score=champion_score,
        new_metrics=new_metrics,
        champion_metrics=champion_metrics,
        hard_constraints={"max_drawdown_limit": 0.35},
    )
    assert decision == "keep", (
        f"Expected 'keep' but got '{decision}' (reason: {reason}), "
        f"new_score={new_score}, champion_score={champion_score}, max_drawdown={max_drawdown}"
    )


# ── Property 3: rollback 硬约束 ───────────────────────────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 3: rollback 决策条件（硬约束）
@settings(max_examples=100)
@given(
    abs_drawdown=st.floats(min_value=0.36, max_value=2.0, allow_nan=False, allow_infinity=False),
    new_score=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
    champion_score=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
)
def test_rollback_on_drawdown_violation(abs_drawdown, new_score, champion_score):
    """Property 3: abs(max_drawdown) > max_drawdown_limit 时应强制返回 rollback"""
    new_metrics = ParsedMetrics(
        status="finished",
        backtest_id="77777",
        total_return=0.2,
        annual_return=0.25,
        max_drawdown=abs_drawdown,
        sharpe=1.5,
        sortino=1.8,
        information_ratio=1.0,
        alpha=0.1,
        beta=0.85,
    )
    champion_metrics = ParsedMetrics(
        status="finished",
        backtest_id="66666",
        total_return=0.1,
        annual_return=0.12,
        max_drawdown=0.1,
        sharpe=1.0,
        sortino=1.2,
        information_ratio=0.7,
        alpha=0.04,
        beta=0.9,
    )

    decision, reason = decide_keep_rollback(
        new_score=new_score,
        champion_score=champion_score,
        new_metrics=new_metrics,
        champion_metrics=champion_metrics,
        hard_constraints={"max_drawdown_limit": 0.35},
    )
    assert decision == "rollback", (
        f"Expected 'rollback' due to drawdown violation but got '{decision}' "
        f"(reason: {reason}), abs_drawdown={abs_drawdown}"
    )


# ── Property 4: rollback 失败状态 ─────────────────────────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 4: rollback 决策条件（失败状态）
@settings(max_examples=100)
@given(
    status=st.sampled_from(["error_exit", "failed", "error", "cancelled", "timeout", "unknown"]),
    new_score=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
    champion_score=st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
)
def test_rollback_on_failed_status(status, new_score, champion_score):
    """Property 4: 回测状态不是成功状态时应返回 rollback"""
    new_metrics = ParsedMetrics(
        status=status,
        backtest_id="55555",
        total_return=0.0,
        annual_return=0.0,
        max_drawdown=0.1,
        sharpe=0.0,
        sortino=0.0,
        information_ratio=0.0,
        alpha=0.0,
        beta=1.0,
    )
    champion_metrics = ParsedMetrics(
        status="finished",
        backtest_id="44444",
        total_return=0.1,
        annual_return=0.12,
        max_drawdown=0.1,
        sharpe=1.0,
        sortino=1.2,
        information_ratio=0.7,
        alpha=0.04,
        beta=0.9,
    )

    decision, reason = decide_keep_rollback(
        new_score=new_score,
        champion_score=champion_score,
        new_metrics=new_metrics,
        champion_metrics=champion_metrics,
        hard_constraints={"max_drawdown_limit": 0.35},
    )
    assert decision == "rollback", (
        f"Expected 'rollback' for failed status '{status}' but got '{decision}' "
        f"(reason: {reason})"
    )
