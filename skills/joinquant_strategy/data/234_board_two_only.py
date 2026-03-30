# 234板策略 - 仅二板版本
# 分板位测试：二板+情绪开关+非涨停开盘

from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.board_level = "two"  # 仅二板
    g.max_turnover_ratio = 15  # 换手率上限
    g.max_lb_1d = 1.5  # 缩量条件

    g.min_max_board = 3  # 最高连板数阈值
    g.min_zt_count = 30  # 涨停家数阈值
    g.min_promote_rate = 20  # 晋级率阈值

    g.ps = 1  # 分仓数量
    g.target_list = []

    run_daily(get_stock_list, "09:25")
    run_daily(check_sentiment, "09:26")
    run_daily(sell_early, "09:30")
    run_daily(buy_stocks, "09:31")
    run_daily(sell_late, "14:50")


def check_sentiment(context):
    date = context.previous_date.strftime("%Y-%m-%d")

    max_lianban = calc_max_lianban(date)
    zt_count = len(get_zt_stocks(date))
    promote_rate = calc_promote_rate(date)

    g.sentiment_ok = False
    g.position_ratio = 0

    if (
        max_lianban >= g.min_max_board
        and zt_count >= g.min_zt_count
        and promote_rate >= g.min_promote_rate
    ):
        g.sentiment_ok = True
        if max_lianban >= 5 and zt_count >= 80:
            g.position_ratio = 1.0
        elif max_lianban >= 4 and zt_count >= 50:
            g.position_ratio = 0.75
        else:
            g.position_ratio = 0.5

    log.info(
        f"情绪: 最高连板={max_lianban}, 涨停数={zt_count}, 晋级率={promote_rate}, 开关={g.sentiment_ok}"
    )


def get_stock_list(context):
    if not g.sentiment_ok:
        g.target_list = []
        return

    date = context.previous_date.strftime("%Y-%m-%d")
    initial_list = prepare_stock_list(date)

    prev_date = get_shifted_date(date, -1)
    prev2_date = get_shifted_date(date, -2)

    hl_1d = filter_yzb(get_hl_stock(initial_list, date), date)
    hl_2d = get_hl_stock(initial_list, prev_date)
    hl_3d = get_hl_stock(initial_list, prev2_date)

    stock_list = list(set(hl_1d) & set(hl_2d) - set(hl_3d))

    stock_list = [
        s for s in stock_list if get_turnover_ratio(s, date) < g.max_turnover_ratio
    ]

    stock_list = filter_by_volume_ratio(stock_list, date)

    stock_list = sort_by_free_cap(context, stock_list)

    g.target_list = stock_list[: g.ps]
    log.info(f"选股: {g.target_list}")


def buy_stocks(context):
    if not g.sentiment_ok or len(g.target_list) == 0:
        return

    current_data = get_current_data()

    for s in g.target_list:
        if current_data[s].last_price == current_data[s].high_limit:
            log.info(f"{s} 涨停开盘，放弃买入")
            continue

        available_cash = context.portfolio.available_cash * g.position_ratio
        value = min(available_cash / g.ps, 5000000)

        if value > 0 and context.portfolio.available_cash > value:
            order_value(s, value)
            log.info(f"买入 {s}")


def sell_early(context):
    current_data = get_current_data()

    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount == 0:
            continue

        open_ratio = current_data[s].day_open / pos.avg_cost
        if open_ratio < 0.96:
            order_target_value(s, 0)
            log.info(f"{s} 低开止损")


def sell_late(context):
    current_data = get_current_data()

    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount == 0:
            continue

        if current_data[s].last_price < current_data[s].high_limit:
            hold_days = (context.current_dt - pos.init_time).days
            if hold_days >= 2 or current_data[s].last_price > pos.avg_cost:
                order_target_value(s, 0)
                log.info(f"{s} 尾盘卖出")


def prepare_stock_list(date):
    initial_list = get_all_securities("stock", date).index.tolist()
    initial_list = filter_cykcbj_stock(initial_list)
    initial_list = filter_new_stock(initial_list, date)
    initial_list = filter_st_stock(initial_list, date)
    initial_list = filter_paused_stock(initial_list, date)
    return initial_list


def get_hl_stock(initial_list, date):
    df = get_price(
        initial_list,
        end_date=date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    return list(df.code)


def filter_yzb(stock_list, date):
    result = []
    for stock in stock_list:
        df = get_price(
            stock, end_date=date, frequency="daily", fields=["low", "high"], count=1
        )
        if df["low"].iloc[0] != df["high"].iloc[0]:
            result.append(stock)
    return result


def get_turnover_ratio(stock, date):
    hsl = HSL([stock], date)
    if stock in hsl[0]:
        return hsl[0][stock]
    return 0


def filter_by_volume_ratio(stock_list, date):
    result = []
    for s in stock_list:
        df = get_price(s, end_date=date, frequency="daily", fields=["volume"], count=2)
        if len(df) >= 2:
            ratio = df["volume"].iloc[-1] / df["volume"].iloc[-2]
            if ratio < g.max_lb_1d:
                result.append(s)
    return result


def sort_by_free_cap(context, stock_list):
    if len(stock_list) < 1:
        return []

    caps = []
    for s in stock_list:
        free_cap = get_free_market_cap(s, context.previous_date)
        caps.append((s, free_cap))

    caps.sort(key=lambda x: x[1])
    return [s for s, _ in caps]


def get_free_market_cap(stock, date):
    q = query(
        valuation.code, valuation.market_cap, valuation.circulating_market_cap
    ).filter(valuation.code == stock)
    df = get_fundamentals(q, date=date)
    if len(df) > 0:
        circulating_cap = df["circulating_market_cap"].iloc[0]
        return circulating_cap
    return 0


def get_shifted_date(date, days):
    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date in all_days:
        idx = all_days.index(date)
        new_idx = idx + days
        if new_idx >= 0 and new_idx < len(all_days):
            return all_days[new_idx]
    return date


def calc_max_lianban(date):
    zt_list = get_zt_stocks(date)
    max_count = 0
    for stock in zt_list[:50]:
        count = 0
        df = get_price(
            stock, end_date=date, count=10, fields=["close", "high_limit"], panel=False
        )
        for i in range(len(df) - 1, -1, -1):
            if df.iloc[i]["close"] == df.iloc[i]["high_limit"]:
                count += 1
            else:
                break
        max_count = max(max_count, count)
    return max_count


def get_zt_stocks(date):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df = df.dropna()
    zt_df = df[df["close"] == df["high_limit"]]
    return list(zt_df["code"])


def calc_promote_rate(date):
    prev_date = get_shifted_date(date, -1)
    prev_zt = get_zt_stocks(prev_date)
    today_zt = get_zt_stocks(date)
    promoted = len(set(prev_zt) & set(today_zt))
    if len(prev_zt) > 0:
        return promoted / len(prev_zt) * 100
    return 0


def filter_cykcbj_stock(initial_list):
    return [
        stock
        for stock in initial_list
        if stock[0] != "4" and stock[0] != "8" and stock[:2] != "68" and stock[0] != "3"
    ]


def filter_new_stock(initial_list, date, days=250):
    from datetime import timedelta

    return [
        stock
        for stock in initial_list
        if date - get_security_info(stock).start_date > timedelta(days=days)
    ]


def filter_st_stock(initial_list, date):
    str_date = date.strftime("%Y-%m-%d")
    df = get_extras(
        "is_st", initial_list, start_date=str_date, end_date=str_date, df=True
    )
    df = df.T
    df.columns = ["is_st"]
    df = df[df["is_st"] == False]
    return list(df.index)


def filter_paused_stock(initial_list, date):
    df = get_price(
        initial_list,
        end_date=date,
        frequency="daily",
        fields=["paused"],
        count=1,
        panel=False,
        fill_paused=True,
    )
    df = df[df["paused"] == 0]
    return list(df.code)
