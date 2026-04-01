# 因子有效性全面验证测试
# 测试多种因子组合在234板策略上的边际贡献

from jqdata import *
from jqfactor import *
from jqlib.technical_analysis import *
import pandas as pd
import numpy as np

print("=" * 60)
print("因子有效性全面验证测试")
print("基于93策略(234板)逻辑")
print("=" * 60)

# ========== 配置 ==========
test_start = "2024-01-01"
test_end = "2024-06-30"  # 测试半年数据
sample_days = 60  # 抽样60个交易日

print(f"\n测试区间: {test_start} 到 {test_end}")
print(f"抽样天数: {sample_days}")


# ========== 因子定义 ==========
def get_factor_market_cap(stock, date):
    """流通市值(亿)"""
    try:
        q = query(valuation.circulating_market_cap).filter(valuation.code == stock)
        df = get_fundamentals(q, date)
        if len(df) > 0:
            return df.iloc[0, 0]
    except:
        pass
    return None


def get_factor_turnover(stock, date):
    """换手率(%)"""
    try:
        hsl = HSL([stock], date)[0]
        return hsl.get(stock, None)
    except:
        pass
    return None


def get_factor_volume_ratio(stock, date):
    """量比(当日/昨日)"""
    try:
        df = get_price(stock, end_date=date, count=2, fields=["volume"], panel=False)
        if len(df) >= 2:
            return df.iloc[-1]["volume"] / max(df.iloc[-2]["volume"], 1)
    except:
        pass
    return None


def get_factor_relative_position(stock, date, days=15):
    """相对位置(0-1, 越低越好)"""
    try:
        df = get_price(
            stock,
            end_date=date,
            fields=["high", "low", "close"],
            count=days,
            panel=False,
            skip_paused=False,
        )
        if len(df) > 0:
            h, l, c = df["high"].max(), df["low"].min(), df["close"].iloc[-1]
            if h > l:
                return (c - l) / (h - l)
    except:
        pass
    return None


def get_factor_left_pressure(stock, date, days=60):
    """左压突破(0/1)"""
    try:
        df = get_price(
            stock,
            end_date=date,
            fields=["close", "high"],
            count=days,
            panel=False,
            skip_paused=False,
        )
        if len(df) > 0:
            return 1 if df["close"].iloc[-1] >= df["high"].max() else 0
    except:
        pass
    return None


def get_factor_consecutive_board(stock, date):
    """连板数"""
    try:
        df = get_price(
            stock, end_date=date, count=10, fields=["close", "high_limit"], panel=False
        )
        count = 0
        for i in range(len(df) - 1, -1, -1):
            if df["close"].iloc[i] == df["high_limit"].iloc[i]:
                count += 1
            else:
                break
        return count if count > 0 else 0
    except:
        pass
    return 0


# ========== 基础信号获取 ==========
def get_base_signals(date):
    """获取基础信号: 昨日涨停的非ST非新股"""
    try:
        # 股票池
        stocks = get_all_securities("stock", date).index.tolist()
        stocks = [s for s in stocks if s[:2] != "68" and s[0] not in ["4", "8"]]

        # 过滤新股
        result = []
        for s in stocks[:2000]:  # 限制数量加速
            try:
                info = get_security_info(s)
                if (pd.Timestamp(date) - info.start_date).days > 250:
                    result.append(s)
            except:
                pass
        stocks = result

        # 过滤ST
        is_st = get_extras("is_st", stocks, start_date=date, end_date=date, df=True)
        if not is_st.empty:
            st_stocks = is_st.T[is_st.iloc[0] == True].index.tolist()
            stocks = [s for s in stocks if s not in st_stocks]

        # 昨日涨停
        df = get_price(
            stocks,
            end_date=date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        df = df.dropna()
        df = df[df["close"] == df["high_limit"]]

        return list(df["code"])
    except Exception as e:
        print(f"获取基础信号错误: {e}")
        return []


# ========== 计算次日收益 ==========
def calc_next_day_return(stock, buy_date):
    """计算次日开盘买入收盘卖出的收益"""
    try:
        trade_days = get_trade_days(
            buy_date,
            (pd.Timestamp(buy_date) + pd.Timedelta(days=5)).strftime("%Y-%m-%d"),
        )
        if len(trade_days) < 2:
            return None
        sell_date = trade_days[trade_days > pd.Timestamp(buy_date)][0].strftime(
            "%Y-%m-%d"
        )

        df = get_price(
            stock, end_date=sell_date, count=1, fields=["open", "close"], panel=False
        )
        if len(df) > 0:
            return (df["close"].iloc[0] / df["open"].iloc[0] - 1) * 100
    except:
        pass
    return None


# ========== 因子组合测试 ==========
def test_factor_combination(signals, date, factor_filters=None, factor_weights=None):
    """
    测试因子组合
    factor_filters: {'market_cap': 50, 'turnover': 30} 硬过滤阈值
    factor_weights: {'market_cap': 0.4, 'turnover': 0.3} 排序权重
    """
    if not signals:
        return {"count": 0, "avg_ret": 0, "win_rate": 0, "returns": []}

    filtered = signals.copy()
    filter_counts = {"original": len(signals)}

    # 硬过滤
    if factor_filters:
        if "market_cap" in factor_filters:
            caps = []
            for s in filtered:
                cap = get_factor_market_cap(s, date)
                if cap is not None and cap < factor_filters["market_cap"]:
                    caps.append(s)
            filtered = caps
            filter_counts["after_cap"] = len(filtered)

        if "turnover" in factor_filters:
            turns = []
            for s in filtered:
                t = get_factor_turnover(s, date)
                if t is not None and t < factor_filters["turnover"]:
                    turns.append(s)
            filtered = turns
            filter_counts["after_turnover"] = len(filtered)

        if "relative_position" in factor_filters:
            poss = []
            for s in filtered:
                p = get_factor_relative_position(s, date)
                if p is not None and p < factor_filters["relative_position"]:
                    poss.append(s)
            filtered = poss
            filter_counts["after_position"] = len(filtered)

    if not filtered:
        return {
            "count": 0,
            "avg_ret": 0,
            "win_rate": 0,
            "returns": [],
            "filter_counts": filter_counts,
        }

    # 排序打分
    if factor_weights:
        scored = []
        for s in filtered:
            score = 0
            total_weight = 0

            if "market_cap" in factor_weights:
                cap = get_factor_market_cap(s, date)
                if cap is not None:
                    score += (1 - cap / 100) * factor_weights["market_cap"]
                    total_weight += factor_weights["market_cap"]

            if "turnover" in factor_weights:
                t = get_factor_turnover(s, date)
                if t is not None:
                    score += (1 - t / 50) * factor_weights["turnover"]
                    total_weight += factor_weights["turnover"]

            if "relative_position" in factor_weights:
                p = get_factor_relative_position(s, date)
                if p is not None:
                    score += (1 - p) * factor_weights["relative_position"]
                    total_weight += factor_weights["relative_position"]

            if "left_pressure" in factor_weights:
                lp = get_factor_left_pressure(s, date)
                if lp is not None:
                    score += lp * factor_weights["left_pressure"]
                    total_weight += factor_weights["left_pressure"]

            if total_weight > 0:
                scored.append((s, score / total_weight))

        if scored:
            scored.sort(key=lambda x: x[1], reverse=True)
            filtered = [s for s, _ in scored[:5]]  # 取Top5

    # 计算收益
    returns = []
    for s in filtered:
        ret = calc_next_day_return(s, date)
        if ret is not None:
            returns.append(ret)

    if returns:
        return {
            "count": len(filtered),
            "avg_ret": np.mean(returns),
            "win_rate": sum(1 for r in returns if r > 0) / len(returns) * 100,
            "returns": returns,
            "filter_counts": filter_counts,
        }

    return {
        "count": len(filtered),
        "avg_ret": 0,
        "win_rate": 0,
        "returns": [],
        "filter_counts": filter_counts,
    }


# ========== 主测试逻辑 ==========
print("\n开始执行测试...")

# 获取测试日期
all_days = get_trade_days(test_start, test_end)
test_days = all_days[:: max(1, len(all_days) // sample_days)][:sample_days]
print(f"实际测试天数: {len(test_days)}")

# 定义测试组合
test_configs = [
    {"name": "A_无增强", "filters": None, "weights": None},
    {"name": "B_市值过滤<30亿", "filters": {"market_cap": 30}, "weights": None},
    {"name": "C_市值过滤<50亿", "filters": {"market_cap": 50}, "weights": None},
    {"name": "D_换手率过滤<30%", "filters": {"turnover": 30}, "weights": None},
    {
        "name": "E_市值+换手双过滤",
        "filters": {"market_cap": 50, "turnover": 30},
        "weights": None,
    },
    {
        "name": "F_市值+换手+位置三过滤",
        "filters": {"market_cap": 50, "turnover": 30, "relative_position": 0.5},
        "weights": None,
    },
    {"name": "G_市值排序(40%)", "filters": None, "weights": {"market_cap": 0.4}},
    {"name": "H_换手率排序(40%)", "filters": None, "weights": {"turnover": 0.4}},
    {"name": "I_位置排序(40%)", "filters": None, "weights": {"relative_position": 0.4}},
    {
        "name": "J_市值+换手排序(各40%)",
        "filters": None,
        "weights": {"market_cap": 0.4, "turnover": 0.4},
    },
    {
        "name": "K_市值+换手+位置排序",
        "filters": None,
        "weights": {"market_cap": 0.4, "turnover": 0.3, "relative_position": 0.3},
    },
    {
        "name": "L_市值过滤+排序组合",
        "filters": {"market_cap": 50},
        "weights": {"turnover": 0.4, "relative_position": 0.3},
    },
    {
        "name": "M_市值过滤<30亿+排序",
        "filters": {"market_cap": 30},
        "weights": {"turnover": 0.4, "relative_position": 0.3},
    },
]

# 初始化结果
results = {
    cfg["name"]: {"total_signals": 0, "total_returns": [], "wins": 0, "days": 0}
    for cfg in test_configs
}

# 执行测试
for i, day in enumerate(test_days):
    ds = day.strftime("%Y-%m-%d")

    # 获取基础信号
    base_signals = get_base_signals(ds)

    if not base_signals:
        continue

    if i % 10 == 0:
        print(f"进度: {i + 1}/{len(test_days)} - {ds} - 基础信号: {len(base_signals)}")

    # 测试各组合
    for cfg in test_configs:
        result = test_factor_combination(
            base_signals,
            ds,
            factor_filters=cfg["filters"],
            factor_weights=cfg["weights"],
        )

        if result["count"] > 0:
            results[cfg["name"]]["total_signals"] += result["count"]
            results[cfg["name"]]["total_returns"].extend(result["returns"])
            results[cfg["name"]]["wins"] += sum(1 for r in result["returns"] if r > 0)
            results[cfg["name"]]["days"] += 1

# ========== 输出结果 ==========
print("\n" + "=" * 80)
print("因子有效性验证结果")
print("=" * 80)

summary = []
for cfg in test_configs:
    r = results[cfg["name"]]
    if r["total_returns"]:
        avg_ret = np.mean(r["total_returns"])
        win_rate = r["wins"] / len(r["total_returns"]) * 100
        max_ret = max(r["total_returns"])
        min_ret = min(r["total_returns"])
    else:
        avg_ret = win_rate = max_ret = min_ret = 0

    summary.append(
        {
            "name": cfg["name"],
            "signals": r["total_signals"],
            "days": r["days"],
            "avg_ret": avg_ret,
            "win_rate": win_rate,
            "max_ret": max_ret,
            "min_ret": min_ret,
        }
    )

# 排序输出
summary.sort(key=lambda x: x["avg_ret"], reverse=True)

print(
    f"\n{'组合名称':<25} {'信号数':>8} {'天数':>6} {'平均收益':>10} {'胜率':>8} {'最大收益':>10} {'最大亏损':>10}"
)
print("-" * 80)
for s in summary:
    print(
        f"{s['name']:<25} {s['signals']:>8} {s['days']:>6} {s['avg_ret']:>9.2f}% {s['win_rate']:>7.1f}% {s['max_ret']:>9.2f}% {s['min_ret']:>9.2f}%"
    )

# 找出最优组合
best = summary[0]
worst = summary[-1]

print("\n" + "=" * 80)
print("关键发现:")
print(
    f"  最优组合: {best['name']} - 平均收益 {best['avg_ret']:.2f}%, 胜率 {best['win_rate']:.1f}%"
)
print(
    f"  最差组合: {worst['name']} - 平均收益 {worst['avg_ret']:.2f}%, 胜率 {worst['win_rate']:.1f}%"
)
print(f"  收益差异: {best['avg_ret'] - worst['avg_ret']:.2f}个百分点")
print("=" * 80)

print("\n测试完成!")
