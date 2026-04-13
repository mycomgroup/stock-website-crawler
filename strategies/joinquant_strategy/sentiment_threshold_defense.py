# 情绪指标阈值搜索 - 小市值防守线策略
from jqdata import *


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")
    g.ps = 10
    g.threshold = 30
    g.rebalance_days = 20
    g.days_counter = 0
    set_benchmark("000300.XSHG")


def before_trading_start(context):
    date = context.previous_date.strftime("%Y-%m-%d")
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in ["4", "8"] and s[:2] != "68"]

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
    g.zt_count = len(zt)
    g.allow_buy = g.zt_count >= g.threshold


def handle_data(context, data):
    g.days_counter += 1

    if g.days_counter < g.rebalance_days:
        return

    g.days_counter = 0

    if hasattr(g, "allow_buy") and not g.allow_buy:
        for stock in list(context.portfolio.positions):
            order_target_value(stock, 0)
        return

    date = context.previous_date.strftime("%Y-%m-%d")

    q = query(
        valuation.code,
        valuation.circulating_market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
    ).filter(
        valuation.circulating_market_cap >= 15,
        valuation.circulating_market_cap <= 60,
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 30,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < 3,
    )

    df = get_fundamentals(q, date=date)

    if df.empty:
        return

    df = df.sort_values("circulating_market_cap").head(g.ps * 2)
    target = df["code"].tolist()[: g.ps]

    for stock in list(context.portfolio.positions):
        if stock not in target:
            order_target_value(stock, 0)

    value = context.portfolio.total_value / g.ps
    for stock in target:
        order_value(stock, value)
