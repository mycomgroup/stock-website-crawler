from jqdata import *
import pandas as pd

print("=" * 60)
print("RFScore7 PB10 策略验证 - 简化版")
print("=" * 60)

test_date = "2024-06-01"
print(f"\n测试日期: {test_date}")

try:
    hs300 = get_index_stocks("000300.XSHG", date=test_date)[:50]
    print(f"测试股票数: {len(hs300)}")

    print("\n获取估值数据...")
    val = get_valuation(
        hs300, end_date=test_date, fields=["pb_ratio", "pe_ratio"], count=1
    )
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
    val = val[(val["pb_ratio"] > 0) & (val["pe_ratio"] < 100)]
    print(f"有效估值数据: {len(val)}")

    print("\n获取财务数据...")
    q = query(
        indicator.code, indicator.roa, indicator.roe, indicator.net_profit_margin
    ).filter(indicator.code.in_(val.index.tolist()))
    fin = get_fundamentals(q, date=test_date)
    fin = fin.set_index("code")
    print(f"有效财务数据: {len(fin)}")

    df = val.join(fin, how="inner").dropna()
    df = df[df["roa"] > 0.5]
    print(f"ROA>0.5筛选后: {len(df)}")

    df["pb_group"] = (
        pd.qcut(df["pb_ratio"].rank(method="first"), 5, labels=False, duplicates="drop")
        + 1
    )
    primary = df[df["pb_group"] == 1].sort_values("roa", ascending=False)

    print(f"\n选出股票 ({len(primary)}只):")
    for i, (code, row) in enumerate(primary.head(10).iterrows()):
        name = get_security_info(code).display_name
        print(
            f"  {i + 1}. {code} {name[:10]:10s} ROA={row['roa']:.2f} ROE={row['roe']:.2f} PB={row['pb_ratio']:.2f}"
        )

    print("\n验证成功！策略逻辑可行。")

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 60)
