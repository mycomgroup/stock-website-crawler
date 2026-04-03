"""
signals/divergence_signals.py
背离类信号检测模块。

背离类信号：从"同步"变"背离"的状态变化

信号返回值：
- 1: 底背离（看涨）- 价格创新低，指标未创新低
- -1: 顶背离（看跌）- 价格创新高，指标未创新高
- 0: 无背离

输出格式：DataFrame
- date: 日期
- signal: 信号值 (1/-1/0)
- type: 信号类型
"""

import warnings
from typing import Optional, Union, Tuple
import pandas as pd
import numpy as np

try:
    from ..factors.technical import _get_daily_ohlcv, _compute_ema, _compute_ma, safe_divide
except ImportError:
    from jk2bt.factors.technical import _get_daily_ohlcv, _compute_ema, _compute_ma
    def safe_divide(a, b, fill_value=np.nan):
        """安全除法，避免除零错误"""
        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.divide(a, b)
            result = np.where(np.isfinite(result), result, fill_value)
        if isinstance(a, pd.Series):
            return pd.Series(result, index=a.index)
        return result


# =====================================================================
# 辅助函数：寻找局部极值
# =====================================================================


def _find_local_extrema(series: pd.Series, window: int = 5) -> Tuple[pd.Series, pd.Series]:
    """
    寻找局部极大值和极小值。

    Parameters
    ----------
    series : pd.Series
        数据序列
    window : int
        判断窗口

    Returns
    -------
    tuple
        (is_local_max, is_local_min) - 布尔序列
    """
    is_local_max = pd.Series(False, index=series.index)
    is_local_min = pd.Series(False, index=series.index)

    for i in range(window, len(series) - window):
        chunk = series.iloc[i - window : i + window + 1]
        if series.iloc[i] == chunk.max():
            is_local_max.iloc[i] = True
        if series.iloc[i] == chunk.min():
            is_local_min.iloc[i] = True

    return is_local_max, is_local_min


def _check_divergence(
    price: pd.Series,
    indicator: pd.Series,
    is_bottom: bool = True,
    lookback: int = 20,
    tolerance: float = 0.02,
) -> pd.Series:
    """
    检测背离。

    Parameters
    ----------
    price : pd.Series
        价格序列
    indicator : pd.Series
        指标序列
    is_bottom : bool
        True=检测底背离，False=检测顶背离
    lookback : int
        回看周期
    tolerance : float
        容差比例

    Returns
    -------
    pd.Series
        背离信号（1/-1/0）
    """
    signal = pd.Series(0, index=price.index)

    # 找局部极值点
    if is_bottom:
        # 底背离：找局部低点
        _, is_local_min = _find_local_extrema(price, window=3)
        local_extrema = is_local_min
    else:
        # 顶背离：找局部高点
        is_local_max, _ = _find_local_extrema(price, window=3)
        local_extrema = is_local_max

    # 获取极值点索引
    extrema_indices = price.index[local_extrema].tolist()

    for i in range(lookback, len(price)):
        if not local_extrema.iloc[i]:
            continue

        # 找之前最近的极值点
        prev_extrema = [idx for idx in extrema_indices if idx < price.index[i]]
        if len(prev_extrema) < 1:
            continue

        prev_idx = prev_extrema[-1]
        j = price.index.get_loc(prev_idx)

        # 比较当前极值和之前极值
        if is_bottom:
            # 底背离：价格创新低，指标未创新低
            price_lower = price.iloc[i] < price.iloc[j] * (1 - tolerance)
            indicator_higher = indicator.iloc[i] > indicator.iloc[j] * (1 + tolerance)

            if price_lower and indicator_higher:
                signal.iloc[i] = 1
        else:
            # 顶背离：价格创新高，指标未创新高
            price_higher = price.iloc[i] > price.iloc[j] * (1 + tolerance)
            indicator_lower = indicator.iloc[i] < indicator.iloc[j] * (1 - tolerance)

            if price_higher and indicator_lower:
                signal.iloc[i] = -1

    return signal


# =====================================================================
# MACD 背离
# =====================================================================


def detect_macd_divergence(
    symbol: str,
    fast: int = 12,
    slow: int = 26,
    signal_period: int = 9,
    lookback: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 MACD 背离信号。

    底背离：价格创新低，MACD柱未创新低
    顶背离：价格创新高，MACD柱未创新高

    Parameters
    ----------
    symbol : str
        股票代码
    fast : int
        快线EMA周期
    slow : int
        慢线EMA周期
    signal_period : int
        DEA周期
    lookback : int
        回看周期
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, macd_value
    """
    need_count = slow + signal_period + lookback + 20
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

    # 计算MACD
    ema_fast = _compute_ema(close, fast)
    ema_slow = _compute_ema(close, slow)
    dif = ema_fast - ema_slow
    dea = _compute_ema(dif, signal_period)
    macd = 2 * (dif - dea)

    # 检测底背离
    bottom_div = _check_divergence(close, macd, is_bottom=True, lookback=lookback)

    # 检测顶背离
    top_div = _check_divergence(close, macd, is_bottom=False, lookback=lookback)

    # 合并信号
    signal = bottom_div + top_div

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "macd_value": macd.values,
        "close": close.values,
    })

    result.loc[result["signal"] == 1, "type"] = "macd_bottom_divergence"
    result.loc[result["signal"] == -1, "type"] = "macd_top_divergence"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# RSI 背离
# =====================================================================


def detect_rsi_divergence(
    symbol: str,
    window: int = 14,
    lookback: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 RSI 背离信号。

    底背离：价格创新低，RSI未创新低
    顶背离：价格创新高，RSI未创新高

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        RSI计算周期
    lookback : int
        回看周期
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, rsi_value
    """
    need_count = window + lookback + 20
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

    # 计算RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = (-delta).where(delta < 0, 0)

    avg_gain = gain.ewm(span=window, adjust=False).mean()
    avg_loss = loss.ewm(span=window, adjust=False).mean()

    rs = safe_divide(avg_gain, avg_loss)
    rsi = 100 - safe_divide(100, 1 + rs)

    # 检测背离
    bottom_div = _check_divergence(close, rsi, is_bottom=True, lookback=lookback)
    top_div = _check_divergence(close, rsi, is_bottom=False, lookback=lookback)

    signal = bottom_div + top_div

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "rsi_value": rsi.values,
        "close": close.values,
    })

    result.loc[result["signal"] == 1, "type"] = "rsi_bottom_divergence"
    result.loc[result["signal"] == -1, "type"] = "rsi_top_divergence"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# Bear Power 背离（空头力量背离）
# =====================================================================


def detect_bear_power_divergence(
    symbol: str,
    window: int = 13,
    lookback: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测空头力量背离信号。

    底背离：价格创新低，空头力量未创新低（空头力量减弱）
    顶背离：价格创新高，多头力量未创新高

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        EMA周期
    lookback : int
        回看周期
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, bear_power
    """
    need_count = window + lookback + 20
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
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    # 计算多头力量和空头力量
    ema = _compute_ema(close, window)
    bull_power = high - ema
    bear_power = low - ema

    # 检测底背离（使用空头力量）
    bottom_div = _check_divergence(close, bear_power, is_bottom=True, lookback=lookback)

    # 检测顶背离（使用多头力量）
    top_div = _check_divergence(close, bull_power, is_bottom=False, lookback=lookback)

    signal = bottom_div + top_div

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "bear_power": bear_power.values,
        "bull_power": bull_power.values,
        "close": close.values,
    })

    result.loc[result["signal"] == 1, "type"] = "bear_power_bottom_divergence"
    result.loc[result["signal"] == -1, "type"] = "bull_power_top_divergence"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# KDJ 背离
# =====================================================================


def detect_kdj_divergence(
    symbol: str,
    n: int = 9,
    m1: int = 3,
    m2: int = 3,
    lookback: int = 20,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    检测 KDJ 背离信号。

    底背离：价格创新低，K值未创新低
    顶背离：价格创新高，K值未创新高

    Parameters
    ----------
    symbol : str
        股票代码
    n : int
        RSV计算周期
    m1 : int
        K值平滑周期
    m2 : int
        D值平滑周期
    lookback : int
        回看周期
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        columns: date, signal, type, k_value, d_value
    """
    need_count = n + m1 + m2 + lookback + 20
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
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    # 计算KDJ
    low_n = low.rolling(window=n, min_periods=n).min()
    high_n = high.rolling(window=n, min_periods=n).max()

    rsv = safe_divide(close - low_n, high_n - low_n) * 100
    k = rsv.ewm(span=m1, adjust=False).mean()
    d = k.ewm(span=m2, adjust=False).mean()

    # 检测背离（使用J值更敏感）
    j = 3 * k - 2 * d

    bottom_div = _check_divergence(close, j, is_bottom=True, lookback=lookback)
    top_div = _check_divergence(close, j, is_bottom=False, lookback=lookback)

    signal = bottom_div + top_div

    result = pd.DataFrame({
        "date": df["date"],
        "signal": signal.values,
        "k_value": k.values,
        "d_value": d.values,
        "j_value": j.values,
        "close": close.values,
    })

    result.loc[result["signal"] == 1, "type"] = "kdj_bottom_divergence"
    result.loc[result["signal"] == -1, "type"] = "kdj_top_divergence"

    result = result[result["signal"] != 0].reset_index(drop=True)

    return result


# =====================================================================
# 批量检测背离信号
# =====================================================================


def detect_all_divergence_signals(
    symbol: str,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    检测所有背离类信号。

    Parameters
    ----------
    symbol : str
        股票代码
    end_date : str, optional
        截止日期

    Returns
    -------
    pd.DataFrame
        所有背离信号汇总
    """
    signals = []

    # MACD背离
    try:
        macd_signals = detect_macd_divergence(
            symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update
        )
        if not macd_signals.empty:
            signals.append(macd_signals)
    except Exception as e:
        warnings.warn(f"MACD背离检测失败: {e}")

    # RSI背离
    try:
        rsi_signals = detect_rsi_divergence(
            symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update
        )
        if not rsi_signals.empty:
            signals.append(rsi_signals)
    except Exception as e:
        warnings.warn(f"RSI背离检测失败: {e}")

    # KDJ背离
    try:
        kdj_signals = detect_kdj_divergence(
            symbol, end_date=end_date, cache_dir=cache_dir, force_update=force_update
        )
        if not kdj_signals.empty:
            signals.append(kdj_signals)
    except Exception as e:
        warnings.warn(f"KDJ背离检测失败: {e}")

    if not signals:
        return pd.DataFrame(columns=["date", "signal", "type"])

    result = pd.concat(signals, ignore_index=True)
    result = result.sort_values("date").reset_index(drop=True)

    return result


__all__ = [
    "detect_macd_divergence",
    "detect_rsi_divergence",
    "detect_bear_power_divergence",
    "detect_kdj_divergence",
    "detect_all_divergence_signals",
]