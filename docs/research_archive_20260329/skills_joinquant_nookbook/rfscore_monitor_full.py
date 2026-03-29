from jqdata import *
from jqfactor import Factor, calc_factors
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json


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


def get_rfscore_candidates(trade_day):
    """获取RFScore候选股"""
    trade_day_str = str(trade_day)

    hs300 = set(get_index_stocks("000300.XSHG", date=trade_day))
    zz500 = set(get_index_stocks("000905.XSHG", date=trade_day))
    stocks = [s for s in (hs300 | zz500) if not s.startswith("688")]

    sec = get_all_securities(types=["stock"], date=trade_day)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= trade_day - pd.Timedelta(days=180)]
    stocks = sec.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=trade_day, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    try:
        paused = get_price(
            stocks, end_date=trade_day_str, count=1, fields="paused", panel=False
        )
        paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
        stocks = paused[paused == 0].index.tolist()
    except:
        pass

    factor = RFScore()
    calc_factors(stocks, [factor], start_date=trade_day_str, end_date=trade_day_str)
    df = factor.basic.copy()
    df["RFScore"] = factor.fscore

    val = get_valuation(
        stocks,
        end_date=trade_day_str,
        fields=["pb_ratio", "pe_ratio", "circulating_market_cap"],
        count=1,
    )
    val = val.drop_duplicates("code").set_index("code")
    df = df.join(val, how="left")
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])

    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )
    candidates = df[(df["RFScore"] >= 7) & (df["pb_group"] <= 2)].copy()
    candidates = candidates.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )

    return candidates


def get_industry_distribution(codes, trade_day):
    """获取行业分布"""
    industries = {}
    for code in codes[:30]:  # 限制数量避免超时
        try:
            info = get_industry(code, date=trade_day)
            sw1 = info.get(code, {}).get("sw_l1", {})
            ind_name = sw1.get("industry_name", "未知")
            industries[ind_name] = industries.get(ind_name, 0) + 1
        except:
            pass
    return industries


# 主程序
today = datetime.now().date()
today = get_trade_days(end_date=today, count=1)[0]

# 获取当前和历史数据
dates = [today]
for i in [1, 5, 20, 60]:
    try:
        past_date = get_trade_days(end_date=today - timedelta(days=i), count=1)[0]
        dates.append(past_date)
    except:
        pass

results = {}
for date in dates[:2]:  # 只取今天和1天前
    try:
        candidates = get_rfscore_candidates(date)
        industries = (
            get_industry_distribution(candidates.index.tolist(), date)
            if len(candidates) > 0
            else {}
        )
        results[str(date)] = {
            "count": len(candidates),
            "pb_mean": float(candidates["pb_ratio"].mean())
            if len(candidates) > 0
            else None,
            "pb_median": float(candidates["pb_ratio"].median())
            if len(candidates) > 0
            else None,
            "pe_mean": float(candidates["pe_ratio"].mean())
            if len(candidates) > 0
            else None,
            "pe_median": float(candidates["pe_ratio"].median())
            if len(candidates) > 0
            else None,
            "roa_mean": float(candidates["ROA"].mean())
            if len(candidates) > 0
            else None,
            "ocfoa_mean": float(candidates["OCFOA"].mean())
            if len(candidates) > 0
            else None,
            "industries": industries,
            "top_candidates": candidates.head(10).index.tolist()
            if len(candidates) > 0
            else [],
        }
    except Exception as e:
        results[str(date)] = {"error": str(e)}

# 输出监控报告
print("=" * 70)
print("RFScore PB10 候选组合质量监控报告")
print(f"生成时间: {today}")
print("=" * 70)

for date, data in results.items():
    print(f"\n【{date}】")
    if "error" in data:
        print(f"  错误: {data['error']}")
        continue
    print(f"  候选数量: {data['count']}")
    if data["count"] > 0:
        print(f"  PB均值/中位: {data['pb_mean']:.4f} / {data['pb_median']:.4f}")
        print(f"  PE均值/中位: {data['pe_mean']:.2f} / {data['pe_median']:.2f}")
        print(f"  ROA均值: {data['roa_mean']:.2f}%")
        print(f"  前3行业: {dict(list(data['industries'].items())[:3])}")
        print(f"  Top3候选: {data['top_candidates'][:3]}")

# 质量评估
latest = results.get(str(today), {})
if "error" not in latest and latest.get("count", 0) > 0:
    print(f"\n" + "=" * 70)
    print("【当前组合质量评估】")

    score = 100
    issues = []

    # 估值检查
    if latest["pe_mean"] > 30:
        score -= 15
        issues.append(f"平均PE={latest['pe_mean']:.1f}过高 (-15)")
    elif latest["pe_mean"] > 20:
        score -= 5
        issues.append(f"平均PE={latest['pe_mean']:.1f}偏高 (-5)")

    # 盈利检查
    if latest["roa_mean"] < 1.0:
        score -= 20
        issues.append(f"平均ROA={latest['roa_mean']:.2f}%过低 (-20)")
    elif latest["roa_mean"] < 2.0:
        score -= 10
        issues.append(f"平均ROA={latest['roa_mean']:.2f}%偏低 (-10)")

    # 数量检查
    if latest["count"] < 5:
        score -= 20
        issues.append(f"候选数量{latest['count']}过少 (-20)")
    elif latest["count"] < 10:
        score -= 10
        issues.append(f"候选数量{latest['count']}偏少 (-10)")

    score = max(0, score)

    if score >= 80:
        grade = "A - 优秀"
    elif score >= 60:
        grade = "B - 良好"
    elif score >= 40:
        grade = "C - 一般"
    else:
        grade = "D - 较差"

    print(f"质量评分: {score}/100 (等级: {grade})")
    print(f"问题列表:")
    for issue in issues:
        print(f"  - {issue}")
    if not issues:
        print(f"  - 无明显问题 ✓")

    print(f"\n结论: 当前组合{'符合' if score >= 60 else '不符合'}预期的RFScore风格")

print("\n" + "=" * 70)
print("完整数据(JSON):")
print(json.dumps(results, ensure_ascii=False, indent=2))
