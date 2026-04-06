# 原文链接：https://www.joinquant.com/post/45250
# 策略：这个可入得了你们法眼
# 作者：量化新手
# 核心逻辑：龙虎榜概念+MACD金叉选股，短线持有
# 注：原版用jqlib_ta+talib，此处改为本地MACD实现

import numpy as np


def ema(prices, n):
    k = 2.0 / (n + 1)
    e = prices[0]
    res = []
    for x in prices:
        e = x * k + e * (1 - k)
        res.append(e)
    return np.array(res)


def calc_macd(prices, fast=12, slow=26, signal=9):
    ema_f = ema(prices, fast)
    ema_s = ema(prices, slow)
    diff = ema_f - ema_s
    dea  = ema(diff, signal)
    hist = (diff - dea) * 2
    return diff, dea, hist


def init(context):
    context.n_stocks = 5
    context.hold_days = 5
    context.stock_pool = []
    context.hold_counter = {}
    scheduler.run_daily(select_and_trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def select_and_trade(context, bar_dict):
    """日度选股：中证500中MACD金叉的强势股"""
    # 更新持仓天数，超过hold_days则卖出
    to_sell = []
    for s in list(context.portfolio.positions.keys()):
        context.hold_counter[s] = context.hold_counter.get(s, 0) + 1
        if context.hold_counter[s] >= context.hold_days:
            to_sell.append(s)

    for s in to_sell:
        order_target_value(s, 0)
        context.hold_counter.pop(s, None)
        logger.info(f"[龙虎榜MACD] 持有到期，卖出 {s}")

    # 选新股：中证500中MACD金叉
    stocks_500 = index_components('000905.XSHG')
    stocks_500 = [s for s in stocks_500 if not s.startswith('688')]

    macd_cross = []
    for s in stocks_500[:200]:  # 限制数量
        prices = history_bars(s, 40, '1d', 'close')
        if prices is None or len(prices) < 35:
            continue
        p = np.array(prices, dtype=float)
        diff, dea, hist = calc_macd(p)
        # MACD金叉：diff上穿dea，且hist由负转正
        if diff[-1] > dea[-1] and diff[-2] <= dea[-2] and hist[-1] > 0:
            # 额外过滤：近5日涨幅 > 0
            if p[-1] > p[-6]:
                macd_cross.append(s)

    # 选前N只
    new_stocks = [s for s in macd_cross if s not in context.portfolio.positions][:context.n_stocks]
    context.stock_pool = new_stocks
    logger.info(f"[龙虎榜MACD] 新选股={context.stock_pool}")

    # 买入
    current_hold = len(context.portfolio.positions)
    slots = context.n_stocks - current_hold
    if slots <= 0:
        return

    value = context.portfolio.total_value * 0.95 / context.n_stocks
    for s in context.stock_pool[:slots]:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
            context.hold_counter[s] = 0
            logger.info(f"[龙虎榜MACD] 买入 {s}")
