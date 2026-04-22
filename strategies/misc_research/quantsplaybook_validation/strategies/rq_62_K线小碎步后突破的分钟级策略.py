# 原文链接：https://www.joinquant.com/post/62000
# 策略：K线小碎步后突破的分钟级策略
# 核心逻辑：K线小碎步突破，选近期低波动后放量突破的股票，分钟级买入。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.n_stocks = 5
    context.hold_days = 3
    context.positions_hold = {}
    scheduler.run_daily(select_stocks, time_rule=market_open(minute=30))
    scheduler.run_daily(check_exit, time_rule=market_open(minute=210))  # 14:30

def handle_bar(context, bar_dict):
    pass

def select_stocks(context, bar_dict):
    """选择低波动后突破的股票"""
    # 清理超期持仓
    to_sell = []
    for s, entry_date in list(context.positions_hold.items()):
        if (context.now.date() - entry_date).days >= context.hold_days:
            to_sell.append(s)
    for s in to_sell:
        order_target_value(s, 0)
        context.positions_hold.pop(s, None)

    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    stocks = stocks[:300]

    candidates = []
    for s in stocks:
        try:
            closes = history_bars(s, 25, '1d', 'close')
            volumes = history_bars(s, 25, '1d', 'volume')
            if closes is None or volumes is None or len(closes) < 20:
                continue
            # 近10日波动率低（小碎步）
            recent_vol = np.std(closes[-10:]) / np.mean(closes[-10:])
            # 今日突破（收盘>近10日最高）
            recent_high = np.max(closes[-11:-1])
            today_close = closes[-1]
            # 今日成交量放大
            avg_vol = np.mean(volumes[-11:-1])
            today_vol = volumes[-1]
            if recent_vol < 0.03 and today_close > recent_high and today_vol > avg_vol * 1.5:
                candidates.append(s)
        except Exception:
            continue

    if not candidates:
        return

    target = candidates[:context.n_stocks]
    cash_per = context.portfolio.cash * 0.9 / max(len(target), 1)
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading and s not in context.positions_hold:
            order_target_value(s, cash_per)
            context.positions_hold[s] = context.now.date()
    logger.info(f"小碎步突破买入: {target}")

def check_exit(context, bar_dict):
    """尾盘检查止损"""
    for s in list(context.positions_hold.keys()):
        if s in bar_dict:
            price = bar_dict[s].close
            closes = history_bars(s, 2, '1d', 'close')
            if closes is not None and len(closes) >= 2:
                entry = closes[-2]
                if price < entry * 0.95:  # 5%止损
                    order_target_value(s, 0)
                    context.positions_hold.pop(s, None)
                    logger.info(f"小碎步止损: {s}")
