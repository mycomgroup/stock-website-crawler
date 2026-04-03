"""
timer_manager.py
定时器管理器，用于模拟聚宽的 run_monthly/run_daily/run_weekly 机制。

包含:
- TimerManager: 定时器管理器类
"""

import warnings
from datetime import datetime, date, timedelta, time


class TimerManager:
    """
    定时器管理器
    模拟聚宽的run_monthly/run_daily/run_weekly机制

    使用 timer_rules 模块进行规则判断
    """

    def __init__(self, strategy, trading_days=None):
        self._strategy = strategy
        self._timers = []
        self._calendar = None
        self._trading_days = trading_days
        self._bar_resolution_minutes = 1
        self._data_frequency = "daily"

        try:
            from .timer_rules import TradingDayCalendar, should_execute_timer
        except ImportError:
            try:
                from timer_rules import TradingDayCalendar, should_execute_timer
            except ImportError:
                warnings.warn("timer_rules 模块导入失败，使用简化逻辑")
                self._calendar = None
                self._should_execute_timer = None
                return

        self._calendar = TradingDayCalendar(trading_days)
        self._should_execute_timer = should_execute_timer

    def set_trading_days(self, trading_days):
        """设置交易日列表"""
        self._trading_days = trading_days
        if self._calendar:
            self._calendar.set_trading_days(trading_days)

    def set_bar_resolution(self, minutes: int):
        """设置 bar 时间粒度（分钟）"""
        self._bar_resolution_minutes = max(1, minutes)

    def set_data_frequency(self, frequency: str):
        """设置数据频率 ('daily', '1m', '5m', '15m', '30m', '60m')"""
        self._data_frequency = frequency
        freq_to_minutes = {
            "daily": 390,
            "1m": 1,
            "5m": 5,
            "15m": 15,
            "30m": 30,
            "60m": 60,
        }
        self._bar_resolution_minutes = freq_to_minutes.get(frequency, 1)

    def infer_bar_resolution(self):
        """从数据推断 bar 时间粒度"""
        if self._strategy.datas and len(self._strategy.datas) > 0:
            try:
                if len(self._strategy.datas[0]) >= 2:
                    dt0 = self._strategy.datas[0].datetime.datetime(0)
                    dt1 = self._strategy.datas[0].datetime.datetime(-1)
                    delta = (dt0 - dt1).total_seconds() / 60
                    if delta > 0:
                        self._bar_resolution_minutes = max(1, int(delta))
                        if delta >= 300:
                            self._data_frequency = "daily"
                        elif delta >= 60:
                            self._data_frequency = f"{int(delta)}m"
                        else:
                            self._data_frequency = f"{int(delta)}m"
            except Exception:
                pass

    def register(self, func, frequency, time_rule=None, day=None, weekday=None):
        """
        注册定时器

        参数:
            func: 回调函数
            frequency: 'daily', 'monthly', 'weekly'
            time_rule: 'before_open', 'open', 'after_close', 'HH:MM', 'open+Nm'
            day: 月内第 N 个交易日 (1=第一个, -1=最后一个)
            weekday: 周几 (1=周一, 5=周五)
        """
        self._timers.append(
            {
                "func": func,
                "frequency": frequency,
                "time_rule": time_rule or "open",
                "day": day,
                "weekday": weekday,
                "last_executed": None,
                "last_executed_date": None,
            }
        )

    def check_and_execute(self):
        """检查并执行到期的定时器"""
        dt = self._strategy.datetime.date(0)
        try:
            dt_datetime = self._strategy.datetime.datetime(0)
            dt_time = dt_datetime.time()
            if dt_time.hour == 0 and dt_time.minute == 0:
                dt_time = None
        except Exception:
            dt_time = None

        for timer in self._timers:
            should_exec, reason = self._should_execute(timer, dt, dt_time)
            if should_exec:
                try:
                    timer["func"](self._strategy.context)
                    timer["last_executed"] = dt
                    timer["last_executed_date"] = dt
                except Exception as e:
                    import traceback
                    self._strategy.log(f"定时器执行错误: {e}")
                    self._strategy.log(f"详细traceback:\n{traceback.format_exc()}")

    def _should_execute(self, timer, dt, dt_time=None):
        """
        判断是否应该执行定时器

        Returns:
            (should_execute, reason)
        """
        time_rule = timer.get("time_rule", "open")

        if time_rule == "every_bar":
            if dt.weekday() >= 5:
                return (False, "weekend")
            return (True, "every_bar")

        if self._should_execute_timer:
            return self._should_execute_timer(
                frequency=timer["frequency"],
                current_date=dt,
                current_time=dt_time,
                last_executed=timer.get("last_executed_date"),
                time_rule=time_rule,
                day=timer.get("day"),
                weekday=timer.get("weekday"),
                trading_days=self._trading_days,
                bar_resolution_minutes=self._bar_resolution_minutes,
            )

        last = timer.get("last_executed_date")
        frequency = timer["frequency"]
        target_weekday = timer.get("weekday", 1)
        target_day = timer.get("day", 1)

        if dt.weekday() >= 5:
            return (False, "weekend")

        if last == dt:
            return (False, "same_day")

        if last is None:
            if not self._check_time_rule(dt_time, time_rule):
                return (False, "time_not_match")
            if frequency == "weekly" and dt.weekday() + 1 != target_weekday:
                return (False, "not_target_weekday")
            if frequency == "monthly":
                target_date = self._get_nth_trading_day(dt.year, dt.month, target_day)
                if target_date != dt:
                    return (False, "not_target_day")
            return (True, "first_execution")

        if frequency == "daily":
            if not self._check_time_rule(dt_time, time_rule):
                return (False, "time_not_match")
            return (True, "next_trading_day")

        elif frequency == "weekly":
            if dt.weekday() + 1 != target_weekday:
                return (False, "not_target_weekday")
            week_start_current = dt - timedelta(days=dt.weekday())
            week_start_last = last - timedelta(days=last.weekday())
            if week_start_current == week_start_last:
                return (False, "same_week")
            if not self._check_time_rule(dt_time, time_rule):
                return (False, "time_not_match")
            return (True, "target_weekday")

        elif frequency == "monthly":
            # 使用更宽松的月度判断，考虑节假日
            # 如果本月还没执行过，且当前日期在月内前几个工作日内，则执行
            if last is not None and last.year == dt.year and last.month == dt.month:
                return (False, "same_month")
            if not self._check_time_rule(dt_time, time_rule):
                return (False, "time_not_match")

            # 检查是否是月内第一个实际交易日（考虑节假日）
            if target_day == 1:  # 第一个交易日
                if self._is_first_trading_day_of_month(dt):
                    return (True, "first_trading_day_of_month")
                else:
                    return (False, "not_first_trading_day")
            else:
                # 对于其他日期，使用原来的精确计算
                target_date = self._get_nth_trading_day(dt.year, dt.month, target_day)
                if target_date != dt:
                    return (False, "not_target_day")
                return (True, "target_day")

        return (False, "unknown_frequency")

    def _check_time_rule(self, bar_time, time_rule):
        """
        检查时间规则匹配（简化版）

        Args:
            bar_time: 当前 bar 时间，若为 None 则跳过时间检查
            time_rule: 时间规则字符串

        Returns:
            是否匹配
        """
        if bar_time is None:
            return True

        rule = (time_rule or "open").lower().strip()

        if rule == "before_open":
            return bar_time < time(9, 30)

        if rule == "open":
            return (
                abs(
                    (
                        datetime.combine(date.today(), bar_time)
                        - datetime.combine(date.today(), time(9, 30))
                    ).total_seconds()
                )
                <= self._bar_resolution_minutes * 60
            )

        if rule == "after_close":
            return (
                bar_time >= time(15, 0)
                or abs(
                    (
                        datetime.combine(date.today(), bar_time)
                        - datetime.combine(date.today(), time(15, 0))
                    ).total_seconds()
                )
                <= self._bar_resolution_minutes * 60
            )

        if ":" in rule and "+" not in rule and "-" not in rule:
            try:
                parts = rule.split(":")
                h, m = int(parts[0]), int(parts[1])
                target = time(h, m)
                return (
                    abs(
                        (
                            datetime.combine(date.today(), bar_time)
                            - datetime.combine(date.today(), target)
                        ).total_seconds()
                    )
                    <= self._bar_resolution_minutes * 60
                )
            except (ValueError, IndexError):
                return True

        if rule.startswith("open+") or rule.startswith("open-"):
            try:
                sign = 1 if "+" in rule else -1
                offset_str = rule.split(sign > 0 and "+" or "-")[1]
                offset = int(offset_str.replace("m", "").replace("min", "").strip())
                base_dt = datetime.combine(date.today(), time(9, 30))
                target_dt = base_dt + timedelta(minutes=sign * offset)
                target = target_dt.time()
                return (
                    abs(
                        (
                            datetime.combine(date.today(), bar_time)
                            - datetime.combine(date.today(), target)
                        ).total_seconds()
                    )
                    <= self._bar_resolution_minutes * 60
                )
            except (ValueError, IndexError):
                return True

        return True

    def _get_nth_trading_day(self, year, month, n):
        """
        获取月内第 N 个交易日（简化版，仅排除周末）

        Args:
            year: 年份
            month: 月份
            n: 第 N 个交易日 (1=第一个, -1=最后一个)

        Returns:
            交易日日期
        """
        import calendar

        days_in_month = calendar.monthrange(year, month)[1]
        month_days = []
        for day in range(1, days_in_month + 1):
            d = date(year, month, day)
            if d.weekday() < 5:
                month_days.append(d)

        if not month_days:
            return None

        month_days.sort()

        if n > 0:
            idx = n - 1
            return month_days[idx] if idx < len(month_days) else month_days[-1]
        elif n < 0:
            idx = len(month_days) + n
            return month_days[idx] if idx >= 0 else month_days[0]

        return month_days[0]

    def _is_first_trading_day_of_month(self, dt):
        """
        检查给定日期是否是当月的第一个实际交易日

        使用策略数据来确定实际交易日，而不是日历计算。
        这可以处理节假日情况。
        """
        # 获取当月第一天的下一个工作日
        import calendar
        days_in_month = calendar.monthrange(dt.year, dt.month)[1]

        # 查找当月第一个工作日
        first_weekday = None
        for day in range(1, days_in_month + 1):
            d = date(dt.year, dt.month, day)
            if d.weekday() < 5:
                first_weekday = d
                break

        if first_weekday is None:
            return False

        # 如果当前日期等于第一个工作日，或者是第一个工作日之后的几天
        # 且之前没有其他工作日（考虑到节假日），则认为是第一个交易日
        # 这里使用宽松的判断：如果当前日期在月内前5个工作日内，且还没执行过，则允许执行
        return dt.day <= first_weekday.day + 4  # 允许节假日偏移

    def reset(self):
        """清空所有定时器"""
        self._timers.clear()


__all__ = ['TimerManager']