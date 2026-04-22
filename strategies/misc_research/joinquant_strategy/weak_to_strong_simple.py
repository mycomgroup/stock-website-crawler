#!/usr/bin/env python3
"""弱转强竞价策略 - 极简测试版"""

from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("order", "error")
    log.set_level("system", "error")

    g.stocks = []
    run_daily(select_stocks, "9:00")
    run_daily(buy_stocks, "9:30")
    run_daily(sell_stocks, "14:50")


def select_stocks(context):
    date = context.current_dt.date()
    date_str = str(date)

    stocks = []

    all_stocks = get_all_securities("stock", date).index
    all_stocks = [
        s for s in all_stocks if s[0] not in ["3", "4", "8"] and s[:2] != "68"
    ]

    for stock in all_stocks[:200]:
        try:
            df = get_price(
                stock,
                end_date=date_str,
                count=2,
                fields=["close", "high_limit", "money", "volume"],
                panel=False,
                skip_paused=True,
            )
            if df.empty or len(df) < 2:
                continue

            yesterday_close = df["close"].iloc[0]
            yesterday_high_limit = df["high_limit"].iloc[0]
            yesterday_money = df["money"].iloc[0]

            if yesterday_close != yesterday_high_limit:
                continue

            if yesterday_money < 500000000:
                continue

            valuation = get_valuation(
                stock, end_date=date_str, count=1, fields=["market_cap"]
            )
            if valuation.empty or valuation["market_cap"].iloc[-1] < 30:
                continue

            today_df = get_price(
                stock,
                end_date=date_str,
                count=1,
                fields=["open", "high_limit"],
                panel=False,
                skip_paused=True,
            )
            if today_df.empty:
                continue

            today_open = today_df["open"].iloc[-1]
            high_limit = today_df["high_limit"].iloc[-1]

            open_ratio = today_open / (high_limit / 1.1)

            if 1.02 <= open_ratio < 1.05:
                stocks.append(stock)

        except:
            continue

    g.stocks = stocks


def buy_stocks(context):
    if len(g.stocks) == 0:
        return

    cash = context.portfolio.available_cash
    per_stock = cash / len(g.stocks)

    for stock in g.stocks:
        try:
            order_value(stock, per_stock)
        except:
            continue


def sell_stocks(context):
    for stock in context.portfolio.positions:
        try:
            position = context.portfolio.positions[stock]
            if position.closeable_amount > 0:
                order_target(stock, 0)
        except:
            continue
