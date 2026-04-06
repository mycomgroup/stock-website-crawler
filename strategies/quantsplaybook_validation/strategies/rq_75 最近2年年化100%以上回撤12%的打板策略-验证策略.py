# 风险及免责提示：该策略由聚宽用户在聚宽社区分享，仅供学习交流使用。
# 原文一般包含策略说明，如有疑问请到原文和作者交流讨论。
# 原文网址：https://www.joinquant.com/post/28552
# 标题：最近2年年化100%以上回撤12%的打板策略-验证策略
# 作者：大思维者

import json
from datetime import timedelta

def init(context):
    print('初始函数开始运行且全局只运行一次')
    context.buy_list = []
    context.minute = 60
    context.buy_stock_count = 10
    context.limit_lists = []
    context.position_count = []
    context.number_of_positions = 0

    scheduler.run_daily(before_open, time_rule=market_open(minute=30))
    scheduler.run_daily(scan_limit_up, time_rule=market_open(minute=0))
    scheduler.run_daily(Screening_stock_purchases, time_rule=market_open(minute=90))
    scheduler.run_daily(sell, time_rule=market_open(minute=60))


def handle_bar(context, bar_dict):
    pass


def before_open(context, bar_dict):
    context.open_positions = len(context.portfolio.positions)
    context.open_time = context.now
    context.limit_lists = []  # Reset daily
    print('===================================================')
    print('开盘持仓数：%s' % context.open_positions)


def scan_limit_up(context, bar_dict):
    """Scan for stocks that hit limit-up at open (replacing zt() which was skipped)"""
    _instr = all_instruments('CS')
    all_stocks = [s for s in _instr['order_book_id'].tolist()
                  if not s.startswith(('688', '3', '4', '8'))]
    limit_lists = []
    for stock in all_stocks:
        try:
            bar = (bar_dict[stock] if stock in bar_dict else None)
            if bar is None or not bar.is_trading:
                continue
            # Check if stock hit limit-up (close == high_limit)
            if bar.close >= bar.high_limit * 0.999:
                # Record stock and minute (0 = at open)
                limit_lists.append([stock, 0, 0])
        except Exception:
            continue
    context.limit_lists = limit_lists
    print('涨停股数量：%s' % len(limit_lists))


def Screening_stock_purchases(context, bar_dict):
    QA = all_instruments('CS')['order_book_id'].tolist()
    QA = filter_specials(context, QA, bar_dict)
    print('')
    print('今日筛选股票池数量：', len(QA))

    before_selling_list = before_selling(context, QA, context.minute, context.limit_lists)
    print('卖出时间之前：数量：%s' % len(before_selling_list), before_selling_list)
    before_selling_list = before_selling_list[:context.buy_stock_count - context.open_positions]

    after_selling_list = after_selling(context, QA, context.minute, context.limit_lists)
    print('卖出时间之后：数量：%s' % len(after_selling_list), after_selling_list)

    for stock_and_time in before_selling_list:
        if context.number_of_positions < 10:
            buy(context, stock_and_time, bar_dict)
            context.number_of_positions += 1
            print('当前持仓数量：', context.number_of_positions, stock_and_time)
    for stock_and_time in after_selling_list:
        if context.number_of_positions < 10:
            buy(context, stock_and_time, bar_dict)
            context.number_of_positions += 1
            print('持仓数量：', context.number_of_positions, stock_and_time)


def before_selling(context, stock_list, minute, limit_lists):
    lists = []
    for stock_and_time in limit_lists:
        if stock_and_time[0] in stock_list:
            if stock_and_time[-1] < minute:
                lists.append(stock_and_time)
    stock_list = lists
    stock_list = sorted(stock_list, key=lambda y: y[-1], reverse=False)
    return stock_list

def after_selling(context, stock_list, minute, limit_lists):
    lists = []
    for stock_and_time in limit_lists:
        if stock_and_time[0] in stock_list:
            if stock_and_time[-1] >= minute:
                lists.append(stock_and_time)
    stock_list = lists
    stock_list = sorted(stock_list, key=lambda y: y[-1], reverse=False)
    return stock_list

def buy(context, stock_and_time, bar_dict):
    gzc = round(context.portfolio.total_value, 2)
    stock = stock_and_time[0]
    limit_time = context.open_time + timedelta(minutes=stock_and_time[-1])
    order_target_value(stock, gzc / context.buy_stock_count)
    print(limit_time, "买入股票：%s " % instruments(stock).symbol, stock,
                 "下单后，剩余资金：", round(context.portfolio.cash, 2))


def sell(context, bar_dict):
    if len(context.portfolio.positions) != 0:
        for position in list(context.portfolio.positions.values()):
            stock = position.order_book_id
            mc = instruments(stock).symbol
            cccb = round(position.avg_cost, 2)
            last_price = bar_dict[stock].close
            closes = history_bars(stock, 2, '1d', 'close')
            high_limit = closes[-2] * 1.1 if closes is not None and len(closes) >= 2 else None
            sl = position.quantity
            if position.sellable_quantity > 0 and (high_limit is None or high_limit != last_price):
                order_target_value(stock, 0)
                context.number_of_positions += -1
                print("卖出股票：%s  " % instruments(stock).symbol, stock,
                            '最新价格：%s' % last_price,
                            '个股盈亏：%s' % round((((last_price - cccb) * 100 / cccb) - 0.15), 2) + '%')
                print('当前持仓数量：', context.number_of_positions)
            else:
                print("涨停！继续持有==》》%s   " % instruments(stock).symbol, stock,
                             '最新价格：%s' % last_price,
                             '个股盈亏：%s' % round((((last_price - cccb) * 100 / cccb) - 0.15), 2) + '%')
                print('当前持仓数量：', context.number_of_positions)
    context.position_count = len(context.portfolio.positions)
    print('卖出以后持仓数量：', context.position_count)


def filter_specials(context, stock_list, bar_dict):
    # RQ: bar_dict[stock] provides current bar data
    stock_list = [stock for stock in stock_list if stock[0:3] != '688']
    stock_list = [stock for stock in stock_list if stock[0:3] != '300']  # filter chi_next
    stock_list = [stock for stock in stock_list if stock in bar_dict and bar_dict[stock].open > 1]
    stock_list = [stock for stock in stock_list if
                  stock in bar_dict and bar_dict[stock].open != bar_dict[stock].close]  # filter limit_up
    return stock_list
