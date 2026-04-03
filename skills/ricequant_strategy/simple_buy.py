"""
二板策略 - 最简版
只买入一只股票，测试回测系统
"""


def init(context):
    print("策略启动")
    context.bought = False


def handle_bar(context, bar_dict):
    # 只买入一次
    if not context.bought:
        stocks = index_components("000300.XSHG")
        if stocks:
            order_target_percent(stocks[0], 0.95)
            print(f"买入: {stocks[0]}")
            context.bought = True
