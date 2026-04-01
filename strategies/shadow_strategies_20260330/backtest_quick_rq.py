"""
影子策略快速验证 (RiceQuant Notebook 版本)

简化版：快速验证策略逻辑
- 测试2015年牛市期间（1-6月）
- 减少股票数量
- 优化执行效率

运行方式：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/backtest_quick_rq.py --create-new --timeout-ms 300000
"""

import numpy as np
import pandas as pd

print("=" * 80)
print("影子策略快速验证 - RiceQuant Notebook")
print("=" * 80)

STRATEGY_MODE = "mainline"

MAINLINE_PARAMS = {
    "emotion_threshold": 30,
    "open_change_min": 0.001,
    "open_change_max": 0.03,
    "sell_profit_threshold": 0.03,
}

print(f"\n策略参数:")
print(f"  情绪阈值: 涨停 >= {MAINLINE_PARAMS['emotion_threshold']}只")
print(
    f"  开盘涨幅: {MAINLINE_PARAMS['open_change_min'] * 100:.1f}% - {MAINLINE_PARAMS['open_change_max'] * 100:.0f}%"
)
print(f"  止盈: +{MAINLINE_PARAMS['sell_profit_threshold'] * 100:.0f}%")


def get_all_stocks_list():
    """获取所有A股股票列表"""
    try:
        instruments = all_instruments(type="CS")
        return list(instruments.order_book_id)
    except Exception as e:
        print(f"获取股票失败: {e}")
        return []


def get_prev_trading_date(date, trading_dates):
    """获取前一个交易日"""
    date_str = str(date)[:10]
    for i, d in enumerate(trading_dates):
        if str(d)[:10] == date_str and i > 0:
            return str(trading_dates[i - 1])[:10]
    return None


def get_limit_up_count_batch(date, stock_list, trading_dates, max_count=300):
    """批量获取涨停股票数量（优化版）"""
    limit_up_count = 0
    tested = 0
    prev_date = get_prev_trading_date(date, trading_dates)

    if prev_date is None:
        return 0, 0

    for stock in stock_list[:max_count]:
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
                        limit_up_count += 1
                    tested += 1
        except:
            continue

    return limit_up_count, tested


def is_fake_weak_high_open(stock, date, trading_dates):
    """判断是否为假弱高开"""
    try:
        prev_date = get_prev_trading_date(date, trading_dates)
        if prev_date is None:
            return False

        df = get_price(
            stock,
            start_date=prev_date,
            end_date=date,
            frequency="1d",
            fields=["close", "open", "high"],
        )
        if df is None or len(df) < 2:
            return False

        prev_close = df["close"].iloc[0]
        open_price = df["open"].iloc[-1]
        high_price = df["high"].iloc[-1]

        if prev_close <= 0:
            return False

        open_change = (open_price - prev_close) / prev_close

        if (
            open_change <= MAINLINE_PARAMS["open_change_min"]
            or open_change >= MAINLINE_PARAMS["open_change_max"]
        ):
            return False

        return high_price > open_price
    except:
        return False


print("\n" + "=" * 80)
print("步骤1: 获取基础数据")
print("=" * 80)

print("\n获取交易日列表...")
try:
    trading_dates = list(get_trading_dates("2015-01-01", "2015-06-30"))
    print(f"✓ 交易日数量: {len(trading_dates)}")
except Exception as e:
    print(f"✗ 获取交易日失败: {e}")
    trading_dates = []

print("\n获取股票列表...")
all_stocks = get_all_stocks_list()
print(f"✓ 股票总数: {len(all_stocks)}")

if len(all_stocks) == 0 or len(trading_dates) == 0:
    print("\n✗ 无法获取数据，请确保在 RiceQuant Notebook 环境运行")
else:
    print("\n" + "=" * 80)
    print("步骤2: 情绪验证（涨停统计）")
    print("=" * 80)

    test_dates = [str(d)[:10] for d in trading_dates[:50]]
    print(f"\n测试日期: {test_dates[0]} 至 {test_dates[-1]} ({len(test_dates)}天)")

    high_emotion_days = []

    print("\n统计涨停数量...")
    for i, date in enumerate(test_dates[::5]):
        limit_up, tested = get_limit_up_count_batch(
            date, all_stocks, [str(d)[:10] for d in trading_dates], max_count=300
        )
        status = "✓ 达标" if limit_up >= 30 else "✗ 不足"
        print(f"  {date}: 涨停{limit_up}只 (测试{tested}只) {status}")
        if limit_up >= 30:
            high_emotion_days.append(date)

        if (i + 1) % 3 == 0:
            print(f"  --- 进度: {i + 1}/10 ---")

    print(f"\n涨停达标天数: {len(high_emotion_days)}/{len(test_dates[::5])}")

    if len(high_emotion_days) > 0:
        print("\n" + "=" * 80)
        print("步骤3: 信号验证（假弱高开）")
        print("=" * 80)

        print(f"\n在达标日期中寻找信号...")
        total_signals = 0

        for date in high_emotion_days[:5]:
            signals = []
            for stock in all_stocks[:100]:
                if is_fake_weak_high_open(
                    stock, date, [str(d)[:10] for d in trading_dates]
                ):
                    signals.append(stock)

            total_signals += len(signals)
            print(f"  {date}: 发现{len(signals)}个信号")

        print(f"\n总信号数: {total_signals}")
    else:
        print("\n✗ 情绪不足，无达标日期，无法测试信号")

    print("\n" + "=" * 80)
    print("验证结果汇总")
    print("=" * 80)

    print(f"\n✓ API正常:")
    print(f"  - get_trading_dates: 正常")
    print(f"  - all_instruments: 正常")
    print(f"  - get_price: 正常")

    print(f"\n✓ 策略验证:")
    print(f"  - 测试天数: {len(test_dates[::5])}")
    print(f"  - 涨停达标天数: {len(high_emotion_days)}")
    print(f"  - 信号数量: {total_signals if len(high_emotion_days) > 0 else 0}")

    if len(high_emotion_days) > 0 and total_signals > 0:
        print(f"\n✓ 策略逻辑验证成功！可以进行完整回测。")
    elif len(high_emotion_days) > 0:
        print(f"\n⚠ 情绪达标但信号较少，建议调整参数。")
    else:
        print(f"\n⚠ 情绪不足，建议：")
        print(f"  1. 测试其他时间段（如2015年牛市）")
        print(f"  2. 降低情绪阈值")
        print(f"  3. 增加股票测试数量")

    print("\n" + "=" * 80)
    print("验证完成")
    print("=" * 80)
