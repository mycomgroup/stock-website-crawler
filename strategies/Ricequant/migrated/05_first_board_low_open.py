# 首板低开策略 - RiceQuant 版本
# 涨停后低开买入策略
# 测试日期: 2024-01-01 到 2024-12-31


def init(context):
    context.target_stocks = []
    context.buy_threshold_low = 0.96
    context.buy_threshold_high = 0.97

    scheduler.run_daily(select_limit_up, time_rule=market_open(minute=0))
    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=35))
    scheduler.run_daily(sell_stocks, time_rule=market_close(minute=10))


def is_limit_up_yesterday(stock):
    """判断昨日是否涨停"""
    bars = history_bars(stock, 2, "1d", ["close", "limit_up"])

    if bars is None or len(bars) < 2:
        return False

    close = bars["close"][-2]
    limit_up = bars["limit_up"][-2]

    return abs(close - limit_up) < 0.01


def select_limit_up(context, bar_dict):
    """选择昨日涨停股票"""
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    stocks = list(set(hs300) | set(zz500))[:150]

    context.target_stocks = []

    for stock in stocks:
        if stock.startswith("688"):
            continue

        try:
            if is_limit_up_yesterday(stock):
                context.target_stocks.append(stock)

                if len(context.target_stocks) >= 20:
                    break
        except:
            pass

    logger.info(f"昨日涨停股票数: {len(context.target_stocks)}")


def buy_stocks(context, bar_dict):
    """买入：低开3-4%"""
    if not context.target_stocks:
        return

    if len(context.portfolio.positions) > 0:
        return

    buy_list = []

    for stock in context.target_stocks:
        try:
            bar = bar_dict[stock]

            if not bar.is_trading:
                continue

            bars = history_bars(stock, 1, "1d", "close")
            if bars is None:
                continue

            pre_close = bars[-1]
            open_price = bar.open
            open_pct = open_price / pre_close

            if context.buy_threshold_low <= open_pct <= context.buy_threshold_high:
                buy_list.append(stock)
                logger.info(f"低开股票: {stock}, 开盘涨幅: {(open_pct - 1) * 100:.2f}%")

        except:
            pass

    if buy_list:
        cash = context.portfolio.cash
        value_per_stock = cash / min(len(buy_list), 3)

        for stock in buy_list[:3]:
            try:
                order_value(stock, value_per_stock)
                logger.info(f"买入: {stock}")
            except Exception as e:
                logger.warning(f"买入 {stock} 失败: {e}")


def sell_stocks(context, bar_dict):
    """卖出"""
    positions = list(context.portfolio.positions.keys())

    for stock in positions:
        pos = context.portfolio.positions[stock]

        if pos.sellable_quantity > 0:
            try:
                bar = bar_dict[stock]
                current_price = bar.close

                bars = history_bars(stock, 1, "1d", "limit_up")
                if bars is not None:
                    limit_up = bars[-1]

                    if current_price < limit_up:
                        order_target_value(stock, 0)
                        logger.info(f"涨停打开，卖出: {stock}")

                avg_cost = pos.avg_cost
                if current_price > avg_cost * 1.05:
                    order_target_value(stock, 0)
                    logger.info(f"止盈卖出: {stock}")

            except:
                pass
