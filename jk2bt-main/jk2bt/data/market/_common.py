"""
market_data/_common.py
公共缓存-下载-标准化-回写流程抽象。

提供 _cached_daily_fetch() 函数，封装以下四步流程：
1. 检查 DuckDB/Parquet 缓存
2. 未命中则调用传入的 fetch 函数下载
3. 调用传入的 normalize 函数标准化列名
4. 写入缓存并返回结果

支持的变体：
- force_update / offline_mode
- fallback_to_cache（下载失败时尝试使用旧缓存）
- 可自定义的 cache_key_extra（如 adjust 参数）
"""

import logging
import pandas as pd
from typing import Callable, Optional

from jk2bt.data.storage.parquet_adapter import (
    get_shared_read_only_manager,
    get_writer_manager,
)
from jk2bt.utils.standardize import standardize_ohlcv

logger = logging.getLogger(__name__)


def _cached_daily_fetch(
    table_name: str,
    symbol: str,
    start: str,
    end: str,
    fetch_fn: Callable[[], pd.DataFrame],
    insert_fn: Callable[[str, pd.DataFrame], None],
    normalize_fn: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
    force_update: bool = False,
    offline_mode: bool = False,
    fallback_to_cache: bool = False,
    cache_key_extra: Optional[str] = None,
    log_prefix: Optional[str] = None,
) -> pd.DataFrame:
    """
    通用的缓存-下载-标准化-回写流程。

    参数
    ----
    table_name : str
        缓存表名，如 'stock_daily', 'etf_daily', 'index_daily'
    symbol : str
        标的代码
    start : str
        起始日期 'YYYY-MM-DD'
    end : str
        结束日期 'YYYY-MM-DD'
    fetch_fn : Callable[[], pd.DataFrame]
        无参函数，返回原始 DataFrame
    insert_fn : Callable[[str, pd.DataFrame], None]
        写入缓存的函数，接收 (symbol, df)
    normalize_fn : Callable[[pd.DataFrame], pd.DataFrame], optional
        标准化函数，默认使用 standardize_ohlcv
    force_update : bool
        强制从数据源重新下载
    offline_mode : bool
        离线模式，仅使用本地缓存
    fallback_to_cache : bool
        下载失败时尝试使用旧缓存（etf_daily 风格）
    cache_key_extra : str, optional
        缓存键的额外部分（如 adjust='qfq'）
    log_prefix : str, optional
        日志前缀，默认使用 symbol

    返回
    ----
    pd.DataFrame
        标准化后的 OHLCV 数据

    异常
    ----
    ValueError
        当 offline_mode 下无缓存，或所有数据源失败时
    """
    if normalize_fn is None:
        normalize_fn = standardize_ohlcv

    prefix = log_prefix or symbol

    # ---- Step 1: 检查缓存 ----
    db_read = get_shared_read_only_manager()

    has_cache = db_read.has_data(table_name, symbol, start, end, cache_key_extra)

    if not force_update and has_cache:
        df = _read_from_cache(db_read, table_name, symbol, start, end, cache_key_extra)
        if df is not None and not df.empty:
            logger.debug(f"{prefix}: 从缓存加载数据")
            return normalize_fn(df)

    # ---- Step 2: 离线模式 ----
    if offline_mode:
        df = _read_from_cache(db_read, table_name, symbol, start, end, cache_key_extra)
        if df is not None and not df.empty:
            logger.debug(f"{prefix}: 离线模式，使用本地缓存")
            return normalize_fn(df)
        raise ValueError(f"{prefix}: 离线模式下无缓存数据可用")

    # ---- Step 3: 下载 ----
    raw_df = None
    fetch_error = None

    try:
        raw_df = fetch_fn()
    except Exception as e:
        fetch_error = e

    # 下载失败处理
    if raw_df is None or raw_df.empty:
        if fallback_to_cache:
            df = _read_from_cache(
                db_read, table_name, symbol, start, end, cache_key_extra
            )
            if df is not None and not df.empty:
                logger.warning(f"{prefix}: 数据源失败，使用本地缓存")
                return normalize_fn(df)

        if fetch_error:
            raise ValueError(f"{prefix}: 所有数据源获取失败 - {fetch_error}")
        raise ValueError(f"{prefix}: 所有数据源获取失败")

    # ---- Step 4: 写入缓存 ----
    try:
        db_write = get_writer_manager()
        insert_fn(symbol, raw_df)
    except Exception as e:
        logger.debug(f"{prefix}: 写入缓存跳过: {e}")

    # 过滤日期范围并标准化
    if "datetime" in raw_df.columns:
        raw_df = raw_df[
            (raw_df["datetime"] >= pd.to_datetime(start))
            & (raw_df["datetime"] <= pd.to_datetime(end))
        ]

    return normalize_fn(raw_df)


def _read_from_cache(db_read, table_name, symbol, start, end, cache_key_extra=None):
    """从缓存读取数据的辅助函数，根据表名调用对应的 get 方法。"""
    try:
        if table_name == "stock_daily":
            return db_read.get_stock_daily(symbol, start, end, cache_key_extra or "qfq")
        elif table_name == "etf_daily":
            return db_read.get_etf_daily(symbol, start, end)
        elif table_name == "index_daily":
            return db_read.get_index_daily(symbol, start, end)
        elif table_name == "lof_daily":
            return db_read.get_lof_daily(symbol, start, end)
        else:
            logger.warning(f"未知表名: {table_name}")
            return pd.DataFrame()
    except Exception as e:
        logger.debug(f"缓存读取失败: {e}")
        return pd.DataFrame()
