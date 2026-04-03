"""
任务02：二板接力买入信号详细测试
RiceQuant Notebook格式
测试周期：2024年（简化测试）
"""

print("=" * 80)
print("任务02：二板接力买入信号详细测试")
print("=" * 80)

import numpy as np

# 测试参数
TEST_YEAR = 2024
CAP_MIN = 5  # 亿
CAP_MAX = 15  # 亿
ZT_THRESHOLD = 30  # 涨停数阈值

print(f"\n测试参数:")
print(f"  测试年份: {TEST_YEAR}")
print(f"  市值区间: {CAP_MIN}-{CAP_MAX}亿")
print(f"  情绪阈值: 涨停数 >= {ZT_THRESHOLD}")

# 获取交易日
print(f"\n获取{TEST_YEAR}年交易日...")
try:
    trading_days = get_trading_dates(f"{TEST_YEAR}-01-01", f"{TEST_YEAR}-12-31")
    print(f"交易日数: {len(trading_days)}")
except Exception as e:
    print(f"获取交易日失败: {e}")
    trading_days = []

if len(trading_days) == 0:
    print("无交易日，测试终止")
else:
    print(f"\n开始回测...（测试前30天）")

    # 结果存储
    all_trades = []
    emotion_stats = []

    # 只测试前30个交易日
    test_days = min(30, len(trading_days) - 1)

    for i in range(test_days):
        date = trading_days[i]

        # 进度
        if i % 5 == 0:
            print(f"\n[{i + 1}/{test_days}] 处理: {date}")

        try:
            # 获取所有股票（DataFrame格式）
            all_inst = all_instruments("CS")
            stock_list = all_inst["order_book_id"].tolist()

            # 过滤：排除科创板(68)、北交所(4,8)
            stocks = [
                s
                for s in stock_list
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ]

            # 统计涨停数（简化：只检查前200只）
            zt_count = 0
            zt_stocks = []

            for stock in stocks[:200]:
                try:
                    bars = history_bars(
                        stock, 1, "1d", ["close", "limit_up"], end_date=date
                    )
                    if bars is not None and len(bars) > 0:
                        if bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99:
                            zt_count += 1
                            zt_stocks.append(stock)
                except:
                    pass

            # 情绪过滤
            if zt_count < ZT_THRESHOLD:
                if i % 5 == 0:
                    print(f"  情绪不达标: 涨停{zt_count}只 < {ZT_THRESHOLD}")
                emotion_stats.append(
                    {"date": date, "zt_count": zt_count, "passed": False}
                )
                continue

            emotion_stats.append({"date": date, "zt_count": zt_count, "passed": True})

            # 找二板股票
            candidates = []
            for stock in zt_stocks[:50]:  # 限制检查数量
                try:
                    # 检查是否是二板：昨日涨停，前天也涨停
                    bars = history_bars(
                        stock, 3, "1d", ["close", "limit_up"], end_date=date
                    )
                    if bars is None or len(bars) < 3:
                        continue

                    # 昨天涨停
                    yesterday_zt = bars[-1]["close"] >= bars[-1]["limit_up"] * 0.99
                    # 前天涨停
                    prev_zt = bars[-2]["close"] >= bars[-2]["limit_up"] * 0.99

                    if yesterday_zt and prev_zt:
                        # 获取市值（简化）
                        try:
                            q = query(valuation).filter(valuation.code == stock)
                            df = get_fundamentals(q, date=date)
                            if df is not None and len(df) > 0:
                                cap = df.iloc[0]["circulating_market_cap"]
                                if CAP_MIN <= cap <= CAP_MAX:
                                    candidates.append((stock, bars[-1]["limit_up"]))
                        except:
                            pass
                except:
                    pass

            if len(candidates) == 0:
                continue

            # 取第一只（简化）
            target, limit_up = candidates[0]

            # 次日开盘买入
            next_date = trading_days[i + 1]
            next_bars = history_bars(
                target, 1, "1d", ["open", "high", "close"], end_date=next_date
            )

            if next_bars is None or len(next_bars) == 0:
                continue

            open_price = next_bars[-1]["open"]
            high_price = next_bars[-1]["high"]
            close_price = next_bars[-1]["close"]

            # 检查开盘涨停（无法买入）
            if open_price >= limit_up * 0.99:
                print(f"  {target}: 开盘涨停，跳过")
                continue

            # 计算收益（考虑滑点0.5%）
            buy_price = open_price * 1.005
            profit = (close_price / buy_price - 1) * 100
            max_profit = (high_price / buy_price - 1) * 100

            all_trades.append(
                {
                    "date": date,
                    "stock": target,
                    "buy_price": buy_price,
                    "sell_price": close_price,
                    "profit": profit,
                    "max_profit": max_profit,
                    "zt_count": zt_count,
                }
            )

            if i % 5 == 0:
                print(
                    f"  买入 {target}: 买价{buy_price:.2f}, 卖价{close_price:.2f}, 收益{profit:.2f}%"
                )

        except Exception as e:
            if i % 5 == 0:
                print(f"  错误: {e}")
            continue

    # 汇总结果
    print("\n" + "=" * 80)
    print("回测结果汇总")
    print("=" * 80)

    if len(all_trades) > 0:
        trades_df = pd.DataFrame(all_trades)

        total_trades = len(trades_df)
        wins = len(trades_df[trades_df["profit"] > 0])
        win_rate = wins / total_trades * 100

        avg_profit = trades_df["profit"].mean()
        avg_max_profit = trades_df["max_profit"].mean()

        cumulative = trades_df["profit"].cumsum()
        peak = np.maximum.accumulate(cumulative)
        max_dd = np.max(peak - cumulative)

        # 盈亏比
        wins_list = trades_df[trades_df["profit"] > 0]["profit"]
        losses_list = trades_df[trades_df["profit"] <= 0]["profit"]
        avg_win = wins_list.mean() if len(wins_list) > 0 else 0
        avg_loss = abs(losses_list.mean()) if len(losses_list) > 0 else 1
        pl_ratio = avg_win / avg_loss if avg_loss > 0 else 0

        # 年化（基于30天估算全年）
        days_traded = test_days
        annual_return = trades_df["profit"].sum() / days_traded * 250

        print(f"\n【总体统计】")
        print(f"  测试天数: {days_traded}")
        print(f"  信号数: {len(emotion_stats)}")
        print(f"  通过情绪: {sum(1 for e in emotion_stats if e['passed'])}")
        print(f"  交易次数: {total_trades}")
        print(f"  胜率: {win_rate:.2f}%")
        print(f"  平均收益: {avg_profit:.2f}%")
        print(f"  平均最大收益: {avg_max_profit:.2f}%")
        print(f"  盈亏比: {pl_ratio:.2f}")
        print(f"  累计收益: {cumulative.iloc[-1]:.2f}%")
        print(f"  最大回撤: {max_dd:.2f}%")
        print(f"  预估年化: {annual_return:.2f}%")

        print(f"\n【月度统计】")
        trades_df["month"] = pd.to_datetime(trades_df["date"]).dt.month
        monthly = trades_df.groupby("month").agg({"profit": ["count", "sum", "mean"]})
        print(monthly)

        # 判定
        print(f"\n【策略判定】")
        if win_rate >= 70 and annual_return >= 100:
            print("✅ 策略逻辑验证通过")
            print("建议：进入完整回测（2021-2024全量数据）")
        elif win_rate >= 60:
            print("⚠️ 策略表现中等，建议优化参数")
        else:
            print("❌ 策略表现不佳，需要调整")

    else:
        print("\n无交易记录")
        print("\n【情绪统计】")
        if len(emotion_stats) > 0:
            passed = sum(1 for e in emotion_stats if e["passed"])
            print(f"情绪达标天数: {passed}/{len(emotion_stats)}")
            avg_zt = np.mean([e["zt_count"] for e in emotion_stats])
            print(f"平均涨停数: {avg_zt:.1f}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
print("\n下一步：")
print("1. 如通过 → 使用 RiceQuant 策略编辑器完整回测（2021-2024）")
print("2. 如需优化 → 调整市值区间/情绪阈值重新测试")
print("3. 最终验证 → JoinQuant Strategy")
