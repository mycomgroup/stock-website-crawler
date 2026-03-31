"""
二板策略 - RiceQuant 正确版本
二板定义：昨天是第二个连续涨停（即前天和昨天都涨停，大前天不涨停）

API 注意事项：
1. all_instruments("CS")["order_book_id"].tolist()
2. order_target_value(stock, 0) 清仓
3. logger.info() 日志
"""


def init(context):
    context.holding_stock = None
    context.buy_price = 0
    context.trades = 0
    context.wins = 0
    context.total_profit = 0
    logger.info("=== 二板策略初始化 ===")


def handle_bar(context, bar_dict):
    today = context.now.date()

    # 只测试 2021
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
                context.total_profit += profit
                context.trades += 1
                if profit > 0:
                    context.wins += 1
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
    stocks = stocks[:400]

    # 找涨停股票
    zt_stocks = []
    for stock in stocks:
        try:
            bars = history_bars(stock, 1, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) > 0:
                if bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99:
                    zt_stocks.append(stock)
        except:
            pass

    # 情绪过滤
    if len(zt_stocks) < 10:
        return

    # 找二板股票
    for stock in zt_stocks:
        try:
            bars = history_bars(stock, 3, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) >= 3:
                # 二板定义：昨天涨停(-1)，前天涨停(-2)，大前天不涨停(-3)
                day1_zt = bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99  # 昨天
                day2_zt = bars[-2]["close"] >= bars[-2]["limit_up"] * 0.99  # 前天
                day3_zt = bars[-3]["close"] >= bars[-3]["limit_up"] * 0.99  # 大前天

                if day1_zt and day2_zt and not day3_zt:
                    # 这是二板！

                    # 检查缩量
                    vol_bars = history_bars(stock, 2, "1d", ["volume"])
                    if vol_bars is not None and len(vol_bars) >= 2:
                        vol_ratio = vol_bars[-1]["volume"] / vol_bars[-2]["volume"]
                        if vol_ratio <= 1.875:
                            # 检查今日是否可买入
                            if stock in bar_dict:
                                bar = bar_dict[stock]
                                if bar.is_trading:
                                    # 非涨停开盘
                                    if bar.open < bars[-1]["limit_up"] * 0.99:
                                        order_shares(stock, 1000)
                                        context.holding_stock = stock
                                        context.buy_price = bar.open
                                        logger.info(
                                            f"{today}: 买入 {stock} @ {bar.open}"
                                        )
                                        return
        except:
            pass
