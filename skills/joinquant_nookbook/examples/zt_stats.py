from jqdata import *

print("2021-2023年涨停家数统计")

for year in [2021, 2022, 2023]:
    print(f"\n{year}年:")

    # 统计每个月的涨停家数
    for month in [1, 4, 7, 10]:
        dates = get_trade_days(f"{year}-{month:02d}-01", f"{year}-{month:02d}-10")

        zt_counts = []
        for d in dates[:5]:
            stocks = [
                s
                for s in get_all_securities("stock", d).index
                if not s.startswith(("68", "4", "8"))
            ][:200]

            df = get_price(
                stocks, end_date=d, count=1, fields=["close", "high_limit"], panel=False
            )
            df = df.dropna()
            zt = len(df[df["close"] == df["high_limit"]])
            zt_counts.append(zt)

        avg = sum(zt_counts) / len(zt_counts) if zt_counts else 0
        print(f"  {month}月: 涨停{zt_counts}, 平均{avg:.1f}")

print("\n完成")
