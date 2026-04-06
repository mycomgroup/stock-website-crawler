# 原文链接：https://www.joinquant.com/post/62002
# 策略：基金溢价模拟效果好
# 核心逻辑：基金溢价策略，选折价率最高的LOF/ETF基金买入，等待溢价回归。

import numpy as np

def ema(p, n):
    k=2.0/(n+1); e=p[0]; r=[]
    for x in p: e=x*k+e*(1-k); r.append(e)
    return np.array(r)

def init(context):
    # 常见LOF/ETF基金池（用ETF代替，选折价较大的）
    context.fund_pool = [
        '510300.XSHG',  # 沪深300ETF
        '510500.XSHG',  # 中证500ETF
        '159915.XSHE',  # 创业板ETF
        '511010.XSHG',  # 国债ETF
        '518880.XSHG',  # 黄金ETF
        '159938.XSHE',  # 消费ETF
        '512760.XSHG',  # 芯片ETF
        '515030.XSHG',  # 新能源ETF
        '159825.XSHE',  # 农业ETF
        '512800.XSHG',  # 银行ETF
    ]
    context.hold_fund = None
    context.n_hold = 3
    scheduler.run_monthly(rebalance, tradingday=1, time_rule=market_open(minute=30))

def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    # 用近期跌幅最大的ETF模拟折价（跌幅大=折价大，等待回归）
    discount_scores = {}
    for fund in context.fund_pool:
        try:
            closes = history_bars(fund, 21, '1d', 'close')
            if closes is not None and len(closes) >= 21:
                # 近20日跌幅（折价程度）
                drawdown = (closes[-1] - closes[0]) / closes[0]
                discount_scores[fund] = drawdown  # 越负越折价
        except Exception:
            continue

    if not discount_scores:
        return

    # 选折价最大（跌幅最大）的基金
    sorted_funds = sorted(discount_scores, key=discount_scores.get, reverse=False)
    target = sorted_funds[:context.n_hold]

    # 过滤：只选跌幅在-30%~0%之间的（真正折价，不是趋势下跌）
    target = [f for f in target if -0.3 < discount_scores[f] < 0]

    if not target:
        logger.info("无合适折价基金")
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        return

    for s in list(context.portfolio.positions.keys()):
        if s not in target:
            order_target_value(s, 0)

    n = len(target)
    value = context.portfolio.total_value * 0.95 / n
    for f in target:
        if f in bar_dict and bar_dict[f].is_trading:
            order_target_value(f, value)
    logger.info(f"基金折价策略，持仓: {target}")
