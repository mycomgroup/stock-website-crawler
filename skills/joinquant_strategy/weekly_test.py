from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")

    g.trades = 0
    g.wins = 0
    g.pnl_list = []

    set_benchmark("000300.XSHG")


def handle_data(context, data):
    date = context.current_dt.date()

    if context.current_dt.hour != 9 or context.current_dt.minute != 35:
        return

    if date.weekday() != 0:
        return

    stocks = ["000001.XSHE", "600000.XSHG", "000002.XSHE", "600036.XSHG"]

    current_data = get_current_data()
    cash = context.portfolio.available_cash / len(stocks)

    for s in stocks:
        if s in current_data and not current_data[s].paused:
            price = current_data[s].last_price
            shares = int(cash / price / 100) * 100
            if shares >= 100:
                order(s, shares)
                g.trades += 1

    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            cd = get_current_data()
            pnl = (cd[s].last_price - pos.avg_cost) / pos.avg_cost * 100
            g.pnl_list.append(pnl)
            if pnl > 0:
                g.wins += 1
            order_target(s, 0)

    if date.month == 12 and date.day >= 25:
        log.info(
            f"Total trades: {g.trades}, Wins: {g.wins}, Avg PnL: {sum(g.pnl_list) / len(g.pnl_list) if g.pnl_list else 0:.2f}%"
        )
