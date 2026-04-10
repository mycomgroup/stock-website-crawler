"""
预下载沪深300行情到本地缓存，带重试
用法：python strategies/local_backtest/prefetch_data.py
"""
import time
import pandas as pd
import akshare as ak
import os, pickle

CACHE_DIR = "./data_cache"
START = "20210101"
END   = "20260101"
os.makedirs(CACHE_DIR, exist_ok=True)

# 读取 pool_panel 里的股票列表
df = pd.read_csv("strategies/local_backtest/pool_panel.csv", usecols=["code"])
codes_jq = df["code"].unique().tolist()

def jq_to_6digit(code: str) -> str:
    return code.split(".")[0]

def download_one(code6: str, retries=3) -> bool:
    cache_file = os.path.join(CACHE_DIR, f"sh{code6}_daily_qfq.pkl" if code6.startswith("6") else f"sz{code6}_daily_qfq.pkl")
    if os.path.exists(cache_file):
        return True  # 已缓存
    for attempt in range(retries):
        try:
            df = ak.stock_zh_a_hist(
                symbol=code6,
                period="daily",
                start_date=START,
                end_date=END,
                adjust="qfq",
                timeout=10,  # 10秒超时，不卡死
            )
            if df.empty:
                print(f"  [EMPTY] {code6}", flush=True)
                return False
            df["date"] = pd.to_datetime(df["日期"])
            df.to_pickle(cache_file)
            return True
        except Exception as e:
            wait = 1  # 固定等1秒，不用指数退避
            print(f"  [RETRY {attempt+1}/{retries}] {code6}: {type(e).__name__} — wait {wait}s", flush=True)
            time.sleep(wait)
    print(f"  [FAIL] {code6}", flush=True)
    return False

ok, fail = 0, 0
for i, jq_code in enumerate(codes_jq):
    code6 = jq_to_6digit(jq_code)
    success = download_one(code6)
    if success:
        ok += 1
    else:
        fail += 1
    if (i + 1) % 10 == 0:
        print(f"进度: {i+1}/{len(codes_jq)}  ok={ok} fail={fail}", flush=True)
    time.sleep(0.2)  # 限速，避免被封

print(f"\n完成: ok={ok}, fail={fail}")
