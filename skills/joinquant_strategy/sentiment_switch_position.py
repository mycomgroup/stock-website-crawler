# 首板低开策略 - 仓位调节器版本
from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.ps = 3
    g.use_position = True
    run_daily(get_stock_list, "9:00")
    run_daily(calc_sentiment, "9:05")
    run_daily(buy, "9:30")
    run_daily(sell, "14:50")


def get_stock_list(context):
    date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
    ]

    price_df = get_price(
        all_stocks,
        end_date=date,
        frequency="daily",
        fields=["paused", "close", "high_limit", "low_limit"],
        count=1,
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    price_df = price_df.dropna()
    price_df = price_df[price_df["paused"] == 0]

    zt_stocks = price_df[price_df["close"] == price_df["high_limit"]]["code"].tolist()
    dt_stocks = price_df[price_df["close"] == price_df["low_limit"]]["code"].tolist()

    g.prev_zt = zt_stocks
    g.zt_count = len(zt_stocks)
    g.dt_count = len(dt_stocks)
    g.zt_dt_ratio = g.zt_count / max(g.dt_count, 1)


def calc_sentiment(context):
    date = context.previous_date.strftime("%Y-%m-%d")

    max_lianban = 0
    if hasattr(g, "prev_zt") and len(g.prev_zt) > 0:
        for stock in g.prev_zt[:30]:
            df = get_price(
                stock,
                end_date=date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=10,
                panel=False,
                fill_paused=False,
                skip_paused=True,
            )
            if len(df) == 0:
                continue

            count = 0
            for i in range(len(df) - 1, -1, -1):
                if df.iloc[i]["close"] == df.iloc[i]["high_limit"]:
                    count += 1
                else:
                    break
            max_lianban = max(max_lianban, count)

    g.max_lianban = max_lianban

    if g.use_position:
        if g.max_lianban >= 5 and g.zt_count >= 40:
            g.position_ratio = 0.3
        elif g.max_lianban >= 3 and g.zt_count >= 25:
            g.position_ratio = 1.0
        elif g.max_lianban >= 2 and g.zt_count >= 15:
            g.position_ratio = 0.5
        else:
            g.position_ratio = 0.0
    else:
        g.position_ratio = 1.0


def buy(context):
    if hasattr(g, "position_ratio") and g.position_ratio == 0:
        return

    date = context.current_dt.strftime("%Y-%m-%d")
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    if not hasattr(g, "prev_zt") or len(g.prev_zt) == 0:
        return

    current_data = get_current_data()

    target_stocks = []
    for stock in g.prev_zt[:30]:
        if stock not in current_data:
            continue

        prev_close = current_data[stock].pre_close
        day_open = current_data[stock].day_open
        low_limit = current_data[stock].low_limit

        if prev_close <= 0:
            continue

        open_ratio = day_open / prev_close - 1

        if -0.05 <= open_ratio <= -0.01 and day_open > low_limit:
            target_stocks.append(stock)

    if len(target_stocks) == 0:
        return

    target_stocks = target_stocks[: g.ps]

    base_value = context.portfolio.total_value / g.ps
    position_ratio = g.position_ratio if hasattr(g, "position_ratio") else 1.0
    value = base_value * position_ratio

    for stock in target_stocks:
        if context.portfolio.available_cash > value:
            order_value(stock, value)


def sell(context):
    hold_list = list(context.portfolio.positions)
    current_data = get_current_data()

    for stock in hold_list:
        if context.portfolio.positions[stock].closeable_amount > 0:
            order_target_value(stock, 0)
