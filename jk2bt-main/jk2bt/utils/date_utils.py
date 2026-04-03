"""
utils/date_utils.py
日期和交易日工具（统一实现）。

主要功能:
1. 交易日查询 - get_all_trade_days, get_trade_days
2. 日期检测 - find_date_column
3. 日期转换 - 各种日期格式转换

依赖:
- DuckDB 缓存（优先）
- AkShare 作为 fallback
"""

import os
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# DuckDB 可用性检测
_DUCKDB_AVAILABLE = False
try:
    from ..db.meta_cache_api import get_trade_days_from_cache
    _DUCKDB_AVAILABLE = True
except ImportError:
    try:
        from jk2bt.db.meta_cache_api import get_trade_days_from_cache
        _DUCKDB_AVAILABLE = True
    except ImportError:
        logger.warning("DuckDB meta_cache_api 不可用，将使用 pickle 缓存")


_DATE_COLUMN_CANDIDATES = {
    "market": ["日期", "date", "trade_date", "trading_date"],
    "financial": [
        "报告期",
        "报告日期",
        "报告日",
        "报表日期",
        "STATEMENT_DATE",
        "date",
        "report_date",
    ],
}


def find_date_column(df: pd.DataFrame, category: str = "market") -> str:
    """动态检测 DataFrame 中的日期列名。

    Parameters
    ----------
    df : pd.DataFrame
    category : str, 'market' 或 'financial'

    Returns
    -------
    str : 日期列名，若找不到则返回 None
    """
    candidates = _DATE_COLUMN_CANDIDATES.get(
        category, _DATE_COLUMN_CANDIDATES["market"]
    )
    for col in candidates:
        if col in df.columns:
            return col
    return None


def get_all_trade_days(cache_dir="meta_cache", force_update=False, use_duckdb=True):
    """
    获取所有交易日列表（聚宽风格）。

    返回 pd.DatetimeIndex 或 Timestamp 列表。

    参数:
        cache_dir: pickle 缓存目录（作为 fallback）
        force_update: 是否强制更新
        use_duckdb: 是否优先使用 DuckDB 缓存

    返回:
        pd.DatetimeIndex 或 list: 交易日列表

    示例:
        days = get_all_trade_days()
        len(days)  # 约 8000+ 个交易日
    """
    # 优先使用 DuckDB 缓存
    if use_duckdb and _DUCKDB_AVAILABLE:
        try:
            days = get_trade_days_from_cache(force_update=force_update, use_duckdb=True)
            if days:
                if isinstance(days, list):
                    return pd.DatetimeIndex(days)
                return days
        except Exception as e:
            logger.warning(f"DuckDB 缓存获取失败，fallback 到 pickle: {e}")

    # Fallback: 使用 pickle 缓存
    cache_dir = _resolve_cache_dir(cache_dir)
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "trade_days.pkl")

    need_dl = force_update or not os.path.exists(cache_file)

    if not need_dl:
        try:
            df = pd.read_pickle(cache_file)
            return pd.DatetimeIndex(pd.to_datetime(df["trade_date"]).tolist())
        except Exception:
            need_dl = True

    # 从 AkShare 下载（延迟导入）
    try:
        import akshare as ak
    except ImportError:
        logger.warning("请安装 akshare: pip install akshare")
        return pd.DatetimeIndex([])

    try:
        df = ak.tool_trade_date_hist_sina()
        df.to_pickle(cache_file)
        return pd.DatetimeIndex(pd.to_datetime(df["trade_date"]).tolist())
    except Exception as e:
        logger.error(f"AkShare 获取交易日失败: {e}")

    # 最后 fallback: 返回空列表
    logger.warning("无法获取交易日数据，返回空列表")
    return pd.DatetimeIndex([])


def get_trade_days(start_date=None, end_date=None, count=None):
    """
    获取指定日期范围内的交易日列表（JoinQuant API 风格）。

    参数:
        start_date: 开始日期，字符串格式 'YYYY-MM-DD' 或 datetime
        end_date: 结束日期，字符串格式 'YYYY-MM-DD' 或 datetime
        count: 返回最近 count 个交易日（如果指定，则从 end_date 往前数）

    返回:
        pd.DatetimeIndex: 交易日列表

    注意:
        - 如果只指定 count，则返回最近 count 个交易日
        - 如果指定 start_date 和 end_date，则返回该范围内的交易日

    示例:
        # 获取最近 10 个交易日
        days = get_trade_days(count=10)

        # 获取 2023 年全年交易日
        days = get_trade_days(start_date='2023-01-01', end_date='2023-12-31')
    """
    # 获取所有交易日
    all_days = get_all_trade_days()

    if all_days is None or len(all_days) == 0:
        # Fallback to business days
        if start_date and end_date:
            dates = pd.date_range(start=start_date, end=end_date, freq="B")
            return pd.DatetimeIndex(dates)
        return pd.DatetimeIndex([])

    # Convert to DatetimeIndex if needed
    if not isinstance(all_days, pd.DatetimeIndex):
        if hasattr(all_days[0], "strftime"):
            all_days = pd.DatetimeIndex(all_days)
        else:
            all_days = pd.DatetimeIndex([pd.to_datetime(d) for d in all_days])

    # Handle count parameter
    if count is not None and end_date is not None:
        end_dt = pd.to_datetime(end_date)
        filtered = all_days[all_days <= end_dt]
        if len(filtered) >= count:
            return filtered[-count:]
        return filtered

    if count is not None and start_date is None and end_date is None:
        # Return last count trading days
        if len(all_days) >= count:
            return all_days[-count:]
        return all_days

    # Filter by date range
    if start_date is not None:
        start_dt = pd.to_datetime(start_date)
        all_days = all_days[all_days >= start_dt]

    if end_date is not None:
        end_dt = pd.to_datetime(end_date)
        all_days = all_days[all_days <= end_dt]

    return all_days


def _resolve_cache_dir(cache_dir):
    """解析缓存目录路径"""
    if os.path.isabs(cache_dir):
        return cache_dir

    # 相对路径转为绝对路径
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, cache_dir)


def is_trade_date(date):
    """
    判断是否为交易日。

    参数:
        date: 日期，字符串或 datetime

    返回:
        bool: 是否为交易日

    示例:
        is_trade_date('2023-01-03')  # True (周二)
        is_trade_date('2023-01-01')  # False (元旦)
    """
    all_days = get_all_trade_days()
    dt = pd.to_datetime(date)
    return dt in all_days


def get_previous_trade_date(date, n=1):
    """
    获取前 n 个交易日。

    参数:
        date: 参考日期
        n: 往前数 n 个交易日

    返回:
        datetime: 前第 n 个交易日

    示例:
        get_previous_trade_date('2023-01-10', n=1)  # 2023-01-09
    """
    all_days = get_all_trade_days()
    dt = pd.to_datetime(date)

    # 找到当前日期或之前的最近交易日
    before = all_days[all_days <= dt]

    if len(before) < n:
        return None

    return before[-n]


def get_next_trade_date(date, n=1):
    """
    获取后 n 个交易日。

    参数:
        date: 参考日期
        n: 往后数 n 个交易日

    返回:
        datetime: 后第 n 个交易日

    示例:
        get_next_trade_date('2023-01-09', n=1)  # 2023-01-10
    """
    all_days = get_all_trade_days()
    dt = pd.to_datetime(date)

    # 找到当前日期或之后的最近交易日
    after = all_days[all_days >= dt]

    if len(after) < n:
        return None

    return after[n - 1]


def count_trade_days_between(start_date, end_date):
    """
    计算两个日期之间的交易日数量。

    参数:
        start_date: 开始日期
        end_date: 结束日期

    返回:
        int: 交易日数量

    示例:
        count_trade_days_between('2023-01-01', '2023-01-31')  # 约 20 天
    """
    days = get_trade_days(start_date, end_date)
    return len(days)


# 兼容别名
get_all_trade_days_jq = get_all_trade_days
get_trading_days = get_all_trade_days  # 常用别名


__all__ = [
    'find_date_column',
    'get_all_trade_days',
    'get_all_trade_days_jq',  # 兼容别名
    'get_trading_days',  # 常用别名
    'get_trade_days',
    'is_trade_date',
    'get_previous_trade_date',
    'get_next_trade_date',
    'count_trade_days_between',
]