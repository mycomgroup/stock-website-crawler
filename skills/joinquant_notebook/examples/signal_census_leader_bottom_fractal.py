# 龙头底分型信号普查
# 时间范围：2021-01-01 到 2026-03-31
# 目标：统计总信号数、2024-01-01后信号数、严格分钟版 vs 日线简化版

from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    set_benchmark("000300.XSHG")
    set_option("use_real_price", True)
    log.set_level("order", "error")

    g.strict_signals = []
    g.simplified_signals = []
    g.strict_signals_2024 = []
    g.simplified_signals_2024 = []

    run_daily(check_signals, "09:30")
    run_daily(print_summary, "15:02")


def check_signals(context):
    date_now = context.current_dt.strftime("%Y-%m-%d")

    if date_now < "2021-01-01" or date_now > "2026-03-31":
        return

    stocks = list(get_all_securities(["stock"], date_now).index)
    stocks = [s for s in stocks if s[0:3] != "300" and s[0:3] != "688"]

    current_data = get_current_data()
    stocks = [
        s for s in stocks if not current_data[s].is_st and not current_data[s].paused
    ]

    stocks = filter_stock_by_days(context, stocks, 250)

    for stock in stocks:
        try:
            strict_signal = check_strict_version(stock, date_now)
            simplified_signal = check_simplified_version(stock, date_now)

            if strict_signal:
                g.strict_signals.append({"stock": stock, "date": date_now})
                if date_now >= "2024-01-01":
                    g.strict_signals_2024.append({"stock": stock, "date": date_now})

            if simplified_signal:
                g.simplified_signals.append({"stock": stock, "date": date_now})
                if date_now >= "2024-01-01":
                    g.simplified_signals_2024.append({"stock": stock, "date": date_now})
        except:
            pass


def check_strict_version(stock, date_now):
    # 严格分钟版：主升浪 + 回调 + 底分型 + 分钟确认
    try:
        df = get_price(
            stock,
            count=60,
            end_date=date_now,
            frequency="daily",
            fields=["open", "high", "close", "low", "high_limit", "pre_close", "money"],
        )
        if len(df) < 60:
            return None

        df_500 = get_price(
            stock,
            count=500,
            end_date=date_now,
            frequency="daily",
            fields=["close", "high"],
        )
        if len(df_500) < 500:
            return None

        high_500 = df_500["high"].max()
        high_40_idx = df["high"].idxmax()
        high_40 = df["high"].max()

        if high_40 < high_500 * 0.95:
            return None

        df_before_high = get_price(
            stock,
            count=12,
            end_date=high_40_idx,
            frequency="daily",
            fields=["open", "close", "low", "high_limit"],
        )
        if len(df_before_high) < 12:
            return None

        max_close_before = df_before_high["close"].max()
        min_close_before = df_before_high["close"].min()
        rate_before = (max_close_before - min_close_before) / min_close_before

        if rate_before < 0.55:
            return None

        limit_count_8 = (
            df_before_high["high_limit"] == df_before_high["high_limit"]
        ).sum()

        df_80 = get_price(
            stock,
            count=80,
            end_date=high_40_idx,
            frequency="daily",
            fields=["close", "low"],
        )
        if len(df_80) < 80:
            return None

        max_80 = df_80["close"].max()
        min_80 = df_80["low"].min()
        rate_80 = (max_80 - min_80) / min_80

        if rate_80 > 3.8:
            return None

        df_3 = get_price(
            stock,
            count=3,
            end_date=date_now,
            frequency="daily",
            fields=["open", "close", "low", "high", "high_limit"],
        )
        if len(df_3) < 3:
            return None

        t0_close = df_3["close"].iloc[-1]
        t0_open = df_3["open"].iloc[-1]
        t0_high_limit = df_3["high_limit"].iloc[-1]

        t1_close = df_3["close"].iloc[-2]
        t1_open = df_3["open"].iloc[-2]
        t1_high = df_3["high"].iloc[-2]
        t1_low = df_3["low"].iloc[-2]

        ma60 = df["close"].mean()

        if t0_close != t0_high_limit:
            return None

        body_ratio = abs(t1_close - t1_open) / ((t1_close + t1_open) / 2)
        swing_ratio = abs(t1_high - t1_low) / ((t1_high + t1_low) / 2)

        if body_ratio > 0.025 or swing_ratio > 0.08:
            return None

        if t1_close < ma60:
            return None

        if t0_open < t1_close * 1.02:
            return None

        if t0_open < t1_open * 1.02:
            return None

        if t0_close < t1_close * 1.07:
            return None

        return "strict"
    except:
        return None


def check_simplified_version(stock, date_now):
    # 日线简化版：主升浪背景 + 底分型 + 高开确认
    try:
        df = get_price(
            stock,
            count=40,
            end_date=date_now,
            frequency="daily",
            fields=["open", "high", "close", "low", "high_limit", "pre_close"],
        )
        if len(df) < 40:
            return None

        high_40 = df["high"].max()
        high_40_idx = df["high"].idxmax()

        df_before = get_price(
            stock,
            count=12,
            end_date=high_40_idx,
            frequency="daily",
            fields=["close", "low", "high_limit"],
        )
        if len(df_before) < 12:
            return None

        max_before = df_before["close"].max()
        min_before = df_before["close"].min()
        rate_before = (max_before - min_before) / min_before

        if rate_before < 0.50:
            return None

        limit_count = (df_before["high_limit"] == df_before["high_limit"]).sum()
        if limit_count < 2:
            return None

        df_3 = get_price(
            stock,
            count=3,
            end_date=date_now,
            frequency="daily",
            fields=["open", "close", "high_limit"],
        )
        if len(df_3) < 3:
            return None

        t0_close = df_3["close"].iloc[-1]
        t0_open = df_3["open"].iloc[-1]
        t0_high_limit = df_3["high_limit"].iloc[-1]

        t1_close = df_3["close"].iloc[-2]
        t1_open = df_3["open"].iloc[-2]

        if t0_close != t0_high_limit:
            return None

        body_ratio = abs(t1_close - t1_open) / ((t1_close + t1_open) / 2)
        if body_ratio > 0.03:
            return None

        if t0_open < t1_close * 1.015:
            return None

        return "simplified"
    except:
        return None


def filter_stock_by_days(context, stock_list, days):
    tmpList = []
    for stock in stock_list:
        try:
            days_public = (
                context.current_dt.date() - get_security_info(stock).start_date
            ).days
            if days_public > days:
                tmpList.append(stock)
        except:
            pass
    return tmpList


def print_summary(context):
    print("===== 信号普查结果 =====")
    print("严格分钟版总信号数:", len(g.strict_signals))
    print("严格分钟版2024年后信号数:", len(g.strict_signals_2024))
    print("日线简化版总信号数:", len(g.simplified_signals))
    print("日线简化版2024年后信号数:", len(g.simplified_signals_2024))

    if len(g.strict_signals) > 0:
        print("严格分钟版信号详情:")
        for signal in g.strict_signals[-10:]:
            print(signal)

    if len(g.simplified_signals) > 0:
        print("日线简化版信号详情:")
        for signal in g.simplified_signals[-10:]:
            print(signal)
