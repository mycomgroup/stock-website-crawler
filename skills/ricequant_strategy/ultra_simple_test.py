"""
极简二板策略 - 验证版
"""


def init(context):
    context.trades = 0
    print("策略启动")


def handle_bar(context, bar_dict):
    # 每日卖出
    for s in list(context.portfolio.positions.keys()):
        order_target_percent(s, 0)

    # 获取沪深300成分股
    stocks = index_components("000300.XSHG")[:50]

    # 找涨幅>9%的股票
    for s in stocks:
        try:
            p = history_bars(s, 1, "1d", "close")
            if p and len(p) > 0:
                # 简化：直接买入第一只
                order_target_percent(s, 0.9)
                context.trades += 1
                print(f"买入: {s}")
                break
        except:
            pass
