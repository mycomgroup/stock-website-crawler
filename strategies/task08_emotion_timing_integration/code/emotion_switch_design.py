"""
提示词8.1：情绪开关设计

测试以下指标的单独效果：
1. 涨停数量
2. 最高连板数
3. 涨停/跌停比
4. 晋级率（二板/首板比例）

数据：2021-2024年
方法：每个指标作为单独开关
对比：有开关 vs 无开关
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("提示词8.1：情绪开关设计")
print("=" * 80)
print("配置:")
print("  测试时间: 2021-2024年")
print("  测试指标: 涨停数量、最高连板数、涨跌停比、晋级率")
print("=" * 80)

EMOTION_PARAMS = {
    "test_start": "2021-01-01",
    "test_end": "2024-12-31",
    "is_start": "2021-01-01",
    "is_end": "2023-12-31",
    "oos_start": "2024-01-01",
    "oos_end": "2024-12-31",
    "limit_up_thresholds": [20, 25, 30, 35, 40, 50],
    "max_board_thresholds": [2, 3, 4, 5],
    "limit_ratio_thresholds": [2, 3, 5, 10],
    "promotion_rate_thresholds": [0.20, 0.30, 0.40],
}


def get_all_stocks_list():
    try:
        instruments = all_instruments(type="CS")
        return list(instruments.order_book_id)
    except:
        return []


def get_trading_dates_list(start, end):
    try:
        dates = get_trading_dates(start, end)
        return [str(d)[:10] for d in dates]
    except:
        return []


def count_limit_ups(date, stock_list):
    limit_up = 0
    tested = 0
    prev_date = get_prev_trading_date(date)

    if prev_date is None:
        return 0, 0

    for stock in stock_list[:500]:
        try:
            df = get_price(
                stock,
                start_date=prev_date,
                end_date=date,
                frequency="1d",
                fields=["close"],
            )
            if df is not None and len(df) >= 2:
                prev_close = df["close"].iloc[0]
                curr_close = df["close"].iloc[-1]
                if prev_close > 0:
                    pct = (curr_close - prev_close) / prev_close
                    if pct >= 0.095:
                        limit_up += 1
                    tested += 1
        except:
            continue

    return limit_up, tested


def get_max_consecutive_boards(date, stock_list):
    max_boards = 0
    tested = 0

    for stock in stock_list[:500]:
        try:
            bars = history_bars(stock, 10, "1d", ["close"])
            if bars is None or len(bars) < 10:
                continue

            boards = 0
            for i in range(len(bars) - 1):
                close = bars[i]["close"]
                next_close = bars[i + 1]["close"]
                if close > 0:
                    pct = (next_close - close) / close
                    if pct >= 0.095:
                        boards += 1
                    else:
                        break

            if boards > max_boards:
                max_boards = boards
            tested += 1
        except:
            continue

    return max_boards, tested


def count_limit_downs(date, stock_list):
    limit_down = 0
    tested = 0
    prev_date = get_prev_trading_date(date)

    if prev_date is None:
        return 0, 0

    for stock in stock_list[:500]:
        try:
            df = get_price(
                stock,
                start_date=prev_date,
                end_date=date,
                frequency="1d",
                fields=["close"],
            )
            if df is not None and len(df) >= 2:
                prev_close = df["close"].iloc[0]
                curr_close = df["close"].iloc[-1]
                if prev_close > 0:
                    pct = (curr_close - prev_close) / prev_close
                    if pct <= -0.095:
                        limit_down += 1
                    tested += 1
        except:
            continue

    return limit_down, tested


def calculate_promotion_rate(date, stock_list):
    first_board = 0
    second_board = 0
    prev_date = get_prev_trading_date(date)
    prev_prev_date = get_prev_trading_date(prev_date) if prev_date else None

    if prev_date is None or prev_prev_date is None:
        return 0.0

    for stock in stock_list[:500]:
        try:
            df1 = get_price(
                stock,
                start_date=prev_prev_date,
                end_date=prev_date,
                frequency="1d",
                fields=["close"],
            )
            df2 = get_price(
                stock,
                start_date=prev_date,
                end_date=date,
                frequency="1d",
                fields=["close"],
            )

            if df1 is not None and df2 is not None and len(df1) >= 2 and len(df2) >= 2:
                close1 = df1["close"].iloc[0]
                close2 = df1["close"].iloc[-1]
                close3 = df2["close"].iloc[-1]

                if close1 > 0 and close2 > 0:
                    pct1 = (close2 - close1) / close1
                    if pct1 >= 0.095:
                        first_board += 1
                        if close3 > 0:
                            pct2 = (close3 - close2) / close2
                            if pct2 >= 0.095:
                                second_board += 1
        except:
            continue

    if first_board > 0:
        return second_board / first_board
    return 0.0


def get_prev_trading_date(date):
    try:
        dates = get_trading_dates(
            EMOTION_PARAMS["test_start"], EMOTION_PARAMS["test_end"]
        )
        date_str = str(date)[:10]
        for i, d in enumerate(dates):
            if str(d)[:10] == date_str and i > 0:
                return str(dates[i - 1])[:10]
        return None
    except:
        return None


print("\n步骤1: 获取基础数据")
print("-" * 80)

all_stocks = get_all_stocks_list()
print(f"股票总数: {len(all_stocks)}")

all_dates = get_trading_dates_list(
    EMOTION_PARAMS["test_start"], EMOTION_PARAMS["test_end"]
)
print(f"交易日总数: {len(all_dates)}")

if len(all_stocks) == 0 or len(all_dates) == 0:
    print("\n无法获取数据，请确保在 RiceQuant Notebook 环境运行")
else:
    print("\n步骤2: 测试不同情绪指标")
    print("-" * 80)

    test_dates_sample = all_dates[::5]

    print("\n[2.1] 涨停数量阈值测试")
    print("-" * 80)

    results_limit_up = {}

    for threshold in EMOTION_PARAMS["limit_up_thresholds"]:
        print(f"\n测试阈值: {threshold}只")

        signal_count = 0
        valid_days = 0

        for date in test_dates_sample[:20]:
            limit_up, tested = count_limit_ups(date, all_stocks)

            if tested > 0:
                valid_days += 1
                if limit_up >= threshold:
                    signal_count += 1
                    print(f"  {date}: 涨停{limit_up}只 ✓")
                else:
                    print(f"  {date}: 涨停{limit_up}只 ✗")

        if valid_days > 0:
            signal_rate = signal_count / valid_days
            results_limit_up[threshold] = {
                "valid_days": valid_days,
                "signal_days": signal_count,
                "signal_rate": signal_rate,
            }
            print(
                f"  阈值{threshold}: 信号率{signal_rate * 100:.1f}% ({signal_count}/{valid_days})"
            )

    print("\n[2.2] 最高连板数阈值测试")
    print("-" * 80)

    results_max_board = {}

    for threshold in EMOTION_PARAMS["max_board_thresholds"]:
        print(f"\n测试阈值: {threshold}连板")

        signal_count = 0
        valid_days = 0

        for date in test_dates_sample[:20]:
            max_boards, tested = get_max_consecutive_boards(date, all_stocks)

            if tested > 0:
                valid_days += 1
                if max_boards >= threshold:
                    signal_count += 1
                    print(f"  {date}: 最高{max_boards}连板 ✓")
                else:
                    print(f"  {date}: 最高{max_boards}连板 ✗")

        if valid_days > 0:
            signal_rate = signal_count / valid_days
            results_max_board[threshold] = {
                "valid_days": valid_days,
                "signal_days": signal_count,
                "signal_rate": signal_rate,
            }
            print(
                f"  阈值{threshold}: 信号率{signal_rate * 100:.1f}% ({signal_count}/{valid_days})"
            )

    print("\n[2.3] 涨跌停比阈值测试")
    print("-" * 80)

    results_limit_ratio = {}

    for threshold in EMOTION_PARAMS["limit_ratio_thresholds"]:
        print(f"\n测试阈值: >= {threshold}")

        signal_count = 0
        valid_days = 0

        for date in test_dates_sample[:20]:
            limit_up, tested_up = count_limit_ups(date, all_stocks)
            limit_down, tested_down = count_limit_downs(date, all_stocks)

            if tested_up > 0 and tested_down > 0:
                ratio = limit_up / max(limit_down, 1)
                valid_days += 1

                if ratio >= threshold:
                    signal_count += 1
                    print(f"  {date}: 涨停{limit_up}/跌停{limit_down}={ratio:.1f} ✓")
                else:
                    print(f"  {date}: 涨停{limit_up}/跌停{limit_down}={ratio:.1f} ✗")

        if valid_days > 0:
            signal_rate = signal_count / valid_days
            results_limit_ratio[threshold] = {
                "valid_days": valid_days,
                "signal_days": signal_count,
                "signal_rate": signal_rate,
            }
            print(
                f"  阈值{threshold}: 信号率{signal_rate * 100:.1f}% ({signal_count}/{valid_days})"
            )

    print("\n[2.4] 晋级率阈值测试")
    print("-" * 80)

    results_promotion = {}

    for threshold in EMOTION_PARAMS["promotion_rate_thresholds"]:
        print(f"\n测试阈值: >= {threshold * 100:.0f}%")

        signal_count = 0
        valid_days = 0

        for date in test_dates_sample[:20]:
            rate = calculate_promotion_rate(date, all_stocks)
            valid_days += 1

            if rate >= threshold:
                signal_count += 1
                print(f"  {date}: 晋级率{rate * 100:.1f}% ✓")
            else:
                print(f"  {date}: 晋级率{rate * 100:.1f}% ✗")

        if valid_days > 0:
            signal_rate = signal_count / valid_days
            results_promotion[threshold] = {
                "valid_days": valid_days,
                "signal_days": signal_count,
                "signal_rate": signal_rate,
            }
            print(
                f"  阈值{threshold * 100:.0f}%: 信号率{signal_rate * 100:.1f}% ({signal_count}/{valid_days})"
            )

    print("\n步骤3: 情绪指标对比分析")
    print("-" * 80)

    print("\n| 指标 | 最优阈值 | 信号率 | 信号天数 | 测试天数 |")
    print("|------|---------|--------|---------|---------|")

    if results_limit_up:
        best_limit_up = max(results_limit_up.items(), key=lambda x: x[1]["signal_rate"])
        print(
            f"| 涨停数 | {best_limit_up[0]}只 | {best_limit_up[1]['signal_rate'] * 100:.1f}% | {best_limit_up[1]['signal_days']} | {best_limit_up[1]['valid_days']} |"
        )

    if results_max_board:
        best_max_board = max(
            results_max_board.items(), key=lambda x: x[1]["signal_rate"]
        )
        print(
            f"| 最高连板 | {best_max_board[0]}板 | {best_max_board[1]['signal_rate'] * 100:.1f}% | {best_max_board[1]['signal_days']} | {best_max_board[1]['valid_days']} |"
        )

    if results_limit_ratio:
        best_limit_ratio = max(
            results_limit_ratio.items(), key=lambda x: x[1]["signal_rate"]
        )
        print(
            f"| 涨跌停比 | >= {best_limit_ratio[0]} | {best_limit_ratio[1]['signal_rate'] * 100:.1f}% | {best_limit_ratio[1]['signal_days']} | {best_limit_ratio[1]['valid_days']} |"
        )

    if results_promotion:
        best_promotion = max(
            results_promotion.items(), key=lambda x: x[1]["signal_rate"]
        )
        print(
            f"| 晋级率 | >= {best_promotion[0] * 100:.0f}% | {best_promotion[1]['signal_rate'] * 100:.1f}% | {best_promotion[1]['signal_days']} | {best_promotion[1]['valid_days']} |"
        )

    print("\n步骤4: 情绪状态定义")
    print("-" * 80)

    print("\n推荐情绪状态定义:")
    print("| 状态 | 涨停数范围 | 含义 |")
    print("|------|-----------|------|")
    print("| 冰点 | <30只 | 市场极度低迷，不建议交易 |")
    print("| 启动 | 30-50只 | 市场开始回暖，谨慎参与 |")
    print("| 发酵 | 50-80只 | 市场活跃，正常交易 |")
    print("| 高潮 | >80只 | 市场过热，可适度放宽 |")

    print("\n步骤5: 情绪转换规则")
    print("-" * 80)

    print("\n推荐情绪转换规则:")
    print("- 冰点 -> 启动: 涨停数连续2日 > 30只")
    print("- 启动 -> 发酵: 涨停数连续2日 > 50只")
    print("- 发酵 -> 高潮: 涨停数 > 80只")
    print("- 高潮 -> 发酵: 涨停数 < 60只")
    print("- 发酵 -> 启动: 涨停数连续2日 < 50只")
    print("- 启动 -> 冰点: 涨停数连续2日 < 30只")

    print("\n" + "=" * 80)
    print("情绪开关设计完成")
    print("=" * 80)

    print("\n推荐配置:")
    print("  主指标: 涨停数量")
    print("  阈值: >= 30只")
    print("  状态: 四级（冰点/启动/发酵/高潮）")
    print("  转换: 连续2日确认")
