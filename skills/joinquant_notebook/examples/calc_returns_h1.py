# 计算信号收益 - 2024年上半年
from jqdata import *
import pandas as pd

print("计算信号收益 (2024-01-01 ~ 2024-06-30)")
print("=" * 70)

signals = [
    ("2024-01-10", "002403.XSHE"),
    ("2024-01-12", "000017.XSHE"),
    ("2024-01-16", "002868.XSHE"),
    ("2024-01-18", "000017.XSHE"),
    ("2024-01-26", "000068.XSHE"),
    ("2024-01-26", "000070.XSHE"),
    ("2024-01-30", "002116.XSHE"),
    ("2024-01-30", "600088.XSHG"),
    ("2024-01-30", "600119.XSHG"),
    ("2024-02-05", "002325.XSHE"),
    ("2024-02-23", "000815.XSHE"),
    ("2024-02-29", "000586.XSHE"),
    ("2024-03-04", "000628.XSHE"),
    ("2024-03-04", "002313.XSHE"),
    ("2024-04-11", "001376.XSHE"),
    ("2024-04-19", "000099.XSHE"),
    ("2024-04-25", "000691.XSHE"),
    ("2024-04-25", "002231.XSHE"),
    ("2024-05-16", "000656.XSHE"),
    ("2024-05-20", "000560.XSHE"),
    ("2024-05-22", "000560.XSHE"),
    ("2024-05-22", "001267.XSHE"),
    ("2024-05-24", "000620.XSHE"),
    ("2024-06-12", "000793.XSHE"),
    ("2024-06-14", "000793.XSHE"),
    ("2024-06-18", "002199.XSHE"),
    ("2024-06-24", "000609.XSHE"),
]

trade_days = get_trade_days("2024-01-01", "2024-06-30")

results = []

for date_str, stock in signals[:15]:
    try:
        day_idx = list(trade_days).index(pd.Timestamp(date_str))

        buy_price = get_price(
            stock, end_date=date_str, count=1, fields=["open"], panel=False
        )

        if day_idx + 1 < len(trade_days):
            sell_date_1d = trade_days[day_idx + 1].strftime("%Y-%m-%d")
            sell_price_1d = get_price(
                stock, end_date=sell_date_1d, count=1, fields=["close"], panel=False
            )
        else:
            sell_price_1d = None

        if day_idx + 3 < len(trade_days):
            sell_date_3d = trade_days[day_idx + 3].strftime("%Y-%m-%d")
            sell_price_3d = get_price(
                stock, end_date=sell_date_3d, count=1, fields=["close"], panel=False
            )
        else:
            sell_price_3d = None

        if day_idx + 5 < len(trade_days):
            sell_date_5d = trade_days[day_idx + 5].strftime("%Y-%m-%d")
            sell_price_5d = get_price(
                stock, end_date=sell_date_5d, count=1, fields=["close"], panel=False
            )
        else:
            sell_price_5d = None

        if len(buy_price) > 0:
            buy_p = buy_price["open"].iloc[0]

            ret_1d = (
                (sell_price_1d["close"].iloc[0] / buy_p - 1) * 100
                if sell_price_1d is not None and len(sell_price_1d) > 0
                else None
            )
            ret_3d = (
                (sell_price_3d["close"].iloc[0] / buy_p - 1) * 100
                if sell_price_3d is not None and len(sell_price_3d) > 0
                else None
            )
            ret_5d = (
                (sell_price_5d["close"].iloc[0] / buy_p - 1) * 100
                if sell_price_5d is not None and len(sell_price_5d) > 0
                else None
            )

            results.append(
                {
                    "date": date_str,
                    "stock": stock,
                    "ret_1d": ret_1d,
                    "ret_3d": ret_3d,
                    "ret_5d": ret_5d,
                }
            )

            print(
                f"{date_str} {stock}: 1天={ret_1d:.2f}%, 3天={ret_3d:.2f}%, 5天={ret_5d:.2f}%"
            )
    except Exception as e:
        print(f"{date_str} {stock}: 错误 - {str(e)[:30]}")

df = pd.DataFrame(results)

print("\n" + "=" * 70)
print("统计结果:")
print(f"信号数: {len(df)}")

if len(df) > 0:
    print("\n持有1天:")
    valid_1d = df[df["ret_1d"].notna()]
    if len(valid_1d) > 0:
        print(f"  胜率: {(valid_1d['ret_1d'] > 0).sum() / len(valid_1d) * 100:.1f}%")
        print(f"  平均收益: {valid_1d['ret_1d'].mean():.2f}%")

    print("\n持有3天:")
    valid_3d = df[df["ret_3d"].notna()]
    if len(valid_3d) > 0:
        print(f"  胜率: {(valid_3d['ret_3d'] > 0).sum() / len(valid_3d) * 100:.1f}%")
        print(f"  平均收益: {valid_3d['ret_3d'].mean():.2f}%")

    print("\n持有5天:")
    valid_5d = df[df["ret_5d"].notna()]
    if len(valid_5d) > 0:
        print(f"  胜率: {(valid_5d['ret_5d'] > 0).sum() / len(valid_5d) * 100:.1f}%")
        print(f"  平均收益: {valid_5d['ret_5d'].mean():.2f}%")

print("\n研究完成!")
