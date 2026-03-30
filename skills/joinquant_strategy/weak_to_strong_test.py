from jqdata import *
import datetime as dt


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.target_list = []
    g.trades = 0
    g.wins = 0

    run_daily(get_stock_list, "9:00")
    run_daily(buy, "09:31")
    run_daily(sell, "14:50")


def get_stock_list(context):
    date = context.previous_date
    date_str = date.strftime("%Y-%m-%d")
    date_1 = get_shifted_date(date_str, -1, "T")
    date_2 = get_shifted_date(date_str, -2, "T")

    initial_list = prepare_stock_list(date_str)
    hl_list = get_hl_stock(initial_list, date_str)
    hl1_list = get_ever_hl_stock(initial_list, date_1)
    hl2_list = get_ever_hl_stock(initial_list, date_2)

    hl_list = [s for s in hl_list if s not in set(hl1_list + hl2_list)]
    g.target_list = hl_list


def buy(context):
    qualified = []
    current_data = get_current_data()

    for s in g.target_list:
        try:
            prev = attribute_history(
                s, 1, "1d", ["close", "volume", "money"], skip_paused=True
            )
            if len(prev) == 0:
                continue

            avg_price_inc = (
                prev["money"][0] / prev["volume"][0] / prev["close"][0] * 1.1 - 1
            )
            if avg_price_inc < 0.07 or prev["money"][0] < 7e8:
                continue

            val = get_valuation(
                s,
                start_date=context.previous_date,
                end_date=context.previous_date,
                fields=["market_cap"],
            )
            if val.empty or val["market_cap"][0] < 70:
                continue

            zyts = calculate_zyts(s, context)
            vol_data = attribute_history(s, zyts, "1d", ["volume"], skip_paused=True)
            if (
                len(vol_data) < 2
                or vol_data["volume"][-1] <= max(vol_data["volume"][:-1]) * 0.9
            ):
                continue

            if s not in current_data:
                continue

            high_limit = current_data[s].high_limit
            open_ratio = current_data[s].day_open / (high_limit / 1.1)

            if open_ratio <= 1 or open_ratio >= 1.06:
                continue

            qualified.append(s)
        except:
            continue

    if qualified:
        value = context.portfolio.available_cash / len(qualified)
        for s in qualified:
            if context.portfolio.available_cash / current_data[s].last_price > 100:
                order_value(s, value, MarketOrderStyle(current_data[s].day_open))
                g.trades += 1


def sell(context):
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            cd = get_current_data()
            if cd[s].last_price < cd[s].high_limit:
                pnl = (cd[s].last_price - pos.avg_cost) / pos.avg_cost
                if pnl > 0:
                    g.wins += 1
                order_target_value(s, 0)


def prepare_stock_list(date):
    initial_list = get_all_securities("stock", date).index.tolist()
    initial_list = [s for s in initial_list if s[0] not in "483" and s[:2] != "68"]
    initial_list = [
        s
        for s in initial_list
        if (
            dt.datetime.strptime(date, "%Y-%m-%d").date()
            - get_security_info(s).start_date
        ).days
        > 50
    ]
    df = get_extras("is_st", initial_list, start_date=date, end_date=date, df=True).T
    df.columns = ["is_st"]
    initial_list = list(df[df["is_st"] == False].index)
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


def get_shifted_date(date, days, days_type="T"):
    d_date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    yesterday = d_date + dt.timedelta(-1)
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


def calculate_zyts(s, context):
    high_prices = attribute_history(s, 101, "1d", ["high"], skip_paused=True)["high"]
    if len(high_prices) < 3:
        return 10
    prev_high = high_prices.iloc[-1]
    zyts_0 = next(
        (i - 1 for i, high in enumerate(high_prices[-3::-1], 2) if high >= prev_high),
        100,
    )
    return zyts_0 + 5
