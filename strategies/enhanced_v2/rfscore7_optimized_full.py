from jqdata import *
import pandas as pd
import numpy as np

print("=" * 60)
print("RFScore7 PB10 优化策略 - 完整测试")
print("=" * 60)

test_dates = ["2024-01-01", "2024-06-01", "2025-01-01"]
target_hold_num = 15
industry_cap_ratio = 0.30

all_results = []

for test_date in test_dates:
    print(f"\n{'=' * 60}")
    print(f"测试日期: {test_date}")
    print("=" * 60)

    try:
        print("\n[1/6] 获取股票池...")
        hs300 = get_index_stocks("000300.XSHG", date=test_date)
        zz500 = get_index_stocks("000905.XSHG", date=test_date)
        stocks = list(set(hs300) | set(zz500))
        stocks = [s for s in stocks if not s.startswith("688")]
        print(f"  沪深300+中证500: {len(stocks)}只")

        print("\n[2/6] 过滤ST和停牌...")
        is_st = get_extras("is_st", stocks, end_date=test_date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()
        print(f"  过滤后: {len(stocks)}只")

        print("\n[3/6] 获取估值数据...")
        val = get_valuation(
            stocks, end_date=test_date, count=1, fields=["pb_ratio", "pe_ratio"]
        )
        val = val.drop_duplicates("code").set_index("code")
        val = val[
            (val["pb_ratio"] > 0) & (val["pe_ratio"] > 0) & (val["pe_ratio"] < 100)
        ]
        print(f"  有效数据: {len(val)}只")

        print("\n[4/6] 计算RFScore和综合得分...")
        df = val.copy()
        df["pb_group"] = (
            pd.qcut(
                df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
            )
            + 1
        )

        df["score"] = (
            100
            + df["pe_ratio"].rank(pct=True) * 20
            - df["pb_ratio"].rank(pct=True) * 30
        )

        print(f"\n[5/6] 选股...")
        primary = df[(df["pb_group"] == 1)].sort_values("score", ascending=False)
        print(f"  主池(PB最低10%): {len(primary)}只")

        print(f"\n[6/6] 行业分散选股 (单行业≤{industry_cap_ratio:.0%})...")
        limit_count = max(1, int(target_hold_num * industry_cap_ratio))
        picks = []
        industry_counts = {}

        for code in primary.index:
            if len(picks) >= target_hold_num:
                break
            ind = (
                get_industry(code, date=test_date)
                .get(code, {})
                .get("sw_l1", {})
                .get("industry_name", "Unknown")
            )
            count = industry_counts.get(ind, 0)
            if count < limit_count:
                picks.append(code)
                industry_counts[ind] = count + 1

        print(f"  最终选出: {len(picks)}只")

        print(f"\n选中股票:")
        for i, code in enumerate(picks):
            name = get_security_info(code).display_name
            row = df.loc[code]
            print(
                f"  {i + 1:2d}. {code} {name[:8]:8s} PB={row['pb_ratio']:.2f} PE={row['pe_ratio']:.1f} 得分={row['score']:.1f}"
            )

        print(f"\n行业分布:")
        for ind, count in sorted(industry_counts.items(), key=lambda x: -x[1]):
            ratio = count / len(picks)
            print(f"  {ind}: {count}只 ({ratio:.1%})")

        max_ind_ratio = (
            max(industry_counts.values()) / len(picks) if industry_counts else 0
        )
        print(f"\n最大行业比例: {max_ind_ratio:.1%}")

        all_results.append(
            {
                "date": test_date,
                "total": len(df),
                "selected": len(picks),
                "max_ind_ratio": max_ind_ratio,
                "avg_pb": df.loc[picks, "pb_ratio"].mean() if picks else 0,
                "avg_pe": df.loc[picks, "pe_ratio"].mean() if picks else 0,
                "industries": industry_counts,
            }
        )

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback

        traceback.print_exc()

print("\n" + "=" * 60)
print("汇总统计")
print("=" * 60)
for r in all_results:
    print(f"\n{r['date']}:")
    print(f"  股票池: {r['total']}只")
    print(f"  选中: {r['selected']}只")
    print(f"  平均PB: {r['avg_pb']:.2f}")
    print(f"  平均PE: {r['avg_pe']:.1f}")
    print(f"  最大行业比例: {r['max_ind_ratio']:.1%}")
    top_inds = sorted(r["industries"].items(), key=lambda x: -x[1])[:3]
    print(f"  前三大行业: {', '.join([f'{k}({v})' for k, v in top_inds])}")

print("\n" + "=" * 60)
print("✓ 测试完成")
print("=" * 60)
