def init(context):
    context.benchmark = "000300.XSHG"
    context.max_holdings = 3

    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=35))
    scheduler.run_daily(sell_stocks, time_rule=market_close(minute=10))


def buy_stocks(context, bar_dict):
    if len(context.portfolio.positions) >= context.max_holdings:
        return

    all_stocks_df = all_instruments("CS")
    stock_list = all_stocks_df["order_book_id"].tolist()
    stock_list = [s for s in stock_list if not s.startswith(("688", "4", "8"))]

    limit_up_stocks = []

    for stock in stock_list[:300]:
        try:
            bars = history_bars(stock, 2, "1d", ["close", "limit_up"])
            if bars is None or len(bars) < 2:
                continue

            if abs(bars[-1]["close"] - bars[-1]["limit_up"]) < 0.01:
                limit_up_stocks.append(stock)
        except:
            continue

    if not limit_up_stocks:
        logger.info("无涨停板股票")
        return

    candidates = []

    for stock in limit_up_stocks[:30]:
        try:
            if stock not in bar_dict:
                continue

            bar = bar_dict[stock]
            if not bar.is_trading:
                continue

            bars = history_bars(stock, 1, "1d", "close")
            if bars is None or len(bars) == 0:
                continue

            pre_close = bars[-1]
            open_price = bar.open
            open_pct = (open_price - pre_close) / pre_close * 100

            if not (0.5 <= open_pct <= 1.5):
                continue

            df = get_factor(stock, factor=["market_cap"])
            if df is None or df.empty:
                continue

            market_cap = df["market_cap"].iloc[0]
            if not (50 <= market_cap <= 150):
                continue

            candidates.append(
                {"stock": stock, "open_pct": open_pct, "market_cap": market_cap}
            )
        except Exception as e:
            continue

    if not candidates:
        logger.info("无符合条件的股票")
        return

    candidates.sort(key=lambda x: x["open_pct"])

    buy_count = min(
        len(candidates), context.max_holdings - len(context.portfolio.positions)
    )

    cash_per_stock = context.portfolio.cash / buy_count * 0.95

    for i in range(buy_count):
        stock = candidates[i]["stock"]
        try:
            order_value(stock, cash_per_stock)
            logger.info(f"买入 {stock}, 开盘涨幅 {candidates[i]['open_pct']:.2f}%")
        except Exception as e:
            logger.info(f"买入 {stock} 失败: {e}")


def sell_stocks(context, bar_dict):
    positions = list(context.portfolio.positions.keys())

    for stock in positions:
        try:
            pos = context.portfolio.positions[stock]
            if pos.sellable_quantity > 0:
                order_target_value(stock, 0)
                logger.info(f"卖出 {stock}")
        except Exception as e:
            logger.info(f"卖出 {stock} 失败: {e}")
