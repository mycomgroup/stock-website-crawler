# 风险控制研究 - 组1：无风控强化版本
# 基础：弱转强竞价战法（参考21号策略）
# 特点：仅保留原始止损规则，不增加任何额外风控

from jqdata import *
from jqfactor import *
from jqlib.technical_analysis import *
import datetime as dt
import pandas as pd


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")

    # 基础参数
    g.max_stocks = 3  # 最多持股数

    run_daily(get_stock_list, "9:01")
    run_daily(buy, "09:30")
    run_daily(sell_basic, "14:50")


# 选股逻辑（与原策略一致）
def get_stock_list(context):
    date = context.previous_date
    date = transform_date(date, "str")
    date_1 = get_shifted_date(date, -1, "T")
    date_2 = get_shifted_date(date, -2, "T")

    initial_list = prepare_stock_list(date)
    hl_list = get_hl_stock(initial_list, date)
    hl1_list = get_ever_hl_stock(initial_list, date_1)
    hl2_list = get_ever_hl_stock(initial_list, date_2)

    elements_to_remove = set(hl1_list + hl2_list)
    hl_list = [stock for stock in hl_list if stock not in elements_to_remove]

    g.target_list = hl_list


# 买入逻辑
def buy(context):
    qualified_stocks = []
    current_data = get_current_data()

    for s in g.target_list:
        prev_day_data = attribute_history(
            s, 1, "1d", fields=["close", "volume", "money"], skip_paused=True
        )
        avg_price_increase_value = (
            prev_day_data["money"][0]
            / prev_day_data["volume"][0]
            / prev_day_data["close"][0]
            * 1.1
            - 1
        )

        if avg_price_increase_value < 0.07 or prev_day_data["money"][0] < 7e8:
            continue

        turnover_ratio_data = get_valuation(
            s,
            start_date=context.previous_date,
            end_date=context.previous_date,
            fields=["turnover_ratio", "market_cap"],
        )
        if turnover_ratio_data.empty or turnover_ratio_data["market_cap"][0] < 70:
            continue

        zyts = calculate_zyts(s, context)
        volume_data = attribute_history(
            s, zyts, "1d", fields=["volume"], skip_paused=True
        )
        if (
            len(volume_data) < 2
            or volume_data["volume"][-1] <= max(volume_data["volume"][:-1]) * 0.9
        ):
            continue

        auction_data = get_call_auction(
            s,
            start_date=context.current_dt,
            end_date=context.current_dt,
            fields=["volume", "current"],
        )
        if (
            auction_data.empty
            or auction_data["volume"][0] / volume_data["volume"][-1] < 0.03
        ):
            continue

        current_ratio = auction_data["current"][0] / (current_data[s].high_limit / 1.1)
        if current_ratio <= 1 or current_ratio >= 1.06:
            continue

        qualified_stocks.append(s)

    # 无风控版本：不限制买入数量，不检查市场状态
    if len(qualified_stocks) != 0:
        available_slots = g.max_stocks - len(context.portfolio.positions)
        if available_slots > 0:
            value = context.portfolio.available_cash / min(
                len(qualified_stocks), available_slots
            )
            for s in qualified_stocks[:available_slots]:
                if context.portfolio.available_cash / current_data[s].last_price > 100:
                    order_value(s, value, MarketOrderStyle(current_data[s].day_open))


# 基础卖出（仅保留原始规则）
def sell_basic(context):
    hold_list = list(context.portfolio.positions)
    current_data = get_current_data()

    for s in hold_list:
        if not (current_data[s].last_price == current_data[s].high_limit):
            if context.portfolio.positions[s].closeable_amount != 0:
                order_target_value(s, 0)


# 辅助函数（与原策略一致）
def transform_date(date, date_type):
    if type(date) == str:
        str_date = date
        dt_date = dt.datetime.strptime(date, "%Y-%m-%d")
        d_date = dt_date.date()
    elif type(date) == dt.datetime:
        str_date = date.strftime("%Y-%m-%d")
        dt_date = date
        d_date = dt_date.date()
    elif type(date) == dt.date:
        str_date = date.strftime("%Y-%m-%d")
        dt_date = dt.datetime.strptime(str_date, "%Y-%m-%d")
        d_date = date
    dct = {"str": str_date, "dt": dt_date, "d": d_date}
    return dct[date_type]


def get_shifted_date(date, days, days_type="T"):
    d_date = transform_date(date, "d")
    yesterday = d_date + dt.timedelta(-1)
    if days_type == "N":
        shifted_date = yesterday + dt.timedelta(days + 1)
    if days_type == "T":
        all_trade_days = [i.strftime("%Y-%m-%d") for i in list(get_all_trade_days())]
        if str(yesterday) in all_trade_days:
            shifted_date = all_trade_days[
                all_trade_days.index(str(yesterday)) + days + 1
            ]
        else:
            for i in range(100):
                last_trade_date = yesterday - dt.timedelta(i)
                if str(last_trade_date) in all_trade_days:
                    shifted_date = all_trade_days[
                        all_trade_days.index(str(last_trade_date)) + days + 1
                    ]
                    break
    return str(shifted_date)


def filter_new_stock(initial_list, date, days=50):
    d_date = transform_date(date, "d")
    return [
        stock
        for stock in initial_list
        if d_date - get_security_info(stock).start_date > dt.timedelta(days=days)
    ]


def filter_st_stock(initial_list, date):
    str_date = transform_date(date, "str")
    if get_shifted_date(str_date, 0, "N") != get_shifted_date(str_date, 0, "T"):
        str_date = get_shifted_date(str_date, -1, "T")
    df = get_extras(
        "is_st", initial_list, start_date=str_date, end_date=str_date, df=True
    )
    df = df.T
    df.columns = ["is_st"]
    df = df[df["is_st"] == False]
    return list(df.index)


def filter_kcbj_stock(initial_list):
    return [
        stock
        for stock in initial_list
        if stock[0] != "4" and stock[0] != "8" and stock[0] != "3" and stock[:2] != "68"
    ]


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


def prepare_stock_list(date):
    initial_list = get_all_securities("stock", date).index.tolist()
    initial_list = filter_kcbj_stock(initial_list)
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


def get_ever_hl_stock(initial_list, date):
    df = get_price(
        initial_list,
        end_date=date,
        frequency="daily",
        fields=["high", "high_limit"],
        count=1,
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df = df.dropna()
    df = df[df["high"] == df["high_limit"]]
    return list(df.code)


def calculate_zyts(s, context):
    high_prices = attribute_history(s, 101, "1d", fields=["high"], skip_paused=True)[
        "high"
    ]
    prev_high = high_prices.iloc[-1]
    zyts_0 = next(
        (i - 1 for i, high in enumerate(high_prices[-3::-1], 2) if high >= prev_high),
        100,
    )
    return zyts_0 + 5
