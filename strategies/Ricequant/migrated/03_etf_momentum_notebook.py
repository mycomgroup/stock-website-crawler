# ETF动量轮动策略 - Notebook 版本

print("=== ETF动量轮动策略测试 ===")

# 定义ETF列表
etf_list = [
    "510300.XSHG",  # 沪深300ETF
    "510500.XSHG",  # 中证500ETF
    "159915.XSHE",  # 创业板ETF
    "512100.XSHG",  # 中证1000ETF
    "510050.XSHG",  # 上证50ETF
]

print(f"\n测试 ETF 列表: {len(etf_list)} 个")

# 计算动量
print("\n计算动量...")
momentum_scores = []

for etf in etf_list:
    try:
        bars = history_bars(etf, 21, "1d", "close")
        if bars is not None and len(bars) >= 21:
            momentum = (bars[-1] / bars[0] - 1) * 100
            momentum_scores.append((etf, momentum))
            print(f"{etf}: 动量 {momentum:.2f}%")
    except Exception as e:
        print(f"{etf}: 获取数据失败")

# 排序选择
if momentum_scores:
    momentum_scores.sort(key=lambda x: x[1], reverse=True)
    print("\n=== 动量排名 ===")
    for i, (etf, mom) in enumerate(momentum_scores, 1):
        print(f"{i}. {etf}: {mom:.2f}%")

    top_2 = [etf for etf, _ in momentum_scores[:2]]
    print(f"\n推荐买入: {top_2}")
else:
    print("\n无法计算动量")

print("\n策略测试完成！")
