"""
大面股数量指标测试 - JoinQuant版本

测试目标：
对比两组情绪择时框架的表现：
- A组：原始情绪开关（涨停家数+连板数）
- B组：新增大面股（涨停家数+连板数+大面股<50）

接入策略：首板低开策略
时间范围：2024-01-01 至 2025-12-31
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 80)
print("大面股数量指标测试")
print("=" * 80)

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

print(f"\n测试范围: {START_DATE} 至 {END_DATE}")
print(f"接入策略: 首板低开策略")


def get_zt_count_and_lianban(date):
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
    )
    df = df.dropna()

    zt_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()
    zt_count = len(zt_stocks)

    max_lianban = 0
    if len(zt_stocks) > 0:
        for stock in zt_stocks[:30]:
            df_lb = get_price(
                stock,
                end_date=date,
                count=10,
                fields=["close", "high_limit"],
                panel=False,
            )
            if len(df_lb) == 0:
                continue

            count = 0
            for i in range(len(df_lb) - 1, -1, -1):
                if df_lb.iloc[i]["close"] == df_lb.iloc[i]["high_limit"]:
                    count += 1
                else:
                    break
            max_lianban = max(max_lianban, count)

    return zt_count, max_lianban


def get_big_face_count(date):
    """
    获取大面股数量（跌幅>7%）
    使用批量计算提高效率
    """
    prev_date = get_trade_days(end_date=date, count=2)[0]

    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks,
        end_date=prev_date,
        count=1,
        fields=["close"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()

    prev_prices = dict(zip(df["code"], df["close"]))

    df_curr = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close"],
        panel=False,
        fill_paused=False,
    )
    df_curr = df_curr.dropna()

    big_face_count = 0
    for idx, row in df_curr.iterrows():
        stock = row["code"]
        curr_close = row["close"]

        if stock not in prev_prices:
            continue

        prev_close = prev_prices[stock]

        if prev_close <= 0:
            continue

        decline_pct = (curr_close - prev_close) / prev_close * 100

        if decline_pct < -7:
            big_face_count += 1

    return big_face_count


def get_sentiment_switch_A(date):
    """
    A组：原始情绪开关（涨停家数+连板数）
    条件：涨停家数>=15 且 最高连板数>=2
    """
    zt_count, max_lianban = get_zt_count_and_lianban(date)

    return zt_count >= 15 and max_lianban >= 2


def get_sentiment_switch_B(date):
    """
    B组：新增大面股指标
    条件：涨停家数>=15 且 最高连板数>=2 且 大面股<50
    """
    zt_count, max_lianban = get_zt_count_and_lianban(date)
    big_face_count = get_big_face_count(date)

    return zt_count >= 15 and max_lianban >= 2 and big_face_count < 50


def get_first_board_signals(date):
    """
    获取首板低开信号（简化版）
    """
    prev_date = get_trade_days(end_date=date, count=2)[0]

    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df_prev = get_price(
        all_stocks,
        end_date=prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df_prev = df_prev.dropna()

    zt_stocks = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()

    if not zt_stocks:
        return []

    prev_prev_date = get_trade_days(end_date=prev_date, count=2)[0]
    df_prev_prev = get_price(
        zt_stocks,
        end_date=prev_prev_date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df_prev_prev = df_prev_prev.dropna()

    prev_zt = df_prev_prev[df_prev_prev["close"] == df_prev_prev["high_limit"]][
        "code"
    ].tolist()

    first_board = [s for s in zt_stocks if s not in prev_zt]

    if not first_board:
        return []

    signals = []

    for stock in first_board[:50]:
        df_curr = get_price(
            stock, end_date=date, count=2, fields=["open", "close"], panel=False
        )

        if len(df_curr) < 2:
            continue

        prev_close = df_curr.iloc[0]["close"]
        curr_open = df_curr.iloc[1]["open"]

        open_pct = (curr_open - prev_close) / prev_close * 100

        if not (-2.0 <= open_pct <= 1.5):
            continue

        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code == stock
        )
        df_cap = get_fundamentals(q, date)

        if df_cap.empty:
            continue

        market_cap = float(df_cap["circulating_market_cap"].iloc[0])

        if not (5 <= market_cap <= 15):
            continue

        signals.append(
            {
                "stock": stock,
                "date": date,
                "open_pct": open_pct,
                "buy_price": curr_open,
                "market_cap": market_cap,
            }
        )

    return signals


def calculate_signal_returns(signal, date):
    """
    计算信号次日收益
    """
    next_dates = get_trade_days(end_date=date, count=2)
    if len(next_dates) < 2:
        return None

    next_date = next_dates[1]

    df_next = get_price(
        signal["stock"],
        end_date=next_date,
        count=1,
        fields=["high", "close"],
        panel=False,
    )

    if df_next.empty:
        return None

    buy_price = signal["buy_price"]
    next_high = float(df_next["high"].iloc[0])
    next_close = float(df_next["close"].iloc[0])

    return_high = (next_high - buy_price) / buy_price * 100
    return_close = (next_close - buy_price) / buy_price * 100

    return {"return_high": return_high, "return_close": return_close}


print("\n开始测试...")
print("=" * 80)

trading_dates = get_trade_days(START_DATE, END_DATE)
print(f"交易日数量: {len(trading_dates)}")

group_A_signals = []
group_B_signals = []

sentiment_data = []

for i, date in enumerate(trading_dates):
    if i % 30 == 0:
        print(f"\n进度: {i}/{len(trading_dates)} ({date})")

    zt_count, max_lianban = get_zt_count_and_lianban(date)
    big_face_count = get_big_face_count(date)

    sentiment_data.append(
        {
            "date": date,
            "zt_count": zt_count,
            "max_lianban": max_lianban,
            "big_face_count": big_face_count,
        }
    )

    switch_A = get_sentiment_switch_A(date)
    switch_B = get_sentiment_switch_B(date)

    signals = get_first_board_signals(date)

    for signal in signals:
        returns = calculate_signal_returns(signal, date)
        if returns:
            signal.update(returns)

            if switch_A:
                group_A_signals.append(signal)

            if switch_B:
                group_B_signals.append(signal)

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)

print("\n情绪指标统计:")
df_sentiment = pd.DataFrame(sentiment_data)
print(f"  平均涨停家数: {df_sentiment['zt_count'].mean():.1f}")
print(f"  平均最高连板数: {df_sentiment['max_lianban'].mean():.1f}")
print(f"  平均大面股数量: {df_sentiment['big_face_count'].mean():.1f}")
print(f"  大面股数量分布:")
print(f"    最小值: {df_sentiment['big_face_count'].min()}")
print(f"    最大值: {df_sentiment['big_face_count'].max()}")
print(f"    中位数: {df_sentiment['big_face_count'].median()}")

print(f"\n大面股>=50的交易日: {(df_sentiment['big_face_count'] >= 50).sum()}天")
print(f"大面股<50的交易日: {(df_sentiment['big_face_count'] < 50).sum()}天")

print("\n" + "=" * 80)
print("A组 vs B组对比")
print("=" * 80)

if group_A_signals:
    df_A = pd.DataFrame(group_A_signals)

    print("\nA组统计（原始情绪开关）:")
    print(f"  信号数量: {len(df_A)}")
    print(f"  平均次日最高收益: {df_A['return_high'].mean():.2f}%")
    print(f"  平均次日收盘收益: {df_A['return_close'].mean():.2f}%")
    print(f"  次日最高胜率: {(df_A['return_high'] > 0).sum() / len(df_A) * 100:.1f}%")
    print(f"  次日收盘胜率: {(df_A['return_close'] > 0).sum() / len(df_A) * 100:.1f}%")
    print(
        f"  盈亏比（最高）: {abs(df_A[df_A['return_high'] > 0]['return_high'].sum() / abs(df_A[df_A['return_high'] < 0]['return_high'].sum())):.2f}"
    )

if group_B_signals:
    df_B = pd.DataFrame(group_B_signals)

    print("\nB组统计（新增大面股指标）:")
    print(f"  信号数量: {len(df_B)}")
    print(f"  平均次日最高收益: {df_B['return_high'].mean():.2f}%")
    print(f"  平均次日收盘收益: {df_B['return_close'].mean():.2f}%")
    print(f"  次日最高胜率: {(df_B['return_high'] > 0).sum() / len(df_B) * 100:.1f}%")
    print(f"  次日收盘胜率: {(df_B['return_close'] > 0).sum() / len(df_B) * 100:.1f}%")
    print(
        f"  盈亏比（最高）: {abs(df_B[df_B['return_high'] > 0]['return_high'].sum() / abs(df_B[df_B['return_high'] < 0]['return_high'].sum())):.2f}"
    )

if group_A_signals and group_B_signals:
    df_A = pd.DataFrame(group_A_signals)
    df_B = pd.DataFrame(group_B_signals)

    print("\n对比分析:")
    print(f"{'指标':<20} {'A组':<15} {'B组':<15} {'差异':<15}")
    print("-" * 60)

    metrics = [
        ("信号数量", len(df_A), len(df_B)),
        ("平均次日最高收益%", df_A["return_high"].mean(), df_B["return_high"].mean()),
        ("平均次日收盘收益%", df_A["return_close"].mean(), df_B["return_close"].mean()),
        (
            "次日最高胜率%",
            (df_A["return_high"] > 0).sum() / len(df_A) * 100,
            (df_B["return_high"] > 0).sum() / len(df_B) * 100,
        ),
        (
            "次日收盘胜率%",
            (df_A["return_close"] > 0).sum() / len(df_A) * 100,
            (df_B["return_close"] > 0).sum() / len(df_B) * 100,
        ),
    ]

    for name, val_A, val_B in metrics:
        diff = val_B - val_A
        print(f"{name:<20} {val_A:<15.2f} {val_B:<15.2f} {diff:<15.2f}")

    print("\n增益判定:")

    if len(df_B) < len(df_A) * 0.7:
        print("  ⚠️  B组信号数量显著减少（<70%），可能过度过滤")

    if df_B["return_high"].mean() > df_A["return_high"].mean():
        improvement_pct = (
            (df_B["return_high"].mean() - df_A["return_high"].mean())
            / df_A["return_high"].mean()
            * 100
        )
        print(f"  ✓ B组平均收益提升 {improvement_pct:.1f}%")
    else:
        decline_pct = (
            (df_A["return_high"].mean() - df_B["return_high"].mean())
            / df_A["return_high"].mean()
            * 100
        )
        print(f"  ✗ B组平均收益下降 {decline_pct:.1f}%")

    if (df_B["return_high"] > 0).sum() / len(df_B) > (
        df_A["return_high"] > 0
    ).sum() / len(df_A):
        print(f"  ✓ B组胜率提升")
    else:
        print(f"  ✗ B组胜率下降")

    print("\n最终判定:")

    if df_B["return_high"].mean() > df_A["return_high"].mean() * 1.1:
        print("  ** Go - 大面股指标有显著增益（收益提升>10%）**")
    elif df_B["return_high"].mean() > df_A["return_high"].mean():
        print("  ** Watch - 大面股指标有轻微增益，需进一步验证 **")
    else:
        print("  ** No-Go - 大面股指标无增益或负贡献 **")

print("\n" + "=" * 80)
print("测试结束")
print("=" * 80)
