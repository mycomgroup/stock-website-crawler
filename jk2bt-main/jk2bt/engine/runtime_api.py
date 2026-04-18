"""
engine/runtime_api.py
策略运行时 API - 只能在策略运行时调用。

包含:
- get_current_data: 获取当前数据
- get_current_tick: 获取当前 tick 数据

这些函数依赖策略运行状态，与 engine 层紧密耦合。
策略代码应该从 engine 层导入这些函数。
"""

from .data_proxies import _CurrentDataProxy, _TickDataProxy


def get_current_data(bt_strategy=None):
    """
    聚宽风格 get_current_data()。

    参数:
        bt_strategy: bt.Strategy 实例（可选）

    返回:
        _CurrentDataProxy 对象

    示例:
        current = get_current_data(context)
        price = current['sh600519'].last_price
    """
    if bt_strategy is None:
        bt_strategy = _get_current_strategy_safe()
    return _CurrentDataProxy(bt_strategy)


def get_current_tick(security, bt_strategy=None):
    """
    获取当前 tick 数据（聚宽兼容接口）。

    参数:
        security: 股票代码，如 '000001.XSHG'
        bt_strategy: bt.Strategy 实例（可选）

    返回:
        _TickDataProxy 对象

    示例:
        tick = get_current_tick('000001.XSHG')
        price = tick.current
    """
    if bt_strategy is None:
        bt_strategy = _get_current_strategy_safe()
    return _TickDataProxy(security, bt_strategy)


def _get_current_strategy_safe():
    """安全获取当前策略实例"""
    from .runner import _get_current_strategy

    return _get_current_strategy()


__all__ = [
    "get_current_data",
    "get_current_tick",
]
