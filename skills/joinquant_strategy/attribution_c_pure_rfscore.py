# 收益归因验证：版本C - 纯RFScore质量策略
# 移除PB低估值过滤，仅保留RFScore=7选股
# 目的：验证RFScore7质量因子是否是核心收益来源

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa",
        "roa_4",
        "net_operate_cash_flow",
        "net_operate_cash_flow_1",
        "net_operate_cash_flow_2",
        "net_operate_cash_flow_3",
        "total_assets",
        "total_assets_1",
        "total_assets_2",
        "total_assets_3",
        "total_assets_4",
        "total_assets_5",
        "total_non_current_liability",
        "total_non_current_liability_1",
        "gross_profit_margin",
        "gross_profit_margin_4",
        "operating_revenue",
        "operating_revenue_4",
    ]

    def calc(self, data):
        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1

        cfo_sum = (
            data["net_operate_cash_flow"]
            + data["net_operate_cash_flow_1"]
            + data["net_operate_cash_flow_2"]
            + data["net_operate_cash_flow_3"]
        )
        ta_ttm = (
            data["total_assets"]
            + data["total_assets_1"]
            + data["total_assets_2"]
            + data["total_assets_3"]
        ) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - roa * 0.01

        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)

        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1

        turnover = (
            data["operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        turnover_1 = (
            data["operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
        delta_turn = turnover / turnover_1 - 1

        indicator_tuple = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicator_tuple).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(sign).sum(axis=1)


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


def select_rfscore7_pure(context, n=20):
    """纯RFScore7选股，不限制PB"""
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

    # 计算RFScore
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=date, end_date=date)
    
    df = factor.basic.copy()
    df["RFScore"] = factor.fscore
    
    # 只选RFScore=7的股票，不限制PB
    df = df[df["RFScore"] == 7].copy()
    
    if df.empty:
        return []
    
    # 按ROA排序
    df = df.sort_values("ROA", ascending=False)
    
    return df.index.tolist()[:n]


def adjust_position(context):
    """月度调仓"""
    g.target_list = select_rfscore7_pure(context, g.stock_num)

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
