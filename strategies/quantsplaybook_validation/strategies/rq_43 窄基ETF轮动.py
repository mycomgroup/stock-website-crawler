# RiceQuant策略迁移 - Fixed for RiceQuant API
# 原文标题：ETF轮动：年化收益82.68%，最大回撤13.54%
# 原文作者：小武子
# 原文网址：https://www.joinquant.com/post/43083

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

    context.etf_pool = [
        '161725.XSHE',  # 白酒
        '159992.XSHE',  # 创新药
        '159647.XSHE',  # 中药ETF
        '515700.XSHG',  # 新能源车
        '159980.XSHE',  # 有色金属
        '515790.XSHG',  # 光伏
        '515880.XSHG',  # 通信
        '159819.XSHE',  # 人工智能
        '512720.XSHG',  # 计算机（云计算，大数据）
        '159740.XSHE',  # 恒生科技
        '159985.XSHE',  # 豆粕
        '162411.XSHE',  # 华宝油气
        '518880.XSHG',  # 黄金ETF（大宗商品）
        '513100.XSHG',  # 纳指100（海外资产）
    ]
    context.m_days = 25  # 动量参考天数
    scheduler.run_daily(trade, time_rule=market_open(minute=40))


def handle_bar(context, bar_dict):
    pass


def get_rank(context, etf_pool):
    """基于年化收益和判定系数打分的动量因子轮动"""
    score_list = []
    for etf in etf_pool:
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
        score_list.append(score)

    df = pd.DataFrame(index=etf_pool, data={'score': score_list})
    df = df.sort_values(by='score', ascending=False)
    rank_list = list(df.index)
    print(df)
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
