from jqdata import *
from jqfactor import get_factor_values, get_all_factors
import pandas as pd
import numpy as np
import datetime

test_date = datetime.date(2024, 6, 1)
print(f"测试日期: {test_date}")

hs300 = set(get_index_stocks("000300.XSHG", date=test_date))
zz500 = set(get_index_stocks("000905.XSHG", date=test_date))
stocks = list(hs300 | zz500)
stocks = [s for s in stocks if not s.startswith("688")]
print(f"股票池数量: {len(stocks)}")

is_st = get_extras("is_st", stocks, end_date=test_date, count=1).iloc[-1]
stocks = is_st[is_st == False].index.tolist()
print(f"过滤ST后: {len(stocks)}")

val = get_valuation(
    stocks, end_date=test_date, fields=["pb_ratio", "pe_ratio"], count=1
)
val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
val = val[(val["pb_ratio"] > 0) & (val["pe_ratio"] > 0) & (val["pe_ratio"] < 100)]
print(f"估值筛选后: {len(val)}")

print("\n直接获取因子数据...")
factors_to_get = [
    "roa",
    "ocfoa",
    "gross_profit_margin",
    "inc_total_revenue_year_on_year",
]
factor_data = get_factor_values(
    stocks[:100], factors_to_get, end_date=str(test_date), count=1
)

print(f"获取的因子: {list(factor_data.keys())}")
for factor_name, df in factor_data.items():
    print(f"\n{factor_name}:")
    print(df.head(5))

print("\n因子获取成功！")

df = pd.DataFrame(
    {
        "roa": factor_data["roa"].iloc[-1],
        "ocfoa": factor_data["ocfoa"].iloc[-1],
        "gross_profit_margin": factor_data["gross_profit_margin"].iloc[-1],
    }
)
df = df.join(val[["pb_ratio", "pe_ratio"]], how="inner")
df = df[(df["roa"] > 0.5) & (df["pb_ratio"] > 0)]
print(f"\n筛选后股票数: {len(df)}")

df["pb_group"] = (
    pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop")
    + 1
)
primary = df[df["pb_group"] == 1].sort_values("roa", ascending=False)
print(f"\nPB最低10%且ROA>0.5的股票:")
for code in primary.index[:10]:
    name = get_security_info(code).display_name
    print(
        f"  {code} {name} ROA={df.loc[code, 'roa']:.2f} PB={df.loc[code, 'pb_ratio']:.2f}"
    )
