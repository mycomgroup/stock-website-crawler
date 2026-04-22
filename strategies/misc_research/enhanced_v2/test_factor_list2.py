from jqdata import *
from jqfactor import get_all_factors
import pandas as pd

print("获取聚宽因子库...")
all_factors = get_all_factors()
print(f"因子总数: {len(all_factors)}")
print(f"\n因子表列名: {all_factors.columns.tolist()}")
print(f"\n因子表前10行:")
print(all_factors.head(10))

print("\n质量类因子 (quality):")
quality_factors = all_factors[all_factors["category"] == "quality"]
print(quality_factors.head(20))

print("\n基础类因子 (basics):")
basics_factors = all_factors[all_factors["category"] == "basics"]
print(basics_factors.head(20))

print("\n成长类因子 (growth):")
growth_factors = all_factors[all_factors["category"] == "growth"]
print(growth_factors.head(20))

print("\n所有因子列表 (factor 列):")
print(all_factors["factor"].tolist())
