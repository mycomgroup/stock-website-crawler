"""
test_timer_rules.py
定时器规则引擎单元测试

使用合成交易日和合成 bar 时间进行测试
"""

import unittest
import sys
import os
from datetime import date, time, datetime, timedelta

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src",
    ),
)

from timer_rules import (
    parse_time_rule,
    check_bar_time_match,
    is_trading_day,
    get_nth_trading_day_in_month,
    check_daily_trigger,
    check_weekly_trigger,
    check_monthly_trigger,
    should_execute_timer,
    TradingDayCalendar,
    MARKET_OPEN_TIME,
    MARKET_CLOSE_TIME,
)


def make_trading_days(year: int, months: list) -> list:
    """
    生成合成交易日列表（排除周末）
    """
    import calendar

    trading_days = []
    for month in months:
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            dt = date(year, month, day)
            if dt.weekday() < 5:
                trading_days.append(dt)
    return trading_days


class TestParseTimeRule(unittest.TestCase):
    """测试时间规则解析"""

    def test_parse_none(self):
        rule_type, target_time, offset = parse_time_rule(None)
        self.assertEqual(rule_type, "open")
        self.assertEqual(target_time, MARKET_OPEN_TIME)

    def test_parse_before_open(self):
        rule_type, target_time, offset = parse_time_rule("before_open")
        self.assertEqual(rule_type, "before_open")
        self.assertIsNone(target_time)

    def test_parse_open(self):
        rule_type, target_time, offset = parse_time_rule("open")
        self.assertEqual(rule_type, "open")
        self.assertEqual(target_time, MARKET_OPEN_TIME)

    def test_parse_after_close(self):
        rule_type, target_time, offset = parse_time_rule("after_close")
        self.assertEqual(rule_type, "after_close")
        self.assertEqual(target_time, MARKET_CLOSE_TIME)

    def test_parse_absolute_time(self):
        rule_type, target_time, offset = parse_time_rule("10:30")
        self.assertEqual(rule_type, "absolute")
        self.assertEqual(target_time, time(10, 30))

    def test_parse_open_offset_plus(self):
        rule_type, target_time, offset = parse_time_rule("open+30m")
        self.assertEqual(rule_type, "open_offset")
        self.assertEqual(target_time, time(10, 0))
        self.assertEqual(offset, 30)

    def test_parse_open_offset_minus(self):
        rule_type, target_time, offset = parse_time_rule("open-5m")
        self.assertEqual(rule_type, "open_offset")
        self.assertEqual(target_time, time(9, 25))
        self.assertEqual(offset, -5)

    def test_parse_close_offset_minus(self):
        rule_type, target_time, offset = parse_time_rule("close-10m")
        self.assertEqual(rule_type, "close_offset")
        self.assertEqual(target_time, time(14, 50))
        self.assertEqual(offset, -10)

    def test_parse_invalid(self):
        with self.assertWarns(UserWarning):
            rule_type, target_time, offset = parse_time_rule("invalid_rule")
        self.assertEqual(rule_type, "open")


class TestCheckBarTimeMatch(unittest.TestCase):
    """测试 bar 时间匹配"""

    def test_before_open_match(self):
        result = check_bar_time_match(time(9, 0), "before_open", None)
        self.assertTrue(result)

    def test_before_open_not_match(self):
        result = check_bar_time_match(time(10, 0), "before_open", None)
        self.assertFalse(result)

    def test_open_match_exact(self):
        result = check_bar_time_match(
            time(9, 30), "open", MARKET_OPEN_TIME, bar_resolution_minutes=1
        )
        self.assertTrue(result)

    def test_open_match_tolerance(self):
        result = check_bar_time_match(
            time(9, 31), "open", MARKET_OPEN_TIME, bar_resolution_minutes=2
        )
        self.assertTrue(result)

    def test_after_close_match(self):
        result = check_bar_time_match(time(15, 0), "after_close", MARKET_CLOSE_TIME)
        self.assertTrue(result)

    def test_after_close_late(self):
        result = check_bar_time_match(time(15, 5), "after_close", MARKET_CLOSE_TIME)
        self.assertTrue(result)

    def test_absolute_match(self):
        result = check_bar_time_match(time(10, 30), "absolute", time(10, 30))
        self.assertTrue(result)

    def test_absolute_near_match(self):
        result = check_bar_time_match(
            time(10, 31), "absolute", time(10, 30), bar_resolution_minutes=2
        )
        self.assertTrue(result)


class TestIsTradingDay(unittest.TestCase):
    """测试交易日判断"""

    def test_weekday_trading(self):
        trading_days = make_trading_days(2023, [1])
        self.assertTrue(is_trading_day(date(2023, 1, 3), trading_days))

    def test_weekend_not_trading(self):
        self.assertFalse(is_trading_day(date(2023, 1, 7)))

    def test_without_calendar_weekday(self):
        self.assertTrue(is_trading_day(date(2023, 1, 3)))

    def test_without_calendar_weekend(self):
        self.assertFalse(is_trading_day(date(2023, 1, 8)))


class TestGetNthTradingDayInMonth(unittest.TestCase):
    """测试月内第 N 个交易日"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2, 3])

    def test_first_trading_day(self):
        result = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        self.assertEqual(result, date(2023, 1, 2))

    def test_second_trading_day(self):
        result = get_nth_trading_day_in_month(1, 2023, 2, self.trading_days)
        self.assertEqual(result, date(2023, 1, 3))

    def test_last_trading_day(self):
        result = get_nth_trading_day_in_month(1, 2023, -1, self.trading_days)
        self.assertEqual(result, date(2023, 1, 31))

    def test_second_last_trading_day(self):
        result = get_nth_trading_day_in_month(1, 2023, -2, self.trading_days)
        self.assertEqual(result, date(2023, 1, 30))

    def test_approx_without_calendar(self):
        result = get_nth_trading_day_in_month(1, 2023, 1)
        self.assertEqual(result, date(2023, 1, 2))


class TestCheckDailyTrigger(unittest.TestCase):
    """测试 daily 定时器触发"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1])

    def test_first_execution(self):
        result = check_daily_trigger(date(2023, 1, 3), None, self.trading_days)
        self.assertTrue(result)

    def test_same_day_not_trigger(self):
        result = check_daily_trigger(
            date(2023, 1, 3), date(2023, 1, 3), self.trading_days
        )
        self.assertFalse(result)

    def test_next_day_trigger(self):
        result = check_daily_trigger(
            date(2023, 1, 4), date(2023, 1, 3), self.trading_days
        )
        self.assertTrue(result)

    def test_weekend_not_trigger(self):
        result = check_daily_trigger(
            date(2023, 1, 7), date(2023, 1, 6), self.trading_days
        )
        self.assertFalse(result)


class TestCheckWeeklyTrigger(unittest.TestCase):
    """测试 weekly 定时器触发"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2])

    def test_first_execution_monday(self):
        result = check_weekly_trigger(date(2023, 1, 2), None, 1, self.trading_days)
        self.assertTrue(result)

    def test_same_week_not_trigger(self):
        result = check_weekly_trigger(
            date(2023, 1, 3), date(2023, 1, 2), 1, self.trading_days
        )
        self.assertFalse(result)

    def test_next_week_trigger(self):
        result = check_weekly_trigger(
            date(2023, 1, 9), date(2023, 1, 2), 1, self.trading_days
        )
        self.assertTrue(result)

    def test_wrong_weekday_not_trigger(self):
        result = check_weekly_trigger(
            date(2023, 1, 3), date(2023, 1, 2), 1, self.trading_days
        )
        self.assertFalse(result)

    def test_friday_trigger(self):
        result = check_weekly_trigger(date(2023, 1, 6), None, 5, self.trading_days)
        self.assertTrue(result)


class TestCheckMonthlyTrigger(unittest.TestCase):
    """测试 monthly 定时器触发"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2, 3])

    def test_first_trading_day_trigger(self):
        first_day = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        result = check_monthly_trigger(first_day, None, 1, self.trading_days)
        self.assertTrue(result)

    def test_same_month_not_trigger(self):
        first_day = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        second_day = get_nth_trading_day_in_month(1, 2023, 2, self.trading_days)
        result = check_monthly_trigger(second_day, first_day, 1, self.trading_days)
        self.assertFalse(result)

    def test_next_month_trigger(self):
        jan_first = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        feb_first = get_nth_trading_day_in_month(2, 2023, 1, self.trading_days)
        result = check_monthly_trigger(feb_first, jan_first, 1, self.trading_days)
        self.assertTrue(result)

    def test_last_trading_day_trigger(self):
        jan_last = get_nth_trading_day_in_month(1, 2023, -1, self.trading_days)
        result = check_monthly_trigger(jan_last, None, -1, self.trading_days)
        self.assertTrue(result)

    def test_wrong_day_not_trigger(self):
        second_day = get_nth_trading_day_in_month(1, 2023, 2, self.trading_days)
        result = check_monthly_trigger(second_day, None, 1, self.trading_days)
        self.assertFalse(result)


class TestShouldExecuteTimer(unittest.TestCase):
    """测试综合定时器触发判断"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2, 3])

    def test_daily_open_trigger(self):
        first_day = date(2023, 1, 3)
        result, reason = should_execute_timer(
            "daily",
            first_day,
            MARKET_OPEN_TIME,
            None,
            time_rule="open",
            trading_days=self.trading_days,
        )
        self.assertTrue(result)
        self.assertEqual(reason, "triggered")

    def test_daily_same_day_not_trigger(self):
        first_day = date(2023, 1, 3)
        result, reason = should_execute_timer(
            "daily",
            first_day,
            MARKET_OPEN_TIME,
            first_day,
            time_rule="open",
            trading_days=self.trading_days,
        )
        self.assertFalse(result)

    def test_weekly_monday_trigger(self):
        monday = date(2023, 1, 2)
        result, reason = should_execute_timer(
            "weekly",
            monday,
            MARKET_OPEN_TIME,
            None,
            time_rule="open",
            weekday=1,
            trading_days=self.trading_days,
        )
        self.assertTrue(result)

    def test_weekly_wrong_day_not_trigger(self):
        tuesday = date(2023, 1, 3)
        result, reason = should_execute_timer(
            "weekly",
            tuesday,
            MARKET_OPEN_TIME,
            None,
            time_rule="open",
            weekday=1,
            trading_days=self.trading_days,
        )
        self.assertFalse(result)

    def test_monthly_first_day_trigger(self):
        first_day = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        result, reason = should_execute_timer(
            "monthly",
            first_day,
            MARKET_OPEN_TIME,
            None,
            time_rule="open",
            day=1,
            trading_days=self.trading_days,
        )
        self.assertTrue(result)

    def test_time_not_match(self):
        first_day = date(2023, 1, 3)
        result, reason = should_execute_timer(
            "daily",
            first_day,
            time(10, 0),
            None,
            time_rule="open",
            trading_days=self.trading_days,
        )
        self.assertFalse(result)
        self.assertIn("time_not_match", reason)

    def test_no_time_check(self):
        first_day = date(2023, 1, 3)
        result, reason = should_execute_timer(
            "daily",
            first_day,
            None,
            None,
            time_rule="open",
            trading_days=self.trading_days,
        )
        self.assertTrue(result)
        self.assertEqual(reason, "no_time_check")


class TestTradingDayCalendar(unittest.TestCase):
    """测试交易日历类"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2, 3])
        self.calendar = TradingDayCalendar(self.trading_days)

    def test_is_trading_day_true(self):
        self.assertTrue(self.calendar.is_trading_day(date(2023, 1, 3)))

    def test_is_trading_day_false(self):
        self.assertFalse(self.calendar.is_trading_day(date(2023, 1, 7)))

    def test_get_first_trading_day(self):
        result = self.calendar.get_nth_trading_day_in_month(2023, 1, 1)
        self.assertEqual(result, date(2023, 1, 2))

    def test_get_last_trading_day(self):
        result = self.calendar.get_nth_trading_day_in_month(2023, 1, -1)
        self.assertEqual(result, date(2023, 1, 31))

    def test_set_trading_days(self):
        new_days = make_trading_days(2024, [1])
        self.calendar.set_trading_days(new_days)
        self.assertTrue(self.calendar.is_trading_day(date(2024, 1, 2)))


class TestNoRepeatTrigger(unittest.TestCase):
    """验证 daily/weekly/monthly 不会在同一交易日重复触发"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2])

    def test_daily_no_repeat(self):
        first_day = date(2023, 1, 3)

        result1, _ = should_execute_timer(
            "daily", first_day, MARKET_OPEN_TIME, None, trading_days=self.trading_days
        )
        self.assertTrue(result1)

        result2, _ = should_execute_timer(
            "daily",
            first_day,
            MARKET_OPEN_TIME,
            first_day,
            trading_days=self.trading_days,
        )
        self.assertFalse(result2)

    def test_weekly_no_repeat_same_day(self):
        monday = date(2023, 1, 2)

        result1, _ = should_execute_timer(
            "weekly",
            monday,
            MARKET_OPEN_TIME,
            None,
            weekday=1,
            trading_days=self.trading_days,
        )
        self.assertTrue(result1)

        result2, _ = should_execute_timer(
            "weekly",
            monday,
            MARKET_OPEN_TIME,
            monday,
            weekday=1,
            trading_days=self.trading_days,
        )
        self.assertFalse(result2)

    def test_monthly_no_repeat_same_month(self):
        first_day = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        second_day = get_nth_trading_day_in_month(1, 2023, 2, self.trading_days)

        result1, _ = should_execute_timer(
            "monthly",
            first_day,
            MARKET_OPEN_TIME,
            None,
            day=1,
            trading_days=self.trading_days,
        )
        self.assertTrue(result1)

        result2, _ = should_execute_timer(
            "monthly",
            second_day,
            MARKET_OPEN_TIME,
            first_day,
            day=1,
            trading_days=self.trading_days,
        )
        self.assertFalse(result2)


class TestBarResolutionDegradation(unittest.TestCase):
    """测试 bar 粒度不足时的降级处理"""

    def test_coarse_bar_resolution_warning(self):
        import warnings

        coarse_resolution = 30
        target_time = time(10, 30)
        bar_time = time(10, 0)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = check_bar_time_match(
                bar_time,
                "absolute",
                target_time,
                bar_resolution_minutes=coarse_resolution,
                rule_str="10:30",
            )
            self.assertTrue(len(w) > 0 or result)


class TestEdgeCases(unittest.TestCase):
    """边界值和特殊场景测试"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2, 3, 12])

    def test_open_time_edge_09_29(self):
        """测试 09:29 在 1 分钟容忍度下匹配 open 规则"""
        result = check_bar_time_match(
            time(9, 29), "open", MARKET_OPEN_TIME, bar_resolution_minutes=1
        )
        self.assertTrue(result)

    def test_open_time_edge_09_31(self):
        """测试 09:31 在 1 分钟容忍度下匹配 open 规则"""
        result = check_bar_time_match(
            time(9, 31), "open", MARKET_OPEN_TIME, bar_resolution_minutes=1
        )
        self.assertTrue(result)

    def test_open_time_edge_09_28_not_match(self):
        """测试 09:28 不匹配 open 规则（超出容忍度）"""
        result = check_bar_time_match(
            time(9, 28), "open", MARKET_OPEN_TIME, bar_resolution_minutes=1
        )
        self.assertFalse(result)

    def test_open_time_edge_09_32_not_match(self):
        """测试 09:32 不匹配 open 规则（超出容忍度）"""
        result = check_bar_time_match(
            time(9, 32), "open", MARKET_OPEN_TIME, bar_resolution_minutes=1
        )
        self.assertFalse(result)

    def test_open_time_with_coarse_resolution(self):
        """测试粗粒度下 09:31 匹配 open"""
        result = check_bar_time_match(
            time(9, 31), "open", MARKET_OPEN_TIME, bar_resolution_minutes=2
        )
        self.assertTrue(result)

    def test_midnight_time_handling(self):
        """测试午夜时间（00:00）处理"""
        result = check_bar_time_match(time(0, 0), "open", MARKET_OPEN_TIME)
        self.assertFalse(result)

    def test_before_open_edge_09_29(self):
        """测试 09:29 属于 before_open"""
        result = check_bar_time_match(time(9, 29), "before_open", None)
        self.assertTrue(result)

    def test_after_close_edge_15_01(self):
        """测试 15:01 属于 after_close"""
        result = check_bar_time_match(time(15, 1), "after_close", MARKET_CLOSE_TIME)
        self.assertTrue(result)

    def test_after_close_edge_14_59(self):
        """测试 14:59 在 1 分钟容忍度下匹配 after_close"""
        result = check_bar_time_match(
            time(14, 59), "after_close", MARKET_CLOSE_TIME, bar_resolution_minutes=1
        )
        self.assertTrue(result)

    def test_after_close_edge_14_58_not_match(self):
        """测试 14:58 不匹配 after_close（超出容忍度）"""
        result = check_bar_time_match(
            time(14, 58), "after_close", MARKET_CLOSE_TIME, bar_resolution_minutes=1
        )
        self.assertFalse(result)

    def test_monthly_cross_year(self):
        """测试跨年 monthly 触发"""
        dec_first = get_nth_trading_day_in_month(12, 2023, 1, self.trading_days)
        jan_first = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        result, _ = should_execute_timer(
            "monthly",
            dec_first,
            MARKET_OPEN_TIME,
            jan_first,
            day=1,
            trading_days=self.trading_days,
        )
        self.assertTrue(result)

    def test_monthly_same_year_different_month(self):
        """测试同年不同月的 monthly"""
        jan_first = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        feb_first = get_nth_trading_day_in_month(2, 2023, 1, self.trading_days)
        result, _ = should_execute_timer(
            "monthly",
            feb_first,
            MARKET_OPEN_TIME,
            jan_first,
            day=1,
            trading_days=self.trading_days,
        )
        self.assertTrue(result)


class TestTimeOffsetRules(unittest.TestCase):
    """时间偏移规则测试"""

    def test_open_plus_0m(self):
        """测试 open+0m 等于 open"""
        rule_type, target_time, offset = parse_time_rule("open+0m")
        self.assertEqual(target_time, MARKET_OPEN_TIME)
        self.assertEqual(offset, 0)

    def test_open_plus_240m(self):
        """测试 open+240m = 13:30"""
        rule_type, target_time, offset = parse_time_rule("open+240m")
        self.assertEqual(target_time, time(13, 30))
        self.assertEqual(offset, 240)

    def test_close_plus_30m(self):
        """测试 close+30m = 15:30"""
        rule_type, target_time, offset = parse_time_rule("close+30m")
        self.assertEqual(target_time, time(15, 30))
        self.assertEqual(offset, 30)

    def test_open_minus_30m(self):
        """测试 open-30m = 09:00"""
        rule_type, target_time, offset = parse_time_rule("open-30m")
        self.assertEqual(target_time, time(9, 0))
        self.assertEqual(offset, -30)

    def test_offset_time_match(self):
        """测试偏移时间匹配"""
        result = check_bar_time_match(time(10, 0), "open_offset", time(10, 0))
        self.assertTrue(result)

    def test_offset_time_near_match(self):
        """测试偏移时间容差匹配"""
        result = check_bar_time_match(
            time(10, 1), "open_offset", time(10, 0), bar_resolution_minutes=2
        )
        self.assertTrue(result)


class TestInvalidInputs(unittest.TestCase):
    """无效输入测试"""

    def test_parse_invalid_time_format(self):
        """测试无效时间格式"""
        with self.assertWarns(UserWarning):
            rule_type, target_time, offset = parse_time_rule("invalid_time")
        self.assertEqual(rule_type, "open")

    def test_parse_empty_string(self):
        """测试空字符串"""
        with self.assertWarns(UserWarning):
            rule_type, target_time, offset = parse_time_rule("")
        self.assertEqual(rule_type, "open")

    def test_get_nth_trading_day_out_of_range(self):
        """测试超出范围的交易日索引"""
        trading_days = make_trading_days(2023, [1])
        result = get_nth_trading_day_in_month(1, 2023, 100, trading_days)
        self.assertIsNone(result)

    def test_get_nth_trading_day_negative_out_of_range(self):
        """测试负索引超出范围"""
        trading_days = make_trading_days(2023, [1])
        result = get_nth_trading_day_in_month(1, 2023, -100, trading_days)
        self.assertIsNone(result)

    def test_unknown_frequency(self):
        """测试未知频率"""
        result, reason = should_execute_timer(
            "unknown", date(2023, 1, 2), MARKET_OPEN_TIME, None
        )
        self.assertFalse(result)
        self.assertIn("unknown_frequency", reason)


class TestWeeklyEdgeCases(unittest.TestCase):
    """Weekly 定时器边界测试"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2])

    def test_all_weekdays(self):
        """测试所有工作日"""
        for weekday in range(1, 6):
            matching_day = [d for d in self.trading_days if d.weekday() + 1 == weekday][
                0
            ]
            result, _ = should_execute_timer(
                "weekly",
                matching_day,
                MARKET_OPEN_TIME,
                None,
                weekday=weekday,
                trading_days=self.trading_days,
            )
            self.assertTrue(result, f"Weekday {weekday} should trigger")

    def test_weekly_monday_to_friday_sequence(self):
        """测试周一到周五的序列"""
        week_days = [d for d in self.trading_days if d.weekday() == 0][:1]
        week_days += [d for d in self.trading_days if d.weekday() == 1][:1]
        result1, _ = should_execute_timer(
            "weekly",
            week_days[0],
            MARKET_OPEN_TIME,
            None,
            weekday=1,
            trading_days=self.trading_days,
        )
        self.assertTrue(result1)
        result2, _ = should_execute_timer(
            "weekly",
            week_days[1],
            MARKET_OPEN_TIME,
            week_days[0],
            weekday=1,
            trading_days=self.trading_days,
        )
        self.assertFalse(result2)

    def test_weekly_skip_week(self):
        """测试跳过一周"""
        mondays = [d for d in self.trading_days if d.weekday() == 0][:2]
        result, _ = should_execute_timer(
            "weekly",
            mondays[1],
            MARKET_OPEN_TIME,
            mondays[0],
            weekday=1,
            trading_days=self.trading_days,
        )
        self.assertTrue(result)


class TestMonthlyEdgeCases(unittest.TestCase):
    """Monthly 定时器边界测试"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2, 3, 4, 5, 6])

    def test_monthly_last_day_each_month(self):
        """测试每月最后一个交易日"""
        for month in [1, 2, 3]:
            last_day = get_nth_trading_day_in_month(month, 2023, -1, self.trading_days)
            result, _ = should_execute_timer(
                "monthly",
                last_day,
                MARKET_OPEN_TIME,
                None,
                day=-1,
                trading_days=self.trading_days,
            )
            self.assertTrue(result, f"Month {month} last day should trigger")

    def test_monthly_second_last_day(self):
        """测试倒数第二个交易日"""
        second_last = get_nth_trading_day_in_month(1, 2023, -2, self.trading_days)
        result, _ = should_execute_timer(
            "monthly",
            second_last,
            MARKET_OPEN_TIME,
            None,
            day=-2,
            trading_days=self.trading_days,
        )
        self.assertTrue(result)

    def test_monthly_first_3_days(self):
        """测试前三个交易日"""
        for n in [1, 2, 3]:
            nth_day = get_nth_trading_day_in_month(1, 2023, n, self.trading_days)
            result, _ = should_execute_timer(
                "monthly",
                nth_day,
                MARKET_OPEN_TIME,
                None,
                day=n,
                trading_days=self.trading_days,
            )
            self.assertTrue(result, f"Day {n} should trigger")


class TestNoTradingDaysCalendar(unittest.TestCase):
    """无交易日历时的降级行为测试"""

    def test_is_trading_day_without_calendar(self):
        """测试无日历时的工作日判断"""
        self.assertTrue(is_trading_day(date(2023, 1, 2), None))
        self.assertFalse(is_trading_day(date(2023, 1, 7), None))
        self.assertFalse(is_trading_day(date(2023, 1, 8), None))

    def test_get_nth_without_calendar(self):
        """测试无日历时获取第N个交易日"""
        result = get_nth_trading_day_in_month(1, 2023, 1, None)
        self.assertEqual(result, date(2023, 1, 2))

    def test_monthly_without_calendar(self):
        """测试无日历时的 monthly 触发"""
        result, _ = should_execute_timer(
            "monthly",
            date(2023, 1, 2),
            MARKET_OPEN_TIME,
            None,
            day=1,
            trading_days=None,
        )
        self.assertTrue(result)


class TestTradingDayCalendarCache(unittest.TestCase):
    """交易日历缓存行为测试"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2])
        self.calendar = TradingDayCalendar(self.trading_days)

    def test_month_cache_hit(self):
        """测试月缓存命中"""
        first_call = self.calendar.get_nth_trading_day_in_month(2023, 1, 1)
        second_call = self.calendar.get_nth_trading_day_in_month(2023, 1, 1)
        self.assertEqual(first_call, second_call)
        self.assertEqual(first_call, date(2023, 1, 2))

    def test_clear_cache_on_set(self):
        """测试设置新交易日历时清除缓存"""
        self.calendar.get_nth_trading_day_in_month(2023, 1, 1)
        new_days = make_trading_days(2024, [1])
        self.calendar.set_trading_days(new_days)
        result = self.calendar.get_nth_trading_day_in_month(2024, 1, 1)
        self.assertEqual(result, date(2024, 1, 1))


class TestMultipleConditions(unittest.TestCase):
    """多条件组合测试"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2, 3])

    def test_weekly_with_time_rule(self):
        """测试 weekly + 时间规则组合"""
        monday = [d for d in self.trading_days if d.weekday() == 0][0]
        result1, _ = should_execute_timer(
            "weekly",
            monday,
            MARKET_OPEN_TIME,
            None,
            weekday=1,
            time_rule="open",
            trading_days=self.trading_days,
        )
        self.assertTrue(result1)
        result2, _ = should_execute_timer(
            "weekly",
            monday,
            time(10, 0),
            None,
            weekday=1,
            time_rule="open",
            trading_days=self.trading_days,
        )
        self.assertFalse(result2)

    def test_monthly_with_time_rule(self):
        """测试 monthly + 时间规则组合"""
        first_day = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        result1, _ = should_execute_timer(
            "monthly",
            first_day,
            MARKET_OPEN_TIME,
            None,
            day=1,
            time_rule="open",
            trading_days=self.trading_days,
        )
        self.assertTrue(result1)
        result2, _ = should_execute_timer(
            "monthly",
            first_day,
            time(14, 0),
            None,
            day=1,
            time_rule="after_close",
            trading_days=self.trading_days,
        )
        self.assertFalse(result2)

    def test_daily_with_multiple_time_rules(self):
        """测试 daily 不同时间规则"""
        first_day = date(2023, 1, 2)
        for rule, expected_time in [
            ("open", MARKET_OPEN_TIME),
            ("after_close", MARKET_CLOSE_TIME),
            ("10:30", time(10, 30)),
        ]:
            result, _ = should_execute_timer(
                "daily",
                first_day,
                expected_time,
                None,
                time_rule=rule,
                trading_days=self.trading_days,
            )
            self.assertTrue(result, f"Rule {rule} should match")


class TestYearTransition(unittest.TestCase):
    """年末年初场景测试"""

    def setUp(self):
        self.trading_days = make_trading_days(2022, [12]) + make_trading_days(2023, [1])

    def test_monthly_dec_to_jan(self):
        """测试 12 月到 1 月的 monthly"""
        dec_last = get_nth_trading_day_in_month(12, 2022, -1, self.trading_days)
        jan_first = get_nth_trading_day_in_month(1, 2023, 1, self.trading_days)
        result, _ = should_execute_timer(
            "monthly",
            jan_first,
            MARKET_OPEN_TIME,
            dec_last,
            day=1,
            trading_days=self.trading_days,
        )
        self.assertTrue(result)

    def test_weekly_cross_year(self):
        """测试跨年的 weekly"""
        dec_mondays = [
            d for d in self.trading_days if d.year == 2022 and d.weekday() == 0
        ]
        jan_mondays = [
            d for d in self.trading_days if d.year == 2023 and d.weekday() == 0
        ]
        if dec_mondays and jan_mondays:
            result, _ = should_execute_timer(
                "weekly",
                jan_mondays[0],
                MARKET_OPEN_TIME,
                dec_mondays[-1],
                weekday=1,
                trading_days=self.trading_days,
            )
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
