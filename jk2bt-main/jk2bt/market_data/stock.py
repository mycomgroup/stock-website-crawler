"""
market_data/stock.py
股票日线行情数据获取模块（使用 DuckDB 存储）。

支持多数据源备份:
1. 东方财富 (akshare.stock_zh_a_hist) - 主数据源
2. Tushare - 备用数据源1 (需要 Token)
3. Baostock - 备用数据源2 (免费)
4. Sina - 备用数据源3
5. 本地 DuckDB 缓存 - 最后备份
"""

import logging
import pandas as pd
import time

try:
    from ..db.duckdb_manager import DuckDBManager
    from ..utils.symbol import format_stock_symbol
    from ..utils.standardize import standardize_ohlcv
    from ..utils.data_source_backup import (
        get_stock_daily_with_fallback,
        fetch_stock_daily_eastmoney,
        fetch_stock_daily_tushare,
        fetch_stock_daily_baostock,
        fetch_stock_daily_sina,
        set_tushare_token,
    )
except ImportError:
    from jk2bt.db.duckdb_manager import DuckDBManager
    from utils.symbol import format_stock_symbol
    from utils.standardize import standardize_ohlcv
    from utils.data_source_backup import (
        get_stock_daily_with_fallback,
        fetch_stock_daily_eastmoney,
        fetch_stock_daily_tushare,
        fetch_stock_daily_baostock,
        fetch_stock_daily_sina,
        set_tushare_token,
    )

logger = logging.getLogger(__name__)

# 数据源优先级配置 (Sina 优先)
DEFAULT_DATA_SOURCES = ["sina", "east_money", "tushare", "baostock"]


def get_stock_daily(
    symbol,
    start,
    end,
    force_update=False,
    adjust="qfq",
    offline_mode=False,
    max_retries=3,
    retry_delay=2,
    data_sources=None,
):
    """
    获取股票日线行情数据，使用 DuckDB 存储和多数据源备份。

    参数
    ----
    symbol : str
        股票代码，如 'sh600000'、'sz000001'
    start : str
        资始日期 'YYYY-MM-DD'
    end : str
        结束日期 'YYYY-MM-DD'
    force_update : bool
        强制从数据源重新下载
    adjust : str
        复权类型：qfq/hfq/none
    offline_mode : bool
        离线模式，仅使用本地缓存数据，不尝试下载
    max_retries : int
        最大重试次数（下载失败时）
    retry_delay : int
        重试间隔（秒）
    data_sources : list
        数据源优先级列表，默认 ["east_money", "tushare", "baostock", "sina"]

    返回
    ----
    pd.DataFrame
        标准化后的 OHLCV 数据

    数据源说明
    ----------
    1. east_money: 东方财富 (akshare.stock_zh_a_hist) - 主数据源
    2. tushare: Tushare Pro (需要 Token) - 备用数据源1
    3. baostock: Baostock (免费，无需注册) - 备用数据源2
    4. sina: 新浪财经 - 备用数据源3
    5. local: 本地 DuckDB 缓存 - 最后备份
    """
    db = DuckDBManager()

    # 检查本地缓存
    if not force_update and db.has_data("stock_daily", symbol, start, end, adjust):
        df = db.get_stock_daily(symbol, start, end, adjust)
        if not df.empty:
            logger.info(f"{symbol} ({adjust}): 从 DuckDB 加载数据")
            return standardize_ohlcv(df)

    # 离线模式
    if offline_mode:
        logger.warning(f"{symbol} ({adjust}): 离线模式，跳过下载")
        df = db.get_stock_daily(symbol, start, end, adjust)
        if not df.empty:
            logger.info(f"{symbol} ({adjust}): 使用本地缓存数据")
            return standardize_ohlcv(df)
        else:
            raise ValueError(f"{symbol}: 离线模式下无缓存数据可用")

    # 使用多数据源备份系统
    sources = data_sources or DEFAULT_DATA_SOURCES

    def cache_getter(sym, s, e, adj):
        try:
            return db.get_stock_daily(sym, s, e, adj)
        except Exception:
            return pd.DataFrame()

    raw_df = get_stock_daily_with_fallback(
        symbol=symbol,
        start=start,
        end=end,
        adjust=adjust,
        sources=sources,
        fallback_to_cache=True,
        cache_getter=cache_getter,
    )

    if raw_df is None or raw_df.empty:
        # 最后尝试本地缓存
        df = db.get_stock_daily(symbol, start, end, adjust)
        if not df.empty:
            logger.warning(f"{symbol}: 所有数据源失败，使用本地缓存")
            return standardize_ohlcv(df)
        raise ValueError(f"{symbol}: 所有数据源获取失败")

    # 存入本地数据库
    try:
        db.insert_stock_daily(symbol, raw_df, adjust)
    except Exception as e:
        logger.warning(f"{symbol}: 写入数据库失败（可能并发锁冲突）: {e}")

    # 过滤日期范围
    if "datetime" in raw_df.columns:
        raw_df = raw_df[
            (raw_df["datetime"] >= pd.to_datetime(start))
            & (raw_df["datetime"] <= pd.to_datetime(end))
        ]

    return standardize_ohlcv(raw_df)


def get_stock_daily_fast(symbol, start, end, adjust="qfq"):
    """
    快速获取股票日线数据（仅使用本地缓存和东方财富）。

    适用于高频查询场景，跳过备用数据源。
    """
    db = DuckDBManager()

    # 仅检查缓存
    if db.has_data("stock_daily", symbol, start, end, adjust):
        df = db.get_stock_daily(symbol, start, end, adjust)
        if not df.empty:
            return standardize_ohlcv(df)

    # 直接从东方财富获取
    raw_df = fetch_stock_daily_eastmoney(symbol, start, end, adjust)
    if raw_df is not None and not raw_df.empty:
        try:
            db.insert_stock_daily(symbol, raw_df, adjust)
        except Exception:
            pass
        return standardize_ohlcv(raw_df)

    raise ValueError(f"{symbol}: 快速获取失败")


def get_stock_daily_legacy(
    symbol,
    start,
    end,
    force_update=False,
    adjust="qfq",
    offline_mode=False,
    max_retries=3,
    retry_delay=2,
):
    """
    旧版获取函数（仅使用 akshare），保留兼容性。
    """
    db = DuckDBManager()

    if not force_update and db.has_data("stock_daily", symbol, start, end, adjust):
        df = db.get_stock_daily(symbol, start, end, adjust)
        if not df.empty:
            logger.info(f"{symbol} ({adjust}): 从 DuckDB 加载数据")
            return standardize_ohlcv(df)

    if offline_mode:
        logger.warning(f"{symbol} ({adjust}): 离线模式，跳过下载")
        df = db.get_stock_daily(symbol, start, end, adjust)
        if not df.empty:
            logger.info(f"{symbol} ({adjust}): 使用本地缓存数据")
            return standardize_ohlcv(df)
        else:
            raise ValueError(f"{symbol}: 离线模式下无缓存数据可用")

    logger.info(f"{symbol} ({adjust}): 从 akshare 下载数据")

    akshare_symbol = format_stock_symbol(symbol)

    from akshare import stock_zh_a_hist

    last_error = None
    for attempt in range(max_retries):
        try:
            raw_df = stock_zh_a_hist(
                symbol=akshare_symbol,
                period="daily",
                start_date=start.replace("-", ""),
                end_date=end.replace("-", ""),
                adjust=adjust,
            )

            if raw_df is not None and not raw_df.empty:
                break
            else:
                raise ValueError(f"{symbol}: akshare 返回空数据")

        except Exception as e:
            last_error = e
            logger.warning(
                f"{symbol}: 下载失败 (尝试 {attempt + 1}/{max_retries}): {e}"
            )
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

                df = db.get_stock_daily(symbol, start, end, adjust)
                if not df.empty:
                    logger.info(f"{symbol} ({adjust}): 下载失败，回退到本地缓存")
                    return standardize_ohlcv(df)
            else:
                df = db.get_stock_daily(symbol, start, end, adjust)
                if not df.empty:
                    logger.warning(f"{symbol}: 所有重试失败，使用本地缓存数据")
                    return standardize_ohlcv(df)
                else:
                    logger.error(f"{symbol}: 下载失败且无本地缓存")
                    raise ValueError(f"{symbol}: 数据获取失败 - {last_error}")

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

    db.insert_stock_daily(symbol, df, adjust)

    df = df[
        (df["datetime"] >= pd.to_datetime(start))
        & (df["datetime"] <= pd.to_datetime(end))
    ]

    return standardize_ohlcv(df)