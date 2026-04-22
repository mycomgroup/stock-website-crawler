# 原文链接：https://www.joinquant.com/post/57000
# 策略：技术分析算法框架与实战之二识别圆弧底
# 核心逻辑：识别圆弧底形态（近期价格从低点缓慢回升），选符合圆弧底的股票买入。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def is_rounding_bottom(closes, n=20):
    """识别圆弧底：价格先下降后上升，形成U形"""
    if len(closes) < n:
        return False
    p = closes[-n:]
    mid = n // 2
    # 前半段下降，后半段上升
    first_half = p[:mid]
    second_half = p[mid:]
    # 前半段趋势向下
    first_trend = np.polyfit(range(mid), first_half, 1)[0]
    # 后半段趋势向上
    second_trend = np.polyfit(range(len(second_half)), second_half, 1)[0]
    # 最低点在中间附近
    min_idx = np.argmin(p)
    min_in_middle = n // 4 < min_idx < 3 * n // 4
    return first_trend < 0 and second_trend > 0 and min_in_middle

def init(context):
    context.n_stocks = 5
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    stocks = all_instruments('CS')['order_book_id'].tolist()
    stocks = [s for s in stocks if not s.startswith('688') and not s.startswith('8')]
    stocks = stocks[:300]

    candidates = []
    for s in stocks:
        try:
            closes = history_bars(s, 25, '1d', 'close')
            if closes is not None and len(closes) >= 20:
                if is_rounding_bottom(closes, n=20):
                    # 当前价格高于20日前价格（确认回升）
                    if closes[-1] > closes[-20] * 1.02:
                        candidates.append(s)
        except Exception:
            continue

    if not candidates:
        logger.info("无圆弧底候选股")
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        return

    target = candidates[:context.n_stocks]

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    value = context.portfolio.total_value * 0.95 / n
    for s in target:
        if s in bar_dict and bar_dict[s].is_trading:
            order_target_value(s, value)
    logger.info(f"圆弧底选股，持仓: {target}")
