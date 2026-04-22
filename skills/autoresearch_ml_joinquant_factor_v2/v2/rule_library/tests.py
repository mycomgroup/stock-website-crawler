"""
rule_library 的快速 smoke tests。运行方式:
    python -m pytest v2/rule_library/tests.py -q

或直接跑:
    python v2/rule_library/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from v2.rule_library import (
    apply_strategy,
    expand_search_space,
    load_aliases,
    load_base_filters,
    load_search_space,
    run_backtest,
)
from v2.rule_library.loader import load_candidates, load_strategy
from v2.rule_library.operators import FILTER_OPS, apply_filter_op
from v2.rule_library.schema import Rule, Strategy


CFG = _HERE / "configs"


# ---------- 1. operators ----------

def test_filter_ops_basic():
    s = pd.Series([1, 2, 3, np.nan, 5])
    assert apply_filter_op("gt", s, {"value": 2}).tolist() == [False, False, True, False, True]
    assert apply_filter_op("le", s, {"value": 2}).tolist() == [True, True, False, False, False]
    assert apply_filter_op("between", s,
                          {"low": 2, "high": 4}).tolist() == [False, True, True, False, False]
    assert apply_filter_op("top_pct", s, {"pct": 0.5}).tolist() == \
        [False, False, True, False, True]
    assert apply_filter_op("not_null", s, {}).tolist() == [True, True, True, False, True]


def test_all_operators_registered():
    for op in ["gt", "ge", "lt", "le", "eq", "ne", "between",
              "not_null", "is_null", "top_pct", "bottom_pct",
              "rank_gt", "rank_lt"]:
        assert op in FILTER_OPS


# ---------- 2. loader ----------

def test_loader_resolves_aliases():
    aliases = load_aliases(CFG / "column_aliases.yaml")
    base = load_base_filters(CFG / "small_cap_base.yaml", aliases)
    assert len(base) >= 5
    # EPS 应该被解析成 eps_ttm
    cols = {r.column for r in base}
    assert "eps_ttm" in cols


def test_loader_candidates_inherit_base():
    aliases = load_aliases(CFG / "column_aliases.yaml")
    base = load_base_filters(CFG / "small_cap_base.yaml", aliases)
    cands = load_candidates(CFG / "candidates.yaml", aliases, base)
    assert len(cands) >= 3
    for c in cands:
        # 所有候选都应该继承 base hard_filters
        assert len(c.hard_filters) >= len(base)


def test_loader_search_space():
    aliases = load_aliases(CFG / "column_aliases.yaml")
    base = load_base_filters(CFG / "small_cap_base.yaml", aliases)
    sp = load_search_space(CFG / "search_space.yaml", aliases, base)
    assert len(sp.filter_choices) > 0
    assert len(sp.sort_keys) > 0
    # null variant 应该被解析为 None
    assert any(v is None for ch in sp.filter_choices for v in ch.variants)

    strats = expand_search_space(sp)
    assert 0 < len(strats) <= sp.max_combinations


# ---------- 3. engine ----------

def _fake_cross_section(n=100, seed=0):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "stock_id": [f"S{i:03d}" for i in range(n)],
        "date": pd.to_datetime("2024-01-01"),
        "pchg": rng.normal(0.001, 0.03, n),
        "eps_ttm": rng.uniform(-1, 2, n),
        "roe_ttm": rng.uniform(-0.2, 0.3, n),
        "debt_to_asset_ratio": rng.uniform(0.1, 0.9, n),
        "circulating_market_cap": rng.uniform(1e9, 5e10, n),
        "Rank1M": rng.uniform(0, 1, n),
        "MAC60": rng.uniform(0.7, 1.3, n),
    })


def test_engine_applies_hard_filters():
    df = _fake_cross_section(200)
    s = Strategy(
        name="t",
        hard_filters=[
            Rule("gt", "eps_ttm", {"value": 0}),
            Rule("gt", "roe_ttm", {"value": 0.1}),
        ],
        sort_by=Rule("sort", "Rank1M", {"ascending": False}),
        n_stocks=10,
    )
    out, diag = apply_strategy(df, s, return_diag=True)
    assert (out["eps_ttm"] > 0).all()
    assert (out["roe_ttm"] > 0.1).all()
    assert len(out) <= 10
    assert diag.n_input == 200
    assert diag.n_output == len(out)


def test_engine_handles_missing_column():
    df = _fake_cross_section(50)
    s = Strategy(
        name="t",
        hard_filters=[Rule("gt", "not_a_real_column", {"value": 0})],
        sort_by=Rule("sort", "Rank1M", {"ascending": False}),
        n_stocks=5,
    )
    out, diag = apply_strategy(df, s, return_diag=True)
    # 不崩溃，跳过缺失列，其他流程照常
    assert len(out) == 5
    assert any("missing" in s for s in diag.skipped_rules)


def test_engine_two_stage():
    df = _fake_cross_section(300, seed=1)
    s = Strategy(
        name="t",
        hard_filters=[],
        soft_filters=[Rule("gt", "eps_ttm", {"value": 0.5})],
        sort_by=Rule("sort", "Rank1M", {"ascending": False}),
        n_stocks=10,
        stage1_top_pct=0.1,
        stage1_sort=Rule("sort", "MAC60", {"ascending": False}),
    )
    out = apply_strategy(df, s)
    assert len(out) <= 10


# ---------- 4. backtest ----------

def _fake_panel(n_stocks=50, n_weeks=30, seed=7):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-05", periods=n_weeks, freq="W-FRI")
    rows = []
    for d in dates:
        for i in range(n_stocks):
            rows.append({
                "stock_id": f"S{i:03d}",
                "date": d,
                "pchg": rng.normal(0.002, 0.03),
                "eps_ttm": rng.uniform(-1, 2),
                "roe_ttm": rng.uniform(-0.2, 0.3),
                "Rank1M": rng.uniform(0, 1),
                "MAC60": rng.uniform(0.7, 1.3),
                "net_operate_cash_flow_ttm": rng.uniform(-1e8, 1e10),
                "debt_to_asset_ratio": rng.uniform(0.1, 0.9),
                "quick_ratio": rng.uniform(0.2, 3),
                "earnings_to_price_ratio": rng.uniform(-0.1, 0.2),
                "circulating_market_cap": rng.uniform(1e9, 5e10),
            })
    return pd.DataFrame(rows)


def test_backtest_returns_populated_metrics():
    panel = _fake_panel()
    s = Strategy(
        name="random_top10",
        sort_by=Rule("sort", "Rank1M", {"ascending": False}),
        n_stocks=10,
    )
    r = run_backtest(panel, s, periods_per_year=52, min_weeks=5)
    assert r.n_weeks > 0
    for k in ["ann_return", "ann_vol", "sharpe", "sortino",
              "max_drawdown", "calmar", "ir", "win_rate"]:
        assert k in r.metrics
    assert r.fill_rate > 0.9  # 随机数据下过滤很少


def test_backtest_sparse_strategy_penalized():
    panel = _fake_panel()
    # 极严硬约束：EPS>1.95 基本没股票
    s = Strategy(
        name="too_strict",
        hard_filters=[Rule("gt", "eps_ttm", {"value": 1.95})],
        sort_by=Rule("sort", "Rank1M", {"ascending": False}),
        n_stocks=10,
    )
    r = run_backtest(panel, s, periods_per_year=52, min_weeks=5)
    assert r.fill_rate < 0.5
    # 稀疏惩罚应该把得分压低
    from v2.rule_library.backtest import score as _score
    raw = _score(r.metrics, s)
    assert r.composite_score <= raw


# ---------- run all ----------

def _run_all():
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    failed = []
    for fn in tests:
        try:
            fn()
            print(f"  OK  {fn.__name__}")
        except AssertionError as e:
            print(f"FAIL  {fn.__name__}: {e}")
            failed.append(fn.__name__)
        except Exception as e:
            print(f"ERR   {fn.__name__}: {type(e).__name__}: {e}")
            failed.append(fn.__name__)
    if failed:
        sys.exit(1)
    print(f"\n{len(tests)} tests passed.")


if __name__ == "__main__":
    _run_all()
