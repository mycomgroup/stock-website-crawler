# 龙头底分型战法 - JoinQuant Notebook格式
# 使用JoinQuant API进行涨停检测和底分型验证

print("=" * 80)
print("龙头底分型战法 - JoinQuant Notebook验证")
print("=" * 80)

import pandas as pd
import numpy as np

try:
    # 获取2024年交易日
    trading_days = get_trade_days(start_date="2024-01-01", end_date="2024-12-31")
    print(f"2024年交易日数: {len(trading_days)}")

    # 采样：每月选1个交易日
    sample_dates = []
    for month in [3, 6, 9, 12]:
        month_days = [d for d in trading_days if d.month == month]
        if len(month_days) > 0:
            mid_idx = len(month_days) // 2
            sample_dates.append(month_days[mid_idx].strftime("%Y-%m-%d"))

    print(f"采样日期: {sample_dates}")

    all_results = []

    for date in sample_dates:
        print(f"\n{'=' * 60}")
        print(f"测试日期: {date}")
        print(f"{'=' * 60}")

        # 1. 获取所有股票（排除科创板、创业板）
        try:
            stocks = list(get_all_securities(["stock"], date).index)
            stocks = [
                s for s in stocks if not (s.startswith("68") or s.startswith("300"))
            ]
            print(f"股票池大小: {len(stocks)}")
        except Exception as e:
            print(f"获取股票池失败: {e}")
            continue

        # 2. 筛选涨停股票
        try:
            # 批量获取涨停价和收盘价
            df = get_price(
                stocks,
                end_date=date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
                fill_paused=False,
            )

            if df.empty:
                print("无行情数据")
                continue

            # 涨停股票：收盘价>=涨停价*99.5%
            limit_up_df = df[df["close"] >= df["high_limit"] * 0.995]
            limit_up_stocks = limit_up_df["code"].tolist()

            print(f"涨停股票数: {len(limit_up_stocks)}")

            if len(limit_up_stocks) == 0:
                print("无涨停股票，跳过")
                continue

            # 显示涨停股示例
            if len(limit_up_stocks) > 0:
                print(f"涨停股示例（前10只）:")
                for s in limit_up_stocks[:10]:
                    row = limit_up_df[limit_up_df["code"] == s].iloc[0]
                    print(
                        f"  {s}: close={row['close']:.2f}, high_limit={row['high_limit']:.2f}"
                    )

        except Exception as e:
            print(f"筛选涨停失败: {e}")
            import traceback

            traceback.print_exc()
            continue

        # 3. 检查底分型形态
        signals = []
        test_count = min(50, len(limit_up_stocks))  # 测试50只

        print(f"\n检查底分型（{test_count}只涨停股）...")

        for stock in limit_up_stocks[:test_count]:
            try:
                # 获取最近3天数据
                df_3 = get_price(
                    stock,
                    end_date=date,
                    count=3,
                    fields=["open", "close", "high", "low", "high_limit"],
                    panel=False,
                )

                if df_3.empty or len(df_3) < 3:
                    continue

                # 获取60日数据计算MA60
                df_60 = get_price(
                    stock, end_date=date, count=60, fields=["close"], panel=False
                )

                if df_60.empty or len(df_60) < 60:
                    continue

                ma60 = df_60["close"].mean()

                # T-2日（十字星）- 倒数第2行
                t2 = df_3.iloc[-2]
                t2_close = t2["close"]
                t2_open = t2["open"]
                t2_high = t2["high"]
                t2_low = t2["low"]

                body_ratio = abs(t2_close - t2_open) / ((t2_close + t2_open) / 2)
                swing_ratio = abs(t2_high - t2_low) / ((t2_high + t2_low) / 2)

                # T-1日（涨停）- 倒数第1行
                t1 = df_3.iloc[-1]
                t1_close = t1["close"]
                t1_open = t1["open"]
                t1_high_limit = t1["high_limit"]

                # 底分型条件
                is_doji = body_ratio < 0.03 and swing_ratio < 0.10
                above_ma60 = t2_close > ma60
                is_limit_up = t1_close >= t1_high_limit * 0.995
                gap_up = t1_open > t2_close * 1.02
                strong_close = t1_close > t2_close * 1.05

                if is_doji and above_ma60 and is_limit_up and gap_up and strong_close:
                    return_pct = (t1_close / t2_close - 1) * 100
                    signals.append(
                        {
                            "stock": stock,
                            "date": date,
                            "t2_close": t2_close,
                            "t1_close": t1_close,
                            "return_pct": return_pct,
                            "body_ratio": body_ratio,
                            "swing_ratio": swing_ratio,
                        }
                    )
                    print(
                        f"  ✓ {stock}: T-2收{t2_close:.2f} T-1收{t1_close:.2f} 涨幅{return_pct:.2f}%"
                    )

            except Exception as e:
                pass

        print(f"\n信号数量: {len(signals)}")

        if len(signals) > 0:
            avg_return = np.mean([s["return_pct"] for s in signals])
            print(f"平均涨幅: {avg_return:.2f}%")
            all_results.extend(signals)
        else:
            print("未发现底分型信号")
            print("可能原因:")
            print("1. 条件过于严格")
            print("2. 该日无符合形态的股票")

    # 4. 总体统计
    print(f"\n{'=' * 80}")
    print("总体统计")
    print(f"{'=' * 80}")
    print(f"测试日期数: {len(sample_dates)}")
    print(f"总信号数: {len(all_results)}")

    if len(all_results) > 0:
        avg_return = np.mean([r["return_pct"] for r in all_results])
        max_return = np.max([r["return_pct"] for r in all_results])
        min_return = np.min([r["return_pct"] for r in all_results])

        print(f"平均涨幅: {avg_return:.2f}%")
        print(f"最大涨幅: {max_return:.2f}%")
        print(f"最小涨幅: {min_return:.2f}%")

        print(f"\n完整信号列表:")
        for r in all_results:
            print(f"  {r['stock']} @ {r['date']}: 涨幅{r['return_pct']:.2f}%")
    else:
        print("\n总结:")
        print("- 在采样的4个交易日中，未发现符合条件的底分型信号")
        print("- 原因：条件严格（十字星+涨停+高开+60日均线）")
        print("- 建议：放宽条件或增加采样日期范围")

except Exception as e:
    print(f"执行错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 80)
print("验证完成")
print("=" * 80)
