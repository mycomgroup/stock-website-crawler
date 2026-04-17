"""
test_timer_manager.py
定时器管理器单元测试

测试场景覆盖:
1. TimerManager 初始化
2. 定时器注册
3. 执行判断逻辑 (daily/weekly/monthly)
4. 时间规则匹配
5. 交易日计算
6. 边界情况
"""

import sys
import types
import importlib.util
import pytest
from pathlib import Path
from datetime import datetime, date, time, timedelta
from unittest.mock import MagicMock

project_root = Path(__file__).parent.parent.parent.parent

# 直接加载模块，绕过 jk2bt.__init__.py 的复杂导入链
_timer_spec = importlib.util.spec_from_file_location(
    "timer_manager", str(project_root / "jk2bt/engine/timer_manager.py")
)
_timer_mod = importlib.util.module_from_spec(_timer_spec)
sys.modules["jk2bt.engine.timer_manager"] = _timer_mod
_timer_spec.loader.exec_module(_timer_mod)

TimerManager = _timer_mod.TimerManager


class TestTimerManagerInit:
    """测试 TimerManager 初始化"""

    def test_init_basic(self):
        strategy = MagicMock()
        manager = TimerManager(strategy)
        assert manager._strategy == strategy
        assert manager._timers == []
        assert manager._bar_resolution_minutes == 1
        assert manager._data_frequency == "daily"

    def test_init_with_trading_days(self):
        strategy = MagicMock()
        trading_days = [date(2023, 1, 1), date(2023, 1, 2)]
        manager = TimerManager(strategy, trading_days=trading_days)
        assert manager._trading_days == trading_days


class TestTimerManagerRegister:
    """测试定时器注册"""

    @pytest.fixture
    def manager(self):
        strategy = MagicMock()
        return TimerManager(strategy)

    def test_register_daily(self, manager):
        func = MagicMock()
        manager.register(func, "daily", time_rule="open")
        assert len(manager._timers) == 1
        assert manager._timers[0]["frequency"] == "daily"
        assert manager._timers[0]["time_rule"] == "open"

    def test_register_weekly(self, manager):
        func = MagicMock()
        manager.register(func, "weekly", weekday=3)
        assert len(manager._timers) == 1
        assert manager._timers[0]["frequency"] == "weekly"
        assert manager._timers[0]["weekday"] == 3

    def test_register_monthly(self, manager):
        func = MagicMock()
        manager.register(func, "monthly", day=1)
        assert len(manager._timers) == 1
        assert manager._timers[0]["frequency"] == "monthly"
        assert manager._timers[0]["day"] == 1

    def test_register_default_time_rule(self, manager):
        func = MagicMock()
        manager.register(func, "daily")
        assert manager._timers[0]["time_rule"] == "open"

    def test_register_multiple(self, manager):
        manager.register(MagicMock(), "daily")
        manager.register(MagicMock(), "weekly")
        manager.register(MagicMock(), "monthly")
        assert len(manager._timers) == 3

    def test_register_timer_has_last_executed_none(self, manager):
        manager.register(MagicMock(), "daily")
        assert manager._timers[0]["last_executed"] is None
        assert manager._timers[0]["last_executed_date"] is None


class TestTimerManagerSettings:
    """测试设置方法"""

    @pytest.fixture
    def manager(self):
        strategy = MagicMock()
        return TimerManager(strategy)

    def test_set_trading_days(self, manager):
        trading_days = [date(2023, 1, 1), date(2023, 1, 2)]
        manager.set_trading_days(trading_days)
        assert manager._trading_days == trading_days

    def test_set_bar_resolution(self, manager):
        manager.set_bar_resolution(5)
        assert manager._bar_resolution_minutes == 5

    def test_set_bar_resolution_minimum_is_1(self, manager):
        manager.set_bar_resolution(-1)
        assert manager._bar_resolution_minutes == 1

    def test_set_data_frequency_daily(self, manager):
        manager.set_data_frequency("daily")
        assert manager._data_frequency == "daily"
        assert manager._bar_resolution_minutes == 390

    def test_set_data_frequency_1m(self, manager):
        manager.set_data_frequency("1m")
        assert manager._bar_resolution_minutes == 1

    def test_set_data_frequency_5m(self, manager):
        manager.set_data_frequency("5m")
        assert manager._bar_resolution_minutes == 5

    def test_set_data_frequency_15m(self, manager):
        manager.set_data_frequency("15m")
        assert manager._bar_resolution_minutes == 15

    def test_set_data_frequency_30m(self, manager):
        manager.set_data_frequency("30m")
        assert manager._bar_resolution_minutes == 30

    def test_set_data_frequency_60m(self, manager):
        manager.set_data_frequency("60m")
        assert manager._bar_resolution_minutes == 60

    def test_set_data_frequency_unknown_defaults_to_1(self, manager):
        manager.set_data_frequency("unknown")
        assert manager._bar_resolution_minutes == 1

    def test_reset_clears_all_timers(self, manager):
        manager.register(MagicMock(), "daily")
        manager.register(MagicMock(), "weekly")
        manager.reset()
        assert len(manager._timers) == 0


class TestShouldExecute:
    """测试执行判断逻辑"""

    @pytest.fixture
    def manager(self):
        strategy = MagicMock()
        return TimerManager(strategy)

    def test_every_bar_weekday_executes(self, manager):
        timer = {"time_rule": "every_bar", "frequency": "daily"}
        monday = date(2023, 1, 2)  # Monday
        result, reason = manager._should_execute(timer, monday)
        assert result is True
        assert reason == "every_bar"

    def test_every_bar_weekend_does_not_execute(self, manager):
        timer = {"time_rule": "every_bar", "frequency": "daily"}
        saturday = date(2023, 1, 7)  # Saturday
        result, reason = manager._should_execute(timer, saturday)
        assert result is False
        assert reason == "weekend"

    def test_daily_first_execution(self, manager):
        timer = {
            "frequency": "daily",
            "time_rule": "open",
            "last_executed_date": None,
        }
        monday = date(2023, 1, 2)
        result, reason = manager._should_execute(timer, monday)
        assert result is True
        assert reason == "first_execution"

    def test_daily_already_executed_same_day(self, manager):
        timer = {
            "frequency": "daily",
            "time_rule": "open",
            "last_executed_date": date(2023, 1, 2),
        }
        result, reason = manager._should_execute(timer, date(2023, 1, 2))
        assert result is False
        assert reason == "same_day"

    def test_daily_next_day_executes(self, manager):
        timer = {
            "frequency": "daily",
            "time_rule": "open",
            "last_executed_date": date(2023, 1, 2),
        }
        result, reason = manager._should_execute(timer, date(2023, 1, 3))
        assert result is True
        assert reason == "next_trading_day"

    def test_weekly_correct_weekday_different_week(self, manager):
        timer = {
            "frequency": "weekly",
            "time_rule": "open",
            "weekday": 1,  # Monday
            "last_executed_date": date(2022, 12, 26),  # Previous Monday
        }
        monday = date(2023, 1, 2)  # Monday
        result, reason = manager._should_execute(timer, monday)
        assert result is True
        assert reason == "target_weekday"

    def test_weekly_wrong_weekday(self, manager):
        timer = {
            "frequency": "weekly",
            "time_rule": "open",
            "weekday": 1,  # Monday
            "last_executed_date": None,
        }
        tuesday = date(2023, 1, 3)  # Tuesday
        result, reason = manager._should_execute(timer, tuesday)
        assert result is False
        assert reason == "not_target_weekday"

    def test_weekly_same_week_different_day(self, manager):
        timer = {
            "frequency": "weekly",
            "time_rule": "open",
            "weekday": 2,  # Tuesday
            "last_executed_date": date(2023, 1, 3),
        }
        # Same week, different day (Wednesday)
        result, reason = manager._should_execute(timer, date(2023, 1, 4))
        assert result is False
        assert reason == "not_target_weekday"

    def test_monthly_first_trading_day(self, manager):
        timer = {
            "frequency": "monthly",
            "time_rule": "open",
            "day": 1,
            "last_executed_date": date(2022, 12, 1),
        }
        jan2 = date(2023, 1, 2)  # First weekday of Jan 2023
        result, reason = manager._should_execute(timer, jan2)
        assert result is True

    def test_monthly_same_month_does_not_execute(self, manager):
        timer = {
            "frequency": "monthly",
            "time_rule": "open",
            "day": 1,
            "last_executed_date": date(2023, 1, 3),
        }
        result, reason = manager._should_execute(timer, date(2023, 1, 10))
        assert result is False
        assert reason == "same_month"

    def test_weekend_daily_does_not_execute(self, manager):
        timer = {"frequency": "daily", "time_rule": "open", "last_executed_date": None}
        saturday = date(2023, 1, 7)
        result, reason = manager._should_execute(timer, saturday)
        assert result is False
        assert reason == "weekend"


class TestCheckTimeRule:
    """测试时间规则匹配"""

    @pytest.fixture
    def manager(self):
        strategy = MagicMock()
        return TimerManager(strategy)

    def test_bar_time_none_always_true(self, manager):
        assert manager._check_time_rule(None, "open") is True

    def test_before_open_early(self, manager):
        assert manager._check_time_rule(time(9, 0), "before_open") is True

    def test_before_open_after_market_open(self, manager):
        assert manager._check_time_rule(time(10, 0), "before_open") is False

    def test_open_exact_time(self, manager):
        manager._bar_resolution_minutes = 1
        assert manager._check_time_rule(time(9, 30), "open") is True

    def test_open_outside_window(self, manager):
        manager._bar_resolution_minutes = 1
        assert manager._check_time_rule(time(10, 0), "open") is False

    def test_after_close_at_close(self, manager):
        manager._bar_resolution_minutes = 1
        assert manager._check_time_rule(time(15, 0), "after_close") is True

    def test_after_close_before_close(self, manager):
        manager._bar_resolution_minutes = 1
        assert manager._check_time_rule(time(14, 0), "after_close") is False

    def test_specific_time_match(self, manager):
        manager._bar_resolution_minutes = 1
        assert manager._check_time_rule(time(10, 30), "10:30") is True

    def test_specific_time_mismatch(self, manager):
        manager._bar_resolution_minutes = 1
        assert manager._check_time_rule(time(14, 0), "10:30") is False

    def test_open_plus_offset(self, manager):
        manager._bar_resolution_minutes = 5
        assert manager._check_time_rule(time(9, 35), "open+5m") is True

    def test_open_minus_offset(self, manager):
        manager._bar_resolution_minutes = 5
        assert manager._check_time_rule(time(9, 25), "open-5m") is True

    def test_invalid_time_format_returns_true(self, manager):
        assert manager._check_time_rule(time(9, 30), "invalid") is True


class TestGetNthTradingDay:
    """测试获取第N个交易日"""

    @pytest.fixture
    def manager(self):
        strategy = MagicMock()
        return TimerManager(strategy)

    def test_first_trading_day_jan_2023(self, manager):
        # Jan 1, 2023 is Sunday, first weekday is Jan 2
        result = manager._get_nth_trading_day(2023, 1, 1)
        assert result == date(2023, 1, 2)

    def test_last_trading_day_jan_2023(self, manager):
        result = manager._get_nth_trading_day(2023, 1, -1)
        assert result == date(2023, 1, 31)

    def test_second_trading_day(self, manager):
        result = manager._get_nth_trading_day(2023, 1, 2)
        assert result == date(2023, 1, 3)

    def test_n_zero_returns_first(self, manager):
        result = manager._get_nth_trading_day(2023, 1, 0)
        assert result == date(2023, 1, 2)

    def test_n_out_of_range_positive_returns_last(self, manager):
        result = manager._get_nth_trading_day(2023, 1, 100)
        assert result == date(2023, 1, 31)

    def test_n_out_of_range_negative_returns_first(self, manager):
        result = manager._get_nth_trading_day(2023, 1, -100)
        assert result == date(2023, 1, 2)


class TestIsFirstTradingDayOfMonth:
    """测试第一个交易日判断"""

    @pytest.fixture
    def manager(self):
        strategy = MagicMock()
        return TimerManager(strategy)

    def test_first_weekday_of_month(self, manager):
        jan2 = date(2023, 1, 2)  # Monday, first weekday
        assert manager._is_first_trading_day_of_month(jan2) is True

    def test_late_in_month(self, manager):
        jan20 = date(2023, 1, 20)
        assert manager._is_first_trading_day_of_month(jan20) is False


class TestCheckAndExecute:
    """测试检查并执行"""

    def test_check_and_execute_calls_callback(self):
        strategy = MagicMock()
        strategy.datetime.date.return_value = date(2023, 1, 2)
        strategy.datetime.datetime.return_value = datetime(2023, 1, 2, 9, 30)
        strategy.context = MagicMock()
        strategy.log = MagicMock()

        manager = TimerManager(strategy)
        callback = MagicMock()
        manager.register(callback, "daily", time_rule="open")

        manager.check_and_execute()
        callback.assert_called_once_with(strategy.context)

    def test_check_and_execute_handles_errors(self):
        strategy = MagicMock()
        strategy.datetime.date.return_value = date(2023, 1, 2)
        strategy.datetime.datetime.return_value = datetime(2023, 1, 2, 9, 30)
        strategy.context = MagicMock()
        strategy.log = MagicMock()

        manager = TimerManager(strategy)

        def failing_func(ctx):
            raise ValueError("Test error")

        manager.register(failing_func, "daily", time_rule="open")
        manager.check_and_execute()

        assert strategy.log.called

    def test_check_and_execute_no_timers(self):
        strategy = MagicMock()
        strategy.datetime.date.return_value = date(2023, 1, 2)
        strategy.datetime.datetime.return_value = datetime(2023, 1, 2, 9, 30)

        manager = TimerManager(strategy)
        manager.check_and_execute()  # Should not raise
