"""
utils/date_utils.py
日期和交易日工具（统一实现）。

主要功能:
1. 交易日查询 - get_all_trade_days, get_trade_days
2. 日期检测 - find_date_column
3. 日期转换 - 各种日期格式转换

依赖:
- DuckDB 缓存（优先）- 延迟导入，避免循环依赖
- AkShare 作为 fallback - 延迟导入

注意: 为避免循环依赖，data.storage 和 data.sources 的导入在函数内部延迟执行。
"""

import os
import pandas as pd
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

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
        "REPORT_DATE",
    ],
    "valuation": [
        "日期",
        "date",
        "REPORT_DATE",
        "NOTICE_DATE",
        "trade_date",
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


def get_all_trade_days(use_duckdb=True):
    """
    获取所有交易日列表（聚宽风格）。

    返回 pd.DatetimeIndex 或 Timestamp 列表。

    参数:
        use_duckdb: 是否优先使用 DuckDB 缓存

    返回:
        pd.DatetimeIndex 或 list: 交易日列表

    示例:
        days = get_all_trade_days()
        len(days)  # 约 8000+ 个交易日
    """
    # 优先使用 DuckDB 缓存（延迟导入避免循环依赖）
    if use_duckdb:
        try:
            from jk2bt.data.storage.meta_cache_api import get_trade_days_from_cache

            days = get_trade_days_from_cache(use_duckdb=True)
            if days:
                if isinstance(days, list):
                    return pd.DatetimeIndex(days)
                return days
        except ImportError:
            logger.debug("DuckDB meta_cache_api 不可用，使用 adapter fallback")
        except Exception as e:
            logger.warning(f"DuckDB 缓存获取失败，fallback 到 adapter: {e}")

    # 通过适配器获取
    try:
        from jk2bt.data.sources import get_adapter

        df = get_adapter().get_trade_dates()
        return pd.DatetimeIndex(pd.to_datetime(df["trade_date"]).tolist())
    except Exception as e:
        logger.error(f"获取交易日失败: {e}")

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
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
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


# 兼容别名：聚宽风格接口返回 list
def get_all_trade_days_jq(use_duckdb=True):
    days = get_all_trade_days(
        use_duckdb=use_duckdb,
    )
    if days is None:
        return []
    if isinstance(days, list):
        return days
    if isinstance(days, pd.DatetimeIndex):
        return days.tolist()
    try:
        return list(days)
    except TypeError:
        return [days]


get_trading_days = get_all_trade_days  # 常用别名


def parse_date(date_str, as_datetime: bool = False) -> Optional:
    """统一日期解析函数，支持多种格式

    Parameters
    ----------
    date_str : 日期字符串
    as_datetime : 是否返回 datetime 对象，默认 False 返回 '%Y-%m-%d' 字符串

    Returns
    -------
    str 或 datetime 或 None
    """
    if not date_str or pd.isna(date_str):
        return None
    date_str = str(date_str).strip()
    for fmt in ["%Y-%m-%d", "%Y%m%d", "%Y/%m/%d", "%Y年%m月", "%Y年%m月%d日"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            if as_datetime:
                return dt
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    # Fallback: 尝试解析纯数字格式 (如 202301)
    if len(date_str) >= 6:
        try:
            year = int(date_str[:4])
            month = int(date_str[4:6])
            dt = datetime(year, month, 1)
            if as_datetime:
                return dt
            return dt.strftime("%Y-%m-%d")
        except Exception:
            pass
    return None


def filter_by_date_range(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date_col: str = "datetime",
) -> pd.DataFrame:
    """统一日期范围过滤"""
    if start_date is None and end_date is None:
        return df
    result = df.copy()
    if date_col not in result.columns:
        return result
    result = result.copy()
    result["_filter_date"] = pd.to_datetime(result[date_col], errors="coerce")
    if start_date:
        result = result[result["_filter_date"] >= pd.to_datetime(start_date)]
    if end_date:
        result = result[result["_filter_date"] <= pd.to_datetime(end_date)]
    return result.drop(columns=["_filter_date"])


def standardize_datetime(df: pd.DataFrame, date_col: str = "datetime") -> pd.DataFrame:
    """标准化DataFrame中的日期列"""
    result = df.copy()
    if date_col not in result.columns:
        return result
    result[date_col] = pd.to_datetime(result[date_col], errors="coerce")
    result = result.dropna(subset=[date_col])
    return result.sort_values(date_col).reset_index(drop=True)


def parse_ratio(value) -> Optional[float]:
    """统一百分比解析函数"""
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace("%", "").replace(",", "").strip()
            if not value:
                return None
            return float(value) / 100 if float(value) > 1 else float(value)
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_num(value) -> Optional[float]:
    """统一数值解析函数（返回 float）"""
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace(",", "").replace("%", "").strip()
            if not value:
                return None
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_int(value) -> Optional[int]:
    """统一整数解析函数"""
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace(",", "").strip()
            if not value:
                return None
        return int(float(value))
    except (ValueError, TypeError):
        return None


__all__ = [
    "find_date_column",
    "get_all_trade_days",
    "get_all_trade_days_jq",  # 兼容别名
    "get_trading_days",  # 常用别名
    "get_trade_days",
    "is_trade_date",
    "get_previous_trade_date",
    "get_next_trade_date",
    "count_trade_days_between",
    "parse_date",
    "filter_by_date_range",
    "standardize_datetime",
    "parse_ratio",
    "parse_num",
    "parse_int",
]
