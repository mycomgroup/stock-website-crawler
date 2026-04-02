print("=== 防守底仓策略测试开始 ===")

try:
    # 测试日期 - 使用最近的交易日
    date = "2026-03-27"
    print(f"测试日期: {date}")

    # 我们优化后的防守底仓策略ETF列表
    target_etfs = {
        "511010.XSHG": 0.75,  # 国债ETF 75%
        "518880.XSHG": 0.10,  # 黄金ETF 10%
        "510880.XSHG": 0.08,  # 红利ETF 8%
        "513100.XSHG": 0.04,  # 纳指ETF 4%
    }

    # 获取所有基金列表
    all_securities = get_all_securities("fund", date)
    print(f"基金总数: {len(all_securities)}")

    # 检查我们策略中的ETF是否存在
    available_etfs = {}
    missing_etfs = []

    for etf, weight in target_etfs.items():
        if etf in all_securities.index:
            available_etfs[etf] = weight
            print(f"✓ {etf} 可用 (目标权重: {weight * 100}%)")
        else:
            missing_etfs.append(etf)
            print(f"✗ {etf} 不可用 (目标权重: {weight * 100}%)")

    if not available_etfs:
        print("错误: 没有可用的ETF")
        exit(1)

    # 获取价格数据 - 最近5天用于计算收益
    print("\n获取价格数据...")
    price_data = get_price(
        list(available_etfs.keys()),
        end_date=date,
        count=5,
        fields=["close"],
        panel=False,
    )
    print(f"价格数据条数: {len(price_data)}")

    # 显示最新价格和计算收益
    if len(price_data) > 0:
        # 按ETF分组获取最新价格
        latest_prices = price_data.groupby("code").last()
        earliest_prices = price_data.groupby("code").first()

        print("\nETF价格信息:")
        total_weighted_return = 0
        total_weight = 0

        for etf, weight in available_etfs.items():
            if etf in latest_prices.index and etf in earliest_prices.index:
                latest_close = latest_prices.loc[etf, "close"]
                earliest_close = earliest_prices.loc[etf, "close"]
                etf_return = (latest_close / earliest_close - 1) * 100
                weighted_return = etf_return * weight

                print(f"{etf}:")
                print(f"  最新价: {latest_close:.4f}")
                print(f"  最早价: {earliest_close:.4f}")
                print(f"  5天收益: {etf_return:.2f}%")
                print(f"  加权收益: {weighted_return:.2f}%")

                total_weighted_return += weighted_return
                total_weight += weight
            else:
                print(f"{etf}: 价格数据不完整")

        if total_weight > 0:
            annualized_return = total_weighted_return * (252 / 5)  # 简单年化
            print(f"\n策略5天总收益: {total_weighted_return:.2f}%")
            print(f"策略年化收益 (简单估算): {annualized_return:.2f}%")

    # 显示当前持仓建议
    print("\n=== 防守底仓策略建议持仓 (30%总仓位) ===")
    for etf, weight in available_etfs.items():
        actual_alloc = weight * 0.30  # 30%总仓位中的分配
        print(f"{etf}: {weight * 100:.0f}%策略权重 → {actual_alloc * 100:.1f}%总资金")

    cash_allocation = (1 - sum(available_etfs.values())) * 0.30
    print(f"现金/货基: {cash_allocation * 100:.1f}%总资金")

    print("\n=== 测试完成 ===")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
