from jqdata import *
import pandas as pd

print("=" * 60)
print("RFScore7 PB10 选股测试")
print("=" * 60)

test_date = "2024-06-01"
print(f"\n日期: {test_date}")

try:
    print("\n[1/5] 获取股票池...")
    stocks = get_index_stocks("000300.XSHG", date=test_date)
    print(f"  沪深300: {len(stocks)}只")

    print("\n[2/5] 获取估值数据...")
    val = get_valuation(
        stocks[:100], end_date=test_date, count=1, fields=["pb_ratio", "pe_ratio"]
    )
    if not val.empty:
        val = val.drop_duplicates("code").set_index("code")
        val = val[
            (val["pb_ratio"] > 0) & (val["pe_ratio"] > 0) & (val["pe_ratio"] < 100)
        ]
        print(f"  有效数据: {len(val)}只")
    else:
        print("  无数据，使用替代方案")
        val = pd.DataFrame()

    print("\n[3/5] 计算RFScore...")
    print("  (简化版，使用市值排序)")

    if not val.empty:
        val["pb_group"] = (
            pd.qcut(
                val["pb_ratio"].rank(method="first"),
                10,
                labels=False,
                duplicates="drop",
            )
            + 1
        )
        picks = val[val["pb_group"] == 1].sort_values("pb_ratio").head(15)

        print(f"\n[4/5] 选出股票 ({len(picks)}只):")
        for i, (code, row) in enumerate(picks.iterrows()):
            name = get_security_info(code).display_name
            print(
                f"  {i + 1:2d}. {code} {name[:8]:8s} PB={row['pb_ratio']:.2f} PE={row['pe_ratio']:.1f}"
            )

        print(f"\n[5/5] 行业分布:")
        industries = {}
        for code in picks.index[:10]:
            ind = (
                get_industry(code, date=test_date)
                .get(code, {})
                .get("sw_l1", {})
                .get("industry_name", "Unknown")
            )
            industries[ind] = industries.get(ind, 0) + 1
        for ind, count in sorted(industries.items(), key=lambda x: -x[1])[:5]:
            print(f"  {ind}: {count}只")
    else:
        print("  无数据")

    print("\n" + "=" * 60)
    print("✓ 测试完成")
    print("=" * 60)

except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback

    traceback.print_exc()
