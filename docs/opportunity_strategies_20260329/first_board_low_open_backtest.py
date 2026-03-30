#!/usr/bin/env python3
"""
首板低开机会仓核心机制研究 - 聚宽回测脚本
研究目标：
1. 拆解不同开盘结构（真低开 vs 假弱高开）
2. 验证不同卖出规则的收益差异
3. 测试情绪过滤的增益效果
4. 分析2024-2026样本外表现
"""

from jqdata import *
from jqfactor import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("首板低开机会仓核心机制研究 - 信号统计分析")
print("=" * 80)

# ============ 全局参数 ============
START_DATE = "2021-01-01"
END_DATE = "2025-12-31"  # 聚宽数据截止
SAMPLE_OUT_DATE = "2024-01-01"  # 样本外起点

# 开盘结构分类阈值
OPEN_TYPES = {
    "deep_low": (-5, -3),  # 深度低开
    "low_a": (-3, -1),  # 真低开A
    "low_b": (-1, 0),  # 真低开B
    "flat": (0, 0.5),  # 平开附近
    "fake_weak": (0.5, 1.5),  # 假弱高开
    "slight_high": (1.5, 2.5),  # 微高开
}

print("\n【1】基础数据准备")
print("-" * 60)


# ============ 辅助函数 ============
def get_trade_days_list(start, end):
    """获取交易日列表"""
    return get_trade_days(start_date=start, end_date=end)


def is_limit_up(stock, date):
    """判断是否涨停"""
    try:
        df = get_price(
            stock,
            end_date=date,
            count=1,
            frequency="daily",
            fields=["close", "high_limit"],
            panel=False,
        )
        if len(df) == 0:
            return False
        return abs(df["close"].iloc[0] - df["high_limit"].iloc[0]) < 0.001
    except:
        return False


def get_yesterday_limit_up_stocks(date):
    """获取昨日涨停股票列表"""
    try:
        # 获取所有股票
        all_stocks = get_all_securities("stock", date).index.tolist()

        # 过滤次新股（上市不足60天）
        filtered = []
        for s in all_stocks:
            info = get_security_info(s)
            if info and (pd.Timestamp(date) - info.start_date).days > 60:
                filtered.append(s)

        # 获取昨日涨停股票
        yesterday = get_trade_days(end_date=date, count=2)[0]
        df = get_price(
            filtered,
            end_date=yesterday,
            count=1,
            frequency="daily",
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
            skip_paused=False,
        )
        df = df.dropna()
        limit_up = df[abs(df["close"] - df["high_limit"]) < 0.001]["code"].tolist()

        # 过滤ST
        st_info = get_extras(
            "is_st", limit_up, start_date=yesterday, end_date=yesterday, df=True
        )
        if not st_info.empty:
            non_st = st_info.T[st_info.iloc[0] == False].index.tolist()
            return non_st
        return limit_up
    except Exception as e:
        print(f"获取涨停股票出错: {e}")
        return []


def get_open_type(stock, date):
    """获取开盘类型"""
    try:
        df = get_price(
            stock,
            start_date=date,
            end_date=date,
            frequency="daily",
            fields=["open", "pre_close"],
            panel=False,
        )
        if len(df) == 0:
            return None

        open_price = df["open"].iloc[0]
        pre_close = df["pre_close"].iloc[0]

        if pre_close == 0:
            return None

        open_change = (open_price - pre_close) / pre_close * 100

        for type_name, (low, high) in OPEN_TYPES.items():
            if low <= open_change < high:
                return type_name, open_change
        return None, open_change
    except:
        return None, None


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
        close_price = get_price(
            stock, end_date=date, count=1, fields=["close"], panel=False
        )["close"].iloc[0]

        if max_high == min_low:
            return 0.5
        return (close_price - min_low) / (max_high - min_low)
    except:
        return None


def has_limit_up_in_n_days(stock, date, n=1):
    """检查近N日是否有涨停"""
    try:
        days_list = get_trade_days(end_date=date, count=n + 1)
        for d in days_list[:-1]:  # 排除当天
            if is_limit_up(stock, d):
                return True
        return False
    except:
        return False


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


def get_turnover_ratio(stock, date):
    """获取换手率"""
    try:
        df = get_price(
            stock,
            end_date=date,
            count=1,
            frequency="daily",
            fields=["volume", "money"],
            panel=False,
        )
        # 简化计算：使用成交额/流通市值近似
        circ_cap = get_market_cap(stock, date)
        if circ_cap and circ_cap > 0:
            money = df["money"].iloc[0]
            return money / (circ_cap * 1e8) * 100 if money > 0 else 0
        return None
    except:
        return None


def get_intraday_return(stock, date, time_point="close"):
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
        if len(df) == 0:
            return None

        open_price = df["open"].iloc[0]
        if time_point == "close":
            exit_price = df["close"].iloc[0]
        elif time_point == "high":
            exit_price = df["high"].iloc[0]
        elif time_point == "low":
            exit_price = df["low"].iloc[0]
        else:
            exit_price = df["close"].iloc[0]

        return (exit_price - open_price) / open_price * 100
    except:
        return None


def get_next_day_return(stock, date):
    """获取次日开盘收益"""
    try:
        trade_days = get_trade_days(start_date=date, end_date=date + timedelta(days=5))
        if len(trade_days) < 2:
            return None

        next_day = trade_days[1]
        df_today = get_price(
            stock,
            start_date=date,
            end_date=date,
            frequency="daily",
            fields=["close"],
            panel=False,
        )
        df_next = get_price(
            stock,
            start_date=next_day,
            end_date=next_day,
            frequency="daily",
            fields=["open", "close", "high"],
            panel=False,
        )

        if len(df_today) == 0 or len(df_next) == 0:
            return None

        today_close = df_today["close"].iloc[0]
        next_open = df_next["open"].iloc[0]
        next_close = df_next["close"].iloc[0]
        next_high = df_next["high"].iloc[0]

        return {
            "next_open_ret": (next_open - today_close) / today_close * 100,
            "next_close_ret": (next_close - today_close) / today_close * 100,
            "next_high_ret": (next_high - today_close) / today_close * 100,
        }
    except:
        return None


# ============ 主要分析逻辑 ============
print("\n【2】信号收集与分类")
print("-" * 60)

trade_days = get_trade_days_list(START_DATE, END_DATE)
print(f"交易日总数: {len(trade_days)}")

# 存储所有信号
all_signals = []
signal_count = 0
error_count = 0

for i, date in enumerate(trade_days):
    if i % 50 == 0:
        print(f"处理进度: {i}/{len(trade_days)} ({date})")

    # 获取昨日涨停股票
    yd_limit_ups = get_yesterday_limit_up_stocks(date)

    for stock in yd_limit_ups:
        try:
            # 获取开盘类型
            open_type, open_change = get_open_type(stock, date)
            if open_type is None:
                continue

            # 获取相对位置
            pos_15d = get_relative_position(stock, date, 15)
            pos_30d = get_relative_position(stock, date, 30)

            # 检查近N日无涨停
            no_limit_1d = not has_limit_up_in_n_days(stock, date, 1)
            no_limit_2d = not has_limit_up_in_n_days(stock, date, 2)

            # 获取市值和换手率
            market_cap = get_market_cap(stock, date)
            turnover = get_turnover_ratio(stock, date)

            # 计算收益
            intraday_ret = get_intraday_return(stock, date, "close")
            intraday_high_ret = get_intraday_return(stock, date, "high")
            intraday_low_ret = get_intraday_return(stock, date, "low")
            next_day_ret = get_next_day_return(stock, date)

            signal = {
                "date": date,
                "stock": stock,
                "open_type": open_type,
                "open_change": open_change,
                "pos_15d": pos_15d,
                "pos_30d": pos_30d,
                "no_limit_1d": no_limit_1d,
                "no_limit_2d": no_limit_2d,
                "market_cap": market_cap,
                "turnover": turnover,
                "intraday_ret": intraday_ret,
                "intraday_high_ret": intraday_high_ret,
                "intraday_low_ret": intraday_low_ret,
                "next_open_ret": next_day_ret["next_open_ret"]
                if next_day_ret
                else None,
                "next_close_ret": next_day_ret["next_close_ret"]
                if next_day_ret
                else None,
                "next_high_ret": next_day_ret["next_high_ret"]
                if next_day_ret
                else None,
                "is_sample_out": date >= pd.Timestamp(SAMPLE_OUT_DATE),
            }

            all_signals.append(signal)
            signal_count += 1

        except Exception as e:
            error_count += 1
            continue

print(f"\n信号收集完成:")
print(f"  总信号数: {signal_count}")
print(f"  错误数: {error_count}")

# ============ 分析结果 ============
print("\n【3】分析结果")
print("=" * 80)

# 转换为DataFrame
df_signals = pd.DataFrame(all_signals)

if len(df_signals) == 0:
    print("未收集到有效信号")
else:
    # 3.1 按开盘类型统计
    print("\n### 3.1 开盘类型分布 ###")
    type_counts = df_signals["open_type"].value_counts()
    for t, c in type_counts.items():
        print(f"  {t}: {c} ({c / len(df_signals) * 100:.1f}%)")

    # 3.2 各开盘类型的收益统计
    print("\n### 3.2 各开盘类型收益统计 ###")
    for open_type in OPEN_TYPES.keys():
        subset = df_signals[df_signals["open_type"] == open_type]
        if len(subset) == 0:
            continue

        print(f"\n【{open_type}】样本数: {len(subset)}")

        # 日内收益
        intraday_mean = subset["intraday_ret"].mean()
        intraday_win = (subset["intraday_ret"] > 0).mean() * 100
        print(f"  日内收益均值: {intraday_mean:.2f}%")
        print(f"  日内胜率: {intraday_win:.1f}%")

        # 次日收益
        if "next_open_ret" in subset.columns:
            next_open_mean = subset["next_open_ret"].mean()
            next_open_win = (subset["next_open_ret"] > 0).mean() * 100
            next_close_mean = subset["next_close_ret"].mean()
            next_close_win = (subset["next_close_ret"] > 0).mean() * 100
            print(f"  次日开盘收益均值: {next_open_mean:.2f}%")
            print(f"  次日开盘胜率: {next_open_win:.1f}%")
            print(f"  次日收盘收益均值: {next_close_mean:.2f}%")
            print(f"  次日收盘胜率: {next_close_win:.1f}%")

    # 3.3 样本内外对比
    print("\n### 3.3 样本内外对比 ###")
    in_sample = df_signals[~df_signals["is_sample_out"]]
    out_sample = df_signals[df_signals["is_sample_out"]]

    print(f"\n样本内 (2021-2023): {len(in_sample)} 信号")
    if len(in_sample) > 0:
        print(f"  日内收益均值: {in_sample['intraday_ret'].mean():.2f}%")
        print(f"  日内胜率: {(in_sample['intraday_ret'] > 0).mean() * 100:.1f}%")

    print(f"\n样本外 (2024-2025): {len(out_sample)} 信号")
    if len(out_sample) > 0:
        print(f"  日内收益均值: {out_sample['intraday_ret'].mean():.2f}%")
        print(f"  日内胜率: {(out_sample['intraday_ret'] > 0).mean() * 100:.1f}%")

    # 3.4 各开盘类型样本内外对比
    print("\n### 3.4 各开盘类型样本内外收益对比 ###")
    for open_type in OPEN_TYPES.keys():
        in_sub = in_sample[in_sample["open_type"] == open_type]
        out_sub = out_sample[out_sample["open_type"] == open_type]

        if len(in_sub) > 0 and len(out_sub) > 0:
            in_ret = in_sub["intraday_ret"].mean()
            out_ret = out_sub["intraday_ret"].mean()
            print(f"\n【{open_type}】")
            print(
                f"  样本内: {len(in_sub)}只, 均值{in_ret:.2f}%, 胜率{(in_sub['intraday_ret'] > 0).mean() * 100:.1f}%"
            )
            print(
                f"  样本外: {len(out_sub)}只, 均值{out_ret:.2f}%, 胜率{(out_sub['intraday_ret'] > 0).mean() * 100:.1f}%"
            )

    # 3.5 过滤因子效果
    print("\n### 3.5 过滤因子效果分析 ###")

    # 相对位置过滤
    print("\n【相对位置过滤】")
    low_pos = df_signals[df_signals["pos_15d"] <= 0.3]
    high_pos = df_signals[df_signals["pos_15d"] > 0.3]
    if len(low_pos) > 0 and len(high_pos) > 0:
        print(
            f"  低位(≤30%): {len(low_pos)}只, 日内均值{low_pos['intraday_ret'].mean():.2f}%"
        )
        print(
            f"  高位(>30%): {len(high_pos)}只, 日内均值{high_pos['intraday_ret'].mean():.2f}%"
        )

    # N日无涨停过滤
    print("\n【N日无涨停过滤】")
    no_limit_1 = df_signals[df_signals["no_limit_1d"]]
    has_limit_1 = df_signals[~df_signals["no_limit_1d"]]
    if len(no_limit_1) > 0 and len(has_limit_1) > 0:
        print(
            f"  近1日无涨停: {len(no_limit_1)}只, 日内均值{no_limit_1['intraday_ret'].mean():.2f}%"
        )
        print(
            f"  近1日有涨停: {len(has_limit_1)}只, 日内均值{has_limit_1['intraday_ret'].mean():.2f}%"
        )

    # 市值过滤
    print("\n【市值过滤】")
    small_cap = df_signals[df_signals["market_cap"] < 50]
    mid_cap = df_signals[
        (df_signals["market_cap"] >= 50) & (df_signals["market_cap"] < 150)
    ]
    large_cap = df_signals[df_signals["market_cap"] >= 150]
    if len(small_cap) > 0:
        print(
            f"  小市值(<50亿): {len(small_cap)}只, 日内均值{small_cap['intraday_ret'].mean():.2f}%"
        )
    if len(mid_cap) > 0:
        print(
            f"  中市值(50-150亿): {len(mid_cap)}只, 日内均值{mid_cap['intraday_ret'].mean():.2f}%"
        )
    if len(large_cap) > 0:
        print(
            f"  大市值(≥150亿): {len(large_cap)}只, 日内均值{large_cap['intraday_ret'].mean():.2f}%"
        )

    # 3.6 卖出规则对比
    print("\n### 3.6 不同卖出规则收益对比 ###")
    print("\n【全样本】")
    sell_rules = {
        "日内最高卖出": df_signals["intraday_high_ret"].mean(),
        "日内收盘卖出": df_signals["intraday_ret"].mean(),
        "次日开盘卖出": df_signals["next_open_ret"].mean()
        if "next_open_ret" in df_signals.columns
        else None,
        "次日收盘卖出": df_signals["next_close_ret"].mean()
        if "next_close_ret" in df_signals.columns
        else None,
        "次日最高卖出": df_signals["next_high_ret"].mean()
        if "next_high_ret" in df_signals.columns
        else None,
    }
    for rule, ret in sell_rules.items():
        if ret is not None:
            win_rate = None
            if rule == "日内最高卖出":
                win_rate = (df_signals["intraday_high_ret"] > 0).mean() * 100
            elif rule == "日内收盘卖出":
                win_rate = (df_signals["intraday_ret"] > 0).mean() * 100
            elif rule == "次日开盘卖出" and "next_open_ret" in df_signals.columns:
                win_rate = (df_signals["next_open_ret"] > 0).mean() * 100
            elif rule == "次日收盘卖出" and "next_close_ret" in df_signals.columns:
                win_rate = (df_signals["next_close_ret"] > 0).mean() * 100
            elif rule == "次日最高卖出" and "next_high_ret" in df_signals.columns:
                win_rate = (df_signals["next_high_ret"] > 0).mean() * 100

            win_str = f", 胜率{win_rate:.1f}%" if win_rate is not None else ""
            print(f"  {rule}: 均值{ret:.2f}%{win_str}")

    # 3.7 最佳结构识别
    print("\n### 3.7 最佳结构识别 ###")
    print("\n【综合评分】(基于收益*胜率*信号量）")

    results = []
    for open_type in OPEN_TYPES.keys():
        subset = df_signals[df_signals["open_type"] == open_type]
        if len(subset) < 10:  # 最少样本要求
            continue

        mean_ret = subset["intraday_ret"].mean()
        win_rate = (subset["intraday_ret"] > 0).mean()
        count = len(subset)

        # 综合得分 = 收益 * 胜率 * log(样本量)
        score = mean_ret * win_rate * np.log10(count) if mean_ret > 0 else 0

        results.append(
            {
                "type": open_type,
                "count": count,
                "mean_ret": mean_ret,
                "win_rate": win_rate,
                "score": score,
            }
        )

    results_df = pd.DataFrame(results).sort_values("score", ascending=False)
    print("\n排名 | 开盘类型 | 样本量 | 日内均值 | 胜率 | 综合得分")
    print("-" * 60)
    for i, row in results_df.iterrows():
        print(
            f"  {results_df.index.tolist().index(i) + 1}  | {row['type']:12} | {int(row['count']):6} | {row['mean_ret']:7.2f}% | {row['win_rate'] * 100:5.1f}% | {row['score']:7.2f}"
        )

    # 3.8 样本外最佳结构
    print("\n### 3.8 样本外最佳结构 (2024-2025) ###")
    out_results = []
    for open_type in OPEN_TYPES.keys():
        subset = out_sample[out_sample["open_type"] == open_type]
        if len(subset) < 5:
            continue

        mean_ret = subset["intraday_ret"].mean()
        win_rate = (subset["intraday_ret"] > 0).mean()
        count = len(subset)
        score = mean_ret * win_rate * np.log10(count) if mean_ret > 0 else 0

        out_results.append(
            {
                "type": open_type,
                "count": count,
                "mean_ret": mean_ret,
                "win_rate": win_rate,
                "score": score,
            }
        )

    out_results_df = pd.DataFrame(out_results).sort_values("score", ascending=False)
    print("\n排名 | 开盘类型 | 样本量 | 日内均值 | 胜率 | 综合得分")
    print("-" * 60)
    for i, row in out_results_df.iterrows():
        print(
            f"  {out_results_df.index.tolist().index(i) + 1}  | {row['type']:12} | {int(row['count']):6} | {row['mean_ret']:7.2f}% | {row['win_rate'] * 100:5.1f}% | {row['score']:7.2f}"
        )

print("\n" + "=" * 80)
print("分析完成!")
print("=" * 80)
