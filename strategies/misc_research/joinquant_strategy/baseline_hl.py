from jqdata import *
import datetime as dt


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trades = 0
    g.wins = 0
    g.pnl_list = []

    run_daily(select_stocks, "9:00")
    run_daily(buy_stocks, "09:35")
    run_daily(sell_stocks, "14:50")


def select_stocks(context):
    g.target = []
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]
    all_stocks = [
        s
        for s in all_stocks
        if (context.previous_date - get_security_info(s).start_date).days > 250
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
    g.target = list(df["code"])


def buy_stocks(context):
    if not g.target:
        return

    current_data = get_current_data()

    # 对比组：无过滤，随机选3只
    stocks = g.target[:3]

    if stocks:
        cash = context.portfolio.available_cash / len(stocks)
        for s in stocks:
            if s in current_data and not current_data[s].paused:
                price = current_data[s].last_price
                shares = int(cash / price / 100) * 100
                if shares >= 100:
                    order(s, shares)
                    g.trades += 1


def sell_stocks(context):
    current_data = get_current_data()
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            cd = current_data[s]
            pnl = (cd.last_price - pos.avg_cost) / pos.avg_cost * 100
            g.pnl_list.append(pnl)
            if pnl > 0:
                g.wins += 1
            order_target(s, 0)
