from jqdata import *
from jqfactor import get_factor_values
import pandas as pd
import datetime

test_date = datetime.date(2024, 6, 1)
print(f"测试日期: {test_date}")

hs300 = set(get_index_stocks("000300.XSHG", date=test_date))
zz500 = set(get_index_stocks("000905.XSHG", date=test_date))
stocks = list(hs300 | zz500)[:200]
print(f"股票池: {len(stocks)}")

val = get_valuation(
    stocks, end_date=test_date, fields=["pb_ratio", "pe_ratio"], count=1
)
val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
val = val[(val["pb_ratio"] > 0) & (val["pe_ratio"] < 100)]
stocks = val.index.tolist()
print(f"估值筛选后: {len(stocks)}")

factors = ["roa_ttm", "net_operate_cash_flow_to_asset"]
factor_data = get_factor_values(stocks, factors, end_date=str(test_date), count=1)
print(f"因子数据获取成功")

df = pd.DataFrame(
    {
        "ROA": factor_data["roa_ttm"].iloc[-1],
        "OCFOA": factor_data["net_operate_cash_flow_to_asset"].iloc[-1],
    }
)
df = df.join(val, how="inner").dropna()
df = df[df["ROA"] > 0.5]
print(f"ROA>0.5: {len(df)}")

df["pb_group"] = (
    pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop")
    + 1
)
primary = df[df["pb_group"] == 1].sort_values("ROA", ascending=False)

print(f"\nPB最低10%的股票 ({len(primary)}只):")
for i, (code, row) in enumerate(primary.head(10).iterrows()):
    name = get_security_info(code).display_name
    print(f"  {i + 1}. {code} {name} ROA={row['ROA']:.2f} PB={row['pb_ratio']:.2f}")

print("\n测试成功！直接使用因子数据可行。")
