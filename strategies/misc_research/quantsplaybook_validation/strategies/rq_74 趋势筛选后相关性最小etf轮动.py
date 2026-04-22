# RiceQuant Python格式策略
# 来源: JoinQuant - 74 趋势筛选后相关性最小etf轮动
# 克隆自聚宽文章：https://www.joinquant.com/post/49507
# 标题：趋势筛选后相关性最小etf轮动
# 作者：蚂蚁量化

# eft池来源：
# 原文网址：https://www.joinquant.com/view/community/detail/cd4f11534d06711f53b4bad1f5105f09?type=1
# 标题：手把手教你构建ETF策略候选池
# 作者：JoelZ

# 本人修改：
# 1. 添加了从历史数据中筛选维持多头趋势性较强的品种
# 2. 添加了'score'的上下限-0.5<'score'<4.5，避免买入过强或过弱的etf

import numpy as np
import pandas as pd
import math

def init(context):

    # 设置交易成本

    context.etf_pool = ['512660.XSHG', '510880.XSHG', '159915.XSHE', '513050.XSHG', '510050.XSHG', '588100.XSHG', '512100.XSHG', '518800.XSHG', '513060.XSHG', '511010.XSHG', '512980.XSHG', '512010.XSHG', '513100.XSHG', '512720.XSHG',
                    '512070.XSHG', '515880.XSHG', '159920.XSHE', '159922.XSHE', '513520.XSHG', '515000.XSHG', '515790.XSHG', '515700.XSHG', '159825.XSHE', '512400.XSHG', '512200.XSHG', '513360.XSHG', '512480.XSHG', '510230.XSHG', '159647.XSHE', '159928.XSHE']
    context.m_days = 25

    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def min_corr(stocks):
    nday = 243
    price_dict = {}
    for stock in stocks:
        try:
            bars = history_bars(stock, nday, '1d', 'close')
            if bars is not None and len(bars) == nday:
                price_dict[stock] = bars
        except Exception:
            continue
    if len(price_dict) < 2:
        return stocks[:4]
    df = pd.DataFrame(price_dict)
    df = df.dropna(axis=1)
    r = np.log(df).diff()[1:]
    m_corr = r.corr()
    corr_mean = {}
    for stock in m_corr.columns:
        corr_mean[stock] = m_corr[stock].abs().mean()
    etf_pool = sorted(corr_mean, key=corr_mean.get)[:4]
    return etf_pool

def get_rank(etf_pool, m_days):
    score_list = []
    for etf in etf_pool:
        close_prices = history_bars(etf, m_days, '1d', 'close')
        if close_prices is None or len(close_prices) == 0:
            continue
        y = np.log(close_prices)
        x = np.arange(y.size)
        slope, intercept = np.polyfit(x, y, 1)
        annualized_returns = math.pow(math.exp(slope), 250) - 1
        r_squared = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
        score = annualized_returns * r_squared
        score_list.append(score)
    df_score = pd.DataFrame(index=etf_pool, data={'score': score_list})
    df_score = df_score.sort_values(by='score', ascending=False)
    df_score = df_score[(df_score['score'] > -0.5) & (df_score['score'] < 4.5)]
    rank_list = list(df_score.index)

    return rank_list


# 交易
def trade(context, bar_dict):
    target_num = 1
    etf_pool = get_trend_length(context.etf_pool, 3)
    etf_pool = min_corr(etf_pool)
    target_list = get_rank(etf_pool, context.m_days)[:target_num]

    # 卖出
    hold_list = list(context.portfolio.positions)
    for etf in hold_list:
        if etf not in target_list:
            order_target_value(etf, 0)
    # 买入
    hold_list = list(context.portfolio.positions)
    if len(hold_list) < target_num:
        value = context.portfolio.cash / (target_num - len(hold_list))
        for etf in target_list:
            pos = context.portfolio.positions.get(etf)
            if pos is None or pos.quantity == 0:
                order_target_value(etf, value)
    hold_list = list(context.portfolio.positions)
    if hold_list:
        print('- 持有:  %s, %s' % (mingcheng(hold_list[0]), hold_list[0]))

# 本人添加程序

def calculate_ma(data, window):
    return data.rolling(window=window).mean()

def count_days_above(data, short_window, long_window):
    # 计算短期和长期均线
    short_ma = calculate_ma(data, short_window)
    long_ma = calculate_ma(data, long_window)

    # 初始化计数器
    count = 0
    total_days = 0

    for i in range(long_window, len(data)):
        if short_ma[i] > long_ma[i]:
            if i == long_window or short_ma[i-1] <= long_ma[i-1]:
                count = 0
            count += 1
        else:
            count = 0

        if count > 0:
            total_days += count

    return total_days / (len(data) - long_window)

def get_trend_length(etf_pool, limit):
    nday = 3500
    price_dict = {}
    for stock in etf_pool:
        try:
            bars = history_bars(stock, nday, '1d', 'close')
            if bars is not None and len(bars) > 0:
                price_dict[stock] = bars
        except Exception:
            continue
    if not price_dict:
        return etf_pool
    # Align lengths
    min_len = min(len(v) for v in price_dict.values())
    df = pd.DataFrame({k: v[-min_len:] for k, v in price_dict.items()})

    stocks_data = {stock: df[stock] for stock in df.columns}

    # 短期和长期均线窗口
    short_window = 10
    long_window = 30

    # 统计每只股票的数据
    results = {stock: count_days_above(data, short_window, long_window) for stock, data in stocks_data.items()}
    results = {stock: results[stock] for stock in results if results[stock] > limit}
    return list(results.keys())


def mingcheng(stock):
    try:
        return instruments(stock).display_name
    except Exception:
        return "还未上市"
