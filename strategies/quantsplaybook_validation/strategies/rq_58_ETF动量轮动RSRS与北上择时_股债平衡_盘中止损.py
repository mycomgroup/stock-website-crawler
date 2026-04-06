# 原文链接：https://www.joinquant.com/post/58000
# 策略：ETF动量轮动RSRS与北上择时_股债平衡_盘中止损
# 核心逻辑：ETF动量轮动+RSRS择时+股债平衡，盘中跌破止损线时清仓。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def calc_rsrs(high, low, n=18):
    x = np.array(low[-n:])
    y = np.array(high[-n:])
    b = np.polyfit(x, y, 1)
    return b[0]

def init(context):
    context.etf_pool = [
        '510300.XSHG',  # 沪深300ETF
        '510500.XSHG',  # 中证500ETF
        '159915.XSHE',  # 创业板ETF
    ]
    context.bond_etf = '511010.XSHG'  # 国债ETF
    context.stock_ratio = 0.6  # 股票仓位
    context.stop_loss = 0.05   # 止损5%
    context.hold_etf = None
    context.entry_price = {}
    context.momentum_days = 20
    scheduler.run_daily(rebalance, time_rule=market_open(minute=30))
    scheduler.run_daily(check_stop_loss, time_rule=market_open(minute=60))

def handle_bar(context, bar_dict):
    pass

def check_stop_loss(context, bar_dict):
    """盘中止损检查"""
    for s, entry in list(context.entry_price.items()):
        if s in bar_dict:
            current = bar_dict[s].close
            if entry > 0 and (entry - current) / entry > context.stop_loss:
                order_target_value(s, 0)
                context.entry_price.pop(s, None)
                logger.info(f"止损触发，清仓 {s}")

def rebalance(context, bar_dict):
    scores = {}
    for etf in context.etf_pool:
        try:
            closes = history_bars(etf, context.momentum_days + 1, '1d', 'close')
            highs = history_bars(etf, 25, '1d', 'high')
            lows = history_bars(etf, 25, '1d', 'low')
            if closes is None or len(closes) < context.momentum_days + 1:
                continue
            mom = (closes[-1] - closes[0]) / closes[0]
            rsrs = calc_rsrs(highs, lows) if highs is not None and lows is not None else 1.0
            scores[etf] = mom * 0.7 + rsrs * 0.3
        except Exception:
            continue

    if not scores:
        return

    best_etf = max(scores, key=scores.get)
    best_score = scores[best_etf]

    # 股债平衡
    stock_value = context.portfolio.total_value * context.stock_ratio
    bond_value = context.portfolio.total_value * (1 - context.stock_ratio) * 0.95

    if best_score > 0:
        if context.hold_etf and context.hold_etf != best_etf:
            order_target_value(context.hold_etf, 0)
        order_target_value(best_etf, stock_value)
        context.hold_etf = best_etf
        if best_etf in bar_dict:
            context.entry_price[best_etf] = bar_dict[best_etf].close
    else:
        if context.hold_etf:
            order_target_value(context.hold_etf, 0)
            context.hold_etf = None

    # 债券仓位
    order_target_value(context.bond_etf, bond_value)
    logger.info(f"股债平衡调仓，股票={best_etf}，评分={best_score:.4f}")
