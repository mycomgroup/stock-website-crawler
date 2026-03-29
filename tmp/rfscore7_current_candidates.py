from jqdata import *
from jqfactor import Factor, calc_factors
from datetime import datetime
import pandas as pd
import numpy as np


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


trade_day = get_trade_days(end_date=datetime.now().date(), count=1)[0]
trade_day_str = str(trade_day)

hs300 = set(get_index_stocks("000300.XSHG", date=trade_day))
zz500 = set(get_index_stocks("000905.XSHG", date=trade_day))
stocks = [stock for stock in (hs300 | zz500) if not stock.startswith("688")]

sec = get_all_securities(types=["stock"], date=trade_day)
sec = sec.loc[sec.index.intersection(stocks)]
sec = sec[sec["start_date"] <= trade_day - pd.Timedelta(days=180)]
stocks = sec.index.tolist()

is_st = get_extras("is_st", stocks, end_date=trade_day, count=1).iloc[-1]
stocks = is_st[is_st == False].index.tolist()

paused = get_price(
    stocks, end_date=trade_day_str, count=1, fields="paused", panel=False
)
paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
stocks = paused[paused == 0].index.tolist()

factor = RFScore()
calc_factors(stocks, [factor], start_date=trade_day_str, end_date=trade_day_str)
df = factor.basic.copy()
df["RFScore"] = factor.fscore

val = get_valuation(
    stocks, end_date=trade_day_str, fields=["pb_ratio", "pe_ratio"], count=1
)
val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
df = df.join(val, how="left")
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])
df["pb_group"] = (
    pd.qcut(
        df["pb_ratio"].rank(method="first"),
        10,
        labels=False,
        duplicates="drop",
    )
    + 1
)

df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()
df = df.sort_values(
    ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
    ascending=[False, False, False, False, False, True],
)

prices = get_price(
    list(hs300), end_date=trade_day_str, count=20, fields=["close"], panel=False
)
close = prices.pivot(index="time", columns="code", values="close")
breadth = float((close.iloc[-1] > close.mean()).mean())
idx = get_price("000300.XSHG", end_date=trade_day_str, count=20, fields=["close"])
trend_on = float(idx["close"].iloc[-1]) > float(idx["close"].mean())

hold_num = 10 if breadth < 0.25 and (not trend_on) else 20

print("trade_day", trade_day_str)
print("breadth", round(breadth, 4))
print("trend_on", trend_on)
print("target_hold_num", hold_num)
print("candidate_count", len(df))
print(
    df[
        [
            "RFScore",
            "pb_ratio",
            "pe_ratio",
            "ROA",
            "OCFOA",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
    ]
    .head(hold_num)
    .round(4)
    .to_string()
)
