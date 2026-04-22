# RiceQuant策略迁移 - Fixed for RiceQuant API
# 原文标题：【回顾3】ETF策略之核心资产轮动-增强版
# 原文作者：wywy1995
# 原文网址：https://www.joinquant.com/post/42673

import numpy as np
import pandas as pd
import math


def init(context):
    # 设定基准
    context.benchmark = '513100.XSHG'
    # 用真实价格交易
    # 打开防未来函数
    # 设置滑点
    # 设置交易成本
    # 参数
    context.etf_pool = [
        '518880.XSHG',  # 黄金ETF（大宗商品）
        '513100.XSHG',  # 纳指100（海外资产）
        '159915.XSHE',  # 创业板100（成长股，科技股，中小盘）
        '510330.XSHG',  # 沪深300ETF华夏（原上证180ETF已退市）
    ]
    context.m_days = 25
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def get_rank(context, etf_pool):
    """基于年化收益和判定系数打分的动量因子轮动"""
    score_list = []
    for etf in etf_pool:
        # 每只股票计算分数流程
        closes = history_bars(etf, context.m_days, '1d', 'close')
        if closes is None or len(closes) == 0:
            score_list.append(0)
            continue

        y = np.log(closes)
        x = np.arange(len(y))
        slope, intercept = np.polyfit(x, y, 1)
        annualized_returns = math.exp(slope) ** 250 - 1
        r_squared = 1 - (np.sum((y - (slope * x + intercept)) ** 2) / ((len(y) - 1) * np.var(y, ddof=1)))
        score = annualized_returns * r_squared

        # 加入反转
        closes2 = history_bars(etf, context.m_days * 8, '1d', 'close')
        if closes2 is not None and len(closes2) > 0:
            y2 = np.log(closes2)
            x2 = np.arange(len(y2))
            slope2, intercept2 = np.polyfit(x2, y2, 1)
            annualized_returns2 = math.exp(slope2) ** 250 - 1
            r_squared2 = 1 - (np.sum((y2 - (slope2 * x2 + intercept2)) ** 2) / ((len(y2) - 1) * np.var(y2, ddof=1)))
            score = score - annualized_returns2 * r_squared2 / 6

        score_list.append(score)

    df = pd.DataFrame(index=etf_pool, data={'score': score_list})
    df = df.sort_values(by='score', ascending=False)
    return df


def trade(context, bar_dict):
    """交易"""
    # 获取动量最高的一只ETF
    target_num = 1
    rank_df = get_rank(context, context.etf_pool)
    c = max(list(rank_df.score)) - min(list(rank_df.score))
    if c < 15 and c > 0.1:
        target_list = list(rank_df.index)[0:target_num]
    else:
        target_list = []

    # rsrs择时
    real_target_list = []
    for etf in target_list:
        highs = history_bars(etf, 18, '1d', 'high')
        lows = history_bars(etf, 18, '1d', 'low')
        if highs is not None and lows is not None and len(highs) > 0 and len(lows) > 0:
            coef = np.polyfit(lows, highs, 1)[0]
            if coef > getBeta(context, etf):
                real_target_list.append(etf)
    target_list = real_target_list

    # 卖出
    hold_list = list(context.portfolio.positions.keys())
    for etf in hold_list:
        if etf not in target_list:
            order_target_value(etf, 0)

    # 买入
    if len(target_list) != 0:
        hold_list = list(context.portfolio.positions.keys())
        if len(hold_list) < target_num:
            value = context.portfolio.cash / (target_num - len(hold_list))
            for etf in target_list:
                position = context.portfolio.positions.get(etf)
                if position is None or position.quantity == 0:
                    order_target_value(etf, value)


def getBeta(context, etf):
    """获取Beta值"""
    beta = 0
    if etf == '518880.XSHG':
        beta = countBeta(context, '518880.XSHG')
    if etf == '513100.XSHG':
        beta = countBeta(context, '513100.XSHG')
    if etf == '159915.XSHE':
        beta = countBeta(context, '159915.XSHE')
    if etf == '510330.XSHG':
        beta = countBeta(context, '510330.XSHG')
    return beta


def countBeta(context, etf):
    """计算Beta"""
    highs = history_bars(etf, 250, '1d', 'high')
    lows = history_bars(etf, 250, '1d', 'low')
    if highs is None or lows is None or len(highs) < 21:
        return 0

    betaList = []
    for i in range(len(highs) - 21):
        h_sub = highs[i:i + 20]
        l_sub = lows[i:i + 20]
        if len(h_sub) == 20:
            betaList.append(np.polyfit(l_sub, h_sub, 1)[0])
    if len(betaList) == 0:
        return 0
    return np.mean(betaList) - 2 * np.std(betaList)
