# 状态路由器V2 - 完整回测验证 (Notebook格式)
# 回测期间: 2024-01-01 ~ 2025-03-28
# 本策略直接执行，适合在 Notebook 中运行

print("=" * 70)
print("状态路由器V2 - 完整回测验证")
print("回测期间: 2024-01-01 ~ 2025-03-28")
print("=" * 70)

from jqdata import *
import pandas as pd
import numpy as np
from scipy import stats

# ============================================================
# 1. 获取资产收益数据
# ============================================================
print("\n【1】获取资产收益数据...")

hs300 = get_price(
    "000300.XSHG",
    start_date="2024-01-01",
    end_date="2025-03-28",
    fields=["close"],
    panel=False,
)
bond = get_price(
    "511010.XSHG",
    start_date="2024-01-01",
    end_date="2025-03-28",
    fields=["close"],
    panel=False,
)
momentum = get_price(
    "510300.XSHG",
    start_date="2024-01-01",
    end_date="2025-03-28",
    fields=["close"],
    panel=False,
)

time_col = "time" if "time" in hs300.columns else "date"
hs300_series = hs300.set_index(time_col)["close"]
bond_series = bond.set_index(time_col)["close"]
momentum_series = momentum.set_index(time_col)["close"]

stock_ret = hs300_series.pct_change().fillna(0)
bond_ret = bond_series.pct_change().fillna(0)
momentum_ret = momentum_series.pct_change().fillna(0)

print(f"  数据获取完成!")
print(f"  交易日数: {len(hs300_series)}")
print(f"  沪深300区间收益: {(hs300_series.iloc[-1] / hs300_series.iloc[0] - 1):.2%}")

# ============================================================
# 2. 计算月度状态
# ============================================================
print("\n【2】计算月度市场状态...")


def get_regime(date_str):
    """计算指定日期的市场状态"""
    try:
        stks = get_index_stocks("000300.XSHG", date=date_str)[:100]
        prices = get_price(
            stks, end_date=date_str, count=21, fields=["close"], panel=False
        )
        tc = "time" if "time" in prices.columns else "date"
        pivot = prices.pivot(index=tc, columns="code", values="close").dropna(axis=1)
        ma20 = pivot.rolling(20).mean().iloc[-1]
        breadth = (pivot.iloc[-1] > ma20).mean()

        if breadth > 0.7:
            return "高估防守"
        elif breadth > 0.5:
            return "趋势进攻"
        elif breadth >= 0.3:
            return "震荡轮动"
        else:
            return "底部试错"
    except:
        return "震荡轮动"


# 获取每月第一个交易日
trade_days = get_trade_days("2024-01-01", "2025-03-28")
monthly_dates = []
prev_month = None
for day in trade_days:
    if day.month != prev_month:
        monthly_dates.append(day)
        prev_month = day.month

regime_history = {}
for date in monthly_dates:
    date_str = str(date)
    regime = get_regime(date_str)
    regime_history[date_str[:7]] = regime
    print(f"  {date_str[:7]}: {regime}")

# ============================================================
# 3. 配置定义
# ============================================================
print("\n【3】配置定义")

REGIME_CONFIGS = {
    "底部试错": {"stock": 0.30, "bond": 0.30, "momentum": 0.10, "cash": 0.30},
    "趋势进攻": {"stock": 0.40, "bond": 0.20, "momentum": 0.30, "cash": 0.10},
    "震荡轮动": {"stock": 0.35, "bond": 0.25, "momentum": 0.20, "cash": 0.20},
    "高估防守": {"stock": 0.15, "bond": 0.40, "momentum": 0.05, "cash": 0.40},
}

STATIC = {"stock": 0.40, "bond": 0.30, "momentum": 0.10, "cash": 0.20}

print("  状态配置:")
for regime, config in REGIME_CONFIGS.items():
    print(
        f"    {regime}: 股票{config['stock']:.0%} + 国债{config['bond']:.0%} + 动量{config['momentum']:.0%} + 现金{config['cash']:.0%}"
    )

# ============================================================
# 4. 计算NAV
# ============================================================
print("\n【4】计算累计净值...")

# 静态配置NAV
static_nav = [1.0]
for i in range(1, len(hs300_series)):
    r = (
        STATIC["stock"] * stock_ret.iloc[i]
        + STATIC["bond"] * bond_ret.iloc[i]
        + STATIC["momentum"] * momentum_ret.iloc[i]
    )
    static_nav.append(static_nav[-1] * (1 + r))

# 状态切换NAV
regime_nav = [1.0]
for i in range(1, len(hs300_series)):
    date = hs300_series.index[i]
    month_str = str(date)[:7]

    current_regime = regime_history.get(month_str, "震荡轮动")
    config = REGIME_CONFIGS[current_regime]

    r = (
        config["stock"] * stock_ret.iloc[i]
        + config["bond"] * bond_ret.iloc[i]
        + config["momentum"] * momentum_ret.iloc[i]
    )
    regime_nav.append(regime_nav[-1] * (1 + r))

# 基准NAV
benchmark_nav = (hs300_series / hs300_series.iloc[0]).tolist()

print(f"  静态配置最终净值: {static_nav[-1]:.4f}")
print(f"  状态切换最终净值: {regime_nav[-1]:.4f}")
print(f"  沪深300最终净值: {benchmark_nav[-1]:.4f}")

# ============================================================
# 5. 统计指标
# ============================================================
print("\n【5】策略对比统计")


def metrics(nav):
    nav = pd.Series(nav)
    total = nav.iloc[-1] - 1
    daily = nav.pct_change().dropna()
    years = len(nav) / 252
    ann_ret = (1 + total) ** (1 / years) - 1
    ann_vol = daily.std() * np.sqrt(252)
    sharpe = (ann_ret - 0.02) / ann_vol if ann_vol > 0 else 0
    max_dd = (nav / nav.cummax() - 1).min()
    return total, ann_ret, sharpe, max_dd


s_total, s_ret, s_sharpe, s_dd = metrics(static_nav)
r_total, r_ret, r_sharpe, r_dd = metrics(regime_nav)
b_total, b_ret, b_sharpe, b_dd = metrics(benchmark_nav)

print(f"\n{'指标':<12}{'静态配置':>14}{'状态切换':>14}{'沪深300':>14}{'差异':>14}")
print("-" * 70)
print(
    f"{'累计收益':<12}{s_total:>13.2%}{r_total:>14.2%}{b_total:>14.2%}{r_total - s_total:>+13.2%}"
)
print(
    f"{'年化收益':<12}{s_ret:>13.2%}{r_ret:>14.2%}{b_ret:>14.2%}{r_ret - s_ret:>+13.2%}"
)
print(
    f"{'夏普比率':<12}{s_sharpe:>13.2f}{r_sharpe:>14.2f}{b_sharpe:>14.2f}{r_sharpe - s_sharpe:>+13.2f}"
)
print(f"{'最大回撤':<12}{s_dd:>13.2%}{r_dd:>14.2%}{b_dd:>14.2%}{r_dd - s_dd:>+13.2%}")

# ============================================================
# 6. 结论
# ============================================================
print("\n" + "=" * 70)
print("【6】结论")
print("=" * 70)

better_sharpe = r_sharpe > s_sharpe
better_dd = r_dd > s_dd
better_ret = r_total > s_total

print(f"\n  夏普比率: {'状态切换更优 ✓' if better_sharpe else '静态配置更优 ✗'}")
print(f"  最大回撤: {'状态切换更优 ✓' if better_dd else '静态配置更优 ✗'}")
print(f"  累计收益: {'状态切换更优 ✓' if better_ret else '静态配置更优 ✗'}")

# 当前状态
last_month = list(regime_history.keys())[-1]
last_regime = regime_history[last_month]
last_config = REGIME_CONFIGS[last_regime]

print(f"\n  当前状态 ({last_month}): 【{last_regime}】")
print(f"  建议配置:")
print(f"    股票: {last_config['stock']:.0%}")
print(f"    国债ETF: {last_config['bond']:.0%}")
print(f"    动量ETF: {last_config['momentum']:.0%}")
print(f"    现金: {last_config['cash']:.0%}")

print("\n" + "=" * 70)
print("验证完成!")
print("=" * 70)
