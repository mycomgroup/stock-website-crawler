from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
from scipy.stats import linregress


class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa",
        "roa_4",
        "net_operate_cash_flow",
        "net_operate_cash_flow_1",
        "net_operate_cash_flow_2",
        "net_operate_cash_flow_3",
        "total_assets",
        "total_assets_1",
        "total_assets_2",
        "total_assets_3",
        "total_assets_4",
        "total_assets_5",
        "total_non_current_liability",
        "total_non_current_liability_1",
        "gross_profit_margin",
        "gross_profit_margin_4",
        "operating_revenue",
        "operating_revenue_4",
    ]

    def calc(self, data):
        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1
        cfo_sum = (
            data["net_operate_cash_flow"]
            + data["net_operate_cash_flow_1"]
            + data["net_operate_cash_flow_2"]
            + data["net_operate_cash_flow_3"]
        )
        ta_ttm = (
            data["total_assets"]
            + data["total_assets_1"]
            + data["total_assets_2"]
            + data["total_assets_3"]
        ) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - roa * 0.01
        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)
        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1
        turnover = (
            data["operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        turnover_1 = (
            data["operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
        delta_turn = turnover / turnover_1 - 1

        def sign(ser):
            return ser.apply(lambda x: np.where(x > 0, 1, 0))

        indicator_tuple = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicator_tuple).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(sign).sum(axis=1)


def initialize(context):
    set_benchmark("000300.XSHG")
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
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

    g.ipo_days = 180
    g.base_hold_num = 20
    g.primary_pb_group = 1
    g.reduced_pb_group = 2
    g.rsrs_slope_series = []
    g.last_month = 0
    g.high_prices = {}

    run_daily(rebalance, time="9:35", reference_security="000300.XSHG")


def get_universe(watch_date):
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]
    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    cutoff = (pd.Timestamp(watch_date) - pd.Timedelta(days=g.ipo_days)).date()
    sec = sec[sec["start_date"].apply(lambda x: x <= cutoff)]
    stocks = sec.index.tolist()
    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()
    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()
    return stocks


def calc_breadth(watch_date):
    try:
        hs300 = get_index_stocks("000300.XSHG", date=watch_date)
        prices = get_price(
            hs300, end_date=watch_date, count=20, fields=["close"], panel=False
        )
        close = prices.pivot(index="time", columns="code", values="close")
        return float((close.iloc[-1] > close.mean()).mean())
    except:
        return 0.5


def calc_rsrs(watch_date):
    try:
        prices = get_price(
            "000300.XSHG",
            end_date=watch_date,
            fields=["high", "low"],
            count=18,
            panel=False,
        )
        high = prices["high"].values
        low = prices["low"].values
        if len(high) < 18:
            return "NEUTRAL", 0.0
        slope, intercept, r_value, _, _ = linregress(low, high)
        r2 = r_value**2
        g.rsrs_slope_series.append(slope)
        if len(g.rsrs_slope_series) > 600:
            g.rsrs_slope_series.pop(0)
        if len(g.rsrs_slope_series) < 50:
            return "NEUTRAL", 0.0
        mean = np.mean(g.rsrs_slope_series)
        std = np.std(g.rsrs_slope_series)
        zscore = (slope - mean) / std
        rsrs = zscore * slope * r2
        if rsrs > 0.7:
            return "BULLISH", rsrs
        elif rsrs < -0.7:
            return "BEARISH", rsrs
        return "NEUTRAL", rsrs
    except:
        return "NEUTRAL", 0.0


def calc_rfscore_table(stocks, watch_date):
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=watch_date, end_date=watch_date)
    df = factor.basic.copy()
    df["RFScore"] = factor.fscore
    val = get_valuation(
        stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1
    )
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    df = df.join(val, how="left")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio"])
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    return df


def choose_stocks(watch_date, hold_num):
    stocks = get_universe(watch_date)
    df = calc_rfscore_table(stocks[:500], str(watch_date))
    primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= g.primary_pb_group)].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )
    picks = primary.index.tolist()
    if len(picks) < hold_num:
        secondary = df[
            (df["RFScore"] >= 6) & (df["pb_group"] <= g.reduced_pb_group)
        ].copy()
        secondary = secondary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
    if len(picks) < hold_num:
        fallback = df.sort_values(
            ["RFScore", "ROA", "OCFOA", "pb_ratio"],
            ascending=[False, False, False, True],
        )
        for code in fallback.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
    return picks[:hold_num]


def filter_buyable(context, stocks):
    current_data = get_current_data()
    buyable = []
    for stock in stocks:
        if stock not in current_data:
            continue
        cd = current_data[stock]
        if cd.paused or cd.is_st:
            continue
        if "ST" in (cd.name or "") or "*" in (cd.name or ""):
            continue
        if cd.last_price >= cd.high_limit * 0.995:
            continue
        buyable.append(stock)
    return buyable


def rebalance(context):
    watch_date = context.previous_date
    current_month = watch_date.month
    if current_month == g.last_month:
        return
    g.last_month = current_month

    breadth = calc_breadth(watch_date)
    rsrs_signal, rsrs_value = calc_rsrs(watch_date)

    if breadth < 0.15:
        position_ratio, target_hold = 0.0, 0
    elif breadth < 0.25:
        position_ratio, target_hold = 0.5, 10
    elif breadth < 0.35:
        position_ratio, target_hold = 0.75, 15
    else:
        position_ratio, target_hold = 1.0, 20

    if rsrs_signal == "BEARISH":
        position_ratio *= 0.7
        target_hold = max(int(target_hold * 0.7), 5)
    elif rsrs_signal == "BULLISH":
        position_ratio = min(position_ratio * 1.1, 1.0)

    target_hold = max(target_hold, 5) if position_ratio > 0 else 0

    log.info(
        f"【{watch_date}】宽度={breadth:.1%}, RSRS={rsrs_signal}, 仓位={position_ratio:.0%}, 持仓={target_hold}只"
    )

    if target_hold > 0:
        target_stocks = choose_stocks(watch_date, target_hold)
        target_stocks = filter_buyable(context, target_stocks)
    else:
        target_stocks = []

    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target_value(stock, 0)
            g.high_prices.pop(stock, None)

    if target_stocks:
        current_data = get_current_data()
        target_value = (
            context.portfolio.total_value * position_ratio / len(target_stocks)
        )
        for stock in target_stocks:
            price = current_data[stock].last_price
            if price > 0:
                target_amount = int(target_value / price / 100) * 100
                if target_amount >= 100:
                    order_target(stock, target_amount)
                    if stock not in g.high_prices:
                        g.high_prices[stock] = price


def handle_data(context):
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        price = pos.price
        avg_cost = pos.avg_cost
        if stock in g.high_prices:
            if price > g.high_prices[stock]:
                g.high_prices[stock] = price
        else:
            g.high_prices[stock] = price
        if avg_cost <= 0:
            continue
        pnl = (price - avg_cost) / avg_cost
        if pnl <= -0.10:
            order_target_value(stock, 0)
            g.high_prices.pop(stock, None)
        elif pnl > 0 and stock in g.high_prices:
            drawdown = (price - g.high_prices[stock]) / g.high_prices[stock]
            if drawdown <= -0.15:
                order_target_value(stock, 0)
                g.high_prices.pop(stock, None)
