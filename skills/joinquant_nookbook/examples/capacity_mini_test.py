from jqdata import *
import pandas as pd

print("=" * 50)
print("首板低开策略 - 滑点影响快速验证")
print("=" * 50)

TEST_DATE = "2024-10-15"
SLIPPAGES = [0, 0.002, 0.005]
SLIPPAGE_NAMES = ["0%", "0.2%", "0.5%"]

COMMISSION = 0.0003
STAMP = 0.001

prev_date = "2024-10-14"

all_stocks = get_all_securities("stock", prev_date).index.tolist()
all_stocks = [s for s in all_stocks if s[0] not in "683"]

print(f"获取{prev_date}涨停股...")
df_prev = get_price(
    all_stocks[:300],
    end_date=prev_date,
    frequency="daily",
    fields=["close", "high_limit"],
    count=1,
    panel=False,
)

df_prev = df_prev.dropna()
limit_up = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()

print(f"涨停股数量: {len(limit_up)}")

if len(limit_up) == 0:
    print("无涨停股，测试终止")
else:
    print(f"\n获取{TEST_DATE}开盘数据...")
    df_today = get_price(
        limit_up[:30],
        end_date=TEST_DATE,
        frequency="daily",
        fields=["open", "close", "high_limit"],
        count=1,
        panel=False,
    )

    df_today = df_today.dropna()
    df_today["ratio"] = df_today["open"] / (df_today["high_limit"] / 1.1)

    signals = df_today[(df_today["ratio"] > 1.005) & (df_today["ratio"] < 1.015)]

    if len(signals) == 0:
        print("无符合条件的信号")
    else:
        print(f"\n信号数量: {len(signals)}")

        buy_price = signals["open"].mean()
        sell_price = signals["close"].mean()

        print(f"平均买入价: {buy_price:.2f}")
        print(f"平均卖出价: {sell_price:.2f}")

        print(f"\n不同滑点下的收益:")
        print("-" * 50)

        for slip_idx, slippage in enumerate(SLIPPAGES):
            slip_name = SLIPPAGE_NAMES[slip_idx]

            buy_cost = buy_price * (1 + slippage + COMMISSION)
            sell_income = sell_price * (1 - slippage - COMMISSION - STAMP)

            pnl_pct = (sell_income - buy_cost) / buy_cost * 100

            print(f"{slip_name}滑点: 收益 {pnl_pct:.2f}%")

        print("-" * 50)
        print(f"\n结论:")
        print("- 0%滑点（理论）: 基准收益")
        print("- 0.2%滑点: 收益衰减约0.4-0.5%")
        print("- 0.5%滑点: 收益衰减约1.0-1.2%，可能转负")
        print("=" * 50)
