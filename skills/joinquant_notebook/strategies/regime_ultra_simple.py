# 状态路由器V2 - 极简回测
# 只使用指数数据，不遍历成分股

print("=" * 60)
print("状态路由器V2 - 极简回测验证")
print("=" * 60)

from jqdata import *
import pandas as pd
import numpy as np

# ============================================================
# 1. 获取数据
# ============================================================
print("\n【1】获取指数数据...")

data = get_price(
    ["000300.XSHG", "511010.XSHG", "510300.XSHG"],
    start_date="2024-10-01",
    end_date="2025-03-28",
    fields=["close"],
    panel=False,
)

tc = "time" if "time" in data.columns else "date"

hs300 = data[data["code"] == "000300.XSHG"].set_index(tc)["close"]
bond = data[data["code"] == "511010.XSHG"].set_index(tc)["close"]
etf = data[data["code"] == "510300.XSHG"].set_index(tc)["close"]

print(f"  数据: {len(hs300)} 交易日")
print(f"  沪深300: {(hs300.iloc[-1] / hs300.iloc[0] - 1):.2%}")
print(f"  国债ETF: {(bond.iloc[-1] / bond.iloc[0] - 1):.2%}")

# ============================================================
# 2. 用指数价格判断状态
# ============================================================
print("\n【2】状态判断 (基于指数价格)...")


def get_regime_simple(month_str):
    """简化版: 用沪深300的20日均线判断"""
    try:
        end = month_str + "-28"
        prices = get_price(
            "000300.XSHG", end_date=end, count=30, fields=["close"], panel=False
        )
        tc2 = "time" if "time" in prices.columns else "date"
        close = prices.set_index(tc2)["close"]
        ma20 = close.rolling(20).mean().iloc[-1]
        current = close.iloc[-1]
        above = current > ma20

        # 用价格位置判断
        high_60 = close.max()
        low_60 = close.min()
        pos = (current - low_60) / (high_60 - low_60)

        if pos > 0.8:
            return "高估防守"
        elif pos > 0.5 and above:
            return "趋势进攻"
        elif pos > 0.3:
            return "震荡轮动"
        else:
            return "底部试错"
    except:
        return "震荡轮动"


months = ["2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03"]
regimes = {}
for m in months:
    r = get_regime_simple(m)
    regimes[m] = r
    print(f"  {m}: {r}")

# ============================================================
# 3. 计算收益
# ============================================================
print("\n【3】收益对比...")

CONFIGS = {
    "底部试错": (0.30, 0.30, 0.10),
    "趋势进攻": (0.40, 0.20, 0.30),
    "震荡轮动": (0.35, 0.25, 0.20),
    "高估防守": (0.15, 0.40, 0.05),
}
STATIC = (0.40, 0.30, 0.10)

print(f"\n{'月份':<10}{'状态':<12}{'状态配置':>12}{'静态配置':>12}{'差异':>12}")
print("-" * 60)

cum_static = 1.0
cum_regime = 1.0

for m in months:
    regime = regimes[m]
    cfg = CONFIGS[regime]

    month_data = [d for d in hs300.index if str(d)[:7] == m]
    if len(month_data) >= 2:
        s = month_data[0]
        e = month_data[-1]

        r_s = hs300.loc[e] / hs300.loc[s] - 1
        r_b = bond.loc[e] / bond.loc[s] - 1
        r_e = etf.loc[e] / etf.loc[s] - 1

        r_regime = cfg[0] * r_s + cfg[1] * r_b + cfg[2] * r_e
        r_static = STATIC[0] * r_s + STATIC[1] * r_b + STATIC[2] * r_e

        cum_regime *= 1 + r_regime
        cum_static *= 1 + r_static

        print(
            f"{m:<10}{regime:<12}{r_regime:>11.2%}{r_static:>12.2%}{r_regime - r_static:>+11.2%}"
        )

print("-" * 60)
print(
    f"{'累计':<10}{'':12}{cum_regime - 1:>11.2%}{cum_static - 1:>12.2%}{cum_regime - cum_static:>+11.2%}"
)

# ============================================================
# 4. 结论
# ============================================================
print("\n" + "=" * 60)
print("【4】结论")
print("=" * 60)

diff = cum_regime - cum_static
print(f"""
  回测: 2024-10 ~ 2025-03 (6个月)
  
  状态切换收益: {(cum_regime - 1):.2%}
  静态配置收益: {(cum_static - 1):.2%}
  差异: {diff:+.2%}
  
  结论: {"状态切换更优 ✓" if diff > 0 else "静态配置更优 ✗"}
""")

last_m = months[-1]
print(f"  当前状态 ({last_m}): 【{regimes[last_m]}】")

print("\n验证完成!")
