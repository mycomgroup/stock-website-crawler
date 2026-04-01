#!/usr/bin/env python3
"""
任务07：情绪指标阈值搜索 - 极简版
参考 test_mini.py 成功案例
只测试阈值30和50，快速验证
"""

from jqdata import *

print("=" * 80)
print("任务07：情绪指标阈值搜索（极简版）")
print("=" * 80)

START_DATE = "2024-01-01"
END_DATE = "2025-03-30"

thresholds = [0, 30, 50]

print(f"\n测试阈值: {thresholds}")
print(f"测试期间: {START_DATE} ~ {END_DATE}")


def get_zt_count(date):
    """获取涨停家数"""
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
    return len(df[df["close"] == df["high_limit"]])


def test_threshold(threshold, test_days):
    """测试单个阈值"""
    signals = 0
    trades = 0
    profits = []

    for d in test_days:
        ds = d.strftime("%Y-%m-%d")

        zt_count = get_zt_count(ds)

        if threshold > 0 and zt_count < threshold:
            continue

        signals += 1

        prev_zt = []
        all_stocks = get_all_securities("stock", ds).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        df = get_price(
            all_stocks,
            end_date=ds,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        prev_zt = list(df[df["close"] == df["high_limit"]]["code"])[:3]

        if len(prev_zt) > 0:
            stock = prev_zt[0]
            try:
                price_df = get_price(
                    stock, end_date=ds, count=1, fields=["open", "close"]
                )
                if len(price_df) > 0:
                    open_p = price_df.iloc[0]["open"]
                    close_p = price_df.iloc[0]["close"]
                    ret = (close_p / open_p - 1) * 100
                    profits.append(ret)
                    trades += 1
            except:
                pass

    if trades == 0:
        return None

    avg_ret = sum(profits) / len(profits)
    win_rate = len([p for p in profits if p > 0]) / len(profits) * 100

    return {
        "threshold": threshold,
        "signals": signals,
        "trades": trades,
        "avg_return": round(avg_ret, 3),
        "win_rate": round(win_rate, 2),
    }


print("\n获取交易日...")
days = get_trade_days(START_DATE, END_DATE)
sample_days = days[-20:]

print(f"采样天数: {len(sample_days)}")

results = []

print("\n" + "=" * 80)
print("阈值测试")
print("=" * 80)

for t in thresholds:
    print(f"\n阈值 {t}...")
    r = test_threshold(t, sample_days)
    if r:
        results.append(r)
        print(f"  信号数: {r['signals']}")
        print(f"  交易数: {r['trades']}")
        print(f"  平均收益: {r['avg_return']}%")
        print(f"  胜率: {r['win_rate']}%")

print("\n" + "=" * 80)
print("结果汇总")
print("=" * 80)

for r in results:
    print(
        f"\n阈值{r['threshold']}: 信号{r['signals']}, 收益{r['avg_return']}%, 胜率{r['win_rate']}%"
    )

print("\n测试完成！")
