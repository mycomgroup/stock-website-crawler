# 首板低开策略 - 无开关版
from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")
    g.ps = 3
    g.target = []


def before_trading(context):
    date = context.previous_date.strftime("%Y-%m-%d")
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in ["4", "8"] and s[:2] != "68"]

    df = get_price(
        all_stocks,
        end_date=date,
        frequency="daily",
        fields=["paused", "close", "high_limit"],
        count=1,
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()
    df = df[df["paused"] == 0]
    zt = df[df["close"] == df["high_limit"]]["code"].tolist()
    g.prev_zt = zt
    g.target = []


def handle_data(context, data):
    if not hasattr(g, "prev_zt") or len(g.prev_zt) == 0:
        return

    # 清仓
    for stock in list(context.portfolio.positions):
        order_target_value(stock, 0)

    # 选股
    current = get_current_data()
    selected = []
    for stock in g.prev_zt[:100]:
        if stock not in current:
            continue
        cd = current[stock]
        if cd.pre_close <= 0:
            continue

        ratio = cd.day_open / cd.pre_close - 1
        if -0.05 <= ratio <= -0.01 and cd.day_open > cd.low_limit:
            selected.append(stock)

    if len(selected) == 0:
        return

    g.target = selected[: g.ps]
    value = context.portfolio.total_value / g.ps

    for stock in g.target:
        order_value(stock, value)
