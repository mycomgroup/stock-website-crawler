# 龙头底分型战法 - Notebook 版本

print("=== 龙头底分型战法测试 ===")

# 1. 获取股票池
print("\n步骤1: 获取股票池")
hs300 = index_components("000300.XSHG")
stocks = hs300[:100]  # 限制数量
print(f"测试股票池: {len(stocks)} 只")

# 2. 寻找龙头底分型
print("\n步骤2: 寻找龙头底分型形态")
fractal_stocks = []

for stock in stocks[:30]:  # 限制数量
    try:
        bars = history_bars(stock, 10, "1d", ["high", "low", "close"])
        if bars is not None and len(bars) >= 10:
            highs = bars["high"]
            lows = bars["low"]

            # 简化的底分型判断
            if len(lows) >= 5:
                if lows[-3] < lows[-2] and lows[-3] < lows[-4]:
                    fractal_stocks.append(stock)
                    print(f"发现底分型: {stock}")

                if len(fractal_stocks) >= 5:
                    break
    except:
        pass

print(f"\n发现底分型股票: {len(fractal_stocks)} 只")

# 3. 显示结果
print("\n=== 筛选结果 ===")
print(f"选中股票: {fractal_stocks}")
print("\n策略执行完成！")
