from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np


START_DATE = "2022-01-01"
END_DATE = "2025-12-31"
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
        turnover = (
            data["operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        turnover_1 = (
            data["operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
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
    stocks = [s for s in stocks if not s.startswith("688")]

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


def calc_rfscore_frame(stocks, date):
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=date, end_date=date)

    basic = factor.basic.copy()
    basic["RFScore"] = factor.fscore

    val = get_valuation(
        stocks,
        end_date=date,
        fields=["pb_ratio", "pe_ratio", "circulating_market_cap"],
        count=1,
    )
    val = val.drop_duplicates("code").set_index("code")[
        ["pb_ratio", "pe_ratio", "circulating_market_cap"]
    ]

    basic = basic.join(val, how="left")
    basic = basic.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["RFScore", "pb_ratio"]
    )
    basic["pb_group"] = (
        pd.qcut(
            basic["pb_ratio"].rank(method="first"),
            10,
            labels=False,
            duplicates="drop",
        )
        + 1
    )

    basic = basic.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN"],
        ascending=[False, False, False, False, False],
    )
    return basic


def calc_turnover(stocks, date):
    df = get_price(
        stocks, end_date=date, count=20, fields=["volume", "money"], panel=False
    )
    if df.empty:
        return pd.Series(dtype=float)

    vol = df.pivot(index="time", columns="code", values="volume")
    val = df.pivot(index="time", columns="code", values="money")

    avg_vol = vol.mean()
    avg_money = val.mean()

    cap = get_valuation(
        stocks, end_date=date, fields=["circulating_market_cap"], count=1
    )
    cap = cap.drop_duplicates("code").set_index("code")["circulating_market_cap"]

    avg_vol = avg_vol.reindex(cap.index)
    avg_money = avg_money.reindex(cap.index)

    turnover = avg_money / (cap * 1e8 + 1)
    return turnover


def calc_cgo(stocks, date, lookback=260):
    prices = get_price(
        stocks, end_date=date, count=lookback, fields=["close"], panel=False
    )
    if prices.empty:
        return pd.Series(dtype=float)

    close = prices.pivot(index="time", columns="code", values="close")
    current_price = close.iloc[-1]
    avg_price = close.mean()

    cgo = (current_price - avg_price) / (current_price + 1e-10)
    return cgo


def choose_portfolio(frame, variant, extra_data=None):
    df = frame.copy()

    if variant == "rfscore_pb10":
        df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    elif variant == "rfscore_pb10_turnover_filter":
        if extra_data is not None and "turnover" in extra_data:
            turnover = extra_data["turnover"]
            df = df.join(turnover.rename("turnover"), how="left")
            turnover_threshold = df["turnover"].quantile(0.8)
            df = df[
                (df["RFScore"] == 7)
                & (df["pb_group"] == 1)
                & (df["turnover"] < turnover_threshold)
            ]
        else:
            df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    elif variant == "rfscore_pb10_cgo_filter":
        if extra_data is not None and "cgo" in extra_data:
            cgo = extra_data["cgo"]
            df = df.join(cgo.rename("cgo"), how="left")
            cgo_threshold = df["cgo"].quantile(0.8)
            df = df[
                (df["RFScore"] == 7)
                & (df["pb_group"] == 1)
                & (df["cgo"] < cgo_threshold)
            ]
        else:
            df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    elif variant == "rfscore_pb10_combined_filter":
        if extra_data is not None and "turnover" in extra_data and "cgo" in extra_data:
            turnover = extra_data["turnover"]
            cgo = extra_data["cgo"]
            df = df.join(turnover.rename("turnover"), how="left").join(
                cgo.rename("cgo"), how="left"
            )
            turnover_threshold = df["turnover"].quantile(0.8)
            cgo_threshold = df["cgo"].quantile(0.8)
            df = df[
                (df["RFScore"] == 7)
                & (df["pb_group"] == 1)
                & (df["turnover"] < turnover_threshold)
                & (df["cgo"] < cgo_threshold)
            ]
        else:
            df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
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


def calc_max_drawdown(nav_series):
    if len(nav_series) == 0:
        return 0.0
    nav = pd.Series(nav_series)
    cummax = nav.cummax()
    drawdown = (nav - cummax) / cummax
    return float(drawdown.min())


def calc_sharpe(returns, annual_factor=12):
    if len(returns) == 0:
        return 0.0
    ret = pd.Series(returns)
    if ret.std() == 0:
        return 0.0
    return float(ret.mean() / ret.std() * np.sqrt(annual_factor))


# 主测试流程
print("开始测试 RFScore PB10 基准策略及过滤器")
print(f"测试期间: {START_DATE} 至 {END_DATE}")

variants = [
    "rfscore_pb10",
    "rfscore_pb10_turnover_filter",
    "rfscore_pb10_cgo_filter",
    "rfscore_pb10_combined_filter",
]

results = {name: [] for name in variants}
stock_counts = {name: [] for name in variants}

dates = get_monthly_dates(START_DATE, END_DATE)
print(f"月度调仓次数: {len(dates)}")

for i in range(len(dates) - 1):
    if i % 12 == 0:  # 每年打印一次进度
        print(f"进度: {i}/{len(dates) - 1} ({i / (len(dates) - 1) * 100:.1f}%)")

    date = pd.Timestamp(dates[i]).date()
    next_date = pd.Timestamp(dates[i + 1]).date()
    date_str = str(date)
    next_date_str = str(next_date)

    stocks = get_universe(date)
    frame = calc_rfscore_frame(stocks, date_str)

    # 计算所需的过滤数据
    turnover = calc_turnover(stocks, date_str)
    cgo = calc_cgo(stocks, date_str)

    extra_data = {"turnover": turnover, "cgo": cgo}

    rf7_pb10_count = len(frame[(frame["RFScore"] == 7) & (frame["pb_group"] == 1)])
    print(f"rebalance {date_str}: universe={len(stocks)}, rf7_pb10={rf7_pb10_count}")

    for variant in variants:
        selected = choose_portfolio(frame, variant, extra_data)
        stock_counts[variant].append(len(selected))
        period_return = get_forward_return(selected, date_str, next_date_str)
        results[variant].append(period_return)

print("\n计算结果...")
for name in variants:
    summarize(name, results[name], stock_counts[name])


def summarize(name, rets, counts):
    ser = pd.Series(rets)
    if len(ser) == 0:
        print(f"\n{name}: 无数据")
        return

    nav = (1 + ser).cumprod()
    cum = nav.iloc[-1] - 1
    ann = (1 + cum) ** (12 / len(ser)) - 1 if len(ser) else 0
    mdd = calc_max_drawdown(nav)
    sharpe = calc_sharpe(rets)
    win_rate = (ser > 0).mean()
    avg_count = np.mean(counts) if counts else 0

    print(f"\n{name}:")
    print(f"  累计收益: {cum:.4f}")
    print(f"  年化收益: {ann:.4f}")
    print(f"  最大回撤: {mdd:.4f}")
    print(f"  夏普比率: {sharpe:.4f}")
    print(f"  月胜率: {win_rate:.4f}")
    print(f"  平均候选股数: {avg_count:.1f}")
    print(f"  调仓次数: {len(ser)}")
