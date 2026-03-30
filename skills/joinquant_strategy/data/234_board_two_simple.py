# 234板策略 - 仅二板简化版本

from jqdata import *
import pandas as pd


def initialize(context):
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("system", "error")

    g.board_level = "two"
    g.max_turnover_ratio = 15
    g.min_max_board = 3
    g.min_zt_count = 30

    g.ps = 1
    g.target_list = []
    g.sentiment_ok = False

    run_daily(get_stock_list, "09:25")
    run_daily(sell_positions, "14:50")


def get_stock_list(context):
    date = context.previous_date

    max_lianban = get_max_lianban(date)
    zt_count = get_zt_count(date)

    if max_lianban >= g.min_max_board and zt_count >= g.min_zt_count:
        g.sentiment_ok = True
    else:
        g.sentiment_ok = False
        g.target_list = []
        return

    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (
            s.startswith("68")
            or s.startswith("4")
            or s.startswith("8")
            or s.startswith("3")
        )
    ]

    prev_date = date - pd.Timedelta(days=1)
    while prev_date not in get_all_trade_days():
        prev_date -= pd.Timedelta(days=1)

    prev2_date = prev_date - pd.Timedelta(days=1)
    while prev2_date not in get_all_trade_days():
        prev2_date -= pd.Timedelta(days=1)

    hl_1d = get_hl_stocks(all_stocks, date)
    hl_2d = get_hl_stocks(all_stocks, prev_date)
    hl_3d = get_hl_stocks(all_stocks, prev2_date)

    two_board_stocks = list(set(hl_1d) & set(hl_2d) - set(hl_3d))

    non_yzb = filter_yzb(two_board_stocks, date)

    low_hsl = []
    for s in non_yzb:
        try:
            hsl_data = HSL([s], date)
            if s in hsl_data[0]:
                hsl = hsl_data[0][s]
                if hsl < g.max_turnover_ratio:
                    low_hsl.append(s)
        except:
            continue

    if len(low_hsl) > 0:
        caps = []
        for s in low_hsl:
            try:
                q = query(valuation.circulating_market_cap).filter(valuation.code == s)
                df = get_fundamentals(q, date=date)
                if len(df) > 0:
                    cap = df["circulating_market_cap"].iloc[0]
                    caps.append((s, cap))
            except:
                continue

        caps.sort(key=lambda x: x[1])
        g.target_list = [s for s, _ in caps[: g.ps]]
    else:
        g.target_list = []

    if len(g.target_list) > 0:
        current_data = get_current_data()
        for s in g.target_list:
            if current_data[s].last_price != current_data[s].high_limit:
                order_value(s, context.portfolio.available_cash / g.ps)
                log.info(f"买入 {s}")


def sell_positions(context):
    current_data = get_current_data()
    for s in list(context.portfolio.positions):
        if current_data[s].last_price < current_data[s].high_limit:
            order_target_value(s, 0)
            log.info(f"卖出 {s}")


def get_hl_stocks(stock_list, date):
    try:
        df = get_price(
            stock_list,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()
        hl = df[df["close"] == df["high_limit"]]
        return list(hl["code"])
    except:
        return []


def filter_yzb(stock_list, date):
    result = []
    for s in stock_list:
        try:
            df = get_price(s, end_date=date, count=1, fields=["low", "high"])
            if df["low"].iloc[0] != df["high"].iloc[0]:
                result.append(s)
        except:
            continue
    return result


def get_max_lianban(date):
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        hl_today = get_hl_stocks(all_stocks, date)
        max_count = 0

        for s in hl_today[:30]:
            try:
                df = get_price(
                    s,
                    end_date=date,
                    count=10,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                count = 0
                for i in range(len(df) - 1, -1, -1):
                    if df.iloc[i]["close"] == df.iloc[i]["high_limit"]:
                        count += 1
                    else:
                        break
                max_count = max(max_count, count)
            except:
                continue

        return max_count
    except:
        return 0


def get_zt_count(date):
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        hl = get_hl_stocks(all_stocks, date)
        return len(hl)
    except:
        return 0
