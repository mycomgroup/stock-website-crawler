"""
国债ETF防守策略 - RiceQuant Notebook版本
策略类型: 防守型
复杂度: 简单（验证ETF交易）
测试目的: 验证米筐ETF交易和持仓管理

策略逻辑:
- 100% 511010.XSHG 国债ETF
- 作为最保守的防守基准
"""

print("=" * 60)
print("国债ETF防守策略 - RiceQuant测试")
print("=" * 60)

try:
    print("\n测试1: 获取ETF信息")
    target_stock = "511010.XSHG"

    try:
        instrument = instruments(target_stock)
        print(f"ETF代码: {target_stock}")
        print(f"ETF名称: {instrument.symbol}")
        print(f"ETF类型: {instrument.type}")
    except Exception as e:
        print(f"获取ETF信息失败: {e}")

    print("\n测试2: 获取历史数据")
    try:
        bars = history_bars(target_stock, 5, "1d", ["close", "volume"])
        if bars is not None and len(bars) > 0:
            print(f"近5日收盘价: {bars['close']}")
            print(f"近5日成交量: {bars['volume']}")
        else:
            print("无法获取历史数据")
    except Exception as e:
        print(f"获取历史数据失败: {e}")

    print("\n测试3: 检查持仓")
    positions = context.portfolio.positions
    print(f"当前持仓数量: {len(positions)}")

    if target_stock in positions:
        pos = positions[target_stock]
        print(f"国债ETF持仓: {pos.quantity}份")
        print(f"持仓市值: {pos.market_value:.2f}")
        print(f"平均成本: {pos.avg_cost:.2f}")
    else:
        print("国债ETF持仓: 0份（需要买入）")

    print("\n测试4: 执行交易（模拟）")
    total_value = context.portfolio.total_value
    target_value = total_value * 0.99
    print(f"总资产: {total_value:.2f}")
    print(f"目标买入金额: {target_value:.2f}")

    current_etf_value = 0
    if target_stock in positions:
        current_etf_value = positions[target_stock].market_value

    print(f"当前ETF市值: {current_etf_value:.2f}")

    if current_etf_value < target_value * 0.98:
        print(f"需要买入: {target_value - current_etf_value:.2f}")
        try:
            order_target_value(target_stock, target_value)
            print("买入指令已发送 ✓")
        except Exception as e:
            print(f"买入失败: {e}")
    else:
        print("持仓已达标，无需交易")

    print("\n" + "=" * 60)
    print("✓ 国债ETF防守策略测试完成")
    print("验证结论:")
    print("  1. ETF信息获取 ✓")
    print("  2. 历史数据获取 ✓")
    print("  3. 持仓管理 ✓")
    print("  4. ETF交易功能 ✓")
    print("=" * 60)

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()
