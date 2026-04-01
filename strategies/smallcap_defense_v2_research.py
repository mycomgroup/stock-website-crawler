"""
小市值防守线v2筛选条件优化调研
测试不同ROE、PB、PE参数组合的影响
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


def test_filter_params(
    watch_date,
    min_roe=None,
    max_pb=None,
    max_pe=None,
    min_cashflow_ratio=None,
    max_debt_ratio=None,
):
    """
    测试不同筛选条件

    Parameters:
    -----------
    watch_date : 调研日期
    min_roe : ROE门槛(%), None表示无要求
    max_pb : PB上限, None表示无要求
    max_pe : PE上限, None表示无要求
    min_cashflow_ratio : 现金流/净利润最小比例, None表示无要求
    max_debt_ratio : 负债率上限, None表示无要求
    """
    stocks = get_smallcap_universe(watch_date)

    if len(stocks) == 0:
        return {"count": 0, "stocks": []}

    filters = [valuation.code.in_(stocks)]

    if max_pb is not None:
        filters.append(valuation.pb_ratio > 0)
        filters.append(valuation.pb_ratio < max_pb)

    if max_pe is not None:
        filters.append(valuation.pe_ratio > 0)
        filters.append(valuation.pe_ratio < max_pe)

    if min_roe is not None:
        filters.append(indicator.roe > min_roe)

    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
    ).filter(*filters)

    df = get_fundamentals(q, date=watch_date)

    if len(df) == 0:
        return {"count": 0, "stocks": []}

    df = df.drop_duplicates("code")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    if min_cashflow_ratio is not None or max_debt_ratio is not None:
        q2 = query(
            valuation.code,
            balance.total_assets,
            balance.total_liability,
            cash_flow.net_operate_cash_flow,
            income.net_profit,
        ).filter(valuation.code.in_(df["code"].tolist()))

        df2 = get_fundamentals(q2, date=watch_date)
        df2 = df2.drop_duplicates("code")

        if max_debt_ratio is not None:
            df2["debt_ratio"] = df2["total_liability"] / df2["total_assets"]
            df2 = df2[df2["debt_ratio"] < max_debt_ratio]

        if min_cashflow_ratio is not None:
            df2["cash_quality"] = df2["net_operate_cash_flow"] / df2["net_profit"]
            df2 = df2[df2["cash_quality"] > min_cashflow_ratio]

        df = df[df["code"].isin(df2["code"].tolist())]

    return {
        "count": len(df),
        "stocks": df["code"].tolist(),
        "avg_pb": df["pb_ratio"].mean() if len(df) > 0 else None,
        "avg_pe": df["pe_ratio"].mean() if len(df) > 0 else None,
        "avg_roe": df["roe"].mean() if len(df) > 0 else None,
    }


def test_backtest(start_date, end_date, params_list, hold_num=15):
    """
    回测不同参数组合

    Parameters:
    -----------
    start_date : 开始日期
    end_date : 结束日期
    params_list : 参数组合列表, 每个元素是dict
    hold_num : 持仓数量
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

    for params in params_list:
        print(f"\n测试参数组合: {params['name']}")

        portfolio_values = [1000000]
        dates = [month_first_dates[0] - timedelta(days=1)]
        positions = {}
        candidate_counts = []

        for i, date in enumerate(month_first_dates):
            result = test_filter_params(
                date,
                min_roe=params.get("min_roe"),
                max_pb=params.get("max_pb"),
                max_pe=params.get("max_pe"),
                min_cashflow_ratio=params.get("min_cashflow"),
                max_debt_ratio=params.get("max_debt"),
            )

            candidate_counts.append(result["count"])

            if result["count"] >= 5:
                selected = result["stocks"][:hold_num]

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

        results.append(
            {
                "name": params["name"],
                "annual_return": annual_return,
                "benchmark_return": benchmark_annual,
                "excess_return": excess_return,
                "max_drawdown": max_drawdown,
                "avg_candidates": avg_candidates,
                "min_candidates": min_candidates,
                "max_candidates": max_candidates,
                "params": params,
            }
        )

        print(f"  年化收益: {annual_return:.2%}")
        print(f"  基准收益: {benchmark_annual:.2%}")
        print(f"  超额收益: {excess_return:.2%}")
        print(f"  最大回撤: {max_drawdown:.2%}")
        print(
            f"  平均候选数: {avg_candidates:.1f} (最少:{min_candidates}, 最多:{max_candidates})"
        )

    return pd.DataFrame(results)


def main():
    """主测试流程"""

    print("=" * 80)
    print("小市值防守线v2筛选条件优化调研")
    print("=" * 80)

    test_date = datetime(2025, 3, 1)

    print("\n" + "=" * 80)
    print("第一部分: 候选池数量分析")
    print("=" * 80)

    print("\n1. 测试不同ROE门槛的影响")
    roe_tests = [
        {"name": "无ROE要求", "min_roe": None},
        {"name": "ROE>6%", "min_roe": 6},
        {"name": "ROE>8%", "min_roe": 8},
        {"name": "ROE>10%", "min_roe": 10},
    ]

    print("\n基础条件: PB<1.5, PE<20")
    for test in roe_tests:
        result = test_filter_params(
            test_date, min_roe=test["min_roe"], max_pb=1.5, max_pe=20
        )
        print(f"{test['name']}: {result['count']} 只股票")

    print("\n2. 测试不同PB限制的影响")
    pb_tests = [
        {"name": "PB<1.5", "max_pb": 1.5},
        {"name": "PB<2.0", "max_pb": 2.0},
        {"name": "PB<2.5", "max_pb": 2.5},
        {"name": "PB<3.0", "max_pb": 3.0},
    ]

    print("\n基础条件: 无ROE, PE<20")
    for test in pb_tests:
        result = test_filter_params(test_date, max_pb=test["max_pb"], max_pe=20)
        print(f"{test['name']}: {result['count']} 只股票")

    print("\n3. 测试不同PE限制的影响")
    pe_tests = [
        {"name": "PE<15", "max_pe": 15},
        {"name": "PE<20", "max_pe": 20},
        {"name": "PE<25", "max_pe": 25},
        {"name": "PE<30", "max_pe": 30},
    ]

    print("\n基础条件: 无ROE, PB<1.5")
    for test in pe_tests:
        result = test_filter_params(test_date, max_pb=1.5, max_pe=test["max_pe"])
        print(f"{test['name']}: {result['count']} 只股票")

    print("\n4. 测试组合条件的影响")
    combo_tests = [
        {
            "name": "v1质量(ROE>8,CF>0.8,Debt<60%)",
            "min_roe": 8,
            "min_cashflow": 0.8,
            "max_debt": 0.6,
        },
        {"name": "v1低估值(PB<1.5,PE<20)", "max_pb": 1.5, "max_pe": 20},
        {
            "name": "组合1(ROE>6,PB<2.0,PE<25)",
            "min_roe": 6,
            "max_pb": 2.0,
            "max_pe": 25,
        },
        {
            "name": "组合2(ROE>6,PB<2.5,PE<25)",
            "min_roe": 6,
            "max_pb": 2.5,
            "max_pe": 25,
        },
        {
            "name": "组合3(ROE>8,PB<2.0,PE<25)",
            "min_roe": 8,
            "max_pb": 2.0,
            "max_pe": 25,
        },
        {
            "name": "组合4(ROE>6,PB<2.0,PE<30)",
            "min_roe": 6,
            "max_pb": 2.0,
            "max_pe": 30,
        },
    ]

    for test in combo_tests:
        result = test_filter_params(
            test_date,
            min_roe=test.get("min_roe"),
            max_pb=test.get("max_pb"),
            max_pe=test.get("max_pe"),
            min_cashflow_ratio=test.get("min_cashflow"),
            max_debt_ratio=test.get("max_debt"),
        )
        print(f"{test['name']}: {result['count']} 只股票")

    print("\n" + "=" * 80)
    print("第二部分: OOS期回测分析 (2024-01-01 至 2025-03-01)")
    print("=" * 80)

    start_date = "2024-01-01"
    end_date = "2025-03-01"

    backtest_params = [
        {
            "name": "v1质量策略",
            "min_roe": 8,
            "min_cashflow": 0.8,
            "max_debt": 0.6,
        },
        {
            "name": "v1低估值(PB<1.5,PE<20)",
            "max_pb": 1.5,
            "max_pe": 20,
        },
        {
            "name": "宽松ROE(PB<1.5,PE<20,ROE>6)",
            "min_roe": 6,
            "max_pb": 1.5,
            "max_pe": 20,
        },
        {
            "name": "放宽PB(PB<2.0,PE<20)",
            "max_pb": 2.0,
            "max_pe": 20,
        },
        {
            "name": "放宽PE(PB<1.5,PE<25)",
            "max_pb": 1.5,
            "max_pe": 25,
        },
        {
            "name": "推荐组合1(ROE>6,PB<2.0,PE<25)",
            "min_roe": 6,
            "max_pb": 2.0,
            "max_pe": 25,
        },
        {
            "name": "推荐组合2(ROE>6,PB<2.5,PE<25)",
            "min_roe": 6,
            "max_pb": 2.5,
            "max_pe": 25,
        },
        {
            "name": "推荐组合3(ROE>6,PB<2.0,PE<30)",
            "min_roe": 6,
            "max_pb": 2.0,
            "max_pe": 30,
        },
    ]

    results_df = test_backtest(start_date, end_date, backtest_params, hold_num=15)

    print("\n" + "=" * 80)
    print("回测结果汇总")
    print("=" * 80)

    print("\n" + results_df.to_string(index=False))

    print("\n" + "=" * 80)
    print("候选池数量对比表")
    print("=" * 80)

    summary_table = results_df[
        ["name", "avg_candidates", "min_candidates", "max_candidates"]
    ].copy()
    summary_table.columns = ["策略名称", "平均候选数", "最少候选数", "最多候选数"]
    print("\n" + summary_table.to_string(index=False))

    print("\n" + "=" * 80)
    print("收益风险对比表")
    print("=" * 80)

    return_table = results_df[
        ["name", "annual_return", "benchmark_return", "excess_return", "max_drawdown"]
    ].copy()
    return_table.columns = ["策略名称", "年化收益", "基准收益", "超额收益", "最大回撤"]
    print("\n" + return_table.to_string(index=False))

    print("\n" + "=" * 80)
    print("调研结论")
    print("=" * 80)

    best_excess = results_df.loc[results_df["excess_return"].idxmax()]
    print(f"\n最优策略(超额收益最高): {best_excess['name']}")
    print(f"  年化收益: {best_excess['annual_return']:.2%}")
    print(f"  超额收益: {best_excess['excess_return']:.2%}")
    print(f"  最大回撤: {best_excess['max_drawdown']:.2%}")
    print(f"  平均候选数: {best_excess['avg_candidates']:.1f}")

    best_balance = results_df[
        (results_df["avg_candidates"] >= 20) & (results_df["avg_candidates"] <= 60)
    ]
    if len(best_balance) > 0:
        best_balance = best_balance.loc[best_balance["excess_return"].idxmax()]
        print(f"\n平衡策略(候选数20-60,超额收益最高): {best_balance['name']}")
        print(f"  年化收益: {best_balance['annual_return']:.2%}")
        print(f"  超额收益: {best_balance['excess_return']:.2%}")
        print(f"  最大回撤: {best_balance['max_drawdown']:.2%}")
        print(f"  平均候选数: {best_balance['avg_candidates']:.1f}")

    print("\n" + "=" * 80)
    print("推荐筛选条件")
    print("=" * 80)

    params = best_excess["params"]
    print(f"\n基于OOS期测试结果,推荐以下筛选条件:")
    print(f"  市值范围: 15-60亿")
    print(f"  市值分位: 后30%(小市值)")
    print(
        f"  ROE要求: {'>=' + str(params.get('min_roe', '无')) + '%' if params.get('min_roe') else '无要求'}"
    )
    print(f"  PB上限: {params.get('max_pb', '无要求')}")
    print(f"  PE上限: {params.get('max_pe', '无要求')}")
    print(
        f"  现金流要求: {'>' + str(params.get('min_cashflow', '无要求')) if params.get('min_cashflow') else '无要求'}"
    )
    print(
        f"  负债率上限: {'<' + str(params.get('max_debt', '无要求')) if params.get('max_debt') else '无要求'}"
    )
    print(f"  持仓数量: 15只")
    print(f"  调仓频率: 月度")


if __name__ == "__main__":
    main()
