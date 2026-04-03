"""
STR因子多月份验证
测试2022-2024年多个月份的IC表现
"""

import pandas as pd
import numpy as np

print("=== STR因子多月份验证 ===")


def calc_str(stocks, date, lookback=22):
    start = (pd.Timestamp(date) - pd.Timedelta(days=lookback * 2)).strftime("%Y-%m-%d")
    end = date
    mkt = get_price("000300.XSHG", start_date=start, end_date=end, fields=["close"])
    mkt_ret = mkt["close"].pct_change().dropna()
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


# 测试月份
test_months = [
    "2022-01-31",
    "2022-04-30",
    "2022-07-31",
    "2022-10-31",
    "2023-01-31",
    "2023-04-30",
    "2023-07-31",
    "2023-10-31",
    "2024-01-31",
    "2024-04-30",
    "2024-07-31",
    "2024-10-31",
]

results = []

for test_date in test_months:
    try:
        # 股票池
        hs300 = get_index_stocks("000300.XSHG")
        zz500 = get_index_stocks("000905.XSHG")
        all_stocks = list(set(hs300 + zz500))

        # 计算STR
        str_vals = calc_str(all_stocks, test_date, 22)
        if len(str_vals) < 100:
            continue

        # 下月收益
        next_end = (pd.Timestamp(test_date) + pd.offsets.MonthEnd(1)).strftime(
            "%Y-%m-%d"
        )
        start_p = get_price(
            list(str_vals.keys()),
            start_date=test_date,
            end_date=test_date,
            fields=["close"],
            panel=False,
        )
        end_p = get_price(
            list(str_vals.keys()),
            start_date=next_end,
            end_date=next_end,
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

        # IC
        valid = [(str_vals[s], rets[s]) for s in str_vals.keys() if s in rets]
        if len(valid) < 50:
            continue
        ic = np.corrcoef([x[0] for x in valid], [x[1] for x in valid])[0, 1]

        # 分组收益
        sorted_str = sorted(str_vals.items(), key=lambda x: x[1])
        n = len(sorted_str)
        low_ret = np.mean([rets.get(s[0], 0) for s in sorted_str[: n // 5]])
        high_ret = np.mean([rets.get(s[0], 0) for s in sorted_str[-n // 5 :]])

        results.append(
            {
                "date": test_date,
                "ic": ic,
                "low_str_return": low_ret,
                "high_str_return": high_ret,
                "spread": low_ret - high_ret,
                "n": len(valid),
            }
        )
        print(
            f"{test_date}: IC={ic:.3f}, 多空spread={spread * 100:.1f}%, n={len(valid)}"
        )
    except Exception as e:
        print(f"{test_date}: Error - {e}")
        continue

# 汇总
print("\n=== 汇总结果 ===")
if len(results) > 0:
    df = pd.DataFrame(results)
    ic_mean = df["ic"].mean()
    spread_mean = df["spread"].mean() * 100
    ic_positive = (df["ic"] < 0).mean()  # IC为负的比例

    print(f"平均IC: {ic_mean:.4f}")
    print(f"IC<0占比: {ic_positive * 100:.1f}%")
    print(f"平均多空spread: {spread_mean:.2f}%")
    print(f"\n结论: STR因子IC{'显著为负' if ic_mean < -0.05 else '不显著'}")

print("\n=== 验证完成 ===")
