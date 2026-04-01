#!/usr/bin/env python3
"""ETF 择时 V2 - 完整回测（Notebook 版本）"""

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
                fields=["close", "pre_close"],
                panel=False,
            )
            df = df.set_index("time")
            df["ret"] = df["close"] / df["pre_close"] - 1
            etf_prices[name] = df
            print(f"  {name}: {len(df)} 天数据")
        except Exception as e:
            print(f"  {name}: 获取失败 - {e}")

    # 计算市场宽度信号
    print(f"\n【2】计算市场宽度信号...")
    hs300_stocks = get_index_stocks(BENCHMARK_INDEX, date=end_date)
    # 使用100只股票来平衡速度和准确性
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

    # 生成不同信号
    width_signals = pd.DataFrame(index=market_width.index)
    width_signals["width"] = market_width
    # 旧逻辑：二元 0.4
    width_signals["binary_0.4"] = (market_width >= 0.4).astype(float)
    # 新逻辑：二元 0.3
    width_signals["binary_0.3"] = (market_width >= 0.3).astype(float)
    # 新逻辑：二元 0.25
    width_signals["binary_0.25"] = (market_width >= 0.25).astype(float)
    # 分级逻辑 0.3-0.5
    width_signals["tiered_0.3_0.5"] = market_width.apply(
        lambda x: 1.0 if x >= 0.5 else (0.5 if x >= 0.3 else 0.0)
    )
    # 分级逻辑 0.25-0.45
    width_signals["tiered_0.25_0.45"] = market_width.apply(
        lambda x: 1.0 if x >= 0.45 else (0.5 if x >= 0.25 else 0.0)
    )

    print(f"\n  信号平均仓位:")
    for col in width_signals.columns:
        if col != "width":
            print(f"    {col}: {width_signals[col].mean():.2%}")

    # 回测函数
    def backtest_with_timing(
        signal_series, etf_prices, momentum_window, hold_days, top_n, cost
    ):
        """带择时的 ETF 轮动回测"""
        # 计算动量
        momentum = {}
        for name, df in etf_prices.items():
            if len(df) > momentum_window:
                mom = df["close"].pct_change(momentum_window)
                momentum[name] = mom

        mom_df = pd.DataFrame(momentum)
        mom_df = mom_df.dropna(how="all")

        # 对齐信号和动量
        common_idx = signal_series.index.intersection(mom_df.index)
        signal_aligned = signal_series.loc[common_idx]
        mom_aligned = mom_df.loc[common_idx]

        # 按调仓日计算收益
        rebal_dates = common_idx[::hold_days]
        daily_returns = []

        for i, date in enumerate(common_idx):
            position = signal_aligned.loc[date]
            rebal_idx = min((i // hold_days) * hold_days, len(rebal_dates) - 1)
            rebal_date = rebal_dates[rebal_idx]

            if rebal_date in mom_aligned.index:
                mom_on_rebal = mom_aligned.loc[rebal_date].dropna()
                if len(mom_on_rebal) >= top_n:
                    top_etfs = mom_on_rebal.nlargest(top_n).index.tolist()

                    day_ret = 0
                    for etf in top_etfs:
                        if etf in etf_prices and date in etf_prices[etf].index:
                            day_ret += etf_prices[etf].loc[date, "ret"]

                    day_ret = day_ret / top_n * position

                    # 扣除成本（调仓日）
                    if date == rebal_date and position > 0:
                        day_ret -= cost * 2

                    daily_returns.append(day_ret)
                else:
                    daily_returns.append(0)
            else:
                daily_returns.append(0)

        returns_series = pd.Series(daily_returns, index=common_idx)
        return returns_series

    def calc_performance(returns, name):
        """计算策略表现指标"""
        if len(returns) == 0 or returns.std() == 0:
            return {
                "name": name,
                "annual_return": 0,
                "max_drawdown": 0,
                "sharpe_ratio": 0,
                "empty_ratio": 0,
                "win_rate": 0,
            }

        cum_ret = (1 + returns).cumprod()
        total_ret = cum_ret.iloc[-1] - 1
        years = len(returns) / 252
        annual_ret = (
            (1 + total_ret) ** (1 / years) - 1 if years > 0 and total_ret > -1 else 0
        )
        max_dd = (cum_ret / cum_ret.cummax() - 1).min()
        sharpe = (
            returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        )
        empty_ratio = (returns == 0).sum() / len(returns)

        return {
            "name": name,
            "total_return": total_ret,
            "annual_return": annual_ret,
            "max_drawdown": max_dd,
            "sharpe_ratio": sharpe,
            "empty_ratio": empty_ratio,
            "win_rate": (returns > 0).sum() / len(returns),
        }

    # 回测对比
    print(f"\n【3】开始回测对比...")
    results = []

    # 1. 基线
    print(f"\n  回测基线（不择时）...")
    baseline_signal = pd.Series(1.0, index=width_signals.index)
    baseline_ret = backtest_with_timing(
        baseline_signal, etf_prices, momentum_window, hold_days, top_n, cost
    )
    baseline_perf = calc_performance(baseline_ret, "基线(不择时)")
    results.append(baseline_perf)
    print(
        f"    年化: {baseline_perf['annual_return']:.2%}, 回撤: {baseline_perf['max_drawdown']:.2%}, 夏普: {baseline_perf['sharpe_ratio']:.2f}"
    )

    # 2. 宽度信号对比
    configs = [
        ("binary_0.4", "宽度二元0.4(旧)"),
        ("binary_0.3", "宽度二元0.3"),
        ("binary_0.25", "宽度二元0.25"),
        ("tiered_0.3_0.5", "宽度分级0.3-0.5"),
        ("tiered_0.25_0.45", "宽度分级0.25-0.45"),
    ]

    for col, name in configs:
        print(f"\n  回测 {name}...")
        signal = width_signals[col]
        ret = backtest_with_timing(
            signal, etf_prices, momentum_window, hold_days, top_n, cost
        )
        perf = calc_performance(ret, name)
        results.append(perf)
        print(
            f"    年化: {perf['annual_return']:.2%}, 回撤: {perf['max_drawdown']:.2%}, 夏普: {perf['sharpe_ratio']:.2f}, 空仓率: {perf['empty_ratio']:.1%}"
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

    # 各信号当前状态
    for col, name in configs:
        pos = width_signals.loc[latest_date, col]
        print(f"  {name}: {pos:.0%}")

    # 综合建议
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
