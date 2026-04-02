# 首板低开策略 - Notebook 版本

print("=== 首板低开策略测试 ===")

# 1. 获取股票池
print("\n步骤1: 获取股票池")
hs300 = index_components("000300.XSHG")
zz500 = index_components("000905.XSHG")
stocks = list(set(hs300) | set(zz500))
stocks = [s for s in stocks if not s.startswith("688")]
print(f"初始股票池: {len(stocks)} 只")

# 2. 寻找昨日涨停股票
print("\n步骤2: 寻找昨日涨停股票")
limit_up_stocks = []

for stock in stocks[:100]:  # 限制数量
    try:
        bars = history_bars(stock, 2, "1d", ["close", "limit_up"])
        if bars is not None and len(bars) >= 2:
            close = bars["close"][-2]
            limit_up = bars["limit_up"][-2]

            # 判断是否涨停
            if abs(close - limit_up) < 0.01:
                limit_up_stocks.append(stock)
                print(f"发现涨停: {stock}")

            if len(limit_up_stocks) >= 10:
                break
    except:
        pass

print(f"\n发现涨停股票: {len(limit_up_stocks)} 只")

# 3. 显示结果
print("\n=== 筛选结果 ===")
print(f"昨日涨停股票: {limit_up_stocks}")
print("\n策略执行完成！")
print("\n提示: 完整策略需要检查今日开盘是否低开3-4%")
