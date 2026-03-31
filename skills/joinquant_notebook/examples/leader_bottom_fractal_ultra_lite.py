# 龙头底分型 - 极简验证版本
# 只测试2024-2025年，每天只检查涨停股票的前5个

from jqdata import *
import pandas as pd

print("龙头底分型极简验证 (2024-2025)")
print("=" * 60)

START = "2024-01-01"
END = "2025-03-31"


def get_zt(date):
    stocks = get_all_securities("stock", date).index.tolist()
    stocks = [s for s in stocks if s[0:3] not in ["68", "4", "8"]]
    df = get_price(
        stocks, end_date=date, count=1, fields=["close", "high_limit"], panel=False
    )
    df = df.dropna()
    return list(df[df["close"] == df["high_limit"]]["code"])[:5]


def check_pattern(stock, date):
    try:
        df = get_price(
            stock, end_date=date, count=12, fields=["close", "high_limit"], panel=False
        )
        if len(df) < 12:
            return False

        max_c = df["close"].max()
        min_c = df["close"].min()
        rate = (max_c - min_c) / min_c

        if rate < 0.5:
            return False

        zt_cnt = (df["close"] == df["high_limit"]).sum()
        if zt_cnt < 2:
            return False

        df3 = get_price(
            stock,
            end_date=date,
            count=3,
            fields=["open", "close", "high_limit"],
            panel=False,
        )
        if len(df3) < 3:
            return False

        t0 = df3.iloc[-1]
        t1 = df3.iloc[-2]

        if t0["close"] != t0["high_limit"]:
            return False

        body = abs(t1["close"] - t1["open"]) / ((t1["close"] + t1["open"]) / 2)
        if body > 0.03:
            return False

        gap = t0["open"] / t1["close"] - 1
        if gap < 0.015:
            return False

        return True
    except:
        return False


days = get_trade_days(start_date=START, end_date=END)[::5]
print(f"采样天数: {len(days)}")

signals = []

for i, d in enumerate(days):
    ds = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else d

    zt_list = get_zt(ds)

    for s in zt_list:
        if check_pattern(s, ds):
            try:
                buy = get_price(s, end_date=ds, count=1, fields=["open"], panel=False)
                if len(buy) > 0:
                    signals.append({"date": ds, "stock": s, "buy": buy["open"].iloc[0]})
                    print(f"发现信号: {ds} {s}")
            except:
                pass

print("\n" + "=" * 60)
print(f"信号总数: {len(signals)}")

if len(signals) > 0:
    print("\n信号列表:")
    for sig in signals:
        print(f"{sig['date']} {sig['stock']} 开盘价:{sig['buy']:.2f}")

    if len(signals) < 10:
        print("\n结论: 样本太少 (<10)")
        rec = "No-Go"
    else:
        print("\n结论: 需要进一步验证收益")
        rec = "Watch"
else:
    print("\n未发现信号")
    rec = "No-Go"

print(f"\n推荐: {rec}")
