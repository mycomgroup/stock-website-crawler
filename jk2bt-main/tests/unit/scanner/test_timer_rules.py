"""
Tests for jk2bt/scanner/timer_rules.py - Timer Rules Engine
"""

import pytest
from datetime import date, time, timedelta
from unittest.mock import patch, MagicMock
from jk2bt.scanner.timer_rules import (
    parse_time_rule,
    check_bar_time_match,
    is_trading_day,
    check_daily_trigger,
    check_weekly_trigger,
    check_monthly_trigger,
    should_execute_timer,
    TradingDayCalendar,
    get_nth_trading_day_in_month,
    MARKET_OPEN_TIME,
    MARKET_CLOSE_TIME,
)


class TestParseTimeRule:
    """Test parse_time_rule function"""

    def test_parse_none(self):
        rule_type, target_time, offset = parse_time_rule(None)
        assert rule_type == "open"
        assert target_time == MARKET_OPEN_TIME

    def test_parse_before_open(self):
        rule_type, target_time, offset = parse_time_rule("before_open")
        assert rule_type == "before_open"

    def test_parse_open(self):
        rule_type, target_time, offset = parse_time_rule("open")
        assert rule_type == "open"
        assert target_time == MARKET_OPEN_TIME

    def test_parse_after_close(self):
        rule_type, target_time, offset = parse_time_rule("after_close")
        assert rule_type == "after_close"
        assert target_time == MARKET_CLOSE_TIME

    def test_parse_absolute_time(self):
        rule_type, target_time, offset = parse_time_rule("14:30")
        assert rule_type == "absolute"
        assert target_time == time(14, 30)

    def test_parse_open_offset(self):
        rule_type, target_time, offset = parse_time_rule("open+30m")
        assert rule_type == "open_offset"
        assert offset == 30

    def test_parse_close_offset(self):
        rule_type, target_time, offset = parse_time_rule("close-15min")
        assert rule_type == "close_offset"
        assert offset == -15

    def test_parse_market_open(self):
        rule_type, target_time, offset = parse_time_rule("market_open")
        assert rule_type == "market_open"

    def test_parse_market_close(self):
        rule_type, target_time, offset = parse_time_rule("market_close")
        assert rule_type == "market_close"


class TestCheckBarTimeMatch:
    """Test check_bar_time_match function"""

    def test_every_bar_always_matches(self):
        assert check_bar_time_match(time(10, 0), "every_bar", None) is True

    def test_intraday_within_market_hours(self):
        assert check_bar_time_match(time(10, 0), "intraday", None) is True
        assert check_bar_time_match(time(9, 0), "intraday", None) is False
        assert check_bar_time_match(time(16, 0), "intraday", None) is False

    def test_before_open(self):
        assert check_bar_time_match(time(9, 0), "before_open", None) is True
        assert check_bar_time_match(time(9, 30), "before_open", None) is False

    def test_open_time_match(self):
        assert check_bar_time_match(time(9, 30), "open", MARKET_OPEN_TIME) is True
        assert (
            check_bar_time_match(
                time(9, 31), "open", MARKET_OPEN_TIME, bar_resolution_minutes=1
            )
            is True
        )

    def test_after_close_time_match(self):
        assert (
            check_bar_time_match(time(15, 0), "after_close", MARKET_CLOSE_TIME) is True
        )
        assert (
            check_bar_time_match(time(15, 1), "after_close", MARKET_CLOSE_TIME) is True
        )

    def test_absolute_time_match(self):
        target = time(14, 30)
        assert check_bar_time_match(time(14, 30), "absolute", target) is True
        assert (
            check_bar_time_match(
                time(14, 31), "absolute", target, bar_resolution_minutes=1
            )
            is True
        )

    def test_open_offset(self):
        target = time(10, 0)
        assert check_bar_time_match(time(10, 0), "open_offset", target) is True


class TestTradingDayCalendar:
    """Test TradingDayCalendar class"""

    def test_set_trading_days(self):
        calendar = TradingDayCalendar()
        test_days = [
            date(2024, 1, 2),
            date(2024, 1, 3),
            date(2024, 1, 4),
        ]
        calendar.set_trading_days(test_days)

        assert calendar.is_trading_day(date(2024, 1, 2)) is True
        assert calendar.is_trading_day(date(2024, 1, 1)) is False

    def test_get_nth_trading_day_in_month(self):
        calendar = TradingDayCalendar()
        calendar.set_trading_days(
            [
                date(2024, 1, 2),
                date(2024, 1, 3),
                date(2024, 1, 4),
                date(2024, 1, 5),
            ]
        )

        first = calendar.get_nth_trading_day_in_month(2024, 1, 1)
        assert first == date(2024, 1, 2)

        last = calendar.get_nth_trading_day_in_month(2024, 1, -1)
        assert last == date(2024, 1, 5)

    def test_get_first_trading_day_of_month(self):
        calendar = TradingDayCalendar()
        calendar.set_trading_days([date(2024, 1, 2), date(2024, 1, 5)])

        first = calendar.get_first_trading_day_of_month(2024, 1)
        assert first == date(2024, 1, 2)

    def test_get_last_trading_day_of_month(self):
        calendar = TradingDayCalendar()
        calendar.set_trading_days([date(2024, 1, 2), date(2024, 1, 5)])

        last = calendar.get_last_trading_day_of_month(2024, 1)
        assert last == date(2024, 1, 5)

    def test_is_first_trading_day_of_month(self):
        calendar = TradingDayCalendar()
        calendar.set_trading_days([date(2024, 1, 2), date(2024, 1, 3)])

        assert calendar.is_first_trading_day_of_month(date(2024, 1, 2)) is True
        assert calendar.is_first_trading_day_of_month(date(2024, 1, 3)) is False


class TestCheckDailyTrigger:
    """Test check_daily_trigger function"""

    def test_trading_day_triggers(self):
        trading_days = [date(2024, 1, 2), date(2024, 1, 3)]
        assert check_daily_trigger(date(2024, 1, 2), None, trading_days) is True

    def test_non_trading_day_no_trigger(self):
        trading_days = [date(2024, 1, 2)]
        assert check_daily_trigger(date(2024, 1, 1), None, trading_days) is False

    def test_same_day_no_trigger(self):
        trading_days = [date(2024, 1, 2)]
        assert (
            check_daily_trigger(date(2024, 1, 2), date(2024, 1, 2), trading_days)
            is False
        )


class TestCheckWeeklyTrigger:
    """Test check_weekly_trigger function"""

    def test_target_weekday_triggers(self):
        trading_days = [date(2024, 1, 1), date(2024, 1, 8)]
        assert check_weekly_trigger(date(2024, 1, 8), None, 1, trading_days) is True

    def test_wrong_weekday_no_trigger(self):
        trading_days = [date(2024, 1, 2), date(2024, 1, 3)]
        assert check_weekly_trigger(date(2024, 1, 3), None, 1, trading_days) is False

    def test_same_week_no_trigger(self):
        trading_days = [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 8)]
        assert (
            check_weekly_trigger(date(2024, 1, 8), date(2024, 1, 2), 1, trading_days)
            is False
        )


class TestCheckMonthlyTrigger:
    """Test check_monthly_trigger function"""

    def test_first_trading_day_triggers(self):
        trading_days = [date(2024, 1, 2), date(2024, 1, 3)]
        assert check_monthly_trigger(date(2024, 1, 2), None, 1, trading_days) is True

    def test_wrong_day_no_trigger(self):
        trading_days = [date(2024, 1, 2), date(2024, 1, 3)]
        assert check_monthly_trigger(date(2024, 1, 3), None, 1, trading_days) is False

    def test_same_month_no_trigger(self):
        trading_days = [date(2024, 1, 2), date(2024, 2, 1)]
        assert (
            check_monthly_trigger(date(2024, 2, 1), date(2024, 1, 2), 1, trading_days)
            is True
        )
        assert (
            check_monthly_trigger(date(2024, 1, 3), date(2024, 1, 2), 1, trading_days)
            is False
        )


class TestShouldExecuteTimer:
    """Test should_execute_timer function"""

    def test_daily_with_trading_day(self):
        trading_days = [date(2024, 1, 2)]
        should_exec, reason = should_execute_timer(
            "daily",
            date(2024, 1, 2),
            time(9, 30),
            None,
            time_rule="open",
            trading_days=trading_days,
        )
        assert should_exec is True
        assert reason == "triggered"

    def test_weekly_with_target_weekday(self):
        trading_days = [date(2024, 1, 1), date(2024, 1, 8)]
        should_exec, reason = should_execute_timer(
            "weekly", date(2024, 1, 8), None, None, weekday=1, trading_days=trading_days
        )
        assert should_exec is True

    def test_monthly_with_target_day(self):
        trading_days = [date(2024, 1, 2), date(2024, 2, 1)]
        should_exec, reason = should_execute_timer(
            "monthly",
            date(2024, 2, 1),
            None,
            date(2024, 1, 2),
            day=1,
            trading_days=trading_days,
        )
        assert should_exec is True

    def test_unknown_frequency(self):
        should_exec, reason = should_execute_timer(
            "yearly", date(2024, 1, 2), None, None
        )
        assert should_exec is False
        assert "unknown_frequency" in reason


class TestGetNthTradingDayInMonth:
    """Test get_nth_trading_day_in_month function"""

    def test_get_first(self):
        trading_days = [
            date(2024, 1, 1),
            date(2024, 1, 2),
            date(2024, 1, 3),
        ]
        result = get_nth_trading_day_in_month(2024, 1, 1, trading_days)
        assert result == date(2024, 1, 2)

    def test_get_last(self):
        trading_days = [
            date(2024, 1, 1),
            date(2024, 1, 2),
            date(2024, 1, 3),
        ]
        result = get_nth_trading_day_in_month(2024, 1, -1, trading_days)
        assert result == date(2024, 1, 3)

    def test_out_of_range(self):
        trading_days = [date(2024, 1, 2)]
        result = get_nth_trading_day_in_month(2024, 1, 10, trading_days)
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
