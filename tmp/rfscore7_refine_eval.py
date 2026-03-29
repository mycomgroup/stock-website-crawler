from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np


START_DATE = "2024-01-01"
END_DATE = "2025-03-26"
HOLD_NUM = 20
IPO_DAYS = 180


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


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
    return stocks


def calc_market_state(date):
    hs300 = get_index_stocks("000300.XSHG", date=date)
    prices = get_price(hs300, end_date=date, count=20, fields=["close"], panel=False)
    close = prices.pivot(index="time", columns="code", values="close")
    breadth = float((close.iloc[-1] > close.mean()).mean())

    idx = get_price("000300.XSHG", end_date=date, count=20, fields=["close"])
    trend_on = float(idx["close"].iloc[-1]) > float(idx["close"].mean())
    return breadth, trend_on


def calc_frame(stocks, date):
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=date, end_date=date)
    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    val = get_valuation(stocks, end_date=date, fields=["pb_ratio", "pe_ratio"], count=1)
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]

    q = query(
        income.code,
        income.total_operating_revenue,
        income.total_operating_cost,
        balance.total_assets,
    ).filter(income.code.in_(stocks))
    gp = get_fundamentals(q, date=date).set_index("code")
    gp["GP"] = (gp["total_operating_revenue"] - gp["total_operating_cost"]) / gp["total_assets"]

    df = df.join(val, how="left").join(gp[["GP"]], how="left")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["RFScore", "pb_ratio", "GP"])
    df["pb_group"] = pd.qcut(
        df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
    ) + 1
    return df


def pick(df, mode):
    use = df[(df["RFScore"] == 7) & (df["pb_group"] <= 2)].copy()
    if use.empty:
        return []

    if mode == "default":
        use = use.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN"],
            ascending=[False, False, False, False, False],
        )
    elif mode == "gp":
        use = use.sort_values(
            ["RFScore", "GP", "ROA", "OCFOA"],
            ascending=[False, False, False, False],
        )
    else:
        raise ValueError("unknown mode")

    return use.index.tolist()[:HOLD_NUM]


def forward_return(stocks, start_date, end_date):
    if not stocks:
        return 0.0
    px0 = get_price(stocks, end_date=start_date, count=1, fields=["close"], panel=False)
    px1 = get_price(stocks, end_date=end_date, count=1, fields=["close"], panel=False)
    px0 = px0.pivot(index="time", columns="code", values="close").iloc[-1]
    px1 = px1.pivot(index="time", columns="code", values="close").iloc[-1]
    ret = (px1 / px0 - 1).dropna()
    return float(ret.mean()) if len(ret) else 0.0


def summarize(name, rets):
    ser = pd.Series(rets)
    nav = (1 + ser).cumprod()
    dd = (nav / nav.cummax() - 1).min()
    cum = nav.iloc[-1] - 1
    ann = (1 + cum) ** (12 / len(ser)) - 1
    print(
        name,
        "cum", round(float(cum), 4),
        "ann", round(float(ann), 4),
        "win", round(float((ser > 0).mean()), 4),
        "mdd", round(float(dd), 4),
        "mean", round(float(ser.mean()), 4),
    )


results = {
    "pb20_default": [],
    "pb20_gp": [],
    "pb20_cash_020": [],
    "pb20_cash_025": [],
    "pb20_half_020": [],
    "pb20_half_025": [],
    "pb20_gp_half_020": [],
    "pb20_gp_half_025": [],
}

dates = get_monthly_dates(START_DATE, END_DATE)

for i in range(len(dates) - 1):
    date = pd.Timestamp(dates[i]).date()
    next_date = pd.Timestamp(dates[i + 1]).date()
    date_str = str(date)
    next_date_str = str(next_date)
    breadth, trend_on = calc_market_state(date_str)

    stocks = get_universe(date)
    frame = calc_frame(stocks, date_str)
    default_ret = forward_return(pick(frame, "default"), date_str, next_date_str)
    gp_ret = forward_return(pick(frame, "gp"), date_str, next_date_str)

    results["pb20_default"].append(default_ret)
    results["pb20_gp"].append(gp_ret)

    risk_off_020 = breadth < 0.20 and (not trend_on)
    risk_off_025 = breadth < 0.25 and (not trend_on)

    results["pb20_cash_020"].append(0.0 if risk_off_020 else default_ret)
    results["pb20_cash_025"].append(0.0 if risk_off_025 else default_ret)
    results["pb20_half_020"].append(default_ret * 0.5 if risk_off_020 else default_ret)
    results["pb20_half_025"].append(default_ret * 0.5 if risk_off_025 else default_ret)
    results["pb20_gp_half_020"].append(gp_ret * 0.5 if risk_off_020 else gp_ret)
    results["pb20_gp_half_025"].append(gp_ret * 0.5 if risk_off_025 else gp_ret)

    print(
        "rebalance", date_str,
        "breadth", round(breadth, 4),
        "trend_on", trend_on,
        "default_ret", round(default_ret, 4),
        "gp_ret", round(gp_ret, 4),
    )

print("\nSUMMARY")
for name, rets in results.items():
    summarize(name, rets)
