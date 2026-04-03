import unittest
import sys
import os
import calendar
import backtrader as bt
import pandas as pd
from datetime import datetime, date, time, timedelta

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src",
    ),
)

from jk2bt.core.strategy_base import (
    JQ2BTBaseStrategy,
    TimerManager,
)


def make_trading_days(year, months):
    trading_days = []
    for month in months:
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            dt = date(year, month, day)
            if dt.weekday() < 5:
                trading_days.append(dt)
    return trading_days


class MockStrategy:
    """模拟策略类用于测试TimerManager"""

    def __init__(self, trading_days=None):
        self._timers_executed = []
        self.context = type("Context", (), {})()
        self._trading_days = trading_days
        self._mock_date = date(2023, 1, 1)
        self._mock_time = time(9, 30)

    def set_mock_datetime(self, dt, dt_time=None):
        self._mock_date = dt
        self._mock_time = dt_time or time(9, 30)

    def log(self, msg):
        pass

    datetime = type(
        "DatetimeProxy",
        (),
        {
            "date": lambda self, idx=0: date(2023, 1, 1),
            "datetime": lambda self, idx=0: datetime(2023, 1, 1, 9, 30),
        },
    )()


class TestTimerManager(unittest.TestCase):
    """TimerManager类测试"""

    def test_register_timer(self):
        """测试定时器注册"""
        manager = TimerManager(MockStrategy())
        callback_called = []

        def callback(context):
            callback_called.append(1)

        manager.register(callback, "daily", "open")
        self.assertEqual(len(manager._timers), 1)
        self.assertEqual(manager._timers[0]["frequency"], "daily")
        self.assertEqual(manager._timers[0]["time_rule"], "open")
        self.assertIsNone(manager._timers[0]["last_executed"])

    def test_register_monthly_timer(self):
        """测试月度定时器注册"""
        manager = TimerManager(MockStrategy())

        def callback(context):
            pass

        manager.register(callback, "monthly", "before_open", day=1)
        self.assertEqual(manager._timers[0]["frequency"], "monthly")
        self.assertEqual(manager._timers[0]["day"], 1)

    def test_register_weekly_timer(self):
        """测试周定时器注册"""
        manager = TimerManager(MockStrategy())

        def callback(context):
            pass

        manager.register(callback, "weekly", "open", weekday=1)
        self.assertEqual(manager._timers[0]["frequency"], "weekly")
        self.assertEqual(manager._timers[0]["weekday"], 1)

    def test_reset_clears_all_timers(self):
        """测试reset清空所有定时器"""
        manager = TimerManager(MockStrategy())

        def callback(context):
            pass

        manager.register(callback, "daily")
        manager.register(callback, "monthly")
        manager.register(callback, "weekly")

        self.assertEqual(len(manager._timers), 3)
        manager.reset()
        self.assertEqual(len(manager._timers), 0)

    def test_should_execute_first_time(self):
        """测试首次执行判断"""
        manager = TimerManager(MockStrategy())
        timer = {"frequency": "daily", "time_rule": "open", "last_executed_date": None}
        result, reason = manager._should_execute(timer, date(2023, 1, 3))
        self.assertTrue(result)

    def test_should_execute_same_day_not_executed(self):
        """测试同一天不重复执行"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "daily",
            "time_rule": "open",
            "last_executed_date": date(2023, 1, 3),
        }
        result, reason = manager._should_execute(timer, date(2023, 1, 3))
        self.assertFalse(result)

    def test_should_execute_daily_next_day(self):
        """测试daily定时器次日执行"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "daily",
            "time_rule": "open",
            "last_executed_date": date(2023, 1, 3),
        }
        result, reason = manager._should_execute(timer, date(2023, 1, 4))
        self.assertTrue(result)

    def test_should_execute_monthly_same_month(self):
        """测试monthly同月不执行"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "monthly",
            "time_rule": "open",
            "day": 1,
            "last_executed_date": date(2023, 1, 3),
        }
        result, reason = manager._should_execute(timer, date(2023, 1, 15))
        self.assertFalse(result)

    def test_should_execute_monthly_next_month(self):
        """测试monthly下月执行"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "monthly",
            "time_rule": "open",
            "day": 1,
            "last_executed_date": date(2023, 1, 3),
        }
        result, reason = manager._should_execute(timer, date(2023, 2, 1))
        self.assertTrue(result)

    def test_should_execute_weekly_same_week(self):
        """测试weekly同一周不执行"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "weekly",
            "time_rule": "open",
            "weekday": 1,
            "last_executed_date": date(2023, 1, 2),
        }
        result, reason = manager._should_execute(timer, date(2023, 1, 3))
        self.assertFalse(result)

    def test_should_execute_weekly_next_week(self):
        """测试weekly下一周执行"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "weekly",
            "time_rule": "open",
            "weekday": 1,
            "last_executed_date": date(2023, 1, 2),
        }
        result, reason = manager._should_execute(timer, date(2023, 1, 9))
        self.assertTrue(result)


class TestTimerStrategyIntegration(unittest.TestCase):
    """定时器策略集成测试"""

    def create_test_data(self, days=30):
        """创建测试数据（仅交易日）"""
        trading_days = make_trading_days(2023, [1, 2, 3])[:days]
        datetime_series = pd.to_datetime(trading_days)
        df = pd.DataFrame(
            {
                "datetime": datetime_series,
                "open": [10.0] * len(trading_days),
                "high": [10.5] * len(trading_days),
                "low": [9.5] * len(trading_days),
                "close": [10.0] * len(trading_days),
                "volume": [1000] * len(trading_days),
                "openinterest": [0] * len(trading_days),
            }
        )
        return bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name="test_stock",
        )

    def test_run_daily_integration(self):
        """测试run_daily集成"""
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)
        cerebro.adddata(self.create_test_data(5))

        class DailyTestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.daily_count = 0
                self.run_daily(self.daily_callback, time="open")

            def daily_callback(self, context):
                self.daily_count += 1

        cerebro.addstrategy(DailyTestStrategy)
        results = cerebro.run()
        strategy = results[0]

        self.assertEqual(strategy.daily_count, 5)

    def test_run_monthly_integration(self):
        """测试run_monthly集成"""
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)
        cerebro.adddata(self.create_test_data(60))

        class MonthlyTestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.monthly_count = 0
                self.run_monthly(self.monthly_callback, day=1, time="open")

            def monthly_callback(self, context):
                self.monthly_count += 1

        cerebro.addstrategy(MonthlyTestStrategy)
        results = cerebro.run()
        strategy = results[0]

        self.assertEqual(strategy.monthly_count, 3)

    def test_run_weekly_integration(self):
        """测试run_weekly集成"""
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)
        cerebro.adddata(self.create_test_data(21))

        class WeeklyTestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.weekly_count = 0
                self.run_weekly(self.weekly_callback, weekday=1, time="open")

            def weekly_callback(self, context):
                self.weekly_count += 1

        cerebro.addstrategy(WeeklyTestStrategy)
        results = cerebro.run()
        strategy = results[0]

        self.assertGreater(strategy.weekly_count, 0)

    def test_unschedule_all_integration(self):
        """测试unschedule_all集成"""
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)
        cerebro.adddata(self.create_test_data(5))

        class UnscheduleTestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.call_count = 0
                self.run_daily(self.callback, time="open")

            def callback(self, context):
                self.call_count += 1
                if self.call_count == 1:
                    self.unschedule_all()

        cerebro.addstrategy(UnscheduleTestStrategy)
        results = cerebro.run()
        strategy = results[0]

        self.assertEqual(strategy.call_count, 1)

    def test_multiple_timers_integration(self):
        """测试多个定时器同时运行"""
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)
        cerebro.adddata(self.create_test_data(30))

        class MultiTimerStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.daily_count = 0
                self.monthly_count = 0
                self.run_daily(self.daily_callback, time="open")
                self.run_monthly(self.monthly_callback, day=1, time="open")

            def daily_callback(self, context):
                self.daily_count += 1

            def monthly_callback(self, context):
                self.monthly_count += 1

        cerebro.addstrategy(MultiTimerStrategy)
        results = cerebro.run()
        strategy = results[0]

        self.assertEqual(strategy.daily_count, 30)
        self.assertEqual(strategy.monthly_count, 2)

    def test_timer_manager_exists(self):
        """测试timer_manager属性存在"""
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)
        cerebro.adddata(self.create_test_data(5))

        class CheckTimerManager(JQ2BTBaseStrategy):
            def initialize(self):
                self.has_timer_manager = hasattr(self, "timer_manager")
                self.timer_manager_type = type(self.timer_manager).__name__

        cerebro.addstrategy(CheckTimerManager)
        results = cerebro.run()
        strategy = results[0]

        self.assertTrue(strategy.has_timer_manager)
        self.assertEqual(strategy.timer_manager_type, "TimerManager")


class TestTimerTimeRules(unittest.TestCase):
    """时间规则测试"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2])

    def test_time_rule_open_plus_30m(self):
        """测试 open+30m 时间规则"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "daily",
            "time_rule": "open+30m",
            "last_executed_date": None,
        }

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(10, 0))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(9, 30))
        self.assertFalse(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(10, 30))
        self.assertFalse(result)

    def test_time_rule_fixed_hhmm(self):
        """测试固定 HH:MM 时间规则"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "daily",
            "time_rule": "10:30",
            "last_executed_date": None,
        }

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(10, 30))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(10, 0))
        self.assertFalse(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(11, 0))
        self.assertFalse(result)

    def test_time_rule_before_open(self):
        """测试 before_open 时间规则"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "daily",
            "time_rule": "before_open",
            "last_executed_date": None,
        }

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(9, 0))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(9, 25))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(9, 30))
        self.assertFalse(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(10, 0))
        self.assertFalse(result)

    def test_time_rule_after_close(self):
        """测试 after_close 时间规则"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "daily",
            "time_rule": "after_close",
            "last_executed_date": None,
        }

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(15, 0))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(15, 30))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(14, 30))
        self.assertFalse(result)

    def test_time_rule_open_minus_5m(self):
        """测试 open-5m 时间规则"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "daily",
            "time_rule": "open-5m",
            "last_executed_date": None,
        }

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(9, 25))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(9, 30))
        self.assertFalse(result)

    def test_no_repeat_trigger_with_time_rule(self):
        """测试带时间规则的定时器不重复触发"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "daily",
            "time_rule": "10:00",
            "last_executed_date": date(2023, 1, 3),
        }

        result, _ = manager._should_execute(timer, date(2023, 1, 3), time(10, 0))
        self.assertFalse(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 4), time(10, 0))
        self.assertTrue(result)


class TestTimerDayRules(unittest.TestCase):
    """日期规则测试"""

    def setUp(self):
        self.trading_days = make_trading_days(2023, [1, 2, 3])

    def test_monthly_first_trading_day(self):
        """测试月内第一个交易日触发"""
        manager = TimerManager(MockStrategy())
        manager._trading_days = self.trading_days

        timer = {
            "frequency": "monthly",
            "time_rule": "open",
            "day": 1,
            "last_executed_date": None,
        }

        result, _ = manager._should_execute(timer, date(2023, 1, 2))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 3))
        self.assertFalse(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 1))
        self.assertFalse(result)

    def test_monthly_last_trading_day(self):
        """测试月内最后一个交易日触发"""
        manager = TimerManager(MockStrategy())
        manager._trading_days = self.trading_days

        timer = {
            "frequency": "monthly",
            "time_rule": "open",
            "day": -1,
            "last_executed_date": None,
        }

        result, _ = manager._should_execute(timer, date(2023, 1, 31))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer, date(2023, 1, 30))
        self.assertFalse(result)

    def test_weekly_target_weekday(self):
        """测试周几触发"""
        manager = TimerManager(MockStrategy())
        manager._trading_days = self.trading_days

        timer_monday = {
            "frequency": "weekly",
            "time_rule": "open",
            "weekday": 1,
            "last_executed_date": None,
        }

        result, _ = manager._should_execute(timer_monday, date(2023, 1, 2))
        self.assertTrue(result)

        result, _ = manager._should_execute(timer_monday, date(2023, 1, 3))
        self.assertFalse(result)

        timer_friday = {
            "frequency": "weekly",
            "time_rule": "open",
            "weekday": 5,
            "last_executed_date": None,
        }

        result, _ = manager._should_execute(timer_friday, date(2023, 1, 6))
        self.assertTrue(result)

    def test_weekly_same_week_no_repeat(self):
        """测试同一周不重复触发"""
        manager = TimerManager(MockStrategy())
        manager._trading_days = self.trading_days

        timer = {
            "frequency": "weekly",
            "time_rule": "open",
            "weekday": 1,
            "last_executed_date": date(2023, 1, 2),
        }

        result, _ = manager._should_execute(timer, date(2023, 1, 9))
        self.assertTrue(result)

        timer_same_week = {
            "frequency": "weekly",
            "time_rule": "open",
            "weekday": 1,
            "last_executed_date": date(2023, 1, 2),
        }
        result, _ = manager._should_execute(timer_same_week, date(2023, 1, 3))
        self.assertFalse(result)

    def test_weekend_not_trading_day(self):
        """测试周末不是交易日"""
        manager = TimerManager(MockStrategy())
        timer = {
            "frequency": "daily",
            "time_rule": "open",
            "last_executed_date": None,
        }

        saturday = date(2023, 1, 7)
        sunday = date(2023, 1, 8)

        result, _ = manager._should_execute(timer, saturday)
        self.assertFalse(result)

        result, _ = manager._should_execute(timer, sunday)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
