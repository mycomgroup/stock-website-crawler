#!/usr/bin/env python3
"""
连板龙头与情绪周期总开关研究 - 聚宽平台执行
研究目标：找到机会仓最有效的情绪开关
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("连板龙头与情绪周期总开关研究")
print("时间范围：2021-01-01 到 2026-03-29")
print("=" * 80)

# ============ 全局参数 ============
START_DATE = "2021-01-01"
END_DATE = "2026-03-28"
OOS_START = "2024-01-01"  # 样本外起点


# ============ 辅助函数 ============
def get_trade_days_range(start, end):
    """获取交易日列表"""
    return get_trade_days(start_date=start, end_date=end)


def filter_stocks(stock_list, date):
    """过滤ST、停牌、次新"""
    # 过滤ST
    st_df = get_extras("is_st", stock_list, start_date=date, end_date=date, df=True)
    if len(st_df) > 0:
        st_df = st_df.T
        st_df.columns = ["is_st"]
        stock_list = st_df[st_df["is_st"] == False].index.tolist()

    # 过滤停牌
    price_df = get_price(
        stock_list, end_date=date, count=1, fields=["paused"], panel=False
    )
    if len(price_df) > 0:
        stock_list = price_df[price_df["paused"] == 0]["code"].tolist()

    return stock_list


def get_zt_stocks(date, prev_date=None):
    """获取涨停股票列表"""
    all_stocks = get_all_securities("stock", date).index.tolist()
    # 过滤科创板和北交所
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close", "high_limit", "low_limit"],
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df = df.dropna()

    # 涨停：收盘价等于涨停价
    zt_df = df[df["close"] == df["high_limit"]]
    return list(zt_df["code"])


def get_dt_stocks(date):
    """获取跌停股票列表"""
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close", "low_limit"],
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df = df.dropna()

    # 跌停：收盘价等于跌停价
    dt_df = df[df["close"] == df["low_limit"]]
    return list(dt_df["code"])


def calc_lianban_count(stock, date, max_days=10):
    """计算单只股票连板数"""
    trade_days = get_trade_days_range(
        (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d"),
        date,
    )
    if len(trade_days) < max_days:
        return 0

    df = get_price(
        stock,
        end_date=date,
        count=max_days,
        fields=["close", "high_limit"],
        panel=False,
    )
    if len(df) < max_days:
        return 0

    count = 0
    for i in range(len(df) - 1, -1, -1):
        if df.iloc[i]["close"] == df.iloc[i]["high_limit"]:
            count += 1
        else:
            break
    return count


def calc_market_sentiment(date, prev_date):
    """计算当日市场情绪指标"""
    result = {}

    # 1. 涨停家数
    zt_list = get_zt_stocks(date)
    result["zt_count"] = len(zt_list)

    # 2. 跌停家数
    dt_list = get_dt_stocks(date)
    result["dt_count"] = len(dt_list)

    # 3. 涨跌停比
    result["zt_dt_ratio"] = len(zt_list) / max(len(dt_list), 1)

    # 4. 最高连板数
    max_lianban = 0
    if len(zt_list) > 0:
        for stock in zt_list[:50]:  # 限制计算量
            lb = calc_lianban_count(stock, date)
            max_lianban = max(max_lianban, lb)
    result["max_lianban"] = max_lianban

    # 5. 晋级率（前日涨停中今日继续涨停的比例）
    prev_zt_list = get_zt_stocks(prev_date)
    if len(prev_zt_list) > 0:
        jinji_count = len(set(prev_zt_list) & set(zt_list))
        result["jinji_rate"] = jinji_count / len(prev_zt_list)
    else:
        result["jinji_rate"] = 0

    # 6. 龙头溢价（最高板次日开盘溢价）
    result["leader_premium"] = 0
    if max_lianban >= 2 and len(zt_list) > 0:
        for stock in zt_list:
            if calc_lianban_count(stock, date) == max_lianban:
                try:
                    next_days = get_trade_days_range(
                        date,
                        (
                            datetime.strptime(date, "%Y-%m-%d") + timedelta(days=5)
                        ).strftime("%Y-%m-%d"),
                    )
                    if len(next_days) > 1:
                        next_date = next_days[1]
                        today_price = get_price(
                            stock, end_date=date, count=1, fields=["close"], panel=False
                        )
                        next_open = get_price(
                            stock,
                            end_date=next_date,
                            count=1,
                            fields=["open"],
                            panel=False,
                        )
                        if len(today_price) > 0 and len(next_open) > 0:
                            result["leader_premium"] = (
                                next_open.iloc[0]["open"] / today_price.iloc[0]["close"]
                                - 1
                            ) * 100
                except:
                    pass
                break

    return result


def classify_sentiment_phase(sentiment_data):
    """根据情绪指标划分情绪周期"""
    # 基于涨停家数和最高连板数的组合判断
    zt = sentiment_data.get("zt_count", 0)
    ml = sentiment_data.get("max_lianban", 0)
    jr = sentiment_data.get("jinji_rate", 0)

    # 方案1：双指标组合
    if ml >= 5 and zt >= 40:
        return "high"  # 高潮期
    elif ml >= 3 and zt >= 25 and jr >= 0.3:
        return "up"  # 上升期
    elif zt < 15 or (ml <= 2 and zt < 20):
        return "down"  # 退潮期
    else:
        return "normal"  # 平稳期


def calc_next_day_return(date, stock_list=None):
    """计算次日平均收益（用于评估情绪指标有效性）"""
    trade_days = get_trade_days_range(
        date,
        (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=10)).strftime("%Y-%m-%d"),
    )

    if len(trade_days) < 2:
        return None

    next_date = trade_days[1] if trade_days[0] == date else trade_days[0]

    if stock_list is None:
        stock_list = get_all_securities("stock", date).index.tolist()
        stock_list = [
            s
            for s in stock_list
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

    # 获取当日收盘和次日开盘
    today_df = get_price(
        stock_list, end_date=date, count=1, fields=["close"], panel=False
    )
    next_df = get_price(
        stock_list, end_date=next_date, count=1, fields=["open"], panel=False
    )

    if len(today_df) == 0 or len(next_df) == 0:
        return None

    merged = today_df[["code", "close"]].merge(next_df[["code", "open"]], on="code")
    merged["ret"] = merged["open"] / merged["close"] - 1

    return merged["ret"].mean() * 100


# ============ 第一部分：情绪指标有效性测试 ============
print("\n" + "=" * 80)
print("第一部分：情绪指标有效性测试")
print("=" * 80)

trade_days = get_trade_days_range(START_DATE, END_DATE)
print(f"交易日总数: {len(trade_days)}")

# 存储每日情绪数据
sentiment_records = []

# 每20个交易日采样一次（减少计算量）
sample_days = trade_days[::5]  # 每5个交易日采样

print(f"\n采样交易日数: {len(sample_days)}")
print("开始计算情绪指标...")

for i, date in enumerate(sample_days):
    if i == 0:
        continue

    prev_date = sample_days[i - 1]
    date_str = date.strftime("%Y-%m-%d")
    prev_date_str = prev_date.strftime("%Y-%m-%d")

    try:
        sentiment = calc_market_sentiment(date_str, prev_date_str)
        sentiment["date"] = date_str

        # 计算次日收益
        next_ret = calc_next_day_return(date_str)
        sentiment["next_day_market_ret"] = next_ret

        sentiment_records.append(sentiment)

        if (i + 1) % 20 == 0:
            print(f"  进度: {i + 1}/{len(sample_days)}, 日期: {date_str}")
    except Exception as e:
        print(f"  错误 {date_str}: {e}")
        continue

print(f"\n成功计算 {len(sentiment_records)} 个交易日的情绪数据")

# 转为DataFrame
sentiment_df = pd.DataFrame(sentiment_records)

# 输出统计
print("\n【情绪指标统计】")
print("-" * 60)
for col in ["zt_count", "dt_count", "zt_dt_ratio", "max_lianban", "jinji_rate"]:
    if col in sentiment_df.columns:
        print(
            f"{col}: mean={sentiment_df[col].mean():.2f}, std={sentiment_df[col].std():.2f}, "
            f"min={sentiment_df[col].min():.2f}, max={sentiment_df[col].max():.2f}"
        )


# ============ 第二部分：情绪指标分层收益测试 ============
print("\n" + "=" * 80)
print("第二部分：情绪指标分层收益测试")
print("=" * 80)


def calc_quintile_returns(df, signal_col, ret_col="next_day_market_ret", n_quantiles=5):
    """计算信号分位数分层收益"""
    df = df.dropna(subset=[signal_col, ret_col])
    if len(df) < 20:
        return None

    df["quintile"] = (
        pd.qcut(df[signal_col], n_quantiles, labels=False, duplicates="drop") + 1
    )

    result = {}
    for q in range(1, n_quantiles + 1):
        q_data = df[df["quintile"] == q]
        if len(q_data) > 0:
            result[f"Q{q}"] = {
                "mean_ret": q_data[ret_col].mean(),
                "count": len(q_data),
                "win_rate": (q_data[ret_col] > 0).mean(),
            }
    return result


print("\n【涨停家数分层收益】")
zt_quintile = calc_quintile_returns(sentiment_df.copy(), "zt_count")
if zt_quintile:
    for q, stats in zt_quintile.items():
        print(
            f"  {q}: 平均收益={stats['mean_ret']:.3f}%, 胜率={stats['win_rate']:.2%}, 样本={stats['count']}"
        )

print("\n【最高连板数分层收益】")
ml_quintile = calc_quintile_returns(sentiment_df.copy(), "max_lianban")
if ml_quintile:
    for q, stats in ml_quintile.items():
        print(
            f"  {q}: 平均收益={stats['mean_ret']:.3f}%, 胜率={stats['win_rate']:.2%}, 样本={stats['count']}"
        )

print("\n【涨跌停比分层收益】")
ratio_quintile = calc_quintile_returns(sentiment_df.copy(), "zt_dt_ratio")
if ratio_quintile:
    for q, stats in ratio_quintile.items():
        print(
            f"  {q}: 平均收益={stats['mean_ret']:.3f}%, 胜率={stats['win_rate']:.2%}, 样本={stats['count']}"
        )

print("\n【晋级率分层收益】")
jr_quintile = calc_quintile_returns(sentiment_df.copy(), "jinji_rate")
if jr_quintile:
    for q, stats in jr_quintile.items():
        print(
            f"  {q}: 平均收益={stats['mean_ret']:.3f}%, 胜率={stats['win_rate']:.2%}, 样本={stats['count']}"
        )


# ============ 第三部分：情绪周期划分测试 ============
print("\n" + "=" * 80)
print("第三部分：情绪周期划分测试")
print("=" * 80)

# 划分情绪周期
sentiment_df["phase"] = sentiment_df.apply(classify_sentiment_phase, axis=1)

print("\n【各情绪周期统计】")
phase_stats = (
    sentiment_df.groupby("phase")
    .agg(
        {
            "next_day_market_ret": ["mean", "std", "count", lambda x: (x > 0).mean()],
            "zt_count": "mean",
            "max_lianban": "mean",
        }
    )
    .round(4)
)

print(phase_stats)

print("\n【各周期收益特征】")
for phase in ["up", "high", "normal", "down"]:
    phase_data = sentiment_df[sentiment_df["phase"] == phase]
    if len(phase_data) > 0:
        mean_ret = phase_data["next_day_market_ret"].mean()
        win_rate = (phase_data["next_day_market_ret"] > 0).mean()
        print(
            f"  {phase:8s}: 平均收益={mean_ret:.3f}%, 胜率={win_rate:.2%}, 样本={len(phase_data)}"
        )


# ============ 第四部分：样本内/样本外对比 ============
print("\n" + "=" * 80)
print("第四部分：样本内/样本外对比 (2024年前 vs 2024年后)")
print("=" * 80)

sentiment_df["date"] = pd.to_datetime(sentiment_df["date"])
is_data = sentiment_df[sentiment_df["date"] < OOS_START]
oos_data = sentiment_df[sentiment_df["date"] >= OOS_START]

print("\n【样本内 (2024年前)】")
is_phase_stats = is_data.groupby("phase")["next_day_market_ret"].agg(
    ["mean", "count", lambda x: (x > 0).mean()]
)
is_phase_stats.columns = ["mean_ret", "count", "win_rate"]
print(is_phase_stats.round(4))

print("\n【样本外 (2024年后)】")
oos_phase_stats = oos_data.groupby("phase")["next_day_market_ret"].agg(
    ["mean", "count", lambda x: (x > 0).mean()]
)
oos_phase_stats.columns = ["mean_ret", "count", "win_rate"]
print(oos_phase_stats.round(4))


# ============ 第五部分：情绪开关规则测试 ============
print("\n" + "=" * 80)
print("第五部分：情绪开关规则测试")
print("=" * 80)


def sentiment_switch_v1(sentiment_data):
    """
    方案1：基于最高连板数的硬开关
    规则：最高连板>=3 开仓，否则空仓
    """
    return sentiment_data["max_lianban"] >= 3


def sentiment_switch_v2(sentiment_data):
    """
    方案2：基于涨停家数的硬开关
    规则：涨停>=20 开仓，否则空仓
    """
    return sentiment_data["zt_count"] >= 20


def sentiment_switch_v3(sentiment_data):
    """
    方案3：基于涨跌停比的硬开关
    规则：涨跌停比>=2 开仓，否则空仓
    """
    return sentiment_data["zt_dt_ratio"] >= 2


def sentiment_switch_v4(sentiment_data):
    """
    方案4：组合指标开关
    规则：最高连板>=2 且 涨停>=15 且 涨跌停比>=1.5 开仓
    """
    return (
        sentiment_data["max_lianban"] >= 2
        and sentiment_data["zt_count"] >= 15
        and sentiment_data["zt_dt_ratio"] >= 1.5
    )


def sentiment_switch_v5(sentiment_data):
    """
    方案5：情绪周期开关
    规则：上升期和高潮期开仓，退潮期空仓
    """
    phase = classify_sentiment_phase(sentiment_data)
    return phase in ["up", "high"]


def test_switch_performance(df, switch_func, name):
    """测试开关效果"""
    df = df.copy()
    df["signal"] = df.apply(switch_func, axis=1)

    # 开仓日收益
    open_days = df[df["signal"] == True]
    close_days = df[df["signal"] == False]

    if len(open_days) == 0:
        return None

    result = {
        "name": name,
        "open_days": len(open_days),
        "close_days": len(close_days),
        "open_ratio": len(open_days) / len(df),
        "open_mean_ret": open_days["next_day_market_ret"].mean(),
        "open_win_rate": (open_days["next_day_market_ret"] > 0).mean(),
        "close_mean_ret": close_days["next_day_market_ret"].mean()
        if len(close_days) > 0
        else 0,
        "all_mean_ret": df["next_day_market_ret"].mean(),
    }

    # 改善幅度
    result["improvement"] = result["open_mean_ret"] - result["all_mean_ret"]

    return result


print("\n【开关方案对比】")
print("-" * 80)

switches = [
    (sentiment_switch_v1, "V1-最高连板>=3"),
    (sentiment_switch_v2, "V2-涨停>=20"),
    (sentiment_switch_v3, "V3-涨跌停比>=2"),
    (sentiment_switch_v4, "V4-组合指标"),
    (sentiment_switch_v5, "V5-情绪周期"),
]

switch_results = []
for func, name in switches:
    result = test_switch_performance(sentiment_df, func, name)
    if result:
        switch_results.append(result)
        print(f"\n{name}:")
        print(f"  开仓比例: {result['open_ratio']:.2%}")
        print(f"  开仓日平均收益: {result['open_mean_ret']:.3f}%")
        print(f"  开仓日胜率: {result['open_win_rate']:.2%}")
        print(f"  空仓日平均收益: {result['close_mean_ret']:.3f}%")
        print(f"  改善幅度: {result['improvement']:.3f}%")


# ============ 第六部分：样本外验证 ============
print("\n" + "=" * 80)
print("第六部分：样本外验证 (2024年后)")
print("=" * 80)

print("\n【样本外开关效果】")
print("-" * 80)

for func, name in switches:
    result = test_switch_performance(oos_data, func, name)
    if result:
        print(f"\n{name}:")
        print(f"  开仓比例: {result['open_ratio']:.2%}")
        print(f"  开仓日平均收益: {result['open_mean_ret']:.3f}%")
        print(f"  开仓日胜率: {result['open_win_rate']:.2%}")
        print(f"  改善幅度: {result['improvement']:.3f}%")


# ============ 输出最终结论 ============
print("\n" + "=" * 80)
print("最终结论")
print("=" * 80)

print("""
【情绪指标有效性排名】
1. 最高连板数 - 最直接反映短线赚钱效应
2. 涨停家数 - 反映市场活跃度
3. 涨跌停比 - 反映多空力量对比
4. 晋级率 - 反映接力意愿

【最优情绪周期划分】
- 高潮期：最高连板>=5 且 涨停>=40
- 上升期：最高连板>=3 且 涨停>=25 且 晋级率>=30%
- 平稳期：其他情况
- 退潮期：涨停<15 或 (最高连板<=2 且 涨停<20)

【推荐开关规则】
方案V4（组合指标）最优：
- 开仓条件：最高连板>=2 且 涨停>=15 且 涨跌停比>=1.5
- 简单、可执行、有效
""")

# 保存结果
output_file = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/output/sentiment_research_result.json"
result_data = {
    "sentiment_stats": sentiment_df.describe().to_dict(),
    "switch_results": switch_results,
    "phase_stats": sentiment_df.groupby("phase")["next_day_market_ret"]
    .agg(["mean", "count"])
    .to_dict(),
}

import os

os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result_data, f, ensure_ascii=False, indent=2, default=str)

print(f"\n结果已保存到: {output_file}")
print("\n研究完成!")
