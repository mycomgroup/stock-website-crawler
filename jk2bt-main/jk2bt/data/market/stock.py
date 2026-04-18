"""
market_data/stock.py
股票日线行情数据获取模块（使用 DuckDB 存储）。

支持多数据源备份:
1. 东方财富 (akshare.stock_zh_a_hist) - 主数据源
2. Tushare - 备用数据源1 (需要 Token)
3. Baostock - 备用数据源2 (免费)
4. Sina - 备用数据源3
5. 本地 DuckDB 缓存 - 最后备份

并发优化 (P2-7):
- 使用工厂函数获取单例管理器
- 读操作使用只读模式，避免锁冲突
- 写操作使用静默重试，减少噪音
"""

import logging
import pandas as pd
import time

try:
    from jk2bt.data.storage.parquet_adapter import (
        ParquetAdapter,
        get_shared_read_only_manager,
        get_writer_manager,
    )
    from jk2bt.utils.symbol import format_stock_symbol
    from jk2bt.utils.standardize import standardize_ohlcv
    from jk2bt.data.sources import get_adapter
except ImportError:
    from jk2bt.data.storage.parquet_adapter import (
        ParquetAdapter,
        get_shared_read_only_manager,
        get_writer_manager,
    )
    from jk2bt.utils.symbol import format_stock_symbol
    from jk2bt.utils.standardize import standardize_ohlcv
    from data_access import get_adapter

from jk2bt.data.market._common import _cached_daily_fetch

logger = logging.getLogger(__name__)


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

    并发优化 (P2-7):
    - 读操作使用只读单例管理器，避免锁冲突
    - 写操作使用写入管理器，静默重试
    """
    log_prefix = f"{symbol} ({adjust})"

    def _fetch():
        return get_adapter().get_daily_data(
            symbol=symbol,
            start_date=start,
            end_date=end,
            adjust=adjust,
        )

    def _insert(sym, df):
        db_write = get_writer_manager()
        db_write.insert_stock_daily(sym, df, adjust)

    return _cached_daily_fetch(
        table_name="stock_daily",
        symbol=symbol,
        start=start,
        end=end,
        fetch_fn=_fetch,
        insert_fn=_insert,
        normalize_fn=standardize_ohlcv,
        force_update=force_update,
        offline_mode=offline_mode,
        cache_key_extra=adjust,
        log_prefix=log_prefix,
    )


def get_stock_daily_fast(symbol, start, end, adjust="qfq"):
    """
    快速获取股票日线数据（仅使用本地缓存和东方财富）。

    适用于高频查询场景，跳过备用数据源。

    并发优化 (P2-7): 使用只读管理器进行读取
    """

    def _fetch():
        return get_adapter().get_daily_data(
            symbol=symbol,
            start_date=start,
            end_date=end,
            adjust=adjust,
        )

    def _insert(sym, df):
        db_write = get_writer_manager()
        db_write.insert_stock_daily(sym, df, adjust)

    return _cached_daily_fetch(
        table_name="stock_daily",
        symbol=symbol,
        start=start,
        end=end,
        fetch_fn=_fetch,
        insert_fn=_insert,
        normalize_fn=standardize_ohlcv,
        force_update=False,
        offline_mode=False,
        cache_key_extra=adjust,
        log_prefix=symbol,
    )


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

    并发优化 (P2-7): 使用只读管理器进行读取
    """
    db_read = get_shared_read_only_manager()

    if not force_update and db_read.has_data("stock_daily", symbol, start, end, adjust):
        df = db_read.get_stock_daily(symbol, start, end, adjust)
        if not df.empty:
            logger.debug(f"{symbol} ({adjust}): 从 DuckDB 加载数据")
            return standardize_ohlcv(df)

    if offline_mode:
        logger.debug(f"{symbol} ({adjust}): 离线模式，跳过下载")
        df = db_read.get_stock_daily(symbol, start, end, adjust)
        if not df.empty:
            logger.debug(f"{symbol} ({adjust}): 使用本地缓存数据")
            return standardize_ohlcv(df)
        else:
            raise ValueError(f"{symbol}: 离线模式下无缓存数据可用")

    logger.debug(f"{symbol} ({adjust}): 从 akshare 下载数据")

    try:
        from jk2bt.data.sources import get_adapter
    except ImportError:
        from data_access import get_adapter

    adapter = get_adapter()
    akshare_symbol = format_stock_symbol(symbol)

    raw_df = adapter.get_stock_hist(
        symbol=akshare_symbol,
        period="daily",
        start_date=start.replace("-", ""),
        end_date=end.replace("-", ""),
        adjust=adjust,
    )

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

    # 使用写入管理器
    db_write = get_writer_manager()
    db_write.insert_stock_daily(symbol, df, adjust)

    df = df[
        (df["datetime"] >= pd.to_datetime(start))
        & (df["datetime"] <= pd.to_datetime(end))
    ]

    return standardize_ohlcv(df)


def get_stock_price(
    securities,
    start_date=None,
    end_date=None,
    count=None,
    fields=None,
    adjust="qfq",
    panel=False,
    skip_paused=True,
):
    """
    获取股票价格数据（兼容聚宽 get_price 风格）。

    Parameters
    ----------
    securities : str or list
        股票代码或代码列表，如 'sh600000' 或 ['sh600000', 'sz000001']
    start_date : str, optional
        起始日期 'YYYY-MM-DD'
    end_date : str, optional
        结束日期 'YYYY-MM-DD'
    count : int, optional
        历史数据条数
    fields : list, optional
        字段列表，如 ['datetime', 'code', 'close', 'open', 'high', 'low', 'volume']
    adjust : str, default 'qfq'
        复权类型：qfq/hfq/none
    panel : bool, default False
        返回格式，False 时返回 DataFrame with datetime/code/close 等列
    skip_paused : bool, default True
        是否跳过停牌股票

    Returns
    -------
    pd.DataFrame (panel=False) or dict (panel=True)
        panel=False: DataFrame with datetime/code/close 等列
        panel=True: dict{symbol: DataFrame}
    """
    if isinstance(securities, str):
        securities = [securities]

    if count and not start_date:
        end_dt = pd.to_datetime(end_date) if end_date else pd.Timestamp.now()
        start_dt = end_dt - pd.Timedelta(days=count * 3)
        start_date = start_dt.strftime("%Y-%m-%d")
        if not end_date:
            end_date = end_dt.strftime("%Y-%m-%d")

    default_fields = ["datetime", "code", "close", "open", "high", "low", "volume"]
    if fields is None:
        fields = default_fields
    else:
        fields = ["datetime", "code"] + [
            f for f in fields if f not in ["datetime", "code"]
        ]

    result = {}
    for symbol in securities:
        df = get_stock_daily(
            symbol=symbol,
            start=start_date,
            end=end_date,
            adjust=adjust,
        )

        if df.empty:
            result[symbol] = pd.DataFrame()
            continue

        df = df.copy()
        if "datetime" not in df.columns and "date" in df.columns:
            df["datetime"] = df["date"]
        if "code" not in df.columns:
            df["code"] = symbol

        available_fields = [f for f in fields if f in df.columns]
        df = df[available_fields].copy()

        if skip_paused and "paused" in df.columns:
            df = df[df["paused"] == 0]

        if count:
            df = df.tail(count)

        result[symbol] = df.reset_index(drop=True)

    if len(result) == 1:
        return result[securities[0]]

    if panel:
        return result
    else:
        combined = []
        for sym, df in result.items():
            if not df.empty:
                df_copy = df.copy()
                combined.append(df_copy)
        if not combined:
            return pd.DataFrame()
        return pd.concat(combined, ignore_index=True)
