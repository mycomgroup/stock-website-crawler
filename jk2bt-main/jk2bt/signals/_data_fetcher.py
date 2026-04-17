"""
signals/_data_fetcher.py
Shared OHLCV data fetching helper for signal detection modules.
"""

from typing import Optional
import pandas as pd


def _fetch_ohlcv(symbol: str, end_date: Optional[str], count: int) -> pd.DataFrame:
    """通过 adapter 获取日线数据，返回带 date 列的 DataFrame"""
    from jk2bt.data_access import get_adapter

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
