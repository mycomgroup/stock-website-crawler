# Migratable ETF Momentum Strategy
# Fixed version for RiceQuant API

"""
RiceQuant Strategy - Migrated from JoinQuant
Original: 安全摸狗策略
Author: MarioC
Clone from: https://www.joinquant.com/post/49263

This is a relatively simple ETF momentum strategy that can be migrated.
Uses history_bars and numpy for momentum calculation.
"""

import numpy as np
import pandas as pd


def init(context):
    # Set benchmark
    context.benchmark = '000300.XSHG'

    # ETF pool
    context.etf_pool = [
        '518880.XSHG',  # Gold ETF
        '513100.XSHG',  # Nasdaq 100 ETF
        '159915.XSHE',  # ChiNext 100 ETF
        '510330.XSHG',  # 沪深300ETF华夏（原上证180ETF已退市）
    ]

    context.m_days = 25  # Momentum lookback days

    # Schedule daily trading
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def MOM(context, etf):
    """Calculate momentum score for ETF"""
    bars = history_bars(etf, context.m_days, '1d', 'close')
    if bars is None or len(bars) < context.m_days:
        return 0

    close_prices = bars
    y = np.log(close_prices)
    n = len(y)
    x = np.arange(n)
    weights = np.linspace(1, 2, n)  # Linear increasing weights

    # Weighted linear regression
    slope, intercept = np.polyfit(x, y, 1, w=weights)
    annualized_returns = np.exp(slope) ** 250 - 1

    residuals = y - (slope * x + intercept)
    weighted_residuals = weights * residuals ** 2
    r_squared = 1 - (np.sum(weighted_residuals) / np.sum(weights * (y - np.mean(y)) ** 2))

    score = annualized_returns * r_squared
    return score


def get_rank(context):
    """Get ETF ranking by momentum score"""
    score_list = []
    for etf in context.etf_pool:
        score = MOM(context, etf)
        score_list.append(score)

    df = pd.DataFrame(index=context.etf_pool, data={'score': score_list})
    df = df.sort_values(by='score', ascending=False)
    # Safe range: momentum not too high or too low
    df = df[(df['score'] > 0) & (df['score'] <= 5)]
    rank_list = list(df.index)

    if len(rank_list) == 0:
        rank_list = []

    return rank_list


def trade(context, bar_dict):
    """Execute trading logic"""
    target_num = 1
    target_list = get_rank(context)[:target_num]

    # Sell
    hold_list = list(context.portfolio.positions.keys())
    for etf in hold_list:
        if etf not in target_list:
            order_target_value(etf, 0)
            print(f'Sell {etf}')
        else:
            print(f'Hold {etf}')

    # Buy
    hold_list = list(context.portfolio.positions.keys())
    if len(hold_list) < target_num:
        cash = context.portfolio.cash
        value = cash / (target_num - len(hold_list))
        for etf in target_list:
            position = context.portfolio.positions.get(etf)
            if position is None or position.quantity == 0:
                order_target_value(etf, value)
                print(f'Buy {etf}')
