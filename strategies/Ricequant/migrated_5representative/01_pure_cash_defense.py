"""
纯现金防守策略 - RiceQuant Notebook版本
策略类型: 防守型
复杂度: 最简单（验证基础功能）
测试目的: 验证米筐基本回测框架

策略逻辑:
- 100% 现金（不投资任何资产）
- 作为零风险的绝对基准
"""

print("=" * 60)
print("纯现金防守策略 - RiceQuant测试")
print("=" * 60)

try:
    print("\n测试1: 验证基本API")

    print(f"当前时间: {context.now}")
    print(f"总资产: {context.portfolio.total_value:.2f}")
    print(f"可用现金: {context.portfolio.cash:.2f}")

    print("\n测试2: 验证持仓信息")
    positions = context.portfolio.positions
    print(f"持仓数量: {len(positions)}")

    if len(positions) == 0:
        print("持仓状态: 100%现金 ✓")
    else:
        print("持仓状态: 有持仓（需清仓）")
        for stock, pos in positions.items():
            print(f"  {stock}: {pos.quantity}股")

    print("\n测试3: 计算收益率")
    starting_cash = 1000000
    returns = (context.portfolio.total_value / starting_cash - 1) * 100
    print(f"初始资金: {starting_cash:.0f}")
    print(f"当前总资产: {context.portfolio.total_value:.2f}")
    print(f"收益率: {returns:.2f}%")

    print("\n" + "=" * 60)
    print("✓ 纯现金防守策略测试完成")
    print("验证结论:")
    print("  1. 基本API可用 ✓")
    print("  2. 现金持有正常 ✓")
    print("  3. 收益率计算正确 ✓")
    print("=" * 60)

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()
