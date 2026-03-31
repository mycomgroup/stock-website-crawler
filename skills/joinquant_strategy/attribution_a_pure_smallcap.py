# 策略A：纯小市值因子
# 选股：流通市值最小的前10%
# 月度等权调仓
# 持仓20只

from jqdata import *
import datetime as dt


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.trade_count = 0
    g.win_count = 0
    g.pnl_list = []

    set_benchmark("000300.XSHG")

    run_monthly(rebalance, 1, "09:35")


def rebalance(context):
    date_str = context.current_dt.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", date_str).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] not in ["4", "8", "3"] and s[:2] != "68"
    ]
    all_stocks = [
        s
        for s in all_stocks
        if (context.current_dt - get_security_info(s).start_date).days > 250
    ]

    st_df = get_extras(
        "is_st", all_stocks, start_date=date_str, end_date=date_str, df=True
    ).T
    st_df.columns = ["is_st"]
    all_stocks = list(st_df[st_df["is_st"] == False].index)

    q = (
        query(valuation.code, valuation.circulating_market_cap)
        .filter(valuation.code.in_(all_stocks), valuation.circulating_market_cap > 0)
        .order_by(valuation.circulating_market_cap.asc())
        .limit(300)
    )

    df = get_fundamentals(q, date=date_str)
    if df.empty:
        return

    target_count = max(1, int(len(df) * 0.1))
    target = list(df["code"])[: min(target_count, 20)]

    for s in list(context.portfolio.positions):
        if s not in target:
            order_target(s, 0)

    if target:
        cash_per_stock = context.portfolio.total_value / len(target)
        for s in target:
            order_target_value(s, cash_per_stock)
