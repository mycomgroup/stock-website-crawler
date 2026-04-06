# RiceQuant Python格式策略
# 来源: JoinQuant - 74 趋势筛选后相关性最小etf轮动
# 克隆自聚宽文章：https://www.joinquant.com/post/49507
# 标题：趋势筛选后相关性最小etf轮动
# 作者：蚂蚁量化

import numpy as np
import pandas as pd
import math


def init(context):


    context.etf_pool = ['512660.XSHG', '510880.XSHG', '159915.XSHE', '513050.XSHG', '510050.XSHG', '588100.XSHG', '512100.XSHG', '518800.XSHG', '513060.XSHG', '511010.XSHG', '512980.XSHG', '512010.XSHG', '513100.XSHG', '512720.XSHG',
                        '512070.XSHG', '515880.XSHG', '159920.XSHE', '159922.XSHE', '513520.XSHG', '515000.XSHG', '515790.XSHG', '515700.XSHG', '159825.XSHE', '512400.XSHG', '512200.XSHG', '513360.XSHG', '512480.XSHG', '510230.XSHG', '159647.XSHE', '159928.XSHE']
    context.m_days = 25

    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def handle_bar(context, bar_dict):
    pass


def min_corr(stocks):
    nday = 243
    # history_bars does not support list - collect per stock
    close_data_dict = {}
    for _s in stocks:
        _bars = history_bars(_s, nday, "1d", "close")
        if _bars is not None and len(_bars) >= nday:
            close_data_dict[_s] = _bars
    close_data = close_data_dict  # dict: stock -> array
    # 转换为DataFrame便于处理
    df = pd.DataFrame(close_data)
    df = df.dropna(axis=1)
    p = df.copy()
    r = np.log(p).diff()[1:]
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
        log_prices = np.log(close_prices)
        x = np.arange(len(log_prices))
        slope, intercept = np.polyfit(x, log_prices, 1)
        annualized_returns = math.pow(math.exp(slope), 250) - 1
        r_squared = 1 - (sum((log_prices - (slope * x + intercept)) ** 2) / ((len(log_prices) - 1) * np.var(log_prices, ddof=1)))
        score = annualized_returns * r_squared
        score_list.append(score)
    df = pd.DataFrame(index=etf_pool, data={'score': score_list})
    df = df.sort_values(by='score', ascending=False)
    df = df[(df['score'] > -0.5) & (df['score'] < 4.5)]
    rank_list = list(df.index)

    return rank_list


def get_trend_length(etf_pool, limit, m_days):
    # history_bars does not support list input - collect per stock
    stocks_data = {}
    for _s in etf_pool:
        try:
            _bars = history_bars(_s, 3500, '1d', 'close')
            if _bars is not None and len(_bars) > 0:
                stocks_data[_s] = list(_bars)
        except Exception:
            continue

    short_window = 10
    long_window = 30

    def count_days_above(data):
        short_ma = pd.Series(data).rolling(window=short_window).mean()
        long_ma = pd.Series(data).rolling(window=long_window).mean()

        count = 0
        total_days = 0

        for i in range(long_window, len(data)):
            if short_ma[i] > long_ma[i]:
                if i == long_window or short_ma[i - 1] <= long_ma[i - 1]:
                    count = 0
                count += 1
            else:
                count = 0

            if count > 0:
                total_days += count

        return total_days / (len(data) - long_window) if len(data) > long_window else 0

    results = {stock: count_days_above(stocks_data[stock]) for stock in stocks_data}
    results = {stock: results[stock] for stock in results if results[stock] > limit}
    return list(results.keys())


def trade(context, bar_dict):
    target_num = 1
    etf_pool = get_trend_length(context.etf_pool, 3, context.m_days)
    etf_pool = min_corr(etf_pool)
    target_list = get_rank(etf_pool, context.m_days)[:target_num]

    hold_list = list(context.portfolio.positions)
    for etf in hold_list:
        if etf not in target_list:
            order_target_value(etf, 0)

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


def mingcheng(stock):
    try:
        return instruments(stock).display_name
    except Exception:
        return "还未上市"
