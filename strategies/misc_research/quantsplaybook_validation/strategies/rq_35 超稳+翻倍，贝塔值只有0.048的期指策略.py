# 原文链接：https://www.joinquant.com/post/超稳翻倍贝塔值只有0.048的期指策略
# 策略：超稳+翻倍，贝塔值只有0.048的期指策略
# 核心逻辑：用沪深300ETF(510300)做CTA趋势跟踪，RSRS择时，低贝塔配置。

import numpy as np

def calc_rsrs(high, low, n=18):
    x = np.array(low[-n:]); y = np.array(high[-n:])
    b = np.polyfit(x, y, 1); return b[0]

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    context.etf = '510300.XSHG'
    context.bond_etf = '511010.XSHG'
    context.rsrs_threshold = 1.0
    context.position_ratio = 0.5  # 低贝塔：只用50%仓位
    context.in_market = False
    scheduler.run_daily(check_signal, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def check_signal(context, bar_dict):
    try:
        high = history_bars(context.etf, 25, '1d', 'high')
        low = history_bars(context.etf, 25, '1d', 'low')
        prices = history_bars(context.etf, 25, '1d', 'close')
        if len(high) < 20:
            return
        rsrs = calc_rsrs(high, low, 18)
    except Exception:
        return

    # RSRS趋势信号
    ma20 = np.mean(prices[-20:])
    current_price = prices[-1]

    if rsrs > context.rsrs_threshold and current_price > ma20:
        if not context.in_market:
            if context.bond_etf in context.portfolio.positions:
                order_target_value(context.bond_etf, 0)
            order_target_value(context.etf, context.portfolio.total_value * context.position_ratio)
            # 剩余仓位持债
            order_target_value(context.bond_etf, context.portfolio.total_value * (0.95 - context.position_ratio))
            context.in_market = True
            logger.info(f"RSRS={rsrs:.2f}，趋势向上，持有ETF+债券低贝塔组合")
    else:
        if context.in_market:
            order_target_value(context.etf, 0)
            order_target_value(context.bond_etf, context.portfolio.total_value * 0.95)
            context.in_market = False
            logger.info(f"RSRS={rsrs:.2f}，趋势向下，切换全债")
