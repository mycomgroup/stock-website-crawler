# 原文链接：https://www.joinquant.com/post/59002
# 策略：追板策略今年收益已翻倍
# 核心逻辑：追板策略，选昨日涨停且今日高开的股票，开盘后买入，持有1-2天。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.hold_days = 2
    context.positions_hold = {}
    context.n_stocks = 3
    scheduler.run_daily(rebalance, time_rule=market_open(minute=5))

def handle_bar(context, bar_dict):
    # 持仓超期清仓
    to_sell = []
    for s, entry_date in list(context.positions_hold.items()):
        days_held = (context.now.date() - entry_date).days
        if days_held >= context.hold_days:
            to_sell.append(s)
    for s in to_sell:
        order_target_value(s, 0)
        context.positions_hold.pop(s, None)

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]

    candidates = []
    for s in stocks:
        try:
            closes = history_bars(s, 3, '1d', 'close')
            opens  = history_bars(s, 3, '1d', 'open')
            if closes is None or opens is None or len(closes) < 3:
                continue
            prev2_close = closes[-3]   # 前天收盘
            prev_close  = closes[-2]   # 昨日收盘
            today_open  = opens[-1]    # 今日开盘
            # 昨日涨停（昨收 >= 前天收盘 * 1.095）
            if prev_close >= prev2_close * 1.095:
                # 今日高开（开盘高于昨收1%以上）
                if today_open > prev_close * 1.01:
                    candidates.append((s, today_open / prev_close))
        except Exception:
            continue

    if not candidates:
        return

    # 按高开幅度排序
    candidates.sort(key=lambda x: x[1], reverse=True)
    target = [s for s, _ in candidates[:context.n_stocks]]

    cash_per = context.portfolio.cash * 0.9 / max(len(target), 1)
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading and s not in context.positions_hold:
            order_target_value(s, cash_per)
            context.positions_hold[s] = context.now.date()
    logger.info(f"追板买入: {target}")
