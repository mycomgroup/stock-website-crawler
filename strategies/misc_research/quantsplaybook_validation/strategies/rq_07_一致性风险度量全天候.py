# 一致性风险度量（全天候）策略 - RiceQuant版本
# 原文：致敬经典作品——小兵哥《一致性风险度量》——极速版
# 作者：jqz1226
# 原文：https://www.joinquant.com/post/37611
# 逻辑：股票+商品+债券+海外，按波动率一致性分配权重，月度再平衡

import numpy as np
import math


EQUITY = ['510300.XSHG']          # 沪深300ETF
COMMODITIES = ['518880.XSHG']     # 黄金ETF
BONDS = ['511010.XSHG']           # 国债ETF
MONEY_FUND = ['513100.XSHG']      # 纳指100
CONFIDENCE = 2.58                 # 99%置信水平


def calc_var(prices, confidence=2.58):
    """计算VaR（历史模拟法）"""
    if len(prices) < 2:
        return 0.01
    p = np.array(prices, dtype=float)
    log_ret = np.diff(np.log(p))
    vol = np.std(log_ret)
    return confidence * vol * math.sqrt(250)


def init(context):
    context.pools = EQUITY + COMMODITIES + BONDS + MONEY_FUND
    context.month = -1


def handle_bar(context, bar_dict):
    current_month = context.now.month
    if current_month == context.month:
        return

    vars_ = {}
    for asset in context.pools:
        try:
            prices = history_bars(asset, 60, '1d', 'close')
            if prices is None or len(prices) < 20:
                continue
            v = calc_var(prices, CONFIDENCE)
            if v > 0:
                vars_[asset] = v
        except Exception:
            continue

    if not vars_:
        return
    context.month = current_month

    # 按VaR倒数分配权重（风险平价）
    inv_var = {a: 1.0 / v for a, v in vars_.items()}
    total = sum(inv_var.values())
    weights = {a: w / total for a, w in inv_var.items()}

    for asset in list(context.portfolio.positions.keys()):
        if asset not in weights:
            order_target_value(asset, 0)

    total_value = context.portfolio.total_value
    for asset, w in weights.items():
        bar = (bar_dict[asset] if asset in bar_dict else None)
        if bar is not None and not bar.is_trading:
            continue
        order_target_value(asset, total_value * w * 0.99)
