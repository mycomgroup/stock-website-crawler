def init(context):
    context.benchmark = "000300.XSHG"
    context.max_holdings = 5
    context.trade_count = 0
    context.win_count = 0

    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=35))
    scheduler.run_daily(sell_stocks, time_rule=market_close(minute=5))


def buy_stocks(context, bar_dict):
    if len(context.portfolio.positions) >= context.max_holdings:
        return

    all_stocks_df = all_instruments("CS")
    stock_list = [
        s
        for s in all_stocks_df["order_book_id"].tolist()
        if not s.startswith(("688", "4", "8"))
    ]

    limit_up_stocks = []

    for stock in stock_list[:500]:
        try:
            bars = history_bars(stock, 3, "1d", "close")
            if bars is None or len(bars) < 3:
                continue

            if bars[-2] >= bars[-3] * 1.095 and bars[-1] < bars[-2] * 1.095:
                limit_up_stocks.append(stock)
        except:
            continue

    if not limit_up_stocks:
        return

    candidates = []

    for stock in limit_up_stocks[:50]:
        try:
            if stock not in bar_dict:
                continue

            bar = bar_dict[stock]
            if not bar.is_trading:
                continue

            bars = history_bars(stock, 1, "1d", "close")
            if bars is None:
                continue

            pre_close = bars[-1]
            open_price = bar.open
            open_pct = (open_price - pre_close) / pre_close * 100

            if not (-3 <= open_pct <= 3):
                continue

            df = get_factor(stock, factor=["market_cap"])
            if df is None or df.empty:
                continue

            market_cap = df["market_cap"].iloc[0]

            candidates.append(
                {"stock": stock, "open_pct": open_pct, "market_cap": market_cap}
            )
        except:
            continue

    if not candidates:
        return

    candidates.sort(key=lambda x: x["market_cap"])

    buy_count = min(
        len(candidates), context.max_holdings - len(context.portfolio.positions)
    )
    cash_per_stock = context.portfolio.cash / buy_count * 0.95

    for i in range(buy_count):
        stock = candidates[i]["stock"]
        try:
            order_value(stock, cash_per_stock)
            context.trade_count += 1
        except:
            continue


def sell_stocks(context, bar_dict):
    positions = list(context.portfolio.positions.keys())

    for stock in positions:
        try:
            pos = context.portfolio.positions[stock]
            if pos.sellable_quantity > 0:
                if pos.last_price > pos.avg_cost:
                    context.win_count += 1
                order_target_value(stock, 0)
        except:
            continue
