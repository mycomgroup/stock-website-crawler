from jqdata import *
from datetime import datetime
import pandas as pd
import numpy as np


trade_day = get_trade_days(end_date=datetime.now().date(), count=1)[0]
trade_day_str = str(trade_day)

index_pool = set(get_index_stocks("000902.XSHG", date=trade_day))
industries = get_industries(name="sw_l1")

rows = []
for ind_code, row in industries.iterrows():
    stocks = [s for s in get_industry_stocks(ind_code, date=trade_day) if s in index_pool]
    stocks = [s for s in stocks if not s.startswith("688")]
    if len(stocks) < 5:
        continue
    try:
        px20 = get_price(stocks, end_date=trade_day_str, count=21, fields=["close"], panel=False)
        close20 = px20.pivot(index="time", columns="code", values="close")
        if len(close20) < 21:
            continue
        ma20 = close20.iloc[-20:].mean()
        last = close20.iloc[-1]
        breadth20 = float((last > ma20).mean())
        ret20 = (close20.iloc[-1] / close20.iloc[-21] - 1).dropna()

        px60 = get_price(stocks, end_date=trade_day_str, count=61, fields=["close"], panel=False)
        close60 = px60.pivot(index="time", columns="code", values="close")
        if len(close60) < 61:
            ret60_med = np.nan
        else:
            ret60_med = float((close60.iloc[-1] / close60.iloc[-61] - 1).median())

        rows.append({
            "industry_code": ind_code,
            "industry_name": row["name"],
            "stock_count": len(stocks),
            "breadth20": round(breadth20, 4),
            "ret20_median": round(float(ret20.median()), 4),
            "ret60_median": round(ret60_med, 4) if not pd.isna(ret60_med) else None,
        })
    except Exception:
        continue


df = pd.DataFrame(rows)
df["composite"] = (
    df["breadth20"].rank(pct=True)
    + df["ret20_median"].rank(pct=True)
    + df["ret60_median"].fillna(df["ret60_median"].median()).rank(pct=True)
) / 3
df = df.sort_values("composite", ascending=False)

print("trade_day", trade_day_str)
print("\nTOP_INDUSTRIES")
print(df.head(12)[["industry_name", "stock_count", "breadth20", "ret20_median", "ret60_median", "composite"]].to_string(index=False))

print("\nBOTTOM_INDUSTRIES")
print(df.tail(12)[["industry_name", "stock_count", "breadth20", "ret20_median", "ret60_median", "composite"]].to_string(index=False))
