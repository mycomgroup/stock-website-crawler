# -*- coding: utf-8 -*-
"""
组合策略：首板低开 + 弱转强竞价
测试三组权重：等权、风险平价、动态权重
"""

from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    # 组合模式: 'equal_weight' | 'risk_parity' | 'dynamic'
    g.portfolio_mode = "equal_weight"

    # 策略权重配置
    g.strategy_weights = {
        "equal_weight": {"first_board": 0.5, "weak_to_strong": 0.5},
        "risk_parity": {"first_board": 0.6, "weak_to_strong": 0.4},
        "dynamic": {"first_board": 0.5, "weak_to_strong": 0.5},
    }

    g.target_list_first_board = []
    g.target_list_weak_to_strong = []
    g.trade_log = []

    run_daily(get_stock_list, "09:01")
    run_daily(buy, "09:30")
    run_daily(sell, "14:50")


def get_stock_list(context):
    date = context.previous_date
    date_str = date.strftime("%Y-%m-%d")
    prev_date = get_shifted_date(date_str, -1, "T")
    prev_date_2 = get_shifted_date(date_str, -2, "T")
    prev_date_3 = get_shifted_date(date_str, -3, "T")

    # 基础股票池
    initial_list = get_all_securities("stock", date_str).index.tolist()
    initial_list = [s for s in initial_list if s[:2] != "68" and s[0] not in ["4", "8"]]
    initial_list = [
        s for s in initial_list if (date - get_security_info(s).start_date).days > 250
    ]

    # ST过滤
    is_st = get_extras(
        "is_st", initial_list, start_date=date_str, end_date=date_str, df=True
    ).T
    initial_list = [s for s in initial_list if not is_st.loc[s].iloc[0]]

    # 昨日涨停股
    df = get_price(
        initial_list,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    hl_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()

    # 首板低开策略信号
    g.target_list_first_board = get_first_board_signals(hl_stocks, date_str, prev_date)

    # 弱转强竞价策略信号
    g.target_list_weak_to_strong = get_weak_to_strong_signals(
        initial_list, date_str, prev_date, prev_date_2, prev_date_3
    )

    log.info(f"首板低开: {len(g.target_list_first_board)} 只")
    log.info(f"弱转强: {len(g.target_list_weak_to_strong)} 只")


def get_first_board_signals(hl_stocks, date_str, prev_date):
    """首板低开：昨日涨停 + 今日假弱高开(0.5%-1.5%)"""
    if not hl_stocks:
        return []

    # 获取今日开盘价
    today_df = get_price(
        hl_stocks,
        end_date=date_str,
        frequency="daily",
        fields=["open", "high_limit"],
        count=1,
        panel=False,
    )
    if today_df.empty:
        return []

    today_df = today_df.dropna()
    today_df["open_ratio"] = today_df["open"] / (today_df["high_limit"] / 1.1)

    # 假弱高开: 0.5%-1.5%
    signals = today_df[
        (today_df["open_ratio"] > 1.005) & (today_df["open_ratio"] < 1.015)
    ]

    # 市值过滤
    if not signals.empty:
        val = get_valuation(
            signals["code"].tolist(),
            end_date=date_str,
            count=1,
            fields=["circulating_market_cap"],
        )
        val = val[
            (val["circulating_market_cap"] >= 50)
            & (val["circulating_market_cap"] <= 150)
        ]
        return val.index.tolist()
    return []


def get_weak_to_strong_signals(
    initial_list, date_str, prev_date, prev_date_2, prev_date_3
):
    """弱转强竞价：昨日涨停 + 高开0-6% + 成交额>5亿 + 流通市值>30亿"""
    # 获取昨日涨停
    df = get_price(
        initial_list,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    if df.empty:
        return []
    df = df.dropna()
    hl_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()

    if not hl_stocks:
        return []

    # 排除前两日曾涨停
    df_2 = get_price(
        initial_list,
        end_date=prev_date_2,
        frequency="daily",
        fields=["high", "high_limit"],
        count=1,
        panel=False,
    )
    prev_hl = (
        df_2[df_2["high"] == df_2["high_limit"]]["code"].tolist()
        if not df_2.empty
        else []
    )

    df_3 = get_price(
        initial_list,
        end_date=prev_date_3,
        frequency="daily",
        fields=["high", "high_limit"],
        count=1,
        panel=False,
    )
    prev_hl2 = (
        df_3[df_3["high"] == df_3["high_limit"]]["code"].tolist()
        if not df_3.empty
        else []
    )

    hl_stocks = [s for s in hl_stocks if s not in set(prev_hl + prev_hl2)]

    if not hl_stocks:
        return []

    # 今日开盘数据
    today_df = get_price(
        hl_stocks,
        end_date=date_str,
        frequency="daily",
        fields=["open", "high_limit", "money"],
        count=1,
        panel=False,
    )
    if today_df.empty:
        return []

    today_df = today_df.dropna()
    today_df["open_ratio"] = today_df["open"] / (today_df["high_limit"] / 1.1)

    # 高开0-6% + 成交额>5亿
    filtered = today_df[
        (today_df["open_ratio"] > 1.0)
        & (today_df["open_ratio"] < 1.06)
        & (today_df["money"] > 5e8)
    ]

    if filtered.empty:
        return []

    # 流通市值>30亿
    val = get_valuation(
        filtered["code"].tolist(),
        end_date=date_str,
        count=1,
        fields=["circulating_market_cap"],
    )
    val = val[val["circulating_market_cap"] > 30]
    return val.index.tolist()


def buy(context):
    weights = g.strategy_weights[g.portfolio_mode]
    current_data = get_current_data()

    # 首板低开买入
    if g.target_list_first_board:
        w = weights["first_board"]
        cash = context.portfolio.available_cash * w
        per_stock = (
            cash / len(g.target_list_first_board) if g.target_list_first_board else 0
        )

        for s in g.target_list_first_board:
            if s in current_data and per_stock > 0:
                order_value(s, per_stock)

    # 弱转强买入
    if g.target_list_weak_to_strong:
        w = weights["weak_to_strong"]
        cash = context.portfolio.available_cash * w
        per_stock = (
            cash / len(g.target_list_weak_to_strong)
            if g.target_list_weak_to_strong
            else 0
        )

        for s in g.target_list_weak_to_strong:
            if s in current_data and per_stock > 0:
                order_value(s, per_stock)


def sell(context):
    hold_list = list(context.portfolio.positions)
    current_data = get_current_data()

    for s in hold_list:
        if s in current_data:
            pos = context.portfolio.positions[s]
            if pos.closeable_amount > 0:
                # 不涨停则卖出
                if current_data[s].last_price < current_data[s].high_limit * 0.99:
                    order_target_value(s, 0)


def get_shifted_date(date, days, days_type="T"):
    d_date = pd.to_datetime(date).date()
    yesterday = d_date + pd.Timedelta(days=-1)
    if days_type == "T":
        all_trade_days = [str(d.date()) for d in list(get_all_trade_days())]
        if str(yesterday) in all_trade_days:
            shifted_date = all_trade_days[
                all_trade_days.index(str(yesterday)) + days + 1
            ]
        else:
            for i in range(100):
                last_trade_date = yesterday - pd.Timedelta(days=i)
                if str(last_trade_date) in all_trade_days:
                    shifted_date = all_trade_days[
                        all_trade_days.index(str(last_trade_date)) + days + 1
                    ]
                    break
        return shifted_date
    else:
        shifted_date = yesterday + pd.Timedelta(days=days + 1)
        return str(shifted_date.date())
