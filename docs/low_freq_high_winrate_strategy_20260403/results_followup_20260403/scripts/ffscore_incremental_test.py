"""
FFScore 对 RFScore 增量验证脚本
================================
用途: 在 JoinQuant Notebook 中验证 FFScore 是否能为 RFScore 提供增量价值
对比三种策略:
  1. 基线: RFScore7 + PB20
  2. 候选A: RFScore7 + PB20 + FFScore >= 3 硬过滤
  3. 候选B: RFScore7 + PB20 + FFScore 排序加分

预期结论: 三者表现差异在统计上不显著 (No-Go)
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
    """RFScore 7因子"""

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

        indicators = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicators).T.replace([-np.inf, np.inf], np.nan)
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


class FFScore(Factor):
    """华泰 FFScore 5因子"""

    name = "FFScore"
    max_window = 1
    dependencies = [
        "roe",
        "roe_4",
        "total_assets",
        "total_assets_1",
        "total_assets_4",
        "total_assets_5",
        "operating_revenue",
        "operating_revenue_4",
        "total_non_current_assets",
        "total_non_current_assets_4",
        "total_non_current_liability",
        "total_non_current_liability_4",
        "total_current_assets",
        "total_current_assets_1",
        "total_current_assets_4",
        "total_current_assets_5",
        "total_operating_revenue",
        "total_operating_revenue_4",
    ]

    def calc(self, data):
        roe = data["roe"]
        delta_roe = roe / data["roe_4"] - 1

        lever = data["total_non_current_liability"] / data["total_non_current_assets"]
        lever1 = (
            data["total_non_current_liability_4"] / data["total_non_current_assets_4"]
        )
        delta_lever = -(lever / lever1 - 1)

        caturn_1 = (
            data["operating_revenue"]
            / (data["total_current_assets"] + data["total_current_assets_1"]).mean()
        )
        caturn_2 = (
            data["operating_revenue_4"]
            / (data["total_current_assets_4"] + data["total_current_assets_5"]).mean()
        )
        delta_caturn = caturn_1 / caturn_2 - 1

        total_turn = (
            data["total_operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        total_turn_1 = (
            data["total_operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
        delta_turn = total_turn / total_turn_1 - 1

        indicators = (roe, delta_roe, delta_caturn, delta_turn, delta_lever)
        self.basic = pd.concat(indicators).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROE",
            "DELTA_ROE",
            "DELTA_CATURN",
            "DELTA_TURN",
            "DELTA_LEVER",
        ]
        self.ffscore = self.basic.apply(sign).sum(axis=1)


def get_universe(watch_date):
    """获取股票池: 沪深300 + 中证500"""
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=180)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    return stocks


def calc_rfscore_table(stocks, watch_date):
    """计算 RFScore 表格"""
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
    df = df.dropna(subset=["RFScore", "ROA", "OCFOA", "pb_ratio", "pe_ratio"])
    df = df[
        (df["pb_ratio"] > 0)
        & (df["pe_ratio"] > 0)
        & (df["pe_ratio"] < 100)
        & (df["ROA"] > 0.5)
    ].copy()

    if df.empty:
        return df

    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    return df


def calc_ffscore_table(stocks, watch_date):
    """计算 FFScore 表格"""
    factor = FFScore()
    calc_factors(stocks, [factor], start_date=watch_date, end_date=watch_date)

    df = factor.basic.copy()
    df["FFScore"] = factor.ffscore
    return df


def calc_market_breadth(watch_date):
    """计算市场宽度"""
    hs300 = get_index_stocks("000300.XSHG", date=watch_date)
    prices = get_price(
        hs300, end_date=watch_date, count=20, fields=["close"], panel=False
    )
    close = prices.pivot(index="time", columns="code", values="close")
    return float((close.iloc[-1] > close.mean()).mean())


def get_target_hold_num(breadth):
    """根据市场宽度确定目标持仓数"""
    if breadth < 0.15:
        return 0
    elif breadth < 0.25:
        return 10
    elif breadth < 0.35:
        idx = get_price("000300.XSHG", end_date=watch_date, count=20, fields=["close"])
        trend_on = float(idx["close"].iloc[-1]) > float(idx["close"].mean())
        return 12 if not trend_on else 15
    else:
        return 15


def select_baseline(df, target_hold_num):
    """基线选股: RFScore7 + PB20"""
    if df.empty or target_hold_num <= 0:
        return []

    candidates = df[(df["RFScore"] == 7) & (df["pb_group"] <= 2)].copy()
    if candidates.empty:
        return []

    candidates["score"] = (
        candidates["RFScore"] * 100
        + candidates["ROA"].rank(pct=True) * 30
        + candidates["OCFOA"].rank(pct=True) * 20
        + candidates["DELTA_MARGIN"].rank(pct=True) * 10
        - candidates["pb_ratio"].rank(pct=True) * 10
    )
    candidates = candidates.sort_values("score", ascending=False)
    return candidates.index.tolist()[:target_hold_num]


def select_with_ffscore_hard_filter(
    df_rfscore, df_ffscore, target_hold_num, ffscore_threshold=3
):
    """方式A: FFScore 硬过滤"""
    if df_rfscore.empty or df_ffscore.empty or target_hold_num <= 0:
        return []

    merged = df_rfscore.join(df_ffscore[["FFScore"]], how="inner")
    merged = merged[merged["FFScore"] >= ffscore_threshold]

    candidates = merged[(merged["RFScore"] == 7) & (merged["pb_group"] <= 2)].copy()
    if candidates.empty:
        return []

    candidates["score"] = (
        candidates["RFScore"] * 100
        + candidates["ROA"].rank(pct=True) * 30
        + candidates["OCFOA"].rank(pct=True) * 20
        + candidates["DELTA_MARGIN"].rank(pct=True) * 10
        - candidates["pb_ratio"].rank(pct=True) * 10
    )
    candidates = candidates.sort_values("score", ascending=False)
    return candidates.index.tolist()[:target_hold_num]


def select_with_ffscore_bonus(df_rfscore, df_ffscore, target_hold_num):
    """方式B: FFScore 排序加分"""
    if df_rfscore.empty or df_ffscore.empty or target_hold_num <= 0:
        return []

    merged = df_rfscore.join(df_ffscore[["FFScore"]], how="inner")
    merged["FFScore"] = merged["FFScore"].fillna(0)

    candidates = merged[(merged["RFScore"] == 7) & (merged["pb_group"] <= 2)].copy()
    if candidates.empty:
        return []

    candidates["score"] = (
        candidates["RFScore"] * 100
        + candidates["ROA"].rank(pct=True) * 30
        + candidates["OCFOA"].rank(pct=True) * 20
        + candidates["DELTA_MARGIN"].rank(pct=True) * 10
        - candidates["pb_ratio"].rank(pct=True) * 10
        + candidates["FFScore"].rank(pct=True) * 15
    )
    candidates = candidates.sort_values("score", ascending=False)
    return candidates.index.tolist()[:target_hold_num]


# ==================== 主回测逻辑 ====================

start_date = "2023-01-01"
end_date = "2025-03-31"

trade_dates = get_trade_days(start_date=start_date, end_date=end_date)
monthly_dates = [d for d in trade_dates if d.day <= 5]
monthly_dates = [monthly_dates[i] for i in range(0, len(monthly_dates), 1)]

results = {
    "baseline": {"dates": [], "returns": [], "hold_count": [], "candidate_count": []},
    "ffscore_hard": {
        "dates": [],
        "returns": [],
        "hold_count": [],
        "candidate_count": [],
    },
    "ffscore_bonus": {
        "dates": [],
        "returns": [],
        "hold_count": [],
        "candidate_count": [],
    },
}

prev_holdings = {"baseline": [], "ffscore_hard": [], "ffscore_bonus": []}

for i, watch_date in enumerate(monthly_dates[:-1]):
    next_date = monthly_dates[i + 1]

    stocks = get_universe(watch_date)
    if not stocks:
        continue

    df_rf = calc_rfscore_table(stocks, str(watch_date))
    if df_rf.empty:
        continue

    df_ff = calc_ffscore_table(stocks, str(watch_date))

    breadth = calc_market_breadth(watch_date)
    target_num = get_target_hold_num(breadth)

    picks_baseline = select_baseline(df_rf, target_num)
    picks_hard = select_with_ffscore_hard_filter(df_rf, df_ff, target_num)
    picks_bonus = select_with_ffscore_bonus(df_rf, df_ff, target_num)

    for strategy, picks in [
        ("baseline", picks_baseline),
        ("ffscore_hard", picks_hard),
        ("ffscore_bonus", picks_bonus),
    ]:
        if not picks:
            ret = 0.0
        else:
            prices = get_price(
                picks,
                start_date=watch_date,
                end_date=next_date,
                fields=["close"],
                panel=False,
            )
            if prices.empty:
                ret = 0.0
            else:
                pivot = prices.pivot(index="time", columns="code", values="close")
                if len(pivot) < 2:
                    ret = 0.0
                else:
                    rets = (pivot.iloc[-1] / pivot.iloc[0] - 1).mean()
                    ret = float(rets)

        results[strategy]["dates"].append(watch_date)
        results[strategy]["returns"].append(ret)
        results[strategy]["hold_count"].append(len(picks))

        if strategy == "baseline":
            results[strategy]["candidate_count"].append(
                len(df_rf[(df_rf["RFScore"] == 7) & (df_rf["pb_group"] <= 2)])
            )
        elif strategy == "ffscore_hard":
            merged = df_rf.join(df_ff[["FFScore"]], how="inner")
            merged = merged[merged["FFScore"] >= 3]
            results[strategy]["candidate_count"].append(
                len(merged[(merged["RFScore"] == 7) & (merged["pb_group"] <= 2)])
            )
        else:
            results[strategy]["candidate_count"].append(
                len(df_rf[(df_rf["RFScore"] == 7) & (df_rf["pb_group"] <= 2)])
            )

    prev_holdings["baseline"] = picks_baseline
    prev_holdings["ffscore_hard"] = picks_hard
    prev_holdings["ffscore_bonus"] = picks_bonus

# ==================== 结果汇总 ====================

print("=" * 80)
print("FFScore 对 RFScore 增量验证结果")
print("=" * 80)

for strategy in ["baseline", "ffscore_hard", "ffscore_bonus"]:
    rets = results[strategy]["returns"]
    holds = results[strategy]["hold_count"]
    cands = results[strategy]["candidate_count"]

    annual_ret = np.mean(rets) * 12
    win_rate = np.sum(np.array(rets) > 0) / len(rets) if rets else 0
    avg_hold = np.mean(holds) if holds else 0
    avg_cand = np.mean(cands) if cands else 0

    print(f"\n策略: {strategy}")
    print(f"  调仓次数: {len(rets)}")
    print(f"  月均收益: {np.mean(rets):.4f}")
    print(f"  年化收益(估算): {annual_ret:.2%}")
    print(f"  月度胜率: {win_rate:.1%}")
    print(f"  平均持仓数: {avg_hold:.1f}")
    print(f"  平均候选数: {avg_cand:.1f}")

print("\n" + "=" * 80)
print("增量对比 (vs 基线)")
print("=" * 80)

baseline_annual = np.mean(results["baseline"]["returns"]) * 12
for strategy in ["ffscore_hard", "ffscore_bonus"]:
    strat_annual = np.mean(results[strategy]["returns"]) * 12
    diff = strat_annual - baseline_annual
    print(f"  {strategy}: 年化差异 = {diff:+.2%}")

print("\n结论预期: 差异 < 0.5%，统计不显著 -> No-Go")
