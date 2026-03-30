#!/usr/bin/env python3
"""
首板低开机会仓 - 完整回测（2024-2025样本外验证）
重点测试：过滤因子效果、情绪条件、卖出规则对比
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 70)
print("首板低开机会仓 - 2024-2025样本外完整验证")
print("=" * 70)

# 测试参数
TEST_START = "2024-01-01"
TEST_END = "2025-12-31"

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
            fields=["open", "close", "high", "low"],
            panel=False,
        )
        if len(df) == 0 or df["open"].iloc[0] == 0:
            return None, None, None
        close_ret = (
            (df["close"].iloc[0] - df["open"].iloc[0]) / df["open"].iloc[0] * 100
        )
        high_ret = (df["high"].iloc[0] - df["open"].iloc[0]) / df["open"].iloc[0] * 100
        low_ret = (df["low"].iloc[0] - df["open"].iloc[0]) / df["open"].iloc[0] * 100
        return close_ret, high_ret, low_ret
    except:
        return None, None, None


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


def get_relative_position(stock, date, days=15):
    """计算相对位置"""
    try:
        df = get_price(
            stock, end_date=date, count=days, fields=["high", "low"], panel=False
        )
        if len(df) < days // 2:
            return None
        max_high = df["high"].max()
        min_low = df["low"].min()
        close = get_price(stock, end_date=date, count=1, fields=["close"], panel=False)[
            "close"
        ].iloc[0]
        if max_high == min_low:
            return 0.5
        return (close - min_low) / (max_high - min_low)
    except:
        return None


def get_market_cap(stock, date):
    """获取流通市值（亿）"""
    try:
        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code == stock
        )
        df = get_fundamentals(q, date=date)
        if len(df) > 0:
            return df["circulating_market_cap"].iloc[0]
        return None
    except:
        return None


def has_limit_up_recently(stock, date, days=1):
    """检查近N日是否有涨停"""
    try:
        days_list = get_trade_days(end_date=date, count=days + 1)
        for d in days_list[:-1]:
            df = get_price(
                stock,
                end_date=d,
                count=1,
                frequency="daily",
                fields=["close", "high_limit"],
                panel=False,
            )
            if (
                len(df) > 0
                and abs(df["close"].iloc[0] - df["high_limit"].iloc[0]) < 0.01
            ):
                return True
        return False
    except:
        return False


def get_market_sentiment(date):
    """获取市场情绪（涨停家数）"""
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()
        df = get_price(
            all_stocks[:2000],
            end_date=date,
            count=1,
            frequency="daily",
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
            skip_paused=False,
        )
        df = df.dropna()
        limit_up_count = len(df[abs(df["close"] - df["high_limit"]) < 0.01])
        return limit_up_count
    except:
        return 0


print(f"\n测试区间: {TEST_START} 到 {TEST_END}")

trade_days = get_trade_days(start_date=TEST_START, end_date=TEST_END)
print(f"交易日数量: {len(trade_days)}")

signals = []
daily_sentiment = {}

for i, date in enumerate(trade_days):
    if i % 20 == 0:
        print(f"\n进度: {i}/{len(trade_days)} ({date})")

    # 获取市场情绪
    sentiment = get_market_sentiment(date)
    daily_sentiment[str(date)] = sentiment

    # 获取所有A股
    try:
        all_stocks = get_all_securities("stock", date).index.tolist()

        # 获取昨日涨停
        yesterday = get_trade_days(end_date=date, count=2)[0]
        df = get_price(
            all_stocks[:3000],
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

        for stock in limit_up:
            open_change = get_open_change(stock, date)
            if open_change is None or open_change > 3 or open_change < -6:
                continue

            # 分类
            open_type = None
            for t, (low, high) in OPEN_TYPES.items():
                if low <= open_change < high:
                    open_type = t
                    break

            if open_type is None:
                continue

            # 获取过滤因子
            pos_15d = get_relative_position(stock, date, 15)
            pos_30d = get_relative_position(stock, date, 30)
            market_cap = get_market_cap(stock, date)
            no_limit_1d = not has_limit_up_recently(stock, date, 1)
            no_limit_2d = not has_limit_up_recently(stock, date, 2)

            close_ret, high_ret, low_ret = get_intraday_return(stock, date)
            next_open, next_close, next_high = get_next_day_return(stock, date)

            signals.append(
                {
                    "date": str(date),
                    "stock": stock,
                    "open_type": open_type,
                    "open_change": open_change,
                    "pos_15d": pos_15d,
                    "pos_30d": pos_30d,
                    "market_cap": market_cap,
                    "no_limit_1d": no_limit_1d,
                    "no_limit_2d": no_limit_2d,
                    "intraday_ret": close_ret,
                    "intraday_high_ret": high_ret,
                    "intraday_low_ret": low_ret,
                    "next_open_ret": next_open,
                    "next_close_ret": next_close,
                    "next_high_ret": next_high,
                    "sentiment": sentiment,
                }
            )

    except Exception as e:
        continue

print(f"\n总信号数: {len(signals)}")

# ============ 分析结果 ============
if len(signals) > 0:
    df_signals = pd.DataFrame(signals)

    # 1. 开盘类型分布
    print("\n" + "=" * 70)
    print("【1】开盘类型分布")
    print("=" * 70)
    type_counts = df_signals["open_type"].value_counts()
    for t, c in type_counts.items():
        print(f"  {t:12}: {c:4} ({c / len(df_signals) * 100:.1f}%)")

    # 2. 各类型收益统计
    print("\n" + "=" * 70)
    print("【2】各开盘类型收益统计（全样本）")
    print("=" * 70)

    results = []
    for open_type in OPEN_TYPES.keys():
        subset = df_signals[df_signals["open_type"] == open_type]
        if len(subset) == 0:
            continue

        intraday_mean = subset["intraday_ret"].mean()
        intraday_win = (subset["intraday_ret"] > 0).mean() * 100
        high_mean = subset["intraday_high_ret"].mean()
        next_open_mean = (
            subset["next_open_ret"].mean()
            if subset["next_open_ret"].notna().any()
            else 0
        )
        next_close_mean = (
            subset["next_close_ret"].mean()
            if subset["next_close_ret"].notna().any()
            else 0
        )
        next_high_mean = (
            subset["next_high_ret"].mean()
            if subset["next_high_ret"].notna().any()
            else 0
        )

        results.append(
            {
                "type": open_type,
                "count": len(subset),
                "intraday_ret": intraday_mean,
                "intraday_win": intraday_win,
                "high_ret": high_mean,
                "next_open": next_open_mean,
                "next_close": next_close_mean,
                "next_high": next_high_mean,
            }
        )

        print(f"\n【{open_type}】({len(subset)}只)")
        print(f"  日内收益: {intraday_mean:.2f}% (胜率{intraday_win:.1f}%)")
        print(f"  日内最高: {high_mean:.2f}%")
        print(f"  次日开盘: {next_open_mean:.2f}%")
        print(f"  次日收盘: {next_close_mean:.2f}%")
        print(f"  次日最高: {next_high_mean:.2f}%")

    # 3. 卖出规则对比
    print("\n" + "=" * 70)
    print("【3】卖出规则收益对比")
    print("=" * 70)

    sell_rules = {
        "日内收盘": df_signals["intraday_ret"].mean(),
        "日内最高": df_signals["intraday_high_ret"].mean(),
        "次日开盘": df_signals["next_open_ret"].mean(),
        "次日收盘": df_signals["next_close_ret"].mean(),
        "次日最高": df_signals["next_high_ret"].mean(),
    }

    print("\n卖出方式 | 平均收益 | 胜率")
    print("-" * 40)
    for rule, ret in sell_rules.items():
        if rule == "日内收盘":
            win = (df_signals["intraday_ret"] > 0).mean() * 100
        elif rule == "日内最高":
            win = (df_signals["intraday_high_ret"] > 0).mean() * 100
        elif rule == "次日开盘":
            win = (df_signals["next_open_ret"] > 0).mean() * 100
        elif rule == "次日收盘":
            win = (df_signals["next_close_ret"] > 0).mean() * 100
        elif rule == "次日最高":
            win = (df_signals["next_high_ret"] > 0).mean() * 100
        print(f"  {rule:10} | {ret:7.2f}% | {win:.1f}%")

    # 4. 过滤因子效果
    print("\n" + "=" * 70)
    print("【4】过滤因子效果分析")
    print("=" * 70)

    # 相对位置过滤
    print("\n【相对位置15日】")
    low_pos = df_signals[df_signals["pos_15d"] <= 0.3]
    mid_pos = df_signals[(df_signals["pos_15d"] > 0.3) & (df_signals["pos_15d"] <= 0.6)]
    high_pos = df_signals[df_signals["pos_15d"] > 0.6]
    if len(low_pos) > 0:
        print(
            f"  低位(≤30%): {len(low_pos)}只, 日内{low_pos['intraday_ret'].mean():.2f}%, 次日最高{low_pos['next_high_ret'].mean():.2f}%"
        )
    if len(mid_pos) > 0:
        print(
            f"  中位(30-60%): {len(mid_pos)}只, 日内{mid_pos['intraday_ret'].mean():.2f}%, 次日最高{mid_pos['next_high_ret'].mean():.2f}%"
        )
    if len(high_pos) > 0:
        print(
            f"  高位(>60%): {len(high_pos)}只, 日内{high_pos['intraday_ret'].mean():.2f}%, 次日最高{high_pos['next_high_ret'].mean():.2f}%"
        )

    # N日无涨停过滤
    print("\n【N日无涨停】")
    no_limit_1 = df_signals[df_signals["no_limit_1d"]]
    has_limit_1 = df_signals[~df_signals["no_limit_1d"]]
    if len(no_limit_1) > 0 and len(has_limit_1) > 0:
        print(
            f"  近1日无涨停: {len(no_limit_1)}只, 日内{no_limit_1['intraday_ret'].mean():.2f}%"
        )
        print(
            f"  近1日有涨停: {len(has_limit_1)}只, 日内{has_limit_1['intraday_ret'].mean():.2f}%"
        )

    # 市值过滤
    print("\n【流通市值】")
    small_cap = df_signals[df_signals["market_cap"] < 50]
    mid_cap = df_signals[
        (df_signals["market_cap"] >= 50) & (df_signals["market_cap"] < 150)
    ]
    large_cap = df_signals[df_signals["market_cap"] >= 150]
    if len(small_cap) > 0:
        print(
            f"  小市值(<50亿): {len(small_cap)}只, 日内{small_cap['intraday_ret'].mean():.2f}%"
        )
    if len(mid_cap) > 0:
        print(
            f"  中市值(50-150亿): {len(mid_cap)}只, 日内{mid_cap['intraday_ret'].mean():.2f}%"
        )
    if len(large_cap) > 0:
        print(
            f"  大市值(≥150亿): {len(large_cap)}只, 日内{large_cap['intraday_ret'].mean():.2f}%"
        )

    # 5. 情绪过滤效果
    print("\n" + "=" * 70)
    print("【5】市场情绪过滤效果")
    print("=" * 70)

    sentiment_median = df_signals["sentiment"].median()
    low_sentiment = df_signals[df_signals["sentiment"] < sentiment_median]
    high_sentiment = df_signals[df_signals["sentiment"] >= sentiment_median]

    print(f"\n情绪中位数: {sentiment_median:.0f}只涨停")
    if len(low_sentiment) > 0:
        print(
            f"  低情绪(<{sentiment_median:.0f}): {len(low_sentiment)}只, 日内{low_sentiment['intraday_ret'].mean():.2f}%"
        )
    if len(high_sentiment) > 0:
        print(
            f"  高情绪(≥{sentiment_median:.0f}): {len(high_sentiment)}只, 日内{high_sentiment['intraday_ret'].mean():.2f}%"
        )

    # 按情绪分层
    print("\n【情绪分层】")
    df_signals["sentiment_bin"] = pd.cut(
        df_signals["sentiment"],
        bins=[0, 30, 50, 80, 200],
        labels=["极低", "低", "中", "高"],
    )
    for bin_name in ["极低", "低", "中", "高"]:
        subset = df_signals[df_signals["sentiment_bin"] == bin_name]
        if len(subset) > 0:
            print(
                f"  {bin_name}: {len(subset)}只, 日内{subset['intraday_ret'].mean():.2f}%, 胜率{(subset['intraday_ret'] > 0).mean() * 100:.1f}%"
            )

    # 6. 组合过滤效果
    print("\n" + "=" * 70)
    print("【6】组合过滤效果（最佳结构识别）")
    print("=" * 70)

    # 测试不同过滤组合
    filter_combinations = [
        ("无过滤", lambda x: True),
        ("低位(pos≤30%)", lambda x: x["pos_15d"] <= 0.3),
        ("中市值(50-150亿)", lambda x: 50 <= x["market_cap"] < 150),
        ("近1日无涨停", lambda x: x["no_limit_1d"]),
        ("高情绪", lambda x: x["sentiment"] >= sentiment_median),
        ("低位+无涨停", lambda x: (x["pos_15d"] <= 0.3) and x["no_limit_1d"]),
        (
            "假弱高开+低位",
            lambda x: (x["open_type"] == "fake_weak") and (x["pos_15d"] <= 0.3),
        ),
        ("真低开A+无涨停", lambda x: (x["open_type"] == "low_a") and x["no_limit_1d"]),
    ]

    print("\n过滤条件 | 样本量 | 日内收益 | 胜率 | 次日最高")
    print("-" * 60)
    for name, filter_func in filter_combinations:
        try:
            subset = df_signals[df_signals.apply(filter_func, axis=1)]
            if len(subset) >= 10:
                ret = subset["intraday_ret"].mean()
                win = (subset["intraday_ret"] > 0).mean() * 100
                next_high = subset["next_high_ret"].mean()
                print(
                    f"  {name:20} | {len(subset):4} | {ret:7.2f}% | {win:5.1f}% | {next_high:7.2f}%"
                )
        except:
            continue

    # 7. 月度收益分布
    print("\n" + "=" * 70)
    print("【7】月度收益分布")
    print("=" * 70)

    df_signals["month"] = df_signals["date"].str[:7]
    monthly = (
        df_signals.groupby("month")
        .agg({"intraday_ret": ["mean", "count"], "next_high_ret": "mean"})
        .round(2)
    )

    print("\n月份 | 信号量 | 日内均值 | 次日最高")
    print("-" * 45)
    for month in sorted(df_signals["month"].unique()):
        subset = df_signals[df_signals["month"] == month]
        if len(subset) > 0:
            print(
                f"  {month} | {len(subset):4} | {subset['intraday_ret'].mean():7.2f}% | {subset['next_high_ret'].mean():7.2f}%"
            )

    # 8. 最终结论
    print("\n" + "=" * 70)
    print("【8】关键发现总结")
    print("=" * 70)

    # 找出最佳结构
    best_type = max(results, key=lambda x: x["intraday_ret"] * x["intraday_win"] / 100)
    print(f"\n1. 最佳日内结构: {best_type['type']}")
    print(
        f"   日内收益: {best_type['intraday_ret']:.2f}%, 胜率: {best_type['intraday_win']:.1f}%"
    )

    best_next = max(results, key=lambda x: x["next_high"])
    print(f"\n2. 最佳隔夜结构: {best_next['type']}")
    print(f"   次日最高收益: {best_next['next_high']:.2f}%")

    print(f"\n3. 卖出规则建议:")
    if sell_rules["次日最高"] > sell_rules["日内收盘"]:
        print(f"   隔夜持有(次日最高卖出)优于日内卖出")
        print(
            f"   次日最高均值: {sell_rules['次日最高']:.2f}% vs 日内收盘: {sell_rules['日内收盘']:.2f}%"
        )
    else:
        print(f"   日内卖出优于隔夜持有")

print("\n" + "=" * 70)
print("分析完成!")
print("=" * 70)
