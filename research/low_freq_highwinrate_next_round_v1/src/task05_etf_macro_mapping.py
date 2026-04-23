from __future__ import annotations

import pandas as pd


def classify_role(strategy_type: str, signal_freq: str, risk_level: str) -> str:
    """子任务5：低频ETF/宏观慢变量并入主账户结构。"""
    s = strategy_type.lower()
    f = signal_freq.lower()
    r = risk_level.lower()

    if "macro" in s and f in {"monthly", "quarterly"}:
        return "仓位器"
    if "etf" in s and r in {"low", "medium"}:
        return "主仓底座"
    if "factor" in s or "vol" in s:
        return "过滤器"
    return "仅参考"


def build_account_mapping(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = {"name", "strategy_type", "signal_freq", "risk_level"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    out = df.copy()
    out["role"] = out.apply(
        lambda r: classify_role(
            str(r["strategy_type"]), str(r["signal_freq"]), str(r["risk_level"])
        ),
        axis=1,
    )
    return out
