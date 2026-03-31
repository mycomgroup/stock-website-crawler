from jqdata import *

print("二板策略快速统计 - 2021年")

dates = list(get_trade_days(start_date="2021-01-01", end_date="2021-12-31"))
dates = [str(d) if hasattr(d, "strftime") else d for d in dates]
print(f"全年交易日: {len(dates)}")

zt_ok = 0
signals = 0
rets = []

for i in range(1, len(dates)):
    d = dates[i]
    try:
        stocks = get_all_securities("stock", d).index.tolist()
        stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]

        p = get_price(
            stocks, end_date=d, count=1, fields=["close", "high_limit"], panel=False
        )
        if p.empty:
            continue

        zt = p[abs(p["close"] - p["high_limit"]) / p["high_limit"] < 0.01]
        zt_count = len(zt)

        if zt_count >= 10:
            zt_ok += 1
            sig_day = int(zt_count * 0.3)
            signals += sig_day
            print(f"{d}: ZT={zt_count}, 估信号~{sig_day}")
    except:
        continue

print(f"\n统计:")
print(f"  情绪OK天数: {zt_ok}/{len(dates)}")
print(f"  估算年信号: ~{signals}")
print(f"  日均信号: {signals / len(dates):.1f}")

print("\n完成")
