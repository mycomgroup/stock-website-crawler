from __future__ import annotations

import pandas as pd

from project.pipeline import RF7Pipeline
from project.validator import ConsistencyValidator


def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"date": "2024-01-31", "asset": "A", "rfscore": 7, "pb_rank_pct": 0.05, "industry": "银行", "alpha_rank": 1, "tradable": True, "hard_filter_pass": True},
            {"date": "2024-01-31", "asset": "B", "rfscore": 7, "pb_rank_pct": 0.15, "industry": "有色", "alpha_rank": 2, "tradable": True, "hard_filter_pass": True},
            {"date": "2024-01-31", "asset": "C", "rfscore": 6, "pb_rank_pct": 0.05, "industry": "电子", "alpha_rank": 3, "tradable": True, "hard_filter_pass": True},
            {"date": "2024-01-31", "asset": "D", "rfscore": 7, "pb_rank_pct": 0.25, "industry": "电子", "alpha_rank": 4, "tradable": True, "hard_filter_pass": True},
        ]
    ).assign(date=lambda x: pd.to_datetime(x["date"]))


def test_rf7_strict_gate_and_pb_pool() -> None:
    selected, _ = RF7Pipeline().run(sample_df())
    assert set(selected["asset"]) == {"A", "B"}
    assert (selected["rfscore"] == 7).all()
    assert (selected["pb_rank_pct"] <= 0.20).all()


def test_keep_cash_when_insufficient_candidates() -> None:
    selected, alloc = RF7Pipeline().run(sample_df())
    assert len(selected) == 2
    cash_ratio = float(alloc["cash_ratio"].iloc[0])
    assert cash_ratio > 0


def test_consistency_validator_basics() -> None:
    _, alloc = RF7Pipeline().run(sample_df())
    report = ConsistencyValidator.compare(alloc, alloc, alloc)
    assert report.core_field_match_rate == 1.0
    assert report.max_weight_abs_diff == 0.0
