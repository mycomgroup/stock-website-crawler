from jqdata import *
import datetime as dt


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trade_count = 0
    g.win_count = 0
    g.pnl_list = []

    run_daily(select_stocks, "9:00")
    run_daily(buy_stocks, "09:35")
    run_daily(sell_stocks, "14:50")


def select_stocks(context):
    g.target = []
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    df = get_price(
        all_stocks,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    g.target = list(df["code"])


def buy_stocks(context):
    if not g.target:
        return

    current_data = get_current_data()
    qualified = []

    for s in g.target[:20]:
        if s not in current_data:
            continue
        cd = current_data[s]
        if cd.paused:
            continue

        high_limit = cd.high_limit
        day_open = cd.day_open

        open_pct = (day_open - cd.pre_close) / cd.pre_close * 100

        if -1.5 <= open_pct <= 1.5:
            qualified.append(s)

    if qualified:
        cash = context.portfolio.available_cash / min(len(qualified), 3)
        for s in qualified[:3]:
            price = current_data[s].last_price
            shares = int(cash / price / 100) * 100
            if shares >= 100:
                order(s, shares)
                g.trade_count += 1


def sell_stocks(context):
    current_data = get_current_data()
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            cd = current_data[s]
            pnl = (cd.last_price - pos.avg_cost) / pos.avg_cost * 100
            g.pnl_list.append(pnl)
            if pnl > 0:
                g.win_count += 1
            order_target(s, 0)
