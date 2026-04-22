# RiceQuant策略 - Debug-输出信息-多标的版ETF策略
# 原文：https://www.joinquant.com/post/48875
# 作者：璐璐202006

import pandas as pd
import numpy as np

def init(context):

    context.etf = [
        '516510.XSHG', '159985.XSHE', '515880.XSHG', '513060.XSHG',
        '512660.XSHG', '513520.XSHG', '513330.XSHG', '515790.XSHG',
        '512100.XSHG', '159998.XSHE', '513500.XSHG', '162719.XSHE',
        '159949.XSHE', '515030.XSHG', '159928.XSHE', '513100.XSHG',
        '159995.XSHE',
    ]

    context.etf_num = 2
    context.change_day = 1
    context.day = 0
    context.min_inc = 0.05
    context.max_inc = 0.2
    context.rank_num = 4
    context.longdays = 20
    context.shortdays = 5
    context.buy_etf = []
    context.sell_etf = []
    context.previous_total_value = context.portfolio.starting_cash

    scheduler.run_daily(check_etf, time_rule=market_open(minute=0))
    scheduler.run_daily(trade, time_rule=market_open(minute=0))
    scheduler.run_daily(print_position_info, time_rule=market_close(minute=10))


def handle_bar(context, bar_dict):
    pass


def calculate_etf_metrics(context, etf_list, long_days, short_days):
    malong = []
    mashort = []
    inclong = []
    valid_etfs = []

    for etf in etf_list:
        data = history_bars(etf, long_days, '1d', 'close')
        if data is None or len(data) < long_days:
            continue
        inclong.append((data[-1] / data[0] - 1) if data[0] != 0 else 0)
        malong.append(np.mean(data))
        mashort.append(np.mean(data[-short_days:]))
        valid_etfs.append(etf)

    d = {'inc': inclong, 'malong': malong, 'mashort': mashort}
    df = pd.DataFrame(data=d, index=valid_etfs)
    return df


def check_etf(context, bar_dict):
    df = calculate_etf_metrics(context, context.etf, context.longdays, context.shortdays)
    df = df.sort_values(by='inc', ascending=False)

    df1 = df[(df['mashort'] > df['malong']) & (df['inc'] > context.min_inc) & (df['inc'] < context.max_inc)]
    context.buy_etf = list(df1.index)[:context.etf_num]
    context.sell_etf = []

    rank_etf = list(df.index)[:context.rank_num]

    for etf in list(context.portfolio.positions):
        etf_inc = df['inc'][etf] if etf in df.index else 0  # FIX: Series doesn't have .get()
        if etf not in rank_etf or (etf_inc > context.max_inc):
            if etf not in context.buy_etf:
                context.sell_etf.append(etf)
        if etf in context.buy_etf and etf not in context.sell_etf:
            context.buy_etf.remove(etf)

    print("-" * 50)
    for i in range(len(df)):
        etf = df.index[i]
        info = instruments(etf)
        name = info.symbol if info else etf
        print("{}. {}，5日均线：{:.2f}，20日均线：{:.2f}，20日涨幅：{:.2%}".format(
            i + 1, name, float(df.iloc[i]['mashort']), float(df.iloc[i]['malong']), float(df.iloc[i]['inc'])
        ))
    print("-" * 50)


def trade(context, bar_dict):
    if context.day % context.change_day == 0:
        for etf in context.sell_etf:
            order_target_value(etf, 0)

        position_count = len(context.portfolio.positions)
        if context.etf_num > position_count:
            cash = context.portfolio.cash / (context.etf_num - position_count)
            for etf in context.buy_etf:
                order_target_value(etf, cash)
                if len(context.portfolio.positions) == context.etf_num:
                    break

    context.day += 1


def print_position_info(context, bar_dict):
    print("-" * 50)
    for position in list(context.portfolio.positions.values()):
        security = position.order_book_id
        info = instruments(security)
        name = info.symbol if info else security
        bar = (bar_dict[security] if security in bar_dict else None) if bar_dict else None
        last_price = bar.close if bar is not None and bar.is_trading else position.avg_price
        pnl_pct = (last_price / position.avg_price - 1) * 100 if position.avg_price > 0 else 0
        print("代码: {}，成本: {:.2f}，现价: {:.2f}，收益: {:.2f}%".format(
            name, position.avg_price, last_price, pnl_pct
        ))

    total_return_rate = (context.portfolio.total_value - context.portfolio.starting_cash) / context.portfolio.starting_cash * 100
    print("累计收益率={:.2f}%".format(total_return_rate))

    if context.previous_total_value:
        daily_return_rate = (context.portfolio.total_value / context.previous_total_value - 1) * 100
        print("今日收益率={:.2f}%".format(daily_return_rate))

    context.previous_total_value = context.portfolio.total_value
    print("-" * 50)
