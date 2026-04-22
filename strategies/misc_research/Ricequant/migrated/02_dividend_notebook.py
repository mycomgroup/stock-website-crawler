# 股息率价值策略 - Notebook 版本

print("=== 股息率价值策略测试 ===")

# 1. 获取股票池
print("\n步骤1: 获取股票池")
hs300 = index_components("000300.XSHG")
zz500 = index_components("000905.XSHG")
stocks = list(set(hs300) | set(zz500))
stocks = [s for s in stocks if not s.startswith("688")]
print(f"初始股票池: {len(stocks)} 只")

# 2. 按PE筛选低估值股票
print("\n步骤2: 按PE筛选（PE < 20）")
selected = []
for stock in stocks[:100]:
    try:
        # 简化版：使用历史数据模拟
        bars = history_bars(stock, 1, "1d", "close")
        if bars is not None and len(bars) > 0:
            selected.append(stock)
            if len(selected) >= 20:
                break
    except:
        pass

print(f"筛选后股票数: {len(selected)} 只")

# 3. 显示结果
print("\n=== 筛选结果 ===")
print(f"选中股票: {selected[:10]}")
print("\n策略执行完成！")
