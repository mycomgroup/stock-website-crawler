# RiceQuant策略 - 折价基金统计套利
# 原文：https://www.joinquant.com/post/35737
# 作者：Gyro
# 注意：原策略用 get_price(unit_net_value) 获取基金净值，RiceQuant 不支持该字段，
# 此版本改用昨日收盘价近似净值（与 rq_76 ETF基金溢价策略同样的思路）。

import pandas as pd

def init(context):

    context.num = 30
    context.buy_list = []
    context.last_adjust_week = -1
    context.last_sell_week = -1

    scheduler.run_daily(weekly_adjust, time_rule=market_open(minute=0))
    scheduler.run_daily(weekly_sell, time_rule=market_close(minute=10))


def handle_bar(context, bar_dict):
    pass


def weekly_adjust(context, bar_dict):
    """每周执行一次（周一或首个交易日）"""
    today = context.now
    week = today.isocalendar()[1]
    if week == context.last_adjust_week:
        return
    context.last_adjust_week = week
    adjust(context, bar_dict)


def weekly_sell(context, bar_dict):
    """每周末执行一次（周五或末个交易日）"""
    today = context.now
    week = today.isocalendar()[1]
    # 在每周最后一个交易日卖出（周四或周五）
    if today.weekday() not in (3, 4) or week == context.last_sell_week:
        return
    context.last_sell_week = week
    sell(context, bar_dict)


def adjust(context, bar_dict):
    all_lof_df = pd.concat([all_instruments('LOF'), all_instruments('ETF')], ignore_index=True)
    lofs_list = all_lof_df.index.tolist()

    # 用昨日收盘价近似净值（RiceQuant 不提供实时净值）
    net_value_dict = {}
    for stock in lofs_list:
        try:
            bars = history_bars(stock, 2, '1d', 'close')
            if bars is not None and len(bars) >= 2:
                net_value_dict[stock] = bars[-2]  # 昨日收盘价作为净值近似
        except Exception:
            continue
    net_value = pd.Series(net_value_dict, name='unit_net_value')

    # 获取收盘价
    close_prices = {}
    for stock in lofs_list:
        try:
            bars = history_bars(stock, 1, '1d', 'close')
            if bars is not None and len(bars) > 0:
                close_prices[stock] = bars[-1]
        except Exception:
            continue

    close_df = pd.Series(close_prices, name='close')
    close_df = close_df[close_df < 10].dropna()

    if len(close_df) == 0 or len(net_value) == 0:
        print('数据不足，跳过')
        return

    val = pd.DataFrame({'close': close_df, 'unit_net_value': net_value}).dropna()
    val['score'] = val['close'] / val['unit_net_value']
    val = val[(val['score'] > 0) & (val['score'] < 0.99)]
    val = val.sort_values('score', ascending=True).head(context.num)
    print('待买列表: %s' % val)

    buy_list = val.index.tolist()
    context.buy_list = buy_list

    if buy_list and context.portfolio.cash > 500:
        buy_value = context.portfolio.total_value / len(buy_list)
        for f in buy_list:
            order_target_value(f, buy_value)
            print('买入%s，金额%s元' % (f, buy_value))
    else:
        print('buy_list为空或资金不足')


def sell(context, bar_dict):
    for f in list(context.portfolio.positions.keys()):
        if f not in context.buy_list:
            print('清仓%s' % f)
            order_target_value(f, 0)
