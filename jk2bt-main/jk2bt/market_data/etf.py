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
    from ..db.duckdb_manager import DuckDBManager
    from ..utils.standardize import standardize_ohlcv
    from ..utils.data_source_backup import (
        get_etf_daily_with_fallback,
        fetch_etf_daily_eastmoney,
        set_tushare_token,
    )
except ImportError:
    from jk2bt.db.duckdb_manager import DuckDBManager
    from jk2bt.utils.standardize import standardize_ohlcv
    from jk2bt.utils.data_source_backup import (
        get_etf_daily_with_fallback,
        fetch_etf_daily_eastmoney,
        set_tushare_token,
    )

logger = logging.getLogger(__name__)

# ETF 数据源优先级 (Sina 优先)
DEFAULT_DATA_SOURCES = ["sina", "east_money", "tushare"]


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
    db = DuckDBManager()

    # 检查本地缓存
    if not force_update and db.has_data("etf_daily", symbol, start, end):
        df = db.get_etf_daily(symbol, start, end)
        if not df.empty:
            logger.info(f"{symbol}: 从 DuckDB 加载数据")
            return standardize_ohlcv(df)

    # 使用多数据源备份系统
    sources = data_sources or DEFAULT_DATA_SOURCES

    def cache_getter(sym, s, e):
        try:
            return db.get_etf_daily(sym, s, e)
        except Exception:
            return pd.DataFrame()

    raw_df = get_etf_daily_with_fallback(
        symbol=symbol,
        start=start,
        end=end,
        sources=sources,
        fallback_to_cache=True,
        cache_getter=cache_getter,
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


def get_etf_daily_legacy(symbol, start, end, force_update=False):
    """
    旧版获取函数（仅使用 akshare），保留兼容性。
    """
    db = DuckDBManager()

    if not force_update and db.has_data("etf_daily", symbol, start, end):
        df = db.get_etf_daily(symbol, start, end)
        if not df.empty:
            logger.info(f"{symbol}: 从 DuckDB 加载数据")
            return standardize_ohlcv(df)

    logger.info(f"{symbol}: 从 akshare 下载数据")

    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    raw_df = ak.fund_etf_hist_em(symbol=symbol)

    if raw_df is None or raw_df.empty:
        raise ValueError(f"{symbol}: akshare 返回空数据")

    df = raw_df.copy()
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

    select_cols = ["datetime", "open", "high", "low", "close", "volume"]
    if "amount" in df.columns:
        select_cols.append("amount")

    df = df[select_cols].copy()

    db.insert_etf_daily(symbol, df)

    df = df[
        (df["datetime"] >= pd.to_datetime(start))
        & (df["datetime"] <= pd.to_datetime(end))
    ]

    return standardize_ohlcv(df)