# 龙头底分型 - 分段测试 2024年上半年
from jqdata import *

print("龙头底分型分段测试 (2024-01-01 ~ 2024-06-30)")
print("=" * 70)

START = "2024-01-01"
END = "2024-06-30"


def get_zt(date):
    stocks = get_all_securities("stock", date).index.tolist()
    stocks = [s for s in stocks if s[0:3] not in ["68", "4", "8"]]
    try:
        df = get_price(
            stocks, end_date=date, count=1, fields=["close", "high_limit"], panel=False
        )
        df = df.dropna()
        return list(df[df["close"] == df["high_limit"]]["code"])[:20]
    except:
        return []


def check_signal(s, ds):
    try:
        df12 = get_price(
            s, end_date=ds, count=12, fields=["close", "high_limit"], panel=False
        )
        if len(df12) < 12:
            return False

        max_c = df12["close"].max()
        min_c = df12["close"].min()
        rate = (max_c - min_c) / min_c

        if rate < 0.50:
            return False

        zt_cnt = (df12["close"] == df12["high_limit"]).sum()
        if zt_cnt < 2:
            return False

        df3 = get_price(
            s, end_date=ds, count=3, fields=["open", "close", "high_limit"], panel=False
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


days = get_trade_days(START, END)[::2]
print(f"采样天数: {len(days)}")

signals = []

for i, d in enumerate(days):
    ds = d.strftime("%Y-%m-%d")
    zt_list = get_zt(ds)

    for s in zt_list:
        if check_signal(s, ds):
            signals.append({"date": ds, "stock": s})
            print(f"发现: {ds} {s}")

    if (i + 1) % 20 == 0:
        print(f"进度: {i + 1}/{len(days)}")

print("\n" + "=" * 70)
print(f"2024上半年信号数: {len(signals)}")

if len(signals) > 0:
    for sig in signals:
        print(f"{sig['date']} {sig['stock']}")

    print(f"\n判断: 发现{len(signals)}个信号")
else:
    print("\n未发现信号")

print(f"\n预计全年信号数: {len(signals) * 2} (推测)")
print("研究完成!")
