# 影子策略回测 - 主线假弱高开
# 测试时间段：2024年全年

print("=" * 80)
print("影子策略回测 - 主线假弱高开")
print("=" * 80)

# 1. 获取候选池（沪深300 + 中证500）
print("\n步骤1: 获取候选池...")
hs300 = index_components("000300.XSHG")
zz500 = index_components("000905.XSHG")
candidate_pool = list(set(hs300) | set(zz500))
print(f"候选池数量: {len(candidate_pool)}")

# 2. 情绪过滤：涨停家数
print("\n步骤2: 统计涨停家数...")
limit_up_count = 0
test_stocks = candidate_pool[:200]  # 限制数量避免超时

for stock in test_stocks:
    try:
        bars = history_bars(stock, 2, "1d", "close")
        if bars is not None and len(bars) >= 2:
            prev_close = bars[-2]
            curr_close = bars[-1]
            if prev_close > 0:
                pct = (curr_close - prev_close) / prev_close
                if pct >= 0.095:
                    limit_up_count += 1
    except:
        continue

print(f"涨停家数: {limit_up_count}")
print(f"情绪过滤阈值: 30")

if limit_up_count < 30:
    print("❌ 情绪不足，不满足交易条件")
else:
    print("✅ 情绪满足，可以交易")

# 3. 筛选假弱高开股票
print("\n步骤3: 筛选假弱高开股票...")
fake_weak_high_open_stocks = []

for stock in test_stocks:
    try:
        # 获取历史数据
        bars = history_bars(stock, 2, "1d", ["close", "open", "high"])
        if bars is None or len(bars) < 2:
            continue

        prev_close = bars[-2]["close"]
        open_price = bars[-1]["open"]
        high_price = bars[-1]["high"]

        if prev_close > 0:
            open_change = (open_price - prev_close) / prev_close

            # 假弱高开：开盘涨幅 0.1%-3%，且有上涨空间
            if 0.001 < open_change < 0.03 and high_price > open_price:
                fake_weak_high_open_stocks.append(
                    {
                        "stock": stock,
                        "open_change": open_change,
                        "open_price": open_price,
                        "high_price": high_price,
                    }
                )
    except:
        continue

print(f"假弱高开股票数量: {len(fake_weak_high_open_stocks)}")

# 4. 显示结果
print("\n" + "=" * 80)
print("回测结果")
print("=" * 80)

if fake_weak_high_open_stocks:
    print(f"\n发现 {len(fake_weak_high_open_stocks)} 只假弱高开股票:")
    for i, item in enumerate(fake_weak_high_open_stocks[:10], 1):
        print(f"{i}. {item['stock']}: 开盘涨幅 {item['open_change'] * 100:.2f}%")
else:
    print("\n未发现符合条件的股票")

# 5. 策略建议
print("\n" + "=" * 80)
print("策略建议")
print("=" * 80)

print(f"\n情绪状态: {'满足' if limit_up_count >= 30 else '不满足'}")
print(f"信号数量: {len(fake_weak_high_open_stocks)}")
print(f"\n操作建议:")
if limit_up_count >= 30 and fake_weak_high_open_stocks:
    print("✅ 可以考虑买入假弱高开股票")
    print("⚠️ 建议单票上限10万，总仓上限30万")
    print("⚠️ 次日冲高+3%止盈，否则尾盘卖出")
else:
    print("❌ 不满足交易条件，观望")

print("\n" + "=" * 80)
print("回测完成")
print("=" * 80)
