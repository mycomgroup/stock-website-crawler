#!/usr/bin/env python
"""
新增功能使用示例
展示: 行业数据、北向资金、RSRS择时、市场情绪指标的实际应用
"""

import warnings

warnings.filterwarnings("ignore")

print("=" * 70)
print("新增功能使用示例")
print("=" * 70)

# -------------------------------------------------------
# 示例1: RSRS择时信号
# -------------------------------------------------------
print("\n【示例1】RSRS择时信号 - 沪深300指数")
print("-" * 70)

from indicators.rsrs import get_current_rsrs_signal

rsrs_signal = get_current_rsrs_signal(index_code="000300", N=18, M=600)
print(f"信号值: {rsrs_signal['signal']}")
print(f"RSRS值: {rsrs_signal['rsrs_value']:.4f}")
print(f"描述: {rsrs_signal['description']}")

# -------------------------------------------------------
# 示例2: 北向资金分析
# -------------------------------------------------------
print("\n【示例2】北向资金分析")
print("-" * 70)

from market_data.north_money import compute_north_money_signal, get_north_money_holdings

# 获取北向资金择时信号
nm_signal = compute_north_money_signal(window=20, threshold=30.0)
print(f"北向资金信号: {nm_signal['signal']}")
print(f"近20日平均净流入: {nm_signal['avg_inflow']:.2f} 亿元")
print(f"描述: {nm_signal['description']}")

# 获取北向资金持股TOP10
print("\n北向资金持股 TOP10:")
holdings = get_north_money_holdings(top_n=10)
if not holdings.empty:
    print(holdings[["code", "name", "holding_value"]].head(10).to_string(index=False))

# -------------------------------------------------------
# 示例3: 市场情绪指标
# -------------------------------------------------------
print("\n【示例3】市场情绪指标汇总")
print("-" * 70)

from indicators.market_sentiment import (
    compute_crowding_ratio,
    compute_fed_model,
    compute_graham_index,
    compute_below_net_ratio,
)

# 拥挤率
cr = compute_crowding_ratio()
print(f"拥挤率: {cr['crowding_ratio']:.2f}%")
print(f"  → {cr['description']}")

# FED模型
fed = compute_fed_model()
print(f"\nFED模型: {fed['fed_value']:.4f}")
pe_val = fed.get("pe", "N/A")
print(f"  PE: {pe_val:.2f}" if isinstance(pe_val, (int, float)) else f"  PE: {pe_val}")
print(f"  → {fed['description']}")

# 格雷厄姆指数
graham = compute_graham_index()
print(f"\n格雷厄姆指数: {graham['graham_index']:.4f}")
print(f"  → {graham['description']}")

# 破净占比
below = compute_below_net_ratio()
print(f"\n破净股占比: {below['below_net_ratio']:.2f}%")
print(f"  破净股数量: {below.get('below_net_count', 0)}")
print(f"  → {below['description']}")

# -------------------------------------------------------
# 示例4: 行业数据
# -------------------------------------------------------
print("\n【示例4】行业数据分析")
print("-" * 70)

from market_data.industry import (
    get_industry_stocks,
    get_industry_performance,
    get_market_breadth,
    SW_LEVEL1_CODES,
)

# 行业涨跌幅排名
print("行业涨跌幅 TOP5:")
perf = get_industry_performance(top_n=5)
if not perf.empty:
    print(perf[["industry_name", "pct_change"]].head(5).to_string(index=False))

# 行业成分股
print("\n电子行业成分股（前10只）:")
stocks = get_industry_stocks("电子")
print(f"共 {len(stocks)} 只股票")
print(stocks[:10])

# -------------------------------------------------------
# 示例5: 综合择时信号
# -------------------------------------------------------
print("\n【示例5】综合择时信号")
print("-" * 70)

# 综合多个指标判断
signals = []

# RSRS信号
if rsrs_signal["signal"] == 1:
    signals.append(("RSRS择时", "看多"))
elif rsrs_signal["signal"] == -1:
    signals.append(("RSRS择时", "看空"))
else:
    signals.append(("RSRS择时", "中性"))

# 北向资金信号
if nm_signal["signal"] == 1:
    signals.append(("北向资金", "流入"))
elif nm_signal["signal"] == -1:
    signals.append(("北向资金", "流出"))
else:
    signals.append(("北向资金", "中性"))

# FED模型
if fed["fed_value"] > 0:
    signals.append(("FED模型", "股票有吸引力"))
else:
    signals.append(("FED模型", "债券有吸引力"))

# 格雷厄姆指数
if graham["graham_index"] > 1.5:
    signals.append(("格雷厄姆", "低估"))
else:
    signals.append(("格雷厄姆", "合理/高估"))

# 拥挤率
if cr["crowding_ratio"] > 60:
    signals.append(("拥挤率", "过热"))
elif cr["crowding_ratio"] < 40:
    signals.append(("拥挤率", "可能见底"))
else:
    signals.append(("拥挤率", "正常"))

print("指标信号汇总:")
for name, signal in signals:
    print(f"  {name:12s}: {signal}")

# 计算综合得分
bullish = sum(
    1 for _, s in signals if s in ["看多", "流入", "股票有吸引力", "低估", "可能见底"]
)
bearish = sum(1 for _, s in signals if s in ["看空", "流出", "债券有吸引力", "过热"])

print(f"\n综合判断: {bullish} 个看多信号, {bearish} 个看空信号")
if bullish > bearish:
    print("结论: 综合偏多")
elif bearish > bullish:
    print("结论: 综合偏空")
else:
    print("结论: 中性")

# -------------------------------------------------------
# 示例6: qlib Alpha因子（可选）
# -------------------------------------------------------
print("\n【示例6】Alpha因子 (需要配置qlib数据源)")
print("-" * 70)

try:
    from factors.qlib_alpha import QLIB_AVAILABLE, init_qlib

    if QLIB_AVAILABLE:
        print("qlib 已安装，使用方法:")
        print("  from factors.qlib_alpha import compute_alpha101")
        print("  alpha = compute_alpha101(['sh600519'], factors=['alpha001'])")
        print("\n注意: 需要先运行 'python -m qlib.init' 初始化数据")
    else:
        print("qlib 未安装或不可用")
except Exception as e:
    print(f"qlib 模块导入失败: {e}")

print("\n" + "=" * 70)
print("示例完成")
print("=" * 70)
