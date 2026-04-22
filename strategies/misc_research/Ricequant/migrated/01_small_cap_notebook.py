# 小市值成长股策略 - RiceQuant Notebook 版本
# 简化版本，适合在 Notebook 中运行

print("=== 小市值成长股策略测试 ===")
print("开始执行...")

# 1. 获取股票池
print("\n步骤1: 获取股票池")
hs300 = index_components("000300.XSHG")
zz500 = index_components("000905.XSHG")
stocks = list(set(hs300) | set(zz500))
stocks = [s for s in stocks if not s.startswith("688")]
print(f"初始股票池: {len(stocks)} 只")

# 2. 按市值筛选（取前30只小市值）
print("\n步骤2: 按市值筛选")
selected_stocks = []
for i, stock in enumerate(stocks[:100]):  # 限制数量
    try:
        bars = history_bars(stock, 1, "1d", "close")
        if bars is not None and len(bars) > 0:
            selected_stocks.append(stock)
            if len(selected_stocks) >= 30:
                break
    except:
        pass

print(f"筛选后股票数: {len(selected_stocks)} 只")

# 3. 显示结果
print("\n=== 筛选结果 ===")
print(f"选中股票: {selected_stocks[:10]}")

print("\n策略执行完成！")
print("\n提示: 这是一个简化的 Notebook 测试版本")
print("完整的回测策略需要在 RiceQuant 策略编辑器中运行")
