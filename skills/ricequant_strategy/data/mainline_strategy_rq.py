"""
主线策略：首板低开/假弱高开 - RiceQuant 策略编辑器版本
测试期间：2024-07-01 至 2025-03-31
"""


def init(context):
    context.position_stock = None
    context.entry_price = 0
    context.hold_days = 0
    context.max_hold_days = 2
    context.stop_loss_pct = -0.04
    scheduler.run_daily(select_and_trade, time_rule=market_open(minute=5))
    scheduler.run_daily(check_exit, time_rule=market_open(minute=120))


def get_limit_up_stocks(context, bar_dict):
    """获取昨日涨停股票"""
    today = context.now.date()
    prev_date = get_previous_trading_date(today)

    all_inst = all_instruments(type="CS", date=today)
    if all_inst is None or len(all_inst) == 0:
        return []

    stock_list = []
    for idx, row in all_inst.iterrows():
        obid = row["order_book_id"]
        if obid.startswith("688") or obid.startswith("4") or obid.startswith("8"):
            continue
        stock_list.append(obid)

    limit_up_stocks = []
    for stock in stock_list[:800]:
        try:
            bars = history_bars(
                stock, 2, "1d", ["close", "high", "limit_up"], bar_dict=bar_dict
            )
            if bars is None or len(bars) < 2:
                continue

            prev_close = bars[-2]["close"]
            prev_high = bars[-2]["high"]
            limit_up = bars[-1]["limit_up"]

            if (
                prev_close >= prev_high * 0.995
                and limit_up
                and prev_close >= limit_up * 0.99
            ):
                limit_up_stocks.append(stock)
        except:
            continue

    return limit_up_stocks


def select_and_trade(context, bar_dict):
    """选股并交易"""
    if context.position_stock is not None:
        return

    yesterday_zt = get_limit_up_stocks(context, bar_dict)

    if len(yesterday_zt) == 0:
        return

    selected = []
    for stock in yesterday_zt[:30]:
        try:
            bars = history_bars(
                stock, 2, "1d", ["close", "open", "limit_up"], bar_dict=bar_dict
            )
            if bars is None or len(bars) < 2:
                continue

            prev_close = bars[-2]["close"]
            today_open = bar_dict[stock].open if stock in bar_dict else None
            limit_up = bar_dict[stock].limit_up if stock in bar_dict else None

            if today_open is None or limit_up is None:
                continue

            open_pct = (today_open / prev_close - 1) * 100

            if 0.5 <= open_pct <= 1.5 and today_open < limit_up * 0.99:
                selected.append(
                    {"stock": stock, "open_pct": open_pct, "open_price": today_open}
                )
        except:
            continue

    if len(selected) == 0:
        return

    target = selected[0]
    stock = target["stock"]
    price = target["open_price"]

    cash = context.portfolio.total_value * 0.95
    shares = int(cash / price / 100) * 100

    if shares > 0:
        order_shares(stock, shares)
        context.position_stock = stock
        context.entry_price = price
        context.hold_days = 0
        print(f"[{context.now.date()}] Bought {stock} at {price:.2f}, shares: {shares}")


def check_exit(context, bar_dict):
    """检查卖出条件"""
    if context.position_stock is None:
        return

    stock = context.position_stock

    if stock not in bar_dict:
        return

    current_price = bar_dict[stock].close
    high_price = bar_dict[stock].high

    profit_pct = current_price / context.entry_price - 1

    sell_signal = False
    sell_reason = ""

    if profit_pct < context.stop_loss_pct:
        sell_signal = True
        sell_reason = "stop_loss"
    elif current_price >= bar_dict[stock].limit_up * 0.99:
        sell_signal = False
        sell_reason = "hold_limit_up"
    elif context.hold_days >= context.max_hold_days:
        sell_signal = True
        sell_reason = "max_hold"

    if sell_signal:
        order_target_percent(stock, 0)
        profit = (current_price / context.entry_price - 1) * 100
        print(
            f"[{context.now.date()}] Sold {stock} at {current_price:.2f}, profit: {profit:.2f}%, reason: {sell_reason}"
        )
        context.position_stock = None
        context.entry_price = 0
        context.hold_days = 0


def after_trading_end(context, bar_dict):
    if context.position_stock is not None:
        context.hold_days += 1
