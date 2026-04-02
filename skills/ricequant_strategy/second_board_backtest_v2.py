"""
二板接力策略 - RiceQuant策略编辑器格式
完整回测版本
回测周期：2021-01-01 至 2024-12-31
"""


def init(context):
    # 策略参数
    context.trade_count = 0
    context.win_count = 0
    context.total_profit = 0
    context.trades = []

    # 选股参数
    context.stock_pool_size = 500  # 股票池大小
    context.emotion_threshold = 10  # 情绪阈值（涨停家数）
    context.volume_ratio_threshold = 1.875  # 缩量阈值
    context.slippage = 0.005  # 滑点

    print("二板接力策略初始化完成")


def handle_bar(context, bar_dict):
    # 每日执行
    date = context.now.date()

    # 换月时输出月度统计
    if date.day == 1:
        if context.trade_count > 0:
            win_rate = context.win_count / context.trade_count * 100
            print(
                f"月度统计: 交易{context.trade_count}笔, 胜率{win_rate:.1f}%, 收益{context.total_profit:.2f}%"
            )

    # 如果持仓，次日卖出
    if context.portfolio.positions:
        for stock in list(context.portfolio.positions.keys()):
            order_target_percent(stock, 0)

    # 获取股票池
    all_stocks = all_instruments("CS")
    stock_list = all_stocks["order_book_id"].tolist()
    stock_list = [
        s
        for s in stock_list
        if isinstance(s, str) and not s.startswith(("688", "4", "8", "68"))
    ][: context.stock_pool_size]

    # 统计涨停
    zt_stocks = []
    for stock in stock_list:
        try:
            price = history_bars(stock, 1, "1d", "close,limit_up")
            if price is not None and len(price) > 0:
                if price[0]["close"] >= price[0]["limit_up"] * 0.99:
                    zt_stocks.append(stock)
        except:
            pass

    zt_count = len(zt_stocks)

    # 情绪开关
    if zt_count < context.emotion_threshold:
        return

    # 获取前两天的交易日
    trading_dates = get_trading_dates(context.start_date, context.end_date)
    date_str = date.strftime("%Y-%m-%d")

    if date_str not in [d.strftime("%Y-%m-%d") for d in trading_dates]:
        return

    date_idx = [d.strftime("%Y-%m-%d") for d in trading_dates].index(date_str)

    if date_idx < 2:
        return

    prev_date = trading_dates[date_idx - 1]
    prev2_date = trading_dates[date_idx - 2]

    # 获取昨天和前天的涨停
    zt_prev = []
    zt_prev2 = []

    for stock in stock_list:
        try:
            # 昨天
            price1 = history_bars(stock, 1, "1d", "close,limit_up")
            if price1 is not None and len(price1) > 0:
                if price1[0]["close"] >= price1[0]["limit_up"] * 0.99:
                    zt_prev.append(stock)

            # 前天
            price2 = history_bars(stock, 2, "1d", "close,limit_up")
            if price2 is not None and len(price2) >= 2:
                if price2[0]["close"] >= price2[0]["limit_up"] * 0.99:
                    zt_prev2.append(stock)
        except:
            pass

    # 二板候选：今天涨停 & 昨天涨停 & 前天不涨停
    sb_candidates = list(set(zt_stocks) & set(zt_prev) - set(zt_prev2))

    if len(sb_candidates) == 0:
        return

    # 筛选：缩量 + 非一字板 + 小市值
    valid_stocks = []

    for stock in sb_candidates:
        try:
            # 缩量检查
            vol = history_bars(stock, 2, "1d", "volume")
            if vol is not None and len(vol) >= 2:
                vol_ratio = vol[1]["volume"] / vol[0]["volume"]
                if vol_ratio > context.volume_ratio_threshold:
                    continue

            # 非一字板检查
            price = history_bars(stock, 1, "1d", "high,low")
            if price is not None and len(price) > 0:
                if price[0]["high"] == price[0]["low"]:
                    continue

            # 市值
            market_cap = get_factor([stock], "market_cap", date, date)
            if market_cap is not None and len(market_cap) > 0:
                cap = market_cap.iloc[0][stock]
                valid_stocks.append((stock, cap))
        except:
            pass

    if len(valid_stocks) == 0:
        return

    # 按市值排序，选最小的
    valid_stocks.sort(key=lambda x: x[1])
    target_stock = valid_stocks[0][0]

    # 非涨停开盘才买入
    try:
        current_price = bar_dict[target_stock]
        if current_price.last_price >= current_price.limit_up * 0.99:
            return
    except:
        return

    # 买入
    order_target_percent(target_stock, 0.95)

    context.trade_count += 1
    print(f"买入: {target_stock}")
