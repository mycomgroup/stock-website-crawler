"""
timer_rules.py
聚宽风格定时器规则引擎 - 纯函数实现

支持规则:
- run_daily / run_weekly / run_monthly
- 时间规则: before_open, open, after_close, HH:MM, open+Nm
- 月内第N个交易日、周几执行

设计原则:
- 所有判断函数都是纯函数，可独立测试
- 交易日历可注入，便于合成测试
- 对不支持的规则显式降级并记录

交易日历:
- 支持从akshare获取真实A股交易日历（包含节假日）
- 自动缓存交易日历数据
"""

from datetime import datetime, date, time, timedelta
from typing import Optional, List, Callable, Tuple, Dict, Any, Set
import warnings
import os
import pickle
import logging

try:
    import pandas as pd
except ImportError:
    pd = None

logger = logging.getLogger(__name__)

MARKET_OPEN_TIME = time(9, 30)
MARKET_CLOSE_TIME = time(15, 0)
MARKET_OPEN_AM = time(9, 30)
MARKET_CLOSE_AM = time(11, 30)
MARKET_OPEN_PM = time(13, 0)
MARKET_CLOSE_PM = time(15, 0)

_TIME_RULE_PRECISION_WARNED = set()

# 全局交易日历缓存
_TRADING_DAYS_CACHE: Optional[Set[date]] = None
_TRADING_DAYS_LIST_CACHE: Optional[List[date]] = None
_CACHE_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "trading_days_cache.pkl")


def _fetch_trading_days_from_akshare() -> List[date]:
    """从akshare获取真实A股交易日历"""
    try:
        import akshare as ak
        df = ak.tool_trade_date_hist_sina()
        if df is not None and not df.empty:
            # 列名可能是 'trade_date'
            date_col = None
            for col in df.columns:
                if 'date' in col.lower():
                    date_col = col
                    break
            if date_col is None:
                date_col = df.columns[0]

            dates = pd.to_datetime(df[date_col]).dt.date.tolist()
            logger.info(f"从akshare获取到 {len(dates)} 个交易日")
            return dates
    except Exception as e:
        logger.warning(f"获取akshare交易日历失败: {e}")
    return []


def get_real_trading_days(force_update: bool = False) -> List[date]:
    """
    获取真实A股交易日历（包含节假日）

    优先级:
    1. 内存缓存
    2. 本地文件缓存
    3. akshare在线获取

    Args:
        force_update: 是否强制更新

    Returns:
        交易日列表
    """
    global _TRADING_DAYS_CACHE, _TRADING_DAYS_LIST_CACHE

    # 检查内存缓存
    if not force_update and _TRADING_DAYS_LIST_CACHE is not None:
        return _TRADING_DAYS_LIST_CACHE

    # 检查文件缓存
    if not force_update and os.path.exists(_CACHE_FILE_PATH):
        try:
            with open(_CACHE_FILE_PATH, "rb") as f:
                cached_data = pickle.load(f)
                # 检查缓存是否过期（超过30天）
                cache_time = cached_data.get("timestamp", 0)
                if (datetime.now().timestamp() - cache_time) < 30 * 24 * 3600:
                    days_list = cached_data.get("trading_days", [])
                    if days_list:
                        _TRADING_DAYS_LIST_CACHE = days_list
                        _TRADING_DAYS_CACHE = set(days_list)
                        logger.info(f"从缓存加载 {len(days_list)} 个交易日")
                        return days_list
        except Exception as e:
            logger.warning(f"加载交易日历缓存失败: {e}")

    # 从akshare获取
    import pandas as pd
    days_list = _fetch_trading_days_from_akshare()

    if not days_list:
        # 降级到近似计算
        logger.warning("无法获取真实交易日历，使用近似计算")
        return None

    # 更新缓存
    _TRADING_DAYS_LIST_CACHE = days_list
    _TRADING_DAYS_CACHE = set(days_list)

    # 保存到文件
    try:
        os.makedirs(os.path.dirname(_CACHE_FILE_PATH), exist_ok=True)
        with open(_CACHE_FILE_PATH, "wb") as f:
            pickle.dump({
                "trading_days": days_list,
                "timestamp": datetime.now().timestamp()
            }, f)
        logger.info(f"交易日历已缓存到 {_CACHE_FILE_PATH}")
    except Exception as e:
        logger.warning(f"保存交易日历缓存失败: {e}")

    return days_list


def get_real_trading_days_set(force_update: bool = False) -> Set[date]:
    """获取真实交易日集合（用于快速查询）"""
    global _TRADING_DAYS_CACHE

    if not force_update and _TRADING_DAYS_CACHE is not None:
        return _TRADING_DAYS_CACHE

    days_list = get_real_trading_days(force_update)
    if days_list:
        _TRADING_DAYS_CACHE = set(days_list)
        return _TRADING_DAYS_CACHE

    return None


def parse_time_rule(rule: str) -> Tuple[str, Optional[time], Optional[int]]:
    """
    解析时间规则字符串

    Returns:
        (rule_type, target_time, offset_minutes)
        rule_type: 'before_open', 'open', 'after_close', 'absolute', 'open_offset', 'close_offset',
                   'every_bar', 'market_open', 'market_close', 'intraday'
    """
    if rule is None:
        return ("open", MARKET_OPEN_TIME, None)

    rule = rule.lower().strip()

    if rule == "before_open":
        return ("before_open", None, None)

    if rule == "open":
        return ("open", MARKET_OPEN_TIME, None)

    if rule == "after_close":
        return ("after_close", MARKET_CLOSE_TIME, None)

    if rule == "every_bar":
        return ("every_bar", None, None)

    if rule in ("market_open", "开盘"):
        return ("market_open", MARKET_OPEN_TIME, None)

    if rule in ("market_close", "收盘", "尾盘"):
        return ("market_close", MARKET_CLOSE_TIME, None)

    if rule == "intraday" or rule == "盘中":
        return ("intraday", None, None)

    if rule == "尾盘":
        return ("market_close", MARKET_CLOSE_TIME, None)

    if ":" in rule and "+" not in rule and "-" not in rule:
        try:
            parts = rule.split(":")
            h, m = int(parts[0]), int(parts[1])
            return ("absolute", time(h, m), None)
        except (ValueError, IndexError):
            warnings.warn(f"无法解析时间规则: {rule}, 默认使用 open")
            return ("open", MARKET_OPEN_TIME, None)

    if rule.startswith("open+"):
        try:
            offset = int(rule.split("+")[1].replace("m", "").replace("min", "").strip())
            base_time = MARKET_OPEN_TIME
            target_dt = datetime.combine(date.today(), base_time) + timedelta(
                minutes=offset
            )
            return ("open_offset", target_dt.time(), offset)
        except (ValueError, IndexError):
            warnings.warn(f"无法解析偏移规则: {rule}")
            return ("open", MARKET_OPEN_TIME, None)

    if rule.startswith("open-"):
        try:
            offset = int(rule.split("-")[1].replace("m", "").replace("min", "").strip())
            base_time = MARKET_OPEN_TIME
            target_dt = datetime.combine(date.today(), base_time) - timedelta(
                minutes=offset
            )
            return ("open_offset", target_dt.time(), -offset)
        except (ValueError, IndexError):
            warnings.warn(f"无法解析偏移规则: {rule}")
            return ("open", MARKET_OPEN_TIME, None)

    if rule.startswith("close+"):
        try:
            offset = int(rule.split("+")[1].replace("m", "").replace("min", "").strip())
            base_time = MARKET_CLOSE_TIME
            target_dt = datetime.combine(date.today(), base_time) + timedelta(
                minutes=offset
            )
            return ("close_offset", target_dt.time(), offset)
        except (ValueError, IndexError):
            warnings.warn(f"无法解析偏移规则: {rule}")
            return ("after_close", MARKET_CLOSE_TIME, None)

    if rule.startswith("close-"):
        try:
            offset = int(rule.split("-")[1].replace("m", "").replace("min", "").strip())
            base_time = MARKET_CLOSE_TIME
            target_dt = datetime.combine(date.today(), base_time) - timedelta(
                minutes=offset
            )
            return ("close_offset", target_dt.time(), -offset)
        except (ValueError, IndexError):
            warnings.warn(f"无法解析偏移规则: {rule}")
            return ("after_close", MARKET_CLOSE_TIME, None)

    warnings.warn(f"未知时间规则: {rule}, 默认使用 open")
    return ("open", MARKET_OPEN_TIME, None)


def check_bar_time_match(
    bar_time: time,
    rule_type: str,
    target_time: Optional[time],
    bar_resolution_minutes: int = 1,
    rule_str: str = "",
) -> bool:
    """
    检查当前 bar 时间是否匹配时间规则

    Args:
        bar_time: 当前 bar 的时间
        rule_type: 规则类型
        target_time: 目标时间
        bar_resolution_minutes: bar 粒度（分钟）
        rule_str: 原始规则字符串（用于警告）

    Returns:
        是否匹配
    """
    if rule_type == "every_bar":
        return True

    if rule_type == "intraday":
        return MARKET_OPEN_TIME <= bar_time <= MARKET_CLOSE_TIME

    if rule_type == "market_open":
        tolerance = timedelta(minutes=max(bar_resolution_minutes, 1))
        bar_dt = datetime.combine(date.today(), bar_time)
        target_dt = datetime.combine(date.today(), MARKET_OPEN_TIME)
        return abs(bar_dt - target_dt) <= tolerance

    if rule_type == "market_close":
        tolerance = timedelta(minutes=max(bar_resolution_minutes, 1))
        bar_dt = datetime.combine(date.today(), bar_time)
        target_dt = datetime.combine(date.today(), MARKET_CLOSE_TIME)
        return abs(bar_dt - target_dt) <= tolerance

    if rule_type == "before_open":
        return bar_time < MARKET_OPEN_TIME

    if rule_type == "open":
        tolerance = timedelta(minutes=bar_resolution_minutes)
        bar_dt = datetime.combine(date.today(), bar_time)
        target_dt = datetime.combine(date.today(), MARKET_OPEN_TIME)
        return abs(bar_dt - target_dt) <= tolerance

    if rule_type == "after_close":
        tolerance = timedelta(minutes=bar_resolution_minutes)
        bar_dt = datetime.combine(date.today(), bar_time)
        target_dt = datetime.combine(date.today(), MARKET_CLOSE_TIME)
        return abs(bar_dt - target_dt) <= tolerance or bar_time >= MARKET_CLOSE_TIME

    if rule_type in ("absolute", "open_offset", "close_offset"):
        if target_time is None:
            return False

        tolerance = timedelta(minutes=max(bar_resolution_minutes, 1))
        bar_dt = datetime.combine(date.today(), bar_time)
        target_dt = datetime.combine(date.today(), target_time)

        if abs(bar_dt - target_dt) <= tolerance:
            return True

        if bar_resolution_minutes > 1 and rule_str not in _TIME_RULE_PRECISION_WARNED:
            _TIME_RULE_PRECISION_WARNED.add(rule_str)
            warnings.warn(
                f"时间规则 '{rule_str}' 目标时间 {target_time} 与 bar 时间 {bar_time} "
                f"差异超过 bar 粒度 {bar_resolution_minutes} 分钟，降级为宽松匹配"
            )

        loose_tolerance = timedelta(minutes=bar_resolution_minutes * 2)
        return abs(bar_dt - target_dt) <= loose_tolerance

    return False


def is_trading_day(dt: date, trading_days: Optional[List[date]] = None) -> bool:
    """
    判断是否为交易日

    Args:
        dt: 待判断日期
        trading_days: 交易日列表（可选，用于精确判断）

    Returns:
        是否为交易日
    """
    if trading_days is not None:
        return dt in trading_days

    # 尝试使用真实交易日历
    real_days = get_real_trading_days_set()
    if real_days is not None:
        return dt in real_days

    # 降级到简单判断（仅排除周末）
    weekday = dt.weekday()
    if weekday >= 5:
        return False

    return True


def get_nth_trading_day_in_month(
    month: int, year: int, n: int, trading_days: Optional[List[date]] = None
) -> Optional[date]:
    """
    获取月内第 N 个交易日

    Args:
        month: 月份 (1-12)
        year: 年份
        n: 第 N 个交易日 (1=第一个, -1=最后一个, -2倒数第二个)
        trading_days: 交易日列表

    Returns:
        交易日日期，若不存在则返回 None
    """
    if trading_days is None:
        trading_days = _generate_approx_trading_days(year, month)

    month_days = [d for d in trading_days if d.year == year and d.month == month]

    if not month_days:
        return None

    month_days.sort()

    if n > 0:
        idx = n - 1
        return month_days[idx] if idx < len(month_days) else None
    elif n < 0:
        idx = len(month_days) + n
        return month_days[idx] if idx >= 0 else None

    return month_days[0]


def _generate_approx_trading_days(year: int, month: int) -> List[date]:
    """
    生成近似交易日列表（排除周末，不含节假日）
    用于无交易日历时的降级判断
    """
    import calendar

    days_in_month = calendar.monthrange(year, month)[1]
    trading_days = []

    for day in range(1, days_in_month + 1):
        dt = date(year, month, day)
        if dt.weekday() < 5:
            trading_days.append(dt)

    return trading_days


def check_daily_trigger(
    current_date: date,
    last_executed: Optional[date],
    trading_days: Optional[List[date]] = None,
) -> bool:
    """
    判断 daily 定时器是否应该触发

    Args:
        current_date: 当前日期
        last_executed: 上次执行日期
        trading_days: 交易日列表

    Returns:
        是否应该触发
    """
    if not is_trading_day(current_date, trading_days):
        return False

    if last_executed is None:
        return True

    if last_executed == current_date:
        return False

    return True


def check_weekly_trigger(
    current_date: date,
    last_executed: Optional[date],
    target_weekday: int,
    trading_days: Optional[List[date]] = None,
) -> bool:
    """
    判断 weekly 定时器是否应该触发

    Args:
        current_date: 当前日期
        last_executed: 上次执行日期
        target_weekday: 目标周几 (1=周一, 5=周五)
        trading_days: 交易日列表

    Returns:
        是否应该触发
    """
    if not is_trading_day(current_date, trading_days):
        return False

    current_weekday = current_date.weekday() + 1

    if current_weekday != target_weekday:
        return False

    if last_executed is None:
        return True

    if last_executed == current_date:
        return False

    week_diff = (current_date - last_executed).days // 7
    if week_diff < 1:
        week_start_current = current_date - timedelta(days=current_date.weekday())
        week_start_last = last_executed - timedelta(days=last_executed.weekday())
        if week_start_current == week_start_last:
            return False

    return True


def check_monthly_trigger(
    current_date: date,
    last_executed: Optional[date],
    target_day: int,
    trading_days: Optional[List[date]] = None,
) -> bool:
    """
    判断 monthly 定时器是否应该触发

    Args:
        current_date: 当前日期
        last_executed: 上次执行日期
        target_day: 月内第 N 个交易日 (1=第一个, -1=最后一个)
        trading_days: 交易日列表

    Returns:
        是否应该触发
    """
    if not is_trading_day(current_date, trading_days):
        return False

    target_date = get_nth_trading_day_in_month(
        current_date.month, current_date.year, target_day, trading_days
    )

    if target_date is None or target_date != current_date:
        return False

    if last_executed is None:
        return True

    if (
        last_executed.year == current_date.year
        and last_executed.month == current_date.month
    ):
        return False

    return True


def should_execute_timer(
    frequency: str,
    current_date: date,
    current_time: Optional[time],
    last_executed: Optional[date],
    time_rule: str = "open",
    day: Optional[int] = None,
    weekday: Optional[int] = None,
    trading_days: Optional[List[date]] = None,
    bar_resolution_minutes: int = 1,
) -> Tuple[bool, str]:
    """
    综合判断定时器是否应该执行

    Args:
        frequency: 频率 ('daily', 'weekly', 'monthly')
        current_date: 当前日期
        current_time: 当前 bar 时间
        last_executed: 上次执行日期
        time_rule: 时间规则
        day: 月内第 N 个交易日
        weekday: 目标周几
        trading_days: 交易日列表
        bar_resolution_minutes: bar 时间粒度

    Returns:
        (should_execute, reason)
    """
    if frequency == "daily":
        if not check_daily_trigger(current_date, last_executed, trading_days):
            return (False, "not_trading_day_or_same_day")

    elif frequency == "weekly":
        target_weekday = weekday if weekday is not None else 1
        if not check_weekly_trigger(
            current_date, last_executed, target_weekday, trading_days
        ):
            return (False, "not_target_weekday_or_same_week")

    elif frequency == "monthly":
        target_day = day if day is not None else 1
        if not check_monthly_trigger(
            current_date, last_executed, target_day, trading_days
        ):
            return (False, "not_target_day_or_same_month")

    else:
        return (False, f"unknown_frequency: {frequency}")

    if current_time is None:
        return (True, "no_time_check")

    rule_type, target_time, offset = parse_time_rule(time_rule)
    time_match = check_bar_time_match(
        current_time, rule_type, target_time, bar_resolution_minutes, time_rule
    )

    if not time_match:
        return (False, f"time_not_match: current={current_time}, rule={time_rule}")

    return (True, "triggered")


class TradingDayCalendar:
    """
    交易日历类，提供交易日查询和缓存

    支持真实A股交易日历（包含节假日）
    """

    def __init__(self, trading_days: Optional[List[date]] = None):
        self._trading_days = trading_days
        self._trading_days_set = None
        self._month_cache: Dict[Tuple[int, int], List[date]] = {}
        self._use_real_calendar = False

        # 如果没有传入交易日列表，尝试使用真实交易日历
        if trading_days is None:
            real_days = get_real_trading_days()
            if real_days:
                self._trading_days = real_days
                self._trading_days_set = set(real_days)
                self._use_real_calendar = True
                logger.info(f"TradingDayCalendar: 使用真实A股交易日历，共 {len(real_days)} 个交易日")

    def set_trading_days(self, trading_days: List[date]):
        """设置交易日列表"""
        self._trading_days = trading_days
        self._trading_days_set = set(trading_days) if trading_days else None
        self._month_cache.clear()
        self._use_real_calendar = False

    def is_trading_day(self, dt: date) -> bool:
        """判断是否为交易日"""
        if self._trading_days_set is not None:
            return dt in self._trading_days_set
        return is_trading_day(dt, self._trading_days)

    def get_nth_trading_day_in_month(
        self, year: int, month: int, n: int
    ) -> Optional[date]:
        """获取月内第 N 个交易日"""
        cache_key = (year, month)
        if cache_key not in self._month_cache:
            if self._trading_days is not None:
                self._month_cache[cache_key] = [
                    d for d in self._trading_days if d.year == year and d.month == month
                ]
            else:
                # 使用真实交易日历
                real_days = get_real_trading_days()
                if real_days:
                    self._month_cache[cache_key] = [
                        d for d in real_days if d.year == year and d.month == month
                    ]
                else:
                    self._month_cache[cache_key] = _generate_approx_trading_days(
                        year, month
                    )

        month_days = self._month_cache[cache_key]
        if not month_days:
            return None

        month_days = sorted(month_days)

        if n > 0:
            idx = n - 1
            return month_days[idx] if idx < len(month_days) else None
        elif n < 0:
            idx = len(month_days) + n
            return month_days[idx] if idx >= 0 else None

        return month_days[0]

    def get_first_trading_day_of_month(self, year: int, month: int) -> Optional[date]:
        """获取月内第一个交易日"""
        return self.get_nth_trading_day_in_month(year, month, 1)

    def get_last_trading_day_of_month(self, year: int, month: int) -> Optional[date]:
        """获取月内最后一个交易日"""
        return self.get_nth_trading_day_in_month(year, month, -1)

    def get_all_trading_days(self) -> Optional[List[date]]:
        """获取所有交易日"""
        return self._trading_days

    def is_first_trading_day_of_month(self, dt: date) -> bool:
        """判断是否为月内第一个交易日"""
        first_day = self.get_first_trading_day_of_month(dt.year, dt.month)
        return first_day is not None and dt == first_day
