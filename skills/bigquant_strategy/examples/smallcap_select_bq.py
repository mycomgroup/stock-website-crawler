"""
小市值选股 - BigQuant 版本
对应 JoinQuant: smallcap_state_baseline.py 的 select_and_buy 逻辑
验证 cn_stock_valuation 数据可用性
"""

import dai
import pandas as pd

DATE = "2024-01-02"
CAP_MIN = 5e8  # 5亿（注意：BigQuant 单位是元，JoinQuant 是亿元）
CAP_MAX = 30e8  # 30亿
TOP_N = 10

print("=== 小市值选股验证 ===")
print("日期:", DATE)

# 获取估值数据
val_df = dai.query(
    """
    SELECT instrument, float_market_cap, total_market_cap, pe_ttm, pb
    FROM cn_stock_valuation
    WHERE date = '{date}'
      AND float_market_cap >= {cap_min}
      AND float_market_cap <= {cap_max}
      AND pe_ttm > 0
    ORDER BY float_market_cap ASC
    LIMIT {n}
""".format(date=DATE, cap_min=CAP_MIN, cap_max=CAP_MAX, n=TOP_N)
).df()

print("选出股票数:", len(val_df))
print(val_df.to_string())
