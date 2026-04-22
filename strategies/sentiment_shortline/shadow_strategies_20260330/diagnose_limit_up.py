"""
涨停统计诊断 - RiceQuant Notebook

目标：找到涨停数量充足的时间段

运行方式：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/diagnose_limit_up.py --create-new --timeout-ms 180000
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("涨停统计诊断 - RiceQuant Notebook")
print("=" * 80)


def get_all_stocks_list():
    """获取所有A股股票列表"""
    try:
        instruments = all_instruments(type="CS")
        return list(instruments.order_book_id)
    except:
        return []


def get_prev_trading_date(date, trading_dates):
    """获取前一个交易日"""
    date_str = str(date)[:10]
    for i, d in enumerate(trading_dates):
        if str(d)[:10] == date_str and i > 0:
            return str(trading_dates[i - 1])[:10]
    return None


def count_limit_ups(date, stock_list, trading_dates, sample_size):
    """统计涨停数量"""
    limit_up = 0
    tested = 0
    prev_date = get_prev_trading_date(date, trading_dates)

    if prev_date is None:
        return 0, 0

    for stock in stock_list[:sample_size]:
        try:
            df = get_price(
                stock,
                start_date=prev_date,
                end_date=date,
                frequency="1d",
                fields=["close"],
            )
            if df is not None and len(df) >= 2:
                prev_close = df["close"].iloc[0]
                curr_close = df["close"].iloc[-1]
                if prev_close > 0:
                    pct = (curr_close - prev_close) / prev_close
                    if pct >= 0.095:
                        limit_up += 1
                    tested += 1
        except:
            continue

    return limit_up, tested


print("\n获取股票列表...")
all_stocks = get_all_stocks_list()
print(f"股票总数: {len(all_stocks)}")

print("\n" + "=" * 80)
print("测试1: 不同时间段的涨停统计")
print("=" * 80)

time_periods = [
    ("2015-03-01", "2015-03-31", "2015年3月"),
    ("2015-05-01", "2015-05-31", "2015年5月（牛市高峰）"),
    ("2015-06-01", "2015-06-15", "2015年6月上半月"),
    ("2014-12-01", "2014-12-31", "2014年12月"),
    ("2019-02-01", "2019-02-28", "2019年2月"),
    ("2020-07-01", "2020-07-31", "2020年7月"),
]

for start, end, desc in time_periods:
    print(f"\n{desc}:")
    try:
        dates = list(get_trading_dates(start, end))
        if len(dates) > 0:
            test_date = str(dates[len(dates) // 2])[:10]
            trading_dates = [
                str(d)[:10] for d in list(get_trading_dates("2014-01-01", "2024-12-31"))
            ]

            for sample_size in [500, 1000]:
                limit_up, tested = count_limit_ups(
                    test_date, all_stocks, trading_dates, sample_size
                )
                pct = limit_up / tested * 100 if tested > 0 else 0
                print(
                    f"  {test_date} (测试{sample_size}只): 涨停{limit_up}只, 比例{pct:.1f}%"
                )
        else:
            print(f"  无交易日数据")
    except Exception as e:
        print(f"  错误: {e}")

print("\n" + "=" * 80)
print("测试2: 不同股票数量的涨停统计")
print("=" * 80)

print("\n使用2015年5月数据（牛市高峰）:")
try:
    dates = list(get_trading_dates("2015-05-01", "2015-05-31"))
    if len(dates) > 0:
        test_date = str(dates[len(dates) // 2])[:10]
        trading_dates = [
            str(d)[:10] for d in list(get_trading_dates("2014-01-01", "2024-12-31"))
        ]

        for sample_size in [100, 300, 500, 1000, 2000]:
            limit_up, tested = count_limit_ups(
                test_date, all_stocks, trading_dates, sample_size
            )
            pct = limit_up / tested * 100 if tested > 0 else 0
            print(
                f"  {test_date} (测试{sample_size}只): 涨停{limit_up}只, 比例{pct:.1f}%"
            )
except Exception as e:
    print(f"  错误: {e}")

print("\n" + "=" * 80)
print("测试3: 涨停阈值建议")
print("=" * 80)

print("\n根据测试结果，建议情绪阈值:")
print("  - 测试500只股票，涨停>=30只 -> 阈值设为30")
print("  - 测试1000只股票，涨停>=50只 -> 阈值设为50")
print("  - 测试2000只股票，涨停>=80只 -> 阈值设为80")

print("\n" + "=" * 80)
print("诊断完成")
print("=" * 80)
