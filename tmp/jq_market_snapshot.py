from jqdata import *
from datetime import datetime
import pandas as pd


def above_ma_ratio(stocks, end_date, ma_window=20):
    price = get_price(
        stocks,
        end_date=end_date,
        count=ma_window,
        fields=["close"],
        panel=False,
    )
    close = price.pivot(index="time", columns="code", values="close")
    ma = close.mean()
    latest = close.iloc[-1]
    ratio = (latest > ma).mean()
    return ratio, int((latest > ma).sum()), int(len(latest))


trade_day = get_trade_days(end_date=datetime.now().date(), count=1)[0]
trade_day_str = trade_day.strftime("%Y-%m-%d")

hs300 = get_index_stocks("000300.XSHG", date=trade_day)
zz500 = get_index_stocks("000905.XSHG", date=trade_day)

hs300_ratio, hs300_count, hs300_total = above_ma_ratio(hs300, trade_day_str)
zz500_ratio, zz500_count, zz500_total = above_ma_ratio(zz500, trade_day_str)

q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    valuation.market_cap,
).filter(valuation.code.in_(hs300))
fund = get_fundamentals(q, date=trade_day_str)
fund = fund[(fund["pe_ratio"] > 0) & (fund["pb_ratio"] > 0)]

print("market_trade_day", trade_day_str)
print("hs300_above_ma20_ratio", round(hs300_ratio, 4), hs300_count, hs300_total)
print("zz500_above_ma20_ratio", round(zz500_ratio, 4), zz500_count, zz500_total)
print("hs300_pe_median", round(float(fund["pe_ratio"].median()), 4))
print("hs300_pb_median", round(float(fund["pb_ratio"].median()), 4))
print("hs300_market_cap_median", round(float(fund["market_cap"].median()), 4))
