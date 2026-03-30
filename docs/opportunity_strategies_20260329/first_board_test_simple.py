#!/usr/bin/env python3
"""
首板低开机会仓 - 简化版测试（只测试最近数据）
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 60)
print("首板低开信号统计 - 简化测试版")
print("=" * 60)

# 测试参数
TEST_START = "2024-12-01"
TEST_END = "2025-01-15"

# 开盘结构分类
OPEN_TYPES = {
    "deep_low": (-5, -3),
    "low_a": (-3, -1),
    "low_b": (-1, 0),
    "flat": (0, 0.5),
    "fake_weak": (0.5, 1.5),
    "slight_high": (1.5, 2.5),
}


def get_open_change(stock, date):
    """计算开盘涨跌幅"""
    try:
        df = get_price(
            stock,
            start_date=date,
            end_date=date,
            frequency="daily",
            fields=["open", "pre_close"],
            panel=False,
        )
        if len(df) == 0 or df["pre_close"].iloc[0] == 0:
            return None
        return (
            (df["open"].iloc[0] - df["pre_close"].iloc[0])
            / df["pre_close"].iloc[0]
            * 100
        )
    except:
        return None


def get_intraday_return(stock, date):
    """获取日内收益"""
    try:
        df = get_price(
            stock,
            start_date=date,
            end_date=date,
            frequency="daily",
            fields=["open", "close", "high"],
            panel=False,
        )
        if len(df) == 0 or df["open"].iloc[0] == 0:
            return None, None
        close_ret = (
            (df["close"].iloc[0] - df["open"].iloc[0]) / df["open"].iloc[0] * 100
        )
        high_ret = (df["high"].iloc[0] - df["open"].iloc[0]) / df["open"].iloc[0] * 100
        return close_ret, high_ret
    except:
        return None, None


def get_next_day_return(stock, date):
    """获取次日收益"""
    try:
        trade_days = get_trade_days(start_date=date, end_date=date + timedelta(days=5))
        if len(trade_days) < 2:
            return None, None, None

        today_close = get_price(
            stock, start_date=date, end_date=date, fields=["close"], panel=False
        )["close"].iloc[0]

        next_day = trade_days[1]
        df_next = get_price(
            stock,
            start_date=next_day,
            end_date=next_day,
            fields=["open", "close", "high"],
            panel=False,
        )
        if len(df_next) == 0:
            return None, None, None

        next_open_ret = (df_next["open"].iloc[0] - today_close) / today_close * 100
        next_close_ret = (df_next["close"].iloc[0] - today_close) / today_close * 100
        next_high_ret = (df_next["high"].iloc[0] - today_close) / today_close * 100

        return next_open_ret, next_close_ret, next_high_ret
    except:
        return None, None, None


print(f"\n测试区间: {TEST_START} 到 {TEST_END}")

trade_days = get_trade_days(start_date=TEST_START, end_date=TEST_END)
print(f"交易日数量: {len(trade_days)}")

signals = []

for date in trade_days:
    print(f"\n处理: {date}")

    # 获取所有A股
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()

        # 获取昨日涨停
        yesterday = get_trade_days(end_date=date, count=2)[0]
        df = get_price(
            all_stocks[:1000],
            end_date=yesterday,
            count=1,
            frequency="daily",
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
            skip_paused=False,
        )
        df = df.dropna()

        # 涨停判定
        limit_up = df[abs(df["close"] - df["high_limit"]) < 0.01]["code"].tolist()
        print(f"  昨日涨停: {len(limit_up)}只")

        for stock in limit_up[:20]:  # 限制数量
            open_change = get_open_change(stock, date)
            if open_change is None:
                continue

            # 分类
            open_type = None
            for t, (low, high) in OPEN_TYPES.items():
                if low <= open_change < high:
                    open_type = t
                    break

            if open_type is None:
                continue

            close_ret, high_ret = get_intraday_return(stock, date)
            next_open, next_close, next_high = get_next_day_return(stock, date)

            signals.append(
                {
                    "date": str(date),
                    "stock": stock,
                    "open_type": open_type,
                    "open_change": open_change,
                    "intraday_ret": close_ret,
                    "intraday_high_ret": high_ret,
                    "next_open_ret": next_open,
                    "next_close_ret": next_close,
                    "next_high_ret": next_high,
                }
            )

    except Exception as e:
        print(f"  错误: {e}")
        continue

print(f"\n总信号数: {len(signals)}")

# 分析
if len(signals) > 0:
    df_signals = pd.DataFrame(signals)

    print("\n【开盘类型分布】")
    type_counts = df_signals["open_type"].value_counts()
    for t, c in type_counts.items():
        print(f"  {t}: {c}")

    print("\n【各类型收益统计】")
    for open_type in OPEN_TYPES.keys():
        subset = df_signals[df_signals["open_type"] == open_type]
        if len(subset) == 0:
            continue

        print(f"\n【{open_type}】({len(subset)}只)")
        print(f"  开盘变化均值: {subset['open_change'].mean():.2f}%")

        if subset["intraday_ret"].notna().any():
            print(f"  日内收益均值: {subset['intraday_ret'].mean():.2f}%")
            print(f"  日内胜率: {(subset['intraday_ret'] > 0).mean() * 100:.1f}%")

        if subset["next_open_ret"].notna().any():
            print(f"  次日开盘收益: {subset['next_open_ret'].mean():.2f}%")
            print(f"  次日收盘收益: {subset['next_close_ret'].mean():.2f}%")
            print(f"  次日最高收益: {subset['next_high_ret'].mean():.2f}%")

print("\n测试完成!")
