# 状态路由器 v1 设计验证
# 测试目标：对比有路由器 vs 无路由器的效果

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_market_breadth(date):
    """
    计算市场广度：沪深300站上20日线占比
    返回：占比百分比（0-100）
    """
    hs300_stocks = get_index_stocks("000300.XSHG", date)

    if len(hs300_stocks) == 0:
        return 0

    count_above_ma20 = 0

    for stock in hs300_stocks:
        prices = get_price(
            stock,
            end_date=date,
            count=21,
            fields=["close"],
            panel=False,
            fill_paused=False,
        )
        if len(prices) < 21:
            continue

        ma20 = prices["close"].iloc[:20].mean()
        current_close = prices["close"].iloc[-1]

        if current_close > ma20:
            count_above_ma20 += 1

    breadth_pct = count_above_ma20 / len(hs300_stocks) * 100
    return breadth_pct


def get_sentiment_zt_count(date):
    """
    计算情绪指标：涨停家数
    返回：涨停数量
    """
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
    ]

    df = get_price(
        all_stocks,
        end_date=date,
        frequency="daily",
        fields=["paused", "close", "high_limit", "low_limit"],
        count=1,
        panel=False,
        fill_paused=False,
    )

    df = df.dropna()
    df = df[df["paused"] == 0]

    zt_count = len(df[df["close"] == df["high_limit"]]["code"].tolist())
    dt_count = len(df[df["close"] == df["low_limit"]]["code"].tolist())

    return zt_count, dt_count


def classify_breadth(breadth_pct):
    """
    分类市场广度
    返回：极弱(1), 弱(2), 中(3), 强(4)
    """
    if breadth_pct < 15:
        return 1  # 极弱
    elif breadth_pct < 25:
        return 2  # 弱
    elif breadth_pct < 35:
        return 3  # 中
    else:
        return 4  # 强


def classify_sentiment(zt_count):
    """
    分类情绪
    返回：冰点(1), 启动(2), 发酵(3), 高潮(4)
    """
    if zt_count < 30:
        return 1  # 冰点
    elif zt_count < 50:
        return 2  # 启动
    elif zt_count < 80:
        return 3  # 发酵
    else:
        return 4  # 高潮


def get_state_position(breadth_level, sentiment_level):
    """
    状态路由器核心逻辑：根据广度和情绪确定仓位
    返回：(状态名称, 目标仓位百分比)
    """
    # 状态路由表（5种简化状态）
    if breadth_level == 1:  # 极弱
        return ("关闭", 0)

    elif breadth_level == 2:  # 弱
        if sentiment_level <= 2:  # 冰点/启动
            return ("防守", 30)
        else:  # 发酵/高潮
            return ("轻仓", 50)

    elif breadth_level == 3:  # 中
        if sentiment_level == 2:  # 启动
            return ("轻仓", 50)
        elif sentiment_level == 3:  # 发酵
            return ("正常", 70)
        elif sentiment_level == 4:  # 高潮
            return ("进攻", 100)
        else:  # 冰点
            return ("防守", 30)

    else:  # 强
        if sentiment_level == 4:  # 高潮
            return ("进攻", 100)
        elif sentiment_level == 3:  # 发酵
            return ("正常", 70)
        else:  # 启动/冰点
            return ("轻仓", 50)


def simulate_strategy_with_router(start_date, end_date, use_router=True):
    """
    模拟策略运行（使用沪深300作为标的）
    use_router: True使用状态路由器，False始终满仓
    返回：每日净值、状态分布、回撤等指标
    """
    trade_days = get_trade_days(start_date, end_date)

    results = []
    nav = 1.0  # 初始净值
    prev_close = None
    position = 100 if not use_router else 0  # 无路由器始终满仓

    state_distribution = {"关闭": 0, "防守": 0, "轻仓": 0, "正常": 0, "进攻": 0}

    for i, date in enumerate(trade_days):
        # 计算市场状态
        breadth_pct = get_market_breadth(date)
        zt_count, dt_count = get_sentiment_zt_count(date)

        breadth_level = classify_breadth(breadth_pct)
        sentiment_level = classify_sentiment(zt_count)

        # 状态路由器决定仓位
        if use_router:
            state_name, target_position = get_state_position(
                breadth_level, sentiment_level
            )
            position = target_position
            state_distribution[state_name] += 1

        # 获取沪深300当日收益
        hs300_price = get_price(
            "000300.XSHG", end_date=date, count=1, fields=["close", "open"], panel=False
        )

        if hs300_price.empty:
            continue

        day_close = float(hs300_price["close"].iloc[0])
        day_open = float(hs300_price["open"].iloc[0])

        if prev_close is not None:
            # 计算当日收益（实际持有仓位）
            daily_return = (day_close / prev_close - 1) * (position / 100)
            nav = nav * (1 + daily_return)

        prev_close = day_close

        results.append(
            {
                "date": date,
                "breadth_pct": breadth_pct,
                "breadth_level": breadth_level,
                "zt_count": zt_count,
                "sentiment_level": sentiment_level,
                "position": position,
                "nav": nav,
                "daily_return": daily_return if prev_close else 0,
            }
        )

    df = pd.DataFrame(results)

    # 计算回撤
    df["nav_peak"] = df["nav"].cummax()
    df["drawdown"] = (df["nav_peak"] - df["nav"]) / df["nav_peak"]

    max_drawdown = df["drawdown"].max()

    # 计算年化收益
    total_days = len(trade_days)
    years = total_days / 252
    annual_return = (nav - 1) / years if years > 0 else 0

    # 计算夏普比率（简化版）
    daily_returns = df["daily_return"].values
    sharpe = (
        np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252)
        if np.std(daily_returns) > 0
        else 0
    )

    # 计算年度胜率
    df["year"] = pd.to_datetime(df["date"]).dt.year
    yearly_returns = (
        df.groupby("year")["nav"].last() / df.groupby("year")["nav"].first() - 1
    )
    win_years = (yearly_returns > 0).sum()
    total_years = len(yearly_returns)
    year_win_rate = win_years / total_years if total_years > 0 else 0

    return {
        "nav_series": df,
        "final_nav": nav,
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "year_win_rate": year_win_rate,
        "state_distribution": state_distribution if use_router else None,
        "total_days": total_days,
    }


def run_comparison():
    """
    运行对比测试：有路由器 vs 无路由器
    """
    start_date = "2018-01-01"
    end_date = "2025-03-30"

    print("=" * 60)
    print("状态路由器 v1 设计验证")
    print("测试期间: {} 至 {}".format(start_date, end_date))
    print("=" * 60)

    # 1. 有路由器版本
    print("\n[1] 运行有路由器版本...")
    result_with_router = simulate_strategy_with_router(
        start_date, end_date, use_router=True
    )

    # 2. 无路由器版本（基准）
    print("\n[2] 运行无路由器版本...")
    result_without_router = simulate_strategy_with_router(
        start_date, end_date, use_router=False
    )

    # 3. 对比分析
    print("\n" + "=" * 60)
    print("对比结果")
    print("=" * 60)

    print("\n【核心指标对比】")
    print("-" * 60)
    print("指标                  | 有路由器  | 无路由器  | 差异")
    print("-" * 60)

    ann_diff = (
        result_with_router["annual_return"] - result_without_router["annual_return"]
    )
    dd_diff = result_with_router["max_drawdown"] - result_without_router["max_drawdown"]
    sharpe_diff = result_with_router["sharpe"] - result_without_router["sharpe"]

    print(
        "年化收益              | {:.2f}%    | {:.2f}%    | {:.2f}%".format(
            result_with_router["annual_return"] * 100,
            result_without_router["annual_return"] * 100,
            ann_diff * 100,
        )
    )
    print(
        "最大回撤              | {:.2f}%    | {:.2f}%    | {:.2f}%".format(
            result_with_router["max_drawdown"] * 100,
            result_without_router["max_drawdown"] * 100,
            dd_diff * 100,
        )
    )
    print(
        "夏普比率              | {:.2f}     | {:.2f}     | {:.2f}".format(
            result_with_router["sharpe"], result_without_router["sharpe"], sharpe_diff
        )
    )
    print(
        "年度胜率              | {:.1f}%    | {:.1f}%    | {:.1f}%".format(
            result_with_router["year_win_rate"] * 100,
            result_without_router["year_win_rate"] * 100,
            (
                result_with_router["year_win_rate"]
                - result_without_router["year_win_rate"]
            )
            * 100,
        )
    )

    print("\n【状态分布（有路由器）】")
    print("-" * 60)
    if result_with_router["state_distribution"]:
        total_states = sum(result_with_router["state_distribution"].values())
        for state, count in result_with_router["state_distribution"].items():
            pct = count / total_states * 100
            print("{}: {} 天 ({:.1f}%)".format(state, count, pct))

    # 4. 关键问题回答
    print("\n" + "=" * 60)
    print("关键问题回答")
    print("=" * 60)

    print("\n问题1：路由器能否显著降低回撤？")
    dd_improve = (
        (result_without_router["max_drawdown"] - result_with_router["max_drawdown"])
        / result_without_router["max_drawdown"]
        * 100
    )
    if dd_improve > 20:
        print("回答：YES - 回撤降低 {:.1f}%（>{:.0f}%门槛）".format(dd_improve, 20))
    else:
        print("回答：NO - 回撤降低 {:.1f}%（<{:.0f}%门槛）".format(dd_improve, 20))

    print("\n问题2：路由器是否会牺牲过多收益？")
    ann_cost = abs(ann_diff) / result_without_router["annual_return"] * 100
    if ann_cost < 20:
        print("回答：NO - 收益损失 {:.1f}%（<{:.0f}%门槛）".format(ann_cost, 20))
    else:
        print("回答：YES - 收益损失 {:.1f}%（>{:.0f}%门槛）".format(ann_cost, 20))

    print("\n问题3：是否存在过度择时导致错过机会的问题？")
    if result_with_router["state_distribution"]:
        close_pct = (
            result_with_router["state_distribution"]["关闭"] / total_states * 100
        )
        if close_pct > 30:
            print(
                "回答：YES - 关闭状态占比 {:.1f}%（>{:.0f}%门槛）".format(close_pct, 30)
            )
        else:
            print(
                "回答：NO - 关闭状态占比 {:.1f}%（<{:.0f}%门槛）".format(close_pct, 30)
            )

    # 5. 最终评估
    print("\n" + "=" * 60)
    print("最终评估")
    print("=" * 60)

    improvement_score = 0
    if dd_improve > 20:
        improvement_score += 1
        print("✓ 回撤改善显著: {:.1f}%".format(dd_improve))
    else:
        print("✗ 回撤改善不足: {:.1f}%".format(dd_improve))

    if ann_cost < 20:
        improvement_score += 1
        print("✓ 收益损失可控: {:.1f}%".format(ann_cost))
    else:
        print("✗ 收益损失过大: {:.1f}%".format(ann_cost))

    if close_pct < 30:
        improvement_score += 1
        print("✓ 无过度择时: {:.1f}%".format(close_pct))
    else:
        print("✗ 过度择时风险: {:.1f}%".format(close_pct))

    if improvement_score >= 2:
        print("\n最终结论: Go - 状态路由器有效")
    elif improvement_score == 1:
        print("\n最终结论: Watch - 状态路由器需优化")
    else:
        print("\n最终结论: No-Go - 状态路由器效果不佳")

    return {
        "with_router": result_with_router,
        "without_router": result_without_router,
        "dd_improve": dd_improve,
        "ann_cost": ann_cost,
        "close_pct": close_pct,
        "improvement_score": improvement_score,
    }


if __name__ == "__builtins__":
    result = run_comparison()
    print("\n分析完成")
