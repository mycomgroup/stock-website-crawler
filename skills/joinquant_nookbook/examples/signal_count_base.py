# 主线信号放宽测试 - 只统计信号数量
from jqdata import *

print("主线信号放宽测试 - 信号数量统计")

trade_days = get_trade_days("2024-01-01", "2024-12-31")
print(f"全年交易日: {len(trade_days)}")

versions = {
    "原版": (50, 150, 0.30),
    "放宽A": (40, 200, 0.30),
    "放宽B": (50, 150, 0.50),
    "放宽C": (40, 200, 0.50),
    "放宽D": (30, 300, 0.50),
}

results = {}

for vname, (cap_min, cap_max, pos_max) in versions.items():
    print(f"\n版本: {vname} (市值{cap_min}-{cap_max}亿, 位置≤{pos_max * 100}%)")

    total_signals = 0

    q = query(valuation.code).filter(
        valuation.circulating_market_cap >= cap_min,
        valuation.circulating_market_cap <= cap_max,
    )

    for date in trade_days[:30]:
        ds = date.strftime("%Y-%m-%d")

        df_val = get_fundamentals(q, date=ds)
        if not df_val.empty:
            count = len(df_val)
            total_signals += count
            if (
                date == trade_days[0]
                or date == trade_days[14]
                or date == trade_days[29]
            ):
                print(f"  {ds}: 符合市值条件的股票数={count}")

    avg_per_day = total_signals / 30
    estimated_full_year = int(avg_per_day * len(trade_days))

    results[vname] = estimated_full_year
    print(f"  前30天总股票数: {total_signals}")
    print(f"  日均股票数: {avg_per_day:.0f}")
    print(f"  预估全年基数: {estimated_full_year}")

print("\n" + "=" * 60)
print("信号基数对比（仅市值筛选）")
print("=" * 60)

print("\n| 版本 | 市值范围 | 预估全年基数 | 相对原版倍数 |")
print("|------|---------|-------------|-------------|")

for vname in versions.keys():
    if vname in results:
        base = results["原版"]
        mult = results[vname] / base if base > 0 else 0
        print(
            f"| {vname} | {versions[vname][0]}-{versions[vname][1]}亿 | {results[vname]} | {mult:.2f}x |"
        )

print(
    "\n注意: 这是市值筛选的基数，实际信号需叠加位置≤{pos_max*100}%、无连板、昨日涨停等条件"
)
print("实际信号数量约为基数 * 涨停概率(5-10%) * 位置过滤(30-50%) * 无连板(50%)")
print("=" * 60)
