# 风险及免责提示：该策略由聚宽用户在聚宽社区分享，仅供学习交流使用。
# 原文一般包含策略说明，如有疑问请到原文和作者交流讨论。
# 原文网址：https://www.joinquant.com/post/36060
# 标题：ETF-控制回撤性能拉满（国债ETF增强）
# 作者：晒太阳的猫

# 回测资金需要 1000000

import pandas as pd
import numpy as np

def init(context):
    # 设定沪深300作为基准
    # 开启动态复权模式(真实价格)
    print('初始函数开始运行且全局只运行一次')

    context.max_net = context.portfolio.total_value
    context.drawback_status = 0
    context.bad_sign = 0

    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税

    # 运行函数
    scheduler.run_daily(before_market_open, time_rule=market_open(minute=30))
    scheduler.run_daily(market_open_func, time_rule=market_open(minute=0))
    scheduler.run_daily(after_market_close, time_rule=market_close(minute=30))


def handle_bar(context, bar_dict):
    pass


def before_market_open(context, bar_dict):
    print('函数运行时间(before_market_open)：' + str(context.now.time()))

    context.stock = ['510300.XSHG', '510220.XSHG', '513500.XSHG', '513100.XSHG']
    context.debt = ['511010.XSHG']

    # 分配资金
    cash_management(context)


def cash_management(context, bar_dict=None):
    HS300_data = history_bars('000300.XSHG', 60, '1d', 'close')
    if HS300_data is None or len(HS300_data) == 0:
        return
    HS300_MA0_20 = HS300_data[-20:-1].mean()
    HS300_MA20_40 = HS300_data[-40:-21].mean()
    HS300_MA40_60 = HS300_data[-60:-41].mean()
    HS300_price = HS300_data[-1]
    HS300_10_max = HS300_data[-10:-1].max()
    HS300_20_max = HS300_data[-20:-1].max()

    if HS300_MA0_20 < HS300_MA20_40 and HS300_MA20_40 < HS300_MA40_60:
        context.bad_sign = 1
    elif HS300_price < 0.92 * HS300_10_max:
        context.bad_sign = 1
    elif HS300_price < 0.85 * HS300_20_max:
        context.bad_sign = 1
    else:
        context.bad_sign = 0

    if context.drawback_status == 0:
        if context.portfolio.total_value < context.max_net * 0.95:
            context.drawback_status = 2
        elif context.portfolio.total_value < context.max_net * 0.975:
            context.drawback_status = 1
    if context.drawback_status == 1:
        if context.portfolio.total_value > context.max_net * 0.99:
            context.drawback_status = 0
        elif context.portfolio.total_value < context.max_net * 0.95:
            context.drawback_status = 2
    if context.drawback_status == 2:
        if context.portfolio.total_value > context.max_net * 0.99:
            context.drawback_status = 0
        elif context.portfolio.total_value > context.max_net * 0.975:
            context.drawback_status = 1

    if context.drawback_status == 0:
        context.stock_cash = 0.3 * context.portfolio.total_value
        context.debt_cash = 0.7 * context.portfolio.total_value
    if context.drawback_status == 1:
        context.stock_cash = 0.4 * context.portfolio.total_value
        context.debt_cash = 0.6 * context.portfolio.total_value
    if context.drawback_status == 2:
        context.stock_cash = 0.5 * context.portfolio.total_value
        context.debt_cash = 0.5 * context.portfolio.total_value

    if context.bad_sign == 1:
        context.stock_cash = 0 * context.portfolio.total_value
        context.debt_cash = 1 * context.portfolio.total_value


def order_stock(context):
    pass

def order_debt(context):
    pass


def market_open_func(context, bar_dict):
    for stock in context.debt:
        order_target_value(stock, context.debt_cash / len(context.debt))

    for stock in context.stock:
        order_target_value(stock, context.stock_cash / len(context.stock))


def after_market_close(context, bar_dict):
    if context.portfolio.total_value > context.max_net:
        context.max_net = context.portfolio.total_value

    print("最高资产：%.2f" % context.max_net)
    print("总资产：%.2f" % context.portfolio.total_value)
    print("可用资产：%.2f" % context.portfolio.cash)
    print("股票资金：%.2f" % context.stock_cash)
    print("债券资产：%.2f" % context.debt_cash)
    print("回撤信号：%d" % context.drawback_status)
    print("回撤信号：%d" % context.bad_sign)
    print('一天结束')
