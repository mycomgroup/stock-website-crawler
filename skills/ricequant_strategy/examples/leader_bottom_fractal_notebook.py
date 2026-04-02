# 龙头底分型战法 - Notebook格式（RiceQuant）
# 使用真实交易日，扩大搜索范围

print("=" * 80)
print("龙头底分型战法 - Notebook验证（改进版）")
print("=" * 80)

import pandas as pd
import numpy as np

try:
    # 获取2024年的交易日
    trading_dates = get_trading_dates("2024-01-01", "2024-12-31")
    print(f"2024年交易日数: {len(trading_dates)}")

    # 采样：每月选1个交易日
    sample_dates = []
    for month in [3, 6, 9, 12]:
        month_dates = [d for d in trading_dates if d.month == month]
        if len(month_dates) > 0:
            # 取月中交易日
            mid_idx = len(month_dates) // 2
            sample_dates.append(month_dates[mid_idx])

    print(f"采样日期: {[d.strftime('%Y-%m-%d') for d in sample_dates]}")

    all_results = []

    for date in sample_dates:
        date_str = date.strftime("%Y-%m-%d")
        print(f"\n{'=' * 60}")
        print(f"测试日期: {date_str}")
        print(f"{'=' * 60}")

        # 1. 获取所有股票（排除科创板、创业板）
        try:
            all_stocks_df = all_instruments("CS", date_str)
            stocks = [
                s
                for s in all_stocks_df["order_book_id"].tolist()
                if not (s.startswith("68") or s.startswith("300"))
            ]
            print(f"股票池大小: {len(stocks)}")
        except Exception as e:
            print(f"获取股票池失败: {e}")
            continue

        # 2. 筛选涨停股票（扩大范围到500只）
        try:
            limit_up_stocks = []
            sample_size = min(500, len(stocks))

            print(f"检测涨停（采样{sample_size}只）...")

            for stock in stocks[:sample_size]:
                try:
                    bars = history_bars(stock, 1, "1d", "close,limit_up", date_str)
                    if bars is not None and len(bars) > 0:
                        # 涨停判断：收盘价>=涨停价*99.5%
                        close = bars[0]["close"]
                        limit_up = bars[0]["limit_up"]

                        if close >= limit_up * 0.995:
                            limit_up_stocks.append(
                                {
                                    "stock": stock,
                                    "close": close,
                                    "limit_up": limit_up,
                                    "pct": (close / limit_up - 1) * 100,
                                }
                            )
                except:
                    pass

            print(f"涨停股票数: {len(limit_up_stocks)}")

            if len(limit_up_stocks) > 0:
                # 显示前10个涨停股
                print("涨停股示例:")
                for i, s in enumerate(limit_up_stocks[:10]):
                    print(
                        f"  {s['stock']}: 收盘{s['close']:.2f}, 涨停价{s['limit_up']:.2f}, 涨幅{s['pct']:.2f}%"
                    )

            if len(limit_up_stocks) == 0:
                print("无涨停股票，跳过")
                continue

        except Exception as e:
            print(f"筛选涨停失败: {e}")
            import traceback

            traceback.print_exc()
            continue

        # 3. 检查底分型形态（测试所有涨停股）
        signals = []
        test_count = len(limit_up_stocks)

        print(f"\n检查底分型（{test_count}只涨停股）...")

        for lu_stock in limit_up_stocks:
            stock = lu_stock["stock"]
            try:
                # 获取最近3天数据
                bars_3 = history_bars(
                    stock, 3, "1d", "open,close,high,low,limit_up", date_str
                )
                if bars_3 is None or len(bars_3) < 3:
                    continue

                # 获取60日数据
                bars_60 = history_bars(stock, 60, "1d", "close", date_str)
                if bars_60 is None or len(bars_60) < 60:
                    continue

                ma60 = np.mean(bars_60["close"])

                # T-2日（十字星）
                t2_close = float(bars_3[1]["close"])
                t2_open = float(bars_3[1]["open"])
                t2_high = float(bars_3[1]["high"])
                t2_low = float(bars_3[1]["low"])

                body_ratio = abs(t2_close - t2_open) / ((t2_close + t2_open) / 2)
                swing_ratio = abs(t2_high - t2_low) / ((t2_high + t2_low) / 2)

                # T-1日（涨停）
                t1_close = float(bars_3[2]["close"])
                t1_open = float(bars_3[2]["open"])
                t1_limit_up = float(bars_3[2]["limit_up"])

                # 底分型条件（简化）
                is_doji = body_ratio < 0.03 and swing_ratio < 0.10
                above_ma60 = t2_close > ma60
                is_limit_up = t1_close >= t1_limit_up * 0.995
                gap_up = t1_open > t2_close * 1.02
                strong_close = t1_close > t2_close * 1.05

                if is_doji and above_ma60 and is_limit_up and gap_up and strong_close:
                    return_pct = (t1_close / t2_close - 1) * 100
                    signals.append(
                        {
                            "stock": stock,
                            "date": date_str,
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
            print(
                f"  {r['stock']} @ {r['date']}: 涨幅{r['return_pct']:.2f}% (实体{r['body_ratio']:.3f}, 振幅{r['swing_ratio']:.3f})"
            )
    else:
        print("无信号发现")
        print("可能原因:")
        print("1. 条件过于严格（十字星+涨停+高开）")
        print("2. 采样日期涨停股数量不足")
        print("3. 2024年市场环境变化，底分型形态减少")

except Exception as e:
    print(f"执行错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 80)
print("验证完成")
print("=" * 80)
