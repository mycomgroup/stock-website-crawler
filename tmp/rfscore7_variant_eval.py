from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np


START_DATE = "2024-01-01"
END_DATE = "2025-03-26"
HOLD_NUM = 20
IPO_DAYS = 180
BREADTH_THRESHOLD = 0.28


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    watch_date = None
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

        turnover = data["operating_revenue"] / (
            data["total_assets"] + data["total_assets_1"]
        ).mean()
        turnover_1 = data["operating_revenue_4"] / (
            data["total_assets_4"] + data["total_assets_5"]
        ).mean()
        delta_turn = turnover / turnover_1 - 1

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


def get_monthly_dates(start_date, end_date):
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    dates = []
    current_month = None
    for day in trade_days:
        if day.month != current_month:
            dates.append(day)
            current_month = day.month
    return dates


def get_universe(date):
    hs300 = set(get_index_stocks("000300.XSHG", date=date))
    zz500 = set(get_index_stocks("000905.XSHG", date=date))
    stocks = list(hs300 | zz500)

    sec = get_all_securities(types=["stock"], date=date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= date - pd.Timedelta(days=IPO_DAYS)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(stocks, end_date=date, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    zdt = get_price(
        stocks,
        end_date=date,
        fields=["close", "high_limit", "low_limit", "paused"],
        count=1,
        panel=False,
        fq="post",
    )
    zdt["zdt_raw"] = zdt.apply(
        lambda x: 1
        if ((x["close"] == x["high_limit"]) or (x["close"] == x["low_limit"]))
        else 0,
        axis=1,
    )
    zdt["zdt"] = zdt.apply(
        lambda x: 0 if ((x["paused"] == 0) and (x["zdt_raw"] == 0)) else 1, axis=1
    )
    zdt = zdt.pivot(index="time", columns="code", values="zdt").iloc[-1]
    stocks = zdt[zdt == 0].index.tolist()

    return stocks


def calc_market_state(date):
    hs300 = get_index_stocks("000300.XSHG", date=date)
    prices = get_price(hs300, end_date=date, count=20, fields=["close"], panel=False)
    close = prices.pivot(index="time", columns="code", values="close")
    latest = close.iloc[-1]
    ma20 = close.mean()
    breadth = float((latest > ma20).mean())

    index_close = get_price("000300.XSHG", end_date=date, count=20, fields=["close"])
    index_latest = float(index_close["close"].iloc[-1])
    index_ma20 = float(index_close["close"].mean())
    trend_on = index_latest > index_ma20

    return {
        "breadth": breadth,
        "trend_on": trend_on,
        "risk_on": breadth >= BREADTH_THRESHOLD and trend_on,
    }


def calc_rfscore_frame(stocks, date):
    factor = RFScore()
    factor.watch_date = date
    calc_factors(stocks, [factor], start_date=date, end_date=date)

    basic = factor.basic.copy()
    basic["RFScore"] = factor.fscore

    val = get_valuation(stocks, end_date=date, fields=["pb_ratio", "pe_ratio"], count=1)
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]

    basic = basic.join(val, how="left")
    basic = basic.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])
    basic["pb_group"] = pd.qcut(
        basic["pb_ratio"].rank(method="first"),
        10,
        labels=False,
        duplicates="drop",
    ) + 1

    basic = basic.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN"],
        ascending=[False, False, False, False, False],
    )
    return basic


def choose_portfolio(frame, variant):
    df = frame.copy()

    if variant == "rfscore_base":
        pass
    elif variant == "rfscore_pb10":
        df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    elif variant == "rfscore_pb20":
        df = df[(df["RFScore"] == 7) & (df["pb_group"] <= 2)]
    elif variant == "rfscore_pb3040":
        df = df[(df["RFScore"] == 7) & (df["pb_group"] == 4)]
    elif variant == "rfscore_pb3040_relaxed":
        df = df[(df["RFScore"] >= 6) & (df["pb_group"] == 4)]
    else:
        raise ValueError("unknown variant")

    if df.empty:
        return []

    return df.index.tolist()[:HOLD_NUM]


def get_forward_return(stocks, start_date, end_date):
    if not stocks:
        return 0.0
    px0 = get_price(stocks, end_date=start_date, count=1, fields=["close"], panel=False)
    px1 = get_price(stocks, end_date=end_date, count=1, fields=["close"], panel=False)
    px0 = px0.pivot(index="time", columns="code", values="close").iloc[-1]
    px1 = px1.pivot(index="time", columns="code", values="close").iloc[-1]
    ret = (px1 / px0 - 1).dropna()
    if len(ret) == 0:
        return 0.0
    return float(ret.mean())


variants = [
    "rfscore_base",
    "rfscore_pb10",
    "rfscore_pb20",
    "rfscore_pb3040",
    "rfscore_pb3040_relaxed",
]

results = {name: [] for name in variants}
results["rfscore_base_width"] = []
results["rfscore_pb3040_width"] = []

dates = get_monthly_dates(START_DATE, END_DATE)
print("monthly_dates", len(dates))

for i in range(len(dates) - 1):
    date = pd.Timestamp(dates[i]).date()
    next_date = pd.Timestamp(dates[i + 1]).date()
    date_str = str(date)
    next_date_str = str(next_date)
    state = calc_market_state(date_str)
    stocks = get_universe(date)
    frame = calc_rfscore_frame(stocks, date_str)

    print("rebalance", date_str, "universe", len(stocks), "breadth", round(state["breadth"], 4), "trend_on", state["trend_on"])

    for variant in variants:
        selected = choose_portfolio(frame, variant)
        period_return = get_forward_return(selected, date_str, next_date_str)
        results[variant].append(period_return)

    base_selected = choose_portfolio(frame, "rfscore_base")
    pb3040_selected = choose_portfolio(frame, "rfscore_pb3040")

    results["rfscore_base_width"].append(
        get_forward_return(base_selected, date_str, next_date_str) if state["risk_on"] else 0.0
    )
    results["rfscore_pb3040_width"].append(
        get_forward_return(pb3040_selected, date_str, next_date_str) if state["risk_on"] else 0.0
    )


def summarize(name, rets):
    ser = pd.Series(rets)
    cum = (1 + ser).prod() - 1
    ann = (1 + cum) ** (12 / len(ser)) - 1 if len(ser) else 0
    print(
        name,
        "count", len(ser),
        "cum", round(cum, 4),
        "ann", round(ann, 4),
        "mean", round(float(ser.mean()), 4),
        "win", round(float((ser > 0).mean()), 4),
        "min", round(float(ser.min()), 4),
        "max", round(float(ser.max()), 4),
    )


print("\nSUMMARY")
for name, rets in results.items():
    summarize(name, rets)
