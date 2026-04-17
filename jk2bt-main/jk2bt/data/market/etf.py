"""
market_data/etf.py
ETF 日线行情数据获取模块（使用 DuckDB 存储）。

支持多数据源备份:
1. 东方财富 (akshare.fund_etf_hist_em) - 主数据源
2. Tushare - 备用数据源 (需要 Token)
3. 本地 DuckDB 缓存 - 最后备份
"""

import logging
import pandas as pd

try:
    from jk2bt.data.storage.parquet_adapter import (
        ParquetAdapter,
        get_writer_manager,
    )
    from jk2bt.utils.standardize import standardize_ohlcv
    from jk2bt.data.sources import get_adapter
except ImportError:
    from jk2bt.data.storage.parquet_adapter import (
        ParquetAdapter,
        get_writer_manager,
    )
    from jk2bt.utils.standardize import standardize_ohlcv
    from data_access import get_adapter

from jk2bt.data.market._common import _cached_daily_fetch

logger = logging.getLogger(__name__)


def get_etf_daily(symbol, start, end, force_update=False, data_sources=None):
    """
    获取 ETF 日线行情数据，使用 DuckDB 存储和多数据源备份。

    参数
    ----
    symbol : str
        ETF 代码，如 '510300'（不含交易所前缀）
    start : str
        资始日期 'YYYY-MM-DD'
    end : str
        结束日期 'YYYY-MM-DD'
    force_update : bool
        强制从数据源重新下载
    data_sources : list
        数据源优先级列表，默认 ["east_money", "tushare"]

    返回
    ----
    pd.DataFrame
        标准化后的 OHLCV 数据
    """

    def _fetch():
        return get_adapter().get_etf_daily(
            symbol=symbol,
            start_date=start,
            end_date=end,
        )

    def _insert(sym, df):
        db_write = get_writer_manager()
        db_write.insert_etf_daily(sym, df)

    return _cached_daily_fetch(
        table_name="etf_daily",
        symbol=symbol,
        start=start,
        end=end,
        fetch_fn=_fetch,
        insert_fn=_insert,
        normalize_fn=standardize_ohlcv,
        force_update=force_update,
        offline_mode=False,
        fallback_to_cache=True,
        log_prefix=symbol,
    )
