# 龙头底分型战法 - RiceQuant 版本
# 基于价格形态的交易策略
# 测试日期: 2024-01-01 到 2024-12-31


def init(context):
    context.lookback_period = 60
    context.hold_list = []

    scheduler.run_daily(select_stocks, time_rule=market_open(minute=5))
    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=35))
    scheduler.run_daily(sell_stocks, time_rule=market_close(minute=20))


def is_fractal_bottom(stock):
    """判断是否形成底分型"""
    bars = history_bars(stock, 5, "1d", ["high", "low", "close"])

    if bars is None or len(bars) < 5:
        return False

    lows = bars["low"]

    if lows[2] < lows[1] and lows[2] < lows[3]:
        if lows[1] < lows[0] and lows[3] < lows[4]:
            return True

    return False


def is_leader_stock(stock, context):
    """判断是否为龙头股"""
    bars = history_bars(stock, context.lookback_period, "1d", "close")

    if bars is None or len(bars) < context.lookback_period:
        return False

    high = max(bars["close"])
    current = bars["close"][-1]

    if current >= high * 0.95:
        return True

    return False


def select_stocks(context, bar_dict):
    """选股：龙头底分型"""
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    stocks = list(set(hs300) | set(zz500))[:100]

    context.hold_list = []

    for stock in stocks:
        if stock.startswith("688"):
            continue

        try:
            if is_leader_stock(stock, context) and is_fractal_bottom(stock):
                context.hold_list.append(stock)
                logger.info(f"选中: {stock}")

                if len(context.hold_list) >= 5:
                    break
        except:
            pass

    logger.info(f"选股完成，共 {len(context.hold_list)} 只")


def buy_stocks(context, bar_dict):
    """买入"""
    if not context.hold_list:
        return

    cash = context.portfolio.cash

    for stock in context.hold_list[:3]:
        if stock not in context.portfolio.positions:
            if cash > 10000:
                try:
                    order_value(stock, cash / 3)
                    logger.info(f"买入: {stock}")
                except Exception as e:
                    logger.warning(f"买入 {stock} 失败: {e}")


def sell_stocks(context, bar_dict):
    """卖出"""
    positions = list(context.portfolio.positions.keys())

    for stock in positions:
        pos = context.portfolio.positions[stock]

        if pos.sellable_quantity > 0:
            current_price = bar_dict[stock].close
            avg_cost = pos.avg_cost

            if current_price < avg_cost * 0.95:
                order_target_value(stock, 0)
                logger.info(
                    f"止损卖出: {stock}, 亏损 {((current_price / avg_cost - 1) * 100):.2f}%"
                )
            elif current_price > avg_cost * 1.1:
                order_target_value(stock, 0)
                logger.info(
                    f"止盈卖出: {stock}, 盈利 {((current_price / avg_cost - 1) * 100):.2f}%"
                )
