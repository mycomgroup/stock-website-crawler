"""
market_data/index.py
指数日线行情数据获取模块（使用 DuckDB 存储）。
"""

import logging
import pandas as pd

try:
    from jk2bt.data.storage.parquet_adapter import (
        ParquetAdapter,
        get_writer_manager,
    )
    from jk2bt.utils.standardize import standardize_ohlcv
except ImportError:
    from jk2bt.data.storage.parquet_adapter import (
        ParquetAdapter,
        get_writer_manager,
    )
    from jk2bt.utils.standardize import standardize_ohlcv

from jk2bt.data.market._common import _cached_daily_fetch

logger = logging.getLogger(__name__)


def _normalize_index(df: pd.DataFrame) -> pd.DataFrame:
    """指数数据列名标准化。"""
    df = df.copy()
    columns_map = {
        "日期": "datetime",
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
        "成交额": "amount",
    }
    for old_col, new_col in columns_map.items():
        if old_col in df.columns:
            df[new_col] = df[old_col]
    df["datetime"] = pd.to_datetime(df["datetime"])
    return standardize_ohlcv(df)


def get_index_daily(symbol, start, end, force_update=False):
    """
    获取指数日线行情数据，使用 DuckDB 存储。

    参数
    ----
    symbol : str
        指数代码，如 '000300'、'000905'
    start : str
        起始日期 'YYYY-MM-DD'
    end : str
        结束日期 'YYYY-MM-DD'
    force_update : bool
        强制从 akshare 重新下载

    返回
    ----
    pd.DataFrame
        标准化后的 OHLCV 数据
    """

    def _fetch():
        try:
            from jk2bt.data.sources import get_adapter
        except ImportError:
            from data_access import get_adapter

        adapter = get_adapter()
        return adapter.get_index_zh_a_hist(symbol=symbol, period="daily")

    def _insert(sym, df):
        db_write = get_writer_manager()
        db_write.insert_index_daily(sym, df)

    return _cached_daily_fetch(
        table_name="index_daily",
        symbol=symbol,
        start=start,
        end=end,
        fetch_fn=_fetch,
        insert_fn=_insert,
        normalize_fn=_normalize_index,
        force_update=force_update,
        offline_mode=False,
        log_prefix=symbol,
    )
