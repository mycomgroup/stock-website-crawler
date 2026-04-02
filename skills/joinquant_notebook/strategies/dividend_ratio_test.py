# 股息率筛选测试
from jqdata import *

print("股息率筛选测试")
print("=" * 70)

test_date = "2025-12-31"

# 获取所有股票
all_stocks = get_all_securities(types=["stock"], date=test_date)
print(f"全市场股票数量: {len(all_stocks)}")

# 过滤上市时间 > 180天
from datetime import datetime, timedelta

test_date_obj = datetime.strptime(test_date, "%Y-%m-%d").date()
cutoff_date = test_date_obj - timedelta(days=180)
all_stocks = all_stocks[all_stocks["start_date"] <= cutoff_date]
stocks_after_ipo = all_stocks.index.tolist()
print(f"上市满180天股票数量: {len(stocks_after_ipo)}")

# 过滤ST股票
is_st = get_extras("is_st", stocks_after_ipo, end_date=test_date, count=1).iloc[-1]
st_count = (is_st == True).sum()
stocks_after_st = is_st[is_st == False].index.tolist()
print(f"ST股票数量: {st_count}")
print(f"过滤ST后股票数量: {len(stocks_after_st)}")

# 过滤科创板 (688开头)
stocks_no_688 = [s for s in stocks_after_st if not s.startswith("688")]
print(f"过滤科创板后股票数量: {len(stocks_no_688)}")

# 获取股息率数据
q_div = query(
    valuation.code,
    valuation.market_cap,
    valuation.pe_ratio,
    indicator.roe,
    valuation.dividend_ratio,
).filter(
    valuation.code.in_(stocks_no_688),
    valuation.market_cap >= 10,
    valuation.market_cap <= 100,
    valuation.pe_ratio > 0,
    valuation.pe_ratio < 100,
)

df_div = get_fundamentals(q_div, date=test_date)
print(f"\n10-100亿 & PE<100 基础池: {len(df_div)} 只")

div_thresholds = [0, 1, 1.5, 2, 2.5, 3]

print(f"\n{'股息率阈值':<12}{'候选数量':>10}{'筛选率':>10}")
print("-" * 35)

for div_th in div_thresholds:
    df_div_filtered = df_div[df_div["dividend_ratio"] >= div_th]
    rate = len(df_div_filtered) / len(df_div) * 100 if len(df_div) > 0 else 0
    print(f"股息率 >= {div_th}%{len(df_div_filtered):>10}{rate:>9.1f}%")

# 完整筛选条件
df_full = df_div[
    (df_div["pe_ratio"] < 30) & (df_div["roe"] > 5) & (df_div["dividend_ratio"] >= 2)
]
print(f"\n完整条件 (PE<30, ROE>5%, 股息率>=2%): {len(df_full)} 只")

# 显示前10只股票
if len(df_full) > 0:
    df_top10 = df_full.sort_values("dividend_ratio", ascending=False).head(10)
    print(f"\n前10只高股息率股票:")
    print("-" * 60)
    for i, row in df_top10.iterrows():
        print(
            f"{row['code'][:6]} | 市值:{row['market_cap']:>7.1f}亿 | PE:{row['pe_ratio']:>5.1f} | ROE:{row['roe']:>5.2f}% | 股息率:{row['dividend_ratio']:>5.2f}%"
        )
