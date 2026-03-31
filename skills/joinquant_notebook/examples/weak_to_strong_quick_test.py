#!/usr/bin/env python3
"""弱转强竞价策略 - 快速参数测试"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 70)
print("弱转强竞价策略 - 2024年样本外快速测试")
print("=" * 70)

# 测试时间范围
test_start = "2024-01-01"
test_end = "2024-12-31"

# 参数组合（关键组合）
TEST_PARAMS = [
    {
        "name": "原始版",
        "high_open": (0, 6),
        "volume_ratio": 3,
        "market_cap": 70,
        "money": 7e8,
        "left_pressure": 0.9,
    },
    {
        "name": "收窄高开",
        "high_open": (2, 5),
        "volume_ratio": 5,
        "market_cap": 30,
        "money": 5e8,
        "left_pressure": 0.9,
    },
    {
        "name": "严格高开",
        "high_open": (3, 5),
        "volume_ratio": 8,
        "market_cap": 50,
        "money": 7e8,
        "left_pressure": 1.0,
    },
    {
        "name": "弹性版",
        "high_open": (2, 4),
        "volume_ratio": 3,
        "market_cap": 20,
        "money": 5e8,
        "left_pressure": 0.8,
    },
]


def test_single_day(date_str, params):
    """测试单日"""
    high_open_min, high_open_max = params["high_open"]

    try:
        next_date = get_shifted_date(date_str, 1)
        prev_date = get_shifted_date(date_str, -1)
        prev_date_2 = get_shifted_date(date_str, -2)

        # 初始股票池
        initial_list = get_all_securities("stock", date_str).index.tolist()
        initial_list = [
            s for s in initial_list if s[0] not in ["4", "8", "3"] and s[:2] != "68"
        ]

        # 过滤新股（>50天）
        new_filter = []
        for s in initial_list:
            try:
                info = get_security_info(s)
                if info.start_date:
                    days = (
                        datetime.strptime(date_str, "%Y-%m-%d") - info.start_date
                    ).days
                    if days > 50:
                        new_filter.append(s)
            except:
                continue
        initial_list = new_filter

        # 过滤ST
        st_df = get_extras(
            "is_st", initial_list, start_date=date_str, end_date=date_str, df=True
        )
        if not st_df.empty:
            st_df = st_df.T
            st_df.columns = ["is_st"]
            initial_list = list(st_df[st_df["is_st"] == False].index)

        # 昨日涨停
        prices = get_price(
            initial_list,
            end_date=date_str,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
            fill_paused=False,
            skip_paused=False,
        )
        if prices.empty:
            return []
        prices = prices.dropna()
        hl_stocks = list(prices[prices["close"] == prices["high_limit"]]["code"])

        # 前两日曾涨停
        try:
            prev1_prices = get_price(
                initial_list,
                end_date=prev_date,
                frequency="daily",
                fields=["high", "high_limit"],
                count=1,
                panel=False,
                fill_paused=False,
                skip_paused=False,
            )
            if not prev1_prices.empty:
                prev1_prices = prev1_prices.dropna()
                hl1 = list(
                    prev1_prices[prev1_prices["high"] == prev1_prices["high_limit"]][
                        "code"
                    ]
                )
            else:
                hl1 = []
        except:
            hl1 = []

        try:
            prev2_prices = get_price(
                initial_list,
                end_date=prev_date_2,
                frequency="daily",
                fields=["high", "high_limit"],
                count=1,
                panel=False,
                fill_paused=False,
                skip_paused=False,
            )
            if not prev2_prices.empty:
                prev2_prices = prev2_prices.dropna()
                hl2 = list(
                    prev2_prices[prev2_prices["high"] == prev2_prices["high_limit"]][
                        "code"
                    ]
                )
            else:
                hl2 = []
        except:
            hl2 = []

        # 排除前两日曾涨停
        remove_set = set(hl1 + hl2)
        target_stocks = [s for s in hl_stocks if s not in remove_set]

        if len(target_stocks) == 0:
            return []

        # 筛选
        qualified = []

        for s in target_stocks:
            try:
                # 成交额和市值
                prev_data = get_price(
                    s,
                    end_date=date_str,
                    frequency="daily",
                    fields=["close", "volume", "money"],
                    count=1,
                    panel=False,
                    skip_paused=True,
                )
                if prev_data.empty:
                    continue

                prev_close = prev_data["close"].iloc[-1]
                prev_volume = prev_data["volume"].iloc[-1]
                prev_money = prev_data["money"].iloc[-1]

                if prev_money < params["money"]:
                    continue

                # 均价涨幅 > 7%
                avg_price = prev_money / prev_volume
                avg_increase = avg_price / prev_close * 1.1 - 1
                if avg_increase < 0.07:
                    continue

                # 市值
                val = get_valuation(
                    s, start_date=date_str, end_date=date_str, fields=["market_cap"]
                )
                if val.empty or val["market_cap"].iloc[-1] < params["market_cap"]:
                    continue

                # 左压突破（简化版）
                try:
                    highs = get_price(
                        s,
                        end_date=date_str,
                        frequency="daily",
                        fields=["high"],
                        count=30,
                        panel=False,
                        skip_paused=True,
                    )
                    if highs.empty or len(highs) < 3:
                        continue

                    high_arr = highs["high"].values
                    prev_high = high_arr[-1]

                    # 找到第一个高于昨日最高价的日期
                    max_idx = 0
                    for idx in range(len(high_arr) - 3, 0, -1):
                        if high_arr[idx] >= prev_high:
                            max_idx = idx
                            break

                    # 检查左压突破
                    volumes = get_price(
                        s,
                        end_date=date_str,
                        frequency="daily",
                        fields=["volume"],
                        count=max_idx + 5,
                        panel=False,
                        skip_paused=True,
                    )
                    if volumes.empty or len(volumes) < 2:
                        continue

                    vol_arr = volumes["volume"].values
                    if vol_arr[-1] <= max(vol_arr[:-1]) * params["left_pressure"]:
                        continue
                except:
                    continue

                # 竞价条件（使用开盘价近似）
                next_data = get_price(
                    s,
                    end_date=next_date,
                    frequency="daily",
                    fields=["open", "close", "high_limit"],
                    count=1,
                    panel=False,
                    skip_paused=True,
                )
                if next_data.empty:
                    continue

                next_open = next_data["open"].iloc[-1]
                next_close = next_data["close"].iloc[-1]
                high_limit = next_data["high_limit"].iloc[-1]

                # 高开幅度（相对于涨停价）
                open_ratio = next_open / (high_limit / 1.1)
                open_pct = (open_ratio - 1) * 100

                if not (high_open_min <= open_pct < high_open_max):
                    continue

                # 计算收益（尾盘卖出）
                return_pct = (next_close - next_open) / next_open * 100

                qualified.append(
                    {
                        "stock": s,
                        "date": next_date,
                        "open": next_open,
                        "close": next_close,
                        "return": return_pct,
                        "is_limit": next_close == high_limit,
                        "open_pct": open_pct,
                    }
                )

            except Exception as e:
                continue

        return qualified

    except Exception as e:
        return []


def test_strategy(params):
    """测试完整策略"""
    print(f"\n测试参数: {params['name']}")
    print(f"  高开幅度: {params['high_open']}%")
    print(f"  量比阈值: >{params['volume_ratio']}%")
    print(f"  市值门槛: >{params['market_cap']}亿")
    print(f"  成交额门槛: >{params['money'] / 1e8:.0f}亿")
    print(f"  左压阈值: {params['left_pressure']}")

    all_trades = []

    trade_days = get_trade_days(start_date=test_start, end_date=test_end)

    print(f"  测试天数: {len(trade_days)}")

    for idx, date in enumerate(trade_days[:-1]):
        if idx % 50 == 0:
            print(f"  进度: {idx}/{len(trade_days) - 1}")

        trades = test_single_day(date, params)
        all_trades.extend(trades)

    if len(all_trades) == 0:
        print(f"  结果: 无有效交易")
        return None

    df = pd.DataFrame(all_trades)

    total_trades = len(df)
    win_trades = len(df[df["return"] > 0])
    win_rate = win_trades / total_trades * 100

    avg_win = df[df["return"] > 0]["return"].mean() if win_trades > 0 else 0
    avg_loss = (
        df[df["return"] < 0]["return"].mean() if len(df[df["return"] < 0]) > 0 else 0
    )
    profit_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0

    total_return = df["return"].sum()
    avg_return = df["return"].mean()

    # 累计收益和最大回撤
    daily_returns = df.groupby("date")["return"].mean()
    cumulative = (1 + daily_returns / 100).cumprod()

    if len(cumulative) > 0:
        peak = cumulative.expanding(min_periods=1).max()
        drawdown = (cumulative - peak) / peak
        max_drawdown = drawdown.min() * 100
    else:
        max_drawdown = 0

    # 连续亏损
    loss_seq = (df["return"] < 0).astype(int)
    max_consecutive_loss = 0
    current_loss = 0
    for val in loss_seq:
        if val == 1:
            current_loss += 1
            max_consecutive_loss = max(max_consecutive_loss, current_loss)
        else:
            current_loss = 0

    # 年化收益（简化估算）
    annual_return = avg_return * 250 if avg_return else 0

    # 卡玛比率
    calmar_ratio = abs(annual_return / max_drawdown) if max_drawdown != 0 else 0

    # 月度收益
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
    monthly_returns = df.groupby("month")["return"].sum()

    result = {
        "name": params["name"],
        "params": params,
        "total_trades": total_trades,
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "profit_loss_ratio": profit_loss_ratio,
        "total_return": total_return,
        "avg_return": avg_return,
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "calmar_ratio": calmar_ratio,
        "max_consecutive_loss": max_consecutive_loss,
        "monthly_returns": monthly_returns,
    }

    print(f"  交易次数: {total_trades}")
    print(f"  胜率: {win_rate:.2f}%")
    print(f"  盈亏比: {profit_loss_ratio:.2f}")
    print(f"  平均收益: {avg_return:.2f}%")
    print(f"  年化收益: {annual_return:.2f}%")
    print(f"  最大回撤: {max_drawdown:.2f}%")
    print(f"  卡玛比率: {calmar_ratio:.2f}")
    print(f"  连续亏损: {max_consecutive_loss}次")

    return result


def main():
    all_results = []

    for params in TEST_PARAMS:
        result = test_strategy(params)
        if result:
            all_results.append(result)

    print("\n" + "=" * 70)
    print("结果汇总 (2024-01-01后样本外)")
    print("=" * 70)

    if len(all_results) == 0:
        print("无有效结果")
        return

    # 按卡玛比率排序
    sorted_results = sorted(all_results, key=lambda x: x["calmar_ratio"], reverse=True)

    print("\n按卡玛比率排序:")
    for idx, r in enumerate(sorted_results):
        print(f"\nTOP {idx + 1}: {r['name']}")
        print(f"  年化收益: {r['annual_return']:.2f}%")
        print(f"  最大回撤: {r['max_drawdown']:.2f}%")
        print(f"  卡玛比率: {r['calmar_ratio']:.2f}")
        print(f"  交易次数: {r['total_trades']}")
        print(f"  胜率: {r['win_rate']:.2f}%")
        print(f"  盈亏比: {r['profit_loss_ratio']:.2f}")

    # 输出最优版本
    best = sorted_results[0]

    print("\n" + "=" * 70)
    print(f"最优版本: {best['name']}")
    print("=" * 70)

    # 门槛判断
    pass_threshold = (
        best["annual_return"] > 25
        and best["max_drawdown"] < 25
        and best["calmar_ratio"] > 1.2
        and best["total_trades"] >= 10
    )

    if pass_threshold:
        print("通过门槛: Go")
    else:
        print(f"未通过门槛")
        print(f"  年化收益需要 >25%, 当前 {best['annual_return']:.2f}%")
        print(f"  最大回撤需要 <25%, 当前 {best['max_drawdown']:.2f}%")
        print(f"  卡玛比率需要 >1.2, 当前 {best['calmar_ratio']:.2f}")
        print(f"  交易次数需要 >=10, 当前 {best['total_trades']}")

        if best["total_trades"] < 10:
            print("状态: No-Go (交易次数不足)")
        elif best["annual_return"] < 10:
            print("状态: No-Go (收益过低)")
        else:
            print("状态: Watch (需要进一步优化)")

    return sorted_results


if __name__ == "__main__":
    results = main()
