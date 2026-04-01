# 因子有效性全面验证测试 v2
# 修复版 - 测试多种因子组合

from jqdata import *
from jqfactor import *
from jqlib.technical_analysis import *
import pandas as pd
import numpy as np

print("=" * 60)
print("因子有效性全面验证测试 v2")
print("=" * 60)

# ========== 配置 ==========
test_start = "2023-07-01"
test_end = "2024-06-30"
sample_days = 40  # 减少抽样天数加速

print(f"\n测试区间: {test_start} 到 {test_end}")
print(f"抽样天数: {sample_days}")


# ========== 基础信号获取(简化版) ==========
def get_zt_stocks(date):
    """获取昨日涨停股票(简化版)"""
    try:
        # 获取全部A股
        all_stocks = get_all_securities("stock", date).index.tolist()

        # 过滤科创和北交所
        stocks = [s for s in all_stocks if s[:2] != "68" and s[0] not in ["4", "8"]]

        # 批量获取价格
        df = get_price(
            stocks,
            end_date=date,
            frequency="daily",
            fields=["close", "high_limit", "paused"],
            count=1,
            panel=False,
        )

        # 过滤停牌
        df = df[df["paused"] == 0]

        # 找涨停
        df = df[df["close"] == df["high_limit"]]

        return list(df["code"])
    except Exception as e:
        print(f"获取涨停股错误 {date}: {e}")
        return []


# ========== 因子函数 ==========
def get_factors_batch(stocks, date):
    """批量获取因子"""
    if not stocks:
        return pd.DataFrame()

    factors = {}

    # 1. 流通市值
    try:
        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code.in_(stocks)
        )
        cap_df = get_fundamentals(q, date)
        factors["market_cap"] = cap_df.set_index("code")[
            "circulating_market_cap"
        ].to_dict()
    except:
        factors["market_cap"] = {}

    # 2. 换手率
    try:
        hsl_df = HSL(stocks, date)
        factors["turnover"] = {s: hsl_df[0].get(s, None) for s in stocks}
    except:
        factors["turnover"] = {}

    # 3. 相对位置(15日)
    try:
        pos_dict = {}
        for s in stocks[:200]:  # 限制数量
            try:
                df = get_price(
                    s,
                    end_date=date,
                    fields=["high", "low", "close"],
                    count=15,
                    panel=False,
                    skip_paused=False,
                )
                if len(df) > 5:
                    h, l, c = df["high"].max(), df["low"].min(), df["close"].iloc[-1]
                    if h > l:
                        pos_dict[s] = (c - l) / (h - l)
            except:
                pass
        factors["relative_position"] = pos_dict
    except:
        factors["relative_position"] = {}

    # 4. 左压突破(60日)
    try:
        lp_dict = {}
        for s in stocks[:100]:  # 限制数量
            try:
                df = get_price(
                    s,
                    end_date=date,
                    fields=["close", "high"],
                    count=60,
                    panel=False,
                    skip_paused=False,
                )
                if len(df) > 10:
                    lp_dict[s] = 1 if df["close"].iloc[-1] >= df["high"].max() else 0
            except:
                pass
        factors["left_pressure"] = lp_dict
    except:
        factors["left_pressure"] = {}

    return factors


# ========== 计算收益 ==========
def calc_returns_batch(stocks, buy_date):
    """批量计算次日收益"""
    if not stocks:
        return {}

    returns = {}
    try:
        # 获取未来2天的数据
        end_date = (pd.Timestamp(buy_date) + pd.Timedelta(days=10)).strftime("%Y-%m-%d")
        trade_days = get_trade_days(buy_date, end_date)

        if len(trade_days) < 2:
            return {}

        sell_date = trade_days[1].strftime("%Y-%m-%d")

        # 批量获取开盘价和收盘价
        for s in stocks[:50]:  # 限制数量
            try:
                df = get_price(
                    s,
                    end_date=sell_date,
                    count=1,
                    fields=["open", "close"],
                    panel=False,
                )
                if len(df) > 0:
                    ret = (df["close"].iloc[0] / df["open"].iloc[0] - 1) * 100
                    returns[s] = ret
            except:
                pass
    except:
        pass

    return returns


# ========== 因子测试 ==========
def apply_factor_filter(stocks, factors, filter_config):
    """应用因子过滤"""
    if not filter_config:
        return stocks

    filtered = stocks.copy()

    for factor_name, threshold in filter_config.items():
        if factor_name not in factors:
            continue

        factor_values = factors[factor_name]
        new_filtered = []

        for s in filtered:
            val = factor_values.get(s)
            if val is not None and val < threshold:
                new_filtered.append(s)

        filtered = new_filtered

    return filtered


def apply_factor_sort(stocks, factors, weight_config, top_n=5):
    """应用因子排序"""
    if not weight_config:
        return stocks[:top_n]

    scored = []

    for s in stocks:
        score = 0
        total_weight = 0

        for factor_name, weight in weight_config.items():
            if factor_name not in factors:
                continue

            val = factors[factor_name].get(s)
            if val is None:
                continue

            # 归一化因子值(越小越好)
            if factor_name == "market_cap":
                norm_val = max(0, 1 - val / 100)
            elif factor_name == "turnover":
                norm_val = max(0, 1 - val / 50)
            elif factor_name == "relative_position":
                norm_val = 1 - val
            elif factor_name == "left_pressure":
                norm_val = val
            else:
                norm_val = val

            score += norm_val * weight
            total_weight += weight

        if total_weight > 0:
            scored.append((s, score / total_weight))

    if scored:
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:top_n]]

    return stocks[:top_n]


# ========== 主测试 ==========
print("\n开始执行测试...")

# 测试日期
all_days = get_trade_days(test_start, test_end)
step = max(1, len(all_days) // sample_days)
test_days = all_days[::step][:sample_days]
print(f"实际测试天数: {len(test_days)}")

# 测试配置
configs = [
    {"name": "A_无增强", "filter": None, "weight": None},
    {"name": "B_市值<30亿", "filter": {"market_cap": 30}, "weight": None},
    {"name": "C_市值<50亿", "filter": {"market_cap": 50}, "weight": None},
    {"name": "D_换手<20%", "filter": {"turnover": 20}, "weight": None},
    {"name": "E_换手<30%", "filter": {"turnover": 30}, "weight": None},
    {"name": "F_位置<0.3", "filter": {"relative_position": 0.3}, "weight": None},
    {
        "name": "G_市值+换手",
        "filter": {"market_cap": 50, "turnover": 30},
        "weight": None,
    },
    {"name": "H_市值排序", "filter": None, "weight": {"market_cap": 1.0}},
    {"name": "I_换手排序", "filter": None, "weight": {"turnover": 1.0}},
    {"name": "J_位置排序", "filter": None, "weight": {"relative_position": 1.0}},
    {
        "name": "K_市值+换手排序",
        "filter": None,
        "weight": {"market_cap": 0.5, "turnover": 0.5},
    },
    {
        "name": "L_三因子排序",
        "filter": None,
        "weight": {"market_cap": 0.4, "turnover": 0.3, "relative_position": 0.3},
    },
    {
        "name": "M_过滤+排序",
        "filter": {"market_cap": 50},
        "weight": {"turnover": 0.5, "relative_position": 0.5},
    },
]

# 结果统计
results = {cfg["name"]: {"signals": 0, "returns": [], "wins": 0} for cfg in configs}

# 执行测试
for i, day in enumerate(test_days):
    ds = day.strftime("%Y-%m-%d")

    # 获取涨停股
    zt_stocks = get_zt_stocks(ds)

    if not zt_stocks:
        continue

    # 获取因子
    factors = get_factors_batch(zt_stocks, ds)

    # 获取次日收益
    next_returns = calc_returns_batch(zt_stocks, ds)

    if i % 5 == 0:
        print(f"进度: {i + 1}/{len(test_days)} - {ds} - 涨停数: {len(zt_stocks)}")

    # 测试各配置
    for cfg in configs:
        # 过滤
        filtered = apply_factor_filter(zt_stocks, factors, cfg["filter"])

        # 排序
        if cfg["weight"]:
            filtered = apply_factor_sort(filtered, factors, cfg["weight"], top_n=5)
        else:
            filtered = filtered[:5]  # 默认取前5个

        # 计算收益
        for s in filtered:
            if s in next_returns:
                ret = next_returns[s]
                results[cfg["name"]]["signals"] += 1
                results[cfg["name"]]["returns"].append(ret)
                if ret > 0:
                    results[cfg["name"]]["wins"] += 1

# ========== 输出结果 ==========
print("\n" + "=" * 90)
print("因子有效性验证结果")
print("=" * 90)

summary = []
for cfg in configs:
    r = results[cfg["name"]]
    n = r["signals"]
    if n > 0:
        avg_ret = np.mean(r["returns"])
        win_rate = r["wins"] / n * 100
        max_ret = max(r["returns"])
        min_ret = min(r["returns"])
    else:
        avg_ret = win_rate = max_ret = min_ret = 0

    summary.append(
        {
            "name": cfg["name"],
            "signals": n,
            "avg_ret": avg_ret,
            "win_rate": win_rate,
            "max_ret": max_ret,
            "min_ret": min_ret,
        }
    )

# 按收益排序
summary.sort(key=lambda x: x["avg_ret"], reverse=True)

print(
    f"\n{'组合':<20} {'信号数':>8} {'平均收益':>10} {'胜率':>8} {'最大收益':>10} {'最大亏损':>10}"
)
print("-" * 90)
for s in summary:
    print(
        f"{s['name']:<20} {s['signals']:>8} {s['avg_ret']:>9.2f}% {s['win_rate']:>7.1f}% {s['max_ret']:>9.2f}% {s['min_ret']:>9.2f}%"
    )

# 分析
best = summary[0]
baseline = next(s for s in summary if s["name"] == "A_无增强")

print("\n" + "=" * 90)
print("关键发现:")
print(
    f"  基准(无增强): 平均收益 {baseline['avg_ret']:.2f}%, 胜率 {baseline['win_rate']:.1f}%"
)
print(
    f"  最优组合: {best['name']} - 平均收益 {best['avg_ret']:.2f}%, 胜率 {best['win_rate']:.1f}%"
)
print(f"  收益提升: {best['avg_ret'] - baseline['avg_ret']:.2f}个百分点")
print(f"  胜率提升: {best['win_rate'] - baseline['win_rate']:.1f}个百分点")
print("=" * 90)

print("\n测试完成!")
