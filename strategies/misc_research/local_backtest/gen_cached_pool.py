"""
用已缓存的股票生成 pool_panel，跑通 strategy_kits pipeline
"""
import os, re
import pandas as pd
import akshare as ak

CACHE_DIR = "./data_cache"
START = "2021-01-01"
END   = "2026-01-01"
OUT   = "strategies/local_backtest/pool_panel_cached.csv"

# 从缓存文件名反推 JQ 格式代码
cached = [f for f in os.listdir(CACHE_DIR) if f.endswith("_daily_qfq.pkl")]
codes_jq = []
for f in cached:
    m = re.match(r"(sh|sz)(\d{6})_daily_qfq\.pkl", f)
    if m:
        prefix, num = m.group(1), m.group(2)
        suffix = "XSHG" if prefix == "sh" else "XSHE"
        codes_jq.append(f"{num}.{suffix}")

codes_jq.sort()
print(f"已缓存股票数: {len(codes_jq)}")

# 交易日历
cal = ak.tool_trade_date_hist_sina()
cal["trade_date"] = pd.to_datetime(cal["trade_date"])
dates = cal[
    (cal["trade_date"] >= START) & (cal["trade_date"] <= END)
]["trade_date"].sort_values()

weight = round(1.0 / len(codes_jq), 6)
rows = []
for d in dates:
    date_str = d.strftime("%Y-%m-%d")
    for i, code in enumerate(codes_jq):
        rows.append({"date": date_str, "code": code, "weight": weight, "score": weight, "rank": i + 1})

df = pd.DataFrame(rows)
df.to_csv(OUT, index=False)
print(f"已生成: {OUT}  ({len(df):,} 行, {len(codes_jq)} 只股票)")
