"""
RiceQuant 平台因子测试 - 使用平台提供的现成因子
"""

print("=" * 80)
print("RiceQuant 平台因子查询示例")
print("=" * 80)

# ============================================================================
# 第一部分：财务因子（fundamentals）
# ============================================================================

print("\n【财务因子】使用 get_fundamentals() 查询")
print("-" * 80)

# 示例1：市值因子
print("\n1. 市值因子（market_cap）")
print("   代码: fundamentals.eod_market_cap")
print("   说明: 流通市值")

try:
    stock = "000001.XSHE"
    cap_data = get_fundamentals(
        query(fundamentals.eod_market_cap).filter(fundamentals.stockcode == stock),
        "2024-12-31"
    )
    if cap_data:
        market_cap = cap_data["eod_market_cap"].iloc[0] / 100000000
        print(f"   示例: {stock} 流通市值 = {market_cap:.2f} 亿元")
except Exception as e:
    print(f"   错误: {e}")

# 示例2：估值因子
print("\n2. 估值因子")
print("   可用指标:")
print("   - fundamentals.eod_derivative_indicator.pe_ratio        # PE市盈率")
print("   - fundamentals.eod_derivative_indicator.pb_ratio        # PB市净率")
print("   - fundamentals.eod_derivative_indicator.turnover_rate   # 换手率")
print("   - fundamentals.eod_derivative_indicator.market_cap      # 总市值")

try:
    pe_data = get_fundamentals(
        query(fundamentals.eod_derivative_indicator.pe_ratio).filter(fundamentals.stockcode == stock),
        "2024-12-31"
    )
    if pe_data:
        pe_ratio = pe_data["pe_ratio"].iloc[0]
        print(f"   示例: {stock} PE = {pe_ratio:.2f}")
except Exception as e:
    print(f"   错误: {e}")

# 示例3：成长因子
print("\n3. 成长因子")
print("   可用指标:")
print("   - fundamentals.financial_indicator.roe                 # ROE净资产收益率")
print("   - fundamentals.financial_indicator.roa                 # ROA总资产收益率")
print("   - fundamentals.financial_indicator.inc_revenue_year     # 营收增长率")
print("   - fundamentals.financial_indicator.inc_net_profit_year  # 净利润增长率")

try:
    roe_data = get_fundamentals(
        query(fundamentals.financial_indicator.roe).filter(fundamentals.stockcode == stock),
        "2024-12-31"
    )
    if roe_data:
        roe = roe_data["roe"].iloc[0]
        print(f"   示例: {stock} ROE = {roe:.2f}%")
except Exception as e:
    print(f"   错误: {e}")

# ============================================================================
# 第二部分：技术因子（需要计算但有现成API）
# ============================================================================

print("\n【技术因子】使用 RiceQuant API 快速获取")
print("-" * 80)

# 示例1：价格数据（可直接获取）
print("\n1. 价格因子（get_price / history_bars）")
print("   可用字段:")
print("   - open      开盘价")
print("   - close     收盘价")
print("   - high      最高价")
print("   - low       最低价")
print("   - volume    成交量")
print("   - total_turnover  成交额")
print("   - limit_up  涨停价")
print("   - limit_down 跌停价")

try:
    bars = history_bars(stock, 5, "1d", ["close", "volume", "limit_up"])
    if bars:
        print(f"   示例: {stock} 最近5天收盘价")
        for i, bar in enumerate(bars):
            print(f"   - 第{i+1}天: {bar['close']:.2f}, 成交量={bar['volume']:.0f}")
except Exception as e:
    print(f"   错误: {e}")

# 示例2：涨停判断（有现成数据）
print("\n2. 涨跌停因子")
print("   代码: history_bars(..., ['limit_up', 'limit_down'])")
print("   说明: 直接获取涨停价、跌停价，无需计算")

# ============================================================================
# 第三部分：RiceQuant 因子库（高级因子）
# ============================================================================

print("\n【RiceQuant 因子库】专业量化因子")
print("-" * 80)

print("\n⚠️  RiceQuant 还提供了更专业的因子库（需要付费或高级账户）")
print("\n可用的高级因子类别:")
print("1. 动量因子")
print("   - momentum_1m   # 1个月动量")
print("   - momentum_3m   # 3个月动量")
print("   - momentum_6m   # 6个月动量")
print("   - momentum_12m  # 12个月动量")

print("\n2. 波动率因子")
print("   - volatility_1m   # 1个月波动率")
print("   - volatility_3m   # 3个月波动率")

print("\n3. 估值因子")
print("   - pe_ttm          # PE TTM")
print("   - pb_ttm          # PB TTM")
print("   - ps_ttm          # PS TTM")

print("\n4. 流动性因子")
print("   - turnover_rate   # 换手率")
print("   - liquidity_score # 流动性评分")

print("\n5. 技术因子")
print("   - ma_5            # 5日均线")
print("   - ma_10           # 10日均线")
print("   - ma_20           # 20日均线")
print("   - ema_12          # 12日EMA")
print("   - ema_26          # 26日EMA")
print("   - macd            # MACD")
print("   - rsi_14          # RSI")

print("\n6. 财务质量因子")
print("   - gross_profit_margin   # 毛利率")
print("   - net_profit_margin     # 净利率")
print("   - operating_margin      # 营业利润率")
print("   - debt_to_asset_ratio   # 资产负债率")

# ============================================================================
# 第四部分：对比：平台因子 vs 自定义因子
# ============================================================================

print("\n【对比】平台因子 vs 自定义计算")
print("-" * 80)

print("\n📊 市值因子对比:")
print("   ✅ 平台提供: fundamentals.eod_market_cap（直接查询）")
print("   ❌ 自己计算: 需要 市值 = 股价 * 流通股本（需要额外查询）")

print("\n📊 PE因子对比:")
print("   ✅ 平台提供: fundamentals.eod_derivative_indicator.pe_ratio（直接查询）")
print("   ❌ 自己计算: 需要 PE = 市值 / 净利润（需要多个数据源）")

print("\n📊 动量因子对比:")
print("   ✅ 平台提供: momentum_1m（高级账户）")
print("   ⚠️  自己计算: (close[-1] / close[-20] - 1)（可以，但麻烦）")

print("\n📊 技术因子对比:")
print("   ✅ 平台提供: ma_20, rsi_14（高级账户）")
print("   ⚠️  自己计算: 使用 numpy/pandas 计算（可行）")

# ============================================================================
# 第五部分：最佳实践建议
# ============================================================================

print("\n【最佳实践】如何选择因子来源")
print("-" * 80)

print("\n✅ 优先使用平台因子（免费）:")
print("   1. fundamentals.eod_market_cap          # 市值")
print("   2. fundamentals.eod_derivative_indicator.pe_ratio  # PE")
print("   3. fundamentals.eod_derivative_indicator.pb_ratio  # PB")
print("   4. fundamentals.eod_derivative_indicator.turnover_rate  # 换手率")
print("   5. fundamentals.financial_indicator.roe  # ROE")
print("   6. history_bars(..., ['limit_up'])       # 涨停价")

print("\n⚠️  需要自己计算的因子:")
print("   1. 涨停判断: close >= limit_up * 0.995")
print("   2. 开盘涨幅: (open - prev_close) / prev_close")
print("   3. 量比: mean(volume[-5:]) / mean(volume)")
print("   4. 价格位置: (close - min) / (max - min)")

print("\n💰 付费因子库（高级账户）:")
print("   1. momentum系列")
print("   2. volatility系列")
print("   3. 技术指标（MACD, RSI, KDJ等）")

print("\n💡 建议:")
print("   - 优先使用平台提供的财务因子和估值因子")
print("   - 技术因子可以使用 history_bars 数据自己计算")
print("   - 如果有高级账户，使用因子库更方便")

# ============================================================================
# 第六部分：完整示例代码
# ============================================================================

print("\n【完整示例】多因子选股")
print("-" * 80)

print("\n示例代码:")
print("""
# 使用平台因子进行选股
stocks = index_components("000300.XSHG")[:50]

for stock in stocks:
    # 1. 获取平台财务因子
    cap_data = get_fundamentals(
        query(fundamentals.eod_market_cap).filter(fundamentals.stockcode == stock),
        context.now
    )
    market_cap = cap_data["eod_market_cap"].iloc[0] / 100000000
    
    # 2. 获取平台估值因子
    pe_data = get_fundamentals(
        query(fundamentals.eod_derivative_indicator.pe_ratio).filter(fundamentals.stockcode == stock),
        context.now
    )
    pe_ratio = pe_data["pe_ratio"].iloc[0]
    
    # 3. 获取价格数据（需要简单计算）
    bars = history_bars(stock, 20, "1d", ["close"])
    momentum = (bars["close"][-1] / bars["close"][0] - 1) * 100
    
    # 4. 综合评分
    score = 0
    if market_cap < 100:  # 小市值偏好
        score += 2
    if pe_ratio < 20:  # 低估值偏好
        score += 2
    if momentum > 5:  # 动量偏好
        score += 2
"")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)

print("\n结论:")
print("✅ RiceQuant 平台提供了大量现成的财务、估值因子")
print("✅ 可以直接查询使用，无需自己计算")
print("⚠️  技术因子（动量、均线等）可以用 history_bars 自己计算")
print("💰 高级因子库（动量、波动率、MACD等）需要付费账户")
print("\n建议：优先使用平台因子，提高效率和准确性！")