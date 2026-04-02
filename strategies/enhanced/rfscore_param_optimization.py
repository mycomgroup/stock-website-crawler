"""
RFScore参数优化快速测试脚本
运行方式：在JoinQuant Notebook中执行
测试目标：找到最优PB阈值、持仓数量、ROA阈值
"""

print("=" * 80)
print("RFScore参数优化快速测试")
print("=" * 80)

try:
    from jqdata import *
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    # ===== 优化参数网格 =====
    param_grid = {
        "pb_threshold": [0.8, 1.0, 1.2, 1.5],
        "hold_num": [5, 10, 15],
        "roa_threshold": [3, 5, 8],
    }

    print("\n优化参数网格:")
    print(f"  PB阈值: {param_grid['pb_threshold']}")
    print(f"  持仓数量: {param_grid['hold_num']}")
    print(f"  ROA阈值: {param_grid['roa_threshold']}")

    # ===== 测试日期 =====
    test_dates = [
        "2023-03-20",
        "2023-06-20",
        "2023-09-20",
        "2023-12-20",
        "2024-03-20",
        "2024-06-20",
    ]

    print(f"\n测试日期: {len(test_dates)}个时间点")

    # ===== 开始优化 =====
    print("\n" + "=" * 80)
    print("开始参数优化测试...")
    print("=" * 80)

    results = []
    total_combinations = (
        len(param_grid["pb_threshold"])
        * len(param_grid["hold_num"])
        * len(param_grid["roa_threshold"])
    )

    print(f"\n总测试组合数: {total_combinations}")

    current = 0

    for pb in param_grid["pb_threshold"]:
        for hold_num in param_grid["hold_num"]:
            for roa in param_grid["roa_threshold"]:
                current += 1

                print(
                    f"\n[{current}/{total_combinations}] 测试: PB<{pb}, 持仓{hold_num}只, ROA>{roa}%"
                )

                # 统计变量
                total_selected = 0
                successful_dates = 0

                for test_date in test_dates:
                    try:
                        # 获取股票池
                        hs300 = set(get_index_stocks("000300.XSHG", date=test_date))
                        zz500 = set(get_index_stocks("000905.XSHG", date=test_date))
                        stocks = list(hs300 | zz500)

                        # ST过滤
                        is_st = get_extras("is_st", stocks, end_date=test_date, count=1)
                        if not is_st.empty:
                            st_stocks = is_st.iloc[-1][
                                is_st.iloc[-1] == True
                            ].index.tolist()
                            stocks = [s for s in stocks if s not in st_stocks]

                        # 停牌过滤
                        paused = get_price(
                            stocks,
                            end_date=test_date,
                            count=1,
                            fields=["paused"],
                            panel=False,
                        )
                        if not paused.empty:
                            paused_stocks = paused[paused["paused"] == 1][
                                "code"
                            ].tolist()
                            stocks = [s for s in stocks if s not in paused_stocks]

                        # 估值筛选
                        q = query(valuation.code, valuation.pb_ratio).filter(
                            valuation.code.in_(stocks),
                            valuation.pb_ratio > 0,
                            valuation.pb_ratio < pb,
                        )

                        df_val = get_fundamentals(q, date=test_date)

                        if df_val is not None and not df_val.empty:
                            # 财务筛选
                            q_factor = query(indicator.code, indicator.roa).filter(
                                indicator.code.in_(df_val["code"].tolist()),
                                indicator.roa > roa,
                            )

                            df_factor = get_fundamentals(q_factor, date=test_date)

                            if df_factor is not None and not df_factor.empty:
                                selected_count = len(df_factor)
                                total_selected += selected_count

                                # 判断是否满足持仓要求
                                if selected_count >= hold_num * 0.8:
                                    successful_dates += 1

                    except Exception as e:
                        print(f"  {test_date} 测试失败: {e}")

                # 计算平均选股数
                avg_selected = total_selected / len(test_dates)
                success_rate = successful_dates / len(test_dates) * 100

                print(
                    f"  结果: 平均选股{avg_selected:.1f}只, 成功率{success_rate:.0f}%"
                )

                # 记录结果
                results.append(
                    {
                        "PB阈值": pb,
                        "持仓数": hold_num,
                        "ROA阈值": roa,
                        "平均选股": avg_selected,
                        "成功率": success_rate,
                    }
                )

    # ===== 输出结果 =====
    print("\n" + "=" * 80)
    print("优化结果汇总")
    print("=" * 80)

    df_results = pd.DataFrame(results)
    print("\n完整结果表:")
    print(df_results.to_string(index=False))

    # ===== 推荐参数 =====
    print("\n" + "=" * 80)
    print("推荐参数组合")
    print("=" * 80)

    # 推荐条件：
    # 1. 平均选股数 >= 持仓数 * 0.8
    # 2. 平均选股数 <= 持仓数 * 1.5
    # 3. 成功率 >= 60%

    recommended = df_results[
        (df_results["平均选股"] >= df_results["持仓数"] * 0.8)
        & (df_results["平均选股"] <= df_results["持仓数"] * 1.5)
        & (df_results["成功率"] >= 60)
    ]

    if not recommended.empty:
        # 按成功率排序
        recommended = recommended.sort_values("成功率", ascending=False)

        print("\n推荐参数组合（成功率>=60%）：")
        print(recommended.to_string(index=False))

        # 最佳参数
        best = recommended.iloc[0]
        print(f"\n最佳参数:")
        print(f"  PB阈值: {best['PB阈值']}")
        print(f"  持仓数: {best['持仓数']}只")
        print(f"  ROA阈值: {best['ROA阈值']}%")
        print(f"  平均选股: {best['平均选股']:.1f}只")
        print(f"  成功率: {best['成功率']:.0f}%")
    else:
        print("\n警告：无符合推荐条件的参数组合")
        print("建议放宽筛选条件")

        # 显示成功率最高的组合
        best = df_results.loc[df_results["成功率"].idxmax()]
        print(f"\n成功率最高的参数:")
        print(f"  PB阈值: {best['PB阈值']}")
        print(f"  持仓数: {best['持仓数']}只")
        print(f"  ROA阈值: {best['ROA阈值']}%")
        print(f"  成功率: {best['成功率']:.0f}%")

    # ===== 参数敏感度分析 =====
    print("\n" + "=" * 80)
    print("参数敏感度分析")
    print("=" * 80)

    # PB敏感度
    print("\n按PB阈值分组:")
    pb_analysis = (
        df_results.groupby("PB阈值")
        .agg({"平均选股": "mean", "成功率": "mean"})
        .round(2)
    )
    print(pb_analysis)

    # 持仓数敏感度
    print("\n按持仓数分组:")
    hold_analysis = (
        df_results.groupby("持仓数")
        .agg({"平均选股": "mean", "成功率": "mean"})
        .round(2)
    )
    print(hold_analysis)

    # ROA敏感度
    print("\n按ROA阈值分组:")
    roa_analysis = (
        df_results.groupby("ROA阈值")
        .agg({"平均选股": "mean", "成功率": "mean"})
        .round(2)
    )
    print(roa_analysis)

    # ===== 优化建议 =====
    print("\n" + "=" * 80)
    print("优化建议")
    print("=" * 80)

    print("\n基于测试结果:")

    # PB建议
    best_pb = pb_analysis["成功率"].idxmax()
    print(f"1. PB阈值建议: {best_pb} (成功率最高)")

    # 持仓数建议
    best_hold = hold_analysis["成功率"].idxmax()
    print(f"2. 持仓数建议: {best_hold}只 (成功率最高)")

    # ROA建议
    best_roa = roa_analysis["成功率"].idxmax()
    print(f"3. ROA阈值建议: {best_roa}% (成功率最高)")

    print(f"\n综合建议配置:")
    print(f"  PB阈值: {best_pb}")
    print(f"  持仓数: {best_hold}只")
    print(f"  ROA阈值: {best_roa}%")

    print("\n" + "=" * 80)
    print("✓ 参数优化测试完成")
    print("=" * 80)

except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback

    traceback.print_exc()

print("\n测试结束")
