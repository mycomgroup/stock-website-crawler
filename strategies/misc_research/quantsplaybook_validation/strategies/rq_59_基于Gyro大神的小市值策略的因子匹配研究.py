# RiceQuant策略迁移 - Fixed for RiceQuant API
# 原文：https://www.joinquant.com/post/45272
# 作者：热情的刀
# 克隆自JoinQuant策略

import pandas as pd


def init(context):
    # 设置系统
    context.days = 0
    context.choice = []
    context.position_size = 0

    scheduler.run_daily(iUpdate, time_rule=market_open(minute=30))
    scheduler.run_daily(iTrader, time_rule=market_open(minute=35))
    scheduler.run_daily(iReport, time_rule=market_close(minute=30))



def handle_bar(context, bar_dict):
    pass

def iUpdate(context, bar_dict):
    """更新选股列表"""
    # 参数
    nchoice = 10
    nposition = 5

    # 全部A股
    all_stock = all_instruments('CS')['order_book_id'].tolist()

    # 过滤ST
    stocks = [s for s in all_stock if instruments(s) and instruments(s).special_type not in ('ST', '*ST')]

    # 过滤68,8,900
    stocks = [stock for stock in stocks if not stock.startswith('8') and not stock.startswith('688') and not stock.startswith('9')]

    # 获取上一个交易日的日期
    previous_trade_day = context.now.date()

    # 用 get_fundamentals 获取因子数据
    try:
        prev_date = context.now.date()
        prev_date = context.now.date()
        factor_df = get_factor(
            stocks,
            ['pb_ratio', 'market_cap', 'circulating_market_cap', 'roe', 'roa']
        )
        if factor_df is None or factor_df.empty:
            return
        df = factor_df.groupby(level=0).last().dropna()
        df = df[df['pb_ratio'] > 0.0]
        df = df[df['roe'] > 0.0]
        df = df.head(500)
        candidates = df.index.tolist()
    except Exception:
        context.choice = []
        return
    if df is None or len(df) == 0:
        context.choice = []
        return

    df = df.dropna()

    circulating_cap_list = sorted(df['circulating_market_cap'].tolist())
    circulating_cap_list = drop_outlier(circulating_cap_list)
    circulating_cap_list = divide_list_into_10(circulating_cap_list)

    if len(circulating_cap_list) < 2:
        context.choice = []
        return

    filtered = df[
        (df['pb_ratio'] > 0) &
        (df['circulating_market_cap'] > circulating_cap_list[0]) &
        (df['circulating_market_cap'] < circulating_cap_list[1]) &
        (df['roe'] > 0.00) &
        (df['roa'] > 0.45)
    ]
    filtered = filtered.sort_values('market_cap', ascending=True).head(nchoice)

    context.choice = filtered.index.tolist()
    print(context.choice)
    context.position_size = 1.0 / nposition * context.portfolio.total_value


def drop_outlier(data_list):
    """将传入的列表中去掉极值"""
    data_list.sort()
    q1 = data_list[int(len(data_list) / 4)]
    q3 = data_list[int(len(data_list) * 3 / 4)]
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    return [x for x in data_list if low <= x <= high]


def divide_list_into_10(data_list):
    """将传入的列表中的值等分成10份，并返回一个列表"""
    data_list.sort()
    chunk_size = len(data_list) // 10
    lst_of_chunks = [data_list[i:i+chunk_size] for i in range(0, len(data_list), chunk_size)]
    return [min(chunk) for chunk in lst_of_chunks if chunk]


def iTrader(context, bar_dict):
    """交易函数"""
    choice = context.choice
    position_size = context.position_size
    lm_value = 0.8 * position_size
    hm_value = 1.2 * position_size

    # 卖出
    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions.get(s)
        if pos is None:
            continue
        last_price = bar_dict[s].close
        _pre_s = history_bars(s, 2, '1d', 'close')
        high_limit = _pre_s[-1] * 1.1 if _pre_s is not None and len(_pre_s) > 0 else None
        _pre_s = history_bars(s, 2, '1d', 'close')
        low_limit = _pre_s[-1] * 0.9 if _pre_s is not None and len(_pre_s) > 0 else None

        if (s not in bar_dict or
            not bar_dict[s].is_trading or
            last_price >= high_limit or
            last_price <= low_limit):
            continue
        if s not in choice:
            print('sell', s, instruments(s).symbol)
            order_target_value(s, 0)

    # 买进
    for s in choice:
        if context.portfolio.cash < position_size:
            break
        if (s not in bar_dict or
            not bar_dict[s].is_trading or
            bar_dict[s].close >= (lambda _b: _b[-1] * 1.1 if _b is not None and len(_b) > 0 else None)(history_bars(s, 2, '1d', 'close')) or
            bar_dict[s].close <= (lambda _b: _b[-1] * 0.9 if _b is not None and len(_b) > 0 else None)(history_bars(s, 2, '1d', 'close'))):
            continue
        if s not in context.portfolio.positions:
            print('buy', s, instruments(s).symbol)
            order_target_value(s, position_size)
        else:
            pos = context.portfolio.positions.get(s)
            if pos is not None and pos.market_value < lm_value:
                print('balance+', s, instruments(s).symbol)
                order_target_value(s, position_size)
            elif pos is not None and pos.market_value > hm_value:
                print('balance-', s, instruments(s).symbol)
                order_target_value(s, position_size)


def iReport(context, bar_dict):
    """报告状态"""
    context.days += 1
    total_return = 0
    if context.portfolio.starting_cash:
        total_return = (
            (context.portfolio.total_value - context.portfolio.starting_cash)
            / context.portfolio.starting_cash
        )
    print(' positions: %d' % len(context.portfolio.positions))
    print(' return: %.2f' % (100 * total_return))
    print(' cash: %.2f' % (context.portfolio.cash / 10000))
    print(' value: %.2f' % (context.portfolio.total_value / 10000))
    print(' running days: %d' % context.days)
