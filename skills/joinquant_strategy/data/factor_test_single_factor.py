"""因子验证-单因子(市值)"""

from jqdata import *
from jqfactor import *
from jqlib.technical_analysis import *
import pandas as pd


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")
    g.max_cap = 50
    g.ps = 5
    run_daily(get_stock_list, "9:25")
    run_daily(buy, "9:30")
    run_daily(sell, "14:50")


def get_stock_list(context):
    date = context.previous_date.strftime("%Y-%m-%d")
    initial_list = get_all_securities("stock", date).index.tolist()
    initial_list = [s for s in initial_list if s[:2] != "68" and s[0] not in ["4", "8"]]
    initial_list = [
        s
        for s in initial_list
        if (context.previous_date - get_security_info(s).start_date).days > 250
    ]
    is_st = get_extras("is_st", initial_list, start_date=date, end_date=date, df=True).T
    initial_list = [s for s in initial_list if not is_st.loc[s].iloc[0]]
    df = get_price(
        initial_list,
        end_date=date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df[df["close"] == df["high_limit"]]
    base_signals = list(df["code"])

    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.code.in_(base_signals)
    )
    cap_df = get_fundamentals(q, date)
    cap_df = cap_df[cap_df["circulating_market_cap"] < g.max_cap]
    g.target_list = list(cap_df["code"])[: g.ps]
    log.info(f"single_factor: {len(base_signals)} -> {len(list(cap_df['code']))}")


def buy(context):
    for s in g.target_list:
        if context.portfolio.available_cash > 100:
            order_value(s, context.portfolio.total_value / g.ps)


def sell(context):
    current_data = get_current_data()
    for s in list(context.portfolio.positions):
        if current_data[s].last_price < current_data[s].high_limit:
            order_target_value(s, 0)
