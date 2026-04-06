# ETF动量轮动评分策略 - RiceQuant版本
# 原文：从相关系数角度探讨etf轮动高评分
# 作者：wywy1995
# 原文：https://www.joinquant.com/post/34475
# 逻辑：对ETF池按年化收益*R²评分，选最高分持仓

import numpy as np
import math
import pandas as pd


ETF_POOL = [
    '510330.XSHG',  # 沪深300ETF华夏（原上证180ETF已退市）
    '159915.XSHE',  # 创业板100
    '513100.XSHG',  # 纳指100
]


def get_rank(etf_pool, momentum_day=29):
    score_list = []
    valid = []
    for etf in etf_pool:
        try:
            prices = history_bars(etf, momentum_day, '1d', 'close')
            if prices is None or len(prices) < momentum_day:
                continue
            y = np.log(np.array(prices, dtype=float))
            x = np.arange(len(y))
            slope, intercept = np.polyfit(x, y, 1)
            annualized = math.pow(math.exp(slope), 250) - 1
            y_hat = slope * x + intercept
            ss_res = np.sum((y - y_hat) ** 2)
            ss_tot = (len(y) - 1) * np.var(y, ddof=1)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            score_list.append(annualized * r2)
            valid.append(etf)
        except Exception:
            continue

    if not valid:
        return []
    df = pd.DataFrame({'score': score_list}, index=valid)
    return df.sort_values('score', ascending=False).index.tolist()


def init(context):
    context.etf_pool = ETF_POOL
    context.stock_num = 1
    context.momentum_day = 29
    scheduler.run_daily(my_trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def my_trade(context, bar_dict):
    ranked = get_rank(context.etf_pool, context.momentum_day)
    if not ranked:
        return

    target = ranked[:context.stock_num]

    for etf in list(context.portfolio.positions.keys()):
        if etf not in target:
            order_target_value(etf, 0)

    if not target:
        return
    weight = 1.0 / len(target)
    for etf in target:
        bar = (bar_dict[etf] if etf in bar_dict else None)
        if bar is None or not bar.is_trading:
            continue
        order_target_value(etf, context.portfolio.total_value * weight * 0.95)
