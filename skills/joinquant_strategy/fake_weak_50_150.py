from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    g.min_cap = 50
    g.max_cap = 150

    set_benchmark("000300.XSHG")

    run_daily(select_and_trade, "09:35")


def select_and_trade(context):
    date = context.current_dt.date()
    date_str = date.strftime("%Y-%m-%d")

    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            cd = get_current_data()
            if s in cd:
                pnl = (cd[s].last_price - pos.avg_cost) / pos.avg_cost * 100
                g.pnl_list.append(pnl)
                if pnl > 0:
                    g.wins += 1
            order_target(s, 0)

    prev_date = (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]
    all_stocks = [
        s for s in all_stocks if (date - get_security_info(s).start_date).days > 250
    ]

    st_df = get_extras(
        "is_st", all_stocks, start_date=prev_date, end_date=prev_date, df=True
    ).T
    st_df.columns = ["is_st"]
    all_stocks = list(st_df[st_df["is_st"] == False].index)

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
    hl_stocks = list(df["code"])

    if not hl_stocks:
        return

    current_data = get_current_data()
    fake_weak = []

    for s in hl_stocks:
        if s not in current_data:
            continue
        cd = current_data[s]
        if cd.paused:
            continue

        pre_close = cd.pre_close
        day_open = cd.day_open

        if pre_close <= 0:
            continue

        limit_price = pre_close * 1.1
        open_pct = (day_open / limit_price - 1) * 100

        if 0.5 <= open_pct <= 1.5:
            val = get_valuation(s, end_date=date, count=1)
            if val is not None and len(val) > 0:
                cap = val["circulating_market_cap"].iloc[0]
                if g.min_cap <= cap <= g.max_cap:
                    fake_weak.append({"stock": s, "open_pct": open_pct, "cap": cap})

    if fake_weak:
        fake_weak.sort(key=lambda x: abs(x["open_pct"] - 1.0))
        cash = context.portfolio.available_cash / min(len(fake_weak), 3)
        for item in fake_weak[:3]:
            s = item["stock"]
            order_value(s, cash)
            g.trades += 1


import datetime
