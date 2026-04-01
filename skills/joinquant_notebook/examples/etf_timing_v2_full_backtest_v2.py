#!/usr/bin/env python3
"""ETF 择时 V2 - 完整回测 V2（修复版）"""

print("=" * 70)
print("ETF 择时 V2 - 完整回测")
print("=" * 70)

try:
    from jqdata import *
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    # 配置
    end_date = "2025-12-31"
    start_date = "2020-01-01"

    # 纯 A ETF 池
    ETF_POOL_A = {
        "沪深300ETF": "510300.XSHG",
        "中证500ETF": "510500.XSHG",
        "创业板ETF": "159915.XSHE",
        "科创50ETF": "588000.XSHG",
        "中证1000ETF": "512100.XSHG",
    }

    # 回测参数
    momentum_window = 20
    hold_days = 10
    top_n = 3
    cost = 0.001

    BENCHMARK_INDEX = "000300.XSHG"

    print(f"\n【配置信息】")
    print(f"  ETF 池: 纯 A 池 ({len(ETF_POOL_A)} 只)")
    print(f"  动量窗口: {momentum_window} 日")
    print(f"  持有周期: {hold_days} 日")
    print(f"  持仓数量: Top {top_n}")
    print(f"  单边成本: {cost:.1%}")
    print(f"  回测区间: {start_date} ~ {end_date}")

    # 获取 ETF 数据
    print(f"\n【1】获取 ETF 价格数据...")
    etf_prices = {}
    for name, code in ETF_POOL_A.items():
        try:
            df = get_price(
                code,
                start_date=start_date,
                end_date=end_date,
                fields=["close"],
                panel=False,
            )
            if df is not None and len(df) > 0:
                df = df.sort_values("time")
                df["pre_close"] = df["close"].shift(1)
                df["ret"] = df["close"] / df["pre_close"] - 1
                df = df.dropna()
                etf_prices[name] = df
                print(f"  {name}: {len(df)} 天数据 ✓")
            else:
                print(f"  {name}: 无数据")
        except Exception as e:
            print(f"  {name}: 获取失败 - {e}")

    if len(etf_prices) == 0:
        print("\n错误: 没有获取到任何 ETF 数据")
    else:
        print(f"\n  成功获取 {len(etf_prices)} 只 ETF 数据")

        # 计算市场宽度信号
        print(f"\n【2】计算市场宽度信号...")
        hs300_stocks = get_index_stocks(BENCHMARK_INDEX, date=end_date)
        test_stocks = hs300_stocks[:100]

        all_prices = get_price(
            test_stocks,
            start_date=start_date,
            end_date=end_date,
            fields=["close"],
            panel=False,
        )
        close_pivot = all_prices.pivot(index="time", columns="code", values="close")
        ma20 = close_pivot.rolling(20).mean()
        market_width = (close_pivot > ma20).sum(axis=1) / len(test_stocks)
        market_width = market_width.dropna()

        print(f"  市场宽度数据量: {len(market_width)}")
        print(f"  市场宽度均值: {market_width.mean():.2%}")

        # 生成信号
        width_signals = pd.DataFrame(index=market_width.index)
        width_signals["width"] = market_width
        width_signals["binary_0.4"] = (market_width >= 0.4).astype(float)
        width_signals["binary_0.3"] = (market_width >= 0.3).astype(float)
        width_signals["binary_0.25"] = (market_width >= 0.25).astype(float)
        width_signals["tiered_0.3_0.5"] = market_width.apply(
            lambda x: 1.0 if x >= 0.5 else (0.5 if x >= 0.3 else 0.0)
        )
        width_signals["tiered_0.25_0.45"] = market_width.apply(
            lambda x: 1.0 if x >= 0.45 else (0.5 if x >= 0.25 else 0.0)
        )

        print(f"\n  信号平均仓位:")
        for col in width_signals.columns:
            if col != "width":
                print(f"    {col}: {width_signals[col].mean():.2%}")

        # 简化的回测
        print(f"\n【3】开始回测...")

        # 获取所有 ETF 的动量数据
        etf_momentum = {}
        for name, df in etf_prices.items():
            if len(df) > momentum_window:
                df_indexed = df.set_index("time")
                mom = df_indexed["close"].pct_change(momentum_window)
                etf_momentum[name] = mom

        mom_df = pd.DataFrame(etf_momentum)

        # 对齐日期
        common_dates = width_signals.index.intersection(mom_df.index)
        width_signals_aligned = width_signals.loc[common_dates]
        mom_df_aligned = mom_df.loc[common_dates]

        print(f"  回测日期数: {len(common_dates)}")

        # 计算各策略收益
        results = []

        for signal_col, signal_name in [
            (None, "基线(不择时)"),
            ("binary_0.4", "宽度二元0.4(旧)"),
            ("binary_0.3", "宽度二元0.3"),
            ("binary_0.25", "宽度二元0.25"),
            ("tiered_0.3_0.5", "宽度分级0.3-0.5"),
            ("tiered_0.25_0.45", "宽度分级0.25-0.45"),
        ]:
            returns = []

            for i, date in enumerate(common_dates):
                # 获取仓位
                if signal_col is None:
                    position = 1.0
                else:
                    position = width_signals_aligned.loc[date, signal_col]

                # 获取调仓日（每10天）
                rebal_idx = (i // hold_days) * hold_days
                if rebal_idx >= len(common_dates):
                    rebal_idx = len(common_dates) - 1
                rebal_date = common_dates[rebal_idx]

                # 在调仓日选股
                if date == rebal_date and position > 0:
                    mom_today = mom_df_aligned.loc[date].dropna()
                    if len(mom_today) >= top_n:
                        top_etfs = mom_today.nlargest(top_n).index.tolist()
                    else:
                        top_etfs = mom_today.index.tolist()

                # 计算当日收益
                day_ret = 0
                if len(top_etfs) > 0 and position > 0:
                    for etf in top_etfs:
                        if etf in etf_prices:
                            etf_df = etf_prices[etf]
                            if date in etf_df["time"].values:
                                day_ret += etf_df[etf_df["time"] == date]["ret"].values[
                                    0
                                ]
                    day_ret = day_ret / len(top_etfs) * position

                    # 扣除交易成本
                    if date == rebal_date:
                        day_ret -= cost * 2

                returns.append(day_ret)

            returns_series = pd.Series(returns, index=common_dates)

            # 计算绩效
            if len(returns_series) > 0 and returns_series.std() > 0:
                cum_ret = (1 + returns_series).cumprod()
                total_ret = cum_ret.iloc[-1] - 1
                years = len(returns_series) / 252
                annual_ret = (1 + total_ret) ** (1 / years) - 1 if years > 0 else 0
                max_dd = (cum_ret / cum_ret.cummax() - 1).min()
                sharpe = returns_series.mean() / returns_series.std() * np.sqrt(252)
                empty_ratio = (returns_series == 0).sum() / len(returns_series)
            else:
                annual_ret = max_dd = sharpe = empty_ratio = 0

            results.append(
                {
                    "name": signal_name,
                    "annual_return": annual_ret,
                    "max_drawdown": max_dd,
                    "sharpe_ratio": sharpe,
                    "empty_ratio": empty_ratio,
                }
            )

            print(
                f"  {signal_name}: 年化={annual_ret:.2%}, 回撤={max_dd:.2%}, 夏普={sharpe:.2f}, 空仓率={empty_ratio:.1%}"
            )

        # 结果汇总
        print(f"\n" + "=" * 70)
        print("【回测结果汇总】")
        print("=" * 70)

        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values("sharpe_ratio", ascending=False)

        print(
            f"\n{'策略名称':<20} {'年化收益':>10} {'最大回撤':>10} {'夏普比率':>10} {'空仓率':>10}"
        )
        print("-" * 70)
        for _, row in results_df.iterrows():
            print(
                f"{row['name']:<20} {row['annual_return']:>10.2%} {row['max_drawdown']:>10.2%} {row['sharpe_ratio']:>10.2f} {row['empty_ratio']:>10.1%}"
            )

        # 当前建议
        print(f"\n" + "=" * 70)
        print("【当前市场仓位建议】")
        print("=" * 70)

        latest_date = width_signals.index[-1]
        latest_width = width_signals.loc[latest_date, "width"]
        print(f"\n  日期: {latest_date.date()}")
        print(f"  市场宽度: {latest_width:.2%}")

        for col, name in [
            ("binary_0.4", "宽度二元0.4"),
            ("binary_0.3", "宽度二元0.3"),
            ("tiered_0.3_0.5", "宽度分级0.3-0.5"),
        ]:
            pos = width_signals.loc[latest_date, col]
            print(f"  {name}: {pos:.0%}")

        if latest_width >= 0.5:
            print(f"\n  建议仓位: 满仓 (100%)")
        elif latest_width >= 0.3:
            print(f"\n  建议仓位: 半仓 (50%)")
        else:
            print(f"\n  建议仓位: 空仓 (0%)")

    print(f"\n" + "=" * 70)
    print("回测完成!")
    print("=" * 70)

except Exception as e:
    print(f"\n错误: {e}")
    import traceback

    traceback.print_exc()
