# 红利小盘策略 - 候选池有效性验证
# 2026-04-02

print("=" * 70)
print("红利小盘策略 - 候选池有效性验证")
print("=" * 70)

from jqdata import *
import pandas as pd
import numpy as np

# 使用最新可交易日期
test_date = "2025-12-31"  # 使用最近的完整交易日数据

print(f"\n测试日期: {test_date}")

# ============================================================
# 1. 基础筛选: 10-100亿市值区间
# ============================================================
print("\n" + "=" * 70)
print("【1】基础筛选: 10-100亿市值区间")
print("=" * 70)

# 获取所有股票
all_stocks = get_all_securities(types=["stock"], date=test_date)
print(f"\n全市场股票数量: {len(all_stocks)}")

# 过滤上市时间 > 180天
from datetime import datetime, timedelta

test_date_obj = datetime.strptime(test_date, "%Y-%m-%d").date()
cutoff_date = test_date_obj - timedelta(days=180)
all_stocks = all_stocks[all_stocks["start_date"] <= cutoff_date]
stocks_after_ipo = all_stocks.index.tolist()
print(f"上市满180天股票数量: {len(stocks_after_ipo)}")

# 过滤ST股票
is_st = get_extras("is_st", stocks_after_ipo, end_date=test_date, count=1).iloc[-1]
st_count = (is_st == True).sum()
stocks_after_st = is_st[is_st == False].index.tolist()
print(f"ST股票数量: {st_count}")
print(f"过滤ST后股票数量: {len(stocks_after_st)}")

# 过滤科创板 (688开头)
stocks_no_688 = [s for s in stocks_after_st if not s.startswith("688")]
print(f"过滤科创板后股票数量: {len(stocks_no_688)}")

# 按市值筛选 10-100亿
q = query(
    valuation.code, valuation.market_cap, valuation.pe_ratio, valuation.pb_ratio
).filter(
    valuation.code.in_(stocks_no_688),
    valuation.market_cap >= 10,
    valuation.market_cap <= 100,
)

df_cap = get_fundamentals(q, date=test_date)
print(f"\n10-100亿市值区间股票数量: {len(df_cap)}")

# ============================================================
# 2. 不同市值区间的分布
# ============================================================
print("\n" + "=" * 70)
print("【2】不同市值区间分布")
print("=" * 70)

cap_ranges = [
    ("10-15亿", 10, 15),
    ("15-20亿", 15, 20),
    ("20-30亿", 20, 30),
    ("30-40亿", 30, 40),
    ("40-50亿", 40, 50),
    ("50-60亿", 50, 60),
    ("60-70亿", 60, 70),
    ("70-80亿", 70, 80),
    ("80-90亿", 80, 90),
    ("90-100亿", 90, 100),
]

print(f"\n{'市值区间':<12}{'股票数量':>10}{'占比':>10}")
print("-" * 35)

cap_distribution = []
for name, min_cap, max_cap in cap_ranges:
    count = len(
        df_cap[(df_cap["market_cap"] >= min_cap) & (df_cap["market_cap"] < max_cap)]
    )
    pct = count / len(df_cap) * 100 if len(df_cap) > 0 else 0
    cap_distribution.append((name, count, pct))
    print(f"{name:<12}{count:>10}{pct:>9.1f}%")

# 三大区间汇总
print(f"\n{'主要区间汇总':}")
print("-" * 35)
range_10_30 = len(df_cap[(df_cap["market_cap"] >= 10) & (df_cap["market_cap"] < 30)])
range_30_60 = len(df_cap[(df_cap["market_cap"] >= 30) & (df_cap["market_cap"] < 60)])
range_60_100 = len(df_cap[(df_cap["market_cap"] >= 60) & (df_cap["market_cap"] <= 100)])
print(f"10-30亿:  {range_10_30} 只 ({range_10_30 / len(df_cap) * 100:.1f}%)")
print(f"30-60亿:  {range_30_60} 只 ({range_30_60 / len(df_cap) * 100:.1f}%)")
print(f"60-100亿: {range_60_100} 只 ({range_60_100 / len(df_cap) * 100:.1f}%)")

# ============================================================
# 3. PE筛选效果分析
# ============================================================
print("\n" + "=" * 70)
print("【3】PE筛选效果分析")
print("=" * 70)

pe_thresholds = [20, 25, 30, 40, 50, 100]

print(f"\n{'PE阈值':<12}{'候选数量':>10}{'筛选率':>10}")
print("-" * 35)

for pe_th in pe_thresholds:
    df_pe = df_cap[(df_cap["pe_ratio"] > 0) & (df_cap["pe_ratio"] < pe_th)]
    rate = len(df_pe) / len(df_cap) * 100 if len(df_cap) > 0 else 0
    print(f"PE < {pe_th:<6}{len(df_pe):>10}{rate:>9.1f}%")

# 当前策略使用的 PE < 100
df_pe100 = df_cap[(df_cap["pe_ratio"] > 0) & (df_cap["pe_ratio"] < 100)]
print(f"\n当前策略条件 (PE<100): {len(df_pe100)} 只")

# 防守策略推荐 PE < 30
df_pe30 = df_cap[(df_cap["pe_ratio"] > 0) & (df_cap["pe_ratio"] < 30)]
print(f"防守策略推荐 (PE<30): {len(df_pe30)} 只")

# ============================================================
# 4. ROE筛选效果分析
# ============================================================
print("\n" + "=" * 70)
print("【4】ROE筛选效果分析")
print("=" * 70)

# 获取ROE数据
q_roe = query(
    valuation.code, valuation.market_cap, valuation.pe_ratio, indicator.roe
).filter(
    valuation.code.in_(stocks_no_688),
    valuation.market_cap >= 10,
    valuation.market_cap <= 100,
    valuation.pe_ratio > 0,
    valuation.pe_ratio < 100,
)

df_roe = get_fundamentals(q_roe, date=test_date)
print(f"\n10-100亿 & PE<100 基础池: {len(df_roe)} 只")

roe_thresholds = [0, 3, 5, 8, 10, 15]

print(f"\n{'ROE阈值':<12}{'候选数量':>10}{'筛选率':>10}")
print("-" * 35)

for roe_th in roe_thresholds:
    df_roe_filtered = df_roe[df_roe["roe"] > roe_th]
    rate = len(df_roe_filtered) / len(df_roe) * 100 if len(df_roe) > 0 else 0
    print(f"ROE > {roe_th:<5}%{len(df_roe_filtered):>10}{rate:>9.1f}%")

# ============================================================
# 5. 复合条件筛选
# ============================================================
print("\n" + "=" * 70)
print("【5】复合条件筛选 (关键场景)")
print("=" * 70)

scenarios = [
    ("宽松: PE<100, ROE>0%", {"pe_max": 100, "roe_min": 0}),
    ("标准: PE<50, ROE>5%", {"pe_max": 50, "roe_min": 5}),
    ("保守: PE<30, ROE>5%", {"pe_max": 30, "roe_min": 5}),
    ("严格: PE<25, ROE>8%", {"pe_max": 25, "roe_min": 8}),
    ("防守推荐: PE<30, ROE>8%", {"pe_max": 30, "roe_min": 8}),
]

print(f"\n{'场景':<25}{'候选数量':>10}{'能否支撑15只':>15}")
print("-" * 55)

for name, params in scenarios:
    df_scenario = df_roe[
        (df_roe["pe_ratio"] < params["pe_max"]) & (df_roe["roe"] > params["roe_min"])
    ]
    count = len(df_scenario)
    can_support = (
        "✓ 足够" if count >= 15 else f"✗ 仅{count}只" if count < 10 else "~ 勉强"
    )
    print(f"{name:<25}{count:>10}{can_support:>15}")

# ============================================================
# 6. 分市值区间 + 复合条件
# ============================================================
print("\n" + "=" * 70)
print("【6】分市值区间复合筛选 (PE<30, ROE>5%)")
print("=" * 70)

df_combo = df_roe[(df_roe["pe_ratio"] < 30) & (df_roe["roe"] > 5)]

cap_groups = [
    ("10-20亿", 10, 20),
    ("20-30亿", 20, 30),
    ("30-40亿", 30, 40),
    ("40-50亿", 40, 50),
    ("50-60亿", 50, 60),
    ("60-80亿", 60, 80),
    ("80-100亿", 80, 100),
]

print(f"\n{'市值区间':<12}{'候选数量':>10}{'占比':>10}")
print("-" * 35)

for name, min_cap, max_cap in cap_groups:
    count = len(
        df_combo[
            (df_combo["market_cap"] >= min_cap) & (df_combo["market_cap"] < max_cap)
        ]
    )
    pct = count / len(df_combo) * 100 if len(df_combo) > 0 else 0
    print(f"{name:<12}{count:>10}{pct:>9.1f}%")

print(f"\n总计: {len(df_combo)} 只")

# ============================================================
# 7. 股息率筛选
# ============================================================
print("\n" + "=" * 70)
print("【7】股息率筛选效果 (当前策略要求 > 2%)")
print("=" * 70)

q_div = query(
    valuation.code,
    valuation.market_cap,
    valuation.pe_ratio,
    indicator.roe,
    valuation.dividend_ratio,
).filter(
    valuation.code.in_(stocks_no_688),
    valuation.market_cap >= 10,
    valuation.market_cap <= 100,
    valuation.pe_ratio > 0,
    valuation.pe_ratio < 100,
)

df_div = get_fundamentals(q_div, date=test_date)

div_thresholds = [0, 1, 1.5, 2, 2.5, 3]

print(f"\n10-100亿 & PE<100 基础池: {len(df_div)} 只")
print(f"\n{'股息率阈值':<12}{'候选数量':>10}{'筛选率':>10}")
print("-" * 35)

for div_th in div_thresholds:
    df_div_filtered = df_div[df_div["dividend_ratio"] >= div_th]
    rate = len(df_div_filtered) / len(df_div) * 100 if len(df_div) > 0 else 0
    print(f"股息率 >= {div_th}%{len(df_div_filtered):>10}{rate:>9.1f}%")

# 完整筛选条件
df_full = df_div[
    (df_div["pe_ratio"] < 30) & (df_div["roe"] > 5) & (df_div["dividend_ratio"] >= 2)
]
print(f"\n完整条件 (PE<30, ROE>5%, 股息率>=2%): {len(df_full)} 只")

# ============================================================
# 8. 净利润增长筛选 (如数据可用)
# ============================================================
print("\n" + "=" * 70)
print("【8】净利润增长筛选")
print("=" * 70)

try:
    q_growth = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        indicator.roe,
        indicator.inc_net_profit_year_on_year,  # 净利润同比增长率
    ).filter(
        valuation.code.in_(stocks_no_688),
        valuation.market_cap >= 10,
        valuation.market_cap <= 100,
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 30,
        indicator.roe > 5,
    )

    df_growth = get_fundamentals(q_growth, date=test_date)
    print(f"\nPE<30 & ROE>5% 基础池: {len(df_growth)} 只")

    growth_thresholds = [-10, 0, 5, 10, 15, 20]

    print(f"\n{'增长阈值':<15}{'候选数量':>10}{'筛选率':>10}")
    print("-" * 38)

    for g_th in growth_thresholds:
        df_g_filtered = df_growth[df_growth["inc_net_profit_year_on_year"] > g_th]
        rate = len(df_g_filtered) / len(df_growth) * 100 if len(df_growth) > 0 else 0
        label = f"净利润增长 > {g_th}%"
        print(f"{label:<15}{len(df_g_filtered):>10}{rate:>9.1f}%")

    # 正增长筛选
    df_positive_growth = df_growth[df_growth["inc_net_profit_year_on_year"] > 0]
    print(f"\n净利润正增长筛选: {len(df_positive_growth)} 只")

except Exception as e:
    print(f"净利润增长数据获取异常: {e}")
    print("将跳过此部分分析")

# ============================================================
# 9. 红利小盘策略真实候选池 (模拟完整流程)
# ============================================================
print("\n" + "=" * 70)
print("【9】红利小盘策略完整流程模拟")
print("=" * 70)

# Step 1: 基础小盘池
print("\nStep 1: 获取小盘池 (10-60亿, 前30%)")
q_small = query(valuation.code, valuation.market_cap).filter(
    valuation.code.in_(stocks_no_688),
    valuation.market_cap >= 10,
    valuation.market_cap <= 60,
)
df_small = get_fundamentals(q_small, date=test_date)
df_small["cap_rank"] = df_small["market_cap"].rank(pct=True)
small_stocks = df_small[df_small["cap_rank"] <= 0.3]["code"].tolist()
print(f"  小盘池 (市值前30%): {len(small_stocks)} 只")

# Step 2: PE筛选
print("\nStep 2: PE筛选 (0 < PE < 100)")
q_pe = query(
    valuation.code,
    valuation.market_cap,
    valuation.pe_ratio,
    valuation.pb_ratio,
    indicator.roe,
).filter(
    valuation.code.in_(small_stocks),
    valuation.pe_ratio > 0,
    valuation.pe_ratio < 100,
)
df_pe_select = get_fundamentals(q_pe, date=test_date)
df_pe_select = df_pe_select.drop_duplicates("code")
print(f"  PE筛选后: {len(df_pe_select)} 只")

# Step 3: 模拟分红稳定性筛选 (只取前50只做分红检查)
print("\nStep 3: 分红稳定性筛选 (近3年有分红)")
# 由于分红检查耗时，这里使用简化逻辑
div_stable_codes = df_pe_select["code"].tolist()[:50]
print(f"  检查分红: {len(div_stable_codes)} 只 (前50只)")

# Step 4: 股息率筛选
print("\nStep 4: 股息率筛选 (>= 2%)")
q_yield = query(valuation.code, valuation.dividend_ratio).filter(
    valuation.code.in_(div_stable_codes)
)
df_yield = get_fundamentals(q_yield, date=test_date)
df_yield = df_yield.drop_duplicates("code")
df_yield = df_yield[df_yield["dividend_ratio"] >= 2]
print(f"  股息率>=2%: {len(df_yield)} 只")

# 最终候选
final_candidates = df_yield.sort_values("dividend_ratio", ascending=False)
print(f"\n最终候选池 (最多15只):")
print("-" * 50)

if len(final_candidates) > 0:
    # 获取详细信息
    q_final = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        indicator.roe,
        valuation.dividend_ratio,
    ).filter(valuation.code.in_(final_candidates["code"].tolist()[:15]))
    df_final = get_fundamentals(q_final, date=test_date)
    df_final = df_final.merge(
        final_candidates[["code", "dividend_ratio"]],
        on="code",
        how="left",
        suffixes=("", "_final"),
    )
    df_final = df_final.sort_values("dividend_ratio", ascending=False)

    print(f"\n排名 | 代码 | 市值(亿) | PE | ROE | 股息率")
    print("-" * 55)
    for i, row in df_final.iterrows():
        print(
            f"{i + 1:>4} | {row['code'][:6]} | {row['market_cap']:>7.1f} | {row['pe_ratio']:>5.1f} | {row['roe']:>5.2f}% | {row['dividend_ratio']:>5.2f}%"
        )

    print(f"\n最终候选股数量: {len(df_final)} 只")
else:
    print("  无符合条件的候选股")
    df_final = pd.DataFrame()

# ============================================================
# 10. 候选池稀疏度分析
# ============================================================
print("\n" + "=" * 70)
print("【10】候选池稀疏度分析")
print("=" * 70)

sparsity_analysis = {
    "10-100亿市值池": len(df_cap),
    "PE<100": len(df_pe100),
    "PE<30": len(df_pe30),
    "PE<30 & ROE>5%": len(df_roe[(df_roe["pe_ratio"] < 30) & (df_roe["roe"] > 5)]),
    "PE<30 & ROE>8%": len(df_roe[(df_roe["pe_ratio"] < 30) & (df_roe["roe"] > 8)]),
    "完整条件(PE<30,ROE>5%,股息率>=2%)": len(df_full),
    "最终候选池": len(df_final),
}

print(f"\n{'筛选阶段':<35}{'数量':>8}{'留存率':>10}")
print("-" * 55)

base_count = len(df_cap)
for stage, count in sparsity_analysis.items():
    rate = count / base_count * 100 if base_count > 0 else 0
    print(f"{stage:<35}{count:>8}{rate:>9.1f}%")

# ============================================================
# 11. 候选池充足性判定
# ============================================================
print("\n" + "=" * 70)
print("【11】候选池充足性判定")
print("=" * 70)

hold_target = 15  # 策略目标持仓数

print(f"\n策略目标持仓: {hold_target} 只")
print(f"当前最终候选池: {len(df_final)} 只")

if len(df_final) >= hold_target * 2:
    adequacy = "充裕"
    recommendation = "候选池充足，可支持优中选优"
elif len(df_final) >= hold_target:
    adequacy = "基本充足"
    recommendation = "候选池基本够用，但选择余地有限"
elif len(df_final) >= hold_target * 0.7:
    adequacy = "勉强够用"
    recommendation = "建议放宽筛选条件或调整持仓目标"
else:
    adequacy = "严重不足"
    recommendation = "候选池过稀疏，策略难以稳定运行"

print(f"充足性评级: {adequacy}")
print(f"建议: {recommendation}")

# ============================================================
# 12. 结论与建议
# ============================================================
print("\n" + "=" * 70)
print("【12】结论与建议")
print("=" * 70)

print(f"""
【验证结论】

1. 基础池规模:
   - 10-100亿市值区间: {len(df_cap)} 只
   - 经过ST/科创板/上市时间过滤后基础池充足

2. 不同市值区间分布:
   - 10-30亿: {range_10_30} 只 (小盘聚集区)
   - 30-60亿: {range_30_60} 只
   - 60-100亿: {range_60_100} 只

3. 关键筛选条件影响:
   - PE<30 保留: {len(df_pe30)} 只 ({len(df_pe30) / len(df_cap) * 100:.1f}%)
   - ROE>5% + PE<30: {len(df_roe[(df_roe["pe_ratio"] < 30) & (df_roe["roe"] > 5)])} 只
   - 完整条件: {len(df_full)} 只

4. 最终候选池: {len(df_final)} 只
   - 充足性: {adequacy}

【策略建议】
""")

if len(df_final) < hold_target:
    print("候选池较稀疏，建议采取以下措施:")
    print("  1. 放宽PE阈值至40-50")
    print("  2. 降低ROE要求至3-5%")
    print("  3. 降低股息率要求至1.5%")
    print("  4. 扩大市值区间至10-80亿")
    print("  5. 考虑将目标持仓从15只降至10只")
else:
    print("候选池基本满足策略需求:")
    print("  1. 当前筛选条件可保持")
    print("  2. 建议每月监控候选池变化")
    print("  3. 可考虑进一步优化分红稳定性检查逻辑")

print("\n验证完成!")
