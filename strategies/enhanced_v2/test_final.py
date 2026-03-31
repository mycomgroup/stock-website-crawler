from jqdata import *
from jqfactor import get_factor_values
import pandas as pd
import numpy as np
import datetime

test_date = datetime.date(2024, 6, 1)
print(f"测试日期: {test_date}")
print("=" * 60)

hs300 = set(get_index_stocks("000300.XSHG", date=test_date))
zz500 = set(get_index_stocks("000905.XSHG", date=test_date))
stocks = list(hs300 | zz500)
stocks = [s for s in stocks if not s.startswith("688")]
print(f"股票池数量: {len(stocks)}")

is_st = get_extras("is_st", stocks, end_date=test_date, count=1).iloc[-1]
stocks = is_st[is_st == False].index.tolist()

val = get_valuation(
    stocks, end_date=test_date, fields=["pb_ratio", "pe_ratio"], count=1
)
val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
val = val[(val["pb_ratio"] > 0) & (val["pe_ratio"] > 0) & (val["pe_ratio"] < 100)]
stocks = val.index.tolist()
print(f"估值筛选后: {len(stocks)}")

print("\n获取因子数据...")
factors = [
    "roa_ttm",
    "net_operate_cash_flow_to_asset",
    "gross_income_ratio",
    "operating_revenue_growth_rate",
    "net_profit_growth_rate",
    "debt_to_asset_ratio",
]
factor_data = get_factor_values(stocks, factors, end_date=str(test_date), count=1)

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
df = df.join(val, how="inner")
df = df.dropna()

print(f"因子数据获取成功，股票数: {len(df)}")


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
df = df[df["ROA"] > 0.5]
df["pb_group"] = (
    pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop")
    + 1
)

print(f"\n筛选后 (ROA>0.5): {len(df)}")
print(f"\nRFScore分布:")
print(df["RFScore"].value_counts().sort_index(ascending=False))

primary = df[(df["RFScore"] >= 6) & (df["pb_group"] == 1)].copy()
primary["score"] = (
    primary["RFScore"] * 100
    + primary["ROA"].rank(pct=True) * 30
    + primary["OCFOA"].rank(pct=True) * 20
    - primary["pb_ratio"].rank(pct=True) * 10
)
primary = primary.sort_values("score", ascending=False)

print(f"\nPB最低10% + RFScore>=6的股票 ({len(primary)}只):")
for i, (code, row) in enumerate(primary.head(15).iterrows()):
    name = get_security_info(code).display_name
    industry = (
        get_industry(code, date=test_date)
        .get(code, {})
        .get("sw_l1", {})
        .get("industry_name", "Unknown")
    )
    print(f"  {i + 1}. {code} {name} [{industry}]")
    print(
        f"      RFScore={row['RFScore']} ROA={row['ROA']:.2f} OCFOA={row['OCFOA']:.2f} PB={row['pb_ratio']:.2f}"
    )

print("\n行业分布:")
industries = {}
for code in primary.head(15).index:
    ind = (
        get_industry(code, date=test_date)
        .get(code, {})
        .get("sw_l1", {})
        .get("industry_name", "Unknown")
    )
    industries[ind] = industries.get(ind, 0) + 1
for ind, count in sorted(industries.items(), key=lambda x: -x[1]):
    print(f"  {ind}: {count} ({count / 15:.1%})")

print("\n测试完成！")
