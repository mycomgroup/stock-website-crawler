# 龙头底分型极简测试版 - RiceQuant策略编辑器
# 昨日涨停 + 今日高开买入


def init(context):
    context.benchmark = "000300.XSHG"
    context.max_holdings = 1
    context.trade_count = 0
    context.win_count = 0

    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=5))
    scheduler.run_daily(sell_stocks, time_rule=market_close(minute=10))


def buy_stocks(context, bar_dict):
    if len(context.portfolio.positions) >= context.max_holdings:
        return

    today = context.now.date()
    today_str = today.strftime("%Y-%m-%d")

    # 获取前一个交易日
    all_dates = get_trading_dates("2024-01-01", "2024-12-31")
    today_idx = -1
    for i, d in enumerate(all_dates):
        if d.strftime("%Y-%m-%d") == today_str:
            today_idx = i
            break

    if today_idx <= 0:
        return

    prev_date_str = all_dates[today_idx - 1].strftime("%Y-%m-%d")

    # 获取所有股票
    all_stocks_df = all_instruments("CS", prev_date_str)
    stock_list = all_stocks_df["order_book_id"].tolist()
    stock_list = [
        s for s in stock_list if not (s.startswith("68") or s.startswith("300"))
    ]

    # 找昨日涨停股
    zt_stocks = []
    for stock in stock_list[:300]:
        try:
            bars = history_bars(stock, 1, "1d", ["close", "high_limit"], prev_date_str)
            if bars is not None and len(bars) > 0:
                if bars[-1]["close"] >= bars[-1]["high_limit"] * 0.995:
                    zt_stocks.append(stock)
        except:
            pass

    if len(zt_stocks) == 0:
        logger.info(f"{today_str}: 无昨日涨停股")
        return

    logger.info(f"{today_str}: 昨日涨停股数: {len(zt_stocks)}")

    # 从涨停股中选今日高开的
    for stock in zt_stocks[:10]:
        if stock not in bar_dict:
            continue

        bar = bar_dict[stock]
        if not bar.is_trading:
            continue

        # 获取昨日收盘价
        try:
            prev_bars = history_bars(stock, 1, "1d", ["close"], prev_date_str)
            if prev_bars is None or len(prev_bars) == 0:
                continue
            prev_close = prev_bars[-1]["close"]
        except:
            continue

        # 检查开盘高开1%-6%
        open_pct = (bar.open - prev_close) / prev_close * 100
        if 1.0 <= open_pct <= 6.0:
            try:
                order_value(stock, context.portfolio.cash * 0.95)
                context.trade_count += 1
                logger.info(f"{today_str}: 买入 {stock} 开盘涨幅{open_pct:.2f}%")
                return
            except:
                pass


def sell_stocks(context, bar_dict):
    positions = list(context.portfolio.positions.keys())

    for stock in positions:
        if stock not in context.portfolio.positions:
            continue

        pos = context.portfolio.positions[stock]
        if pos.sellable_quantity == 0:
            continue

        if stock not in bar_dict:
            continue

        bar = bar_dict[stock]
        current_price = bar.last

        # 止损5%
        if current_price < pos.avg_price * 0.95:
            order_target_value(stock, 0)
            logger.info(f"止损 {stock}")
            continue

        # 止盈40%
        if current_price > pos.avg_price * 1.4:
            context.win_count += 1
            order_target_value(stock, 0)
            logger.info(f"止盈 {stock}")
            continue

        # 持有超过3天不管盈亏都卖
        holding_days = (context.now.date() - pos.init_date.date()).days
        if holding_days >= 3:
            order_target_value(stock, 0)
            logger.info(f"时间卖出 {stock}")
