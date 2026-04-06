# RiceQuant策略迁移 - Fixed for RiceQuant API
# 原文标题：ETF策略之核心资产轮动（线性增加权重）
# 原文作者：MarioC
# 原文网址：https://www.joinquant.com/post/47888

import numpy as np
import pandas as pd
import math


def init(context):
    # 设定基准
    context.benchmark = '000300.XSHG'
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
    context.m_days = 25  # 动量参考天数
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def MOM(context, etf):
    """计算动量分数"""
    closes = history_bars(etf, context.m_days, '1d', 'close')
    if closes is None or len(closes) == 0:
        return 0

    y = np.log(closes)
    n = len(y)
    x = np.arange(n)
    weights = np.linspace(1, 2, n)  # 线性增加权重
    slope, intercept = np.polyfit(x, y, 1, w=weights)
    annualized_returns = math.exp(slope) ** 250 - 1
    residuals = y - (slope * x + intercept)
    weighted_residuals = weights * residuals ** 2
    r_squared = 1 - (np.sum(weighted_residuals) / np.sum(weights * (y - np.mean(y)) ** 2))
    score = annualized_returns * r_squared
    return score


def get_rank(context, etf_pool):
    """基于年化收益和判定系数打分的动量因子轮动"""
    score_list = []
    for etf in etf_pool:
        score = MOM(context, etf)
        score_list.append(score)
    df = pd.DataFrame(index=etf_pool, data={'score': score_list})
    df = df.sort_values(by='score', ascending=False)
    rank_list = list(df.index)
    return rank_list


def trade(context, bar_dict):
    """交易"""
    # 获取动量最高的一只ETF
    target_num = 1
    target_list = get_rank(context, context.etf_pool)[:target_num]

    # 卖出
    hold_list = list(context.portfolio.positions.keys())
    for etf in hold_list:
        if etf not in target_list:
            order_target_value(etf, 0)
            print('卖出' + str(etf))
        else:
            print('继续持有' + str(etf))

    # 买入
    hold_list = list(context.portfolio.positions.keys())
    if len(hold_list) < target_num:
        value = context.portfolio.cash / (target_num - len(hold_list))
        for etf in target_list:
            position = context.portfolio.positions.get(etf)
            if position is None or position.quantity == 0:
                order_target_value(etf, value)
                print('买入' + str(etf))
