#!/usr/bin/env python3
"""弱转强竞价策略 - 简化版（仅使用基础jqdata）"""

from jqdata import *
import datetime as dt


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.target_list = []

    run_daily(get_stock_list, "9:01")
    run_daily(buy, "09:30")
    run_daily(sell, "14:50")


def get_stock_list(context):
    date = context.previous_date
    date_str = date.strftime("%Y-%m-%d")

    try:
        prev_date = get_previous_trade_date(date)
        prev_prev_date = get_previous_trade_date(prev_date)

        initial_list = get_all_securities("stock", date_str).index.tolist()

        # 过滤创业板科创板北交所
        initial_list = [
            s for s in initial_list if s[0] not in ["4", "8", "3"] and s[:2] != "68"
        ]

        # 过滤新股
        new_list = []
        for s in initial_list:
            try:
                info = get_security_info(s)
                days_listed = (date - info.start_date).days
                if days_listed > 50:
                    new_list.append(s)
            except:
                continue
        initial_list = new_list

        # 过滤ST
        st_df = get_extras(
            "is_st", initial_list, start_date=date_str, end_date=date_str, df=True
        )
        if not st_df.empty:
            st_df = st_df.T
            st_df.columns = ["is_st"]
            initial_list = list(st_df[st_df["is_st"] == False].index)

        # 昨日涨停
        prices = get_price(
            initial_list,
            end_date=date_str,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
            skip_paused=True,
        )
        if prices.empty:
            g.target_list = []
            return

        prices = prices.dropna()
        hl_stocks = list(prices[prices["close"] == prices["high_limit"]]["code"])

        # 前两日曾涨停（排除）
        try:
            prev1_prices = get_price(
                initial_list,
                end_date=prev_date.strftime("%Y-%m-%d"),
                frequency="daily",
                fields=["high", "high_limit"],
                count=1,
                panel=False,
                skip_paused=True,
            )
            if not prev1_prices.empty:
                prev1_prices = prev1_prices.dropna()
                hl1 = list(
                    prev1_prices[prev1_prices["high"] == prev1_prices["high_limit"]][
                        "code"
                    ]
                )
            else:
                hl1 = []
        except:
            hl1 = []

        try:
            prev2_prices = get_price(
                initial_list,
                end_date=prev_prev_date.strftime("%Y-%m-%d"),
                frequency="daily",
                fields=["high", "high_limit"],
                count=1,
                panel=False,
                skip_paused=True,
            )
            if not prev2_prices.empty:
                prev2_prices = prev2_prices.dropna()
                hl2 = list(
                    prev2_prices[prev2_prices["high"] == prev2_prices["high_limit"]][
                        "code"
                    ]
                )
            else:
                hl2 = []
        except:
            hl2 = []

        remove_set = set(hl1 + hl2)
        g.target_list = [s for s in hl_stocks if s not in remove_set]

    except Exception as e:
        g.target_list = []


def buy(context):
    qualified_stocks = []
    current_data = get_current_data()

    for s in g.target_list:
        try:
            # 成交额和市值检查
            prev_data = get_price(
                s,
                end_date=context.previous_date,
                frequency="daily",
                fields=["close", "volume", "money"],
                count=1,
                panel=False,
                skip_paused=True,
            )
            if prev_data.empty:
                continue

            prev_close = prev_data["close"].iloc[-1]
            prev_volume = prev_data["volume"].iloc[-1]
            prev_money = prev_data["money"].iloc[-1]

            # 成交额>5亿
            if prev_money < 5e8:
                continue

            # 均价涨幅>7%
            avg_price = prev_money / prev_volume
            avg_increase = avg_price / prev_close * 1.1 - 1
            if avg_increase < 0.07:
                continue

            # 市值>30亿
            val = get_valuation(
                s,
                start_date=context.previous_date,
                end_date=context.previous_date,
                fields=["market_cap"],
            )
            if val.empty or val["market_cap"].iloc[-1] < 30:
                continue

            # 左压突破（简化版）
            try:
                highs = get_price(
                    s,
                    end_date=context.previous_date,
                    frequency="daily",
                    fields=["high"],
                    count=30,
                    panel=False,
                    skip_paused=True,
                )
                if highs.empty or len(highs) < 3:
                    continue

                volumes = get_price(
                    s,
                    end_date=context.previous_date,
                    frequency="daily",
                    fields=["volume"],
                    count=30,
                    panel=False,
                    skip_paused=True,
                )
                if volumes.empty or len(volumes) < 2:
                    continue

                # 简化：昨日量 > 前29日最大量 * 0.9
                vol_arr = volumes["volume"].values
                if vol_arr[-1] <= max(vol_arr[:-1]) * 0.9:
                    continue
            except:
                continue

            if s not in current_data:
                continue

            # 高开幅度检查
            high_limit = current_data[s].high_limit
            day_open = current_data[s].day_open

            # 高开幅度2%~5%（相对于涨停价）
            open_ratio = day_open / (high_limit / 1.1)
            if open_ratio <= 1.02 or open_ratio >= 1.05:
                continue

            qualified_stocks.append(s)

        except Exception as e:
            continue

    if len(qualified_stocks) > 0:
        value = context.portfolio.available_cash / len(qualified_stocks)
        for s in qualified_stocks:
            if s in current_data:
                try:
                    order_value(s, value, MarketOrderStyle(current_data[s].day_open))
                except:
                    continue


def sell(context):
    hold_list = list(context.portfolio.positions)
    current_data = get_current_data()

    for s in hold_list:
        if s in current_data:
            if current_data[s].last_price != current_data[s].high_limit:
                if context.portfolio.positions[s].closeable_amount != 0:
                    try:
                        order_target_value(s, 0)
                    except:
                        continue


def get_previous_trade_date(date):
    """获取上一个交易日"""
    all_days = list(get_all_trade_days())
    date_str = date.strftime("%Y-%m-%d")

    for i, d in enumerate(all_days):
        if d.strftime("%Y-%m-%d") == date_str:
            if i > 0:
                return all_days[i - 1]
            else:
                return date - dt.timedelta(days=1)

    return date - dt.timedelta(days=1)
