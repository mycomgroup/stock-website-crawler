from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ConsistencyReport:
    core_field_match_rate: float
    avg_weight_abs_diff: float
    max_weight_abs_diff: float
    holding_diff_count: int


class ConsistencyValidator:
    """Research/Monitor/Production consistency checker."""

    @staticmethod
    def compare(research: pd.DataFrame, monitor: pd.DataFrame, production: pd.DataFrame) -> ConsistencyReport:
        keys = ["date", "asset"]
        r = research[keys + ["target_weight"]].rename(columns={"target_weight": "w_research"})
        m = monitor[keys + ["target_weight"]].rename(columns={"target_weight": "w_monitor"})
        p = production[keys + ["target_weight"]].rename(columns={"target_weight": "w_production"})

        merged = r.merge(m, on=keys, how="outer").merge(p, on=keys, how="outer")
        merged = merged.fillna(0.0)

        merged["match_flag"] = (
            (merged["w_research"] == merged["w_monitor"])
            & (merged["w_monitor"] == merged["w_production"])
        )

        merged["abs_diff_rm"] = (merged["w_research"] - merged["w_monitor"]).abs()
        merged["abs_diff_rp"] = (merged["w_research"] - merged["w_production"]).abs()

        core_field_match_rate = float(merged["match_flag"].mean()) if len(merged) else 1.0
        avg_weight_abs_diff = float((merged["abs_diff_rm"] + merged["abs_diff_rp"]).mean() / 2.0) if len(merged) else 0.0
        max_weight_abs_diff = float(pd.concat([merged["abs_diff_rm"], merged["abs_diff_rp"]]).max()) if len(merged) else 0.0

        holding_diff_count = int(
            ((merged["w_research"] == 0) ^ (merged["w_monitor"] == 0)).sum()
            + ((merged["w_research"] == 0) ^ (merged["w_production"] == 0)).sum()
        )

        return ConsistencyReport(
            core_field_match_rate=core_field_match_rate,
            avg_weight_abs_diff=avg_weight_abs_diff,
            max_weight_abs_diff=max_weight_abs_diff,
            holding_diff_count=holding_diff_count,
        )
