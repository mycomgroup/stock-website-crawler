"""
主线策略测试 - RiceQuant API兼容版
首板低开/假弱高开策略
测试期间: 最近日期
"""


def init(context):
    context.stocks = ["000001.XSHE", "600000.XSHG", "000002.XSHE"]
    context.bought = False
    scheduler.run_daily(rebalance)


def rebalance(context, bar_dict):
    if context.bought:
        return

    for stock in context.stocks:
        try:
            prices = history_bars(stock, 5, "1d", "close")
            if prices is None or len(prices) < 5:
                continue

            ma5 = sum(prices[-5:]) / 5
            current = prices[-1]

            if current > ma5 * 1.02:
                order_target_percent(stock, 0.33)
                context.bought = True
        except Exception as e:
            log.info(f"Error: {e}")


def after_trading_end(context, bar_dict):
    pass
