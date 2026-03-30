"""
因子排序与增强过滤验证策略
测试: 无增强 vs 单因子 vs 双因子 vs 多因子
"""

from jqdata import *
from jqfactor import *
from jqlib.technical_analysis import *
import pandas as pd
import numpy as np


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.test_mode = "double_factor"  # 'no_enhance' | 'single_factor' | 'double_factor' | 'multi_factor'
    g.max_cap = 50  # 亿
    g.max_turnover = 30  # %
    g.ps = 5

    run_daily(get_stock_list, "9:25")
    run_daily(buy, "9:30")
    run_daily(sell, "14:50")


def get_stock_list(context):
    date = context.previous_date.strftime("%Y-%m-%d")

    # 基础信号: 昨日涨停的非ST非新股
    initial_list = get_all_securities("stock", date).index.tolist()
    initial_list = [s for s in initial_list if s[:2] != "68" and s[0] not in ["4", "8"]]
    initial_list = [
        s
        for s in initial_list
        if (context.previous_date - get_security_info(s).start_date).days > 250
    ]

    is_st = get_extras("is_st", initial_list, start_date=date, end_date=date, df=True).T
    initial_list = [s for s in initial_list if not is_st.loc[s].iloc[0]]

    # 昨日涨停
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

    # 因子筛选
    if g.test_mode == "no_enhance":
        filtered = base_signals
    elif g.test_mode == "single_factor":
        filtered = filter_by_market_cap(base_signals, date, g.max_cap)
    elif g.test_mode == "double_factor":
        filtered = filter_by_market_cap(base_signals, date, g.max_cap)
        filtered = filter_by_turnover(filtered, date, g.max_turnover)
    else:  # multi_factor
        filtered = filter_by_market_cap(base_signals, date, g.max_cap)
        filtered = filter_by_turnover(filtered, date, g.max_turnover)
        filtered = sort_by_multi_factors(filtered, date)

    g.target_list = filtered[: g.ps]
    log.info(f"{g.test_mode}: 基础信号{len(base_signals)} -> 筛选后{len(filtered)}")


def filter_by_market_cap(stock_list, date, max_cap):
    if not stock_list:
        return []
    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.code.in_(stock_list)
    )
    df = get_fundamentals(q, date)
    df = df[df["circulating_market_cap"] < max_cap]
    return list(df["code"])


def filter_by_turnover(stock_list, date, max_turnover):
    if not stock_list:
        return []
    result = []
    for s in stock_list:
        try:
            hsl = HSL([s], date)[0][s]
            if hsl < max_turnover:
                result.append(s)
        except:
            pass
    return result


def sort_by_multi_factors(stock_list, date):
    if not stock_list:
        return []
    scores = []
    for s in stock_list:
        score = 0
        try:
            cap = get_fundamentals(
                query(valuation.circulating_market_cap).filter(valuation.code == s),
                date,
            ).iloc[0, 0]
            score += (1 - cap / 50) * 40

            hsl = HSL([s], date)[0][s]
            score += (1 - hsl / 30) * 30
        except:
            pass
        scores.append((s, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scores]


def buy(context):
    current_data = get_current_data()
    for s in g.target_list:
        if context.portfolio.available_cash > 100:
            order_value(s, context.portfolio.total_value / g.ps)


def sell(context):
    current_data = get_current_data()
    for s in list(context.portfolio.positions):
        if current_data[s].last_price < current_data[s].high_limit:
            order_target_value(s, 0)
