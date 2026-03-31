"""
简单买入测试 - RiceQuant
测试数据获取和交易功能
"""


def init(context):
    logger.info("=== 策略初始化 ===")
    context.bought = False
    context.stock = "000001.XSHE"
    scheduler.run_daily(daily_check, time_rule=market_open(minute=5))


def daily_check(context, bar_dict):
    today = context.now.date()

    if context.bought:
        return

    stock = context.stock

    if stock not in bar_dict:
        logger.info(f"{today}: {stock} not in bar_dict")
        return

    bar = bar_dict[stock]

    if not bar.is_trading:
        logger.info(f"{today}: {stock} not trading")
        return

    logger.info(
        f"{today}: {stock} open={bar.open:.2f}, close={bar.close:.2f}, high={bar.high:.2f}"
    )

    # 获取历史数据
    bars = history_bars(stock, 5, "1d", ["close", "volume"])
    if bars is not None and len(bars) > 0:
        logger.info(f"{today}: 历史5日收盘价: {bars['close']}")
        logger.info(f"{today}: 历史5日成交量: {bars['volume']}")

    # 买入1000股
    order_shares(stock, 1000)
    context.bought = True
    logger.info(f"{today}: 买入 {stock} 1000股 @ {bar.open}")

    positions = context.portfolio.positions
    logger.info(f"{today}: 持仓: {list(positions.keys())}")


def after_trading(context):
    today = context.now.date()
    logger.info(f"{today}: 收盘后检查")

    positions = context.portfolio.positions
    for stock, pos in positions.items():
        logger.info(f"  {stock}: 数量={pos.quantity}, 市值={pos.market_value}")


__all__ = ["init", "daily_check", "after_trading"]
