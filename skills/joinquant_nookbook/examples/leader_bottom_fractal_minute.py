# 龙头底分型战法 - 分钟级严格版
# 基于原始策略02进行滚动验证研究
# 回测时间：2021-01-01 到 2026-03-31

from jqdata import *
import pandas as pd
import numpy as np

help_stock = []


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

    run_daily(before_market_open, time="before_open", reference_security="000300.XSHG")
    run_daily(market_open, time="every_bar", reference_security="000300.XSHG")
    run_daily(after_market_close, time="after_close", reference_security="000300.XSHG")


def market_open(context):
    time_buy = context.current_dt.strftime("%H:%M:%S")
    date_now = (context.current_dt + timedelta(days=-1)).strftime("%Y-%m-%d")
    ten_day = datetime.datetime.strptime("09:35:00", "%H:%M:%S").strftime("%H:%M:%S")
    cash = context.portfolio.available_cash

    if len(help_stock) > 0:
        for stock in help_stock:
            if cash > 5000:
                day_open_price = get_current_data()[stock].day_open
                current_price = get_current_data()[stock].last_price
                pre_date = (context.current_dt + timedelta(days=-1)).strftime(
                    "%Y-%m-%d"
                )
                df_panel = get_price(
                    stock,
                    count=1,
                    end_date=pre_date,
                    frequency="daily",
                    fields=["open", "close", "high_limit", "money", "low"],
                )
                pre_close_price = df_panel["close"].values[0]

                # 确认买入条件
                if (
                    current_price > day_open_price * 1.02
                    and current_price > pre_close_price
                    and day_open_price < pre_close_price * 1.05
                    and day_open_price > pre_close_price * 0.99
                ):
                    print("1." + stock + "买入金额" + str(cash))
                    order_value(stock, cash)
                    help_stock.remove(stock)
                elif (
                    day_open_price > pre_close_price * 1.05
                    and current_price > pre_close_price * 1.03
                    and time_buy > ten_day
                ):
                    print("2." + stock + "买入金额" + str(cash))
                    order_value(stock, cash)
                    help_stock.remove(stock)

    # 卖出逻辑
    time_sell = context.current_dt.strftime("%H:%M:%S")
    cday = datetime.datetime.strptime("14:40:00", "%H:%M:%S").strftime("%H:%M:%S")
    stock_owner = context.portfolio.positions

    if time_sell > cday:
        if len(stock_owner) > 0:
            for stock_two in stock_owner:
                if context.portfolio.positions[stock_two].closeable_amount > 0:
                    current_price = context.portfolio.positions[stock_two].price
                    cost = context.portfolio.positions[stock_two].avg_cost

                    # 止损：亏损5%
                    if current_price < cost * 0.95:
                        print("止损卖出：亏5个点")
                        order_target(stock_two, 0)
    else:
        for stock_two in stock_owner:
            if context.portfolio.positions[stock_two].closeable_amount > 0:
                current_price = context.portfolio.positions[stock_two].price
                cost = context.portfolio.positions[stock_two].avg_cost

                # 止损条件
                if current_price < cost * 0.95:
                    print("止损卖出：亏5个点")
                    order_target(stock_two, 0)
                # 止盈：盈利40%后跌破MA5
                elif current_price > cost * 1.4:
                    close_data = attribute_history(stock_two, 5, "1d", ["close"])
                    MA5 = close_data["close"].mean()
                    if current_price < MA5:
                        print("止盈卖出：盈利40%后跌破MA5")
                        order_target(stock_two, 0)

    if time_sell > cday and len(help_stock) > 0:
        instead_stock = help_stock[:]
        for stock_remove in instead_stock:
            help_stock.remove(stock_remove)


def before_market_open(context):
    date_now = (context.current_dt + timedelta(days=-1)).strftime("%Y-%m-%d")
    yesterday = (context.current_dt + timedelta(days=-31)).strftime("%Y-%m-%d")
    trade_date = get_trade_days(start_date=yesterday, end_date=date_now, count=None)
    yes_date_one = trade_date[trade_date.size - 1]

    stocks = list(get_all_securities(["stock"]).index)
    # 先筛选昨日涨停
    pick_high_list = pick_high_limit(stocks, yes_date_one)
    codelist = filter_st(pick_high_list)
    filter_paused_list = filter_paused_stock(codelist)
    templist = filter_stock_by_days(context, filter_paused_list, 1080)

    for stock in templist:
        high_continous(stock, trade_date, date_now, context)

    print("------今天要扫描的股票------")
    print(help_stock)


def high_continous(stock, trade_date, date_now, context):
    try:
        df_panel = get_price(
            stock,
            count=40,
            end_date=date_now,
            frequency="daily",
            fields=["open", "high", "close", "low", "high_limit", "money"],
        )
        if len(df_panel) < 40:
            return

        sum_plus_num_40 = (
            df_panel.loc[:, "open"] > df_panel.loc[:, "close"] * 1.14
        ).sum()
        time_high = df_panel["high"].idxmax()
        df_max_high = df_panel["close"].max()

        df_panel_40 = get_price(
            stock,
            count=12,
            end_date=time_high,
            frequency="daily",
            fields=["open", "high", "close", "low", "high_limit", "money"],
        )
        if len(df_panel_40) < 12:
            return
        df_max_high_40 = df_panel_40["close"].max()
        df_min_low_40 = df_panel_40["close"].min()
        rate_40 = (df_max_high_40 - df_min_low_40) / df_min_low_40

        df_panel_80 = get_price(
            stock,
            count=80,
            end_date=time_high,
            frequency="daily",
            fields=["open", "high", "close", "low", "high_limit", "money"],
        )
        if len(df_panel_80) < 80:
            return
        df_max_high_80 = df_panel_80["high"].max()
        df_min_low_80 = df_panel_80["close"].min()
        rate_80 = (df_max_high_80 - df_min_low_80) / df_min_low_80

        pre_date = (time_high + timedelta(days=-1)).strftime("%Y-%m-%d")
        df_panel_eight = get_price(
            stock,
            count=8,
            end_date=pre_date,
            frequency="daily",
            fields=["open", "high", "close", "low", "high_limit", "money"],
        )
        if len(df_panel_eight) < 8:
            return

        sum_plus_num_two = (
            df_panel_eight.loc[:, "high"] == df_panel_eight.loc[:, "high_limit"]
        ).sum()
        sum_down = (
            df_panel_eight.loc[:, "close"] < df_panel_eight.loc[:, "open"]
        ).sum()
        df_max_high = df_panel_eight["high"].max()

        yes_date_two = trade_date[trade_date.size - 2]
        df_panel_five = get_price(
            stock,
            count=6,
            end_date=yes_date_two,
            frequency="daily",
            fields=["open", "high", "close", "low", "high_limit", "money", "pre_close"],
        )
        if len(df_panel_five) < 6:
            return
        sum_limit_num_five = (
            df_panel_five.loc[:, "close"] > df_panel_five.loc[:, "high_limit"] * 0.95
        ).sum()

        df_panel_10 = get_price(
            stock,
            count=10,
            end_date=yes_date_two,
            frequency="daily",
            fields=["open", "high", "close", "low", "high_limit", "money", "pre_close"],
        )
        if len(df_panel_10) < 10:
            return
        sum_close_low_pre_close = (
            df_panel_10.loc[:, "close"] <= df_panel_10.loc[:, "pre_close"]
        ).sum()

        pre_date_20 = (time_high + timedelta(days=-30)).strftime("%Y-%m-%d")
        df_panel_500 = get_price(
            stock,
            count=500,
            end_date=pre_date_20,
            frequency="daily",
            fields=["open", "high", "close", "low", "high_limit", "money", "pre_close"],
        )
        if len(df_panel_500) < 500:
            return
        df_max_high_500 = df_panel_500["close"].max()

        # 主升浪条件
        if (
            sum_plus_num_two >= 3
            and sum_down <= 3
            and sum_plus_num_40 == 0
            and df_max_high > df_max_high_500
            and rate_40 >= 0.55
            and rate_80 < 3.8
            and sum_close_low_pre_close >= 5
            and sum_limit_num_five == 0
        ):
            pre_date = (context.current_dt + timedelta(days=-1)).strftime("%Y-%m-%d")
            df_panel_three = get_price(
                stock,
                count=3,
                end_date=pre_date,
                frequency="daily",
                fields=["open", "close", "high_limit", "money", "low", "high"],
            )
            if len(df_panel_three) < 3:
                return

            df_close_one = df_panel_three["close"].iloc[0]
            df_open_one = df_panel_three["open"].iloc[0]
            df_high_one = df_panel_three["high"].iloc[0]
            df_close_two = df_panel_three["close"].iloc[1]
            df_open_two = df_panel_three["open"].iloc[1]
            df_high_two = df_panel_three["high"].iloc[1]
            df_low_two = df_panel_three["low"].iloc[1]

            # 十字星判断
            rate_two = abs(df_close_two - df_open_two) / (
                (df_close_two + df_open_two) / 2
            )
            rate_two_high = abs(df_high_two - df_low_two) / (
                (df_high_two + df_low_two) / 2
            )
            df_close_three = df_panel_three["close"].iloc[2]
            df_high_limit_three = df_panel_three["high_limit"].iloc[2]

            # 60日均线条件
            df_panel_60 = get_price(
                stock,
                count=60,
                end_date=yes_date_two,
                frequency="daily",
                fields=["open", "close", "high_limit", "money"],
            )
            if len(df_panel_60) < 60:
                return
            df_close_mean_60 = df_panel_60["close"].mean()

            # 底分型条件
            if (
                df_close_three == df_high_limit_three
                and df_close_two > df_close_mean_60
                and rate_two < 0.025
                and rate_two_high < 0.08
                and df_open_one > df_close_two * 1.02
                and df_open_one > df_open_two * 1.02
                and df_close_three > df_close_two * 1.07
                and df_close_three > df_open_one
            ):
                help_stock.append(stock)
    except Exception as e:
        pass


def pick_high_limit(stocks, end_date):
    try:
        df_panel = get_price(
            stocks,
            count=1,
            end_date=end_date,
            frequency="daily",
            fields=["open", "close", "high_limit", "money", "pre_close"],
        )
        df_close = df_panel["close"]
        df_open = df_panel["open"]
        df_high_limit = df_panel["high_limit"]
        df_pre_close = df_panel["pre_close"]
        high_limit_stock = []
        for stock in stocks:
            try:
                _high_limit = df_high_limit[stock].values[0]
                _close = df_close[stock].values[0]
                _open = df_open[stock].values[0]
                _pre_close = df_pre_close[stock].values[0]
                if stock[0:3] == "300" or stock[0:3] == "688":
                    continue
                if _high_limit == _close and _close > _pre_close * 1.05:
                    high_limit_stock.append(stock)
            except:
                pass
        return high_limit_stock
    except:
        return []


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


def filter_st(codelist):
    current_data = get_current_data()
    codelist = [code for code in codelist if not current_data[code].is_st]
    return codelist


def filter_paused_stock(stock_list):
    current_data = get_current_data()
    stock_list = [stock for stock in stock_list if not current_data[stock].paused]
    return stock_list


def after_market_close(context):
    log.info(str("函数运行时间(after_market_close):" + str(context.current_dt.time())))
    for stock_remove in help_stock:
        help_stock.remove(stock_remove)
    log.info("一天结束")
