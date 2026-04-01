"""
情绪冰点捕捉测试
研究假设：冰点次日可能反弹，冰点次日开仓收益可能更高
对比：A组（原始情绪开关）vs B组（冰点次日开仓）
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 80)
print("情绪冰点捕捉测试")
print("=" * 80)

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

print(f"\n研究范围: {START_DATE} 至 {END_DATE}")


def get_limit_up_stats(date):
    """获取涨停统计：涨停家数、最高连板数、炸板率"""
    try:
        all_stocks = get_all_securities(types=["stock"], date=date)
        all_stocks = [
            s
            for s in all_stocks.index.tolist()
            if not (
                s.startswith("688")
                or s.startswith("300")
                or s.startswith("4")
                or s.startswith("8")
            )
        ]

        if not all_stocks:
            return None

        df = get_price(
            all_stocks,
            end_date=date,
            frequency="daily",
            fields=["close", "high_limit", "low_limit"],
            count=1,
            panel=False,
        )
        df = df.dropna()

        limit_up_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()
        limit_down_stocks = df[df["close"] == df["low_limit"]]["code"].tolist()

        zt_count = len(limit_up_stocks)

        prev_dates = get_trade_days(end_date=date, count=2)
        if len(prev_dates) >= 2:
            prev_date = prev_dates[0]
            df_prev = get_price(
                all_stocks,
                end_date=prev_date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
            )
            df_prev = df_prev.dropna()
            prev_zt = df_prev[df_prev["close"] == df_prev["high_limit"]][
                "code"
            ].tolist()

            consecutive_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

            for stock in limit_up_stocks:
                if stock in prev_zt:
                    lianban = 2
                    for lookback in range(2, 6):
                        prev_dates_n = get_trade_days(
                            end_date=prev_date, count=lookback + 1
                        )
                        if len(prev_dates_n) < lookback + 1:
                            break
                        check_date = prev_dates_n[0]
                        df_check = get_price(
                            stock,
                            end_date=check_date,
                            frequency="daily",
                            fields=["close", "high_limit"],
                            count=1,
                            panel=False,
                        )
                        if (
                            len(df_check) > 0
                            and df_check["close"].iloc[0]
                            == df_check["high_limit"].iloc[0]
                        ):
                            lianban = lookback + 1
                        else:
                            break

                    consecutive_counts[min(lianban, 5)] = (
                        consecutive_counts.get(min(lianban, 5), 0) + 1
                    )
                else:
                    consecutive_counts[1] = consecutive_counts.get(1, 0) + 1

            max_lianban = (
                max([k for k, v in consecutive_counts.items() if v > 0])
                if any(consecutive_counts.values())
                else 0
            )
        else:
            max_lianban = 1
            consecutive_counts = {1: zt_count}

        df_high = get_price(
            all_stocks,
            end_date=date,
            frequency="daily",
            fields=["high", "close", "high_limit"],
            count=1,
            panel=False,
        )
        df_high = df_high.dropna()

        touched_limit = df_high[df_high["high"] == df_high["high_limit"]][
            "code"
        ].tolist()
        sealed_limit = df_high[df_high["close"] == df_high["high_limit"]][
            "code"
        ].tolist()

        broken_rate = (
            (len(touched_limit) - len(sealed_limit)) / len(touched_limit) * 100
            if len(touched_limit) > 0
            else 0
        )

        return {
            "zt_count": zt_count,
            "max_lianban": max_lianban,
            "broken_rate": broken_rate,
            "limit_down_count": len(limit_down_stocks),
        }
    except Exception as e:
        print(f"获取涨停统计出错 {date}: {e}")
        return None


def is_ice_point(stats):
    """判断是否为情绪冰点"""
    if stats is None:
        return False

    zt_count = stats["zt_count"]
    max_lianban = stats["max_lianban"]
    broken_rate = stats["broken_rate"]

    if zt_count < 10:
        return True
    if max_lianban == 1:
        return True
    if broken_rate > 50:
        return True

    return False


def is_sentiment_ok(stats, threshold=30):
    """原始情绪开关：涨停>=threshold"""
    if stats is None:
        return False
    return stats["zt_count"] >= threshold


def get_first_board_low_open_stocks(date):
    """获取首板低开股票"""
    try:
        prev_dates = get_trade_days(end_date=date, count=2)
        if len(prev_dates) < 2:
            return []

        prev_date = prev_dates[0]

        all_stocks = get_all_securities(types=["stock"], date=date)
        all_stocks = [
            s
            for s in all_stocks.index.tolist()
            if not (
                s.startswith("688")
                or s.startswith("300")
                or s.startswith("4")
                or s.startswith("8")
            )
        ]

        df_prev = get_price(
            all_stocks,
            end_date=prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        df_prev = df_prev.dropna()
        zt_stocks = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()

        if not zt_stocks:
            return []

        prev_prev_dates = get_trade_days(end_date=prev_date, count=2)
        if len(prev_prev_dates) >= 2:
            prev_prev_date = prev_prev_dates[0]
            df_prev_prev = get_price(
                zt_stocks,
                end_date=prev_prev_date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
            )
            df_prev_prev = df_prev_prev.dropna()
            prev_zt = df_prev_prev[df_prev_prev["close"] == df_prev_prev["high_limit"]][
                "code"
            ].tolist()
            first_board = [s for s in zt_stocks if s not in prev_zt]
        else:
            first_board = zt_stocks

        if not first_board:
            return []

        df_today = get_price(
            first_board,
            end_date=date,
            frequency="daily",
            fields=["open", "close", "pre_close"],
            count=1,
            panel=False,
        )
        df_today = df_today.dropna()

        low_open_stocks = []
        for stock in df_today["code"].unique():
            stock_df = df_today[df_today["code"] == stock]
            open_price = stock_df["open"].iloc[0]
            pre_close = stock_df["pre_close"].iloc[0]

            if pre_close > 0:
                open_change = (open_price - pre_close) / pre_close * 100
                if -5 < open_change < 1:
                    low_open_stocks.append(
                        {
                            "stock": stock,
                            "open_change": open_change,
                            "close_price": stock_df["close"].iloc[0],
                        }
                    )

        return low_open_stocks
    except Exception as e:
        print(f"获取首板低开股票出错 {date}: {e}")
        return []


def calculate_intraday_return(stock, date):
    """计算日内收益"""
    try:
        df = get_price(
            stock,
            end_date=date,
            frequency="daily",
            fields=["open", "close"],
            count=1,
            panel=False,
        )
        if len(df) == 0:
            return None
        return (df["close"].iloc[0] - df["open"].iloc[0]) / df["open"].iloc[0] * 100
    except:
        return None


print("\n【步骤1】收集交易日和市场情绪数据")
print("-" * 60)

trade_days = get_trade_days(START_DATE, END_DATE)
print(f"交易日总数: {len(trade_days)}")

ice_points = []
sentiment_data = []

for i, date in enumerate(trade_days):
    if i % 50 == 0:
        print(f"处理进度: {i}/{len(trade_days)} ({date})")

    stats = get_limit_up_stats(date)
    if stats:
        sentiment_data.append(
            {
                "date": date,
                "zt_count": stats["zt_count"],
                "max_lianban": stats["max_lianban"],
                "broken_rate": stats["broken_rate"],
            }
        )

        if is_ice_point(stats):
            ice_points.append(date)

print(f"\n情绪冰点识别完成:")
print(f"  总交易日: {len(trade_days)}")
print(f"  冰点日数量: {len(ice_points)}")
print(f"  冰点日占比: {len(ice_points) / len(trade_days) * 100:.1f}%")

print("\n【步骤2】识别冰点次日")
print("-" * 60)

ice_point_next_days = []
for i, date in enumerate(trade_days[:-1]):
    if date in ice_points:
        next_idx = i + 1
        if next_idx < len(trade_days):
            ice_point_next_days.append(trade_days[next_idx])

print(f"冰点次日数量: {len(ice_point_next_days)}")

print("\n【步骤3】A组回测：原始情绪开关（涨停>=30）")
print("-" * 60)

group_a_trades = []
group_a_dates = []

for i, date in enumerate(trade_days):
    if i >= len(sentiment_data):
        break

    stats = sentiment_data[i]

    if is_sentiment_ok(stats, threshold=30):
        low_open_stocks = get_first_board_low_open_stocks(date)

        if low_open_stocks:
            group_a_dates.append(date)
            for stock_info in low_open_stocks[:3]:
                ret = calculate_intraday_return(stock_info["stock"], date)
                if ret is not None:
                    group_a_trades.append(
                        {
                            "date": date,
                            "stock": stock_info["stock"],
                            "open_change": stock_info["open_change"],
                            "return": ret,
                        }
                    )

print(f"A组交易天数: {len(group_a_dates)}")
print(f"A组交易次数: {len(group_a_trades)}")

if group_a_trades:
    df_a = pd.DataFrame(group_a_trades)
    print(f"A组平均收益: {df_a['return'].mean():.2f}%")
    print(f"A组胜率: {(df_a['return'] > 0).mean() * 100:.1f}%")
    print(f"A组最大收益: {df_a['return'].max():.2f}%")
    print(f"A组最大亏损: {df_a['return'].min():.2f}%")

print("\n【步骤4】B组回测：冰点次日开仓")
print("-" * 60)

group_b_trades = []
group_b_dates = []

for date in ice_point_next_days:
    low_open_stocks = get_first_board_low_open_stocks(date)

    if low_open_stocks:
        group_b_dates.append(date)
        for stock_info in low_open_stocks[:3]:
            ret = calculate_intraday_return(stock_info["stock"], date)
            if ret is not None:
                group_b_trades.append(
                    {
                        "date": date,
                        "stock": stock_info["stock"],
                        "open_change": stock_info["open_change"],
                        "return": ret,
                    }
                )

print(f"B组交易天数: {len(group_b_dates)}")
print(f"B组交易次数: {len(group_b_trades)}")

if group_b_trades:
    df_b = pd.DataFrame(group_b_trades)
    print(f"B组平均收益: {df_b['return'].mean():.2f}%")
    print(f"B组胜率: {(df_b['return'] > 0).mean() * 100:.1f}%")
    print(f"B组最大收益: {df_b['return'].max():.2f}%")
    print(f"B组最大亏损: {df_b['return'].min():.2f}%")

print("\n【步骤5】冰点次日反弹成功率统计")
print("-" * 60)

success_count = 0
total_count = 0
next_day_stats = []

for i, date in enumerate(trade_days[:-1]):
    if date in ice_points:
        next_idx = i + 1
        if next_idx < len(trade_days):
            next_date = trade_days[next_idx]
            next_stats = (
                sentiment_data[next_idx] if next_idx < len(sentiment_data) else None
            )

            if next_stats:
                total_count += 1
                if next_stats["zt_count"] > sentiment_data[i]["zt_count"]:
                    success_count += 1
                    next_day_stats.append(
                        {
                            "date": next_date,
                            "prev_zt": sentiment_data[i]["zt_count"],
                            "next_zt": next_stats["zt_count"],
                            "rebound": "Success",
                        }
                    )
                else:
                    next_day_stats.append(
                        {
                            "date": next_date,
                            "prev_zt": sentiment_data[i]["zt_count"],
                            "next_zt": next_stats["zt_count"],
                            "rebound": "Fail",
                        }
                    )

if total_count > 0:
    success_rate = success_count / total_count * 100
    print(f"冰点次日反弹成功率: {success_rate:.1f}%")
    print(f"成功次数: {success_count}/{total_count}")

    df_next = pd.DataFrame(next_day_stats)
    print(f"\n冰点次日涨停家数变化:")
    print(f"  平均前日涨停: {df_next['prev_zt'].mean():.1f}")
    print(f"  平均次日涨停: {df_next['next_zt'].mean():.1f}")

print("\n【步骤6】详细对比分析")
print("-" * 60)

if group_a_trades and group_b_trades:
    df_a = pd.DataFrame(group_a_trades)
    df_b = pd.DataFrame(group_b_trades)

    print("\n=== 年化收益对比 ===")
    trading_days_per_year = 244

    a_annual_return = (
        df_a["return"].mean()
        * len(group_a_dates)
        / (len(trade_days) / trading_days_per_year)
    )
    b_annual_return = (
        df_b["return"].mean()
        * len(group_b_dates)
        / (len(trade_days) / trading_days_per_year)
    )

    print(f"A组（原始情绪开关）:")
    print(f"  交易天数: {len(group_a_dates)}")
    print(f"  平均单次收益: {df_a['return'].mean():.2f}%")
    print(f"  胜率: {(df_a['return'] > 0).mean() * 100:.1f}%")
    print(f"  估算年化收益: {a_annual_return:.2f}%")

    print(f"\nB组（冰点次日开仓）:")
    print(f"  交易天数: {len(group_b_dates)}")
    print(f"  平均单次收益: {df_b['return'].mean():.2f}%")
    print(f"  胜率: {(df_b['return'] > 0).mean() * 100:.1f}%")
    print(f"  估算年化收益: {b_annual_return:.2f}%")

    print("\n=== 冰点类型分析 ===")

    ice_type_stats = {"zt_lt_10": 0, "lianban_eq_1": 0, "broken_gt_50": 0}
    for i, date in enumerate(trade_days):
        if date in ice_points and i < len(sentiment_data):
            stats = sentiment_data[i]
            if stats["zt_count"] < 10:
                ice_type_stats["zt_lt_10"] += 1
            elif stats["max_lianban"] == 1:
                ice_type_stats["lianban_eq_1"] += 1
            elif stats["broken_rate"] > 50:
                ice_type_stats["broken_gt_50"] += 1

    print(f"冰点类型分布:")
    print(f"  涨停<10: {ice_type_stats['zt_lt_10']}次")
    print(f"  连板=1: {ice_type_stats['lianban_eq_1']}次")
    print(f"  炸板率>50%: {ice_type_stats['broken_gt_50']}次")

print("\n" + "=" * 80)
print("测试完成!")
print("=" * 80)
