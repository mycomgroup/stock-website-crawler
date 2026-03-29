# ETF 择时插件对比验证
# 固定基线: 20日动量, 10日持有, top3 ETF

from jqdata import *
import pandas as pd
import numpy as np
from scipy import stats

print("=" * 70)
print("ETF 择时插件对比验证 (2020-01-01 ~ 2025-12-31)")
print("=" * 70)

START = "2020-01-01"
END = "2025-12-31"
MOM_WINDOW = 20
HOLD_DAYS = 10
TOP_N = 3
COST = 0.001

ETF_POOL = {
    "510300.XSHG": "沪深300ETF",
    "510500.XSHG": "中证500ETF",
    "159915.XSHE": "创业板ETF",
    "588000.XSHG": "科创50ETF",
    "518880.XSHG": "黄金ETF",
    "511010.XSHG": "国债ETF",
    "159941.XSHE": "纳指ETF",
    "513500.XSHG": "标普500ETF",
}
CODES = list(ETF_POOL.keys())


def get_rebal_dates(start, end, freq_days):
    all_days = get_trade_days(start, end)
    result = [all_days[0]]
    for d in all_days[1:]:
        if (d - result[-1]).days >= freq_days:
            result.append(d)
    return result


# ---- 择时信号函数 ----
def signal_breadth(date, threshold=0.4):
    """市场宽度: 沪深300成分股中 close>MA20 比例 > threshold 才做多"""
    try:
        stks = get_index_stocks("000300.XSHG", date=date)[:200]
        prices = get_price(
            stks, end_date=str(date), count=21, fields=["close"], panel=False
        )
        pivot = prices.pivot(index="time", columns="code", values="close").dropna(
            axis=1
        )
        if len(pivot) < 21:
            return True
        ma20 = pivot.rolling(20).mean().iloc[-1]
        ratio = (pivot.iloc[-1] > ma20).mean()
        return ratio > threshold
    except:
        return True


def signal_rsrs(date, n=18, m=600, buy_thresh=0.7, sell_thresh=-0.7):
    """RSRS 标准化右偏分"""
    try:
        prices = get_price(
            "000300.XSHG",
            end_date=str(date),
            count=m + n,
            fields=["high", "low"],
            panel=False,
        ).set_index("time")
        if len(prices) < m + n:
            return True
        slopes = []
        for i in range(n, len(prices)):
            sl, _, _, _, _ = stats.linregress(
                prices["low"].values[i - n : i], prices["high"].values[i - n : i]
            )
            slopes.append(sl)
        s = pd.Series(slopes)
        z = (s - s.rolling(m).mean()) / s.rolling(m).std()
        right = s * z
        latest = right.dropna().iloc[-1]
        return latest > buy_thresh
    except:
        return True


def signal_bbi(date):
    """BBI 大盘趋势: 收盘 > BBI(3,6,12,24) 才做多"""
    try:
        prices = get_price(
            "000300.XSHG", end_date=str(date), count=25, fields=["close"], panel=False
        )["close"]
        bbi = (
            prices.rolling(3).mean()
            + prices.rolling(6).mean()
            + prices.rolling(12).mean()
            + prices.rolling(24).mean()
        ) / 4
        return prices.iloc[-1] > bbi.iloc[-1]
    except:
        return True


def run_with_timing(timing_fn, label, dates):
    """运行带择时插件的版本"""
    rets, empty_periods = [], 0
    prev_holdings = []
    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i + 1])
        try:
            # 择时判断
            if timing_fn is not None and not timing_fn(d):
                rets.append(0.0)
                empty_periods += 1
                prev_holdings = []
                continue
            # 动量选 ETF
            prices = get_price(
                CODES,
                end_date=d_str,
                count=MOM_WINDOW + 1,
                fields=["close"],
                panel=False,
            )
            pivot = prices.pivot(index="time", columns="code", values="close").dropna(
                axis=1
            )
            if len(pivot) < MOM_WINDOW + 1:
                continue
            mom = pivot.iloc[-1] / pivot.iloc[0] - 1
            selected = mom.nlargest(TOP_N).index.tolist()
            p0 = get_price(
                selected, end_date=d_str, count=1, fields=["close"], panel=False
            )
            p1 = get_price(
                selected, end_date=next_d_str, count=1, fields=["close"], panel=False
            )
            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            gross = ((p1 / p0) - 1).mean()
            turnover = len(set(selected) - set(prev_holdings)) / TOP_N
            rets.append(gross - turnover * COST * 2)
            prev_holdings = selected
        except:
            continue
    if not rets:
        return None
    s = pd.Series(rets)
    cum = (1 + s).cumprod()
    ppy = 252 / HOLD_DAYS
    ann = cum.iloc[-1] ** (ppy / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (ppy**0.5) if s.std() > 0 else 0
    empty_pct = empty_periods / len(s)
    return {
        "插件": label,
        "年化(扣费)": f"{ann:.1%}",
        "最大回撤": f"{dd:.1%}",
        "夏普": f"{sharpe:.2f}",
        "空仓率": f"{empty_pct:.0%}",
        "样本数": len(s),
    }


dates = get_rebal_dates(START, END, HOLD_DAYS)
print(f"调仓次数: {len(dates) - 1}")

plugins = [
    (None, "不择时 (基线)"),
    (signal_breadth, "仅市场宽度"),
    (signal_rsrs, "仅 RSRS"),
    (signal_bbi, "仅 BBI"),
    (lambda d: signal_breadth(d) and signal_rsrs(d), "宽度 + RSRS"),
]

rows = []
for fn, label in plugins:
    print(f"  运行: {label} ...")
    r = run_with_timing(fn, label, dates)
    if r:
        rows.append(r)
        print(f"    年化={r['年化(扣费)']}  回撤={r['最大回撤']}  空仓率={r['空仓率']}")

print("\n" + "=" * 70)
print("【择时插件对比汇总】")
print("=" * 70)
if rows:
    df_res = pd.DataFrame(rows).set_index("插件")
    print(df_res.to_string())

# 当前信号状态
print("\n" + "=" * 70)
print("【当前市场择时信号状态】")
print("=" * 70)
today = get_trade_days(end_date="2026-03-28", count=1)[-1]
print(f"  市场宽度信号: {'做多' if signal_breadth(today) else '空仓'}")
print(f"  RSRS 信号:    {'做多' if signal_rsrs(today) else '空仓'}")
print(f"  BBI 信号:     {'做多' if signal_bbi(today) else '空仓'}")
print("\n验证完成!")
