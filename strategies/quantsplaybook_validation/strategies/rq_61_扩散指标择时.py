# 扩散指标择时策略 - RiceQuant版本
# 原文：【复现】扩散指标择时
# 逻辑：计算全市场个股相对于N日前的涨跌比例（扩散指标），高于阈值买入，低于阈值卖出

import numpy as np


def init(context):
    context.security = '000300.XSHG'
    context.N = 20          # 扩散指标计算周期
    context.buy_threshold = 0.55
    context.sell_threshold = 0.45
    context.pos = False
    context.sample_stocks = []
    context.last_update_month = -1


def handle_bar(context, bar_dict):
    # 每月更新样本股票池
    if context.now.month != context.last_update_month:
        context.last_update_month = context.now.month
        try:
            stocks = index_components('000300.XSHG')
            context.sample_stocks = stocks if stocks else []
        except Exception:
            context.sample_stocks = []

    if not context.sample_stocks:
        return

    # 计算扩散指标：当前价格高于N日前价格的股票比例
    up_count = 0
    total = 0
    for stock in context.sample_stocks[:100]:  # 取前100只避免超时
        try:
            closes = history_bars(stock, context.N + 1, '1d', 'close')
            if closes is None or len(closes) < context.N + 1:
                continue
            if closes[-1] > closes[0]:
                up_count += 1
            total += 1
        except Exception:
            continue

    if total == 0:
        return

    diffusion = up_count / total

    # 择时交易
    if diffusion > context.buy_threshold and not context.pos:
        order_target_value(context.security, context.portfolio.total_value * 0.95)
        context.pos = True
    elif diffusion < context.sell_threshold and context.pos:
        order_target_value(context.security, 0)
        context.pos = False
