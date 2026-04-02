from jqdata import *
import pandas as pd

print("主线策略放宽版测试")
print("=" * 60)

test_dates = ["2024-06-17", "2024-06-18", "2024-06-19", "2024-06-20", "2024-06-21"]

trades = []

for i in range(1, len(test_dates)):
    prev_date = test_dates[i - 1]
    curr_date = test_dates[i]

    print(f"\n{curr_date}:")

    all_stocks = get_all_securities("stock", prev_date).index.tolist()[:500]

    limit_up = []
    for stock in all_stocks:
        try:
            p = get_price(
                stock,
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )
            if not p.empty:
                c = float(p["close"].iloc[0])
                h = float(p["high_limit"].iloc[0])
                if abs(c - h) / h < 0.01:
                    limit_up.append(stock)
        except:
            pass

    print(f"  涨停: {len(limit_up)}只")

    for stock in limit_up:
        try:
            p = get_price(
                stock,
                end_date=curr_date,
                count=1,
                fields=["open", "close", "high", "low"],
                panel=False,
            )
            if p.empty:
                continue

            v = get_fundamentals(
                query(valuation.circulating_market_cap).filter(valuation.code == stock),
                date=curr_date,
            )
            if v.empty:
                continue

            mc = float(v["circulating_market_cap"].iloc[0])

            # 放宽市值：20-200亿
            if not (20 <= mc <= 200):
                continue

            p_prev = get_price(
                stock, end_date=prev_date, count=1, fields=["close"], panel=False
            )
            if p_prev.empty:
                continue

            pre_c = float(p_prev["close"].iloc[0])
            op = float(p["open"].iloc[0])
            cl = float(p["close"].iloc[0])
            hi = float(p["high"].iloc[0])
            lo = float(p["low"].iloc[0])

            op_pct = (op - pre_c) / pre_c * 100

            if op == hi or op == lo:
                continue

            # 放宽开盘：-1%~+3%
            if -1 <= op_pct <= 3:
                ret = (cl - op) / op * 100
                trades.append(
                    {
                        "stock": stock,
                        "open_pct": op_pct,
                        "market_cap": mc,
                        "return": ret,
                    }
                )
                print(f"  ✓ {stock}: 开盘{op_pct:.2f}%, 市值{mc:.0f}亿, 收益{ret:.2f}%")
        except:
            pass

print("\n" + "=" * 60)
if trades:
    df = pd.DataFrame(trades)
    print(f"交易数: {len(df)}")
    print(f"平均收益: {df['return'].mean():.2f}%")
    print(f"胜率: {(df['return'] > 0).sum() / len(df) * 100:.0f}%")
    print(f"平均市值: {df['market_cap'].mean():.0f}亿")
else:
    print("无交易")

print("\n完成！")
