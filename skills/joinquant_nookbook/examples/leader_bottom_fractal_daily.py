# 龙头底分型战法 - 日级简化版
# 基于原始策略简化，去掉分钟确认，使用日线信号
# 回测时间：2021-01-01 到 2026-03-31

from jqdata import *
import pandas as pd
import numpy as np

g.target_list = []
g.signals = []


def initialize(context):
    set_benchmark("000300.XSHG")
    set_option("use_real_price", True)
    log.set_level("order", "error")
    set_order_cost(
        OrderCost(
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )

    g.ps = 1
    g.hold_days = 0
    g.max_hold_days = 5

    run_daily(get_stock_list, "9:25")
    run_daily(buy_signal, "09:30")
    run_daily(check_sell, "14:50")
    run_daily(print_position_info, "15:02")


def get_stock_list(context):
    g.target_list = []
    date_now = context.previous_date.strftime("%Y-%m-%d")

    stocks = list(get_all_securities(["stock"], date_now).index)
    stocks = [s for s in stocks if s[0:3] != "300" and s[0:3] != "688"]

    current_data = get_current_data()
    stocks = [
        s for s in stocks if not current_data[s].is_st and not current_data[s].paused
    ]

    stocks = filter_stock_by_days(context, stocks, 250)

    for stock in stocks:
        try:
            signal = check_leader_bottom_fractal(stock, date_now)
            if signal:
                g.target_list.append(stock)
                g.signals.append({"stock": stock, "date": date_now, "type": signal})
        except:
            pass

    print("筛选结果:", g.target_list)


def check_leader_bottom_fractal(stock, date_now):
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

        # 最近40日最高点
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

        # 最近3天形态
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
        t0_high = df_3["high"].iloc[-1]
        t0_high_limit = df_3["high_limit"].iloc[-1]

        t1_close = df_3["close"].iloc[-2]
        t1_open = df_3["open"].iloc[-2]
        t1_high = df_3["high"].iloc[-2]
        t1_low = df_3["low"].iloc[-2]

        t2_close = df_3["close"].iloc[-3]

        ma60 = df["close"].mean()

        # 底分型判断
        if t0_close != t0_high_limit:
            return None

        body_ratio = abs(t1_close - t1_open) / ((t1_close + t1_open) / 2)
        swing_ratio = abs(t1_high - t1_low) / ((t1_high + t1_low) / 2)

        if body_ratio > 0.03 or swing_ratio > 0.10:
            return None

        if t1_close < ma60:
            return None

        if t0_open < t1_close * 1.02:
            return None

        if t0_open < t1_open * 1.01:
            return None

        if t0_close < t1_close * 1.05:
            return None

        return "bottom_fractal"
    except:
        return None


def buy_signal(context):
    hold_list = list(context.portfolio.positions)
    if len(hold_list) >= g.ps:
        return

    current_data = get_current_data()
    cash = context.portfolio.available_cash

    for stock in g.target_list:
        if len(context.portfolio.positions) >= g.ps:
            break

        if cash / current_data[stock].last_price < 100:
            continue

        if current_data[stock].paused:
            continue

        # 日级简化版：开盘即买入（不需要分钟确认）
        if current_data[stock].day_open > current_data[stock].pre_close:
            value = cash / (g.ps - len(context.portfolio.positions))
            order_value(stock, value)
            g.hold_days = 0
            print("买入:", stock)


def check_sell(context):
    hold_list = list(context.portfolio.positions)
    current_data = get_current_data()

    for stock in hold_list:
        if context.portfolio.positions[stock].closeable_amount == 0:
            continue

        price = context.portfolio.positions[stock].price
        cost = context.portfolio.positions[stock].avg_cost

        # 止损5%
        if price < cost * 0.95:
            order_target(stock, 0)
            print("止损卖出:", stock)
            continue

        # 止盈分档
        if price > cost * 1.4:
            order_target(stock, 0)
            print("止盈卖出(40%):", stock)
            continue

        if price > cost * 1.3:
            if price < cost * 1.25:
                order_target(stock, 0)
                print("止盈回撤(30%):", stock)
                continue

        # 不涨停且盈利
        if current_data[stock].last_price != current_data[stock].high_limit:
            if price > cost:
                g.hold_days += 1
                if g.hold_days >= g.max_hold_days:
                    order_target(stock, 0)
                    print("时间止盈:", stock)


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


def print_position_info(context):
    position_percent = (
        100 * context.portfolio.positions_value / context.portfolio.total_value
    )
    record(仓位=round(position_percent, 2))

    for position in list(context.portfolio.positions.values()):
        securities = position.security
        cost = position.avg_cost
        price = position.price
        ret = 100 * (price / cost - 1)
        print("代码:{} 收益率:{}%".format(securities, format(ret, ".2f")))
