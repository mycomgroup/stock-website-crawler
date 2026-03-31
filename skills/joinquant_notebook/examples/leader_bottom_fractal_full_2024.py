# 龙头底分型完整回测 - 2024-01-01后样本外验证
from jqdata import *
import pandas as pd

print("=" * 80)
print("龙头底分型样本外回测 (2024-01-01 ~ 2026-03-20)")
print("=" * 80)

START = "2024-01-01"
END = "2026-03-20"


def get_zt_stocks(date):
    stocks = get_all_securities("stock", date).index.tolist()
    stocks = [s for s in stocks if s[0:3] not in ["68", "4", "8"]]
    try:
        df = get_price(
            stocks,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()
        return list(df[df["close"] == df["high_limit"]]["code"])
    except:
        return []


def check_leader_pattern(stock, date):
    try:
        df_40 = get_price(
            stock,
            end_date=date,
            count=40,
            fields=["close", "high", "high_limit"],
            panel=False,
        )
        if len(df_40) < 40:
            return False

        high_40 = df_40["high"].max()
        current_close = df_40["close"].iloc[-1]

        if current_close < high_40 * 0.85:
            return False

        df_before = get_price(
            stock,
            end_date=date,
            count=12,
            fields=["close", "low", "high_limit"],
            panel=False,
        )
        if len(df_before) < 12:
            return False

        max_before = df_before["close"].max()
        min_before = df_before["close"].min()
        rate_before = (max_before - min_before) / min_before

        if rate_before < 0.50:
            return False

        limit_count = (df_before["close"] == df_before["high_limit"]).sum()
        if limit_count < 2:
            return False

        return True
    except:
        return False


def check_bottom_fractal(stock, date):
    try:
        df_3 = get_price(
            stock,
            end_date=date,
            count=3,
            fields=["open", "close", "high", "low", "high_limit"],
            panel=False,
        )
        if len(df_3) < 3:
            return False, False, False

        t0 = df_3.iloc[-1]
        t1 = df_3.iloc[-2]

        is_zt = t0["close"] == t0["high_limit"]

        body_ratio = abs(t1["close"] - t1["open"]) / ((t1["close"] + t1["open"]) / 2)
        is_cross = body_ratio < 0.03

        open_gap = t0["open"] / t1["close"] - 1
        is_high_open = open_gap > 0.015

        return is_zt, is_cross, is_high_open
    except:
        return False, False, False


trade_days = get_trade_days(start_date=START, end_date=END)
sample_days = trade_days[::2]
print(f"交易日总数: {len(trade_days)}, 采样天数: {len(sample_days)}")

signals = []

for i, date in enumerate(sample_days):
    ds = date.strftime("%Y-%m-%d")

    zt_list = get_zt_stocks(ds)[:30]

    for stock in zt_list:
        has_leader = check_leader_pattern(stock, ds)
        if not has_leader:
            continue

        is_zt, is_cross, is_high_open = check_bottom_fractal(stock, ds)

        if is_zt and is_cross and is_high_open:
            try:
                buy_price = get_price(
                    stock, end_date=ds, count=1, fields=["open"], panel=False
                )
                if len(buy_price) > 0:
                    signals.append(
                        {
                            "date": ds,
                            "stock": stock,
                            "buy_open": buy_price["open"].iloc[0],
                        }
                    )
                    print(
                        f"信号 #{len(signals)}: {ds} {stock} 开盘:{buy_price['open'].iloc[0]:.2f}"
                    )
            except:
                pass

    if (i + 1) % 50 == 0:
        print(f"进度: {i + 1}/{len(sample_days)}")

print("\n" + "=" * 80)
print(f"样本外信号总数: {len(signals)}")
print("=" * 80)

if len(signals) > 0:
    print("\n详细信号列表:")
    for i, sig in enumerate(signals, 1):
        print(f"{i}. {sig['date']} {sig['stock']} 开盘价:{sig['buy_open']:.2f}")

    if len(signals) < 10:
        print("\n判断: 样本太少 (<10次)")
        print("推荐: No-Go")
    elif len(signals) < 20:
        print("\n判断: 样本不足 (<20次)")
        print("推荐: Watch - 需要更多样本验证")
    else:
        print("\n判断: 样本充足 (>=20次)")
        print("推荐: 进一步验证收益率")
else:
    print("\n未发现信号")
    print("推荐: No-Go")

print("\n研究完成!")
