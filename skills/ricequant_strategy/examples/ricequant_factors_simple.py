"""
RiceQuant 平台因子查询示例 - 简化版
"""

print("=" * 80)
print("RiceQuant 平台因子测试")
print("=" * 80)

# ============================================================================
# 第一部分：财务因子（fundamentals）- 平台直接提供
# ============================================================================

print("\n【财务因子】平台直接提供，无需计算")
print("-" * 80)

# 1. 市值因子
print("\n1. 市值因子（直接查询）")
print("   API: fundamentals.eod_market_cap")

# 2. 估值因子
print("\n2. 估值因子（直接查询）")
print("   - fundamentals.eod_derivative_indicator.pe_ratio      # PE市盈率")
print("   - fundamentals.eod_derivative_indicator.pb_ratio      # PB市净率")
print("   - fundamentals.eod_derivative_indicator.turnover_rate # 换手率")

# 3. 成长因子
print("\n3. 成长因子（直接查询）")
print("   - fundamentals.financial_indicator.roe                # ROE")
print("   - fundamentals.financial_indicator.roa                # ROA")
print("   - fundamentals.financial_indicator.inc_revenue_year   # 营收增长")

# ============================================================================
# 第二部分：价格因子 - 有现成数据
# ============================================================================

print("\n【价格因子】平台提供原始数据")
print("-" * 80)

print("\n可用字段（history_bars / get_price）:")
print("   - open         开盘价")
print("   - close        收盘价")
print("   - high         最高价")
print("   - low          最低价")
print("   - volume       成交量")
print("   - limit_up     涨停价（重要！）")
print("   - limit_down   跌停价")

# ============================================================================
# 第三部分：需要自己计算的因子
# ============================================================================

print("\n【需要简单计算的因子】")
print("-" * 80)

print("\n虽然平台提供了原始数据，但以下因子需要自己计算:")
print("   1. 涨停判断: close >= limit_up * 0.995")
print("   2. 开盘涨幅: (open - prev_close) / prev_close")
print("   3. 动量因子: (close[-1] / close[-20] - 1) * 100")
print("   4. 量比: mean(volume[-5:]) / mean(volume)")

# ============================================================================
# 第四部分：对比总结
# ============================================================================

print("\n【对比】平台因子 vs 自己计算")
print("-" * 80)

print("\n✅ 平台直接提供（推荐使用）:")
print("   财务因子: 市值、PE、PB、ROE、营收增长...")
print("   价格数据: 开盘、收盘、涨停价、跌停价...")
print("   估值因子: 换手率、市盈率、市净率...")

print("\n⚠️  需要自己计算:")
print("   技术指标: 动量、均线、MACD、RSI...")
print("   组合因子: 开盘涨幅、涨停判断...")

print("\n💡 最佳实践:")
print("   1. 优先使用平台财务因子（更准确、更高效）")
print("   2. 价格因子使用 history_bars 获取原始数据")
print("   3. 技术因子可以自己计算（numpy/pandas）")
print("   4. 避免重复造轮子，善用平台能力")

print("\n" + "=" * 80)
print("结论: RiceQuant 提供了丰富的财务和估值因子，无需自己计算！")
print("=" * 80)
