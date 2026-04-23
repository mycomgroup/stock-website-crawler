from __future__ import annotations

import pandas as pd


def build_rfscore_whitelist(
    metrics_df: pd.DataFrame,
    min_sharpe_improve: float = 0.05,
    min_drawdown_improve: float = 0.00,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """子任务4：RFScore增强因子白名单化。

    输入列建议：
    - factor
    - sharpe_improve
    - drawdown_improve
    - stability_score
    """
    required_cols = {"factor", "sharpe_improve", "drawdown_improve", "stability_score"}
    missing = required_cols - set(metrics_df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    is_whitelist = (
        (metrics_df["sharpe_improve"] >= min_sharpe_improve)
        & (metrics_df["drawdown_improve"] >= min_drawdown_improve)
        & (metrics_df["stability_score"] >= 0.6)
    )

    whitelist = metrics_df[is_whitelist].copy().sort_values(
        ["sharpe_improve", "stability_score"], ascending=False
    )
    blacklist = metrics_df[~is_whitelist].copy().sort_values(
        ["sharpe_improve", "stability_score"], ascending=[True, True]
    )
    return whitelist, blacklist
