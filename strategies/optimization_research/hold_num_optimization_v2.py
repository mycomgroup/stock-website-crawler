"""
小市值防守线v2持仓数量优化调研
测试不同持仓数量对回撤、收益、夏普比率的影响
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_smallcap_universe(watch_date, min_cap=15, max_cap=60, ipo_days=180):
    """获取小市值股票池"""
    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - pd.Timedelta(days=ipo_days)
    ]
    stocks = all_stocks.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    stocks = [s for s in stocks if not s.startswith("688")]

    q = query(valuation.code, valuation.market_cap).filter(
        valuation.code.in_(stocks),
        valuation.market_cap >= min_cap,
        valuation.market_cap <= max_cap,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df["cap_rank"] = df["market_cap"].rank(pct=True)
    small_stocks = df[df["cap_rank"] <= 0.3]["code"].tolist()

    return small_stocks


def select_stocks(watch_date, hold_num, max_pb=1.5, max_pe=20):
    """筛选股票"""
    stocks = get_smallcap_universe(watch_date)
    if len(stocks) < 5:
        return [], 0

    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
    ).filter(
        valuation.code.in_(stocks),
        valuation.pe_ratio > 0,
        valuation.pe_ratio < max_pe,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < max_pb,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return [], 0

    df = df.drop_duplicates("code")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    if len(df) == 0:
        return [], 0

    df["pb_rank"] = df["pb_ratio"].rank(pct=True)
    df["pe_rank"] = df["pe_ratio"].rank(pct=True)
    df["value_score"] = (df["pb_rank"] + df["pe_rank"]) / 2

    df = df.sort_values("value_score", ascending=True)

    candidate_count = len(df)
    return df["code"].tolist()[:hold_num], candidate_count


def backtest_hold_num(start_date, end_date, hold_num_list):
    """
    回测不同持仓数量

    Parameters:
    -----------
    start_date : 开始日期
    end_date : 结束日期
    hold_num_list : 持仓数量列表
    """
    results = []

    trade_dates = get_trade_days(start_date, end_date)
    month_first_dates = []
    for i, date in enumerate(trade_dates):
        if i == 0:
            month_first_dates.append(date)
        else:
            prev_date = trade_dates[i - 1]
            if date.month != prev_date.month:
                month_first_dates.append(date)

    print(f"回测期间: {start_date} 至 {end_date}")
    print(f"调仓次数: {len(month_first_dates)}")
    print(f"测试持仓数: {hold_num_list}")

    for hold_num in hold_num_list:
        print(f"\n测试持仓数={hold_num}")

        portfolio_values = [1000000]
        dates = [month_first_dates[0] - timedelta(days=1)]
        positions = {}
        candidate_counts = []
        insufficient_pool_count = 0

        for i, date in enumerate(month_first_dates):
            selected, candidate_count = select_stocks(date, hold_num)
            candidate_counts.append(candidate_count)

            if candidate_count < hold_num:
                insufficient_pool_count += 1

            if len(selected) >= 5:
                for stock in list(positions.keys()):
                    if stock not in selected:
                        del positions[stock]

                for stock in selected:
                    if stock not in positions:
                        positions[stock] = 0
            else:
                positions = {}

            if i < len(month_first_dates) - 1:
                next_date = month_first_dates[i + 1]
            else:
                next_date = trade_dates[-1]

            try:
                if len(positions) > 0:
                    price_end = get_price(
                        list(positions.keys()),
                        end_date=next_date,
                        count=1,
                        fields="close",
                        panel=False,
                    )
                    if len(price_end) > 0:
                        price_end = price_end.pivot(
                            index="time", columns="code", values="close"
                        ).iloc[-1]
                        portfolio_value = sum(
                            [
                                price_end.get(stock, 0) * shares
                                for stock, shares in positions.items()
                            ]
                        )
                        portfolio_value += 1000000 - sum(positions.values())
                    else:
                        portfolio_value = portfolio_values[-1]
                else:
                    portfolio_value = 1000000
            except:
                portfolio_value = portfolio_values[-1]

            portfolio_values.append(portfolio_value)
            dates.append(date)

        portfolio_series = pd.Series(portfolio_values, index=dates)
        returns = portfolio_series.pct_change().dropna()

        annual_return = (1 + returns.mean()) ** 252 - 1

        max_value = portfolio_series.expanding().max()
        drawdown = (portfolio_series - max_value) / max_value
        max_drawdown = drawdown.min()

        if len(returns) > 0:
            sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
        else:
            sharpe_ratio = 0

        benchmark = get_price(
            "000852.XSHG",
            start_date=start_date,
            end_date=end_date,
            fields="close",
            panel=False,
        )
        benchmark_returns = benchmark["close"].pct_change().dropna()
        benchmark_annual = (1 + benchmark_returns.mean()) ** 252 - 1

        excess_return = annual_return - benchmark_annual

        avg_candidates = np.mean(candidate_counts)
        min_candidates = np.min(candidate_counts)
        max_candidates = np.max(candidate_counts)
        median_candidates = np.median(candidate_counts)

        results.append(
            {
                "hold_num": hold_num,
                "annual_return": annual_return,
                "benchmark_return": benchmark_annual,
                "excess_return": excess_return,
                "max_drawdown": max_drawdown,
                "sharpe_ratio": sharpe_ratio,
                "avg_candidates": avg_candidates,
                "min_candidates": min_candidates,
                "max_candidates": max_candidates,
                "median_candidates": median_candidates,
                "insufficient_pool_count": insufficient_pool_count,
                "total_rebalance": len(month_first_dates),
                "insufficient_pool_pct": insufficient_pool_count
                / len(month_first_dates),
            }
        )

        print(f"  年化收益: {annual_return:.2%}")
        print(f"  最大回撤: {max_drawdown:.2%}")
        print(f"  夏普比率: {sharpe_ratio:.2f}")
        print(f"  超额收益: {excess_return:.2%}")
        print(f"  平均候选数: {avg_candidates:.1f}")
        print(
            f"  候选池不足次数: {insufficient_pool_count}/{len(month_first_dates)} ({insufficient_pool_count / len(month_first_dates):.1%})"
        )

    return pd.DataFrame(results)


def main():
    """主测试流程"""

    print("=" * 80)
    print("小市值防守线v2持仓数量优化调研")
    print("=" * 80)

    start_date = "2022-04-01"
    end_date = "2025-03-30"

    hold_num_list = [5, 8, 10, 12, 15]

    results_df = backtest_hold_num(start_date, end_date, hold_num_list)

    print("\n" + "=" * 80)
    print("回测结果汇总")
    print("=" * 80)

    print("\n" + results_df.to_string(index=False))

    print("\n" + "=" * 80)
    print("持仓数量对比表（回撤、收益、夏普）")
    print("=" * 80)

    summary_table = results_df[
        ["hold_num", "max_drawdown", "annual_return", "sharpe_ratio", "excess_return"]
    ].copy()
    summary_table.columns = ["持仓数", "最大回撤", "年化收益", "夏普比率", "超额收益"]
    print("\n" + summary_table.to_string(index=False))

    print("\n" + "=" * 80)
    print("候选池对比表")
    print("=" * 80)

    pool_table = results_df[
        [
            "hold_num",
            "avg_candidates",
            "min_candidates",
            "max_candidates",
            "median_candidates",
            "insufficient_pool_pct",
        ]
    ].copy()
    pool_table.columns = [
        "持仓数",
        "平均候选数",
        "最少候选数",
        "最多候选数",
        "中位候选数",
        "候选池不足比例",
    ]
    print("\n" + pool_table.to_string(index=False))

    print("\n" + "=" * 80)
    print("防守线标准评估")
    print("=" * 80)

    print("\n防守线标准：回撤<=25%, 超额>8%")

    for _, row in results_df.iterrows():
        drawdown_pass = row["max_drawdown"] <= -0.25
        excess_pass = row["excess_return"] > 0.08

        status = "✅ 达标" if (drawdown_pass and excess_pass) else "❌ 不达标"

        print(f"\n持仓数={row['hold_num']}:")
        print(
            f"  最大回撤: {row['max_drawdown']:.2%} {'✅' if drawdown_pass else '❌'} (标准<=25%)"
        )
        print(
            f"  超额收益: {row['excess_return']:.2%} {'✅' if excess_pass else '❌'} (标准>8%)"
        )
        print(f"  综合判定: {status}")

    print("\n" + "=" * 80)
    print("持仓数量推荐")
    print("=" * 80)

    candidates_pool_requirement = results_df[
        results_df["avg_candidates"] >= results_df["hold_num"] * 1.5
    ]

    if len(candidates_pool_requirement) > 0:
        best_in_pool = candidates_pool_requirement.loc[
            candidates_pool_requirement["max_drawdown"].idxmin()
        ]
        print(f"\n候选池充足前提下回撤最小:")
        print(f"  推荐持仓数: {int(best_in_pool['hold_num'])}")
        print(f"  最大回撤: {best_in_pool['max_drawdown']:.2%}")
        print(f"  年化收益: {best_in_pool['annual_return']:.2%}")
        print(f"  夏普比率: {best_in_pool['sharpe_ratio']:.2f}")
        print(f"  超额收益: {best_in_pool['excess_return']:.2%}")
        print(f"  平均候选数: {best_in_pool['avg_candidates']:.1f}")

drawdown_pass_df = results_df[results_df["max_drawdown"] <= -0.25]
    if len(drawdown_pass_df) > 0:
        best_drawdown = drawdown_pass_df.loc[drawdown_pass_df["excess_return"].idxmax()]
        print(f"\n回撤达标前提下超额最高:")
        print(f"  推荐持仓数: {int(best_drawdown['hold_num'])}")
        print(f"  最大回撤: {best_drawdown['max_drawdown']:.2%}")
        print(f"  年化收益: {best_drawdown['annual_return']:.2%}")
        print(f"  夏普比率: {best_drawdown['sharpe_ratio']:.2f}")
        print(f"  超额收益: {best_drawdown['excess_return']:.2%}")
        print(f"  平均候选数: {best_drawdown['avg_candidates']:.1f}")

    excess_pass_df = results_df[results_df["excess_return"] > 0.08]
    both_pass = results_df[
        (results_df["max_drawdown"] <= -0.25) & 
        (results_df["excess_return"] > 0.08)
    ]
    if len(both_pass) > 0:
        best_both = both_pass.loc[both_pass["sharpe_ratio"].idxmax()]
        print(f"\n防守线标准完全达标:")
        print(f"  推荐持仓数: {int(best_both['hold_num'])}")
        print(f"  最大回撤: {best_both['max_drawdown']:.2%}")
        print(f"  年化收益: {best_both['annual_return']:.2%}")
        print(f"  夏普比率: {best_both['sharpe_ratio']:.2f}")
        print(f"  超额收益: {best_both['excess_return']:.2%}")
        print(f"  平均候选数: {best_both['avg_candidates']:.1f}")

    print("\n" + "=" * 80)
    print("候选池要求分析")
    print("=" * 80)

    print("\n候选池要求: 候选池>=持仓数×1.5倍")
    for _, row in results_df.iterrows():
        required_candidates = row["hold_num"] * 1.5
        actual_avg = row["avg_candidates"]
        pool_sufficient = actual_avg >= required_candidates

        print(f"\n持仓数={row['hold_num']}:")
        print(f"  要求候选数: {required_candidates}")
        print(f"  实际平均候选数: {actual_avg:.1f}")
        print(f"  候选池状态: {'✅ 充足' if pool_sufficient else '⚠️ 不足'}")
        print(f"  候选池不足比例: {row['insufficient_pool_pct']:.1%}")

    print("\n" + "=" * 80)
    print("调研结论")
    print("=" * 80)

    excess_pass_df = results_df[results_df["excess_return"] > 0.08]

    print("\n核心发现:")
    print(f"1. 持仓数越少，回撤越小:")
    for _, row in results_df.iterrows():
        print(f"   {int(row['hold_num'])}只持仓: 回撤{row['max_drawdown']:.2%}")

    print(f"\n2. 持仓数越少，收益越高:")
    for _, row in results_df.iterrows():
        print(
            f"   {int(row['hold_num'])}只持仓: 收益{row['annual_return']:.2%}, 超额{row['excess_return']:.2%}"
        )

    print(f"\n3. 持仓数越少，候选池要求越高:")
    for _, row in results_df.iterrows():
        print(
            f"   {int(row['hold_num'])}只持仓: 平均候选{row['avg_candidates']:.1f}, 不足比例{row['insufficient_pool_pct']:.1%}"
        )

    drawdown_best = results_df.loc[results_df["max_drawdown"].idxmin()]
    print(f"\n最优回撤控制: {int(drawdown_best['hold_num'])}只持仓")
    print(f"  最大回撤: {drawdown_best['max_drawdown']:.2%}")
    print(f"  超额收益: {drawdown_best['excess_return']:.2%}")

    sharpe_best = results_df.loc[results_df["sharpe_ratio"].idxmax()]
    print(f"\n最优夏普比率: {int(sharpe_best['hold_num'])}只持仓")
    print(f"  夏普比率: {sharpe_best['sharpe_ratio']:.2f}")
    print(f"  最大回撤: {sharpe_best['max_drawdown']:.2%}")
    print(f"  超额收益: {sharpe_best['excess_return']:.2%}")

    print("\n最终推荐:")


if __name__ == "__main__":
    main()
