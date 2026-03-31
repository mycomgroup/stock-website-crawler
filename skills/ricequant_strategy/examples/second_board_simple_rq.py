"""
二板策略简化版测试 - RiceQuant DataFrame正确处理
"""

print("=" * 60)
print("二板策略简化测试 - 2022年")
print("=" * 60)


def init(context):
    context.trades = 0
    context.wins = 0
    context.total_profit = 0

    scheduler.run_daily(daily_check, time_rule=market_open(minute=5))


def daily_check(context, bar_dict):
    today = context.now.date()

    if today.year != 2022:
        return

    if today.month > 6:
        return

    all_inst = all_instruments("CS")
    stock_list = all_inst["order_book_id"].tolist()

    stocks = [
        s
        for s in stock_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ][:300]

    def is_zt(stock):
        try:
            bars = history_bars(stock, 1, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) > 0:
                return bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99
        except:
            pass
        return False

    zt_stocks = [s for s in stocks if is_zt(s)]

    if len(zt_stocks) < 10:
        logger.info(f"{today}: 涨停股数不足 ({len(zt_stocks)})")
        return

    def is_zt_on_date(stock, days_ago):
        try:
            bars = history_bars(stock, days_ago + 1, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) > days_ago:
                return bars[-days_ago]["close"] >= bars[-days_ago]["limit_up"] * 0.99
        except:
            pass
        return False

    second_board = []
    for s in zt_stocks:
        if is_zt_on_date(s, 1) and not is_zt_on_date(s, 2):
            second_board.append(s)

    if len(second_board) == 0:
        logger.info(f"{today}: 无二板股票")
        return

    logger.info(f"{today}: 发现 {len(second_board)} 只二板股票")

    valid = []
    for s in second_board[:5]:
        try:
            bars = history_bars(s, 2, "1d", ["volume"])
            if bars is not None and len(bars) >= 2:
                vol_ratio = bars[-1]["volume"] / bars[-2]["volume"]
                if vol_ratio <= 1.875:
                    valid.append(s)
        except:
            pass

    if len(valid) == 0:
        logger.info(f"{today}: 无符合条件的股票")
        return

    target = valid[0]
    logger.info(f"{today}: 选择 {target}")

    if target in bar_dict:
        bar = bar_dict[target]
        if bar.is_trading:
            bars = history_bars(target, 1, "1d", ["close", "limit_up"])
            if bars is not None and len(bars) > 0:
                limit_up = bars[-1]["limit_up"]

                if bar.open < limit_up * 0.99:
                    order_shares(target, 1000)
                    context.trades += 1
                    logger.info(f"{today}: 买入 {target} @ {bar.open}")


def after_trading(context):
    pass


__all__ = ["init", "daily_check", "after_trading"]
