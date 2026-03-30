#!/usr/bin/env python3
"""对照组A: 无择时基线策略 - 首板低开"""

from jqdata import *
import pandas as pd
import numpy as np
import datetime as dt


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")
    set_benchmark("000300.XSHG")
    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    g.max_positions = 5
    g.position_value_ratio = 0.2
    g.target_stocks = []
    g.total_position_ratio = 1.0  # 全仓, 无择时

    run_daily(get_stock_list, "9:20")
    run_daily(buy, "9:35")
    run_daily(sell, "14:50")
    run_daily(record_stats, "15:02")


def get_stock_list(context):
    g.target_stocks = []
    prev_date = context.previous_date
    try:
        all_stocks = get_all_securities("stock", date=prev_date).index.tolist()
        all_stocks = [
            s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
        ]

        st_df = get_extras(
            "is_st", all_stocks, start_date=prev_date, end_date=prev_date, df=True
        )
        if st_df is not None and len(st_df) > 0:
            st_df = st_df.T
            all_stocks = st_df[st_df.iloc[:, 0] == False].index.tolist()

        paused_df = get_price(
            all_stocks,
            end_date=prev_date,
            count=1,
            fields=["paused"],
            panel=False,
            fill_paused=True,
        )
        if paused_df is not None and len(paused_df) > 0:
            all_stocks = paused_df[paused_df["paused"] == 0]["code"].tolist()

        df = get_price(
            all_stocks,
            end_date=prev_date,
            count=2,
            fields=["close", "high_limit", "money"],
            panel=False,
        )
        df = df.dropna()
        hl_today = df[df["close"] == df["high_limit"]]["code"].unique()

        if len(hl_today) > 0:
            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.code.in_(list(hl_today[:100]))
            )
            val_df = get_fundamentals(q, date=prev_date)
            if val_df is not None and len(val_df) > 0:
                val_df = val_df[val_df["circulating_market_cap"] < 100].sort_values(
                    "circulating_market_cap"
                )
                g.target_stocks = val_df["code"].tolist()[: g.max_positions]
    except:
        pass


def buy(context):
    if len(g.target_stocks) == 0:
        return
    current_data = get_current_data()
    total_value = context.portfolio.total_value
    target_per_stock = total_value * g.position_value_ratio
    for stock in g.target_stocks:
        if stock in context.portfolio.positions:
            continue
        if context.portfolio.available_cash < target_per_stock * 0.5:
            break
        try:
            price = current_data[stock].last_price
            if price > 0:
                order_value(
                    stock, min(target_per_stock, context.portfolio.available_cash)
                )
        except:
            continue


def sell(context):
    hold_list = list(context.portfolio.positions)
    current_data = get_current_data()
    for stock in hold_list:
        try:
            position = context.portfolio.positions[stock]
            if position.closeable_amount == 0:
                continue
            current_price = current_data[stock].last_price
            high_limit = current_data[stock].high_limit
            if current_price == high_limit:
                continue
            cost = position.avg_cost
            ret = (current_price / cost - 1) * 100
            if ret > 0:
                order_target_value(stock, 0)
        except:
            continue


def record_stats(context):
    position_pct = (
        100 * context.portfolio.positions_value / max(context.portfolio.total_value, 1)
    )
    ret_pct = 100 * (
        context.portfolio.total_value / context.portfolio.starting_cash - 1
    )
    record(仓位=position_pct, 累计收益=ret_pct)
