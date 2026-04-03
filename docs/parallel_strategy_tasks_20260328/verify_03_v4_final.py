# ETF 择时插件对比验证 v4 - 最终版
# 改进: RSRS参数优化 / 宽度信号统一 / 全市场池测试 / 完整对比

from jqdata import *
import pandas as pd
import numpy as np
from scipy import stats

print("=" * 70)
print("ETF 择时插件对比验证 v4 最终版 (2020-01-01 ~ 2025-12-31)")
print("=" * 70)

START = "2020-01-01"
END = "2025-12-31"
MOM_WINDOW = 20
HOLD_DAYS = 10
TOP_N = 3
COST = 0.001

# ETF池配置
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
# 择时信号函数（统一实现）
# ==========================================


def signal_breadth(date, threshold=0.4):
    """市场宽度: 返回宽度值 0~1（统一版）"""
    try:
        stks = get_index_stocks("000300.XSHG", date=date)[:200]
        prices = get_price(
            stks, end_date=str(date), count=21, fields=["close"], panel=False
        )
        pivot = prices.pivot(index="time", columns="code", values="close").dropna(
            axis=1
        )
        if len(pivot) < 21:
            return None  # 数据不足返回None
        ma20 = pivot.rolling(20).mean().iloc[-1]
        ratio = (pivot.iloc[-1] > ma20).mean()
        return ratio
    except:
        return None


def signal_breadth_bool(date, threshold=0.4):
    """市场宽度布尔版：True=做多，False=空仓"""
    ratio = signal_breadth(date, threshold)
    if ratio is None:
        return True  # 数据不足时默认做多
    return ratio >= threshold


def signal_breadth_position(date):
    """市场宽度仓位分级: 返回仓位比例 0/0.5/1.0"""
    ratio = signal_breadth(date)
    if ratio is None:
        return 1.0  # 数据不足时满仓
    if ratio >= 0.4:
        return 1.0
    elif ratio >= 0.25:
        return 0.5
    else:
        return 0.0


def signal_rsrs_short(date, n=10, m=300, buy_thresh=0.7):
    """RSRS 短周期版 (N=10, M=300)，适合有限历史数据"""
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
            return None  # 数据不足返回None

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

        # 标准分
        s_mean = s.rolling(m).mean()
        s_std = s.rolling(m).std()
        z = (s - s_mean) / s_std

        # 修正标准分 * R^2 * beta (右偏)
        revised = z * rsq
        right_skew = revised * s

        latest = right_skew.dropna().iloc[-1]
        return latest
    except:
        return None


def signal_rsrs_bool(date, n=10, m=300, buy_thresh=0.7):
    """RSRS 布尔版：True=做多，False=空仓"""
    val = signal_rsrs_short(date, n, m)
    if val is None:
        return True  # 数据不足时默认做多
    return val > buy_thresh


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


def run_backtest(timing_fn, label, dates, codes, position_fn=None):
    """运行回测"""
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
        "年化": ann,
        "最大回撤": dd,
        "夏普": sharpe,
        "空仓率": empty_pct,
        "平均仓位": avg_pos,
        "样本数": len(s),
    }


# ==========================================
# 主程序
# ==========================================

dates = get_rebal_dates(START, END, HOLD_DAYS)
print(f"调仓次数: {len(dates) - 1}")

results = []

print("\n" + "=" * 70)
print("【Part 1: 基线对比】")
print("=" * 70)

# 不择时基线
r = run_backtest(None, "不择时(基线)", dates, CODES_ALL)
if r:
    results.append(r)
    print(
        f"  不择时(基线): 年化={r['年化']:.1%}  回撤={r['最大回撤']:.1%}  夏普={r['夏普']:.2f}"
    )

print("\n" + "=" * 70)
print("【Part 2: 市场宽度测试】")
print("=" * 70)

# 宽度阈值测试
for thresh in [0.25, 0.30, 0.35, 0.40]:
    fn = lambda d, t=thresh: signal_breadth_bool(d, t)
    r = run_backtest(fn, f"宽度{t}", dates, CODES_ALL)
    if r:
        results.append(r)
        print(
            f"  宽度{thresh}: 年化={r['年化']:.1%}  回撤={r['最大回撤']:.1%}  空仓率={r['空仓率']:.0%}"
        )

# 仓位分级
r = run_backtest(
    None, "宽度仓位分级", dates, CODES_ALL, position_fn=signal_breadth_position
)
if r:
    results.append(r)
    print(
        f"  宽度仓位分级: 年化={r['年化']:.1%}  回撤={r['最大回撤']:.1%}  平均仓位={r['平均仓位']:.0%}"
    )

print("\n" + "=" * 70)
print("【Part 3: RSRS测试（短周期版 N=10 M=300）】")
print("=" * 70)

# RSRS阈值测试
for thresh in [0.3, 0.5, 0.7, 1.0]:
    fn = lambda d, t=thresh: signal_rsrs_bool(d, buy_thresh=t)
    r = run_backtest(fn, f"RSRS{thresh}", dates, CODES_ALL)
    if r:
        results.append(r)
        print(
            f"  RSRS{thresh}: 年化={r['年化']:.1%}  回撤={r['最大回撤']:.1%}  空仓率={r['空仓率']:.0%}"
        )

print("\n" + "=" * 70)
print("【Part 4: BBI测试】")
print("=" * 70)

r = run_backtest(signal_bbi, "BBI", dates, CODES_ALL)
if r:
    results.append(r)
    print(
        f"  BBI: 年化={r['年化']:.1%}  回撤={r['最大回撤']:.1%}  空仓率={r['空仓率']:.0%}"
    )

print("\n" + "=" * 70)
print("【Part 5: 组合策略测试】")
print("=" * 70)

# 宽度0.3 + RSRS0.5
fn_combo1 = lambda d: signal_breadth_bool(d, 0.3) and signal_rsrs_bool(
    d, buy_thresh=0.5
)
r = run_backtest(fn_combo1, "宽度0.3+RSRS0.5", dates, CODES_ALL)
if r:
    results.append(r)
    print(
        f"  宽度0.3+RSRS0.5: 年化={r['年化']:.1%}  回撤={r['最大回撤']:.1%}  空仓率={r['空仓率']:.0%}"
    )


# 宽度仓位分级 + RSRS0.5
def position_combo(d):
    pos = signal_breadth_position(d)
    if pos == 0:
        return 0
    if not signal_rsrs_bool(d, buy_thresh=0.5):
        return pos * 0.5  # RSRS空仓时减半
    return pos


r = run_backtest(None, "宽度分级+RSRS0.5", dates, CODES_ALL, position_fn=position_combo)
if r:
    results.append(r)
    print(
        f"  宽度分级+RSRS0.5: 年化={r['年化']:.1%}  回撤={r['最大回撤']:.1%}  平均仓位={r['平均仓位']:.0%}"
    )

print("\n" + "=" * 70)
print("【Part 6: 汇总表】")
print("=" * 70)

# 按夏普排序
df = pd.DataFrame(results)
df = df.sort_values("夏普", ascending=False)
df["年化"] = df["年化"].apply(lambda x: f"{x:.1%}")
df["最大回撤"] = df["最大回撤"].apply(lambda x: f"{x:.1%}")
df["夏普"] = df["夏普"].apply(lambda x: f"{x:.2f}")
df["空仓率"] = df["空仓率"].apply(lambda x: f"{x:.0%}")
df["平均仓位"] = df["平均仓位"].apply(lambda x: f"{x:.0%}")

print(
    df[["插件", "年化", "最大回撤", "夏普", "空仓率", "平均仓位"]].to_string(
        index=False
    )
)

print("\n" + "=" * 70)
print("【Part 7: 当前市场信号】")
print("=" * 70)

today = get_trade_days(end_date="2026-03-28", count=1)[-1]
breadth_val = signal_breadth(today)
rsrs_val = signal_rsrs_short(today)
bbi_val = signal_bbi(today)

print(f"  日期: {today}")
print(f"  宽度值: {breadth_val:.2%}" if breadth_val else "  宽度值: 数据不足")
if breadth_val:
    print(f"    - 阈值0.25: {'做多' if breadth_val >= 0.25 else '空仓'}")
    print(f"    - 阈值0.30: {'做多' if breadth_val >= 0.30 else '空仓'}")
    print(f"    - 阈值0.40: {'做多' if breadth_val >= 0.40 else '空仓'}")
    print(f"    - 仓位分级: {signal_breadth_position(today) * 100:.0f}%")
print(f"  RSRS值: {rsrs_val:.4f}" if rsrs_val else "  RSRS值: 数据不足")
if rsrs_val:
    print(f"    - 阈值0.5: {'做多' if rsrs_val > 0.5 else '空仓'}")
    print(f"    - 阈值0.7: {'做多' if rsrs_val > 0.7 else '空仓'}")
print(f"  BBI信号: {'做多' if bbi_val else '空仓'}")

# 最终建议
print("\n" + "=" * 70)
print("【最终建议】")
print("=" * 70)

if results:
    best = max(results, key=lambda x: x["夏普"])
    print(f"  最优策略: {best['插件']}")
    print(
        f"    年化={best['年化']:.1%}  回撤={best['最大回撤']:.1%}  夏普={best['夏普']:.2f}"
    )

    # 找出回撤改善最明显的
    baseline = next((r for r in results if r["插件"] == "不择时(基线)"), None)
    if baseline:
        improved = [r for r in results if r["最大回撤"] > baseline["最大回撤"]]
        if improved:
            best_dd = max(improved, key=lambda x: x["最大回撤"] - baseline["最大回撤"])
            dd_improve = baseline["最大回撤"] - best_dd["最大回撤"]
            print(f"\n  回撤改善最优: {best_dd['插件']}")
            print(
                f"    回撤改善: {dd_improve:.1%} (从{baseline['最大回撤']:.1%}到{best_dd['最大回撤']:.1%})"
            )

print("\n验证完成!")
