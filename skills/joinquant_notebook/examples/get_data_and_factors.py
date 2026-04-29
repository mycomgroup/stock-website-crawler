"""
获取基础数据和因子数据示例

这个示例展示如何从 JoinQuant 获取：
1. 基础数据 - 股票列表、行情数据
2. 因子数据 - 聚宽因子库、因子看板

运行方式:
    node run-strategy.js --strategy examples/get_data_and_factors.py
"""

from jqdata import *
import pandas as pd

print("=" * 60)
print("JoinQuant 基础数据和因子数据获取示例")
print("=" * 60)

# ============================================================
# 1. 基础数据 - 获取股票列表
# ============================================================
print("\n【1】获取股票列表")

# 获取指定日期所有股票
date = "2024-01-02"
all_stocks = get_all_securities(['stock'], date)
print(f"  {date} 在市的股票数量: {len(all_stocks)}")
print(f"  示例股票:\n{all_stocks.head(3)}")

# ============================================================
# 2. 基础数据 - 获取行情数据
# ============================================================
print("\n【2】获取行情数据 (get_price)")

# 获取单只股票近5日行情
stock = '000001.XSHE'
df_price = get_price(stock, count=5, end_date='2024-01-10', frequency='daily',
                     fields=['open', 'close', 'high', 'low', 'volume', 'money'])
print(f"  {stock} 近5日行情:")
print(df_price)

# 获取多只股票行情
stocks = ['000001.XSHE', '000002.XSHE', '000004.XSHE']
df_multi = get_price(stocks, count=3, end_date='2024-01-10', frequency='daily',
                     fields=['close', 'volume'])
print(f"\n  多只股票({len(stocks)}只)近3日收盘价:")
print(df_multi)

# ============================================================
# 3. 因子数据 - 获取聚宽因子列表
# ============================================================
print("\n【3】获取聚宽因子列表 (get_all_factors)")

# 获取所有因子
df_factors = get_all_factors()
print(f"  聚宽因子库共有 {len(df_factors)} 个因子")
print(f"  因子分类: {df_factors['category'].unique().tolist()}")
print(f"\n  因子示例:")
print(df_factors.head(10))

# 按分类统计因子数量
factor_counts = df_factors.groupby('category').size().sort_values(ascending=False)
print(f"\n  各分类因子数量:")
print(factor_counts)

# ============================================================
# 4. 因子数据 - 获取因子看板数据
# ============================================================
print("\n【4】获取因子看板数据 (get_factor_kanban_values)")

# 获取因子表现数据
df_kanban = get_factor_kanban_values(
    universe='hs300',        # 沪深300
    bt_cycle='month_3',      # 近3个月
    model='long_only',       # 纯多头
    category=['quality', 'basics', 'growth', 'risk'],
    skip_paused=False,
    commision_slippage=0
)
print(f"  因子看板数据 (最近5条):")
print(df_kanban.head())

# 筛选表现好的因子
print(f"\n  IC均值大于0.05的因子:")
good_factors = df_kanban[df_kanban['ic_mean'] > 0.05][['date', 'category', 'code', 'ic_mean', 'ir']]
print(good_factors)

print("\n" + "=" * 60)
print("示例完成!")
print("=" * 60)