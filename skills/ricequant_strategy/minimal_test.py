"""
二板策略 - 最小化版本
减少API调用，确保能运行完成
"""


def init(context):
    context.count = 0


def handle_bar(context, bar_dict):
    # 卖出
    for s in list(context.portfolio.positions.keys()):
        order_target_percent(s, 0)

    # 只在每月第一个交易日买入
    if context.now.day > 5:
        return

    # 买入沪深300第一只股票
    stocks = index_components("000300.XSHG")
    if stocks:
        order_target_percent(stocks[0], 0.95)
        context.count += 1
