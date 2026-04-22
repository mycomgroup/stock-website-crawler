# 原文链接：https://www.joinquant.com/post/28789
# 策略：昨日炸板股策略
# 作者：WiseFurther
# 核心逻辑：选昨日触及涨停但未封板（炸板）的股票，次日低开买入
# 注：原版用 talib.MACD 做大盘过滤，此处用 numpy 实现

import numpy as np


def calc_macd(prices, fast=12, slow=26, signal=9):
    def ema(p, n):
        k = 2.0 / (n + 1)
        e = p[0]
        res = []
        for x in p:
            e = x * k + e * (1 - k)
            res.append(e)
        return np.array(res)
    ema_f = ema(prices, fast)
    ema_s = ema(prices, slow)
    diff = ema_f - ema_s
    dea  = ema(diff, signal)
    hist = (diff - dea) * 2
    return diff, dea, hist


def init(context):
    context.stock_pool = []
    context.max_hold = 3
    scheduler.run_daily(before_market_open, time_rule=market_open(minute=0))
    scheduler.run_daily(market_open_trade, time_rule=market_open(minute=5))
    scheduler.run_daily(after_market_close, time_rule=market_close(minute=0))


def handle_bar(context, bar_dict):
    pass


def before_market_open(context):
    """盘前：筛选昨日炸板股"""
    # 大盘MACD过滤
    prices_idx = history_bars('000001.XSHG', 40, '1d', 'close')
    if prices_idx is not None and len(prices_idx) >= 35:
        p = np.array(prices_idx, dtype=float)
        _, _, hist = calc_macd(p)
        if hist[-1] < hist[-2]:
            context.stock_pool = []
            print("[炸板] 大盘MACD死叉，今日不交易")
            return

    # 获取全市场股票
    instruments_df = all_instruments('CS')
    all_stocks = [s for s in instruments_df['order_book_id'].tolist()
                  if not s.startswith('688')
                  and not s.startswith('8')]

    # 筛选昨日炸板股：昨日最高价 >= 涨停价 且 收盘价 < 涨停价
    candidates = []
    for stock in all_stocks[:2000]:  # 限制数量避免超时
        try:
            highs      = history_bars(stock, 2, '1d', 'high')
            closes     = history_bars(stock, 2, '1d', 'close')
            _pre_stock = history_bars(stock, 2, '1d', 'close')
            limit_ups = _pre_stock * 1.1 if _pre_stock is not None else None
            opens      = history_bars(stock, 2, '1d', 'open')
            if any(x is None or len(x) < 2 for x in [highs, closes, limit_ups, opens]):
                continue
            yesterday_high  = highs[-2]
            yesterday_close = closes[-2]
            yesterday_limit = limit_ups[-2]
            yesterday_open  = opens[-2]

            # 炸板条件：最高价触及涨停 且 收盘未封板 且 开盘未一字板
            if (yesterday_high >= yesterday_limit * 0.999 and
                    yesterday_close < yesterday_limit * 0.999 and
                    yesterday_open < yesterday_limit * 0.999):
                # 收阳（收盘 > 开盘）
                if yesterday_close > yesterday_open:
                    candidates.append(stock)
        except Exception:
            continue

    context.stock_pool = candidates[:context.max_hold * 3]
    print(f"[炸板] 候选股票: {len(context.stock_pool)}")


def market_open_trade(context, bar_dict):
    """开盘后5分钟：买入炸板股"""
    if not context.stock_pool:
        return

    # 卖出不在池中的持仓
    for s in list(context.portfolio.positions.keys()):
        if s not in context.stock_pool:
            order_target_value(s, 0)

    # 买入
    hold_count = len(context.portfolio.positions)
    slots = context.max_hold - hold_count
    if slots <= 0:
        return

    weight = 1.0 / context.max_hold
    for stock in context.stock_pool[:slots]:
        if stock in context.portfolio.positions:
            continue
        bar = (bar_dict[stock] if stock in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        order_target_value(stock, context.portfolio.total_value * weight * 0.95)
        print(f"[炸板] 买入 {stock}")


def after_market_close(context):
    print(f"[炸板] 持仓: {list(context.portfolio.positions.keys())}")
