#!/usr/bin/env python3
"""
二板接力跨周期验证 - 轻量版
优化：批量查询、减少API调用、快速验证核心逻辑

验证范围：2021-2025年度切片
关键问题：是否存在生命周期问题
"""

from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("二板接力跨周期验证（轻量版）")
print("=" * 80)

YEARS = ["2021", "2022", "2023", "2024", "2025"]
CAP_FILTER = 30  # 流通市值上限（亿元）


def run_year_backtest_lite(year):
    """
    轻量版年度回测
    优化策略：
    1. 每月只采样月初、月中、月末3个交易日
    2. 批量获取所有股票的涨停数据
    3. 批量获取市值数据
    """
    year_start = f"{year}-01-01"
    year_end = f"{year}-12-31" if year != "2025" else "2025-03-30"

    all_days = get_trade_days(start_date=year_start, end_date=year_end)
    if len(all_days) == 0:
        return None

    # 采样策略：每月采样3个交易日（月初、月中、月末）
    sampled_days = []
    month_dict = {}
    for day in all_days:
        month_key = day.strftime("%Y-%m")
        if month_key not in month_dict:
            month_dict[month_key] = []
        month_dict[month_key].append(day)

    for month, days in month_dict.items():
        if len(days) >= 3:
            sampled_days.extend([days[0], days[len(days) // 2], days[-1]])
        else:
            sampled_days.extend(days)

    sampled_days = sorted(set(sampled_days))

    trades = []

    for i in range(len(sampled_days) - 1):
        date = sampled_days[i]
        date_str = date.strftime("%Y-%m-%d")
        next_date = sampled_days[i + 1].strftime("%Y-%m-%d")

        # 批量获取当日涨停股票
        all_stocks = get_all_securities("stock", date_str).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        if len(all_stocks) > 500:
            all_stocks = all_stocks[:500]

        try:
            # 批量获取涨停数据
            df_today = get_price(
                all_stocks,
                end_date=date_str,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
                fill_paused=True,
            )
            df_today = df_today.dropna()
            zt_today = df_today[df_today["close"] == df_today["high_limit"]]
            zt_list = list(zt_today["code"])

            if len(zt_list) == 0:
                continue

            # 批量获取市值
            q = query(valuation.code, valuation.circulating_market_cap).filter(
                valuation.code.in_(zt_list),
                valuation.circulating_market_cap < CAP_FILTER,
            )
            cap_df = get_fundamentals(q, date=date_str)

            if cap_df.empty:
                continue

            filtered_stocks = list(cap_df["code"])

            if len(filtered_stocks) == 0:
                continue

            # 批量获取次日数据
            df_next = get_price(
                filtered_stocks,
                end_date=next_date,
                count=1,
                fields=["open", "high", "close"],
                panel=False,
                fill_paused=True,
            )
            df_next = df_next.dropna()

            # 批量获取前一日涨停价作为买入价
            df_entry = get_price(
                filtered_stocks,
                end_date=date_str,
                count=1,
                fields=["high_limit"],
                panel=False,
                fill_paused=True,
            )

            for stock in filtered_stocks:
                if stock not in df_next.index or stock not in df_entry.index:
                    continue

                entry_price = df_entry.loc[stock, "high_limit"]
                high_next = df_next.loc[stock, "high"]
                close_next = df_next.loc[stock, "close"]

                if entry_price <= 0 or high_next <= 0:
                    continue

                # 模拟两种退出方式
                ret_high = (high_next - entry_price) / entry_price
                ret_close = (close_next - entry_price) / entry_price

                trades.append(
                    {
                        "stock": stock,
                        "date": date_str,
                        "entry_price": entry_price,
                        "high_next": high_next,
                        "close_next": close_next,
                        "ret_high": ret_high,
                        "ret_close": ret_close,
                    }
                )
        except Exception as e:
            print(f"Error on {date_str}: {e}")
            continue

    if len(trades) == 0:
        return None

    returns_high = [t["ret_high"] for t in trades]
    returns_close = [t["ret_close"] for t in trades]

    result = {
        "year": year,
        "signal_count": len(trades),
        "avg_return_high": np.mean(returns_high),
        "avg_return_close": np.mean(returns_close),
        "win_rate_high": len([r for r in returns_high if r > 0]) / len(returns_high),
        "win_rate_close": len([r for r in returns_close if r > 0]) / len(returns_close),
        "max_win_high": max(returns_high),
        "max_win_close": max(returns_close),
        "max_loss_high": min(returns_high),
        "max_loss_close": min(returns_close),
        "returns_high": returns_high,
        "returns_close": returns_close,
    }

    return result


def calc_sharpe(returns):
    """计算夏普比率"""
    if len(returns) == 0 or np.std(returns) == 0:
        return 0
    return np.mean(returns) / np.std(returns)


def run_all_years():
    """运行所有年度"""
    results = {}

    for year in YEARS:
        print(f"\n验证 {year} 年...")
        result = run_year_backtest_lite(year)
        if result:
            results[year] = result
            print(f"  信号数: {result['signal_count']}")
            print(f"  次日最高价收益: {result['avg_return_high'] * 100:.2f}%")
            print(f"  次日收盘价收益: {result['avg_return_close'] * 100:.2f}%")
            print(f"  胜率(最高): {result['win_rate_high'] * 100:.2f}%")
            print(f"  胜率(收盘): {result['win_rate_close'] * 100:.2f}%")
        else:
            print(f"  无数据")

    return results


def generate_report(results):
    """生成完整报告"""
    print("\n" + "=" * 80)
    print("年度对比表（次日最高价卖出）")
    print("=" * 80)
    print("年份 | 信号数 | 平均收益 | 胜率 | 最大盈利 | 最大亏损 | 夏普")
    print("-" * 80)

    for year in YEARS:
        if year in results:
            r = results[year]
            sharpe = calc_sharpe(r["returns_high"])
            print(
                f"{year} | {r['signal_count']} | "
                f"{r['avg_return_high'] * 100:.2f}% | "
                f"{r['win_rate_high'] * 100:.2f}% | "
                f"{r['max_win_high'] * 100:.2f}% | "
                f"{r['max_loss_high'] * 100:.2f}% | "
                f"{sharpe:.2f}"
            )
        else:
            print(f"{year} | 无数据")

    print("\n" + "=" * 80)
    print("年度对比表（次日收盘价卖出）")
    print("=" * 80)
    print("年份 | 信号数 | 平均收益 | 胜率 | 最大盈利 | 最大亏损 | 夏普")
    print("-" * 80)

    for year in YEARS:
        if year in results:
            r = results[year]
            sharpe = calc_sharpe(r["returns_close"])
            print(
                f"{year} | {r['signal_count']} | "
                f"{r['avg_return_close'] * 100:.2f}% | "
                f"{r['win_rate_close'] * 100:.2f}% | "
                f"{r['max_win_close'] * 100:.2f}% | "
                f"{r['max_loss_close'] * 100:.2f}% | "
                f"{sharpe:.2f}"
            )
        else:
            print(f"{year} | 无数据")

    print("\n" + "=" * 80)
    print("策略稳定性判定")
    print("=" * 80)

    years_with_data = [y for y in YEARS if y in results]

    if len(years_with_data) == 0:
        print("❌ 已失效：无有效数据")
        return "failed", "failed"

    positive_high = [y for y in years_with_data if results[y]["avg_return_high"] > 0]
    positive_close = [y for y in years_with_data if results[y]["avg_return_close"] > 0]

    avg_high = np.mean([results[y]["avg_return_high"] for y in years_with_data])
    avg_close = np.mean([results[y]["avg_return_close"] for y in years_with_data])

    print(f"\n有效年度: {len(years_with_data)}")
    print(f"正收益年度(最高价): {len(positive_high)} {positive_high}")
    print(f"正收益年度(收盘价): {len(positive_close)} {positive_close}")
    print(f"整体平均(最高价): {avg_high * 100:.2f}%")
    print(f"整体平均(收盘价): {avg_close * 100:.2f}%")

    print(f"\n信号数量趋势:")
    counts = [results[y]["signal_count"] for y in years_with_data]
    for y in years_with_data:
        print(f"  {y}: {results[y]['signal_count']}")

    if len(counts) >= 3:
        trend = counts[-1] - counts[0]
        if trend < -counts[0] * 0.3:
            print("  ⚠️ 信号数量显著衰减")
        elif trend < 0:
            print("  ⚠️ 信号数量呈下降趋势")
        else:
            print("  ✓ 信号数量相对稳定")

    # 判定稳定性
    stability_high = "failed"
    stability_close = "failed"

    if len(positive_high) == len(years_with_data) and avg_high > 0.02:
        print("\n✅ 次日最高价方案：跨周期稳定")
        stability_high = "stable"
    elif len(years_with_data) - len(positive_high) <= 2 and avg_high > 0:
        print("\n⚠️ 次日最高价方案：部分失效")
        stability_high = "partial"
    else:
        print("\n❌ 次日最高价方案：已失效")

    if len(positive_close) == len(years_with_data) and avg_close > 0.02:
        print("✅ 次日收盘价方案：跨周期稳定")
        stability_close = "stable"
    elif len(years_with_data) - len(positive_close) <= 2 and avg_close > 0:
        print("⚠️ 次日收盘价方案：部分失效")
        stability_close = "partial"
    else:
        print("❌ 次日收盘价方案：已失效")

    return stability_high, stability_close


def provide_recommendation(stability_high, stability_close, results):
    """提供建议"""
    print("\n" + "=" * 80)
    print("是否纳入进攻线的建议")
    print("=" * 80)

    if stability_high == "stable":
        print("\n✅ 建议：纳入进攻线")
        print("推荐方案：次日最高价卖出")
        print("理由：所有年度正收益，跨周期稳定")
        print("仓位建议：占进攻线20-30%")
        print("监控指标：月度胜率>40%，否则暂停")
    elif stability_close == "stable":
        print("\n✅ 建议：纳入进攻线")
        print("推荐方案：次日收盘价卖出")
        print("理由：所有年度正收益，跨周期稳定")
        print("仓位建议：占进攻线20-30%")
        print("监控指标：月度胜率>40%，否则暂停")
    elif stability_high == "partial" or stability_close == "partial":
        print("\n⚠️ 建议：谨慎纳入")
        print("理由：部分年度失效，需加强监控")
        print("仓位建议：占进攻线10-15%")
        print("退出机制：连续3月负收益暂停")
    else:
        print("\n❌ 建议：不纳入进攻线")
        print("理由：策略已失效或数据不足")


if __name__ == "__main__":
    results = run_all_years()
    stability_high, stability_close = generate_report(results)
    provide_recommendation(stability_high, stability_close, results)
    print("\n验证完成！")
