print("=== 简化版国债固收+ 策略测试开始 ===")

try:
    # 测试日期 - 使用最近的交易日
    date = "2026-03-27"
    print(f"测试日期: {date}")

    # 获取所有股票/ETF列表
    all_securities = get_all_securities("fund", date)
    print(f"基金总数: {len(all_securities)}")

    # 检查我们策略中的ETF是否存在
    target_etfs = ["511010.XSHG", "518880.XSHG", "510880.XSHG", "513100.XSHG"]
    available_etfs = []

    for etf in target_etfs:
        if etf in all_securities.index:
            available_etfs.append(etf)
            print(f"✓ {etf} 可用")
        else:
            print(f"✗ {etf} 不可用")

    # 获取价格数据
    if available_etfs:
        print("\n获取价格数据...")
        price_data = get_price(
            available_etfs,
            end_date=date,
            count=5,
            fields=["close", "high", "low"],
            panel=False,
        )
        print(f"价格数据条数: {len(price_data)}")

        # 显示最近价格
        if len(price_data) > 0:
            latest_prices = price_data.groupby("code").last()
            print("\n最新价格:")
            for etf in target_etfs:
                if etf in latest_prices.index:
                    close_price = latest_prices.loc[etf, "close"]
                    print(f"{etf}: {close_price:.4f}")

    # 计算简单持有收益（假设持有5天）
    if len(price_data) >= 2:
        print("\n计算5天持有收益...")
        returns = {}
        for etf in target_etfs:
            etf_data = price_data[price_data["code"] == etf].sort_values("date")
            if len(etf_data) >= 2:
                start_price = etf_data.iloc[0]["close"]
                end_price = etf_data.iloc[-1]["close"]
                ret = (end_price / start_price - 1) * 100
                returns[etf] = ret
                print(f"{etf}: {ret:.2f}%")

        # 按策略权重计算组合收益
        weights = {
            "511010.XSHG": 0.75,
            "518880.XSHG": 0.10,
            "510880.XSHG": 0.08,
            "513100.XSHG": 0.04,
        }
        portfolio_return = sum(returns.get(etf, 0) * weights[etf] for etf in weights)
        print(f"\n策略5天收益: {portfolio_return:.2f}%")

    print("\n=== 测试完成 ===")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
