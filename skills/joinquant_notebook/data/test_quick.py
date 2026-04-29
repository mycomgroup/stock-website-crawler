"""
快速测试脚本 - 测试核心 API
"""

from jqdata import *
import pandas as pd

print("开始测试...")

# 1. 获取股票列表
print("\n1. get_all_securities(['stock'], '2024-01-02')")
try:
    df = get_all_securities(['stock'], '2024-01-02')
    print(f"  成功: {len(df)} 只股票")
    print(f"  示例: {df.head(2).to_string()}")
except Exception as e:
    print(f"  失败: {e}")

# 2. 获取日线行情
print("\n2. get_price('000001.XSHE', count=5, frequency='daily')")
try:
    df = get_price('000001.XSHE', count=5, frequency='daily')
    print(f"  成功: {df.shape}")
    print(f"  列名: {list(df.columns)}")
    print(f"  数据:\n{df.to_string()}")
except Exception as e:
    print(f"  失败: {e}")

# 3. 获取交易日列表
print("\n3. get_trade_days(start_date='2024-01-01', end_date='2024-01-10')")
try:
    dates = get_trade_days(start_date='2024-01-01', end_date='2024-01-10')
    print(f"  成功: {len(dates)} 个交易日")
    print(f"  日期: {list(dates)}")
except Exception as e:
    print(f"  失败: {e}")

# 4. 获取指数成分股
print("\n4. get_index_stocks('000300.XSHG')")
try:
    stocks = get_index_stocks('000300.XSHG')
    print(f"  成功: {len(stocks)} 只成分股")
    print(f"  前5只: {list(stocks[:5])}")
except Exception as e:
    print(f"  失败: {e}")

# 5. 获取行业
print("\n5. get_industry('000001.XSHE')")
try:
    industry = get_industry('000001.XSHE')
    print(f"  成功: {industry}")
except Exception as e:
    print(f"  失败: {e}")

# 6. 获取因子列表
print("\n6. get_all_factors()")
try:
    df = get_all_factors()
    print(f"  成功: {len(df)} 个因子")
    print(f"  分类: {df['category'].unique().tolist()}")
    print(f"  示例:\n{df.head(3).to_string()}")
except Exception as e:
    print(f"  失败: {e}")

# 7. 获取因子看板
print("\n7. get_factor_kanban_values(universe='hs300', bt_cycle='month_3')")
try:
    df = get_factor_kanban_values(universe='hs300', bt_cycle='month_3', model='long_only', category=['quality', 'basics'])
    print(f"  成功: {df.shape}")
    print(f"  列名: {list(df.columns)}")
    print(f"  数据:\n{df.head(3).to_string()}")
except Exception as e:
    print(f"  失败: {e}")

# 8. 获取资金流向
print("\n8. get_money_flow('000001.XSHE', start_date='2024-01-02', end_date='2024-01-05')")
try:
    df = get_money_flow('000001.XSHE', start_date='2024-01-02', end_date='2024-01-05')
    print(f"  成功: {df.shape if df is not None else 'None'}")
    if df is not None and not df.empty:
        print(f"  列名: {list(df.columns)}")
        print(f"  数据:\n{df.to_string()}")
except Exception as e:
    print(f"  失败: {e}")

# 9. 获取龙虎榜
print("\n9. get_billboard_list(date='2024-01-02')")
try:
    df = get_billboard_list(date='2024-01-02')
    print(f"  成功: {df.shape if df is not None else 'None'}")
    if df is not None and not df.empty:
        print(f"  列名: {list(df.columns)}")
        print(f"  数据:\n{df.head(3).to_string()}")
except Exception as e:
    print(f"  失败: {e}")

# 10. 获取限售解禁
print("\n10. get_locked_shares(start_date='2024-01-01', end_date='2024-01-31')")
try:
    df = get_locked_shares(start_date='2024-01-01', end_date='2024-01-31')
    print(f"  成功: {df.shape if df is not None else 'None'}")
    if df is not None and not df.empty:
        print(f"  列名: {list(df.columns)}")
        print(f"  数据:\n{df.head(3).to_string()}")
except Exception as e:
    print(f"  失败: {e}")

print("\n测试完成!")