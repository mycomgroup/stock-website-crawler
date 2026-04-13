# 首板低开策略 - 简化测试版
# 假弱高开结构 (+0.5% ~ +1.5%)

from jqdata import *
import datetime as dt


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.target_list = []
    g.trade_count = 0

    run_daily(get_stock_list, "9:00")
    run_daily(buy, "09:31")
    run_daily(sell, "14:50")


def get_stock_list(context):
    date_str = context.previous_date.strftime("%Y-%m-%d")
    initial_list = get_all_securities("stock", date_str).index.tolist()
    initial_list = [
        s for s in initial_list if s[0] not in ["4", "8", "3"] and s[:2] != "68"
    ]
    initial_list = [
        s
        for s in initial_list
        if (context.previous_date - get_security_info(s).start_date).days > 250
    ]

    df = get_price(
        initial_list,
        end_date=date_str,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    g.target_list = list(df["code"])


def buy(context):
    if len(g.target_list) == 0:
        return

    current_data = get_current_data()
    qualified = []

    for s in g.target_list:
        if s not in current_data:
            continue

        cd = current_data[s]
        if cd.paused or cd.is_st:
            continue

        prev_close = cd.pre_close
        if prev_close <= 0:
            continue

        high_limit = cd.high_limit
        day_open = cd.day_open

        open_ratio = day_open / (high_limit / 1.1)

        if 1.005 <= open_ratio <= 1.015:
            val = get_valuation(s, end_date=context.previous_date, count=1)
            if val is not None and len(val) > 0:
                cap = val["circulating_market_cap"].iloc[0]
                if 50 <= cap <= 150:
                    qualified.append(s)

    if len(qualified) > 0:
        cash_per_stock = context.portfolio.available_cash / len(qualified)
        for s in qualified:
            price = current_data[s].last_price
            if cash_per_stock / price > 100:
                order_value(s, cash_per_stock)
                g.trade_count += 1


def sell(context):
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            order_target_value(s, 0)
