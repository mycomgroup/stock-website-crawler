# 策略B：小市值 + 事件（首板低开）
# 选股：流通市值5-15亿 + 首板 + 低开
# 次日退出


def init(context):
    context.target_stock = None
    context.buy_price = 0
    context.hold_days = 0


def handle_bar(context, bar_dict):
    # 如果有持仓，检查是否需要卖出（次日卖出）
    if context.target_stock and context.target_stock in context.portfolio.positions:
        context.hold_days += 1

        # 持有一天后卖出
        if context.hold_days >= 1:
            order_target_percent(context.target_stock, 0)
            context.target_stock = None
            context.hold_days = 0
            logger.info("卖出股票")
        return

    # 如果没有持仓，寻找买入机会
    if not context.target_stock:
        find_and_buy(context, bar_dict)


def find_and_buy(context, bar_dict):
    # 获取昨日数据
    yesterday = context.now - timedelta(days=1)

    # 获取所有股票
    stocks_df = all_instruments("CS")
    all_codes = list(stocks_df.order_book_id)[:300]  # 限制数量

    # 筛选小市值股票（5-15亿）
    small_cap_stocks = []
    for code in all_codes:
        try:
            df = get_factor(code, factor=["market_cap"])
            if df is not None and len(df) > 0:
                cap = df["market_cap"].iloc[0]
                if 5 <= cap <= 15:
                    small_cap_stocks.append(code)
        except:
            pass

    if not small_cap_stocks:
        return

    # 寻找首板股票（昨日涨停）
    limit_up_stocks = []
    for code in small_cap_stocks[:50]:  # 限制检查数量
        try:
            bars = history_bars(code, 1, "1d", ["close", "limit_up"], yesterday)
            if bars is not None and len(bars) > 0:
                close = bars["close"][-1]
                limit_up = bars["limit_up"][-1]
                if abs(close - limit_up) < 0.01:
                    limit_up_stocks.append(code)
        except:
            pass

    if not limit_up_stocks:
        return

    # 检查今日低开
    for code in limit_up_stocks:
        try:
            if code not in bar_dict:
                continue

            bar = bar_dict[code]
            if not bar.is_trading:
                continue

            # 获取昨日收盘价
            prev_bars = history_bars(code, 1, "1d", ["close"], yesterday)
            if prev_bars is None or len(prev_bars) == 0:
                continue

            prev_close = prev_bars["close"][-1]
            open_price = bar.open

            # 计算开盘涨幅
            open_pct = (open_price - prev_close) / prev_close * 100

            # 低开范围：-3% ~ +1.5%
            if -3.0 <= open_pct <= 1.5:
                # 买入
                order_target_percent(code, 1.0)
                context.target_stock = code
                context.buy_price = bar.close
                context.hold_days = 0
                logger.info("买入 %s, 开盘涨幅: %.2f%%" % (code, open_pct))
                break
        except:
            pass
