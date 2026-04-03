"""
日期工具API模块
提供日期偏移、交易日计算、日期格式转换等功能
"""

import datetime
from datetime import date, datetime as dt, timedelta
from typing import Union, Literal
import pandas as pd

try:
    from jk2bt.core.strategy_base import get_all_trade_days_jq
except ImportError:
    from ..core.strategy_base import get_all_trade_days_jq


def _get_trade_days_list() -> list:
    """获取所有交易日列表（内部使用）

    Returns:
        list: datetime.date 对象列表（按时间升序排列）
    """
    all_days = get_all_trade_days_jq()
    if all_days is None or len(all_days) == 0:
        return []

    # 转换为 date 对象列表
    trade_days = []
    for d in all_days:
        if isinstance(d, pd.Timestamp):
            trade_days.append(d.date())
        elif isinstance(d, dt):
            trade_days.append(d.date())
        elif isinstance(d, date):
            trade_days.append(d)
        else:
            try:
                trade_days.append(pd.to_datetime(d).date())
            except Exception:
                continue

    # 按时间升序排列
    trade_days.sort()
    return trade_days


# 缓存交易日列表以提高性能
_trade_days_cache = None


def _get_cached_trade_days() -> list:
    """获取缓存的交易日列表"""
    global _trade_days_cache
    if _trade_days_cache is None:
        _trade_days_cache = _get_trade_days_list()
    return _trade_days_cache


def clear_trade_days_cache():
    """清除交易日缓存（用于强制刷新数据）"""
    global _trade_days_cache
    _trade_days_cache = None


def transform_date(
    date_input: Union[str, date, dt, pd.Timestamp],
    output_type: Literal['date', 'datetime', 'str', 'timestamp'] = 'date'
) -> Union[date, dt, str, pd.Timestamp]:
    """
    日期格式转换

    支持多种输入格式并转换为指定输出格式。

    Args:
        date_input: 输入日期，支持以下格式:
            - 字符串: 'YYYY-MM-DD', 'YYYYMMDD', 'YYYY/MM/DD'
            - datetime.date 对象
            - datetime.datetime 对象
            - pandas.Timestamp 对象
        output_type: 输出类型，可选:
            - 'date': datetime.date 对象
            - 'datetime': datetime.datetime 对象
            - 'str': 字符串格式 'YYYY-MM-DD'
            - 'timestamp': pandas.Timestamp 对象

    Returns:
        转换后的日期对象

    Raises:
        ValueError: 输入日期格式无效

    Examples:
        >>> transform_date('2023-01-01', 'date')
        datetime.date(2023, 1, 1)
        >>> transform_date(datetime.date(2023, 1, 1), 'str')
        '2023-01-01'
        >>> transform_date('20230101', 'datetime')
        datetime.datetime(2023, 1, 1, 0, 0)
    """
    # 首先将输入转换为 datetime.date 对象
    result_date = None

    if isinstance(date_input, date) and not isinstance(date_input, dt):
        # 已经是 date 对象
        result_date = date_input
    elif isinstance(date_input, dt):
        # datetime 对象
        result_date = date_input.date()
    elif isinstance(date_input, pd.Timestamp):
        # pandas Timestamp 对象
        result_date = date_input.date()
    elif isinstance(date_input, str):
        # 字符串格式
        date_str = date_input.strip()
        try:
            # 尝试多种常见格式
            if '-' in date_str:
                result_date = dt.strptime(date_str, '%Y-%m-%d').date()
            elif '/' in date_str:
                result_date = dt.strptime(date_str, '%Y/%m/%d').date()
            elif len(date_str) == 8:
                result_date = dt.strptime(date_str, '%Y%m%d').date()
            else:
                # 尝试 pandas 的灵活解析
                result_date = pd.to_datetime(date_str).date()
        except ValueError as e:
            raise ValueError(f"无法解析日期字符串: '{date_input}'") from e
    else:
        raise ValueError(f"不支持的日期类型: {type(date_input)}")

    # 根据 output_type 返回相应格式
    if output_type == 'date':
        return result_date
    elif output_type == 'datetime':
        return dt.combine(result_date, dt.min.time())
    elif output_type == 'str':
        return result_date.strftime('%Y-%m-%d')
    elif output_type == 'timestamp':
        return pd.Timestamp(result_date)
    else:
        raise ValueError(f"不支持的输出类型: '{output_type}'")


def get_shifted_date(
    base_date: Union[str, date, dt, pd.Timestamp],
    days: int,
    days_type: Literal['T', 'D'] = 'T'
) -> date:
    """
    日期偏移

    从基准日期偏移指定天数，支持交易日偏移和自然日偏移。

    Args:
        base_date: 基准日期，支持多种格式（字符串、date、datetime、Timestamp）
        days: 偏移天数，正数表示向后，负数表示向前
        days_type: 偏移类型:
            - 'T': 交易日偏移（只计算交易日）
            - 'D': 自然日偏移（包括周末和节假日）

    Returns:
        datetime.date: 偏移后的日期

    Raises:
        ValueError: 交易日偏移时超出交易日范围

    Examples:
        >>> get_shifted_date('2023-01-05', 5, 'D')  # 自然日偏移
        datetime.date(2023, 1, 10)
        >>> get_shifted_date('2023-01-05', 5, 'T')  # 交易日偏移（跳过周末）
        datetime.date(2023, 1, 12)  # 假设跳过了周末
    """
    # 转换基准日期为 date 对象
    base = transform_date(base_date, 'date')

    if days_type == 'D':
        # 自然日偏移，简单加减
        return base + timedelta(days=days)

    elif days_type == 'T':
        # 交易日偏移
        trade_days = _get_cached_trade_days()

        if not trade_days:
            raise ValueError("无法获取交易日列表")

        # 查找基准日期在交易日列表中的位置
        try:
            idx = trade_days.index(base)
        except ValueError:
            # 基准日期不在交易日列表中，需要找到最近的位置
            if days > 0:
                # 向后偏移，找下一个交易日作为起点
                for i, d in enumerate(trade_days):
                    if d > base:
                        idx = i
                        days -= 1  # 减去一步（因为从下一个交易日开始）
                        break
                else:
                    raise ValueError(f"基准日期 {base} 超出交易日范围（之后没有交易日）")
            else:
                # 向前偏移，找上一个交易日作为起点
                for i in range(len(trade_days) - 1, -1, -1):
                    if trade_days[i] < base:
                        idx = i
                        days += 1  # 加上一步（因为从上一个交易日开始）
                        break
                else:
                    raise ValueError(f"基准日期 {base} 超出交易日范围（之前没有交易日）")

        new_idx = idx + days

        # 边界检查
        if new_idx < 0:
            raise ValueError(f"偏移后的日期超出交易日范围（向前超出 {abs(new_idx)} 个交易日）")
        if new_idx >= len(trade_days):
            raise ValueError(f"偏移后的日期超出交易日范围（向后超出 {new_idx - len(trade_days) + 1} 个交易日）")

        return trade_days[new_idx]

    else:
        raise ValueError(f"不支持的偏移类型: '{days_type}'，应为 'T' 或 'D'")


def get_previous_trade_date(
    base_date: Union[str, date, dt, pd.Timestamp],
    n: int = 1
) -> date:
    """
    获取前n个交易日

    Args:
        base_date: 基准日期
        n: 向前偏移的交易日数量，默认为1

    Returns:
        datetime.date: 前第n个交易日的日期

    Raises:
        ValueError: 超出交易日范围或n为负数

    Examples:
        >>> get_previous_trade_date('2023-01-10', 1)
        datetime.date(2023, 1, 9)  # 假设1月9日是交易日
        >>> get_previous_trade_date('2023-01-10', 5)
        datetime.date(2023, 1, 4)  # 假设这期间有5个交易日
    """
    if n < 0:
        raise ValueError(f"n必须为非负数: {n}")

    if n == 0:
        # n=0 时返回基准日期本身（如果是交易日）或最近的交易日
        base = transform_date(base_date, 'date')
        trade_days = _get_cached_trade_days()
        if base in trade_days:
            return base
        # 否则找最近的交易日
        for d in trade_days:
            if d <= base:
                return d
        return trade_days[0] if trade_days else None

    return get_shifted_date(base_date, -n, 'T')


def get_next_trade_date(
    base_date: Union[str, date, dt, pd.Timestamp],
    n: int = 1
) -> date:
    """
    获取后n个交易日

    Args:
        base_date: 基准日期
        n: 向后偏移的交易日数量，默认为1

    Returns:
        datetime.date: 后第n个交易日的日期

    Raises:
        ValueError: 超出交易日范围或n为负数

    Examples:
        >>> get_next_trade_date('2023-01-05', 1)
        datetime.date(2023, 1, 6)  # 假设1月6日是交易日
        >>> get_next_trade_date('2023-01-05', 5)
        datetime.date(2023, 1, 12)  # 假设这期间有5个交易日
    """
    if n < 0:
        raise ValueError(f"n必须为非负数: {n}")

    if n == 0:
        # n=0 时返回基准日期本身（如果是交易日）或最近的交易日
        base = transform_date(base_date, 'date')
        trade_days = _get_cached_trade_days()
        if base in trade_days:
            return base
        # 否则找最近的交易日
        for i in range(len(trade_days) - 1, -1, -1):
            if trade_days[i] >= base:
                return trade_days[i]
        return trade_days[-1] if trade_days else None

    return get_shifted_date(base_date, n, 'T')


def is_trade_date(
    check_date: Union[str, date, dt, pd.Timestamp]
) -> bool:
    """
    判断是否为交易日

    Args:
        check_date: 待检查的日期

    Returns:
        bool: 是否为交易日

    Examples:
        >>> is_trade_date('2023-01-05')
        True  # 假设1月5日是交易日
        >>> is_trade_date('2023-01-07')  # 周六
        False
    """
    d = transform_date(check_date, 'date')
    trade_days = _get_cached_trade_days()
    return d in trade_days


def get_trade_dates_between(
    start_date: Union[str, date, dt, pd.Timestamp],
    end_date: Union[str, date, dt, pd.Timestamp]
) -> list:
    """
    获取两个日期之间的所有交易日

    Args:
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        list: datetime.date 对象列表，按时间升序排列

    Examples:
        >>> get_trade_dates_between('2023-01-01', '2023-01-10')
        [datetime.date(2023, 1, 2), datetime.date(2023, 1, 3), ...]
    """
    start = transform_date(start_date, 'date')
    end = transform_date(end_date, 'date')

    trade_days = _get_cached_trade_days()

    result = []
    for d in trade_days:
        if start <= d <= end:
            result.append(d)

    return result


def count_trade_dates_between(
    start_date: Union[str, date, dt, pd.Timestamp],
    end_date: Union[str, date, dt, pd.Timestamp]
) -> int:
    """
    计算两个日期之间的交易日数量

    Args:
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        int: 交易日数量

    Examples:
        >>> count_trade_dates_between('2023-01-01', '2023-01-10')
        6  # 假设这期间有6个交易日
    """
    return len(get_trade_dates_between(start_date, end_date))


# 模块级导出
__all__ = [
    'get_shifted_date',
    'get_previous_trade_date',
    'get_next_trade_date',
    'transform_date',
    'is_trade_date',
    'get_trade_dates_between',
    'count_trade_dates_between',
    'clear_trade_days_cache',
]