#!/usr/bin/env python3
"""对照组C: 宏观+情绪择时策略 - 234板接力"""

from jqdata import *
from jqdata import macro
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
    g.total_position_ratio = 1.0

    g.macro_state = 2
    g.macro_score = 50
    g.last_macro_update = None
    g.sentiment_state = 2
    g.sentiment_score = 50
    g.hl_count = 0
    g.ll_count = 0

    run_daily(update_macro_state, "9:00")
    run_daily(update_sentiment_state, "9:10")
    run_daily(calculate_position_ratio, "9:15")
    run_daily(get_stock_list, "9:20")
    run_daily(buy, "9:35")
    run_daily(sell, "14:50")
    run_daily(record_stats, "15:02")


def update_macro_state(context):
    current_date = context.current_dt.strftime("%Y-%m")
    if g.last_macro_update == current_date:
        return
    g.last_macro_update = current_date

    try:
        pmi_df = macro.run_query(
            query(
                macro.MAC_MANUFACTURING_PMI.stat_month,
                macro.MAC_MANUFACTURING_PMI.pmi,
                macro.MAC_MANUFACTURING_PMI.produce_idx,
                macro.MAC_MANUFACTURING_PMI.new_orders_idx,
                macro.MAC_MANUFACTURING_PMI.raw_material_idx,
                macro.MAC_MANUFACTURING_PMI.finished_produce_idx,
            )
            .filter(
                macro.MAC_MANUFACTURING_PMI.stat_month
                >= calc_n_months_ago(current_date, 15),
                macro.MAC_MANUFACTURING_PMI.stat_month <= current_date,
            )
            .order_by(macro.MAC_MANUFACTURING_PMI.stat_month.asc())
        )

        if len(pmi_df) >= 3:
            latest_pmi = pmi_df["pmi"].iloc[-1]
            recent_3 = pmi_df["pmi"].tail(3).values
            slope = np.polyfit([0, 1, 2], recent_3, 1)[0] if len(recent_3) == 3 else 0
            new_orders_diff = (
                pmi_df["new_orders_idx"].iloc[-1] - pmi_df["produce_idx"].iloc[-1]
            )
            inventory_sig = (
                pmi_df["raw_material_idx"].iloc[-1]
                - pmi_df["finished_produce_idx"].iloc[-1]
            )

            score = 50
            score += 15 if latest_pmi >= 50 else -15
            score += 10 * max(-1, min(1, slope / 0.5))
            score += 5 * max(-1, min(1, new_orders_diff / 5))
            score += 5 * max(-1, min(1, -inventory_sig / 5))
            score = max(0, min(100, score))

            g.macro_score = score
            if score >= 70:
                g.macro_state = 3
            elif score >= 55:
                g.macro_state = 2
            elif score >= 40:
                g.macro_state = 1
            else:
                g.macro_state = 0

            record(宏观得分=g.macro_score, 宏观状态=g.macro_state)
    except:
        pass


def update_sentiment_state(context):
    current_date = context.previous_date
    try:
        all_stocks = get_all_securities("stock", date=current_date).index.tolist()
        all_stocks = [
            s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
        ]

        sample_stocks = all_stocks[:500]
        df = get_price(
            sample_stocks,
            end_date=current_date,
            count=1,
            fields=["close", "high_limit", "low_limit"],
            panel=False,
        )
        df = df.dropna()

        hl_count = len(df[df["close"] == df["high_limit"]])
        ll_count = len(df[df["close"] == df["low_limit"]])
        g.hl_count = hl_count
        g.ll_count = ll_count

        score = 50
        if hl_count > 80:
            score += 20
        elif hl_count > 50:
            score += 10
        elif hl_count > 30:
            score += 5
        elif hl_count < 15:
            score -= 15
        elif hl_count < 25:
            score -= 5

        ratio = hl_count / max(ll_count, 1)
        if ratio > 5:
            score += 15
        elif ratio > 2:
            score += 5
        elif ratio < 0.5:
            score -= 15
        elif ratio < 1:
            score -= 5

        score = max(0, min(100, score))
        g.sentiment_score = score

        if score >= 75:
            g.sentiment_state = 4
        elif score >= 60:
            g.sentiment_state = 3
        elif score >= 45:
            g.sentiment_state = 2
        elif score >= 30:
            g.sentiment_state = 1
        else:
            g.sentiment_state = 0

        record(
            情绪得分=g.sentiment_score,
            情绪状态=g.sentiment_state,
            涨停数=g.hl_count,
            跌停数=g.ll_count,
        )
    except:
        pass


def calculate_position_ratio(context):
    if g.macro_state == 3:
        base_ratio = 0.8
    elif g.macro_state == 2:
        base_ratio = 0.6
    elif g.macro_state == 1:
        base_ratio = 0.3
    else:
        base_ratio = 0.0

    if g.sentiment_state >= 3:
        sent_adj = 1.0
    elif g.sentiment_state == 2:
        sent_adj = 0.8
    elif g.sentiment_state == 1:
        sent_adj = 0.5
    else:
        sent_adj = 0.2

    g.total_position_ratio = min(1.0, base_ratio * sent_adj)
    record(目标仓位=g.total_position_ratio * 100)


def get_continue_board_stocks(context):
    prev_date = context.previous_date
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
        count=5,
        fields=["close", "high_limit"],
        panel=False,
    )
    df = df.dropna()

    latest = df.groupby("code").last()
    hl_stocks = latest[latest["close"] == latest["high_limit"]].index.tolist()

    board_counts = {}
    for stock in hl_stocks:
        stock_df = df[df["code"] == stock].sort_values("time")
        if len(stock_df) < 2:
            continue
        consecutive = 1
        closes = stock_df["close"].values
        limits = stock_df["high_limit"].values
        for i in range(len(closes) - 2, -1, -1):
            if closes[i] == limits[i]:
                consecutive += 1
            else:
                break
        if consecutive >= 2:
            board_counts[stock] = consecutive

    return board_counts


def get_stock_list(context):
    g.target_stocks = []
    if g.total_position_ratio <= 0:
        return
    try:
        board_counts = get_continue_board_stocks(context)
        candidates = {s: c for s, c in board_counts.items() if 2 <= c <= 4}

        if len(candidates) > 0:
            prev_date = context.previous_date
            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.code.in_(list(candidates.keys()))
            )
            val_df = get_fundamentals(q, date=prev_date)
            if val_df is not None and len(val_df) > 0:
                val_df = val_df[val_df["circulating_market_cap"] < 80]
                val_df["board_count"] = val_df["code"].map(candidates)
                val_df = val_df.sort_values("board_count", ascending=False)
                g.target_stocks = val_df["code"].tolist()[: g.max_positions]
    except:
        pass


def buy(context):
    if g.total_position_ratio <= 0 or len(g.target_stocks) == 0:
        return
    current_data = get_current_data()
    total_value = context.portfolio.total_value
    target_per_stock = total_value * g.total_position_ratio * g.position_value_ratio

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
            if ret > 3 or ret < -5:
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


def calc_n_months_ago(date_str, n):
    year = int(date_str[:4])
    month = int(date_str[5:7])
    month -= n
    while month <= 0:
        year -= 1
        month += 12
    return f"{year:04d}-{month:02d}"
