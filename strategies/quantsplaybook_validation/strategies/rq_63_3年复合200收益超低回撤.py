# 原文链接：https://www.joinquant.com/post/32630
# 策略：3年复合200+%收益+超低回撤11%以内，无惧大跌（ETF轮动）
# 核心逻辑：ETF池动量轮动 + 成交量风控，每天14:37交易

import numpy as np

ETF_POOL = [
    '159915.XSHE',  # 创业板ETF
    '510300.XSHG',  # 沪深300ETF
    '510500.XSHG',  # 中证500ETF
    '510050.XSHG',  # 上证50ETF
    '510880.XSHG',  # 红利ETF
    '159905.XSHE',  # 深红利
    '159949.XSHE',  # 创业板50
]
MONEY_FUND = '511880.XSHG'  # 货币基金
LAG = 6    # 成交量风控窗口
LAG0 = 7   # 成交量均值窗口
LAG1 = 13  # 动量窗口

def init(context):
    context.etf_pool = ETF_POOL
    scheduler.run_daily(before_open, time_rule=market_open(minute=0))
    scheduler.run_daily(get_signal, time_rule=market_close(minute=23))
    scheduler.run_daily(etf_trade_sell, time_rule=market_close(minute=22))
    scheduler.run_daily(etf_trade_buy, time_rule=market_close(minute=21))


def handle_bar(context, bar_dict):
    pass

def check_volume_signal(context):
    """成交量风控：连续LAG天成交量 < LAG0天均量则空仓"""
    volumes = history_bars('510300.XSHG', LAG0 + 1, '1d', 'volume')
    if volumes is None or len(volumes) < LAG0 + 1:
        return True
    v = np.array(volumes, dtype=float)
    avg_vol = np.mean(v[-LAG0:])
    recent = v[-LAG:]
    if np.all(recent < avg_vol):
        return False  # 空仓信号
    return True  # 正常交易

def get_signal(context, bar_dict):
    if not check_volume_signal(context):
        context.target = MONEY_FUND
        return

    scores = {}
    for etf in context.etf_pool:
        prices = history_bars(etf, LAG1 + 20, '1d', 'close')
        if prices is None or len(prices) < LAG1 + 10:
            continue
        p = np.array(prices, dtype=float)
        momentum = p[-1] / p[-LAG1] - 1
        ma_short = np.mean(p[-5:])
        ma_long  = np.mean(p[-10:])
        ma_diff = ma_short / ma_long - 1
        if momentum > 0 and ma_diff > 0:
            scores[etf] = momentum + ma_diff

    if scores:
        context.target = max(scores, key=scores.get)
    else:
        context.target = MONEY_FUND

def etf_trade_sell(context, bar_dict):
    target = getattr(context, 'target', MONEY_FUND)
    for s in list(context.portfolio.positions.keys()):
        if s != target:
            order_target_value(s, 0)

def etf_trade_buy(context, bar_dict):
    target = getattr(context, 'target', MONEY_FUND)
    order_target_value(target, context.portfolio.total_value * 0.95)

def before_open(context, bar_dict):
    pass
