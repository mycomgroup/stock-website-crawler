from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

"""
任务01：主线信号定义收敛
目标：将首板低开从多个有效片段收敛成1个主版本+1个备选版本

结构分组：
1. 假弱高开：开盘涨跌幅 +0.5%~+1.5%
2. 真低开A：开盘涨跌幅 -3.0%~-1.0%
3. 真低开B：开盘涨跌幅 -1.0%~0.0%
4. 边界样本A：开盘涨跌幅 0.0%~+0.5%（平开附近）
5. 边界样本B：开盘涨跌幅 -5.0%~-3.0%（深度低开）
6. 边界样本C：开盘涨跌幅 +1.5%~+2.5%（微高开）

统一买点：开盘价买入（集合竞价可得）
卖出策略：
- S1：当日收盘价卖出
- S2：次日开盘价卖出
- S3：次日收盘价卖出
- S4：次日最高价卖出（理想卖出）

训练期：2021-01-01 ~ 2023-12-31
验证期：2024-01-01 ~ 2024-12-31
样本外：2025-01-01 ~ 2026-03-31（如数据充足）
"""


def get_first_board_signals(start_date, end_date):
    """
    获取首板信号
    """
    signals = []

    trade_days = get_trade_days(start_date, end_date)

    for i, date in enumerate(trade_days[:-1]):
        try:
            current_date = date
            prev_date = trade_days[i - 1] if i > 0 else None

            if prev_date is None:
                continue

            prev_stocks = get_all_securities("stock", prev_date).index.tolist()
            current_stocks = get_all_securities("stock", current_date).index.tolist()

            for stock in prev_stocks[:500]:
                try:
                    prev_price = get_price(
                        stock,
                        end_date=prev_date,
                        count=1,
                        fields=["close", "high_limit"],
                        panel=False,
                    )
                    curr_price = get_price(
                        stock,
                        end_date=current_date,
                        count=1,
                        fields=[
                            "open",
                            "close",
                            "high",
                            "low",
                            "high_limit",
                            "low_limit",
                        ],
                        panel=False,
                    )

                    if prev_price.empty or curr_price.empty:
                        continue

                    prev_close = float(prev_price["close"].iloc[0])
                    prev_high_limit = float(prev_price["high_limit"].iloc[0])
                    curr_open = float(curr_price["open"].iloc[0])
                    curr_close = float(curr_price["close"].iloc[0])
                    curr_high = float(curr_price["high"].iloc[0])
                    curr_low = float(curr_price["low"].iloc[0])
                    curr_high_limit = float(curr_price["high_limit"].iloc[0])
                    curr_low_limit = float(curr_price["low_limit"].iloc[0])

                    if abs(prev_close - prev_high_limit) / prev_high_limit < 0.001:
                        open_pct = (curr_open - prev_close) / prev_close * 100

                        signal = {
                            "date": current_date,
                            "stock": stock,
                            "prev_close": prev_close,
                            "curr_open": curr_open,
                            "open_pct": open_pct,
                            "curr_close": curr_close,
                            "curr_high": curr_high,
                            "curr_low": curr_low,
                            "curr_high_limit": curr_high_limit,
                            "curr_low_limit": curr_low_limit,
                        }
                        signals.append(signal)
                except Exception as e:
                    continue
        except Exception as e:
            continue

    return pd.DataFrame(signals)


def classify_open_type(open_pct):
    """
    分类开盘类型
    """
    if 0.5 <= open_pct <= 1.5:
        return "假弱高开"
    elif -3.0 <= open_pct < -1.0:
        return "真低开A"
    elif -1.0 <= open_pct < 0.0:
        return "真低开B"
    elif 0.0 <= open_pct < 0.5:
        return "边界样本A_平开附近"
    elif -5.0 <= open_pct < -3.0:
        return "边界样本B_深度低开"
    elif 1.5 <= open_pct <= 2.5:
        return "边界样本C_微高开"
    else:
        return "其他"


def calculate_returns(signal, next_date=None):
    """
    计算各种卖出策略的收益
    """
    results = {}

    open_price = signal["curr_open"]

    results["S1_当日收盘"] = (signal["curr_close"] - open_price) / open_price * 100

    results["S4_次日最高"] = (
        (signal["curr_high"] - open_price) / open_price * 100
        if signal["curr_high"] > open_price
        else results["S1_当日收盘"]
    )

    if next_date:
        try:
            next_price = get_price(
                signal["stock"],
                end_date=next_date,
                count=1,
                fields=["open", "close", "high"],
                panel=False,
            )
            if not next_price.empty:
                next_open = float(next_price["open"].iloc[0])
                next_close = float(next_price["close"].iloc[0])
                next_high = float(next_price["high"].iloc[0])

                results["S2_次日开盘"] = (next_open - open_price) / open_price * 100
                results["S3_次日收盘"] = (next_close - open_price) / open_price * 100
                results["S4_次日最高"] = (next_high - open_price) / open_price * 100
        except:
            results["S2_次日开盘"] = None
            results["S3_次日收盘"] = None
            results["S4_次日最高"] = results["S4_当日最高"]

    return results


def run_analysis():
    """
    运行完整分析
    """
    print("开始首板信号收敛分析...")
    print("=" * 80)

    print("\n阶段1: 训练期 (2021-01-01 ~ 2023-12-31)")
    train_signals = get_first_board_signals("2021-01-01", "2023-12-31")
    print(f"训练期信号数: {len(train_signals)}")

    print("\n阶段2: 验证期 (2024-01-01 ~ 2024-12-31)")
    valid_signals = get_first_board_signals("2024-01-01", "2024-12-31")
    print(f"验证期信号数: {len(valid_signals)}")

    print("\n阶段3: 样本外期 (2025-01-01 ~ 2026-03-31)")
    test_signals = get_first_board_signals("2025-01-01", "2026-03-31")
    print(f"样本外期信号数: {len(test_signals)}")

    all_signals = pd.concat(
        [train_signals, valid_signals, test_signals], ignore_index=True
    )

    print("\n阶段4: 分类开盘类型")
    all_signals["open_type"] = all_signals["open_pct"].apply(classify_open_type)

    print("\n阶段5: 计算收益")

    type_stats = []

    for open_type in all_signals["open_type"].unique():
        if open_type == "其他":
            continue

        subset = all_signals[all_signals["open_type"] == open_type]

        stats = {
            "open_type": open_type,
            "count": len(subset),
            "avg_open_pct": subset["open_pct"].mean(),
            "S1_当日收盘_均值": subset.apply(
                lambda x: (x["curr_close"] - x["curr_open"]) / x["curr_open"] * 100,
                axis=1,
            ).mean(),
            "S4_次日最高_均值": subset.apply(
                lambda x: (x["curr_high"] - x["curr_open"]) / x["curr_open"] * 100,
                axis=1,
            ).mean(),
            "胜率_S1": (
                subset.apply(
                    lambda x: (x["curr_close"] - x["curr_open"]) / x["curr_open"] * 100,
                    axis=1,
                )
                > 0
            ).sum()
            / len(subset)
            * 100,
        }

        type_stats.append(stats)

    results_df = pd.DataFrame(type_stats)
    results_df = results_df.sort_values("S4_次日最高_均值", ascending=False)

    print("\n结构分组收益对比:")
    print("=" * 80)
    print(results_df.to_string(index=False))

    train_results = results_df[results_df["open_type"] != "其他"].copy()

    valid_stats = []
    for open_type in valid_signals["open_type"].unique():
        if open_type == "其他":
            continue

        subset = valid_signals[valid_signals["open_type"] == open_type]

        stats = {
            "open_type": open_type,
            "count": len(subset),
            "avg_open_pct": subset["open_pct"].mean(),
            "S1_当日收盘_均值": subset.apply(
                lambda x: (x["curr_close"] - x["curr_open"]) / x["curr_open"] * 100,
                axis=1,
            ).mean(),
            "S4_次日最高_均值": subset.apply(
                lambda x: (x["curr_high"] - x["curr_open"]) / x["curr_open"] * 100,
                axis=1,
            ).mean(),
            "胜率_S1": (
                subset.apply(
                    lambda x: (x["curr_close"] - x["curr_open"]) / x["curr_open"] * 100,
                    axis=1,
                )
                > 0
            ).sum()
            / len(subset)
            * 100
            if len(subset) > 0
            else 0,
        }

        valid_stats.append(stats)

    valid_results = pd.DataFrame(valid_stats)

    print("\n验证期 (2024) 结果:")
    print("=" * 80)
    print(valid_results.to_string(index=False))

    test_stats = []
    for open_type in test_signals["open_type"].unique():
        if open_type == "其他":
            continue

        subset = test_signals[test_signals["open_type"] == open_type]

        stats = {
            "open_type": open_type,
            "count": len(subset),
            "avg_open_pct": subset["open_pct"].mean(),
            "S1_当日收盘_均值": subset.apply(
                lambda x: (x["curr_close"] - x["curr_open"]) / x["curr_open"] * 100,
                axis=1,
            ).mean(),
            "S4_次日最高_均值": subset.apply(
                lambda x: (x["curr_high"] - x["curr_open"]) / x["curr_open"] * 100,
                axis=1,
            ).mean(),
            "胜率_S1": (
                subset.apply(
                    lambda x: (x["curr_close"] - x["curr_open"]) / x["curr_open"] * 100,
                    axis=1,
                )
                > 0
            ).sum()
            / len(subset)
            * 100
            if len(subset) > 0
            else 0,
        }

        test_stats.append(stats)

    test_results = pd.DataFrame(test_stats)

    print("\n样本外期 (2025-2026) 结果:")
    print("=" * 80)
    print(test_results.to_string(index=False))

    print("\n最终结论:")
    print("=" * 80)

    if len(train_results) > 0:
        best_train = train_results.iloc[0]
        print(f"\n训练期最佳结构: {best_train['open_type']}")
        print(f"  - 信号数: {best_train['count']}")
        print(f"  - 日内收益: {best_train['S1_当日收盘_均值']:.2f}%")
        print(f"  - 次日最高收益: {best_train['S4_次日最高_均值']:.2f}%")
        print(f"  - 胜率: {best_train['胜率_S1']:.1f}%")

    return results_df, valid_results, test_results


if __name__ == "__main__":
    results_df, valid_results, test_results = run_analysis()

    output_file = "/Users/fengzhi/Downloads/git/testlixingren/output/first_board_signal_convergence.json"
    import json

    output_data = {
        "timestamp": datetime.now().isoformat(),
        "train_results": results_df.to_dict("records"),
        "valid_results": valid_results.to_dict("records")
        if len(valid_results) > 0
        else [],
        "test_results": test_results.to_dict("records")
        if len(test_results) > 0
        else [],
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存至: {output_file}")
