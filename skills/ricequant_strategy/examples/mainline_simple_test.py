def init(context):
    context.benchmark = "000300.XSHG"
    context.max_holdings = 3

    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=40))
    scheduler.run_daily(sell_stocks, time_rule=market_close(minute=5))


def buy_stocks(context, bar_dict):
    if len(context.portfolio.positions) >= context.max_holdings:
        return

    logger.info(f"=== 开始选股 {context.now} ===")

    all_stocks_df = all_instruments("CS")
    stock_list = all_stocks_df["order_book_id"].tolist()
    stock_list = [s for s in stock_list if not s.startswith(("688", "4", "8", "68"))]

    logger.info(f"筛选前股票数: {len(stock_list)}")

    limit_up_stocks = []
    check_count = 0

    for stock in stock_list[:100]:
        try:
            check_count += 1
            bars = history_bars(stock, 2, "1d", "close")
            if bars is None or len(bars) < 2:
                continue

            pre_close = bars[-2]
            curr_close = bars[-1]

            # 涨停判断：涨幅>=9.0%
            pct_change = (curr_close - pre_close) / pre_close
            if pct_change >= 0.090:
                limit_up_stocks.append({"stock": stock, "pct": pct_change * 100})
        except Exception as e:
            continue

    logger.info(f"检查股票数: {check_count}, 涨停股票数: {len(limit_up_stocks)}")

    if not limit_up_stocks:
        logger.info("无涨停股票，结束")
        return

    candidates = []

    for item in limit_up_stocks[:30]:
        stock = item["stock"]
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

            # 放宽条件：开盘涨幅-2%~+3%
            if not (-2 <= open_pct <= 3):
                continue

            df = get_factor(stock, factor=["market_cap"])
            if df is None or df.empty:
                continue

            market_cap = df["market_cap"].iloc[0]

            candidates.append(
                {"stock": stock, "open_pct": open_pct, "market_cap": market_cap}
            )

            logger.info(f"候选: {stock}, 开盘{open_pct:.2f}%, 市值{market_cap:.1f}亿")

        except Exception as e:
            logger.info(f"{stock} 处理失败: {e}")
            continue

    logger.info(f"候选股票数: {len(candidates)}")

    if not candidates:
        logger.info("无候选股票，买入第一只涨停股测试")
        if limit_up_stocks:
            test_stock = limit_up_stocks[0]["stock"]
            if test_stock in bar_dict and bar_dict[test_stock].is_trading:
                order_shares(test_stock, 100)
                logger.info(f"测试买入 {test_stock} 100股")
        return

    # 按市值排序，选最小的
    candidates.sort(key=lambda x: x["market_cap"])

    buy_count = min(
        len(candidates), context.max_holdings - len(context.portfolio.positions)
    )
    cash_per_stock = context.portfolio.cash / buy_count * 0.95

    for i in range(buy_count):
        stock = candidates[i]["stock"]
        try:
            order_value(stock, cash_per_stock)
            logger.info(
                f"买入 {stock}, 开盘{candidates[i]['open_pct']:.2f}%, 市值{candidates[i]['market_cap']:.1f}亿"
            )
        except Exception as e:
            logger.info(f"买入失败 {stock}: {e}")


def sell_stocks(context, bar_dict):
    positions = list(context.portfolio.positions.keys())

    for stock in positions:
        try:
            pos = context.portfolio.positions[stock]
            if pos.sellable_quantity > 0:
                pnl_pct = (pos.last_price - pos.avg_cost) / pos.avg_cost * 100
                order_target_value(stock, 0)
                logger.info(f"卖出 {stock}, 盈亏{pnl_pct:.2f}%")
        except Exception as e:
            logger.info(f"卖出失败 {stock}: {e}")
