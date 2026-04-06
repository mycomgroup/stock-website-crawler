# 原文链接：https://www.joinquant.com/post/50000
# 策略：昨日炸板股策略
# 核心逻辑：选昨日触及涨停但未封板（炸板）的股票，次日低开买入，持有1-2天。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.hold_days = 2
    context.positions_hold = {}
    scheduler.run_daily(rebalance, time_rule=market_open(minute=5))

def handle_bar(context, bar_dict):
    # 持仓超过hold_days则清仓
    to_sell = []
    for s, entry_date in list(context.positions_hold.items()):
        days_held = (context.now.date() - entry_date).days
        if days_held >= context.hold_days:
            to_sell.append(s)
    for s in to_sell:
        order_target_value(s, 0)
        context.positions_hold.pop(s, None)
        logger.info(f"持仓到期清仓: {s}")

def rebalance(context, bar_dict):
    # 获取全市场股票
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    candidates = []
    for s in stocks:
        try:
            closes = history_bars(s, 3, '1d', 'close')
            highs  = history_bars(s, 3, '1d', 'high')
            opens  = history_bars(s, 3, '1d', 'open')
            if closes is None or highs is None or opens is None or len(closes) < 3:
                continue
            prev2_close = closes[-3]   # 前天收盘（用于计算昨日涨幅基准）
            prev_close  = closes[-2]   # 昨日收盘
            prev_high   = highs[-2]    # 昨日最高
            today_open  = opens[-1]    # 今日开盘
            # 昨日触及涨停（最高>=前天收盘*1.095）但收盘未封板（收盘<前天收盘*1.09）
            if prev_high >= prev2_close * 1.095 and prev_close < prev2_close * 1.09:
                # 今日低开（开盘低于昨收）
                if today_open < prev_close:
                    candidates.append(s)
        except Exception:
            continue

    if not candidates:
        logger.info("无炸板候选股")
        return

    # 选前5只，等权买入
    target = candidates[:5]
    cash_per = context.portfolio.cash * 0.9 / len(target)
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, cash_per)
            context.positions_hold[s] = context.now.date()
    logger.info(f"炸板买入: {target}")
