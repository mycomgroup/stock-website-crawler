from jqdata import *
from jqfactor import get_factor_values
import pandas as pd

test_date = "2024-06-01"
stocks = ["000001.XSHE", "600000.XSHG", "600036.XSHG"]
print(f"测试日期: {test_date}")
print(f"测试股票: {stocks}")

print("\n获取ROA因子...")
roa_data = get_factor_values(stocks, "roa_ttm", end_date=test_date, count=1)
print(roa_data)
print("成功！")
