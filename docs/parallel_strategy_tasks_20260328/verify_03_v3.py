# ETF 择时插件对比验证 v3 - 全面改进版
# 改进: 纯A股池 / 修复RSRS / 多阈值宽度 / 仓位分级

from jqdata import *
import pandas as pd
import numpy as np
from scipy import stats

print("=" * 70)
print("ETF 择时插件对比验证 v3 (2020-01-01 ~ 2025-12-31)")
print("=" * 70)

START = "2020-01-01"
END = "2025-12-31"
MOM_WINDOW = 20
HOLD_DAYS = 10
TOP_N = 3
COST = 0.001

# === 改进1: 纯A股ETF池 ===
ETF_POOL_A = {
    "510300.XSHG": "沪深300ETF",
    "510500.XSHG": "中证500ETF",
    "159915.XSHE": "创业板ETF",
    "588000.XSHG": "科创50ETF",
}
CODES_A = list(ETF_POOL_A.keys())

# 原始池（对比用）
ETF_POOL_ALL = {
    "510300.XSHG": "沪深300ETF",
    "510500.XSHG": "中证500ETF",
    "159915.XSHE": "创业板ETF",
    "588000.XSHG": "科创50ETF",
    "518880.XSHG": "黄金ETF",
    "511010.XSHG": "国债ETF",
    "159941.XSHE": "纳指ETF",
    "513500.XSHG": "标普500ETF",
}
CODES_ALL = list(ETF_POOL_ALL.keys())


def get_rebal_dates(start, end, freq_days):
    all_days = get_trade_days(start, end)
    result = [all_days[0]]
    for d in all_days[1:]:
        if (d - result[-1]).days >= freq_days:
            result.append(d)
    return result


# ==========================================
# 择时信号函数
# ==========================================


def signal_breadth(date, threshold=0.4):
    """市场宽度: 返回宽度值 0~1"""
    try:
        stks = get_index_stocks("000300.XSHG", date=date)[:200]
        prices = get_price(
            stks, end_date=str(date), count=21, fields=["close"], panel=False
        )
        pivot = prices.pivot(index="time", columns="code", values="close").dropna(
            axis=1
        )
        if len(pivot) < 21:
            return 1.0
        ma20 = pivot.rolling(20).mean().iloc[-1]
        ratio = (pivot.iloc[-1] > ma20).mean()
        return ratio
    except:
        return 1.0


def signal_breadth_position(date):
    """市场宽度仓位分级: 返回仓位比例 0/0.5/1.0"""
    ratio = signal_breadth(date)
    if ratio >= 0.4:
        return 1.0
    elif ratio >= 0.25:
        return 0.5
    else:
        return 0.0


def signal_rsrs_fixed(date, n=18, m=600, buy_thresh=0.7):
    """RSRS 右偏修正标准分 (修复版)"""
    try:
        total_needed = m + n + 10
        prices = get_price(
            "000300.XSHG",
            end_date=str(date),
            count=total_needed,
            fields=["high", "low"],
            panel=False,
        ).set_index("time")

        if len(prices) < m + n:
            return False

        slopes = []
        rsq_list = []
        for i in range(n, len(prices)):
            x = prices["low"].values[i - n : i]
            y = prices["high"].values[i - n : i]
            sl, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            slopes.append(sl)
            rsq_list.append(r_value**2)

        s = pd.Series(slopes, index=prices.index[n:])
        rsq = pd.Series(rsq_list, index=prices.index[n:])

        s_mean = s.rolling(m).mean()
        s_std = s.rolling(m).std()
        z = (s - s_mean) / s_std

        revised = z * rsq
        right_skew = revised * s

        latest = right_skew.dropna().iloc[-1]
        return latest > buy_thresh
    except:
        return False


def signal_rsrs_debug(date, n=18, m=600):
    """RSRS 返回原始值用于调试"""
    try:
        total_needed = m + n + 10
        prices = get_price(
            "000300.XSHG",
            end_date=str(date),
            count=total_needed,
            fields=["high", "low"],
            panel=False,
        ).set_index("time")

        if len(prices) < m + n:
            return None

        slopes = []
        for i in range(n, len(prices)):
            x = prices["low"].values[i - n : i]
            y = prices["high"].values[i - n : i]
            sl, _, r_value, _, _ = stats.linregress(x, y)
            slopes.append(sl)

        s = pd.Series(slopes, index=prices.index[n:])
        z = (s - s.rolling(m).mean()) / s.rolling(m).std()
        right_skew = (z * s.pow(2)).dropna().iloc[-1]

        return right_skew
    except:
        return None


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


# ==========================================
# 回测框架
# ==========================================


def run_with_timing(timing_fn, label, dates, codes, position_fn=None):
    """运行带择时插件的版本"""
    rets, empty_periods = [], 0
    prev_holdings = []
    position_records = []

    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i + 1])
        try:
            # 确定仓位
            if position_fn is not None:
                position = position_fn(d)
            elif timing_fn is not None:
                signal = timing_fn(d)
                position = 1.0 if signal else 0.0
            else:
                position = 1.0

            if position == 0.0:
                rets.append(0.0)
                empty_periods += 1
                prev_holdings = []
                position_records.append(0.0)
                continue

            # 动量选 ETF
            prices = get_price(
                codes,
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

            # 应用仓位
            net_ret = position * (gross - turnover * COST * 2)
            rets.append(net_ret)
            prev_holdings = selected
            position_records.append(position)
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
    avg_pos = np.mean(position_records) if position_records else 1.0

    return {
        "插件": label,
        "年化": f"{ann:.1%}",
        "最大回撤": f"{dd:.1%}",
        "夏普": f"{sharpe:.2f}",
        "空仓率": f"{empty_pct:.0%}",
        "平均仓位": f"{avg_pos:.0%}",
        "样本数": len(s),
    }


# ==========================================
# 主程序
# ==========================================

dates = get_rebal_dates(START, END, HOLD_DAYS)
print(f"调仓次数: {len(dates) - 1}")

print("\n" + "=" * 70)
print("【Part 1: ETF池对比 - 纯A股 vs 全市场】")
print("=" * 70)

print("\n--- 纯A股池 (沪深300/中证500/创业板/科创50) ---")
r1 = run_with_timing(None, "纯A股池-不择时", dates, CODES_A)
if r1:
    print(f"  年化={r1['年化']}  回撤={r1['最大回撤']}  夏普={r1['夏普']}")

print("\n--- 全市场池 (含黄金/国债/纳指/标普) ---")
r2 = run_with_timing(None, "全市场池-不择时", dates, CODES_ALL)
if r2:
    print(f"  年化={r2['年化']}  回撤={r2['最大回撤']}  夏普={r2['夏普']}")

print("\n" + "=" * 70)
print("【Part 2: 宽度阈值测试 (纯A股池)】")
print("=" * 70)

thresholds = [0.25, 0.3, 0.35, 0.4]
for thresh in thresholds:
    fn = lambda d, t=thresh: signal_breadth(d, t)
    label = f"宽度阈值={thresh}"
    r = run_with_timing(fn, label, dates, CODES_A)
    if r:
        print(
            f"  {label}: 年化={r['年化']}  回撤={r['最大回撤']}  空仓率={r['空仓率']}"
        )

print("\n" + "=" * 70)
print("【Part 3: 仓位分级测试 (纯A股池)】")
print("=" * 70)

r3 = run_with_timing(
    None, "仓位分级", dates, CODES_A, position_fn=signal_breadth_position
)
if r3:
    print(
        f"  仓位分级: 年化={r3['年化']}  回撤={r3['最大回撤']}  平均仓位={r3['平均仓位']}  空仓率={r3['空仓率']}"
    )

r_base = run_with_timing(None, "不择时(基线)", dates, CODES_A)
if r_base:
    print(f"  不择时(基线): 年化={r_base['年化']}  回撤={r_base['最大回撤']}")

print("\n" + "=" * 70)
print("【Part 4: RSRS调试】")
print("=" * 70)

test_dates = dates[-10:]
print("最近10个调仓日RSRS值:")
for d in test_dates:
    val = signal_rsrs_debug(d)
    if val is not None:
        signal_str = "做多" if val > 0.7 else "空仓"
        print(f"  {d}: RSRS={val:.4f} -> {signal_str}")
    else:
        print(f"  {d}: RSRS=数据不足")

print("\n" + "=" * 70)
print("【Part 5: RSRS择时对比 (纯A股池)】")
print("=" * 70)

for thresh in [0.3, 0.5, 0.7]:
    fn = lambda d, t=thresh: signal_rsrs_fixed(d, buy_thresh=t)
    label = f"RSRS阈值={thresh}"
    r = run_with_timing(fn, label, dates, CODES_A)
    if r:
        print(
            f"  {label}: 年化={r['年化']}  回撤={r['最大回撤']}  空仓率={r['空仓率']}"
        )

print("\n" + "=" * 70)
print("【Part 6: 组合策略对比 (纯A股池)】")
print("=" * 70)

r_bbi = run_with_timing(signal_bbi, "BBI", dates, CODES_A)
if r_bbi:
    print(
        f"  BBI: 年化={r_bbi['年化']}  回撤={r_bbi['最大回撤']}  空仓率={r_bbi['空仓率']}"
    )

fn_combo = lambda d: signal_breadth(d, 0.3) >= 0.3 and signal_rsrs_fixed(
    d, buy_thresh=0.5
)
r_combo = run_with_timing(fn_combo, "宽度0.3+RSRS0.5", dates, CODES_A)
if r_combo:
    print(
        f"  宽度0.3+RSRS0.5: 年化={r_combo['年化']}  回撤={r_combo['最大回撤']}  空仓率={r_combo['空仓率']}"
    )

print("\n" + "=" * 70)
print("【Part 7: 当前市场信号】")
print("=" * 70)
today = get_trade_days(end_date="2026-03-28", count=1)[-1]
breadth_val = signal_breadth(today)
rsrs_val = signal_rsrs_debug(today)
bbi_val = signal_bbi(today)

print(f"  日期: {today}")
print(f"  宽度值: {breadth_val:.2%}")
print(f"    - 阈值0.25: {'做多' if breadth_val >= 0.25 else '空仓'}")
print(f"    - 阈值0.30: {'做多' if breadth_val >= 0.30 else '空仓'}")
print(f"    - 阈值0.40: {'做多' if breadth_val >= 0.40 else '空仓'}")
print(f"    - 仓位分级: {signal_breadth_position(today) * 100:.0f}%")
print(f"  RSRS值: {rsrs_val if rsrs_val is not None else 'N/A'}")
print(f"  BBI信号: {'做多' if bbi_val else '空仓'}")

print("\n验证完成!")
