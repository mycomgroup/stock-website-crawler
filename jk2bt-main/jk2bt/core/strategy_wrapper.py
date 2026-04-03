"""
JQStrategyWrapper - 聚宽策略包装器类

将聚宽风格策略包装为 Backtrader 可运行的策略类。
"""

import pandas as pd
import inspect
from datetime import timedelta

# 导入基类和必要组件
try:
    from .strategy_base import (
        JQ2BTBaseStrategy,
        GlobalState,
        ContextProxy,
        JQLogAdapter,
        TimerManager,
    )
except ImportError:
    from jk2bt.core.strategy_base import (
        JQ2BTBaseStrategy,
        GlobalState,
        ContextProxy,
        JQLogAdapter,
        TimerManager,
    )


class _DataProxy:
    """模拟 JoinQuant handle_data 函数的 data 参数"""

    def __init__(self, strategy):
        self._strategy = strategy

    def __getitem__(self, security):
        """获取证券的当前数据"""
        return self._strategy._get_security_data(security)

    @property
    def current_price(self):
        """返回一个可索引的当前价格字典"""
        return _CurrentPriceProxy(self._strategy)


class _CurrentPriceProxy:
    """模拟 data.current_price[security]"""

    def __init__(self, strategy):
        self._strategy = strategy

    def __getitem__(self, security):
        """获取证券当前价格"""
        return self._strategy._get_current_price(security)


# 当前策略实例（模块级变量）
_current_strategy_instance = None


def _set_current_strategy_instance(strategy):
    """设置当前策略实例"""
    global _current_strategy_instance
    _current_strategy_instance = strategy


def _get_current_strategy():
    """获取当前策略实例"""
    global _current_strategy_instance
    return _current_strategy_instance


class JQStrategyWrapper(JQ2BTBaseStrategy):
    """
    聚宽策略包装器

    将聚宽风格的策略函数包装为 Backtrader 可执行的策略类。

    参数:
        strategy_functions: 策略函数字典，包含 initialize, handle_data 等
        printlog: 是否打印日志
        log_dir: 日志目录
        prerun_mode: 是否预运行模式
        max_prerun_days: 预运行最大天数
        frequency: 数据频率 ('daily', '1m', '5m', '15m', '30m', '60m')
        initial_capital: 初始资金
        start_date: 回测开始日期
        end_date: 回测结束日期
    """

    params = (
        ("strategy_functions", None),
        ("printlog", True),
        ("log_dir", "logs"),
        ("prerun_mode", False),
        ("max_prerun_days", 5),
        ("frequency", "daily"),
        ("initial_capital", 1000000),
        ("start_date", None),
        ("end_date", None),
    )

    def __init__(self):
        """初始化策略包装器"""
        # 设置初始资金
        self._initial_capital = self.params.initial_capital

        # 设置当前策略实例（全局访问）
        _set_current_strategy_instance(self)

        # 调用父类初始化
        super().__init__()

        # 在调用策略initialize函数前，设置 current_dt 和 previous_date
        # 这样在 initialize 函数中就可以使用这些值
        if self.params.start_date:
            start_dt = pd.to_datetime(self.params.start_date)
            self.current_dt = start_dt
            # previous_date 设为 start_date 前一天
            self.previous_date = start_dt - timedelta(days=1)
            # 同时更新 context 的 current_dt
            self.context.current_dt = start_dt

        # 设置数据频率和 bar_resolution
        frequency = self.params.frequency
        if frequency != "daily":
            self.timer_manager.set_data_frequency(frequency)
            freq_to_minutes = {
                "1m": 1,
                "5m": 5,
                "15m": 15,
                "30m": 30,
                "60m": 60,
            }
            minutes = freq_to_minutes.get(frequency, 1)
            self.timer_manager.set_bar_resolution(minutes)

        # 获取策略函数
        strategy_funcs = self.params.strategy_functions or {}

        # 调用initialize函数
        if "initialize" in strategy_funcs:
            try:
                strategy_funcs["initialize"](self.context)
            except Exception as e:
                import traceback
                self.log(f"initialize执行错误: {e}")
                self.log(f"详细traceback:\n{traceback.format_exc()}")

        # 调用after_code_changed函数（聚宽风格）
        if "after_code_changed" in strategy_funcs:
            try:
                strategy_funcs["after_code_changed"](self.context)
            except Exception as e:
                import traceback
                self.log(f"after_code_changed执行错误: {e}")
                self.log(f"详细traceback:\n{traceback.format_exc()}")

        # 保存handle函数引用
        self._handle_functions = {}
        for name, func in strategy_funcs.items():
            if name.startswith("handle_") or name.startswith("trading_"):
                self._handle_functions[name] = func

        # 保存before_trading_start函数引用（聚宽特殊函数）
        self._before_trading_start_func = strategy_funcs.get("before_trading_start", None)

    def next(self):
        """每日/每bar执行"""
        # 更新当前策略实例
        _set_current_strategy_instance(self)

        # 调用父类的next（包括净值记录等）
        super().next()

        # 执行before_trading_start函数（聚宽特殊函数，在每个交易日开盘前执行）
        if self._before_trading_start_func is not None:
            try:
                sig = inspect.signature(self._before_trading_start_func)
                params = list(sig.parameters.keys())
                if len(params) >= 1:
                    self._before_trading_start_func(self.context)
            except Exception as e:
                self.log(f"before_trading_start执行错误: {e}")

        # 执行handle函数（如果定时器中没有注册）
        # 创建 data 参数代理
        data_proxy = _DataProxy(self)
        for name, func in self._handle_functions.items():
            try:
                # 检查函数签名，判断是否需要 data 参数
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                if len(params) >= 2:
                    # handle_data(context, data) 格式
                    func(self.context, data_proxy)
                else:
                    # handle_data(context) 格式
                    func(self.context)
            except Exception as e:
                self.log(f"{name}执行错误: {e}")

    def _get_security_data(self, security):
        """获取证券的当前数据"""
        # 返回一个简单的数据对象
        class _SecurityData:
            def __init__(self, parent, sec):
                self._parent = parent
                self._security = sec

            @property
            def price(self):
                return self._parent._get_current_price(self._security)

            @property
            def close(self):
                return self._parent._get_current_price(self._security)

            @property
            def high(self):
                return self._parent._get_current_high(self._security)

            @property
            def low(self):
                return self._parent._get_current_low(self._security)

            @property
            def open(self):
                return self._parent._get_current_open(self._security)

            @property
            def volume(self):
                return self._parent._get_current_volume(self._security)

        return _SecurityData(self, security)

    def _get_current_price(self, security):
        """获取证券当前价格"""
        for data in self.datas:
            if data._name == security:
                return data.close[0]
        return None

    def _get_current_high(self, security):
        """获取证券当前最高价"""
        for data in self.datas:
            if data._name == security:
                return data.high[0]
        return None

    def _get_current_low(self, security):
        """获取证券当前最低价"""
        for data in self.datas:
            if data._name == security:
                return data.low[0]
        return None

    def _get_current_open(self, security):
        """获取证券当前开盘价"""
        for data in self.datas:
            if data._name == security:
                return data.open[0]
        return None

    def _get_current_volume(self, security):
        """获取证券当前成交量"""
        for data in self.datas:
            if data._name == security:
                return data.volume[0]
        return None


__all__ = [
    'JQStrategyWrapper',
    '_DataProxy',
    '_CurrentPriceProxy',
    '_set_current_strategy_instance',
    '_get_current_strategy',
]