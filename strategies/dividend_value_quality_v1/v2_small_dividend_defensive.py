# 红利/价值/质量 策略 V2: 红利小盘 防守版
# 纯防守策略，熊市正收益，牛市也有弹性

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

    g.stock_num = 15  # 小盘股适当减少持仓数
    g.hold_list = []
    g.target_list = []

    run_monthly(adjust_position, 1, time="9:30")
    run_daily(check_limit_up, time="14:00")


def select_small_dividend(context, n=15):
    """红利小盘选股: 小市值 + 低PE + 正增长"""
    date = str(context.previous_date)

    # 全市场选股
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
            valuation.market_cap > 10,  # 市值>10亿
            valuation.market_cap < 100,  # 市值<100亿
            valuation.pe_ratio > 0,
            valuation.pe_ratio < 30,
            indicator.inc_net_profit_year_on_year > 5,  # 利润增长>5%
        )
        .order_by(valuation.pe_ratio.asc())
        .limit(n * 3)
    )

    df = get_fundamentals(q, date=date)

    # 过滤ST、停牌、科创板、北交所
    current_data = get_current_data()
    df = df[
        df["code"].apply(
            lambda x: not current_data[x].is_st
            and not current_data[x].paused
            and "ST" not in current_data[x].name
            and "退" not in current_data[x].name
            and not x.startswith("68")  # 科创板
            and not x.startswith("8")  # 北交所
            and not x.startswith("4")  # 北交所
        )
    ]

    # 流通市值过滤（避免流动性太差）
    df = df[df["circulating_market_cap"] > 20]  # 流通市值>20亿

    return df["code"].tolist()[:n]


def adjust_position(context):
    """月度调仓"""
    g.target_list = select_small_dividend(context, g.stock_num)

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
            if stock in g.hold_list:
                order_target(stock, 0)
                log.info(f"涨停打开卖出: {stock}")


def after_trading_end(context):
    """收盘后更新持仓列表"""
    g.hold_list = list(context.portfolio.positions.keys())
