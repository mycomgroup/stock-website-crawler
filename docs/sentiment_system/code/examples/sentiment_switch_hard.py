# 首板低开策略 - 硬开关版本
from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.ps = 3
    g.use_switch = True
    set_benchmark("000300.XSHG")


def before_trading_start(context):
    date = context.previous_date.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
    ]

    df = get_price(
        all_stocks,
        end_date=date,
        frequency="daily",
        fields=["paused", "close", "high_limit", "low_limit"],
        count=1,
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()
    df = df[df["paused"] == 0]

    zt = df[df["close"] == df["high_limit"]]["code"].tolist()
    dt = df[df["close"] == df["low_limit"]]["code"].tolist()

    g.prev_zt = zt
    g.zt_count = len(zt)
    g.dt_count = len(dt)
    g.zt_dt_ratio = g.zt_count / max(g.dt_count, 1)

    max_lb = 0
    for stock in zt[:30]:
        d = get_price(
            stock,
            end_date=date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=10,
            panel=False,
            fill_paused=False,
        )
        if len(d) == 0:
            continue
        c = 0
        for i in range(len(d) - 1, -1, -1):
            if d.iloc[i]["close"] == d.iloc[i]["high_limit"]:
                c += 1
            else:
                break
        max_lb = max(max_lb, c)

    g.max_lianban = max_lb

    if g.use_switch:
        g.allow_buy = g.max_lianban >= 2 and g.zt_count >= 15 and g.zt_dt_ratio >= 1.5
    else:
        g.allow_buy = True


def handle_data(context, data):
    if hasattr(g, "allow_buy") and not g.allow_buy:
        return

    if not hasattr(g, "prev_zt") or len(g.prev_zt) == 0:
        return

    current_data = get_current_data()

    target = []
    for stock in g.prev_zt[:50]:
        if stock not in current_data:
            continue

        cd = current_data[stock]
        prev_close = cd.pre_close
        day_open = cd.day_open
        low_limit = cd.low_limit

        if prev_close <= 0 or day_open <= 0:
            continue

        open_ratio = day_open / prev_close - 1

        if -0.05 <= open_ratio <= -0.01 and day_open > low_limit:
            target.append(stock)

    if len(target) == 0:
        return

    target = target[: g.ps]

    for stock in list(context.portfolio.positions):
        order_target_value(stock, 0)

    value = context.portfolio.total_value / g.ps
    for stock in target:
        order_value(stock, value)
