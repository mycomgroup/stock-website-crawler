from jqdata import *
from jqfactor import get_factor_values
import pandas as pd
import numpy as np
import datetime

print("=" * 60)
print("RFScore7 PB10 优化策略 - Notebook 回测")
print("=" * 60)

test_dates = ["2024-01-01", "2024-06-01", "2025-01-01"]
target_hold_num = 15

results = []

for test_date in test_dates:
    print(f"\n测试日期: {test_date}")
    print("-" * 40)

    try:
        hs300 = set(get_index_stocks("000300.XSHG", date=test_date))
        zz500 = set(get_index_stocks("000905.XSHG", date=test_date))
        stocks = list(hs300 | zz500)
        stocks = [s for s in stocks if not s.startswith("688")]
        print(f"初始股票池: {len(stocks)}")

        is_st = get_extras("is_st", stocks, end_date=test_date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()
        print(f"过滤ST后: {len(stocks)}")

        val = get_valuation(
            stocks, end_date=test_date, fields=["pb_ratio", "pe_ratio"], count=1
        )
        val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
        val = val[
            (val["pb_ratio"] > 0) & (val["pe_ratio"] > 0) & (val["pe_ratio"] < 100)
        ]
        stocks = val.index.tolist()
        print(f"估值筛选后: {len(stocks)}")

        print("获取因子数据...")
        factors = [
            "roa_ttm",
            "net_operate_cash_flow_to_asset",
            "gross_income_ratio",
            "operating_revenue_growth_rate",
            "net_profit_growth_rate",
            "debt_to_asset_ratio",
        ]

        factor_data = get_factor_values(stocks, factors, end_date=test_date, count=1)
        print("因子数据获取成功")

        df = pd.DataFrame(
            {
                "ROA": factor_data["roa_ttm"].iloc[-1],
                "OCFOA": factor_data["net_operate_cash_flow_to_asset"].iloc[-1],
                "GrossMargin": factor_data["gross_income_ratio"].iloc[-1],
                "RevenueGrowth": factor_data["operating_revenue_growth_rate"].iloc[-1],
                "ProfitGrowth": factor_data["net_profit_growth_rate"].iloc[-1],
                "DebtRatio": factor_data["debt_to_asset_ratio"].iloc[-1],
            }
        )
        df = df.join(val, how="inner").dropna()
        df = df[df["ROA"] > 0.5]
        print(f"ROA>0.5筛选后: {len(df)}")

        def calc_rfscore(row):
            score = 0
            if row["ROA"] > 0:
                score += 1
            if row["RevenueGrowth"] > 0:
                score += 1
            if row["OCFOA"] > 0:
                score += 1
            if row["OCFOA"] > row["ROA"]:
                score += 1
            if row["ProfitGrowth"] > 0:
                score += 1
            if row["GrossMargin"] > 0:
                score += 1
            if row["DebtRatio"] < 0.5:
                score += 1
            return score

        df["RFScore"] = df.apply(calc_rfscore, axis=1)
        df["pb_group"] = (
            pd.qcut(
                df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
            )
            + 1
        )

        primary = df[(df["RFScore"] >= 6) & (df["pb_group"] == 1)].copy()
        primary["score"] = (
            primary["RFScore"] * 100
            + primary["ROA"].rank(pct=True) * 30
            + primary["OCFOA"].rank(pct=True) * 20
            - primary["pb_ratio"].rank(pct=True) * 10
        )
        primary = primary.sort_values("score", ascending=False)

        print(f"\n选出股票数: {len(primary)}")
        print(
            f"RFScore分布:\n{df['RFScore'].value_counts().sort_index(ascending=False).head()}"
        )

        picks = primary.head(target_hold_num)
        print(f"\n最终持仓 ({len(picks)}只):")

        industries = {}
        for i, (code, row) in enumerate(picks.iterrows()):
            name = get_security_info(code).display_name
            ind = (
                get_industry(code, date=test_date)
                .get(code, {})
                .get("sw_l1", {})
                .get("industry_name", "Unknown")
            )
            industries[ind] = industries.get(ind, 0) + 1
            print(
                f"  {i + 1}. {code} {name[:8]:8s} [{ind:6s}] RFScore={row['RFScore']} ROA={row['ROA']:.2f} PB={row['pb_ratio']:.2f}"
            )

        max_ind_ratio = max(industries.values()) / len(picks) if industries else 0
        print(f"\n行业分布:")
        for ind, count in sorted(industries.items(), key=lambda x: -x[1]):
            print(f"  {ind}: {count} ({count / len(picks):.1%})")
        print(f"最大行业比例: {max_ind_ratio:.1%}")

        results.append(
            {
                "date": test_date,
                "total_stocks": len(df),
                "selected": len(picks),
                "max_ind_ratio": max_ind_ratio,
                "avg_roa": picks["ROA"].mean(),
                "avg_pb": picks["pb_ratio"].mean(),
            }
        )

    except Exception as e:
        print(f"错误: {e}")
        import traceback

        traceback.print_exc()

print("\n" + "=" * 60)
print("测试汇总")
print("=" * 60)
for r in results:
    print(
        f"日期: {r['date']}, 选出: {r['selected']}, 最大行业比例: {r['max_ind_ratio']:.1%}, 平均ROA: {r['avg_roa']:.2f}, 平均PB: {r['avg_pb']:.2f}"
    )

print("\n测试完成！")
