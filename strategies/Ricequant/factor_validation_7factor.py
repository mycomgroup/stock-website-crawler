# -*- coding: utf-8 -*-
"""
7因子短名单 — RiceQuant 可计算性验证
"""

print("=" * 70)
print("7因子短名单 — RiceQuant 可计算性验证")
print("=" * 70)

import pandas as pd
import numpy as np

BASELINE_OK = False
PRICE_OK = False
STR_OK = False
AMP_OK = False
MOM_OK = False
price_data = {}
ohlc_data = {}
str_series = pd.Series(dtype=float)
amp_series = pd.Series(dtype=float)
mom_series = pd.Series(dtype=float)
factors = None

START_DATE = "2024-01-01"
END_DATE = "2024-12-31"
INDEX = "000905.XSHG"
LOOKBACK = 22

print(f"\n股票池: {INDEX}")
print(f"时间范围: {START_DATE} ~ {END_DATE}")
print(f"回望期: {LOOKBACK} 交易日")

print("\n[1/5] 获取股票池...")
stocks = index_components(INDEX, START_DATE)
print(f"  成分股数量: {len(stocks)}")

valid_stocks = []
for s in stocks:
    info = instruments(s)
    if info and info.listed_date:
        listed = (
            pd.Timestamp(info.listed_date)
            if isinstance(info.listed_date, str)
            else info.listed_date
        )
        days_listed = (pd.Timestamp(START_DATE) - listed).days
        if days_listed > 180:
            valid_stocks.append(s)

print(f"  过滤后数量: {len(valid_stocks)}")
test_stocks = valid_stocks[:50]
print(f"  测试数量: {len(test_stocks)}")

print("\n[2/5] 验证基线因子...")
try:
    factors = get_factor(
        test_stocks,
        ["pe_ratio", "pb_ratio", "roe", "roa"],
        start_date=START_DATE,
        end_date=END_DATE,
    )
    print(f"  OK 基线因子获取成功, 形状: {factors.shape}")
    # get_factor returns MultiIndex: (order_book_id, date)
    ld = factors.index.get_level_values(1).max()
    lt = factors.xs(ld, level=1)
    print(f"  最新日期: {ld}")
    for col in ["pe_ratio", "pb_ratio", "roe", "roa"]:
        if col in lt.columns:
            s = lt[col].dropna()
            if len(s) > 0:
                print(f"    {col}: mean={s.mean():.4f}, count={len(s)}")
    BASELINE_OK = True
except Exception as e:
    print(f"  FAIL: {e}")

print("\n[3/5] 获取价格数据...")
try:
    price_df = get_price(
        test_stocks,
        start_date=START_DATE,
        end_date=END_DATE,
        frequency="1d",
        fields=["close", "high", "low", "open"],
    )
    print(f"  OK 价格数据获取成功, 形状: {price_df.shape}")
    print(f"  Index names: {price_df.index.names}")

    # MultiIndex: level 0 = order_book_id, level 1 = date
    for stock in test_stocks:
        try:
            sd = price_df.xs(stock, level="order_book_id")
            closes = sd["close"].dropna().values
            if len(closes) >= LOOKBACK:
                price_data[stock] = closes
            if all(f in sd.columns for f in ["open", "high", "low", "close"]):
                ohlc = sd[["open", "high", "low", "close"]].dropna()
                if len(ohlc) >= LOOKBACK:
                    ohlc_data[stock] = ohlc
        except:
            continue
    print(f"  有效收盘价: {len(price_data)}, 有效OHLC: {len(ohlc_data)}")
    if len(price_data) > 0:
        PRICE_OK = True
except Exception as e:
    print(f"  FAIL: {e}")
    import traceback

    traceback.print_exc()

if PRICE_OK:
    print("\n[4/5] 计算新因子...")

    # Get market returns
    try:
        mkt_df = get_price(
            "000300.XSHG",
            start_date=START_DATE,
            end_date=END_DATE,
            frequency="1d",
            fields=["close"],
        )
        mkt_closes = (
            mkt_df.xs("000300.XSHG", level="order_book_id")["close"].dropna().values
        )
        mkt_returns = np.diff(mkt_closes) / mkt_closes[:-1]
        mkt_returns = mkt_returns[-LOOKBACK:]
        print(f"  市场收益率: {len(mkt_returns)} 天")
    except Exception as e:
        print(f"  市场数据获取失败: {e}")
        mkt_returns = np.zeros(LOOKBACK)

    print("\n  [5.1] STR 因子...")
    try:
        str_values = {}
        for stock in test_stocks:
            if stock not in price_data:
                continue
            closes = price_data[stock][-LOOKBACK - 1 :]
            ret = np.diff(closes) / closes[:-1]
            ret = ret[-LOOKBACK:]
            if len(ret) < 10:
                continue
            ml = min(len(ret), len(mkt_returns))
            ret, mkt_ret = ret[-ml:], mkt_returns[-ml:]
            theta = 0.001
            salience = np.abs(ret - mkt_ret) / (np.abs(ret) + np.abs(mkt_ret) + theta)
            ranks = np.argsort(np.argsort(-salience)) + 1
            delta = 0.7
            weights = delta**ranks
            weights = weights / weights.mean()
            if np.std(weights) > 0 and np.std(ret) > 0:
                str_values[stock] = np.cov(weights, ret)[0, 1]

        str_series = pd.Series(str_values)
        print(
            f"    OK 覆盖:{len(str_series)}, mean={str_series.mean():.6f}, "
            f"min={str_series.min():.6f}, max={str_series.max():.6f}"
        )
        STR_OK = True
    except Exception as e:
        print(f"    FAIL: {e}")
        import traceback

        traceback.print_exc()

    print("\n  [6.1] 理想振幅因子...")
    try:
        LAMBDA = 0.25
        amp_values = {}
        for stock in test_stocks:
            if stock not in ohlc_data:
                continue
            bars = ohlc_data[stock][-LOOKBACK:]
            highs, lows, closes = (
                bars["high"].values,
                bars["low"].values,
                bars["close"].values,
            )
            if len(closes) < 2:
                continue
            amp = (highs[1:] - lows[1:]) / closes[:-1]
            if len(amp) < LOOKBACK * 0.5:
                continue
            mid = (highs[1:] + lows[1:]) / 2
            th_high = np.percentile(mid, 100 - LAMBDA * 100)
            th_low = np.percentile(mid, LAMBDA * 100)
            mask_h = mid >= th_high
            mask_l = mid <= th_low
            if mask_h.sum() > 0 and mask_l.sum() > 0:
                std = amp.std()
                if std > 1e-8:
                    amp_values[stock] = (amp[mask_h].mean() - amp[mask_l].mean()) / std

        amp_series = pd.Series(amp_values)
        print(
            f"    OK 覆盖:{len(amp_series)}, mean={amp_series.mean():.6f}, "
            f"min={amp_series.min():.6f}, max={amp_series.max():.6f}"
        )
        AMP_OK = True
    except Exception as e:
        print(f"    FAIL: {e}")
        import traceback

        traceback.print_exc()

    print("\n  [7.1] 二阶动量...")
    try:
        mom_values = {}
        lw = 20
        for stock in test_stocks:
            if stock not in price_data:
                continue
            closes = price_data[stock]
            if len(closes) < lw + 10:
                continue
            moms = [closes[i] / closes[i - lw] - 1 for i in range(lw, len(closes))]
            if len(moms) < 10:
                continue
            arr = np.array(moms)
            ewma = np.average(
                arr[:-1], weights=np.exp(np.linspace(-1, 0, len(arr) - 1))
            )
            mom_values[stock] = arr[-1] - ewma

        mom_series = pd.Series(mom_values)
        print(
            f"    OK 覆盖:{len(mom_series)}, mean={mom_series.mean():.6f}, "
            f"min={mom_series.min():.6f}, max={mom_series.max():.6f}"
        )
        MOM_OK = True
    except Exception as e:
        print(f"    FAIL: {e}")
        import traceback

        traceback.print_exc()

print("\n[5/5] 因子相关性...")
try:
    af = {}
    if BASELINE_OK and factors is not None:
        ld = factors.index.get_level_values(1).max()
        lt = factors.xs(ld, level=1)
        for c in ["pe_ratio", "pb_ratio"]:
            if c in lt.columns:
                af[c] = lt[c].dropna()
    if STR_OK and len(str_series) > 0:
        af["STR"] = str_series
    if AMP_OK and len(amp_series) > 0:
        af["ideal_amp"] = amp_series
    if MOM_OK and len(mom_series) > 0:
        af["mom2"] = mom_series

    fdf = pd.DataFrame(af)
    print(f"  合并前样本: {len(fdf)}")
    fdf = fdf.dropna()
    print(f"  有效样本(dropna后): {len(fdf)}, 因子: {fdf.columns.tolist()}")
    if len(fdf) > 2:
        cm = fdf.rank().corr()
        print(f"\n  秩相关矩阵:")
        print(cm.round(3).to_string())
        print(f"\n  高相关(|r|>0.5):")
        found = False
        for i in range(len(cm.columns)):
            for j in range(i + 1, len(cm.columns)):
                v = cm.iloc[i, j]
                if abs(v) > 0.5:
                    print(f"    {cm.columns[i]} vs {cm.columns[j]}: {v:.3f}")
                    found = True
        if not found:
            print(f"    无")
    else:
        print(f"  样本不足，跳过相关性分析")
except Exception as e:
    print(f"  FAIL: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 70)
print("【结论】")
print("=" * 70)
for name, ok in [
    ("基线因子", BASELINE_OK),
    ("STR", STR_OK),
    ("理想振幅", AMP_OK),
    ("二阶动量", MOM_OK),
]:
    print(f"  {name}: {'OK' if ok else 'FAIL'}")

if all([BASELINE_OK, STR_OK, AMP_OK, MOM_OK]):
    print("\n全部通过，进入阶段B（单因子IC验证）")
else:
    print("\n部分失败，需排查")
