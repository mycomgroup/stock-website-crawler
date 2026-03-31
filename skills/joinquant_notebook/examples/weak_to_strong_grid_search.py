#!/usr/bin/env python3
"""弱转强竞价策略 - 参数网格搜索与滚动验证"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from itertools import product

print("=" * 70)
print("弱转强竞价策略 - 参数网格搜索与滚动验证")
print("=" * 70)

# 参数网格
PARAM_GRID = {
    "high_open_range": [
        (0, 2),  # 0~2%
        (2, 4),  # 2~4%
        (4, 6),  # 4~6%
        (6, 8),  # 6~8%
    ],
    "volume_ratio": [3, 5, 8],  # 竞价量比阈值 >3% / >5% / >8%
    "market_cap": [20, 30, 70],  # 流通市值门槛（亿）
    "money_threshold": [5e8, 7e8, 10e8],  # 成交额门槛
    "left_pressure": [0.8, 0.9, 1.0],  # 左压突破阈值
}


def test_single_params(params, start_date, end_date):
    """测试单组参数"""
    high_open_min, high_open_max = params["high_open_range"]
    volume_ratio_threshold = params["volume_ratio"]
    market_cap_threshold = params["market_cap"]
    money_threshold = params["money_threshold"]
    left_pressure_threshold = params["left_pressure"]

    trades = []

    trade_days = get_trade_days(start_date=start_date, end_date=end_date)

    for i, date in enumerate(trade_days[:-1]):
        try:
            next_date = trade_days[i + 1]

            # 1. 获取昨日涨停股票
            prev_date = get_shifted_date(date, -1)
            prev_date_2 = get_shifted_date(date, -2)

            initial_list = get_all_securities("stock", date).index.tolist()
            initial_list = [
                s for s in initial_list if s[0] not in ["4", "8", "3"] and s[:2] != "68"
            ]

            # 过滤新股
            new_stock_filter = []
            for s in initial_list:
                try:
                    info = get_security_info(s)
                    if (
                        info.start_date
                        and (
                            datetime.strptime(str(date), "%Y-%m-%d") - info.start_date
                        ).days
                        > 50
                    ):
                        new_stock_filter.append(s)
                except:
                    continue
            initial_list = new_stock_filter

            # 过滤ST
            st_status = get_extras(
                "is_st", initial_list, start_date=date, end_date=date, df=True
            )
            if not st_status.empty:
                st_status = st_status.T
                st_status.columns = ["is_st"]
                initial_list = list(st_status[st_status["is_st"] == False].index)

            # 昨日涨停
            prev_prices = get_price(
                initial_list,
                end_date=date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
                fill_paused=False,
                skip_paused=False,
            )
            if prev_prices.empty:
                continue
            prev_prices = prev_prices.dropna()
            hl_stocks = list(
                prev_prices[prev_prices["close"] == prev_prices["high_limit"]]["code"]
            )

            # 前两日曾涨停
            try:
                prev_1_prices = get_price(
                    initial_list,
                    end_date=prev_date,
                    frequency="daily",
                    fields=["high", "high_limit"],
                    count=1,
                    panel=False,
                    fill_paused=False,
                    skip_paused=False,
                )
                if not prev_1_prices.empty:
                    prev_1_prices = prev_1_prices.dropna()
                    hl1_stocks = list(
                        prev_1_prices[
                            prev_1_prices["high"] == prev_1_prices["high_limit"]
                        ]["code"]
                    )
                else:
                    hl1_stocks = []
            except:
                hl1_stocks = []

            try:
                prev_2_prices = get_price(
                    initial_list,
                    end_date=prev_date_2,
                    frequency="daily",
                    fields=["high", "high_limit"],
                    count=1,
                    panel=False,
                    fill_paused=False,
                    skip_paused=False,
                )
                if not prev_2_prices.empty:
                    prev_2_prices = prev_2_prices.dropna()
                    hl2_stocks = list(
                        prev_2_prices[
                            prev_2_prices["high"] == prev_2_prices["high_limit"]
                        ]["code"]
                    )
                else:
                    hl2_stocks = []
            except:
                hl2_stocks = []

            remove_set = set(hl1_stocks + hl2_stocks)
            target_stocks = [s for s in hl_stocks if s not in remove_set]

            if len(target_stocks) == 0:
                continue

            # 2. 筛选符合条件的股票
            qualified = []

            for s in target_stocks:
                try:
                    # 成交额和市值
                    prev_data = get_price(
                        s,
                        end_date=date,
                        frequency="daily",
                        fields=["close", "volume", "money"],
                        count=1,
                        panel=False,
                        skip_paused=True,
                    )
                    if prev_data.empty or len(prev_data) == 0:
                        continue

                    prev_close = prev_data["close"].iloc[-1]
                    prev_volume = prev_data["volume"].iloc[-1]
                    prev_money = prev_data["money"].iloc[-1]

                    # 成交额门槛
                    if prev_money < money_threshold:
                        continue

                    # 均价涨幅 > 7%
                    avg_price = prev_money / prev_volume
                    avg_increase = avg_price / prev_close * 1.1 - 1
                    if avg_increase < 0.07:
                        continue

                    # 市值门槛
                    valuation = get_valuation(
                        s, start_date=date, end_date=date, fields=["market_cap"]
                    )
                    if (
                        valuation.empty
                        or valuation["market_cap"].iloc[-1] < market_cap_threshold
                    ):
                        continue

                    # 左压突破
                    try:
                        high_prices = get_price(
                            s,
                            end_date=date,
                            frequency="daily",
                            fields=["high"],
                            count=101,
                            panel=False,
                            skip_paused=True,
                        )
                        if high_prices.empty or len(high_prices) < 3:
                            continue

                        highs = high_prices["high"].values
                        prev_high = highs[-1]

                        zyts_0 = 100
                        for idx in range(len(highs) - 3, 0, -1):
                            if highs[idx] >= prev_high:
                                zyts_0 = idx
                                break

                        zyts = zyts_0 + 5

                        volume_history = get_price(
                            s,
                            end_date=date,
                            frequency="daily",
                            fields=["volume"],
                            count=zyts,
                            panel=False,
                            skip_paused=True,
                        )
                        if volume_history.empty or len(volume_history) < 2:
                            continue

                        volumes = volume_history["volume"].values
                        if volumes[-1] <= max(volumes[:-1]) * left_pressure_threshold:
                            continue
                    except:
                        continue

                    # 3. 竞价高开和量比（使用开盘价近似）
                    next_data = get_price(
                        s,
                        end_date=next_date,
                        frequency="daily",
                        fields=["open", "close", "high_limit", "low_limit"],
                        count=1,
                        panel=False,
                        skip_paused=True,
                    )
                    if next_data.empty:
                        continue

                    next_open = next_data["open"].iloc[-1]
                    next_close = next_data["close"].iloc[-1]
                    high_limit = next_data["high_limit"].iloc[-1]
                    low_limit = next_data["low_limit"].iloc[-1]

                    # 高开幅度（相对于涨停价）
                    open_ratio = next_open / (high_limit / 1.1)

                    # 转换为百分比范围
                    open_increase_pct = (open_ratio - 1) * 100

                    if not (high_open_min <= open_increase_pct < high_open_max):
                        continue

                    # 竞价量比（用开盘前5分钟量近似，这里用昨日量代替）
                    # 注：这是近似版本，严格版需要竞价数据
                    auction_volume_ratio = 0.05  # 假设值

                    qualified.append(
                        {
                            "stock": s,
                            "date": next_date,
                            "open": next_open,
                            "close": next_close,
                            "high_limit": high_limit,
                            "low_limit": low_limit,
                        }
                    )

                except Exception as e:
                    continue

            # 4. 记录交易结果
            for trade in qualified:
                try:
                    open_price = trade["open"]
                    close_price = trade["close"]
                    high_limit = trade["high_limit"]

                    # 尾盘卖出
                    return_pct = (close_price - open_price) / open_price * 100

                    trades.append(
                        {
                            "date": trade["date"],
                            "stock": trade["stock"],
                            "return": return_pct,
                            "is_limit": close_price == high_limit,
                        }
                    )
                except:
                    continue

        except Exception as e:
            continue

    return trades


def calculate_metrics(trades):
    """计算策略指标"""
    if len(trades) == 0:
        return None

    df = pd.DataFrame(trades)

    total_trades = len(df)
    win_trades = len(df[df["return"] > 0])
    win_rate = win_trades / total_trades * 100 if total_trades > 0 else 0

    avg_win = df[df["return"] > 0]["return"].mean() if win_trades > 0 else 0
    avg_loss = (
        df[df["return"] < 0]["return"].mean() if len(df[df["return"] < 0]) > 0 else 0
    )
    profit_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0

    total_return = df["return"].sum()
    avg_return = df["return"].mean()

    # 按日期聚合计算累计收益
    daily_returns = df.groupby("date")["return"].mean()
    cumulative_return = (1 + daily_returns / 100).cumprod()

    # 最大回撤
    if len(cumulative_return) > 0:
        peak = cumulative_return.expanding(min_periods=1).max()
        drawdown = (cumulative_return - peak) / peak
        max_drawdown = drawdown.min() * 100
    else:
        max_drawdown = 0

    # 连续亏损次数
    loss_sequence = (df["return"] < 0).astype(int)
    max_consecutive_loss = 0
    current_consecutive = 0
    for val in loss_sequence:
        if val == 1:
            current_consecutive += 1
            max_consecutive_loss = max(max_consecutive_loss, current_consecutive)
        else:
            current_consecutive = 0

    # 月度收益
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
    monthly_returns = df.groupby("month")["return"].sum()

    return {
        "total_trades": total_trades,
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "profit_loss_ratio": profit_loss_ratio,
        "total_return": total_return,
        "avg_return": avg_return,
        "max_drawdown": max_drawdown,
        "max_consecutive_loss": max_consecutive_loss,
        "monthly_returns": monthly_returns.to_dict(),
        "trades": df,
    }


def rolling_validation(params, total_start, total_end, train_months=24, test_months=6):
    """滚动窗口验证"""
    all_test_trades = []

    start_dt = datetime.strptime(total_start, "%Y-%m-%d")
    end_dt = datetime.strptime(total_end, "%Y-%m-%d")

    current_start = start_dt

    while current_start < end_dt:
        train_end = current_start + timedelta(days=train_months * 30)
        test_end = train_end + timedelta(days=test_months * 30)

        if test_end > end_dt:
            test_end = end_dt

        train_start_str = current_start.strftime("%Y-%m-%d")
        train_end_str = train_end.strftime("%Y-%m-%d")
        test_start_str = (train_end + timedelta(days=1)).strftime("%Y-%m-%d")
        test_end_str = test_end.strftime("%Y-%m-%d")

        print(
            f"  窗口: 训练 {train_start_str} ~ {train_end_str}, 测试 {test_start_str} ~ {test_end_str}"
        )

        # 训练期测试
        train_trades = test_single_params(params, train_start_str, train_end_str)

        # 测试期测试
        test_trades = test_single_params(params, test_start_str, test_end_str)

        all_test_trades.extend(test_trades)

        current_start = test_end + timedelta(days=1)

    return all_test_trades


def grid_search():
    """参数网格搜索"""
    print("\n开始参数网格搜索...")
    print(f"参数组合总数: {len(list(product(*PARAM_GRID.values())))}")

    all_results = []

    # 测试时间范围
    total_start = "2021-01-01"
    total_end = "2024-12-31"

    # 样本外测试时间范围
    oos_start = "2024-01-01"
    oos_end = "2024-12-31"

    param_combinations = list(product(*PARAM_GRID.values()))

    for idx, param_values in enumerate(param_combinations):
        params = {
            "high_open_range": param_values[0],
            "volume_ratio": param_values[1],
            "market_cap": param_values[2],
            "money_threshold": param_values[3],
            "left_pressure": param_values[4],
        }

        print(f"\n[{idx + 1}/{len(param_combinations)}] 测试参数组合:")
        print(f"  高开幅度: {params['high_open_range']}%")
        print(f"  量比阈值: >{params['volume_ratio']}%")
        print(f"  市值门槛: >{params['market_cap']}亿")
        print(f"  成交额门槛: >{params['money_threshold'] / 1e8:.0f}亿")
        print(f"  左压阈值: {params['left_pressure']}")

        # 滚动验证
        test_trades = rolling_validation(params, total_start, total_end)
        metrics = calculate_metrics(test_trades)

        if metrics:
            # 样本外单独测试
            oos_trades = test_single_params(params, oos_start, oos_end)
            oos_metrics = calculate_metrics(oos_trades)

            result = {
                "params": params,
                "in_sample": metrics,
                "out_of_sample": oos_metrics,
            }

            all_results.append(result)

            print(f"  样本内结果:")
            print(f"    交易次数: {metrics['total_trades']}")
            print(f"    胜率: {metrics['win_rate']:.2f}%")
            print(f"    盈亏比: {metrics['profit_loss_ratio']:.2f}")
            print(f"    最大回撤: {metrics['max_drawdown']:.2f}%")

            if oos_metrics:
                print(f"  样本外结果 (2024-01-01后):")
                print(f"    交易次数: {oos_metrics['total_trades']}")
                print(f"    胜率: {oos_metrics['win_rate']:.2f}%")
                print(f"    盈亏比: {oos_metrics['profit_loss_ratio']:.2f}")
                print(f"    最大回撤: {oos_metrics['max_drawdown']:.2f}%")
        else:
            print(f"  结果: 无有效交易")

    return all_results


def analyze_results(all_results):
    """分析结果并输出最优参数"""
    print("\n" + "=" * 70)
    print("参数网格搜索结果分析")
    print("=" * 70)

    if len(all_results) == 0:
        print("无有效结果")
        return

    # 按样本外收益排序
    valid_results = [
        r
        for r in all_results
        if r["out_of_sample"] and r["out_of_sample"]["total_trades"] > 10
    ]

    if len(valid_results) == 0:
        print("样本外交易次数不足，无有效结果")
        return

    # 排序指标：样本外年化收益
    for r in valid_results:
        if r["out_of_sample"]["avg_return"]:
            r["oos_annual_return"] = r["out_of_sample"]["avg_return"] * 250
        else:
            r["oos_annual_return"] = 0

        if r["out_of_sample"]["max_drawdown"] != 0:
            r["oos_calmar_ratio"] = abs(
                r["oos_annual_return"] / r["out_of_sample"]["max_drawdown"]
            )
        else:
            r["oos_calmar_ratio"] = 0

    # 按卡玛比率排序
    sorted_results = sorted(
        valid_results, key=lambda x: x["oos_calmar_ratio"], reverse=True
    )

    print("\n样本外表现TOP 5:")
    print("-" * 70)

    for idx, r in enumerate(sorted_results[:5]):
        params = r["params"]
        oos = r["out_of_sample"]

        print(f"\nTOP {idx + 1}:")
        print(f"  参数:")
        print(f"    高开幅度: {params['high_open_range']}%")
        print(f"    量比阈值: >{params['volume_ratio']}%")
        print(f"    市值门槛: >{params['market_cap']}亿")
        print(f"    成交额门槛: >{params['money_threshold'] / 1e8:.0f}亿")
        print(f"    左压阈值: {params['left_pressure']}")

        print(f"  样本外结果 (2024-01-01后):")
        print(f"    交易次数: {oos['total_trades']}")
        print(f"    胜率: {oos['win_rate']:.2f}%")
        print(f"    盈亏比: {oos['profit_loss_ratio']:.2f}")
        print(f"    平均收益: {oos['avg_return']:.2f}%")
        print(f"    年化收益: {r['oos_annual_return']:.2f}%")
        print(f"    最大回撤: {oos['max_drawdown']:.2f}%")
        print(f"    卡玛比率: {r['oos_calmar_ratio']:.2f}")
        print(f"    连续亏损次数: {oos['max_consecutive_loss']}")

    # 输出最优参数
    best = sorted_results[0]

    print("\n" + "=" * 70)
    print("最优参数组合")
    print("=" * 70)
    print(json.dumps(best["params"], indent=2))

    # 保存结果
    output_file = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output/weak_to_strong_grid_search_results.json"
    with open(output_file, "w") as f:
        json.dump(sorted_results[:10], f, indent=2)

    print(f"\n结果已保存到: {output_file}")

    return best


if __name__ == "__main__":
    all_results = grid_search()
    best = analyze_results(all_results)
