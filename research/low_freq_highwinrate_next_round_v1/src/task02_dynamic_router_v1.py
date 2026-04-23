from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from common import Thresholds


@dataclass
class RouteDecision:
    state: str
    target_holdings: int
    equity_weight: float
    bond_weight: float
    cash_weight: float


def decide_route(breadth: float, trend_off: bool, thresholds: Thresholds) -> RouteDecision:
    """子任务2：主仓动态路由V1工程化验收规则。"""
    if breadth < thresholds.breadth_empty:
        return RouteDecision("EMPTY", 0, 0.0, 0.6, 0.4)
    if breadth < thresholds.breadth_defensive:
        return RouteDecision("DEFENSIVE", 10, 0.4, 0.4, 0.2)
    if breadth < thresholds.breadth_cautious and trend_off:
        return RouteDecision("CAUTIOUS", 12, 0.6, 0.25, 0.15)
    return RouteDecision("RISK_ON", 15, 0.8, 0.1, 0.1)


def route_dataframe(df: pd.DataFrame, thresholds: Thresholds) -> pd.DataFrame:
    required_cols = {"date", "breadth", "trend_off"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    rows = []
    for _, r in df.iterrows():
        decision = decide_route(float(r["breadth"]), bool(r["trend_off"]), thresholds)
        rows.append(
            {
                "date": r["date"],
                "state": decision.state,
                "target_holdings": decision.target_holdings,
                "equity_weight": decision.equity_weight,
                "bond_weight": decision.bond_weight,
                "cash_weight": decision.cash_weight,
            }
        )
    return pd.DataFrame(rows)
