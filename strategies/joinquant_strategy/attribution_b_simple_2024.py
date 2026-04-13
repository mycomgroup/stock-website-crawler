# 策略B：小市值 + 事件（简化版 - 2024年测试）
# 选股：流通市值5-15亿 + 首板 + 低开
# 次日退出
# 持仓1只

from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trade_count = 0
    g.win_count = 0
    g.pnl_list = []

    set_benchmark("000300.XSHG")

    run_daily(select_stocks, "9:00")
    run_daily(buy_stocks, "09:31")
    run_daily(sell_stocks, "14:50")


def select_stocks(context):
    g.target = []
    prev_date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"
    ]
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

    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.code.in_(all_stocks),
        valuation.circulating_market_cap >= 5,
        valuation.circulating_market_cap <= 15,
    )
    val_df = get_fundamentals(q, date=prev_date)
    if val_df.empty:
        return
    small_cap_stocks = set(val_df["code"])

    df = get_price(
        list(small_cap_stocks),
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

    for s in g.target:
        if s not in current_data:
            continue

        cd = current_data[s]
        if cd.paused:
            continue

        prev_close = cd.pre_close
        if prev_close <= 0:
            continue

        day_open = cd.day_open
        open_pct = (day_open - prev_close) / prev_close * 100

        if -3.0 <= open_pct <= 1.5:
            qualified.append(s)

    if qualified:
        target = qualified[0]
        cash = context.portfolio.available_cash
        price = current_data[target].last_price
        shares = int(cash / price / 100) * 100
        if shares >= 100:
            order(target, shares)
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
