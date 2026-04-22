from jqdata import *
from jqfactor import Factor, calc_factors
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

val = get_valuation(
    stocks, end_date=test_date, fields=["pb_ratio", "pe_ratio"], count=1
)
val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
val = val[(val["pb_ratio"] > 0) & (val["pe_ratio"] > 0) & (val["pe_ratio"] < 100)]
print(f"估值筛选后: {len(val)}")


class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = ["roa", "roa_4"]

    def calc(self, data):
        roa = data["roa"]
        self.basic = pd.DataFrame({"ROA": roa})
        self.fscore = roa.apply(lambda x: 7 if x > 3 else 6 if x > 1 else 5)


try:
    factor = RFScore()
    calc_factors(
        stocks[:50], [factor], start_date=str(test_date), end_date=str(test_date)
    )
    print(f"因子计算成功，样本数: 50")
    print(factor.basic.head(10))
except Exception as e:
    print(f"因子计算失败: {e}")

print("\n简单选股测试完成")
