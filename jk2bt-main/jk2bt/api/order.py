"""
订单与组合管理模块（权威文件）

包含订单相关函数和组合管理工具：
- order_shares: 按股数下单
- order_target_percent: 按目标仓位百分比下单
- LimitOrderStyle: 限价单样式类
- MarketOrderStyle: 市价单样式类
- rebalance_portfolio: 组合再平衡
- get_portfolio_weights: 获取组合权重
- calculate_position_value: 计算持仓价值

此模块是订单相关功能的权威来源，从 enhancements.py 拆分而来。
"""

import warnings
from jk2bt.core.strategy_base import get_current_data  # noqa: F401（延迟导入，避免循环）


def order_shares(security, amount, style=None):
    """
    聚宽 order_shares API
    按股数下单（买入或卖出指定数量的股票）

    参数:
        security: 股票代码，如 '600519.XSHG', 'sh600519'
        amount: 股数，正数表示买入，负数表示卖出
        style: 订单类型（可选），如 LimitOrderStyle(limit_price)

    返回:
        Order 对象
    """
    from jk2bt.core.strategy_base import _current_strategy

    if _current_strategy is None:
        warnings.warn("order_shares 需要在策略运行时调用")
        return None

    return _current_strategy.order(security, amount)


def order_target_percent(security, percent):
    """
    聚宽 order_target_percent API
    调整持仓到目标比例（占总资产的百分比）

    参数:
        security: 股票代码
        percent: 目标仓位比例 (0.0 - 1.0)

    返回:
        Order 对象
    """
    from jk2bt.core.strategy_base import _current_strategy

    if _current_strategy is None:
        warnings.warn("order_target_percent 需要在策略运行时调用")
        return None

    return _current_strategy.order_target_percent(security, percent)


class LimitOrderStyle:
    """限价单风格"""

    def __init__(self, limit_price):
        self.limit_price = limit_price


class MarketOrderStyle:
    """市价单风格"""

    def __init__(self):
        pass


def calculate_position_value(security, amount=None):
    """
    计算持仓市值

    参数:
        security: 股票代码
        amount: 持仓数量（可选，默认使用当前持仓）

    返回:
        持仓市值
    """
    from jk2bt.core.strategy_base import _current_strategy, get_current_data as _get_cd

    if _current_strategy is None:
        return 0

    current_data = _get_cd()
    price = current_data[security].last_price

    if amount is None:
        pos = _current_strategy.getposition(security)
        amount = pos.size if pos else 0

    return amount * price


def get_position_ratio(security):
    """
    获取当前持仓比例

    参数:
        security: 股票代码

    返回:
        持仓比例（占总资产的百分比）
    """
    from jk2bt.core.strategy_base import _current_strategy

    if _current_strategy is None:
        return 0

    total_value = _current_strategy.broker.getvalue()
    pos_value = calculate_position_value(security)

    return pos_value / total_value if total_value > 0 else 0


def will_sell_on_limit_up(security):
    """
    判断是否会在涨停时卖出

    参数:
        security: 股票代码

    返回:
        bool
    """
    from jk2bt.core.strategy_base import _current_strategy, get_current_data as _get_cd

    if _current_strategy is None:
        return False

    current_data = _get_cd()
    cd = current_data[security]

    return cd.last_price >= cd.high_limit * 0.99


def will_buy_on_limit_down(security):
    """
    判断是否会在跌停时买入

    参数:
        security: 股票代码

    返回:
        bool
    """
    from jk2bt.core.strategy_base import _current_strategy, get_current_data as _get_cd

    if _current_strategy is None:
        return False

    current_data = _get_cd()
    cd = current_data[security]

    return cd.last_price <= cd.low_limit * 1.01


def rebalance_portfolio(target_weights, stock_list=None):
    """
    按目标权重重新平衡组合

    参数:
        target_weights: dict {股票代码: 目标权重}
        stock_list: 股票列表（可选）
    """
    from jk2bt.core.strategy_base import _current_strategy

    if _current_strategy is None:
        return

    for security, weight in target_weights.items():
        order_target_percent(security, weight)

    if stock_list:
        positions = _current_strategy.context.portfolio.positions
        for security in positions:
            if security not in target_weights:
                order_target_percent(security, 0)


def get_portfolio_weights():
    """
    获取当前组合权重

    返回:
        dict {股票代码: 当前权重}
    """
    from jk2bt.core.strategy_base import _current_strategy

    if _current_strategy is None:
        return {}

    total_value = _current_strategy.broker.getvalue()
    positions = _current_strategy.context.portfolio.positions

    weights = {}
    for security, pos in positions.items():
        pos_value = pos.size * pos.price
        weights[security] = pos_value / total_value if total_value > 0 else 0

    return weights


__all__ = [
    "order_shares",
    "order_target_percent",
    "LimitOrderStyle",
    "MarketOrderStyle",
    "rebalance_portfolio",
    "get_portfolio_weights",
    "calculate_position_value",
    "get_position_ratio",
    "will_sell_on_limit_up",
    "will_buy_on_limit_down",
]
