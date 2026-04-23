from __future__ import annotations

import numpy as np
import pandas as pd

try:
    import talib
except Exception:
    talib = None


def _norm_clip(series: pd.Series, low_q=0.03, high_q=0.97) -> pd.Series:
    s = series.replace([np.inf, -np.inf], np.nan).copy()
    lo, hi = s.quantile(low_q), s.quantile(high_q)
    s = s.clip(lo, hi)
    denom = s.max() - s.min()
    if pd.isna(denom) or denom == 0:
        return pd.Series(0.5, index=s.index)
    return (s - s.min()) / denom


def _fallback(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    close, high, low, vol = df["close"], df["high"], df["low"], df["volume"]
    out["rsi"] = _norm_clip(close.pct_change(6).rolling(14).mean())
    out["macd_hist"] = _norm_clip(close.ewm(span=12).mean() - close.ewm(span=26).mean())
    out["stoch_kd"] = _norm_clip((close - low.rolling(9).min()) / (high.rolling(9).max() - low.rolling(9).min() + 1e-9))
    out["cci"] = _norm_clip((close - close.rolling(14).mean()) / (close.rolling(14).std() + 1e-9))
    out["willr"] = _norm_clip((high.rolling(14).max() - close) / (high.rolling(14).max() - low.rolling(14).min() + 1e-9))
    out["adx"] = 0.5
    out["plus_di_minus_di"] = _norm_clip(close.pct_change(3))
    out["mfi"] = _norm_clip((close.diff().fillna(0) * vol).rolling(14).mean())
    out["obv_slope"] = _norm_clip((np.sign(close.diff()).fillna(0) * vol).cumsum().diff(5))
    out["adosc"] = _norm_clip(((close - low) - (high - close)) / (high - low + 1e-9) * vol)
    out["bb_pos"] = _norm_clip((close - close.rolling(20).mean()) / (close.rolling(20).std() + 1e-9))
    out["atr_pct"] = 1 - _norm_clip((high - low).rolling(14).mean() / (close + 1e-9))
    out["mom"] = _norm_clip(close.pct_change(10))
    out["trix"] = _norm_clip(close.ewm(span=15).mean().pct_change())
    out["ultosc"] = _norm_clip((close - low.rolling(7).min()) / (high.rolling(7).max() - low.rolling(7).min() + 1e-9))
    return out.fillna(0.5)


def compute_15_ta_factors(df: pd.DataFrame) -> pd.DataFrame:
    if talib is None:
        return _fallback(df)

    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    vol = df["volume"].values

    out = pd.DataFrame(index=df.index)
    out["rsi"] = talib.RSI(close, 14)
    _, _, macdh = talib.MACD(close, 12, 26, 9)
    out["macd_hist"] = macdh
    k, d = talib.STOCH(high, low, close, 9, 3, 0, 3, 0)
    out["stoch_kd"] = k - d
    out["cci"] = talib.CCI(high, low, close, 14)
    out["willr"] = -talib.WILLR(high, low, close, 14)
    out["adx"] = talib.ADX(high, low, close, 14)
    out["plus_di_minus_di"] = talib.PLUS_DI(high, low, close, 14) - talib.MINUS_DI(high, low, close, 14)
    out["mfi"] = talib.MFI(high, low, close, vol, 14)
    out["obv_slope"] = pd.Series(talib.OBV(close, vol), index=df.index).diff(5)
    out["adosc"] = talib.ADOSC(high, low, close, vol, 3, 10)
    up, _, lowb = talib.BBANDS(close, 20, 2, 2, 0)
    out["bb_pos"] = (close - lowb) / (up - lowb + 1e-9)
    out["atr_pct"] = 1 - talib.ATR(high, low, close, 14) / (close + 1e-9)
    out["mom"] = talib.MOM(close, 10)
    out["trix"] = talib.TRIX(close, 15)
    out["ultosc"] = talib.ULTOSC(high, low, close, 7, 14, 28)

    for c in out.columns:
        out[c] = _norm_clip(pd.Series(out[c], index=df.index))
    return out.fillna(0.5)
