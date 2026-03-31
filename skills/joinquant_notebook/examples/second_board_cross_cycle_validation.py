#!/usr/bin/env python3
"""
二板接力跨周期验证 - 聚宽平台执行
严格按照任务要求：2021-2025年度切片分析，验证策略生命周期问题

二板定义：首板次日继续涨停
退出方式：次日最高价卖出 / 次日收盘价卖出
市值过滤：<30亿流通市值

关键问题：
1. 是否存在某一年显著失效？
2. 收益是否逐年下降（衰减趋势）？
3. 信号数量是否逐年减少（拥挤信号）？
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("二板接力跨周期验证 - 2021-2025年度切片分析")
print("=" * 80)

START_DATE = "2021-01-01"
END_DATE = "2025-03-30"
YEARS = ["2021", "2022", "2023", "2024", "2025"]
CAP_FILTER = 30  # 流通市值上限（亿元）


def get_zt_stocks(date):
    """获取当日涨停股票"""
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
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df = df.dropna()
    zt_df = df[df["close"] == df["high_limit"]]
    return list(zt_df["code"])


def get_first_board_stocks(date):
    """获取首板股票（当日涨停，前一日未涨停）"""
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df_today = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df_today = df_today.dropna()
    zt_today = df_today[df_today["close"] == df_today["high_limit"]]

    prev_date = get_shifted_date(date, -1)
    df_prev = get_price(
        all_stocks,
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
        skip_paused=False,
    )
    df_prev = df_prev.dropna()
    zt_prev = df_prev[df_prev["close"] == df_prev["high_limit"]]

    first_board = [
        s for s in zt_today["code"].tolist() if s not in zt_prev["code"].tolist()
    ]
    return first_board


def get_second_board_candidates(date, prev_date):
    """获取二板候选股票（前一日首板，当日有继续涨停可能）"""
    first_board = get_first_board_stocks(prev_date)
    return first_board


def get_shifted_date(date, days):
    """获取偏移日期（交易日）"""
    all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
    if date not in all_days:
        return date
    idx = all_days.index(date)
    new_idx = idx + days
    if new_idx < 0 or new_idx >= len(all_days):
        return date
    return all_days[new_idx]


def filter_by_cap(stock_list, date, max_cap):
    """按流通市值过滤"""
    if not stock_list:
        return []

    q = query(valuation.code, valuation.circulating_market_cap).filter(
        valuation.code.in_(stock_list)
    )
    df = get_fundamentals(q, date=date)
    if df.empty:
        return []

    filtered = df[df["circulating_market_cap"] < max_cap]
    return list(filtered["code"])


def filter_st_stocks(stock_list, date):
    """过滤ST股票"""
    if not stock_list:
        return []

    st_stocks = get_all_securities(["st"], date).index.tolist()
    return [s for s in stock_list if s not in st_stocks]


def filter_yzb(stock_list, date):
    """过滤一字板"""
    result = []
    for stock in stock_list:
        try:
            df = get_price(
                stock, end_date=date, frequency="daily", fields=["low", "high"], count=1
            )
            if df["low"].iloc[0] != df["high"].iloc[0]:
                result.append(stock)
        except:
            continue
    return result


def check_second_board(stock, date):
    """检查是否成功二板（当日涨停）"""
    try:
        df = get_price(
            stock,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        if df.empty:
            return False
        return df.iloc[0]["close"] == df.iloc[0]["high_limit"]
    except:
        return False


def get_next_day_prices(stock, entry_date):
    """获取次日价格数据"""
    next_date = get_shifted_date(entry_date, 1)
    try:
        df = get_price(
            stock,
            end_date=next_date,
            count=1,
            fields=["open", "high", "close", "low"],
            panel=False,
        )
        if df.empty:
            return None
        return {
            "open": df.iloc[0]["open"],
            "high": df.iloc[0]["high"],
            "close": df.iloc[0]["close"],
            "low": df.iloc[0]["low"],
        }
    except:
        return None


def get_entry_price(stock, date):
    """获取买入价格（涨停价）"""
    try:
        df = get_price(
            stock,
            end_date=date,
            count=1,
            fields=["high_limit"],
            panel=False,
        )
        if df.empty:
            return None
        return df.iloc[0]["high_limit"]
    except:
        return None


def simulate_trade(stock, entry_date, exit_type="close"):
    """
    模拟交易
    entry_date: 买入日期（二板当日）
    exit_type: "high" - 次日最高价卖出, "close" - 次日收盘价卖出
    返回：(收益率, 买入价, 卖出价)
    """
    entry_price = get_entry_price(stock, entry_date)
    if entry_price is None:
        return None, None, None

    next_prices = get_next_day_prices(stock, entry_date)
    if next_prices is None:
        return None, None, None

    if exit_type == "high":
        exit_price = next_prices["high"]
    else:
        exit_price = next_prices["close"]

    if entry_price <= 0 or exit_price <= 0:
        return None, None, None

    ret = (exit_price - entry_price) / entry_price
    return ret, entry_price, exit_price


def run_yearly_backtest(year, exit_type="close"):
    """
    单年度回测
    返回：{
        "year": 年份,
        "signal_count": 信号数量,
        "trades": 交易列表,
        "avg_return": 平均收益,
        "win_rate": 胜率,
        "max_loss": 最大亏损,
        "max_win": 最大盈利,
        "total_return": 总收益,
        "returns": 收益列表
    }
    """
    year_start = f"{year}-01-01"
    year_end = f"{year}-12-31"
    if year == "2025":
        year_end = "2025-03-30"

    trade_days = get_trade_days(start_date=year_start, end_date=year_end)
    if len(trade_days) == 0:
        return None

    trades = []

    for i, date in enumerate(trade_days[:-1]):
        date_str = date.strftime("%Y-%m-%d")
        next_date = trade_days[i + 1].strftime("%Y-%m-%d")

        candidates = get_second_board_candidates(
            date_str, get_shifted_date(date_str, -1)
        )
        candidates = filter_by_cap(
            candidates, get_shifted_date(date_str, -1), CAP_FILTER
        )
        candidates = filter_st_stocks(candidates, get_shifted_date(date_str, -1))

        for stock in candidates:
            if check_second_board(stock, date_str):
                ret, entry_price, exit_price = simulate_trade(
                    stock, date_str, exit_type
                )
                if ret is not None:
                    trades.append(
                        {
                            "stock": stock,
                            "entry_date": date_str,
                            "exit_date": next_date,
                            "entry_price": entry_price,
                            "exit_price": exit_price,
                            "return": ret,
                        }
                    )

    if len(trades) == 0:
        return {
            "year": year,
            "signal_count": 0,
            "trades": [],
            "avg_return": 0,
            "win_rate": 0,
            "max_loss": 0,
            "max_win": 0,
            "total_return": 0,
            "returns": [],
        }

    returns = [t["return"] for t in trades]
    wins = [r for r in returns if r > 0]

    result = {
        "year": year,
        "signal_count": len(trades),
        "trades": trades,
        "avg_return": np.mean(returns),
        "win_rate": len(wins) / len(returns) if len(returns) > 0 else 0,
        "max_loss": min(returns),
        "max_win": max(returns),
        "total_return": sum(returns),
        "returns": returns,
    }

    return result


def calc_sharpe(returns_list):
    """计算夏普比率（简化版，假设无风险利率为0）"""
    if len(returns_list) == 0:
        return 0

    returns = np.array(returns_list)
    if np.std(returns) == 0:
        return 0

    return np.mean(returns) / np.std(returns)


def calc_max_drawdown(returns_list):
    """计算最大回撤"""
    if len(returns_list) == 0:
        return 0

    cumulative = np.cumsum(returns_list)
    peak = np.maximum.accumulate(cumulative)
    drawdown = peak - cumulative
    return np.max(drawdown)


def run_full_validation():
    """运行完整验证"""
    print("\n开始年度切片验证...")
    print(f"时间范围: {START_DATE} - {END_DATE}")
    print(f"市值过滤: <{CAP_FILTER}亿流通市值")
    print(f"退出方式: 次日最高价 / 次日收盘价")
    print("=" * 80)

    results_high = {}
    results_close = {}

    for year in YEARS:
        print(f"\n正在验证 {year} 年...")

        print(f"  - 次日收盘价卖出...")
        result_close = run_yearly_backtest(year, exit_type="close")
        if result_close:
            results_close[year] = result_close
            print(f"    信号数: {result_close['signal_count']}")
            print(f"    平均收益: {result_close['avg_return'] * 100:.2f}%")
            print(f"    胜率: {result_close['win_rate'] * 100:.2f}%")

        print(f"  - 次日最高价卖出...")
        result_high = run_yearly_backtest(year, exit_type="high")
        if result_high:
            results_high[year] = result_high
            print(f"    信号数: {result_high['signal_count']}")
            print(f"    平均收益: {result_high['avg_return'] * 100:.2f}%")
            print(f"    胜率: {result_high['win_rate'] * 100:.2f}%")

    return results_close, results_high


def generate_summary_table(results):
    """生成年度对比表"""
    print("\n" + "=" * 80)
    print("年度对比表")
    print("=" * 80)

    print(
        "\n年份 | 信号数 | 平均收益 | 胜率 | 最大盈利 | 最大亏损 | 夏普比率 | 最大回撤"
    )
    print("-" * 80)

    for year in YEARS:
        if year in results and results[year]:
            r = results[year]
            sharpe = calc_sharpe(r["returns"])
            max_dd = calc_max_drawdown(r["returns"])
            print(
                f"{year} | {r['signal_count']} | "
                f"{r['avg_return'] * 100:.2f}% | "
                f"{r['win_rate'] * 100:.2f}% | "
                f"{r['max_win'] * 100:.2f}% | "
                f"{r['max_loss'] * 100:.2f}% | "
                f"{sharpe:.2f} | "
                f"{max_dd * 100:.2f}%"
            )
        else:
            print(f"{year} | 无数据")


def analyze_stability(results):
    """分析策略稳定性"""
    print("\n" + "=" * 80)
    print("策略稳定性判定")
    print("=" * 80)

    years_with_data = [
        y for y in YEARS if y in results and results[y]["signal_count"] > 0
    ]

    if len(years_with_data) == 0:
        print("❌ 已失效：无有效数据")
        return "failed"

    positive_years = [y for y in years_with_data if results[y]["avg_return"] > 0]

    negative_years = [y for y in years_with_data if results[y]["avg_return"] <= 0]

    avg_returns = [results[y]["avg_return"] for y in years_with_data]
    overall_avg = np.mean(avg_returns)

    print(f"\n有效年度数: {len(years_with_data)}")
    print(f"正收益年度: {len(positive_years)} ({positive_years})")
    print(f"负收益年度: {len(negative_years)} ({negative_years})")
    print(f"整体平均收益: {overall_avg * 100:.2f}%")

    signal_counts = [results[y]["signal_count"] for y in years_with_data]
    print(f"\n信号数量趋势:")
    for y in years_with_data:
        print(f"  {y}: {results[y]['signal_count']} 个信号")

    if len(signal_counts) >= 3:
        if signal_counts[-1] < signal_counts[0] * 0.5:
            print("  ⚠️ 信号数量显著衰减")
        elif np.mean(signal_counts[-2:]) < np.mean(signal_counts[:2]):
            print("  ⚠️ 信号数量呈下降趋势")
        else:
            print("  ✓ 信号数量相对稳定")

    if len(negative_years) == 0 and overall_avg > 0.02:
        print("\n✅ 跨周期稳定：所有年度均为正收益")
        return "stable"
    elif len(negative_years) <= 2 and overall_avg > 0:
        print("\n⚠️ 部分失效：1-2个年度为负，但整体仍为正")
        return "partial"
    else:
        print("\n❌ 已失效：多个年度为负，或整体已负")
        return "failed"


def provide_recommendation(stability, results):
    """提供是否纳入进攻线的建议"""
    print("\n" + "=" * 80)
    print("是否纳入进攻线的建议")
    print("=" * 80)

    if stability == "stable":
        print("\n✅ 建议：纳入进攻线")
        print("理由：")
        print("  - 所有年度均为正收益，跨周期稳定")
        print("  - 策略生命周期无明显衰减迹象")
        print("  - 可作为小市值进攻线的核心策略之一")
        print("\n实施建议：")
        print("  - 仓位配置：建议占进攻线仓位20-30%")
        print("  - 风控措施：设置止损线，单笔亏损超10%止损")
        print("  - 监控指标：每月跟踪信号数量和胜率，如胜率低于40%暂停")
    elif stability == "partial":
        print("\n⚠️ 建议：谨慎纳入，需加强监控")
        print("理由：")
        print("  - 策略部分年度失效，存在生命周期风险")
        print("  - 但整体收益仍为正，有一定价值")
        print("\n实施建议：")
        print("  - 仓位配置：建议占进攻线仓位10-15%")
        print("  - 风控措施：严格止损，胜率监控")
        print("  - 退出机制：连续3个月负收益暂停策略")
        print("  - 季度复盘：每季度重新评估是否继续使用")
    else:
        print("\n❌ 建议：不纳入进攻线")
        print("理由：")
        print("  - 策略已失效或数据不足")
        print("  - 存在严重生命周期问题")
        print("  - 不适合作为正式策略")
        print("\n后续建议：")
        print("  - 继续观察，等待新的验证周期")
        print("  - 或寻找替代策略")


if __name__ == "__main__":
    results_close, results_high = run_full_validation()

    print("\n\n" + "=" * 80)
    print("方案一：次日收盘价卖出")
    print("=" * 80)
    generate_summary_table(results_close)
    stability_close = analyze_stability(results_close)
    provide_recommendation(stability_close, results_close)

    print("\n\n" + "=" * 80)
    print("方案二：次日最高价卖出")
    print("=" * 80)
    generate_summary_table(results_high)
    stability_high = analyze_stability(results_high)
    provide_recommendation(stability_high, results_high)

    print("\n\n" + "=" * 80)
    print("综合建议")
    print("=" * 80)

    if stability_close == "stable" or stability_high == "stable":
        print("✅ 二板接力策略跨周期验证通过")
        if stability_high == "stable":
            print("   推荐使用次日最高价卖出方案（收益更高）")
        else:
            print("   推荐使用次日收盘价卖出方案（更稳健）")
    elif stability_close == "partial" or stability_high == "partial":
        print("⚠️ 二板接力策略存在部分失效风险，需加强监控")
    else:
        print("❌ 二板接力策略已失效，不建议纳入进攻线")

    print("\n验证完成！")
