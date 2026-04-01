# 红利/价值/质量 策略 V3: 静态组合版 (60/40)
# RFScore7进攻60% + 红利小盘防守40%

from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    set_benchmark("000300.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    set_slippage(FixedSlippage(0.001))
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.00012,
            close_commission=0.00012,
            min_commission=5,
        ),
        type="stock",
    )
    log.set_level("order", "error")

    # 组合配置
    g.rfscore_weight = 0.6  # RFScore7权重
    g.dividend_weight = 0.4  # 红利小盘权重
    g.total_stock_num = 25  # 总持仓数
    g.rfscore_num = 15  # RFScore7持仓数
    g.dividend_num = 10  # 红利小盘持仓数

    g.hold_list = []
    g.target_rfscore = []
    g.target_dividend = []

    run_monthly(adjust_position, 1, time="9:30")
    run_daily(check_limit_up, time="14:00")


def select_rfscore7(context, n=15):
    """RFScore7 + PB低20%选股"""
    date = str(context.previous_date)

    stocks_300 = get_index_stocks("000300.XSHG", date=date)
    stocks_500 = get_index_stocks("000905.XSHG", date=date)
    stocks = list(set(stocks_300 + stocks_500))

    current_data = get_current_data()
    stocks = [
        s
        for s in stocks
        if not current_data[s].is_st
        and not current_data[s].paused
        and "ST" not in current_data[s].name
        and "退" not in current_data[s].name
    ]

    q = (
        query(valuation.code, valuation.pb_ratio, indicator.roa, indicator.roe)
        .filter(
            valuation.code.in_(stocks),
            valuation.pe_ratio > 0,
            valuation.pb_ratio > 0,
            indicator.roa > 0,
        )
        .order_by(valuation.pb_ratio.asc())
        .limit(int(len(stocks) * 0.2))
    )

    df = get_fundamentals(q, date=date)
    df = df.sort_values("roa", ascending=False)

    return df["code"].tolist()[:n]


def select_small_dividend(context, n=10):
    """红利小盘选股"""
    date = str(context.previous_date)

    q = (
        query(
            valuation.code,
            valuation.pe_ratio,
            valuation.pb_ratio,
            valuation.market_cap,
            valuation.circulating_market_cap,
            indicator.inc_net_profit_year_on_year,
            indicator.roe,
        )
        .filter(
            valuation.market_cap > 10,
            valuation.market_cap < 100,
            valuation.pe_ratio > 0,
            valuation.pe_ratio < 30,
            indicator.inc_net_profit_year_on_year > 5,
        )
        .order_by(valuation.pe_ratio.asc())
        .limit(n * 3)
    )

    df = get_fundamentals(q, date=date)

    current_data = get_current_data()
    df = df[
        df["code"].apply(
            lambda x: not current_data[x].is_st
            and not current_data[x].paused
            and "ST" not in current_data[x].name
            and "退" not in current_data[x].name
            and not x.startswith("68")
            and not x.startswith("8")
            and not x.startswith("4")
        )
    ]

    df = df[df["circulating_market_cap"] > 20]

    return df["code"].tolist()[:n]


def adjust_position(context):
    """月度调仓"""
    # 获取两组选股
    g.target_rfscore = select_rfscore7(context, g.rfscore_num)
    g.target_dividend = select_small_dividend(context, g.dividend_num)

    # 合并目标列表
    g.target_list = g.target_rfscore + g.target_dividend

    # 卖出不在目标列表的持仓
    for stock in context.portfolio.positions:
        if stock not in g.target_list:
            if not get_current_data()[stock].paused:
                order_target(stock, 0)
                log.info(f"卖出: {stock}")

    # 按权重分配资金买入
    total_value = context.portfolio.total_value

    # 买入RFScore7股票
    rfscore_value = total_value * g.rfscore_weight / g.rfscore_num
    for stock in g.target_rfscore:
        if stock not in context.portfolio.positions:
            if order_value(stock, rfscore_value):
                log.info(f"买入RFScore7: {stock}")

    # 买入红利小盘股票
    dividend_value = total_value * g.dividend_weight / g.dividend_num
    for stock in g.target_dividend:
        if stock not in context.portfolio.positions:
            if order_value(stock, dividend_value):
                log.info(f"买入红利小盘: {stock}")


def check_limit_up(context):
    """检查涨停股"""
    current_data = get_current_data()
    for stock in context.portfolio.positions:
        if current_data[stock].last_price < current_data[stock].high_limit:
            if stock in g.hold_list:
                order_target(stock, 0)
                log.info(f"涨停打开卖出: {stock}")


def after_trading_end(context):
    """收盘后更新持仓列表"""
    g.hold_list = list(context.portfolio.positions.keys())
