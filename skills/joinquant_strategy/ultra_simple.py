from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")
    set_benchmark("000300.XSHG")

    g.trades = 0
    run_daily(buy, "09:31")
    run_daily(sell, "14:50")


def buy(context):
    prev = context.previous_date.strftime("%Y-%m-%d")

    # 只查100只股票
    stocks = get_all_securities("stock", prev).index.tolist()[:100]
    stocks = [s for s in stocks if s[0] not in "483"]

    try:
        df = get_price(
            stocks, end_date=prev, count=1, fields=["close", "high_limit"], panel=False
        )
        df = df.dropna()
        hl = df[df["close"] == df["high_limit"]]
        targets = list(hl["code"])[:5]
    except:
        targets = ["000001.XSHE"]

    current = get_current_data()
    for s in targets:
        cd = current.get(s)
        if cd and not cd.paused and not cd.is_st:
            open_pct = (cd.day_open - cd.pre_close) / cd.pre_close * 100
            if -1.5 <= open_pct <= 1.5:
                order_value(s, context.portfolio.available_cash / 3)
                g.trades += 1


def sell(context):
    for s in list(context.portfolio.positions):
        if context.portfolio.positions[s].closeable_amount > 0:
            order_target(s, 0)
