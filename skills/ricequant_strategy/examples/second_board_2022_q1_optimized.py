"""
二板接力 2022年Q1测试 - 优化版
测试范围：2022-01-01 至 2022-03-31
优化：减少API调用，提升速度
"""

print("=" * 80)
print("二板接力 2022年Q1测试（优化版）")
print("=" * 80)

try:
    import pandas as pd
    import numpy as np

    print("✓ 导入依赖成功")

    start_date = "2022-01-01"
    end_date = "2022-03-31"

    print(f"\n测试范围: {start_date} 至 {end_date}")

    # 获取交易日
    all_dates = get_trading_dates(start_date, end_date)
    print(f"交易日数: {len(all_dates)}")

    # 预先获取所有股票列表
    all_stocks_list = [s for s in get_all_securities(["stock"]).index.tolist()]
    all_stocks_list = [
        s
        for s in all_stocks_list
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    all_stocks_list = all_stocks_list[:300]  # 限制为300只，提升速度
    print(f"测试股票数: {len(all_stocks_list)}")

    signals = []

    # 批量获取价格数据，减少API调用
    print("\n批量获取价格数据...")

    for i in range(2, min(len(all_dates), 40)):  # 限制前40天
        prev_prev = all_dates[i - 2]
        prev = all_dates[i - 1]
        curr = all_dates[i]

        if i % 10 == 0:
            print(f"处理第{i}天: {prev} -> {curr}")

        try:
            # 批量获取三日数据
            price_data = get_price(
                all_stocks_list,
                start_date=prev_prev,
                end_date=curr,
                frequency="1d",
                fields=["close", "limit_up", "open"],
                adjust_orig=None,
            )

            if price_data.empty:
                continue

            # 分析涨停股票
            zt_stocks = []
            for stock in all_stocks_list:
                try:
                    # 检查前一日是否涨停
                    prev_close = price_data.loc[prev, (stock, "close")]
                    prev_limit = price_data.loc[prev, (stock, "limit_up")]

                    if abs(prev_close - prev_limit) / prev_limit < 0.01:
                        # 检查前前一日是否涨停
                        pp_close = price_data.loc[prev_prev, (stock, "close")]
                        pp_limit = price_data.loc[prev_prev, (stock, "limit_up")]

                        if abs(pp_close - pp_limit) / pp_limit < 0.01:
                            zt_stocks.append(stock)
                except:
                    continue

            if i % 10 == 0:
                print(f"  二板候选数: {len(zt_stocks)}")

            # 模拟交易
            for stock in zt_stocks[:20]:  # 限制前20只
                try:
                    curr_open = price_data.loc[curr, (stock, "open")]
                    curr_close = price_data.loc[curr, (stock, "close")]
                    curr_limit = price_data.loc[curr, (stock, "limit_up")]

                    # 涨停开盘跳过
                    if abs(curr_open - curr_limit) / curr_limit < 0.01:
                        continue

                    ret = (curr_close - curr_open) / curr_open * 100
                    signals.append(
                        {
                            "date": str(curr),
                            "stock": stock,
                            "return": ret,
                            "win": ret > 0,
                        }
                    )
                except:
                    continue
        except Exception as e:
            if i % 10 == 0:
                print(f"  错误: {e}")
            continue

    # 统计结果
    print("\n" + "=" * 80)
    print("2022年Q1测试结果")
    print("=" * 80)

    if len(signals) > 0:
        df = pd.DataFrame(signals)
        print(f"信号数: {len(df)}")
        print(f"平均收益: {df['return'].mean():.2f}%")
        print(f"胜率: {df['win'].sum() / len(df) * 100:.1f}%")
        print(f"最大收益: {df['return'].max():.2f}%")
        print(f"最大亏损: {df['return'].min():.2f}%")
    else:
        print("无信号")

    print("\n✓ 2022年Q1测试完成")

except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback

    traceback.print_exc()

print("=" * 80)
