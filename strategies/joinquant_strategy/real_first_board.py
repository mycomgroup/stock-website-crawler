from jqdata import *

SLIPPAGE_BPS = 0


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")
    set_benchmark("000300.XSHG")

    if SLIPPAGE_BPS > 0:
        set_slippage(FixedSlippage(SLIPPAGE_BPS / 10000))

    g.trades = 0
    run_daily(select, "09:00")
    run_daily(buy, "09:32")
    run_daily(sell, "14:50")


def select(context):
    g.targets = []
    prev = context.previous_date.strftime("%Y-%m-%d")

    # 获取所有股票
    stocks = get_all_securities("stock", prev).index.tolist()
    stocks = [s for s in stocks if s[0] not in "483" and s[:2] != "68"]

    # 找涨停
    df = get_price(
        stocks, end_date=prev, count=1, fields=["close", "high_limit"], panel=False
    )
    df = df.dropna()
    hl = df[df["close"] == df["high_limit"]]
    g.targets = list(hl["code"])[:30]


def buy(context):
    if not g.targets:
        return

    curr = get_current_data()
    buy_list = []

    for s in g.targets:
        cd = curr.get(s)
        if not cd or cd.paused or cd.is_st:
            continue

        open_pct = (cd.day_open - cd.pre_close) / cd.pre_close * 100
        if -1.5 <= open_pct <= 1.5:
            # 检查市值
            val = get_valuation(s, end_date=context.previous_date, count=1, panel=False)
            if val is not None and len(val) > 0:
                cap = val["circulating_market_cap"].iloc[0]
                if 5 <= cap <= 30:  # 5-30亿
                    buy_list.append((s, cap))

    if buy_list:
        # 按市值从小到大排序
        buy_list.sort(key=lambda x: x[1])
        cash = context.portfolio.available_cash / min(len(buy_list), 3)
        for s, _ in buy_list[:3]:
            order_value(s, cash)
            g.trades += 1


def sell(context):
    curr = get_current_data()
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            order_target(s, 0)
