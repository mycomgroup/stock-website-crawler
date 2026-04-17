"""
signals/_base.py
信号检测模块的基础工具函数。
"""

from typing import Optional
import pandas as pd
import numpy as np


def safe_divide(a, b, fill_value=np.nan):
    """安全除法，避免除零错误"""
    with np.errstate(divide="ignore", invalid="ignore"):
        result = np.divide(a, b)
        result = np.where(np.isfinite(result), result, fill_value)
    if isinstance(a, pd.Series):
        return pd.Series(result, index=a.index)
    return result


def _fetch_ohlcv(symbol: str, end_date: Optional[str], count: int) -> pd.DataFrame:
    """通过 adapter 获取日线数据，返回带 date 列的 DataFrame"""
    from jk2bt.data.sources import get_adapter

    if end_date is None:
        end_date = pd.Timestamp.now().strftime("%Y-%m-%d")
    start_date = (
        pd.Timestamp(end_date) - pd.Timedelta(days=int(count * 1.5))
    ).strftime("%Y-%m-%d")

    df = get_adapter().get_daily_data(symbol, start_date, end_date)
    if df.empty:
        return df

    df = df.copy()
    if "datetime" in df.columns:
        df["date"] = pd.to_datetime(df["datetime"]).dt.strftime("%Y-%m-%d")
    if "amount" in df.columns and "money" not in df.columns:
        df["money"] = df["amount"]
    return df
