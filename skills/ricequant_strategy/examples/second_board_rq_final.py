"""
二板策略 - RiceQuant 正确 API 版本
2021-2023 年验证

关键 API 注意事项：
1. all_instruments("CS")["order_book_id"].tolist() 获取股票列表
2. order_target_value(stock, 0) 清仓（不是 order_target）
3. logger.info() 打日志（不是 log.info）
"""


def init(context):
    context.trades = []
    context.trade_log = []
    logger.info("=== 二板策略初始化 ===")


def handle_bar(context, bar_dict):
    today = context.now.date()

    # 只测试 2021-2023
    if today.year < 2021 or today.year > 2023:
        return

    # 获取所有股票（正确方式）
    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()

    # 过滤科创板、北交所
    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    stocks = stocks[:500]  # 限制数量避免超时

    # 获取昨日涨停股票
    zt_stocks = []
    for stock in stocks:
        try:
            bars = history_bars(stock, 2, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) >= 2:
                # 昨日收盘接近涨停价
                if bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99:
                    zt_stocks.append(stock)
        except:
            pass

    # 情绪过滤：涨停数>=10
    if len(zt_stocks) < 10:
        return

    # 找二板股票
    def is_zt_on_date(stock, days_ago):
        """检查指定天数前是否涨停"""
        try:
            bars = history_bars(stock, days_ago + 2, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) > days_ago:
                return bars[-days_ago]["close"] >= bars[-days_ago]["limit_up"] * 0.99
        except:
            pass
        return False

    second_board = []
    for stock in zt_stocks:
        # 昨日涨停，前天不涨停 = 二板
        if is_zt_on_date(stock, 1) and not is_zt_on_date(stock, 2):
            # 检查缩量
            try:
                vol_bars = history_bars(stock, 2, "1d", ["volume"])
                if vol_bars is not None and len(vol_bars) >= 2:
                    vol_ratio = vol_bars[-1]["volume"] / vol_bars[-2]["volume"]
                    if vol_ratio <= 1.875:
                        second_board.append(stock)
            except:
                pass

    if len(second_board) == 0:
        return

    # 选择第一只
    target = second_board[0]

    # 检查今日是否可买入
    if target in bar_dict:
        bar = bar_dict[target]
        if bar.is_trading:
            # 获取涨停价
            try:
                price_bars = history_bars(target, 1, "1d", ["limit_up"])
                if price_bars is not None and len(price_bars) > 0:
                    limit_up = price_bars[-1]["limit_up"]

                    # 非涨停开盘才买入
                    if bar.open < limit_up * 0.99:
                        shares = 1000
                        order_shares(target, shares)
                        context.trades.append(
                            {
                                "date": str(today),
                                "stock": target,
                                "buy_price": bar.open,
                                "shares": shares,
                            }
                        )
                        logger.info(f"{today}: 买入 {target} @ {bar.open}")
            except:
                pass

    # 检查是否需要卖出（持仓超过0）
    for trade in context.trades[:]:
        stock = trade["stock"]
        if stock in context.portfolio.positions:
            position = context.portfolio.positions[stock]
            if position.quantity > 0:
                # 次日卖出
                bar = bar_dict.get(stock)
                if bar and bar.is_trading:
                    order_target_value(stock, 0)  # 正确的清仓方式
                    profit = (bar.close - trade["buy_price"]) / trade["buy_price"] * 100
                    context.trade_log.append(
                        {
                            "date": str(today),
                            "stock": stock,
                            "buy_price": trade["buy_price"],
                            "sell_price": bar.close,
                            "profit": profit,
                        }
                    )
                    logger.info(
                        f"{today}: 卖出 {stock} @ {bar.close}, 收益: {profit:.2f}%"
                    )
                    context.trades.remove(trade)


def after_trading(context):
    pass
