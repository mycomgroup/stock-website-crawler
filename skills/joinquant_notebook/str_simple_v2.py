"""
STR (Salience Theory Return) 因子验证
验证日期: 2023-06-30
"""

import pandas as pd
import numpy as np

print("=== STR因子验证开始 ===")

# 1. 获取股票池
hs300 = get_index_stocks("000300.XSHG")
zz500 = get_index_stocks("000905.XSHG")
all_stocks = list(set(hs300 + zz500))
print(f"原始股票数: {len(all_stocks)}")

# 2. 过滤ST
st_status = get_extras("is_st", all_stocks, end_date="2023-06-30", count=1).iloc[-1]
stocks = [s for s in all_stocks if not st_status.get(s, False)]
print(f"过滤ST后: {len(stocks)}")


# 3. 计算STR
def calc_str(stocks, date, lookback=22):
    start = (pd.Timestamp(date) - pd.Timedelta(days=lookback * 2)).strftime("%Y-%m-%d")
    end = date

    # 市场收益
    mkt = get_price("000300.XSHG", start_date=start, end_date=end, fields=["close"])
    mkt_ret = mkt["close"].pct_change().dropna()

    # 股票收益
    prices = get_price(
        stocks, start_date=start, end_date=end, fields=["close"], panel=False
    )

    results = {}
    for s in stocks:
        try:
            sp = prices[prices["code"] == s]["close"].dropna()
            sr = sp.pct_change().dropna()
            min_len = min(len(sr), len(mkt_ret))
            if min_len < 10:
                continue
            sret = sr.iloc[-min_len:].values
            mret = mkt_ret.iloc[-min_len:].values
            dev = np.abs(sret - mret)
            tot = np.sum(dev)
            if tot < 1e-10:
                continue
            results[s] = np.sum(sret * dev) / tot
        except:
            continue
    return results


str_vals = calc_str(stocks, "2023-06-30", 22)
print(f"STR计算成功: {len(str_vals)}只股票")

# 4. 获取次月收益
start_p = get_price(
    list(str_vals.keys()),
    start_date="2023-06-30",
    end_date="2023-06-30",
    fields=["close"],
    panel=False,
)
end_p = get_price(
    list(str_vals.keys()),
    start_date="2023-07-31",
    end_date="2023-07-31",
    fields=["close"],
    panel=False,
)

rets = {}
for s in str_vals.keys():
    try:
        p0 = start_p[start_p["code"] == s]["close"].values[0]
        p1 = end_p[end_p["code"] == s]["close"].values[0]
        rets[s] = (p1 - p0) / p0
    except:
        continue
print(f"收益计算成功: {len(rets)}只股票")

# 5. 分组测试
sorted_str = sorted(str_vals.items(), key=lambda x: x[1])
n = len(sorted_str)
g = n // 5

print("\n=== STR分组测试 ===")
print(f"{'组别':<12} {'平均收益':>10} {'股票数':>8}")
for i in range(5):
    idx = 4 - i  # 反过来显示，STR最低的在前
    start_i = idx * g
    end_i = (idx + 1) * g if idx < 4 else n
    grp = [s[0] for s in sorted_str[start_i:end_i]]
    grp_rets = [rets.get(s, 0) for s in grp]
    avg_r = np.mean(grp_rets)
    print(
        f"Q{idx + 1}(STR{'低' if idx == 4 else '高'}): {avg_r * 100:>9.2f}% {len(grp_rets):>8}"
    )

# 6. 多空组合
low_str_rets = [rets.get(s[0], 0) for s in sorted_str[-100:]]  # STR最低100只
high_str_rets = [rets.get(s[0], 0) for s in sorted_str[:100]]  # STR最高100只
spread = np.mean(low_str_rets) - np.mean(high_str_rets)
print(f"\n多空组合收益: {spread * 100:.2f}%")

# 7. IC
valid = [(str_vals[s], rets[s]) for s in str_vals.keys() if s in rets]
if len(valid) > 10:
    ic = np.corrcoef([x[0] for x in valid], [x[1] for x in valid])[0, 1]
    print(f"IC相关系数: {ic:.4f}")
    print(f"预期IC<0: {'✓' if ic < 0 else '✗'}")
