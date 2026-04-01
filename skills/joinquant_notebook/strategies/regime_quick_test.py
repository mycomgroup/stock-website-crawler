# 状态路由器V2 - 快速回测 (2024Q4)
# 使用单季度数据快速验证

print("=" * 60)
print("状态路由器V2 - 快速回测 (2024-10 ~ 2025-03)")
print("=" * 60)

from jqdata import *
import pandas as pd
import numpy as np

# ============================================================
# 1. 获取资产数据
# ============================================================
print("\n【1】获取资产数据...")

hs300 = get_price(
    "000300.XSHG",
    start_date="2024-10-01",
    end_date="2025-03-28",
    fields=["close"],
    panel=False,
)
bond = get_price(
    "511010.XSHG",
    start_date="2024-10-01",
    end_date="2025-03-28",
    fields=["close"],
    panel=False,
)
etf = get_price(
    "510300.XSHG",
    start_date="2024-10-01",
    end_date="2025-03-28",
    fields=["close"],
    panel=False,
)

tc = "time" if "time" in hs300.columns else "date"
h = hs300.set_index(tc)["close"]
b = bond.set_index(tc)["close"]
e = etf.set_index(tc)["close"]

print(
    f"  沪深300: {h.iloc[0]:.0f} -> {h.iloc[-1]:.0f} ({(h.iloc[-1] / h.iloc[0] - 1):.2%})"
)
print(
    f"  国债ETF: {b.iloc[0]:.0f} -> {b.iloc[-1]:.0f} ({(b.iloc[-1] / b.iloc[0] - 1):.2%})"
)

# ============================================================
# 2. 计算月度状态
# ============================================================
print("\n【2】月度状态...")


def get_regime(date_str):
    try:
        stks = get_index_stocks("000300.XSHG", date=date_str)[:80]
        prices = get_price(
            stks, end_date=date_str, count=21, fields=["close"], panel=False
        )
        tc2 = "time" if "time" in prices.columns else "date"
        pv = prices.pivot(index=tc2, columns="code", values="close").dropna(axis=1)
        ma20 = pv.rolling(20).mean().iloc[-1]
        breadth = (pv.iloc[-1] > ma20).mean()

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


months = ["2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03"]
regime_data = {}
for m in months:
    r = get_regime(m + "-15")
    regime_data[m] = r
    print(f"  {m}: {r}")

# ============================================================
# 3. 计算收益
# ============================================================
print("\n【3】配置收益计算...")

CONFIGS = {
    "底部试错": (0.30, 0.30, 0.10),
    "趋势进攻": (0.40, 0.20, 0.30),
    "震荡轮动": (0.35, 0.25, 0.20),
    "高估防守": (0.15, 0.40, 0.05),
}
STATIC = (0.40, 0.30, 0.10)

# 按月计算收益
print(f"\n{'月份':<10}{'状态':<12}{'状态配置':>12}{'静态配置':>12}{'差异':>12}")
print("-" * 60)

total_static = 1.0
total_regime = 1.0

for i in range(len(months)):
    m = months[i]
    regime = regime_data[m]
    config = CONFIGS[regime]

    # 找当月数据
    mask = [str(d)[:7] == m for d in h.index]
    idx = [j for j, x in enumerate(mask) if x]

    if len(idx) > 1:
        s, e_idx = idx[0], idx[-1]

        stock_r = h.iloc[e_idx] / h.iloc[s] - 1
        bond_r = b.iloc[e_idx] / b.iloc[s] - 1
        etf_r = e.iloc[e_idx] / e.iloc[s] - 1

        r_month = config[0] * stock_r + config[1] * bond_r + config[2] * etf_r
        s_month = STATIC[0] * stock_r + STATIC[1] * bond_r + STATIC[2] * etf_r

        total_regime *= 1 + r_month
        total_static *= 1 + s_month

        print(
            f"{m:<10}{regime:<12}{r_month:>11.2%}{s_month:>12.2%}{r_month - s_month:>+11.2%}"
        )

print("-" * 60)
print(
    f"{'累计':<10}{'':12}{total_regime - 1:>11.2%}{total_static - 1:>12.2%}{(total_regime - total_static):>+11.2%}"
)

# ============================================================
# 4. 结论
# ============================================================
print("\n" + "=" * 60)
print("【4】结论")
print("=" * 60)

print(f"""
  回测期间: 2024-10 ~ 2025-03 (6个月)
  
  状态切换配置收益: {(total_regime - 1):.2%}
  静态配置收益: {(total_static - 1):.2%}
  差异: {(total_regime - total_static):+.2%}
  
  {"状态切换更优 ✓" if total_regime > total_static else "静态配置更优 ✗"}
""")

# 当前状态
last_m = months[-1]
last_r = regime_data[last_m]
last_c = CONFIGS[last_r]

print(f"  当前状态 ({last_m}): 【{last_r}】")
print(f"  建议配置:")
print(f"    股票: {last_c[0]:.0%}")
print(f"    国债ETF: {last_c[1]:.0%}")
print(f"    动量ETF: {last_c[2]:.0%}")
print(f"    现金: {(1 - sum(last_c)):.0%}")

print("\n验证完成!")
