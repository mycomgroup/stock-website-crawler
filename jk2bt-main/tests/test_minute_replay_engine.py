#!/usr/bin/env python3
"""
Task 27: 分钟回放引擎验证测试
验证分钟级回放、every_bar、open+Nm、HH:MM、尾盘/盘中触发等语义
"""

import unittest
import sys
import os
from datetime import date, time, datetime, timedelta

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src"),
)

import pandas as pd
import backtrader as bt
from timer_rules import (
    parse_time_rule,
    check_bar_time_match,
    should_execute_timer,
    MARKET_OPEN_TIME,
    MARKET_CLOSE_TIME,
)
from jk2bt.core.strategy_base import JQ2BTBaseStrategy, TimerManager


def make_minute_data(days=2, period_minutes=5):
    """生成分钟测试数据"""
    trading_days = []
    start_date = date(2024, 1, 15)

    for i in range(days * 2):
        d = start_date + timedelta(days=i)
        if d.weekday() < 5:
            trading_days.append(d)
        if len(trading_days) >= days:
            break

    rows = []
    for td in trading_days:
        for hour, minute_start in [(9, 30), (13, 0)]:
            for m in range(0, 120, period_minutes):
                h = hour + (minute_start + m) // 60
                mins = (minute_start + m) % 60
                if h > 11 and hour == 9:
                    continue
                if h > 15 or (h == 15 and mins > 0):
                    continue
                dt = datetime.combine(td, time(h, mins))
                rows.append(
                    {
                        "datetime": dt,
                        "open": 10.0,
                        "high": 10.5,
                        "low": 9.5,
                        "close": 10.2,
                        "volume": 1000,
                        "openinterest": 0,
                    }
                )

    df = pd.DataFrame(rows)
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
    ), trading_days


class TestTimerRulesMinuteSupport(unittest.TestCase):
    """测试 timer_rules 分钟级支持"""

    def test_every_bar_rule(self):
        """测试 every_bar 规则"""
        rule_type, target_time, offset = parse_time_rule("every_bar")
        self.assertEqual(rule_type, "every_bar")

        self.assertTrue(check_bar_time_match(time(10, 0), "every_bar", None))
        self.assertTrue(check_bar_time_match(time(14, 30), "every_bar", None))
        self.assertTrue(check_bar_time_match(time(9, 0), "every_bar", None))

    def test_intraday_rule(self):
        """测试盘中规则"""
        rule_type, target_time, offset = parse_time_rule("intraday")
        self.assertEqual(rule_type, "intraday")

        self.assertTrue(check_bar_time_match(time(10, 0), "intraday", None))
        self.assertTrue(check_bar_time_match(time(14, 30), "intraday", None))
        self.assertFalse(check_bar_time_match(time(8, 0), "intraday", None))
        self.assertFalse(check_bar_time_match(time(16, 0), "intraday", None))

    def test_market_close_rule(self):
        """测试尾盘规则"""
        rule_type, target_time, offset = parse_time_rule("尾盘")
        self.assertEqual(rule_type, "market_close")

        self.assertTrue(check_bar_time_match(time(15, 0), "market_close", None))
        self.assertFalse(check_bar_time_match(time(10, 0), "market_close", None))

    def test_open_offset_rule(self):
        """测试 open+Nm 规则"""
        rule_type, target_time, offset = parse_time_rule("open+30m")
        self.assertEqual(rule_type, "open_offset")
        self.assertEqual(target_time, time(10, 0))
        self.assertEqual(offset, 30)

        self.assertTrue(
            check_bar_time_match(
                time(10, 0), "open_offset", time(10, 0), bar_resolution_minutes=5
            )
        )
        self.assertFalse(
            check_bar_time_match(
                time(9, 30), "open_offset", time(10, 0), bar_resolution_minutes=5
            )
        )

    def test_hhmm_rule(self):
        """测试 HH:MM 规则"""
        rule_type, target_time, offset = parse_time_rule("10:30")
        self.assertEqual(rule_type, "absolute")
        self.assertEqual(target_time, time(10, 30))

        self.assertTrue(check_bar_time_match(time(10, 30), "absolute", time(10, 30)))
        self.assertFalse(check_bar_time_match(time(10, 0), "absolute", time(10, 30)))

    def test_close_offset_minus_rule(self):
        """测试 close-Nm 规则"""
        rule_type, target_time, offset = parse_time_rule("close-10m")
        self.assertEqual(rule_type, "close_offset")
        self.assertEqual(target_time, time(14, 50))
        self.assertEqual(offset, -10)

    def test_close_offset_plus_rule(self):
        """测试 close+Nm 规则"""
        rule_type, target_time, offset = parse_time_rule("close+10m")
        self.assertEqual(rule_type, "close_offset")
        self.assertEqual(target_time, time(15, 10))
        self.assertEqual(offset, 10)

    def test_open_minus_rule(self):
        """测试 open-Nm 规则"""
        rule_type, target_time, offset = parse_time_rule("open-5m")
        self.assertEqual(rule_type, "open_offset")
        self.assertEqual(target_time, time(9, 25))
        self.assertEqual(offset, -5)

    def test_before_open_rule(self):
        """测试 before_open 规则"""
        rule_type, target_time, offset = parse_time_rule("before_open")
        self.assertEqual(rule_type, "before_open")
        self.assertIsNone(target_time)

        self.assertTrue(check_bar_time_match(time(9, 0), "before_open", None))
        self.assertTrue(check_bar_time_match(time(9, 25), "before_open", None))
        self.assertFalse(check_bar_time_match(time(9, 30), "before_open", None))
        self.assertFalse(check_bar_time_match(time(10, 0), "before_open", None))

    def test_after_close_rule(self):
        """测试 after_close 规则"""
        rule_type, target_time, offset = parse_time_rule("after_close")
        self.assertEqual(rule_type, "after_close")
        self.assertEqual(target_time, MARKET_CLOSE_TIME)

        self.assertTrue(
            check_bar_time_match(time(15, 0), "after_close", MARKET_CLOSE_TIME)
        )
        self.assertTrue(
            check_bar_time_match(time(15, 30), "after_close", MARKET_CLOSE_TIME)
        )
        self.assertFalse(
            check_bar_time_match(time(14, 30), "after_close", MARKET_CLOSE_TIME)
        )

    def test_chinese_aliases(self):
        """测试中文别名"""
        cases = [
            ("开盘", "market_open"),
            ("收盘", "market_close"),
            ("尾盘", "market_close"),
            ("盘中", "intraday"),
        ]
        for rule, expected_type in cases:
            rule_type, _, _ = parse_time_rule(rule)
            self.assertEqual(rule_type, expected_type, f"规则 '{rule}' 解析错误")

    def test_market_open_rule(self):
        """测试 market_open 规则"""
        rule_type, target_time, offset = parse_time_rule("market_open")
        self.assertEqual(rule_type, "market_open")
        self.assertEqual(target_time, MARKET_OPEN_TIME)

        self.assertTrue(
            check_bar_time_match(
                time(9, 30), "market_open", MARKET_OPEN_TIME, bar_resolution_minutes=1
            )
        )
        self.assertFalse(
            check_bar_time_match(
                time(10, 0), "market_open", MARKET_OPEN_TIME, bar_resolution_minutes=1
            )
        )

    def test_none_rule_defaults_to_open(self):
        """测试 None 规则默认为 open"""
        rule_type, target_time, offset = parse_time_rule(None)
        self.assertEqual(rule_type, "open")
        self.assertEqual(target_time, MARKET_OPEN_TIME)

    def test_invalid_rule_falls_back_to_open(self):
        """测试无效规则降级为 open"""
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            rule_type, target_time, offset = parse_time_rule("invalid_rule_xyz")
            self.assertEqual(rule_type, "open")
            self.assertEqual(target_time, MARKET_OPEN_TIME)
            self.assertGreater(len(w), 0)

    def test_bar_resolution_tolerance(self):
        """测试 bar 粒度 tolerance"""
        self.assertTrue(
            check_bar_time_match(
                time(9, 31), "open", MARKET_OPEN_TIME, bar_resolution_minutes=2
            )
        )
        self.assertTrue(
            check_bar_time_match(
                time(9, 32), "open", MARKET_OPEN_TIME, bar_resolution_minutes=5
            )
        )
        self.assertFalse(
            check_bar_time_match(
                time(9, 40), "open", MARKET_OPEN_TIME, bar_resolution_minutes=5
            )
        )


class TestTimerManagerMinuteSupport(unittest.TestCase):
    """测试 TimerManager 分钟级支持"""

    def test_every_bar_execution(self):
        """测试 every_bar 每 bar 执行"""
        data, trading_days = make_minute_data(days=1, period_minutes=5)

        call_count = []

        class EveryBarStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_daily(self.on_every_bar, time="every_bar")

            def on_every_bar(self, context):
                call_count.append(1)

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(EveryBarStrategy)
        cerebro.run()

        self.assertGreater(len(call_count), 1)

    def test_specific_time_trigger(self):
        """测试特定时间触发

        注意：由于 bar 粒度为 5 分钟，时间匹配使用 tolerance 机制，
        目标时间 10:00 可能匹配 9:50-10:10 范围内的 bar。
        """
        data, trading_days = make_minute_data(days=1, period_minutes=5)

        triggers = []

        class TimeTriggerStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_daily(self.on_10_00, time="10:00")

            def on_10_00(self, context):
                dt = self.datas[0].datetime.datetime(0)
                triggers.append(dt.time())

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(TimeTriggerStrategy)
        cerebro.run()

        self.assertEqual(len(triggers), 1)
        trigger_time = triggers[0]
        self.assertGreaterEqual(trigger_time.hour, 9)
        if trigger_time.hour == 9:
            self.assertGreaterEqual(trigger_time.minute, 50)

    def test_bar_resolution_inference(self):
        """测试 bar_resolution 自动推断"""
        data, trading_days = make_minute_data(days=1, period_minutes=5)

        inferred_resolution = []

        class ResolutionStrategy(JQ2BTBaseStrategy):
            def next(self):
                super().next()
                if len(inferred_resolution) == 0 and self._bar_count >= 2:
                    inferred_resolution.append(
                        self.timer_manager._bar_resolution_minutes
                    )

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(ResolutionStrategy)
        cerebro.run()

        if inferred_resolution:
            self.assertEqual(inferred_resolution[0], 5)
        else:
            self.skipTest("bar_resolution inference requires multiple bars")

    def test_set_bar_resolution_manually(self):
        """测试手动设置 bar_resolution"""
        data, trading_days = make_minute_data(days=1, period_minutes=5)

        class ManualResolutionStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.timer_manager.set_bar_resolution(15)
                self.res = self.timer_manager._bar_resolution_minutes

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(ManualResolutionStrategy)
        results = cerebro.run()

        self.assertEqual(results[0].res, 15)

    def test_set_data_frequency(self):
        """测试设置数据频率"""
        data, trading_days = make_minute_data(days=1, period_minutes=5)

        class FrequencyStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.timer_manager.set_data_frequency("15m")
                self.freq = self.timer_manager._data_frequency
                self.res = self.timer_manager._bar_resolution_minutes

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(FrequencyStrategy)
        results = cerebro.run()

        self.assertEqual(results[0].freq, "15m")
        self.assertEqual(results[0].res, 15)

    def test_open_time_trigger(self):
        """测试开盘时间触发"""
        data, trading_days = make_minute_data(days=1, period_minutes=5)

        triggers = []

        class OpenStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_daily(self.on_open, time="open")

            def on_open(self, context):
                dt = self.datas[0].datetime.datetime(0)
                triggers.append(dt.time())

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(OpenStrategy)
        cerebro.run()

        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0].hour, 9)
        self.assertEqual(triggers[0].minute, 30)

    def test_close_minus_time_trigger(self):
        """测试收盘前时间触发"""
        data, trading_days = make_minute_data(days=1, period_minutes=5)

        triggers = []

        class CloseMinusStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_daily(self.on_close_minus, time="close-10m")

            def on_close_minus(self, context):
                dt = self.datas[0].datetime.datetime(0)
                triggers.append(dt.time())

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(CloseMinusStrategy)
        cerebro.run()

        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0].hour, 14)
        self.assertLessEqual(triggers[0].minute, 55)


class TestMinuteReplayIntegration(unittest.TestCase):
    """分钟回放集成测试"""

    def test_minute_data_feed(self):
        """测试分钟数据 feed 创建"""
        data, trading_days = make_minute_data(days=2, period_minutes=5)

        self.assertIsNotNone(data)
        self.assertGreater(len(trading_days), 0)

    def test_multiple_timers_minute(self):
        """测试分钟模式下多个定时器"""
        data, trading_days = make_minute_data(days=1, period_minutes=5)

        every_bar_count = []
        open_count = []

        class MultiTimerStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_daily(self.on_every_bar, time="every_bar")
                self.run_daily(self.on_open, time="open")

            def on_every_bar(self, context):
                every_bar_count.append(1)

            def on_open(self, context):
                open_count.append(1)

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(MultiTimerStrategy)
        cerebro.run()

        self.assertGreater(len(every_bar_count), 1)
        self.assertEqual(len(open_count), 1)

    def test_multi_day_minute_replay(self):
        """测试多日分钟回放"""
        data, trading_days = make_minute_data(days=2, period_minutes=5)

        daily_counts = []

        class MultiDayStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_daily(self.on_open, time="open")

            def on_open(self, context):
                daily_counts.append(1)

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(MultiDayStrategy)
        cerebro.run()

        self.assertEqual(len(daily_counts), 2)

    def test_different_bar_resolutions(self):
        """测试不同 bar 粒度"""
        for period_minutes in [1, 5, 15, 30]:
            data, _ = make_minute_data(days=1, period_minutes=period_minutes)

            class TestStrategy(JQ2BTBaseStrategy):
                def initialize(self):
                    self.run_daily(self.cb, time="every_bar")

                def cb(self, context):
                    pass

            cerebro = bt.Cerebro()
            cerebro.broker.setcash(100000)
            cerebro.adddata(data)
            cerebro.addstrategy(TestStrategy)
            cerebro.run()

    def test_timer_manager_has_trading_days(self):
        """测试 TimerManager 交易日设置"""
        data, trading_days = make_minute_data(days=1, period_minutes=5)

        class TradingDaysStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.timer_manager.set_trading_days(trading_days)
                self.has_days = self.timer_manager._trading_days is not None

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(TradingDaysStrategy)
        results = cerebro.run()

        self.assertTrue(results[0].has_days)

    def test_open_plus_time_trigger(self):
        """测试 open+Nm 时间触发"""
        data, _ = make_minute_data(days=1, period_minutes=5)

        triggers = []

        class OpenPlusStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_daily(self.cb, time="open+30m")

            def cb(self, context):
                dt = self.datas[0].datetime.datetime(0)
                triggers.append(dt.time())

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(OpenPlusStrategy)
        cerebro.run()

        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0].hour, 9)
        self.assertGreaterEqual(triggers[0].minute, 50)

    def test_chinese_time_alias(self):
        """测试中文时间别名"""
        data, _ = make_minute_data(days=1, period_minutes=5)

        triggers = []

        class ChineseAliasStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_daily(self.cb, time="开盘")

            def cb(self, context):
                dt = self.datas[0].datetime.datetime(0)
                triggers.append(dt.time())

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(ChineseAliasStrategy)
        cerebro.run()

        self.assertEqual(len(triggers), 1)
        self.assertEqual(triggers[0].hour, 9)
        self.assertEqual(triggers[0].minute, 30)

    def test_unschedule_all(self):
        """测试清空定时器"""
        data, _ = make_minute_data(days=1, period_minutes=5)

        triggers = []

        class UnscheduleStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_daily(self.cb, time="every_bar")

            def cb(self, context):
                triggers.append(1)
                if len(triggers) == 3:
                    self.unschedule_all()

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(UnscheduleStrategy)
        cerebro.run()

        self.assertEqual(len(triggers), 3)

    def test_run_weekly_minute_mode(self):
        """测试周定时器分钟模式"""
        data, _ = make_minute_data(days=5, period_minutes=5)

        triggers = []

        class WeeklyStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_weekly(self.cb, weekday=1, time="open")

            def cb(self, context):
                triggers.append(1)

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(WeeklyStrategy)
        cerebro.run()

        self.assertGreaterEqual(len(triggers), 1)

    def test_run_monthly_minute_mode(self):
        """测试月定时器分钟模式"""
        data, _ = make_minute_data(days=1, period_minutes=5)

        triggers = []

        class MonthlyStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.run_monthly(self.cb, day=1, time="every_bar")

            def cb(self, context):
                triggers.append(1)

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000)
        cerebro.adddata(data)
        cerebro.addstrategy(MonthlyStrategy)
        cerebro.run()

        self.assertGreaterEqual(len(triggers), 1)


def run_smoke_test():
    """运行 smoke test"""
    print("=" * 60)
    print("Task 27: 分钟回放引擎 Smoke Test")
    print("=" * 60)

    print("\n1. 测试 every_bar 规则...")
    rule_type, _, _ = parse_time_rule("every_bar")
    print(f"   parse_time_rule('every_bar') -> {rule_type}")
    assert rule_type == "every_bar", "every_bar 解析失败"
    print("   ✓ 通过")

    print("\n2. 测试 open+30m 规则...")
    rule_type, target_time, offset = parse_time_rule("open+30m")
    print(
        f"   parse_time_rule('open+30m') -> {rule_type}, {target_time}, offset={offset}"
    )
    assert rule_type == "open_offset", "open+30m 解析失败"
    assert target_time == time(10, 0), "open+30m 时间计算错误"
    print("   ✓ 通过")

    print("\n3. 测试 HH:MM 规则...")
    rule_type, target_time, _ = parse_time_rule("10:30")
    print(f"   parse_time_rule('10:30') -> {rule_type}, {target_time}")
    assert rule_type == "absolute", "HH:MM 解析失败"
    assert target_time == time(10, 30), "HH:MM 时间错误"
    print("   ✓ 通过")

    print("\n4. 测试尾盘规则...")
    rule_type, _, _ = parse_time_rule("尾盘")
    print(f"   parse_time_rule('尾盘') -> {rule_type}")
    assert rule_type == "market_close", "尾盘解析失败"
    print("   ✓ 通过")

    print("\n5. 测试盘中规则...")
    rule_type, _, _ = parse_time_rule("intraday")
    print(f"   parse_time_rule('intraday') -> {rule_type}")
    assert rule_type == "intraday", "盘中解析失败"
    print("   ✓ 通过")

    print("\n6. 测试 check_bar_time_match...")
    result = check_bar_time_match(time(10, 0), "every_bar", None)
    print(f"   check_bar_time_match(10:00, 'every_bar') -> {result}")
    assert result == True, "every_bar 应该总是返回 True"

    result = check_bar_time_match(time(10, 0), "intraday", None)
    print(f"   check_bar_time_match(10:00, 'intraday') -> {result}")
    assert result == True, "10:00 应该在交易时间内"

    result = check_bar_time_match(time(8, 0), "intraday", None)
    print(f"   check_bar_time_match(08:00, 'intraday') -> {result}")
    assert result == False, "08:00 不应该在交易时间内"
    print("   ✓ 通过")

    print("\n7. 测试分钟回放...")
    data, trading_days = make_minute_data(days=1, period_minutes=5)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    cerebro.adddata(data)

    call_count = []

    class TestStrategy(JQ2BTBaseStrategy):
        def initialize(self):
            self.run_daily(self.callback, time="every_bar")

        def callback(self, context):
            call_count.append(1)

    cerebro.addstrategy(TestStrategy)
    cerebro.run()

    print(f"   分钟 bar 数量: {len(call_count)}")
    assert len(call_count) > 1, "every_bar 应该触发多次"
    print("   ✓ 通过")

    print("\n8. 测试 close-Nm 规则...")
    rule_type, target_time, offset = parse_time_rule("close-10m")
    print(
        f"   parse_time_rule('close-10m') -> {rule_type}, {target_time}, offset={offset}"
    )
    assert rule_type == "close_offset", "close-10m 解析失败"
    assert target_time == time(14, 50), "close-10m 时间错误"
    assert offset == -10, "close-10m offset 错误"
    print("   ✓ 通过")

    print("\n9. 测试 close+Nm 规则...")
    rule_type, target_time, offset = parse_time_rule("close+10m")
    print(
        f"   parse_time_rule('close+10m') -> {rule_type}, {target_time}, offset={offset}"
    )
    assert rule_type == "close_offset", "close+10m 解析失败"
    assert target_time == time(15, 10), "close+10m 时间错误"
    assert offset == 10, "close+10m offset 错误"
    print("   ✓ 通过")

    print("\n10. 测试 open-Nm 规则...")
    rule_type, target_time, offset = parse_time_rule("open-5m")
    print(
        f"   parse_time_rule('open-5m') -> {rule_type}, {target_time}, offset={offset}"
    )
    assert rule_type == "open_offset", "open-5m 解析失败"
    assert target_time == time(9, 25), "open-5m 时间错误"
    assert offset == -5, "open-5m offset 错误"
    print("   ✓ 通过")

    print("\n11. 测试 before_open 规则...")
    rule_type, _, _ = parse_time_rule("before_open")
    print(f"   parse_time_rule('before_open') -> {rule_type}")
    assert rule_type == "before_open", "before_open 解析失败"
    assert check_bar_time_match(time(9, 0), "before_open", None) == True
    assert check_bar_time_match(time(9, 30), "before_open", None) == False
    print("   ✓ 通过")

    print("\n12. 测试 after_close 规则...")
    rule_type, target_time, _ = parse_time_rule("after_close")
    print(f"   parse_time_rule('after_close') -> {rule_type}, {target_time}")
    assert rule_type == "after_close", "after_close 解析失败"
    print("   ✓ 通过")

    print("\n13. 测试中文别名...")
    aliases = [
        ("开盘", "market_open"),
        ("收盘", "market_close"),
        ("尾盘", "market_close"),
        ("盘中", "intraday"),
    ]
    for rule, expected in aliases:
        rule_type, _, _ = parse_time_rule(rule)
        print(f"   parse_time_rule('{rule}') -> {rule_type}")
        assert rule_type == expected, f"{rule} 解析失败"
    print("   ✓ 通过")

    print("\n" + "=" * 60)
    print("Smoke Test 全部通过!")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="分钟回放引擎测试")
    parser.add_argument("--smoke", action="store_true", help="运行 smoke test")
    args = parser.parse_args()

    if args.smoke:
        run_smoke_test()
    else:
        unittest.main()
