from jqdata import *
from jqfactor import get_all_factors
import pandas as pd

print("获取聚宽因子库...")
all_factors = get_all_factors()
print(f"因子总数: {len(all_factors)}")
print(f"\n因子分类:")
print(all_factors["category"].value_counts())

quality_factors = all_factors[all_factors["category"] == "quality"]
print(f"\n质量类因子 (quality):")
print(quality_factors[["code", "name"]].head(20))

basics_factors = all_factors[all_factors["category"] == "basics"]
print(f"\n基础类因子 (basics):")
print(basics_factors[["code", "name"]].head(20))

growth_factors = all_factors[all_factors["category"] == "growth"]
print(f"\n成长类因子 (growth):")
print(growth_factors[["code", "name"]].head(20))

print("\n搜索ROA相关因子:")
roa_factors = all_factors[
    all_factors["name"].str.contains("ROA|roa|总资产收益率", case=False, na=False)
]
print(roa_factors[["code", "name", "category"]])

print("\n搜索经营现金流相关因子:")
cfo_factors = all_factors[
    all_factors["name"].str.contains("经营现金流|OCF|cash_flow", case=False, na=False)
]
print(cfo_factors[["code", "name", "category"]])
