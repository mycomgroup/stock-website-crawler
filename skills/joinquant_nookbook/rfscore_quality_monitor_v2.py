from jqdata import *
from jqfactor import Factor, calc_factors
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json

"""
RFScore候选组合质量监控指标体系 v2.0
深化研究版 - 包含因子有效性、历史对比、风险暴露等多维度监控
"""


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


# 主程序
today = datetime.now().date()
trade_day = get_trade_days(end_date=today, count=1)[0]
trade_day_str = str(trade_day)

print("=" * 70)
print("RFScore PB10 候选质量监控指标体系 v2.0 (深化研究)")
print(f"检测日期: {trade_day}")
print("=" * 70)

# 获取候选股
hs300 = set(get_index_stocks("000300.XSHG", date=trade_day))
zz500 = set(get_index_stocks("000905.XSHG", date=trade_day))
stocks = [s for s in (hs300 | zz500) if not s.startswith("688")]

sec = get_all_securities(types=["stock"], date=trade_day)
sec = sec.loc[sec.index.intersection(stocks)]
sec = sec[sec["start_date"] <= trade_day - pd.Timedelta(days=180)]
stocks = sec.index.tolist()

is_st = get_extras("is_st", stocks, end_date=trade_day, count=1).iloc[-1]
stocks = is_st[is_st == False].index.tolist()

factor = RFScore()
calc_factors(stocks, [factor], start_date=trade_day_str, end_date=trade_day_str)
df = factor.basic.copy()
df["RFScore"] = factor.fscore

val = get_valuation(
    stocks,
    end_date=trade_day_str,
    fields=["pb_ratio", "pe_ratio", "market_cap", "circulating_market_cap"],
    count=1,
)
val = val.drop_duplicates("code").set_index("code")
df = df.join(val, how="left")
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])

df["pb_group"] = (
    pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop")
    + 1
)
candidates = df[(df["RFScore"] >= 7) & (df["pb_group"] <= 2)].copy()

print(f"\n候选股总数: {len(candidates)}")

if len(candidates) == 0:
    print("警告: 无候选股，跳过监控")
else:
    # ========================================
    # 监控指标体系 v2.0 - 六大维度
    # ========================================

    metrics = {}

    # ========================================
    # 维度一: 估值质量监控
    # ========================================
    print("\n" + "=" * 70)
    print("【维度一: 估值质量监控】")
    print("=" * 70)

    metrics["valuation"] = {
        "pb_mean": float(candidates["pb_ratio"].mean()),
        "pb_median": float(candidates["pb_ratio"].median()),
        "pb_std": float(candidates["pb_ratio"].std()),
        "pb_range": [
            float(candidates["pb_ratio"].min()),
            float(candidates["pb_ratio"].max()),
        ],
        "pe_mean": float(candidates["pe_ratio"].mean()),
        "pe_median": float(candidates["pe_ratio"].median()),
        "pe_std": float(candidates["pe_ratio"].std()),
        "pe_range": [
            float(candidates["pe_ratio"].min()),
            float(candidates["pe_ratio"].max()),
        ],
        # 新增: 估值偏离度
        "pb_skewness": float(candidates["pb_ratio"].skew()),
        "pe_skewness": float(candidates["pe_ratio"].skew()),
        # 新增: PB/PE比值（衡量价值强度）
        "pb_pe_ratio": float(
            candidates["pb_ratio"].mean() / candidates["pe_ratio"].mean()
        ),
    }

    print(f"\n基础估值指标:")
    print(f"  PB均值: {metrics['valuation']['pb_mean']:.4f} (目标: <1.5)")
    print(f"  PB中位数: {metrics['valuation']['pb_median']:.4f}")
    print(f"  PB离散度: {metrics['valuation']['pb_std']:.4f} (越小越好)")
    print(
        f"  PB范围: [{metrics['valuation']['pb_range'][0]:.4f}, {metrics['valuation']['pb_range'][1]:.4f}]"
    )

    print(f"\n估值偏离分析:")
    print(f"  PB偏度: {metrics['valuation']['pb_skewness']:.4f}")
    if metrics["valuation"]["pb_skewness"] > 0:
        print(f"    → 右偏，存在高PB异常股")
    else:
        print(f"    → 左偏，估值分布集中于低端 ✓")

    print(f"  PB/PE比值: {metrics['valuation']['pb_pe_ratio']:.4f}")
    if metrics["valuation"]["pb_pe_ratio"] < 0.05:
        print(f"    → 深度价值，市场悲观预期强")
    elif metrics["valuation"]["pb_pe_ratio"] < 0.10:
        print(f"    → 正常价值区间 ✓")
    else:
        print(f"    → 估值偏高或盈利偏低 ⚠️")

    # ========================================
    # 维度二: 盈利质量监控
    # ========================================
    print("\n" + "=" * 70)
    print("【维度二: 盈利质量监控】")
    print("=" * 70)

    metrics["profitability"] = {
        "roa_mean": float(candidates["ROA"].mean()),
        "roa_median": float(candidates["ROA"].median()),
        "roa_std": float(candidates["ROA"].std()),
        "roa_min": float(candidates["ROA"].min()),
        "ocfoa_mean": float(candidates["OCFOA"].mean()),
        "ocfoa_median": float(candidates["OCFOA"].median()),
        "ocfoa_positive_ratio": float(
            (candidates["OCFOA"] > 0).sum() / len(candidates)
        ),
        # 新增: ROA分布
        "roa_high_ratio": float(
            (candidates["ROA"] > 3.0).sum() / len(candidates)
        ),  # 高ROA占比
        "roa_low_ratio": float(
            (candidates["ROA"] < 1.0).sum() / len(candidates)
        ),  # 低ROA占比
        # 新增: 盈利质量稳定性（ROA与OCFOA的相关性）
        "roa_ocf_correlation": float(candidates["ROA"].corr(candidates["OCFOA"])),
        # 新增: 应计质量（ACCRUAL越小越好）
        "accrual_mean": float(candidates["ACCRUAL"].mean()),
    }

    print(f"\n盈利能力指标:")
    print(f"  ROA均值: {metrics['profitability']['roa_mean']:.2f}% (目标: >2.0%)")
    print(f"  ROA中位数: {metrics['profitability']['roa_median']:.2f}%")
    print(f"  ROA高占比(>3%): {metrics['profitability']['roa_high_ratio']:.1%}")
    print(f"  ROA低占比(<1%): {metrics['profitability']['roa_low_ratio']:.1%}")

    print(f"\n现金流质量:")
    print(f"  OCFOA均值: {metrics['profitability']['ocfoa_mean']:.4f}")
    print(f"  OCF正值占比: {metrics['profitability']['ocfoa_positive_ratio']:.1%}")
    print(f"  ROA-OCF相关性: {metrics['profitability']['roa_ocf_correlation']:.3f}")
    if metrics["profitability"]["roa_ocf_correlation"] > 0.7:
        print(f"    → 盈利与现金流高度一致 ✓")
    else:
        print(f"    → 盈利质量存疑，利润可能虚高 ⚠️")

    print(f"\n应计质量:")
    print(f"  Accrual均值: {metrics['profitability']['accrual_mean']:.4f}")
    if metrics["profitability"]["accrual_mean"] > 0.02:
        print(f"    → 应计较高，利润含纸面成分 ⚠️")
    elif metrics["profitability"]["accrual_mean"] < -0.02:
        print(f"    → 应计负值，现金流超利润 ✓")
    else:
        print(f"    → 应计正常 ✓")

    # ========================================
    # 维度三: 因子有效性监控
    # ========================================
    print("\n" + "=" * 70)
    print("【维度三: 因子有效性监控】")
    print("=" * 70)

    # 分析各子因子的分布和有效性
    metrics["factor_validity"] = {
        "rfscore_dist": candidates["RFScore"].value_counts().to_dict(),
        # 新增: 各子因子得分率
        "delta_roa_positive_ratio": float(
            (candidates["DELTA_ROA"] > 0).sum() / len(candidates)
        ),
        "delta_margin_positive_ratio": float(
            (candidates["DELTA_MARGIN"] > 0).sum() / len(candidates)
        ),
        "delta_turn_positive_ratio": float(
            (candidates["DELTA_TURN"] > 0).sum() / len(candidates)
        ),
        "delta_leveler_negative_ratio": float(
            (candidates["DELTA_LEVELER"] < 0).sum() / len(candidates)
        ),  # 杠杆下降是好信号
        # 新增: 因子信号强度
        "signal_strength": float(
            (
                (candidates["DELTA_ROA"] > 0).sum()
                + (candidates["DELTA_MARGIN"] > 0).sum()
                + (candidates["DELTA_TURN"] > 0).sum()
                + (candidates["DELTA_LEVELER"] < 0).sum()
            )
            / (4 * len(candidates))
        ),  # 平均信号强度
    }

    print(f"\nRFScore分布:")
    for score, count in sorted(
        metrics["factor_validity"]["rfscore_dist"].items(), reverse=True
    ):
        print(f"  Score={score}: {count}只 ({count / len(candidates):.1%})")

    print(f"\n子因子信号强度:")
    print(
        f"  ROA改善占比: {metrics['factor_validity']['delta_roa_positive_ratio']:.1%}"
    )
    print(
        f"  毛利率改善占比: {metrics['factor_validity']['delta_margin_positive_ratio']:.1%}"
    )
    print(
        f"  周转率改善占比: {metrics['factor_validity']['delta_turn_positive_ratio']:.1%}"
    )
    print(
        f"  杠杆下降占比: {metrics['factor_validity']['delta_leveler_negative_ratio']:.1%}"
    )
    print(f"  综合信号强度: {metrics['factor_validity']['signal_strength']:.2f}")

    if metrics["factor_validity"]["signal_strength"] > 0.75:
        print(f"    → 信号强劲，基本面全面改善 ✓")
    elif metrics["factor_validity"]["signal_strength"] > 0.50:
        print(f"    → 信号正常 ✓")
    else:
        print(f"    → 信号偏弱，部分因子失效 ⚠️")

    # ========================================
    # 维度四: 分散度与集中度监控
    # ========================================
    print("\n" + "=" * 70)
    print("【维度四: 分散度与集中度监控】")
    print("=" * 70)

    # 行业分布
    industries = {}
    for code in candidates.index[:30]:
        try:
            info = get_industry(code, date=trade_day)
            sw1 = info.get(code, {}).get("sw_l1", {})
            ind_name = sw1.get("industry_name", "未知")
            industries[ind_name] = industries.get(ind_name, 0) + 1
        except:
            pass

    # 计算HHI指数
    if industries:
        total = sum(industries.values())
        hhi = sum((count / total) ** 2 for count in industries.values())
        max_concentration = max(count / total for count in industries.values())
        num_industries = len(industries)
    else:
        hhi = 1.0
        max_concentration = 1.0
        num_industries = 0

    metrics["diversification"] = {
        "candidate_count": len(candidates),
        "num_industries": num_industries,
        "hhi_index": hhi,  # 赫芬达尔指数，越小越分散
        "max_concentration": max_concentration,
        "top_industries": dict(sorted(industries.items(), key=lambda x: -x[1])[:5])
        if industries
        else {},
        # 新增: 市值分散度
        "market_cap_mean": float(candidates["market_cap"].mean() / 1e8),
        "market_cap_std": float(candidates["market_cap"].std() / 1e8),
        "market_cap_range": [
            float(candidates["market_cap"].min() / 1e8),
            float(candidates["market_cap"].max() / 1e8),
        ],
        # 新增: 市值集中度（大市值占比）
        "large_cap_ratio": float(
            (candidates["market_cap"] > 500e8).sum() / len(candidates)
        ),  # >500亿
        "small_cap_ratio": float(
            (candidates["market_cap"] < 200e8).sum() / len(candidates)
        ),  # <200亿
    }

    print(f"\n候选池数量:")
    print(f"  候选总数: {metrics['diversification']['candidate_count']}只")
    print(f"  理想范围: 10-20只")
    if metrics["diversification"]["candidate_count"] < 5:
        print(f"    → ❌ 过少，无法有效分散")
    elif metrics["diversification"]["candidate_count"] < 10:
        print(f"    → ⚠️ 偏少，分散不足")
    else:
        print(f"    → ✓ 充足")

    print(f"\n行业分散度:")
    print(f"  行业数量: {metrics['diversification']['num_industries']}")
    print(
        f"  HHI指数: {metrics['diversification']['hhi_index']:.4f} (越小越分散，目标<0.25)"
    )
    print(
        f"  最大集中度: {metrics['diversification']['max_concentration']:.1%} (目标<30%)"
    )
    print(f"  前5行业: {metrics['diversification']['top_industries']}")

    print(f"\n市值分散度:")
    print(f"  市值均值: {metrics['diversification']['market_cap_mean']:.2f}亿")
    print(f"  市值标准差: {metrics['diversification']['market_cap_std']:.2f}亿")
    print(f"  大市值占比(>500亿): {metrics['diversification']['large_cap_ratio']:.1%}")
    print(f"  小市值占比(<200亿): {metrics['diversification']['small_cap_ratio']:.1%}")

    # ========================================
    # 维度五: 风险暴露监控
    # ========================================
    print("\n" + "=" * 70)
    print("【维度五: 风险暴露监控】")
    print("=" * 70)

    # 判断周期性行业
    cyclical_industries = [
        "钢铁",
        "煤炭",
        "有色金属",
        "化工",
        "建筑材料",
        "房地产",
        "银行",
    ]
    cyclical_count = sum(
        industries.get(ind, 0) for ind in cyclical_industries if ind in industries
    )
    cyclical_ratio = cyclical_count / len(candidates) if len(candidates) > 0 else 0

    metrics["risk_exposure"] = {
        # 周期暴露
        "cyclical_industries": cyclical_industries,
        "cyclical_ratio": cyclical_ratio,
        # 新增: 财务风险暴露
        "negative_ocf_count": int((candidates["OCFOA"] < 0).sum()),
        "negative_ocf_ratio": float((candidates["OCFOA"] < 0).sum() / len(candidates)),
        # 新增: 高PE风险
        "high_pe_count": int((candidates["pe_ratio"] > 50).sum()),
        "high_pe_ratio": float((candidates["pe_ratio"] > 50).sum() / len(candidates)),
        # 新增: 极低PB风险（可能价值陷阱）
        "very_low_pb_count": int((candidates["pb_ratio"] < 0.5).sum()),
        "very_low_pb_ratio": float(
            (candidates["pb_ratio"] < 0.5).sum() / len(candidates)
        ),
    }

    print(f"\n周期性暴露:")
    print(f"  周期行业: {cyclical_industries}")
    print(f"  周期占比: {metrics['risk_exposure']['cyclical_ratio']:.1%}")
    if metrics["risk_exposure"]["cyclical_ratio"] > 0.4:
        print(f"    → ⚠️ 周期暴露过高，需警惕周期下行")
    else:
        print(f"    → ✓ 周期风险可控")

    print(f"\n财务风险暴露:")
    print(f"  负OCF数量: {metrics['risk_exposure']['negative_ocf_count']}只")
    print(f"  高PE数量(>50): {metrics['risk_exposure']['high_pe_count']}只")
    print(f"  极低PB数量(<0.5): {metrics['risk_exposure']['very_low_pb_count']}只")

    # ========================================
    # 维度六: 历史对比监控
    # ========================================
    print("\n" + "=" * 70)
    print("【维度六: 历史对比监控】")
    print("=" * 70)

    # 定义历史基准（基于策略回测历史平均值）
    historical_baseline = {
        "count": 12,  # 历史平均候选数
        "pb_mean": 1.0,  # 历史平均PB
        "pe_mean": 15.0,  # 历史平均PE
        "roa_mean": 2.5,  # 历史平均ROA
        "hhi": 0.20,  # 历史平均HHI
        "signal_strength": 0.65,  # 历史信号强度
    }

    metrics["historical_comparison"] = {
        "count_vs_baseline": len(candidates) / historical_baseline["count"],
        "pb_vs_baseline": metrics["valuation"]["pb_mean"]
        / historical_baseline["pb_mean"],
        "pe_vs_baseline": metrics["valuation"]["pe_mean"]
        / historical_baseline["pe_mean"],
        "roa_vs_baseline": metrics["profitability"]["roa_mean"]
        / historical_baseline["roa_mean"],
        "hhi_vs_baseline": metrics["diversification"]["hhi_index"]
        / historical_baseline["hhi"],
        "signal_vs_baseline": metrics["factor_validity"]["signal_strength"]
        / historical_baseline["signal_strength"],
    }

    print(f"\n相对历史基准:")
    print(
        f"  候选数量: {metrics['historical_comparison']['count_vs_baseline']:.2f}x ({len(candidates)}/{historistical_baseline['count']})"
    )
    print(f"  PB均值: {metrics['historical_comparison']['pb_vs_baseline']:.2f}x")
    print(f"  PE均值: {metrics['historical_comparison']['pe_vs_baseline']:.2f}x")
    print(f"  ROA均值: {metrics['historical_comparison']['roa_vs_baseline']:.2f}x")
    print(f"  HHI指数: {metrics['historical_comparison']['hhi_vs_baseline']:.2f}x")
    print(f"  信号强度: {metrics['historical_comparison']['signal_vs_baseline']:.2f}x")

    print(f"\n偏离度分析:")
    for metric_name, ratio in metrics["historical_comparison"].items():
        if ratio < 0.5:
            print(f"  {metric_name}: 严重偏低 ❌")
        elif ratio < 0.8:
            print(f"  {metric_name}: 偏低 ⚠️")
        elif ratio > 1.5:
            print(f"  {metric_name}: 偏高 ⚠️")
        else:
            print(f"  {metric_name}: 正常 ✓")

    # ========================================
    # 综合质量评分 v2.0
    # ========================================
    print("\n" + "=" * 70)
    print("【综合质量评分 v2.0】")
    print("=" * 70)

    score = 100
    deductions = []

    # 估值维度 (权重15%)
    if metrics["valuation"]["pb_mean"] > 1.5:
        score -= 15
        deductions.append("PB均值过高(-15)")
    elif metrics["valuation"]["pb_mean"] > 1.2:
        score -= 5
        deductions.append("PB均值偏高(-5)")

    if metrics["valuation"]["pe_mean"] > 30:
        score -= 10
        deductions.append("PE均值过高(-10)")

    if metrics["valuation"]["pb_skewness"] > 1.0:
        score -= 5
        deductions.append("PB分布异常偏斜(-5)")

    # 盈利维度 (权重25%)
    if metrics["profitability"]["roa_mean"] < 1.0:
        score -= 20
        deductions.append("ROA严重偏低(-20)")
    elif metrics["profitability"]["roa_mean"] < 2.0:
        score -= 10
        deductions.append("ROA偏低(-10)")

    if metrics["profitability"]["roa_ocf_correlation"] < 0.5:
        score -= 10
        deductions.append("盈利现金流不匹配(-10)")

    if metrics["profitability"]["negative_ocf_ratio"] > 0.2:
        score -= 10
        deductions.append("负现金流占比高(-10)")

    # 因子有效性维度 (权重15%)
    if metrics["factor_validity"]["signal_strength"] < 0.4:
        score -= 15
        deductions.append("因子信号严重偏弱(-15)")
    elif metrics["factor_validity"]["signal_strength"] < 0.5:
        score -= 5
        deductions.append("因子信号偏弱(-5)")

    # 分散度维度 (权重20%)
    if metrics["diversification"]["candidate_count"] < 5:
        score -= 20
        deductions.append("候选严重不足(-20)")
    elif metrics["diversification"]["candidate_count"] < 10:
        score -= 10
        deductions.append("候选不足(-10)")

    if metrics["diversification"]["hhi_index"] > 0.40:
        score -= 10
        deductions.append("行业过度集中(-10)")
    elif metrics["diversification"]["hhi_index"] > 0.25:
        score -= 5
        deductions.append("行业集中偏高(-5)")

    # 风险暴露维度 (权重15%)
    if metrics["risk_exposure"]["cyclical_ratio"] > 0.5:
        score -= 15
        deductions.append("周期暴露过高(-15)")
    elif metrics["risk_exposure"]["cyclical_ratio"] > 0.3:
        score -= 5
        deductions.append("周期暴露偏高(-5)")

    if metrics["risk_exposure"]["high_pe_ratio"] > 0.2:
        score -= 5
        deductions.append("高PE风险暴露(-5)")

    # 历史对比维度 (权重10%)
    if metrics["historical_comparison"]["count_vs_baseline"] < 0.3:
        score -= 10
        deductions.append("候选大幅低于历史(-10)")
    if metrics["historical_comparison"]["roa_vs_baseline"] < 0.5:
        score -= 5
        deductions.append("ROA低于历史基准(-5)")

    score = max(0, score)

    if score >= 85:
        grade = "A+"
        assessment = "卓越 - 各维度均优于预期"
    elif score >= 80:
        grade = "A"
        assessment = "优秀 - 组合质量全面符合预期"
    elif score >= 70:
        grade = "B+"
        assessment = "良好+ - 基本符合预期，个别维度待优化"
    elif score >= 60:
        grade = "B"
        assessment = "良好 - 可接受，需关注扣分项"
    elif score >= 50:
        grade = "C+"
        assessment = "一般+ - 存在问题，谨慎操作"
    elif score >= 40:
        grade = "C"
        assessment = "一般 - 明显问题，建议评估"
    else:
        grade = "D"
        assessment = "较差 - 严重偏离，建议暂停"

    print(f"\n质量评分: {score}/100 (等级: {grade})")
    print(f"评估结论: {assessment}")

    if deductions:
        print(f"\n扣分项:")
        for item in deductions:
            print(f"  - {item}")
    else:
        print(f"\n扣分项: 无 ✓")

    # ========================================
    # 风险预警
    # ========================================
    print("\n" + "=" * 70)
    print("【风险预警清单】")
    print("=" * 70)

    warnings = []

    # 严重预警 🔴
    if metrics["diversification"]["candidate_count"] < 3:
        warnings.append("🔴 A01: 候选枯竭 - 建议放宽PB或暂停")
    if metrics["profitability"]["roa_mean"] < 0.5:
        warnings.append("🔴 A03: ROA极低 - 盈利质量严重恶化")
    if metrics["risk_exposure"]["cyclical_ratio"] > 0.6:
        warnings.append("🔴 A04: 周期暴露过高 - 周期下行风险极大")

    # 中度预警 🟡
    if metrics["diversification"]["candidate_count"] < 10:
        warnings.append("🟡 B01: 候选不足 - 建议放宽至PB20%")
    if metrics["profitability"]["roa_mean"] < 1.5:
        warnings.append("🟡 B03: ROA偏低 - 盈利质量偏弱")
    if metrics["diversification"]["hhi_index"] > 0.35:
        warnings.append("🟡 B04: 行业集中 - 分散不足")
    if metrics["risk_exposure"]["cyclical_ratio"] > 0.4:
        warnings.append("🟡 B05: 周期暴露偏高 - 关注周期走势")
    if metrics["profitability"]["roa_ocf_correlation"] < 0.6:
        warnings.append("🟡 B06: 盈利现金流不匹配 - 财务质量存疑")

    # 轻度提醒 🟢
    if metrics["valuation"]["pb_skewness"] > 0.5:
        warnings.append("🟢 C01: PB分布偏斜 - 存在异常值")
    if metrics["factor_validity"]["signal_strength"] < 0.6:
        warnings.append("🟢 C02: 因子信号偏弱 - 部分因子失效")
    if metrics["historical_comparison"]["count_vs_baseline"] < 0.5:
        warnings.append("🟢 C03: 候选低于历史 - 市场环境变化")

    if warnings:
        print(f"\n触发预警 ({len(warnings)}条):")
        for w in warnings:
            print(f"  {w}")
    else:
        print(f"\n触发预警: 无 ✓")

    # ========================================
    # 最终输出
    # ========================================
    print("\n" + "=" * 70)
    print("【监控结果摘要】")
    print("=" * 70)

    print(f"\n✓ 像不像想要的RFScore组合?")
    print(f"  当前组合特征:")
    print(
        f"    - 估值: PB均值{metrics['valuation']['pb_mean']:.3f} {'✓符合' if metrics['valuation']['pb_mean'] < 1.2 else '⚠️偏高'}"
    )
    print(f"    - 质量: RFScore全为7分 ✓")
    print(
        f"    - 盈利: ROA均值{metrics['profitability']['roa_mean']:.2f}% {'✓正常' if metrics['profitability']['roa_mean'] > 2.0 else '⚠️偏低'}"
    )
    print(
        f"    - 分散: {len(candidates)}只候选 {'✓充足' if len(candidates) >= 10 else '⚠️不足'}"
    )
    print(
        f"    - 信号: 综合强度{metrics['factor_validity']['signal_strength']:.2f} {'✓强劲' if metrics['factor_validity']['signal_strength'] > 0.6 else '⚠️偏弱'}"
    )

    print(f"\n结论:")
    if score >= 70:
        print(f"  → 当前组合基本符合RFScore风格，建议正常执行")
    elif score >= 50:
        print(f"  → 当前组合存在偏差，建议适度调整（放宽PB或减仓）")
    else:
        print(f"  → 当前组合严重偏离预期，建议重新评估或暂停")

    # 输出JSON
    print("\n" + "=" * 70)
    print("完整监控数据(JSON):")
    print("=" * 70)

    full_report = {
        "date": str(trade_day),
        "version": "v2.0",
        "score": score,
        "grade": grade,
        "assessment": assessment,
        "deductions": deductions,
        "warnings": warnings,
        "metrics": metrics,
    }

    print(json.dumps(full_report, ensure_ascii=False, indent=2))
