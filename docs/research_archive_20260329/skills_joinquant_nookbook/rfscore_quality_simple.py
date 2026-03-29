from jqdata import *
from jqfactor import Factor, calc_factors
from datetime import datetime
import pandas as pd
import numpy as np

# 简化的RFScore计算
trade_day = get_trade_days(end_date=datetime.now().date(), count=1)[0]
trade_day_str = str(trade_day)

hs300 = set(get_index_stocks("000300.XSHG", date=trade_day))
zz500 = set(get_index_stocks("000905.XSHG", date=trade_day))
stocks = [s for s in (hs300 | zz500) if not s.startswith("688")]

sec = get_all_securities(types=["stock"], date=trade_day)
sec = sec.loc[sec.index.intersection(stocks)]
sec = sec[sec["start_date"] <= trade_day - pd.Timedelta(days=180)]
stocks = sec.index.tolist()

is_st = get_extras("is_st", stocks, end_date=trade_day, count=1).iloc[-1]
stocks = is_st[is_st == False].index.tolist()

# 获取估值数据
val = get_valuation(
    stocks,
    end_date=trade_day_str,
    fields=["pb_ratio", "pe_ratio", "market_cap"],
    count=1,
)
val = val.drop_duplicates("code").set_index("code")

# 简单过滤：低PB股票
df = val.copy()
df = df.dropna()
df["pb_rank"] = df["pb_ratio"].rank(pct=True)
df = df[df["pb_rank"] <= 0.2]  # PB最低的20%

print(f"=" * 60)
print(f"RFScore候选组合质量监控 (简化版)")
print(f"检测日期: {trade_day}")
print(f"=" * 60)
print(f"\n候选股数量: {len(df)}")
print(f"\n估值统计:")
print(f"  PB均值: {df['pb_ratio'].mean():.4f}")
print(f"  PB中位数: {df['pb_ratio'].median():.4f}")
print(f"  PB范围: [{df['pb_ratio'].min():.4f}, {df['pb_ratio'].max():.4f}]")
print(f"  PE均值: {df['pe_ratio'].mean():.4f}")
print(f"  PE中位数: {df['pe_ratio'].median():.4f}")
print(f"\n市值统计(亿元):")
print(f"  均值: {df['market_cap'].mean() / 1e8:.2f}")
print(f"  中位数: {df['market_cap'].median() / 1e8:.2f}")

# 显示前10只股票
print(f"\n前10只候选股:")
print(df.head(10)[["pb_ratio", "pe_ratio"]].round(4).to_string())
