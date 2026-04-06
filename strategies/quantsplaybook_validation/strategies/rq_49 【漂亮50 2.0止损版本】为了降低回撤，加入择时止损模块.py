# 原文链接：https://www.joinquant.com/post/49xxx
# 策略：漂亮50 2.0止损版本
# 核心逻辑：漂亮50（大市值高ROE低PE），加入MACD择时止损，跌破止损线时清仓

import numpy as np

HOLD_NUM = 10
STOP_LOSS_RATIO = 0.08  # 8%止损

def ema(p, n):
    k = 2.0 / (n + 1); e = p[0]; r = []
    for x in p: e = x * k + e * (1 - k); r.append(e)
    return np.array(r)

def calc_macd(p, f=12, s=26, sig=9):
    d = ema(p, f) - ema(p, s)
    return d, ema(d, sig), (d - ema(d, sig)) * 2

def init(context):
    context.index = '000300.XSHG'
    context.buy_prices = {}
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))
    scheduler.run_daily(check_stop_loss, time_rule=market_open(minute=60))

def handle_bar(context, bar_dict):
    pass

def check_stop_loss(context, bar_dict):
    """每日检查止损"""
    # 大盘MACD择时
    closes = history_bars('000300.XSHG', 35, '1d', 'close')
    if len(closes) < 35:
        return
    macd, signal, hist = calc_macd(closes)
    # MACD死叉，清仓
    if macd[-1] < signal[-1] and macd[-2] >= signal[-2]:
        logger.info("MACD死叉，清仓止损")
        for stock in list(context.portfolio.positions.keys()):
            order_target_value(stock, 0)
        return

    # 个股止损
    for stock, pos in list(context.portfolio.positions.items()):
        buy_price = context.buy_prices.get(stock, pos.avg_cost)
        current_price = bar_dict[stock].close if stock in bar_dict else pos.price
        if (current_price - buy_price) / buy_price < -STOP_LOSS_RATIO:
            logger.info(f"{stock} 触发止损，卖出")
            order_target_value(stock, 0)

def rebalance(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        order_target_value(stock, 0)

    instruments_df = all_instruments('CS')
    stocks = instruments_df['order_book_id'].tolist()
    prev_date = context.now.date()

    try:
        factor_df = get_factor(
            stocks,
            ['market_cap', 'pe_ratio', 'roe'],
        )
    except Exception as e:
        logger.info(f"获取数据失败: {e}")
        return

    if factor_df is None or len(factor_df) == 0:
        return

    df = factor_df.groupby(level=0).last().dropna()
    df = df[df['market_cap'] > 5e10]  # 大市值 > 500亿
    df = df[df['pe_ratio'] > 0]
    df = df[df['pe_ratio'] < 30]
    df = df[df['roe'] > 0.15]
    df = df.sort_values('market_cap', ascending=False).head(50)
    if df.empty:
        return

    df['score'] = df['roe'] / df['pe_ratio']
    df = df.sort_values('score', ascending=False)
    selected = df.index.tolist()[:HOLD_NUM]
    value_per = context.portfolio.cash / len(selected) if selected else 0

    for stock in selected:
        order_target_value(stock, value_per)
        context.buy_prices[stock] = bar_dict[stock].close if stock in bar_dict else 0
        logger.info(f"买入 {stock}")
