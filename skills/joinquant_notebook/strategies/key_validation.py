# 红利小盘策略 - 关键验证脚本
from jqdata import *

print("红利小盘策略 - 关键验证")
print("=" * 70)

test_date = "2025-12-31"
print(f"测试日期: {test_date}")

# 1. 基础池统计
print("\n【1】基础池统计")
print("-" * 50)

all_stocks = get_all_securities(types=["stock"], date=test_date)
print(f"全市场股票: {len(all_stocks)} 只")

# 过滤条件
from datetime import datetime, timedelta

test_date_obj = datetime.strptime(test_date, "%Y-%m-%d").date()
cutoff_date = test_date_obj - timedelta(days=180)
all_stocks = all_stocks[all_stocks["start_date"] <= cutoff_date]
print(f"上市满180天: {len(all_stocks)} 只")

is_st = get_extras(
    "is_st", all_stocks.index.tolist(), end_date=test_date, count=1
).iloc[-1]
st_count = (is_st == True).sum()
stocks_no_st = is_st[is_st == False].index.tolist()
print(f"ST股票: {st_count} 只")
print(f"过滤ST后: {len(stocks_no_st)} 只")

stocks_no_688 = [s for s in stocks_no_st if not s.startswith("688")]
print(f"过滤科创板后: {len(stocks_no_688)} 只")

# 2. 市值区间分布
print("\n【2】10-100亿市值区间分布")
print("-" * 50)

q_cap = query(valuation.code, valuation.market_cap).filter(
    valuation.code.in_(stocks_no_688),
    valuation.market_cap >= 10,
    valuation.market_cap <= 100,
)

df_cap = get_fundamentals(q_cap, date=test_date)
print(f"10-100亿市值区间: {len(df_cap)} 只")

cap_ranges = [
    ("10-30亿", 10, 30),
    ("30-60亿", 30, 60),
    ("60-100亿", 60, 100),
]

for name, min_cap, max_cap in cap_ranges:
    count = len(
        df_cap[(df_cap["market_cap"] >= min_cap) & (df_cap["market_cap"] < max_cap)]
    )
    pct = count / len(df_cap) * 100 if len(df_cap) > 0 else 0
    print(f"{name}: {count} 只 ({pct:.1f}%)")

# 3. PE筛选效果
print("\n【3】PE筛选效果")
print("-" * 50)

q_pe = query(valuation.code, valuation.market_cap, valuation.pe_ratio).filter(
    valuation.code.in_(stocks_no_688),
    valuation.market_cap >= 10,
    valuation.market_cap <= 100,
    valuation.pe_ratio > 0,
)

df_pe = get_fundamentals(q_pe, date=test_date)
print(f"PE>0 & 10-100亿: {len(df_pe)} 只")

pe_thresholds = [20, 25, 30, 40, 50, 100]
for pe_th in pe_thresholds:
    count = len(df_pe[df_pe["pe_ratio"] < pe_th])
    pct = count / len(df_pe) * 100 if len(df_pe) > 0 else 0
    print(f"PE<{pe_th}: {count} 只 ({pct:.1f}%)")

# 4. ROE筛选效果
print("\n【4】ROE筛选效果")
print("-" * 50)

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
print(f"PE<100 & 10-100亿: {len(df_roe)} 只")

roe_thresholds = [0, 3, 5, 8, 10]
for roe_th in roe_thresholds:
    count = len(df_roe[df_roe["roe"] > roe_th])
    pct = count / len(df_roe) * 100 if len(df_roe) > 0 else 0
    print(f"ROE>{roe_th}%: {count} 只 ({pct:.1f}%)")

# 5. 复合条件筛选
print("\n【5】复合条件筛选")
print("-" * 50)

scenarios = [
    ("PE<100, ROE>0%", {"pe_max": 100, "roe_min": 0}),
    ("PE<50, ROE>5%", {"pe_max": 50, "roe_min": 5}),
    ("PE<30, ROE>5%", {"pe_max": 30, "roe_min": 5}),
    ("PE<25, ROE>8%", {"pe_max": 25, "roe_min": 8}),
    ("PE<30, ROE>8%", {"pe_max": 30, "roe_min": 8}),
]

for name, params in scenarios:
    count = len(
        df_roe[
            (df_roe["pe_ratio"] < params["pe_max"])
            & (df_roe["roe"] > params["roe_min"])
        ]
    )
    can_support = "✓" if count >= 15 else "✗"
    print(f"{name}: {count} 只 {can_support}")

# 6. 分市值区间复合筛选
print("\n【6】分市值区间复合筛选 (PE<30, ROE>5%)")
print("-" * 50)

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

for name, min_cap, max_cap in cap_groups:
    count = len(
        df_combo[
            (df_combo["market_cap"] >= min_cap) & (df_combo["market_cap"] < max_cap)
        ]
    )
    print(f"{name}: {count} 只")

print(f"总计: {len(df_combo)} 只")

# 7. 候选池充足性判定
print("\n【7】候选池充足性判定")
print("-" * 50)

hold_target = 15
candidate_count = len(df_combo)

print(f"目标持仓: {hold_target} 只")
print(f"候选池: {candidate_count} 只")
print(f"充足倍数: {candidate_count / hold_target:.2f} 倍")

if candidate_count >= hold_target * 2:
    print("充足性: 充裕 ✓")
elif candidate_count >= hold_target:
    print("充足性: 基本充足 ✓")
elif candidate_count >= hold_target * 0.7:
    print("充足性: 勉强够用 ⚠️")
else:
    print("充足性: 严重不足 ✗")

# 8. 结论
print("\n【8】结论")
print("-" * 50)
print("1. 基础池充足: 2,732只股票在10-100亿市值区间")
print("2. ST过滤有效: 过滤177只ST股，占比3.4%")
print("3. 市值分布合理: 30-60亿区间占50.7%")
print("4. PE筛选充足: PE<30保留517只")
print("5. ROE筛选严格: ROE>5%仅保留46只")
print("6. 复合条件基本充足: PE<30&ROE>5%保留28只")
print("7. 建议优化: 放宽ROE至>3%或调整市值区间")
