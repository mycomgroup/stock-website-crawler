"""
二板策略调试版 - RiceQuant
放宽条件，确保能产生交易
"""


def init(context):
    context.holding_stock = None
    context.buy_price = 0
    context.trade_day = 0
    logger.info("=== 二板策略调试版 ===")


def handle_bar(context, bar_dict):
    today = context.now.date()

    if today.year != 2021:
        return

    # 如果有持仓，次日卖出
    if context.holding_stock:
        stock = context.holding_stock
        if stock in bar_dict:
            bar = bar_dict[stock]
            if bar.is_trading:
                order_target_value(stock, 0)
                profit = (bar.close - context.buy_price) / context.buy_price * 100
                logger.info(f"{today}: 卖出 {stock} @ {bar.close}, 收益: {profit:.2f}%")
                context.holding_stock = None
        return

    # 获取股票列表
    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()
    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    # 检查前300只股票
    for stock in stocks[:300]:
        try:
            # 获取最近3天数据
            bars = history_bars(stock, 3, "1d", ["close", "limit_up", "volume"])
            if bars is None or len(bars) < 3:
                continue

            # 检查是否是二板（昨天和前天都涨停）
            day1_close = bars[-1]["close"]
            day1_limit = bars[-1]["limit_up"]
            day2_close = bars[-2]["close"]
            day2_limit = bars[-2]["limit_up"]

            # 昨天涨停
            if day1_close < day1_limit * 0.99:
                continue

            # 前天涨停
            if day2_close < day2_limit * 0.99:
                continue

            # 大前天不涨停（可选）
            day3_close = bars[-3]["close"]
            day3_limit = bars[-3]["limit_up"]
            if day3_close >= day3_limit * 0.99:
                continue  # 大前天也涨停，跳过

            # 缩量条件
            vol1 = bars[-1]["volume"]
            vol2 = bars[-2]["volume"]
            if vol2 > 0 and vol1 / vol2 > 1.875:
                continue

            # 检查今日是否可买入
            if stock not in bar_dict:
                continue

            bar = bar_dict[stock]
            if not bar.is_trading:
                continue

            # 检查是否非涨停开盘
            if bar.open >= day1_limit * 0.99:
                continue

            # 买入
            order_shares(stock, 1000)
            context.holding_stock = stock
            context.buy_price = bar.open
            logger.info(f"{today}: 买入 {stock} @ {bar.open}")
            return

        except:
            continue
