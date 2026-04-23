from __future__ import annotations

import pandas as pd

from common import Thresholds


def apply_rsrs_filter(df: pd.DataFrame, thresholds: Thresholds) -> pd.DataFrame:
    """子任务3：RSRS过滤层收口（只做过滤层，不做独立策略）。"""
    required_cols = {"date", "signal", "rsrs", "breadth", "sentiment"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    out["pass_rsrs"] = out["rsrs"] >= thresholds.rsrs_min
    out["pass_breadth"] = out["breadth"] >= thresholds.breadth_empty
    out["pass_sentiment"] = out["sentiment"] >= thresholds.sentiment_min
    out["pass_all"] = out[["pass_rsrs", "pass_breadth", "pass_sentiment"]].all(axis=1)
    out["filtered_signal"] = out["signal"].where(out["pass_all"], 0.0)
    return out
