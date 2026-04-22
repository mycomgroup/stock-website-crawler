# 原文链接：https://www.joinquant.com/post/63002
# 策略：怎么让龟速变奔跑首版突破一进二
# 核心逻辑：突破一进二，选近期突破前高的股票，持有至回调止损。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 5
    context.stop_loss = 0.07  # 7%止损
    context.entry_prices = {}
    context.lookback = 20  # 突破前N日高点
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 止损检查
    to_sell = []
    for s, entry in list(context.entry_prices.items()):
        if s in bar_dict and entry > 0:
            price = bar_dict[s].close
            if (entry - price) / entry > context.stop_loss:
                to_sell.append(s)
    for s in to_sell:
        order_target_value(s, 0)
        context.entry_prices.pop(s, None)
        logger.info(f"突破止损: {s}")

    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    stocks = stocks[:300]

    candidates = []
    for s in stocks:
        try:
            closes = history_bars(s, context.lookback + 2, '1d', 'close')
            volumes = history_bars(s, context.lookback + 2, '1d', 'volume')
            if closes is None or volumes is None or len(closes) < context.lookback + 1:
                continue
            # 前N日最高价（不含今日）
            prev_high = np.max(closes[-(context.lookback+1):-1])
            today_close = closes[-1]
            avg_vol = np.mean(volumes[-(context.lookback+1):-1])
            today_vol = volumes[-1]
            # 突破前高且放量
            if today_close > prev_high * 1.01 and today_vol > avg_vol * 1.3:
                candidates.append(s)
        except Exception:
            continue

    if not candidates:
        return

    # 已持仓不重复买入
    current_positions = set(context.portfolio.positions.keys())
    new_candidates = [s for s in candidates if s not in current_positions]

    if not new_candidates:
        return

    available_slots = context.n_stocks - len(current_positions)
    if available_slots <= 0:
        return

    target_new = new_candidates[:available_slots]
    cash_per = context.portfolio.cash * 0.9 / max(len(target_new), 1)
    for s in target_new:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, cash_per)
            context.entry_prices[s] = bar_dict[s].close
    logger.info(f"突破一进二买入: {target_new}")
