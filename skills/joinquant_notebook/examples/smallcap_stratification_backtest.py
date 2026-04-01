"""
小市值市值区间分层基线研究
按流通市值分层为 5档，月度调仓等权持有
时间范围：2018-01-01 至 2025-03-30
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def initialize(context):
    set_benchmark("000300.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")

    g.market_cap_ranges = [
        (5, 15, "A组_5-15亿"),
        (15, 30, "B组_15-30亿"),
        (30, 60, "C组_30-60亿"),
        (60, 100, "D组_60-100亿"),
        (100, 200, "E组_100-200亿"),
    ]

    g.stock_num = 10
    g.monthly_trade = False

    run_monthly(rebalance_all_groups, 1, time="09:30")

    g.results = {}
    for _, _, name in g.market_cap_ranges:
        g.results[name] = {
            "annual_returns": [],
            "max_drawdowns": [],
            "trade_counts": [],
            "turnover_rates": [],
            "avg_volumes": [],
        }


def get_base_stocks(date):
    stocks = get_all_securities(types=["stock"], date=date).index.tolist()

    stocks = filter_st_stock(stocks)
    stocks = filter_kcb_stock(stocks)

    paused_stocks = []
    current_data = get_current_data()
    for stock in stocks:
        if current_data[stock].paused:
            paused_stocks.append(stock)
    stocks = [s for s in stocks if s not in paused_stocks]

    listed_dates = get_all_securities(types=["stock"], date=date)["start_date"]
    stocks = [s for s in stocks if (date - pd.to_datetime(listed_dates[s])).days > 180]

    q = query(valuation.code, valuation.pb_ratio).filter(valuation.code.in_(stocks))
    df = get_fundamentals(q, date=date)
    if df is not None and len(df) > 0:
        stocks = df[df["pb_ratio"] > 0]["code"].tolist()

    return stocks


def get_stocks_by_market_cap(stocks, date, cap_min, cap_max):
    q = (
        query(valuation.code, valuation.circulating_market_cap)
        .filter(
            valuation.code.in_(stocks),
            valuation.circulating_market_cap >= cap_min,
            valuation.circulating_market_cap < cap_max,
        )
        .order_by(valuation.circulating_market_cap.asc())
        .limit(g.stock_num)
    )

    df = get_fundamentals(q, date=date)
    if df is None or len(df) == 0:
        return []

    return df["code"].tolist()


def rebalance_all_groups(context):
    date = context.current_dt
    prev_date = context.previous_date

    base_stocks = get_base_stocks(prev_date)

    for cap_min, cap_max, group_name in g.market_cap_ranges:
        target_stocks = get_stocks_by_market_cap(
            base_stocks, prev_date, cap_min, cap_max
        )

        rebalance_single_group(context, target_stocks, group_name, date)


def rebalance_single_group(context, target_stocks, group_name, date):
    current_positions = [
        stock
        for stock in context.portfolio.positions.keys()
        if stock.startswith(group_name.split("_")[0])
    ]

    for stock in current_positions:
        if stock not in target_stocks:
            order_target_value(stock, 0)

    if len(target_stocks) == 0:
        return

    available_cash = context.portfolio.available_cash
    position_count = len(context.portfolio.positions)
    target_num = min(len(target_stocks), g.stock_num)

    if target_num > position_count:
        value_per_stock = available_cash / (target_num - position_count)

        for stock in target_stocks:
            if stock not in context.portfolio.positions:
                order_target_value(stock, value_per_stock)
                if len(context.portfolio.positions) >= target_num:
                    break


def after_trading_end(context):
    date = context.current_dt

    for cap_min, cap_max, group_name in g.market_cap_ranges:
        calc_group_performance(context, group_name, date, cap_min, cap_max)


def calc_group_performance(context, group_name, date, cap_min, cap_max):
    pass


def process_data(context):
    import json

    start_date = "2018-01-01"
    end_date = "2025-03-30"

    trade_dates = get_trade_days(start_date, end_date)

    all_results = {}
    for _, _, name in g.market_cap_ranges:
        all_results[name] = {"yearly": {}, "total": {}}

    initial_capital = 100000
    capitals = {name: initial_capital for _, _, name in g.market_cap_ranges}
    positions = {name: {} for _, _, name in g.market_cap_ranges}
    daily_values = {name: [] for _, _, name in g.market_cap_ranges}

    monthly_dates = []
    for i, date in enumerate(trade_dates):
        date_obj = pd.to_datetime(date)
        if i == 0 or date_obj.month != pd.to_datetime(trade_dates[i - 1]).month:
            monthly_dates.append(date)

    print(f"总交易日数: {len(trade_dates)}")
    print(f"月度调仓次数: {len(monthly_dates)}")

    for i, date in enumerate(monthly_dates):
        prev_date = trade_dates[trade_dates.index(date) - 1] if i > 0 else date

        base_stocks = get_base_stocks_fast(prev_date)

        for cap_min, cap_max, group_name in g.market_cap_ranges:
            target_stocks = get_stocks_by_market_cap_fast(
                base_stocks, prev_date, cap_min, cap_max
            )

            new_positions = rebalance_positions_fast(
                positions[group_name], target_stocks, capitals[group_name], date
            )

            positions[group_name] = new_positions

            capital_value = calc_position_value_fast(new_positions, date)

            capitals[group_name] = capital_value

            year = str(pd.to_datetime(date).year)
            if year not in all_results[group_name]["yearly"]:
                all_results[group_name]["yearly"][year] = {
                    "start_value": capital_value,
                    "values": [],
                }
            all_results[group_name]["yearly"][year]["values"].append(capital_value)

        if (i + 1) % 12 == 0:
            print(f"已处理 {i + 1}/{len(monthly_dates)} 月")

    for _, _, group_name in g.market_cap_ranges:
        calc_final_results(all_results[group_name], initial_capital)

    output_path = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output/smallcap_stratification_results.json"
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n结果已保存到: {output_path}")
    return all_results


def get_base_stocks_fast(date):
    try:
        stocks = get_all_securities(types=["stock"], date=date).index.tolist()

        stocks = filter_st_stock(stocks)
        stocks = filter_kcb_stock(stocks)

        q = query(valuation.code, valuation.pb_ratio).filter(
            valuation.code.in_(stocks), valuation.pb_ratio > 0
        )
        df = get_fundamentals(q, date=date)
        if df is not None and len(df) > 0:
            stocks = df["code"].tolist()

        return stocks
    except:
        return []


def get_stocks_by_market_cap_fast(stocks, date, cap_min, cap_max):
    try:
        q = (
            query(valuation.code, valuation.circulating_market_cap)
            .filter(
                valuation.code.in_(stocks),
                valuation.circulating_market_cap >= cap_min,
                valuation.circulating_market_cap < cap_max,
            )
            .order_by(valuation.circulating_market_cap.asc())
            .limit(10)
        )

        df = get_fundamentals(q, date=date)
        if df is None or len(df) == 0:
            return []

        return df["code"].tolist()
    except:
        return []


def rebalance_positions_fast(old_positions, target_stocks, capital, date):
    if len(target_stocks) == 0:
        return {}

    try:
        prices = get_price(
            target_stocks, end_date=date, count=1, fields=["close"], panel=False
        )
        if prices is None or len(prices) == 0:
            return old_positions

        price_dict = {}
        for row in prices.itertuples():
            price_dict[row.code] = row.close

        valid_stocks = [
            s for s in target_stocks if s in price_dict and price_dict[s] > 0
        ]

        if len(valid_stocks) == 0:
            return old_positions

        value_per_stock = capital / len(valid_stocks)

        new_positions = {}
        for stock in valid_stocks:
            shares = int(value_per_stock / price_dict[stock])
            new_positions[stock] = {"shares": shares, "buy_price": price_dict[stock]}

        return new_positions
    except:
        return old_positions


def calc_position_value_fast(positions, date):
    if len(positions) == 0:
        return 0

    stocks = list(positions.keys())

    try:
        prices = get_price(
            stocks, end_date=date, count=1, fields=["close"], panel=False
        )
        if prices is None or len(prices) == 0:
            return 0

        total_value = 0
        for row in prices.itertuples():
            if row.code in positions:
                total_value += positions[row.code]["shares"] * row.close

        return total_value
    except:
        return 0


def calc_final_results(group_data, initial_capital):
    yearly_data = group_data["yearly"]

    total_return = 0
    for year, data in yearly_data.items():
        if len(data["values"]) > 0:
            year_return = (data["values"][-1] - data["start_value"]) / data[
                "start_value"
            ]
            total_return += year_return

    group_data["total"] = {
        "total_return": total_return,
        "annual_return": total_return / len(yearly_data),
    }


if __name__ == "__builtin__":
    pass
else:
    result = process_data(None)
    print("\n=== 五组市值分层回测结果 ===")
    for group_name in [
        "A组_5-15亿",
        "B组_15-30亿",
        "C组_30-60亿",
        "D组_60-100亿",
        "E组_100-200亿",
    ]:
        if group_name in result:
            print(f"\n{group_name}:")
            print(f"  总收益率: {result[group_name]['total']['total_return']:.2%}")
            print(f"  年化收益率: {result[group_name]['total']['annual_return']:.2%}")
