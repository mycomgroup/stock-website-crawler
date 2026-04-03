"""
首板低开选股 - BigQuant 版本
对应 JoinQuant: simple_first_board.py
数据来源：cn_stock_bar1d（含 upper_limit、lower_limit）
"""

import dai
import pandas as pd

PREV_DATE = "2024-01-02"  # 前一天（涨停日）
TODAY = "2024-01-03"  # 今天（开盘观察日）
CAP_MIN = 50e8  # 50亿（元）
CAP_MAX = 150e8  # 150亿（元）

print("=== 首板低开选股 ===")
print("涨停日:", PREV_DATE, "  观察日:", TODAY)

prev_df = dai.query(
    """
    SELECT instrument, close, upper_limit, lower_limit
    FROM cn_stock_bar1d
    WHERE date = '{date}'
      AND close >= upper_limit * 0.999
""".format(date=PREV_DATE)
).df()

print("前一天涨停股票数:", len(prev_df))
zt_stocks = prev_df["instrument"].tolist()

if not zt_stocks:
    print("没有涨停股票，退出")
else:
    inst_str = "','".join(zt_stocks[:200])
    today_df = dai.query(
        """
        SELECT b.instrument, b.open, b.upper_limit as today_upper,
               v.float_market_cap
        FROM cn_stock_bar1d b
        LEFT JOIN cn_stock_valuation v
          ON b.instrument = v.instrument AND b.date = v.date
        WHERE b.date = '{today}'
          AND b.instrument IN ('{insts}')
    """.format(today=TODAY, insts=inst_str)
    ).df()

    df = today_df.merge(
        prev_df[["instrument", "upper_limit"]].rename(
            columns={"upper_limit": "prev_upper"}
        ),
        on="instrument",
    )

    df["prev_close_approx"] = df["prev_upper"] / 1.1
    df["open_ratio"] = df["open"] / df["prev_close_approx"]

    qualified = df[
        (df["open_ratio"] >= 1.005)
        & (df["open_ratio"] <= 1.015)
        & (df["float_market_cap"] >= CAP_MIN)
        & (df["float_market_cap"] <= CAP_MAX)
    ]

    print("符合条件股票数:", len(qualified))
    if len(qualified) > 0:
        print(
            qualified[
                ["instrument", "open", "prev_upper", "open_ratio", "float_market_cap"]
            ].to_string()
        )
    else:
        print("当日无符合条件股票（正常，需要找有涨停的日期）")
        print("\n前一天涨停股票样本（前5只）:")
        print(prev_df.head().to_string())
