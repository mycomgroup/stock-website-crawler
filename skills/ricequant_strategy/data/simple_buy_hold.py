def init(context):
    context.stock = "000001.XSHE"
    context.bought = False
    scheduler.run_daily(trade, time_rule=market_open(minute=30))


def trade(context, bar_dict):
    if context.bought:
        return

    stock = context.stock

    try:
        prices = history_bars(stock, 5, "1d", "close")
        if prices is None or len(prices) < 5:
            return

        current_price = bar_dict[stock].close
        if current_price is None or current_price <= 0:
            return

        cash = context.portfolio.total_value * 0.95
        shares = int(cash / current_price / 100) * 100

        if shares > 0:
            order_shares(stock, shares)
            context.bought = True
            print(f"Bought {shares} shares of {stock} at {current_price}")
    except Exception as e:
        print(f"Trade error: {e}")


def after_trading_end(context, bar_dict):
    pass
