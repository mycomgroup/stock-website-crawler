"""
risk/volatility.py
波动率风控模块。

用途：根据波动率调整仓位、计算止损价等。
"""

import warnings
from typing import Optional, Union, Dict
import pandas as pd
import numpy as np

try:
    from ..factors.technical import _get_daily_ohlcv, _compute_ema, safe_divide
except ImportError:
    from jk2bt.factors.technical import _get_daily_ohlcv, _compute_ema
    def safe_divide(a, b, fill_value=np.nan):
        """安全除法，避免除零错误"""
        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.divide(a, b)
            result = np.where(np.isfinite(result), result, fill_value)
        if isinstance(a, pd.Series):
            return pd.Series(result, index=a.index)
        return result


# =====================================================================
# 波动率计算
# =====================================================================


def compute_volatility(
    symbol: str,
    window: int = 20,
    annualized: bool = True,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算历史波动率。

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        计算窗口（默认20日）
    annualized : bool
        是否年化（默认True）
    end_date : str, optional
        截止日期

    Returns
    -------
    float or pd.Series
        波动率
    """
    need_count = window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    # 计算收益率
    ret = close.pct_change()

    # 计算波动率
    vol = ret.rolling(window=window, min_periods=window).std()

    if annualized:
        vol = vol * np.sqrt(252)

    if len(vol) == 1 or end_date:
        return float(vol.iloc[-1])
    return vol


# =====================================================================
# 波动率调整仓位
# =====================================================================


def compute_volatility_adjusted_position(
    symbol: str,
    base_position: float = 1.0,
    target_vol: float = 0.15,
    window: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Dict:
    """
    根据波动率调整仓位。

    公式：adjusted_position = base_position * (target_vol / current_vol)

    Parameters
    ----------
    symbol : str
        股票代码
    base_position : float
        基础仓位比例（默认1.0 = 100%）
    target_vol : float
        目标年化波动率（默认15%）
    window : int
        波动率计算窗口
    end_date : str, optional
        截止日期

    Returns
    -------
    dict
        {
            'adjusted_position': 调整后仓位,
            'current_vol': 当前波动率,
            'target_vol': 目标波动率,
            'vol_ratio': 波动率比率,
        }
    """
    current_vol = compute_volatility(
        symbol,
        window=window,
        annualized=True,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
    )

    if np.isnan(current_vol) or current_vol <= 0:
        return {
            "adjusted_position": base_position,
            "current_vol": np.nan,
            "target_vol": target_vol,
            "vol_ratio": 1.0,
        }

    vol_ratio = target_vol / current_vol
    adjusted_position = base_position * vol_ratio

    # 限制仓位范围
    adjusted_position = max(0.0, min(adjusted_position, base_position * 2))

    return {
        "adjusted_position": adjusted_position,
        "current_vol": current_vol,
        "target_vol": target_vol,
        "vol_ratio": vol_ratio,
    }


# =====================================================================
# ATR 止损
# =====================================================================


def compute_atr_based_stop_loss(
    symbol: str,
    atr_window: int = 14,
    atr_multiplier: float = 2.0,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Dict:
    """
    基于ATR计算止损价。

    Parameters
    ----------
    symbol : str
        股票代码
    atr_window : int
        ATR计算窗口（默认14日）
    atr_multiplier : float
        ATR倍数（默认2倍）
    end_date : str, optional
        截止日期

    Returns
    -------
    dict
        {
            'stop_loss_price': 止损价,
            'atr_value': ATR值,
            'risk_per_share': 每股风险,
            'current_price': 当前价格,
        }
    """
    need_count = atr_window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return {
            "stop_loss_price": np.nan,
            "atr_value": np.nan,
            "risk_per_share": np.nan,
            "current_price": np.nan,
        }

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    # 计算TR
    tr1 = high - low
    tr2 = np.abs(high - close.shift(1))
    tr3 = np.abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # 计算ATR
    atr = tr.ewm(span=atr_window, adjust=False).mean()

    current_price = float(close.iloc[-1])
    atr_value = float(atr.iloc[-1])

    # 计算止损价
    stop_loss_price = current_price - atr_multiplier * atr_value
    risk_per_share = current_price - stop_loss_price

    return {
        "stop_loss_price": stop_loss_price,
        "atr_value": atr_value,
        "risk_per_share": risk_per_share,
        "current_price": current_price,
    }


# =====================================================================
# 波动率突破检测
# =====================================================================


def detect_volatility_regime_change(
    symbol: str,
    short_window: int = 10,
    long_window: int = 60,
    multiplier: float = 1.5,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测波动率状态变化。

    波动率上升：短期波动率 > 长期波动率 × multiplier
    波动率下降：短期波动率 < 长期波动率 / multiplier

    Parameters
    ----------
    symbol : str
        股票代码
    short_window : int
        短期窗口（默认10日）
    long_window : int
        长期窗口（默认60日）
    multiplier : float
        判断阈值倍数
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        波动率状态变化信号
    """
    need_count = long_window + 20
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return pd.DataFrame(columns=["date", "signal", "type"])

    df = df.copy()
    close = df["close"].astype(float)

    # 计算收益率
    ret = close.pct_change()

    # 计算短期和长期波动率
    short_vol = ret.rolling(window=short_window).std() * np.sqrt(252)
    long_vol = ret.rolling(window=long_window).std() * np.sqrt(252)

    # 检测波动率状态变化
    vol_ratio = safe_divide(short_vol, long_vol)

    vol_increase = vol_ratio > multiplier
    vol_decrease = vol_ratio < 1 / multiplier

    signal = pd.Series(0, index=df.index)
    signal[vol_increase] = 1  # 波动率上升
    signal[vol_decrease] = -1  # 波动率下降

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "short_vol": short_vol.values,
        "long_vol": long_vol.values,
        "vol_ratio": vol_ratio.values,
    })

    result.loc[result["signal"] == 1, "type"] = "volatility_increase"
    result.loc[result["signal"] == -1, "type"] = "volatility_decrease"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


__all__ = [
    "compute_volatility",
    "compute_volatility_adjusted_position",
    "compute_atr_based_stop_loss",
    "detect_volatility_regime_change",
]