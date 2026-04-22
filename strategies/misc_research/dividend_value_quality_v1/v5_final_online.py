# 红利/价值/质量 策略 V5: 最终线上版
# 综合优化: 动态调仓 + 止损 + 风控 + 均线过滤

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

    # 策略参数
    g.total_stock_num = 25
    g.breadth_high = 0.50
    g.breadth_low = 0.35
    g.stop_loss_ratio = 0.08  # 个股止损线8%

    # 权重
    g.rfscore_weight = 0.6
    g.dividend_weight = 0.4
    g.rfscore_num = 15
    g.dividend_num = 10

    # 状态
    g.hold_list = []
    g.target_list = []
    g.market_state = "neutral"
    g.avg_costs = {}  # 记录持仓成本

    run_monthly(adjust_position, 1, time="9:30")
    run_daily(risk_control, time="10:00")  # 盘中风控
    run_daily(check_limit_up, time="14:00")


def calc_market_breadth(context):
    """计算市场宽度"""
    try:
        date = str(context.previous_date)
        trade_days = get_trade_days(end_date=date, count=21)
        if len(trade_days) < 21:
            return 0.5

        stocks = get_index_stocks("000300.XSHG", date=date)
        prices = get_price(
            stocks,
            start_date=trade_days[0],
            end_date=trade_days[-1],
            fields=["close"],
            panel=False,
        )
        pivot = prices.pivot(index="time", columns="code", values="close")

        if len(pivot) < 2:
            return 0.5

        ret = pivot.iloc[-1] / pivot.iloc[0] - 1
        return (ret > 0).sum() / len(ret)
    except:
        return 0.5


def calc_market_trend(context):
    """计算市场趋势"""
    try:
        date = str(context.previous_date)
        prices = get_price(
            "000300.XSHG", end_date=date, count=60, fields=["close"], panel=False
        )
        if len(prices) < 60:
            return True

        ma20 = prices["close"].iloc[-20:].mean()
        ma60 = prices["close"].mean()
        return ma20 > ma60
    except:
        return True


def get_dynamic_weights(context):
    """动态权重"""
    breadth = calc_market_breadth(context)
    trend = calc_market_trend(context)

    log.info(f"市场宽度: {breadth:.2%}, 趋势: {'上升' if trend else '下降'}")

    if breadth > g.breadth_high and trend:
        g.market_state = "bull"
        return 0.8, 0.2
    elif breadth < g.breadth_low or not trend:
        g.market_state = "bear"
        return 0.2, 0.8
    else:
        g.market_state = "neutral"
        return 0.6, 0.4


def select_rfscore7(context, n=15):
    """RFScore7选股"""
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
        query(valuation.code, valuation.pb_ratio, indicator.roa)
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
            valuation.market_cap,
            valuation.circulating_market_cap,
            indicator.inc_net_profit_year_on_year,
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


def risk_control(context):
    """盘中风控: 个股止损"""
    current_data = get_current_data()

    for stock in list(context.portfolio.positions.keys()):
        position = context.portfolio.positions[stock]

        # 计算盈亏
        if stock in g.avg_costs:
            cost = g.avg_costs[stock]
            current_price = current_data[stock].last_price
            pnl_ratio = (current_price / cost) - 1

            # 止损
            if pnl_ratio < -g.stop_loss_ratio:
                order_target(stock, 0)
                log.info(f"止损卖出: {stock}, 亏损: {pnl_ratio:.2%}")


def adjust_position(context):
    """月度调仓"""
    # 动态权重
    rf_weight, div_weight = get_dynamic_weights(context)
    g.rfscore_weight = rf_weight
    g.dividend_weight = div_weight

    g.rfscore_num = int(g.total_stock_num * rf_weight)
    g.dividend_num = g.total_stock_num - g.rfscore_num

    log.info(
        f"市场状态: {g.market_state}, RFScore7: {rf_weight:.0%}, 红利小盘: {div_weight:.0%}"
    )

    # 选股
    g.target_rfscore = select_rfscore7(context, g.rfscore_num)
    g.target_dividend = select_small_dividend(context, g.dividend_num)
    g.target_list = g.target_rfscore + g.target_dividend

    # 卖出
    for stock in context.portfolio.positions:
        if stock not in g.target_list:
            if not get_current_data()[stock].paused:
                order_target(stock, 0)
                log.info(f"卖出: {stock}")
                if stock in g.avg_costs:
                    del g.avg_costs[stock]

    # 买入
    total_value = context.portfolio.total_value

    if g.rfscore_num > 0:
        rfscore_value = total_value * rf_weight / g.rfscore_num
        for stock in g.target_rfscore:
            if stock not in context.portfolio.positions:
                if order_value(stock, rfscore_value):
                    log.info(f"买入RFScore7: {stock}")
                    g.avg_costs[stock] = get_current_data()[stock].last_price

    if g.dividend_num > 0:
        dividend_value = total_value * div_weight / g.dividend_num
        for stock in g.target_dividend:
            if stock not in context.portfolio.positions:
                if order_value(stock, dividend_value):
                    log.info(f"买入红利小盘: {stock}")
                    g.avg_costs[stock] = get_current_data()[stock].last_price


def check_limit_up(context):
    """检查涨停股"""
    current_data = get_current_data()
    for stock in context.portfolio.positions:
        if current_data[stock].last_price < current_data[stock].high_limit:
            if stock in g.hold_list:
                order_target(stock, 0)
                log.info(f"涨停打开卖出: {stock}")


def after_trading_end(context):
    """收盘后更新"""
    g.hold_list = list(context.portfolio.positions.keys())
