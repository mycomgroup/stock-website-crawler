# 234板策略 - 仅二板版本
# 测试时间：2024-01-01 至 2024-12-31

from jqdata import *
import pandas as pd


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("system", "error")

    g.max_turnover = 30
    g.target_stock = None
    g.ps = 1

    run_daily(select_stock, "09:25")
    run_daily(buy_stock, "09:31")
    run_daily(sell_stock, "14:50")


def select_stock(context):
    date = context.previous_date.strftime("%Y-%m-%d")

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

    prev_date = get_prev_date(date)
    prev2_date = get_prev_date(prev_date)

    hl_today = get_hl_stocks(all_stocks, date)
    hl_prev = get_hl_stocks(all_stocks, prev_date)
    hl_prev2 = get_hl_stocks(all_stocks, prev2_date)

    two_board = list(set(hl_today) & set(hl_prev) - set(hl_prev2))

    non_yzb = filter_yzb(two_board, date)

    low_turnover = []
    for s in non_yzb[:50]:
        try:
            hsl = HSL([s], date)
            if s in hsl[0] and hsl[0][s] < g.max_turnover:
                low_turnover.append(s)
        except:
            pass

    if len(low_turnover) > 0:
        caps = []
        for s in low_turnover:
            try:
                q = query(valuation.circulating_market_cap).filter(valuation.code == s)
                df = get_fundamentals(q, date=date)
                if len(df) > 0:
                    caps.append((s, df["circulating_market_cap"].iloc[0]))
            except:
                pass

        if len(caps) > 0:
            caps.sort(key=lambda x: x[1])
            g.target_stock = caps[0][0]
        else:
            g.target_stock = None
    else:
        g.target_stock = None


def buy_stock(context):
    if g.target_stock is None:
        return

    current_data = get_current_data()
    stock = g.target_stock

    if current_data[stock].last_price == current_data[stock].high_limit:
        log.info(f"{stock} 涨停开盘，放弃买入")
        return

    if len(context.portfolio.positions) == 0:
        value = context.portfolio.available_cash / g.ps
        order_value(stock, value)
        log.info(f"买入 {stock}")


def sell_stock(context):
    current_data = get_current_data()

    for stock in list(context.portfolio.positions):
        if current_data[stock].last_price < current_data[stock].high_limit:
            order_target_value(stock, 0)
            log.info(f"卖出 {stock}")


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
            pass
    return result


def get_prev_date(date):
    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date in all_days:
        idx = all_days.index(date)
        if idx > 0:
            return all_days[idx - 1]
    return date
