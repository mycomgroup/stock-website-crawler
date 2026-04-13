from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trades = 0
    g.wins = 0
    g.total_pnl = 0

    run_daily(buy, "09:35")
    run_daily(sell, "14:50")


def buy(context):
    date_str = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", date_str).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483" and s[:2] != "68"]

    df = get_price(
        all_stocks,
        end_date=date_str,
        frequency="daily",
        fields=["close", "high_limit", "paused"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    df = df[df["paused"] == 0]
    df = df[df["close"] == df["high_limit"]]

    hl_stocks = list(df["code"])[:5]

    if len(hl_stocks) == 0:
        return

    current_data = get_current_data()
    cash_per = context.portfolio.available_cash / len(hl_stocks)

    for s in hl_stocks:
        if s in current_data and not current_data[s].paused:
            order_value(s, cash_per)
            g.trades += 1


def sell(context):
    current_data = get_current_data()
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            pnl = (current_data[s].last_price - pos.avg_cost) / pos.avg_cost * 100
            g.total_pnl += pnl
            if pnl > 0:
                g.wins += 1
            order_target_value(s, 0)

    if context.current_dt.strftime("%Y-%m-%d").endswith("-12-31"):
        log.info(f"Trades: {g.trades}, Wins: {g.wins}, Total PnL: {g.total_pnl:.2f}%")
