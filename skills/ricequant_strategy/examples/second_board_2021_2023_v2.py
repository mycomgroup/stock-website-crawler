"""
二板策略 - RiceQuant 正确 API 版本
2021-2023 年验证
"""


def init(context):
    context.trades = []
    context.daily_count = 0


def handle_bar(context, bar_dict):
    today = context.now.date()

    # 只测试 2021-2023
    if today.year < 2021 or today.year > 2023:
        return

    # 每天只执行一次（在开盘后）
    context.daily_count += 1
    if context.daily_count > 3:
        return  # 限制测试天数

    logger.info(f"=== {today} ===")

    # 正确方式获取股票列表
    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()

    # 过滤
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

    logger.info(f"涨停股票数: {len(zt_stocks)}")

    if len(zt_stocks) < 10:
        logger.info("涨停数不足，跳过")
        return

    # 找二板股票
    def is_zt(stock, bars_index):
        """检查指定天数前是否涨停"""
        try:
            bars = history_bars(stock, bars_index + 2, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) > bars_index:
                return (
                    bars[-bars_index]["close"] >= bars[-bars_index]["limit_up"] * 0.99
                )
        except:
            pass
        return False

    second_board = []
    for stock in zt_stocks:
        # 昨日涨停，前天不涨停 = 二板
        if is_zt(stock, 1) and not is_zt(stock, 2):
            # 检查缩量
            try:
                vol_bars = history_bars(stock, 2, "1d", ["volume"])
                if vol_bars is not None and len(vol_bars) >= 2:
                    vol_ratio = vol_bars[-1]["volume"] / vol_bars[-2]["volume"]
                    if vol_ratio <= 1.875:
                        second_board.append(stock)
            except:
                pass

    logger.info(f"二板股票数: {len(second_board)}")

    if len(second_board) == 0:
        return

    # 选择第一只（实际应该按市值排序）
    target = second_board[0]
    logger.info(f"选择: {target}")

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
                                "price": bar.open,
                                "shares": shares,
                            }
                        )
                        logger.info(f"买入: {target} @ {bar.open}")
            except:
                pass


def after_trading(context):
    pass
