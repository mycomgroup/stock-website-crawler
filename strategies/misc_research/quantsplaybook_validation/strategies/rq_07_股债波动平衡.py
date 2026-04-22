# 股债波动平衡策略 - RiceQuant版本
# 原文：股债波动平衡
# 作者：囚徒
# 原文：https://www.joinquant.com/post/28893
# 逻辑：按波动率倒数分配权重，每周五再平衡

import numpy as np
import math


ASSETS = [
    '510300.XSHG',  # 沪深300ETF（股票）
    '518880.XSHG',  # 黄金ETF（大宗商品）
    '511010.XSHG',  # 国债ETF（债券）
    '513100.XSHG',  # 纳指100（海外）
    '513500.XSHG',  # 标普500（海外）
    '159928.XSHE',  # 消费ETF
    '512010.XSHG',  # 军工ETF
]


def get_volatility(prices, annualize=True):
    """计算年化波动率"""
    if len(prices) < 2:
        return float('nan')
    p = np.array(prices, dtype=float)
    log_ret = np.diff(np.log(p))
    vol = np.std(log_ret)
    return vol * math.sqrt(250) * 100 if annualize else vol


def init(context):
    context.assets = ASSETS
    context.lookback = 40
    scheduler.run_weekly(rebalance, weekday=5, time_rule=market_open(minute=0))



def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    waves = []
    valid_assets = []
    for asset in context.assets:
        try:
            prices = history_bars(asset, context.lookback, '1d', 'close')
            if prices is None or len(prices) < context.lookback:
                continue
            vol = get_volatility(prices)
            if not math.isnan(vol) and vol > 0:
                waves.append(vol)
                valid_assets.append(asset)
        except Exception:
            continue

    if not valid_assets:
        return

    # 按波动率倒数分配权重
    inv_vol = [1.0 / w for w in waves]
    total = sum(inv_vol)
    weights = {valid_assets[i]: inv_vol[i] / total for i in range(len(valid_assets))}

    # 检查是否需要再平衡（偏差>5%）
    need_rebal = False
    for asset, target_w in weights.items():
        pos = context.portfolio.positions.get(asset)
        current_w = pos.market_value / context.portfolio.total_value if pos else 0
        if abs(current_w - target_w) > 0.05:
            need_rebal = True
            break

    if not need_rebal and len(context.portfolio.positions) > 0:
        return

    # 先卖出不在目标的
    for asset in list(context.portfolio.positions.keys()):
        if asset not in weights:
            order_target_value(asset, 0)

    total_value = context.portfolio.total_value
    for asset, w in weights.items():
        bar = (bar_dict[asset] if asset in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        order_target_value(asset, total_value * w * 0.99)
