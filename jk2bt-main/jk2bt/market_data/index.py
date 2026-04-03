"""
market_data/index.py
指数日线行情数据获取模块（使用 DuckDB 存储）。
"""

import logging
import pandas as pd

try:
    from ..db.duckdb_manager import DuckDBManager
    from ..utils.standardize import standardize_ohlcv
except ImportError:
    from jk2bt.db.duckdb_manager import DuckDBManager
    from utils.standardize import standardize_ohlcv

logger = logging.getLogger(__name__)


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
    # 先尝试使用只读模式读取缓存数据（避免锁冲突）
    db_readonly = DuckDBManager(read_only=True)

    if not force_update:
        try:
            df = db_readonly.get_index_daily(symbol, start, end)
            if not df.empty:
                logger.info(f"{symbol}: 从 DuckDB 加载数据（只读模式）")
                return standardize_ohlcv(df)
        except Exception as e:
            logger.warning(f"{symbol}: 只读模式读取失败: {e}")

    # 需要写入数据时才使用写模式
    db = DuckDBManager()

    if not force_update and db.has_data("index_daily", symbol, start, end):
        df = db.get_index_daily(symbol, start, end)
        if not df.empty:
            logger.info(f"{symbol}: 从 DuckDB 加载数据")
            return standardize_ohlcv(df)

    logger.info(f"{symbol}: 从 akshare 下载数据")

    from akshare import index_zh_a_hist

    raw_df = index_zh_a_hist(symbol=symbol, period="daily")

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

    db.insert_index_daily(symbol, df)

    df = df[
        (df["datetime"] >= pd.to_datetime(start))
        & (df["datetime"] <= pd.to_datetime(end))
    ]

    return standardize_ohlcv(df)
