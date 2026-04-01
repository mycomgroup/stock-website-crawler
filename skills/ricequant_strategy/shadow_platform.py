"""
影子策略 - Ricequant平台版本
主线策略：假弱高开
"""


def init(context):
    context.strategy_mode = "mainline"
    context.limit_up_count = 0

    scheduler.run_daily(daily_check, time_rule=market_open(minute=5))


def daily_check(context, bar_dict):
    """
    每日检查
    """
    # 获取候选池
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300) | set(zz500))
        stocks = [s for s in stocks if not s.startswith("688")][:200]
    except:
        return

    # 统计涨停
    limit_up_count = 0
    for stock in stocks[:100]:
        try:
            bars = history_bars(stock, 2, "1d", "close")
            if bars and len(bars) >= 2:
                prev = bars[-2]
                curr = bars[-1]
                if prev > 0 and (curr - prev) / prev >= 0.095:
                    limit_up_count += 1
        except:
            continue

    context.limit_up_count = limit_up_count
    logger.info(f"涨停家数: {limit_up_count}")

    # 情绪过滤
    if limit_up_count < 30:
        logger.info("情绪不足")
        return

    # 筛选假弱高开
    signals = []
    for stock in stocks:
        try:
            bars = history_bars(stock, 2, "1d", ["close", "open", "high"])
            if not bars or len(bars) < 2:
                continue

            prev_close = bars[-2]["close"]
            open_price = bars[-1]["open"]
            high_price = bars[-1]["high"]

            if prev_close > 0:
                open_change = (open_price - prev_close) / prev_close
                if 0.001 < open_change < 0.03 and high_price > open_price:
                    signals.append(stock)
        except:
            continue

    logger.info(f"假弱高开信号: {len(signals)}")

    # 买入
    if signals and len(context.portfolio.positions) < 3:
        stock = signals[0]
        price = bar_dict[stock].close
        amount = min(100000, context.portfolio.total_value * 0.3)
        shares = int(amount / price / 100) * 100

        if shares > 0:
            order_shares(stock, shares)
            logger.info(f"买入 {stock}: {shares}股")

    # 卖出
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        hold_days = (context.now - pos.entry_date).days

        profit_pct = (bar_dict[stock].close - pos.avg_price) / pos.avg_price

        if profit_pct >= 0.03 or hold_days >= 1:
            order_shares(stock, -pos.quantity)
            logger.info(f"卖出 {stock}")


def after_trading(context):
    """
    收盘后
    """
    logger.info(f"持仓: {len(context.portfolio.positions)}")
