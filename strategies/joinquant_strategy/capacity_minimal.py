# 首板低开容量测试 - 极简版

from jqdata import *

SLIPPAGE_BPS = 0


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    if SLIPPAGE_BPS > 0:
        set_slippage(FixedSlippage(SLIPPAGE_BPS / 10000))

    set_benchmark("000300.XSHG")

    run_daily(buy, "09:31")
    run_daily(sell, "14:50")


def buy(context):
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    stocks = get_all_securities("stock", prev_date).index.tolist()
    stocks = [s for s in stocks if s[0] not in "483" and s[:2] != "68"]

    df = get_price(
        stocks, end_date=prev_date, count=1, fields=["close", "high_limit"], panel=False
    )
    df = df.dropna()
    hl = df[df["close"] == df["high_limit"]]

    if len(hl) == 0:
        return

    current_data = get_current_data()
    buy_list = []

    for code in list(hl["code"])[:10]:
        cd = current_data.get(code)
        if cd is None or cd.paused or cd.is_st:
            continue

        open_pct = (cd.day_open - cd.pre_close) / cd.pre_close * 100
        if -1.5 <= open_pct <= 1.5:
            buy_list.append(code)

    if buy_list:
        cash = context.portfolio.available_cash / len(buy_list)
        for code in buy_list[:3]:
            order_value(code, cash)


def sell(context):
    for s in list(context.portfolio.positions):
        if context.portfolio.positions[s].closeable_amount > 0:
            order_target(s, 0)
