# 状态路由器 v1 - 简化版（快速回测）
from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.state = "正常"
    g.target_position = 70
    g.hs300_stocks = []
    set_benchmark("000300.XSHG")

    run_daily(update_hs300, time="09:00")


def update_hs300(context):
    date = context.current_dt.strftime("%Y-%m-%d")
    g.hs300_stocks = get_index_stocks("000300.XSHG", date)[:30]


def before_trading_start(context):
    date = context.previous_date.strftime("%Y-%m-%d")

    breadth_pct = calculate_breadth_simple(date)
    zt_count = get_zt_count_cached(date)

    g.breadth_pct = breadth_pct
    g.zt_count = zt_count

    breadth_level = classify_breadth(breadth_pct)
    sentiment_level = classify_sentiment(zt_count)

    state, position = get_state_position(breadth_level, sentiment_level)

    g.state = state
    g.target_position = position


def calculate_breadth_simple(date):
    if not hasattr(g, "hs300_stocks") or len(g.hs300_stocks) == 0:
        g.hs300_stocks = get_index_stocks("000300.XSHG", date)[:30]

    count_above = 0
    checked = 0

    for stock in g.hs300_stocks:
        prices = get_price(
            stock,
            end_date=date,
            count=21,
            fields=["close"],
            panel=False,
            fill_paused=False,
        )
        if len(prices) < 21:
            continue

        checked += 1
        ma20 = float(prices["close"].iloc[:20].mean())
        current = float(prices["close"].iloc[-1])

        if current > ma20:
            count_above += 1

    if checked == 0:
        return 30

    return count_above / checked * 100


def get_zt_count_cached(date):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
    ]

    df = get_price(
        all_stocks[:200],
        end_date=date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
        fill_paused=False,
    )

    if df.empty:
        return 40

    df = df.dropna()

    return len(df[df["close"] == df["high_limit"]])


def classify_breadth(pct):
    if pct < 15:
        return 1
    elif pct < 25:
        return 2
    elif pct < 35:
        return 3
    else:
        return 4


def classify_sentiment(count):
    if count < 30:
        return 1
    elif count < 50:
        return 2
    elif count < 80:
        return 3
    else:
        return 4


def get_state_position(breadth_level, sentiment_level):
    if breadth_level == 1:
        return ("关闭", 0)

    elif breadth_level == 2:
        if sentiment_level <= 2:
            return ("防守", 30)
        else:
            return ("轻仓", 50)

    elif breadth_level == 3:
        if sentiment_level == 2:
            return ("轻仓", 50)
        elif sentiment_level == 3:
            return ("正常", 70)
        elif sentiment_level == 4:
            return ("进攻", 100)
        else:
            return ("防守", 30)

    else:
        if sentiment_level == 4:
            return ("进攻", 100)
        elif sentiment_level == 3:
            return ("正常", 70)
        else:
            return ("轻仓", 50)


def handle_data(context, data):
    if g.target_position == 0:
        for stock in list(context.portfolio.positions):
            order_target_value(stock, 0)
        return

    target_value = context.portfolio.total_value * g.target_position / 100

    if "000300.XSHG" in context.portfolio.positions:
        current_value = context.portfolio.positions["000300.XSHG"].value
    else:
        current_value = 0

    if abs(target_value - current_value) > context.portfolio.total_value * 0.05:
        order_value("000300.XSHG", target_value)
