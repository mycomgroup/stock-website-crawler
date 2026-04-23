from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .config import RF7UniverseConfig


REQUIRED_COLUMNS = {
    "date",
    "asset",
    "rfscore",
    "pb_rank_pct",
    "industry",
    "alpha_rank",
    "tradable",
}


@dataclass
class SelectionArtifacts:
    selected: pd.DataFrame
    dropped: pd.DataFrame


class RF7Selector:
    def __init__(self, config: RF7UniverseConfig) -> None:
        self.config = config

    def select(self, df: pd.DataFrame) -> SelectionArtifacts:
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        data = df.copy()
        data["in_pb_main"] = data["pb_rank_pct"] <= self.config.pb_main_threshold
        data["in_pb_secondary"] = (data["pb_rank_pct"] > self.config.pb_main_threshold) & (
            data["pb_rank_pct"] <= self.config.pb_secondary_threshold
        )
        data["rf7_pass"] = data["rfscore"] == self.config.rfscore_exact
        data["hard_filter_pass"] = data.get(self.config.hard_filter_column, True).astype(bool)
        data["tradable"] = data["tradable"].astype(bool)

        data["pool_type"] = "none"
        data.loc[data["in_pb_main"], "pool_type"] = "main"
        data.loc[data["in_pb_secondary"], "pool_type"] = "secondary"

        gate = (
            data["rf7_pass"]
            & data["hard_filter_pass"]
            & data["tradable"]
            & data["pool_type"].isin(["main", "secondary"])
        )
        selected = data[gate].copy()
        selected = selected.sort_values(["date", "pool_type", "alpha_rank"], ascending=[True, True, True])

        dropped = data[~gate].copy()
        return SelectionArtifacts(selected=selected, dropped=dropped)
