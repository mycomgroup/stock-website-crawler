#!/usr/bin/env python3
# RFScore PB10 候选组合质量监控脚本
# 用于监控当前候选池的质量指标

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


def get_candidates(trade_day, pb_group_limit=2, rfscore_filter=7):
    """获取指定日期的候选股"""
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
        stocks,
        end_date=trade_day_str,
        fields=["pb_ratio", "pe_ratio", "market_cap"],
        count=1,
    )
    val = val.drop_duplicates("code").set_index("code")[
        ["pb_ratio", "pe_ratio", "market_cap"]
    ]
    df = df.join(val, how="left")
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])

    # PB分位数分组
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    # RFScore 7 + PB前20% (即 pb_group <= 2)
    candidates = df[
        (df["RFScore"] >= rfscore_filter) & (df["pb_group"] <= pb_group_limit)
    ].copy()
    candidates = candidates.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )

    return candidates


def get_industry_info(codes, trade_day):
    """获取行业信息"""
    industry_rows = []
    for code in codes:
        try:
            info = get_industry(code, date=trade_day)
            sw1 = info.get(code, {}).get("sw_l1", {})
            industry_rows.append(
                {
                    "code": code,
                    "industry_code": sw1.get("industry_code"),
                    "industry_name": sw1.get("industry_name"),
                }
            )
        except:
            industry_rows.append(
                {"code": code, "industry_code": None, "industry_name": None}
            )
    return pd.DataFrame(industry_rows).set_index("code")


def analyze_candidates(candidates, trade_day):
    """分析候选组合质量"""
    report = {
        "date": str(trade_day),
        "total_candidates": len(candidates),
        "metrics": {},
    }

    if len(candidates) == 0:
        report["status"] = "ERROR"
        report["error"] = "无候选股"
        return report

    # 估值指标
    report["metrics"]["valuation"] = {
        "pb_mean": round(float(candidates["pb_ratio"].mean()), 4),
        "pb_median": round(float(candidates["pb_ratio"].median()), 4),
        "pb_std": round(float(candidates["pb_ratio"].std()), 4),
        "pb_min": round(float(candidates["pb_ratio"].min()), 4),
        "pb_max": round(float(candidates["pb_ratio"].max()), 4),
        "pe_mean": round(float(candidates["pe_ratio"].mean()), 4),
        "pe_median": round(float(candidates["pe_ratio"].median()), 4),
        "pe_std": round(float(candidates["pe_ratio"].std()), 4),
        "pe_max": round(float(candidates["pe_ratio"].max()), 4),
    }

    # RFScore 分布
    report["metrics"]["rfscore_dist"] = candidates["RFScore"].value_counts().to_dict()

    # 盈利质量指标
    report["metrics"]["profitability"] = {
        "roa_mean": round(float(candidates["ROA"].mean()), 4),
        "roa_median": round(float(candidates["ROA"].median()), 4),
        "roa_min": round(float(candidates["ROA"].min()), 4),
        "ocfoa_mean": round(float(candidates["OCFOA"].mean()), 4),
        "ocfoa_median": round(float(candidates["OCFOA"].median()), 4),
        "delta_margin_mean": round(float(candidates["DELTA_MARGIN"].mean()), 4),
        "delta_turn_mean": round(float(candidates["DELTA_TURN"].mean()), 4),
    }

    # 市值分布
    report["metrics"]["market_cap"] = {
        "mean_billion": round(float(candidates["market_cap"].mean() / 1e8), 2),
        "median_billion": round(float(candidates["market_cap"].median() / 1e8), 2),
        "min_billion": round(float(candidates["market_cap"].min() / 1e8), 2),
        "max_billion": round(float(candidates["market_cap"].max() / 1e8), 2),
    }

    # 行业分布
    industry_df = get_industry_info(candidates.index.tolist(), trade_day)
    industry_dist = industry_df["industry_name"].value_counts()
    report["metrics"]["industry"] = {
        "unique_industries": len(industry_dist),
        "top_industries": industry_dist.head(5).to_dict(),
        "concentration_ratio": round(float(industry_dist.iloc[0] / len(candidates)), 2)
        if len(industry_dist) > 0
        else 0,
    }

    # 异常股检测
    anomalies = []

    # 极端高估值
    pe_threshold = 50
    high_pe = candidates[candidates["pe_ratio"] > pe_threshold]
    for code in high_pe.index:
        anomalies.append(
            {
                "code": code,
                "type": "极高PE",
                "value": round(float(high_pe.loc[code, "pe_ratio"]), 2),
                "threshold": pe_threshold,
                "reason": f"PE={high_pe.loc[code, 'pe_ratio']:.1f} > {pe_threshold}",
            }
        )

    # 极端低ROA (负值或极低)
    roa_threshold = 0.5
    low_roa = candidates[candidates["ROA"] < roa_threshold]
    for code in low_roa.index:
        anomalies.append(
            {
                "code": code,
                "type": "低ROA",
                "value": round(float(low_roa.loc[code, "ROA"]), 2),
                "threshold": roa_threshold,
                "reason": f"ROA={low_roa.loc[code, 'ROA']:.2f}% < {roa_threshold}%",
            }
        )

    # 负经营现金流
    negative_ocf = candidates[candidates["OCFOA"] < 0]
    for code in negative_ocf.index:
        anomalies.append(
            {
                "code": code,
                "type": "负OCF",
                "value": round(float(negative_ocf.loc[code, "OCFOA"]), 4),
                "threshold": 0,
                "reason": f"OCFOA={negative_ocf.loc[code, 'OCFOA']:.4f} < 0",
            }
        )

    # 极高PB (超出PB10%范围但仍在筛选内的情况)
    pb_threshold = 2.0
    high_pb = candidates[candidates["pb_ratio"] > pb_threshold]
    for code in high_pb.index:
        anomalies.append(
            {
                "code": code,
                "type": "高PB",
                "value": round(float(high_pb.loc[code, "pb_ratio"]), 2),
                "threshold": pb_threshold,
                "reason": f"PB={high_pb.loc[code, 'pb_ratio']:.2f} > {pb_threshold}",
            }
        )

    report["anomalies"] = anomalies
    report["anomaly_count"] = len(anomalies)

    # 质量评分 (0-100)
    quality_score = 100
    quality_deductions = []

    # PE过高扣分
    pe_mean = candidates["pe_ratio"].mean()
    if pe_mean > 30:
        quality_score -= 15
        quality_deductions.append(f"平均PE={pe_mean:.1f}过高 (-15)")
    elif pe_mean > 20:
        quality_score -= 5
        quality_deductions.append(f"平均PE={pe_mean:.1f}偏高 (-5)")

    # ROA过低扣分
    roa_mean = candidates["ROA"].mean()
    if roa_mean < 1.0:
        quality_score -= 20
        quality_deductions.append(f"平均ROA={roa_mean:.2f}%过低 (-20)")
    elif roa_mean < 2.0:
        quality_score -= 10
        quality_deductions.append(f"平均ROA={roa_mean:.2f}%偏低 (-10)")

    # 异常股比例过高扣分
    anomaly_ratio = len(anomalies) / len(candidates) if len(candidates) > 0 else 0
    if anomaly_ratio > 0.3:
        quality_score -= 20
        quality_deductions.append(f"异常股比例{anomaly_ratio:.1%}过高 (-20)")
    elif anomaly_ratio > 0.15:
        quality_score -= 10
        quality_deductions.append(f"异常股比例{anomaly_ratio:.1%}偏高 (-10)")

    # 行业集中度过高扣分
    concentration = report["metrics"]["industry"]["concentration_ratio"]
    if concentration > 0.4:
        quality_score -= 15
        quality_deductions.append(f"行业集中度{concentration:.0%}过高 (-15)")
    elif concentration > 0.25:
        quality_score -= 5
        quality_deductions.append(f"行业集中度{concentration:.0%}偏高 (-5)")

    report["quality_score"] = max(0, quality_score)
    report["quality_deductions"] = quality_deductions

    # 判定是否符合预期
    if quality_score >= 80:
        report["quality_grade"] = "A"
        report["quality_assessment"] = "优秀 - 组合质量符合预期"
    elif quality_score >= 60:
        report["quality_grade"] = "B"
        report["quality_assessment"] = "良好 - 组合质量基本可接受"
    elif quality_score >= 40:
        report["quality_grade"] = "C"
        report["quality_assessment"] = "一般 - 组合存在明显问题，需谨慎"
    else:
        report["quality_grade"] = "D"
        report["quality_assessment"] = "较差 - 组合质量严重偏离预期，建议重新评估"

    return report


# 主程序
trade_day = get_trade_days(end_date=datetime.now().date(), count=1)[0]
print(f"=" * 60)
print(f"RFScore PB10 候选组合质量监控报告")
print(f"检测日期: {trade_day}")
print(f"=" * 60)

# 获取当前候选
candidates = get_candidates(trade_day, pb_group_limit=2, rfscore_filter=7)
print(f"\n候选股总数: {len(candidates)}")

if len(candidates) > 0:
    report = analyze_candidates(candidates, trade_day)

    print(
        f"\n【质量评分】: {report['quality_score']}/100 (等级: {report['quality_grade']})"
    )
    print(f"【评估结论】: {report['quality_assessment']}")

    print(f"\n【估值指标】")
    for k, v in report["metrics"]["valuation"].items():
        print(f"  {k}: {v}")

    print(f"\n【盈利质量】")
    for k, v in report["metrics"]["profitability"].items():
        print(f"  {k}: {v}")

    print(f"\n【行业分布】")
    print(f"  行业数量: {report['metrics']['industry']['unique_industries']}")
    print(f"  集中度: {report['metrics']['industry']['concentration_ratio']}")
    print(f"  前5行业: {report['metrics']['industry']['top_industries']}")

    print(f"\n【异常股检测】")
    if report["anomaly_count"] > 0:
        print(f"  发现 {report['anomaly_count']} 只异常股:")
        for anomaly in report["anomalies"]:
            print(f"    - {anomaly['code']}: {anomaly['type']} ({anomaly['reason']})")
    else:
        print(f"  未发现异常股 ✓")

    if report["quality_deductions"]:
        print(f"\n【扣分项】")
        for deduction in report["quality_deductions"]:
            print(f"  - {deduction}")

    # 输出完整JSON报告
    print(f"\n{'=' * 60}")
    print("完整监控报告 (JSON格式):")
    print(json.dumps(report, ensure_ascii=False, indent=2))
else:
    print("警告: 当前无符合条件的候选股！")
