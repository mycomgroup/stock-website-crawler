"""
二板策略简化版 - RiceQuant
2021 年验证
"""


def init(context):
    context.bought_stock = None
    context.buy_price = 0
    context.buy_date = None
    context.trade_count = 0
    context.win_count = 0
    context.total_profit = 0
    logger.info("=== 二板策略初始化 ===")


def handle_bar(context, bar_dict):
    today = context.now.date()

    # 只测试 2021
    if today.year != 2021:
        return

    # 如果有持仓，检查是否需要卖出（持有1天后卖出）
    if context.bought_stock:
        stock = context.bought_stock
        if stock in bar_dict:
            bar = bar_dict[stock]
            if bar.is_trading:
                # 卖出
                order_target_value(stock, 0)
                profit = (bar.close - context.buy_price) / context.buy_price * 100
                context.total_profit += profit
                context.trade_count += 1
                if profit > 0:
                    context.win_count += 1
                logger.info(f"{today}: 卖出 {stock} @ {bar.close}, 收益: {profit:.2f}%")
                context.bought_stock = None
        return

    # 获取所有股票
    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()

    # 过滤
    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    stocks = stocks[:300]

    # 找涨停股票
    zt_stocks = []
    for stock in stocks:
        try:
            bars = history_bars(stock, 2, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) >= 2:
                if bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99:
                    zt_stocks.append(stock)
        except:
            pass

    # 情绪过滤
    if len(zt_stocks) < 10:
        return

    # 找二板
    for stock in zt_stocks:
        try:
            # 检查是否是二板（昨日涨停，前天不涨停）
            bars = history_bars(stock, 3, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) >= 3:
                # 昨天（-1）涨停，前天（-2）不涨停
                yesterday_zt = bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99
                prevday_zt = bars[-2]["close"] >= bars[-2]["limit_up"] * 0.99

                if yesterday_zt and not prevday_zt:
                    # 检查缩量
                    vol_bars = history_bars(stock, 2, "1d", ["volume"])
                    if vol_bars is not None and len(vol_bars) >= 2:
                        vol_ratio = vol_bars[-1]["volume"] / vol_bars[-2]["volume"]
                        if vol_ratio <= 1.875:
                            # 检查是否可买入
                            if stock in bar_dict:
                                bar = bar_dict[stock]
                                if bar.is_trading:
                                    # 检查是否非涨停开盘
                                    if bar.open < bars[-1]["limit_up"] * 0.99:
                                        order_shares(stock, 1000)
                                        context.bought_stock = stock
                                        context.buy_price = bar.open
                                        context.buy_date = today
                                        logger.info(
                                            f"{today}: 买入 {stock} @ {bar.open}"
                                        )
                                        return
        except:
            pass
