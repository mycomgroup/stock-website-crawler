"""
market_data/minute.py
分钟级行情数据获取模块（使用 DuckDB 存储）。
支持股票和ETF的 1m/5m/15m/30m/60m 分钟数据。

统一标准化：
- 使用 utils/standardize.py 的标准函数
- 输出标准列：datetime/open/high/low/close/volume/money/openinterest

数据源备份:
- 东方财富 (主数据源)
- 本地 DuckDB 缓存 (备用，分钟数据难以获取其他备用源)
"""

import logging
import pandas as pd
from typing import Optional

try:
    from ..db.duckdb_manager import DuckDBManager
    from ..utils.symbol import format_stock_symbol
    from ..utils.standardize import (
        standardize_minute_ohlcv,
        normalize_columns,
        normalize_datetime,
        COLUMN_MAP_COMMON,
    )
    from ..utils.data_source_backup import (
        get_stock_minute_with_fallback,
        fetch_stock_minute_eastmoney,
    )
except ImportError:
    from jk2bt.db.duckdb_manager import DuckDBManager
    from utils.symbol import format_stock_symbol
    from utils.standardize import (
        standardize_minute_ohlcv,
        normalize_columns,
        normalize_datetime,
        COLUMN_MAP_COMMON,
    )
    from utils.data_source_backup import (
        get_stock_minute_with_fallback,
        fetch_stock_minute_eastmoney,
    )

logger = logging.getLogger(__name__)

PERIOD_MAP = {"1m": "1", "5m": "5", "15m": "15", "30m": "30", "60m": "60"}
VALID_PERIODS = ["1m", "5m", "15m", "30m", "60m"]


def _validate_period(period: str) -> str:
    """验证并标准化周期参数"""
    if period in VALID_PERIODS:
        return period
    period_lower = period.lower()
    if period_lower in VALID_PERIODS:
        return period_lower
    if period_lower == "minute":
        return "1m"
    raise ValueError(f"不支持的周期: {period}，支持的周期: {VALID_PERIODS}")


def get_stock_minute(
    symbol: str,
    start: str,
    end: str,
    period: str = "1m",
    adjust: str = "qfq",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取股票分钟行情数据，使用 DuckDB 存储。

    参数
    ----
    symbol : str
        股票代码，如 'sh600000'、'sz000001'
    start : str
        起始时间 'YYYY-MM-DD' 或 'YYYY-MM-DD HH:MM:SS'
    end : str
        结束时间 'YYYY-MM-DD' 或 'YYYY-MM-DD HH:MM:SS'
    period : str
        周期：1m/5m/15m/30m/60m
    adjust : str
        复权类型：qfq/hfq/none（分钟数据通常不复权，但保留接口）
    force_update : bool
        强制从 akshare 重新下载

    返回
    ----
    pd.DataFrame
        标准化后的分钟 OHLCV 数据，列：datetime/open/high/low/close/volume/money/openinterest
    """
    period = _validate_period(period)
    akshare_period = PERIOD_MAP[period]

    db_read = DuckDBManager(read_only=True)

    if not force_update:
        try:
            if db_read.has_data(
                "stock_minute", symbol, start, end, adjust, akshare_period
            ):
                df = db_read.get_stock_minute(
                    symbol, akshare_period, start, end, adjust
                )
                if not df.empty:
                    logger.info(f"{symbol} ({period}): 从 DuckDB 加载分钟数据")
                    return standardize_minute_ohlcv(df)
        except Exception as e:
            logger.warning(f"{symbol} ({period}): 只读查询失败，尝试写入模式: {e}")

    logger.info(f"{symbol} ({period}): 从 akshare 下载分钟数据")

    akshare_symbol = format_stock_symbol(symbol)

    try:
        import akshare as ak

        raw_df = ak.stock_zh_a_hist_min_em(
            symbol=akshare_symbol,
            period=akshare_period,
            start_date=start,
            end_date=end,
            adjust=adjust,
        )
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")
    except Exception as e:
        raise ValueError(f"{symbol} ({period}): akshare 获取分钟数据失败: {e}")

    if raw_df is None or raw_df.empty:
        raise ValueError(f"{symbol} ({period}): akshare 返回空数据")

    df = _prepare_for_storage(raw_df)

    try:
        db_write = DuckDBManager(read_only=False)
        db_write.insert_stock_minute(symbol, akshare_period, df, adjust)
    except Exception as e:
        logger.warning(
            f"{symbol} ({period}): 写入数据库失败（可能并发锁冲突），继续使用数据: {e}"
        )

    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    df = df[(df["datetime"] >= start_dt) & (df["datetime"] <= end_dt)]

    return standardize_minute_ohlcv(df)


def get_etf_minute(
    symbol: str,
    start: str,
    end: str,
    period: str = "1m",
    force_update: bool = False,
) -> pd.DataFrame:
    """
    获取 ETF 分钟行情数据，使用 DuckDB 存储。

    参数
    ----
    symbol : str
        ETF 代码，如 '510300'（不含交易所前缀）
    start : str
        起始时间 'YYYY-MM-DD' 或 'YYYY-MM-DD HH:MM:SS'
    end : str
        结束时间 'YYYY-MM-DD' 或 'YYYY-MM-DD HH:MM:SS'
    period : str
        周期：1m/5m/15m/30m/60m
    force_update : bool
        强制从 akshare 重新下载

    返回
    ----
    pd.DataFrame
        标准化后的分钟 OHLCV 数据，列：datetime/open/high/low/close/volume/money/openinterest
    """
    period = _validate_period(period)
    akshare_period = PERIOD_MAP[period]

    db_read = DuckDBManager(read_only=True)

    if not force_update:
        try:
            if db_read.has_data("etf_minute", symbol, start, end, None, akshare_period):
                df = db_read.get_etf_minute(symbol, akshare_period, start, end)
                if not df.empty:
                    logger.info(f"{symbol} ({period}): 从 DuckDB 加载分钟数据")
                    return standardize_minute_ohlcv(df)
        except Exception as e:
            logger.warning(f"{symbol} ({period}): 只读查询失败，尝试写入模式: {e}")

    logger.info(f"{symbol} ({period}): 从 akshare 下载分钟数据")

    try:
        import akshare as ak

        raw_df = ak.fund_etf_hist_min_em(
            symbol=symbol,
            period=akshare_period,
            start_date=start,
            end_date=end,
            adjust="qfq",
        )
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")
    except Exception as e:
        raise ValueError(f"{symbol} ({period}): akshare 获取分钟数据失败: {e}")

    if raw_df is None or raw_df.empty:
        raise ValueError(f"{symbol} ({period}): akshare 返回空数据")

    df = _prepare_for_storage(raw_df)

    try:
        db_write = DuckDBManager(read_only=False)
        db_write.insert_etf_minute(symbol, akshare_period, df)
    except Exception as e:
        logger.warning(
            f"{symbol} ({period}): 写入数据库失败（可能并发锁冲突），继续使用数据: {e}"
        )

    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    df = df[(df["datetime"] >= start_dt) & (df["datetime"] <= end_dt)]

    return standardize_minute_ohlcv(df)


def _prepare_for_storage(df: pd.DataFrame) -> pd.DataFrame:
    """
    为存储到 DuckDB 准备分钟数据。

    使用统一的标准化层处理：
    1. 列名映射（中文 -> 英文）
    2. 时间戳格式统一
    3. 数值类型转换

    返回
    ----
    pd.DataFrame
        包含 datetime/open/high/low/close/volume/money 列，适合存储到 DuckDB
    """
    df = normalize_columns(df, COLUMN_MAP_COMMON)
    df = normalize_datetime(df)

    if df.empty:
        raise ValueError("分钟数据缺少时间列或时间列全部无效")

    for col in ["open", "high", "low", "close", "volume", "money"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    required_cols = ["datetime", "open", "high", "low", "close"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"分钟数据缺少必要列: {missing}")

    select_cols = ["datetime", "open", "high", "low", "close", "volume"]
    if "money" in df.columns:
        select_cols.append("money")

    df = df[select_cols].copy()

    return df.sort_values("datetime").reset_index(drop=True)
