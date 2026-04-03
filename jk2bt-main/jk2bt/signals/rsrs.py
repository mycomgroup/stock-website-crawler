"""
indicators/rsrs.py
RSRS择时指标实现（阻力支撑相对强度）。

核心逻辑:
1. 对N日最高价与最低价进行线性回归，得到斜率β
2. 对β进行M日标准化: Z = (β - μ) / σ
3. 右偏修正: RSRS = β × Z
4. 信号规则:
   - RSRS > 0.8: 买入信号
   - RSRS < -0.8: 卖出信号

参考: 《阻力支撑相对强度（RSRS）市场择时策略》
"""

import warnings
from typing import Optional, Union, Dict
import pandas as pd
import numpy as np
from datetime import datetime

try:
    import statsmodels.api as sm

    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    warnings.warn("statsmodels未安装，RSRS指标将不可用")


def compute_rsrs(
    high: pd.Series,
    low: pd.Series,
    N: int = 18,
    M: int = 800,
    method: str = "right_bias",
) -> pd.Series:
    """
    计算 RSRS 指标。

    参数
    ----
    high : pd.Series
        最高价序列
    low : pd.Series
        最低价序列
    N : int
        回归窗口（默认18日）
    M : int
        标准化窗口（默认800日）
    method : str
        计算方法:
        - 'basic': 基础RSRS（仅斜率）
        - 'right_bias': 右偏修正（推荐）
        - 'weighted': 成交量加权

    返回
    ----
    pd.Series
        RSRS指标序列
    """
    if len(high) < N + M:
        warnings.warn(f"数据长度不足，至少需要 {N + M} 个交易日")
        return pd.Series(index=high.index, data=np.nan)

    beta_series = pd.Series(index=high.index, data=np.nan)

    for i in range(N, len(high)):
        high_window = high.iloc[i - N + 1 : i + 1]
        low_window = low.iloc[i - N + 1 : i + 1]

        try:
            X = sm.add_constant(low_window.values)
            y = high_window.values
            model = sm.OLS(y, X).fit()
            beta_series.iloc[i] = model.params[1]
        except Exception:
            beta_series.iloc[i] = np.nan

    if method == "basic":
        return beta_series

    beta_mean = beta_series.rolling(window=M, min_periods=M).mean()
    beta_std = beta_series.rolling(window=M, min_periods=M).std()

    z_score = (beta_series - beta_mean) / beta_std

    if method == "right_bias":
        rsrs = beta_series * z_score
    elif method == "weighted":
        rsrs = beta_series * z_score * np.abs(beta_series)
    else:
        rsrs = z_score

    return rsrs


def compute_rsrs_signal(
    rsrs: pd.Series,
    buy_threshold: float = 0.8,
    sell_threshold: float = -0.8,
) -> pd.Series:
    """
    根据 RSRS 指标生成择时信号。

    参数
    ----
    rsrs : pd.Series
        RSRS指标序列
    buy_threshold : float
        买入阈值（默认0.8）
    sell_threshold : float
        卖出阈值（默认-0.8）

    返回
    ----
    pd.Series
        择时信号: 1 (买入), -1 (卖出), 0 (观望)
    """
    signal = pd.Series(index=rsrs.index, data=0)

    signal[rsrs > buy_threshold] = 1
    signal[rsrs < sell_threshold] = -1

    return signal


def get_rsrs_for_index(
    index_code: str = "000300",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    N: int = 18,
    M: int = 800,
    method: str = "right_bias",
) -> pd.DataFrame:
    """
    计算指数的 RSRS 指标。

    参数
    ----
    index_code : str
        指数代码，如 '000300' (沪深300), '000905' (中证500)
    start_date : str
        开始日期
    end_date : str
        结束日期
    N : int
        回归窗口
    M : int
        标准化窗口
    method : str
        计算方法

    返回
    ----
    pd.DataFrame
        包含 RSRS 指标和择时信号
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    need_days = N + M + 50
    if start_date is None:
        start_dt = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = (start_dt - pd.Timedelta(days=need_days * 1.5)).strftime(
            "%Y-%m-%d"
        )

    try:
        df = ak.stock_zh_index_daily(symbol=f"sh{index_code}")

        if df is not None and not df.empty:
            df = df.rename(
                columns={
                    "date": "date",
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "volume": "volume",
                }
            )

            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date").reset_index(drop=True)

            if start_date:
                df = df[df["date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["date"] <= pd.to_datetime(end_date)]

            high = df["high"]
            low = df["low"]

            rsrs = compute_rsrs(high, low, N, M, method)
            signal = compute_rsrs_signal(rsrs)

            df["rsrs"] = rsrs
            df["rsrs_signal"] = signal

            return df[["date", "close", "rsrs", "rsrs_signal"]]
    except Exception as e:
        warnings.warn(f"获取指数数据失败: {e}")

    return pd.DataFrame()


def get_current_rsrs_signal(
    index_code: str = "000300",
    N: int = 18,
    M: int = 800,
    method: str = "right_bias",
) -> Dict[str, any]:
    """
    获取当前 RSRS 择时信号。

    返回
    ----
    Dict[str, any]
        {
            'signal': 1/-1/0,
            'rsrs_value': 当前RSRS值,
            'description': 信号描述,
            'rsrs_series': 最近RSRS序列
        }
    """
    df = get_rsrs_for_index(index_code, N=N, M=M, method=method)

    if df.empty:
        return {
            "signal": 0,
            "rsrs_value": 0.0,
            "description": "数据获取失败",
            "rsrs_series": None,
        }

    latest = df.iloc[-1]
    rsrs_value = float(latest["rsrs"])
    signal = int(latest["rsrs_signal"])

    if signal == 1:
        desc = f"RSRS={rsrs_value:.2f}，看多信号（大于0.8）"
    elif signal == -1:
        desc = f"RSRS={rsrs_value:.2f}，看空信号（小于-0.8）"
    else:
        desc = f"RSRS={rsrs_value:.2f}，观望信号"

    return {
        "signal": signal,
        "rsrs_value": rsrs_value,
        "description": desc,
        "rsrs_series": df["rsrs"].tail(20),
    }


def compute_rsrs钝化(
    high: pd.Series,
    low: pd.Series,
    N: int = 18,
    M: int = 800,
    S: int = 5,
) -> pd.Series:
    """
    计算 RSRS 钝化版本（减少频繁信号）。

    参数
    ----
    S : int
        钝化窗口，连续S日信号确认后才执行

    返回
    ----
    pd.Series
        钝化后的择时信号
    """
    rsrs = compute_rsrs(high, low, N, M, "right_bias")
    raw_signal = compute_rsrs_signal(rsrs)

    smooth_signal = pd.Series(index=raw_signal.index, data=0)

    for i in range(S, len(raw_signal)):
        window = raw_signal.iloc[i - S : i]

        if (window == 1).all():
            smooth_signal.iloc[i] = 1
        elif (window == -1).all():
            smooth_signal.iloc[i] = -1

    return smooth_signal


def compute_rsrs_weighted(
    high: pd.Series,
    low: pd.Series,
    volume: pd.Series,
    N: int = 18,
    M: int = 800,
) -> pd.Series:
    """
    计算成交量加权 RSRS。

    成交量越大，斜率权重越高。
    """
    beta_series = pd.Series(index=high.index, data=np.nan)

    for i in range(N, len(high)):
        high_window = high.iloc[i - N + 1 : i + 1]
        low_window = low.iloc[i - N + 1 : i + 1]
        volume_window = volume.iloc[i - N + 1 : i + 1]

        try:
            X = sm.add_constant(low_window.values)
            y = high_window.values

            weights = volume_window.values
            weights = weights / weights.sum()

            model = sm.WLS(y, X, weights=weights).fit()
            beta_series.iloc[i] = model.params[1]
        except Exception:
            beta_series.iloc[i] = np.nan

    beta_mean = beta_series.rolling(window=M, min_periods=M).mean()
    beta_std = beta_series.rolling(window=M, min_periods=M).std()

    z_score = (beta_series - beta_mean) / beta_std
    rsrs = beta_series * z_score

    return rsrs


__all__ = [
    "compute_rsrs",
    "compute_rsrs_signal",
    "get_rsrs_for_index",
    "get_current_rsrs_signal",
    "compute_rsrs钝化",
    "compute_rsrs_weighted",
]
