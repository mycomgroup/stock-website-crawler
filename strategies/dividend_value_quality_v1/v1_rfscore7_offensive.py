# 红利/价值/质量 策略 V1: RFScore7 进攻版
# 纯进攻策略，牛市弹性大，熊市会亏

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

    g.stock_num = 20
    g.hold_list = []
    g.target_list = []

    run_monthly(adjust_position, 1, time="9:30")
    run_daily(check_limit_up, time="14:00")


def select_rfscore7(context, n=20):
    """RFScore7 + PB低20%选股"""
    date = str(context.previous_date)

    # 中证800股票池
    stocks_300 = get_index_stocks("000300.XSHG", date=date)
    stocks_500 = get_index_stocks("000905.XSHG", date=date)
    stocks = list(set(stocks_300 + stocks_500))

    # 过滤ST、停牌
    current_data = get_current_data()
    stocks = [
        s
        for s in stocks
        if not current_data[s].is_st
        and not current_data[s].paused
        and "ST" not in current_data[s].name
        and "退" not in current_data[s].name
    ]

    # PB低20%筛选
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

    # 按ROA排序
    df = df.sort_values("roa", ascending=False)

    return df["code"].tolist()[:n]


def adjust_position(context):
    """月度调仓"""
    g.target_list = select_rfscore7(context, g.stock_num)

    # 卖出不在目标列表的持仓
    for stock in context.portfolio.positions:
        if stock not in g.target_list:
            if not get_current_data()[stock].paused:
                order_target(stock, 0)
                log.info(f"卖出: {stock}")

    # 买入
    position_count = len(context.portfolio.positions)
    if g.stock_num > position_count:
        cash_per_stock = context.portfolio.available_cash / (
            g.stock_num - position_count
        )
        for stock in g.target_list:
            if stock not in context.portfolio.positions:
                if order_value(stock, cash_per_stock):
                    log.info(f"买入: {stock}")
                if len(context.portfolio.positions) >= g.stock_num:
                    break


def check_limit_up(context):
    """检查涨停股是否需要卖出"""
    current_data = get_current_data()
    for stock in context.portfolio.positions:
        if current_data[stock].last_price < current_data[stock].high_limit:
            # 涨停打开，卖出
            if stock in g.hold_list:
                order_target(stock, 0)
                log.info(f"涨停打开卖出: {stock}")


def after_trading_end(context):
    """收盘后更新持仓列表"""
    g.hold_list = list(context.portfolio.positions.keys())
