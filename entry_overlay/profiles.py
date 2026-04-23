from __future__ import annotations

from typing import Dict

BASE = {
    "rsi": 0.08,
    "macd_hist": 0.08,
    "stoch_kd": 0.07,
    "cci": 0.06,
    "willr": 0.06,
    "adx": 0.05,
    "plus_di_minus_di": 0.05,
    "mfi": 0.07,
    "obv_slope": 0.06,
    "adosc": 0.06,
    "bb_pos": 0.07,
    "atr_pct": 0.06,
    "mom": 0.07,
    "trix": 0.08,
    "ultosc": 0.08,
}

TREND = {
    **BASE,
    "macd_hist": 0.10,
    "adx": 0.08,
    "plus_di_minus_di": 0.08,
    "trix": 0.10,
    "mom": 0.09,
}

REVERSAL = {
    **BASE,
    "rsi": 0.10,
    "stoch_kd": 0.10,
    "willr": 0.09,
    "bb_pos": 0.10,
    "cci": 0.08,
}

PROFILE_LIBRARY = {
    "general": BASE,
    "trend": TREND,
    "reversal": REVERSAL,
}


def build_profile_weights(profile: str = "general", normalize: bool = True) -> Dict[str, float]:
    if profile not in PROFILE_LIBRARY:
        raise ValueError(f"unknown profile: {profile}")
    w = PROFILE_LIBRARY[profile].copy()
    if normalize:
        s = sum(w.values())
        w = {k: v / s for k, v in w.items()}
    return w
