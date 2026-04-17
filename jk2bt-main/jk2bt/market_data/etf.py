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
    from ..db.parquet_adapter import ParquetAdapter
    from ..utils.standardize import standardize_ohlcv
    from ..data_access import get_adapter
except ImportError:
    from jk2bt.db.parquet_adapter import ParquetAdapter
    from jk2bt.utils.standardize import standardize_ohlcv
    from data_access import get_adapter

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
    db = ParquetAdapter()

    # 检查本地缓存
    if not force_update and db.has_data("etf_daily", symbol, start, end):
        df = db.get_etf_daily(symbol, start, end)
        if not df.empty:
            logger.info(f"{symbol}: 从 DuckDB 加载数据")
            return standardize_ohlcv(df)

    raw_df = get_adapter().get_etf_daily(
        symbol=symbol,
        start_date=start,
        end_date=end,
    )

    if raw_df is None or raw_df.empty:
        # 最后尝试本地缓存
        df = db.get_etf_daily(symbol, start, end)
        if not df.empty:
            logger.warning(f"{symbol}: 所有数据源失败，使用本地缓存")
            return standardize_ohlcv(df)
        raise ValueError(f"{symbol}: 所有数据源获取失败")

    # 存入本地数据库
    try:
        db.insert_etf_daily(symbol, raw_df)
    except Exception as e:
        logger.warning(f"{symbol}: 写入数据库失败: {e}")

    # 过滤日期范围
    if "datetime" in raw_df.columns:
        raw_df = raw_df[
            (raw_df["datetime"] >= pd.to_datetime(start))
            & (raw_df["datetime"] <= pd.to_datetime(end))
        ]

    return standardize_ohlcv(raw_df)
