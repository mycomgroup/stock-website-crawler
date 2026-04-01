from jqdata import *
import pandas as pd
import numpy as np

print("北向资金流向指标深挖测试（简化版）")
print("=" * 60)
print("时间范围: 2024-01-01 至 2024-08-17")
print("=" * 60)

START_DATE = "2024-01-01"
END_DATE = "2024-08-17"

print("\n第一部分: 获取北向资金数据")
print("-" * 40)

q = (
    query(finance.STK_ML_QUOTA)
    .filter(
        finance.STK_ML_QUOTA.day >= START_DATE,
        finance.STK_ML_QUOTA.day <= END_DATE,
        finance.STK_ML_QUOTA.link_id.in_([310001, 310002]),
    )
    .order_by(finance.STK_ML_QUOTA.day.asc())
)

nb_full = finance.run_query(q)

if len(nb_full) > 0:
    nb_daily = (
        nb_full.groupby("day")
        .agg({"buy_amount": "sum", "sell_amount": "sum", "sum_amount": "sum"})
        .reset_index()
    )

    nb_daily["net_flow"] = nb_daily["buy_amount"] - nb_daily["sell_amount"]
    nb_daily["net_flow_5d_ma"] = nb_daily["net_flow"].rolling(5).mean()

    print(f"北向数据条数: {len(nb_daily)}")
    print(f"北向净流入均值: {nb_daily['net_flow'].mean() / 1e8:.2f}亿")
    print(f"北向净流入累计: {nb_daily['net_flow'].sum() / 1e8:.2f}亿")

    print("\n北向资金趋势:")
    print(
        f"  净流入>0天数: {(nb_daily['net_flow'] > 0).sum()} ({(nb_daily['net_flow'] > 0).mean() * 100:.1f}%)"
    )
    print(
        f"  5日MA>0天数: {(nb_daily['net_flow_5d_ma'] > 0).sum()} ({(nb_daily['net_flow_5d_ma'] > 0).mean() * 100:.1f}%)"
    )
else:
    print("未获取到北向资金数据")
    nb_daily = pd.DataFrame()

print("\n第二部分: 获取市场数据（简化）")
print("-" * 40)

trade_days = get_trade_days(START_DATE, END_DATE)
print(f"交易日数: {len(trade_days)}")

index_data = get_price(
    "000300.XSHG", START_DATE, END_DATE, fields=["close"], panel=False
)

index_data["time"] = pd.to_datetime(index_data["time"])
index_data["return"] = index_data["close"].pct_change()

print(f"沪深300收益均值: {index_data['return'].mean() * 100:.3f}%")

print("\n第三部分: 模拟情绪开关与北向资金关联")
print("-" * 40)

if len(nb_daily) > 0:
    nb_daily["day"] = pd.to_datetime(nb_daily["day"])

    merged = pd.merge(index_data, nb_daily, left_on="time", right_on="day", how="inner")

    if len(merged) > 0:
        print(f"合并数据条数: {len(merged)}")

        correlation = merged["return"].corr(merged["net_flow"])
        print(f"\n沪深300收益 vs 北向净流入相关性: {correlation:.3f}")

        nb_positive_days = merged[merged["net_flow"] > 0]
        nb_negative_days = merged[merged["net_flow"] < 0]

        if len(nb_positive_days) > 0 and len(nb_negative_days) > 0:
            print(f"\n北向净流入>0时:")
            print(f"  天数: {len(nb_positive_days)}")
            print(f"  平均收益: {nb_positive_days['return'].mean() * 100:.3f}%")
            print(
                f"  正收益天数: {(nb_positive_days['return'] > 0).sum()} ({(nb_positive_days['return'] > 0).mean() * 100:.1f}%)"
            )

            print(f"\n北向净流入<0时:")
            print(f"  天数: {len(nb_negative_days)}")
            print(f"  平均收益: {nb_negative_days['return'].mean() * 100:.3f}%")
            print(
                f"  正收益天数: {(nb_negative_days['return'] > 0).sum()} ({(nb_negative_days['return'] > 0).mean() * 100:.1f}%)"
            )

            return_diff = (
                nb_positive_days["return"].mean() - nb_negative_days["return"].mean()
            )
            print(f"\n收益差异: 北向>0 vs 北向<0 = {return_diff * 100:.3f}%")

            print("\n第四部分: 理论增益分析")
            print("=" * 60)

            print("假设情绪开关开仓概率为p，北向净流入>0时的收益增益为Δ")
            print(f"  当前数据: Δ = {return_diff * 100:.3f}%")

            if return_diff > 0.002:
                print(f"\n结论: Go - 北向净流入>0时收益明显更高")
                print(f"  增益幅度: {return_diff * 100:.3f}%")
                print("  建议: 北向资金可作为辅助过滤指标")
            elif return_diff < -0.002:
                print(f"\n结论: Watch - 北向净流入<0时收益反而更高")
                print(f"  增益幅度: {return_diff * 100:.3f}%")
                print("  建议: 北向资金指标可能存在反向作用，需谨慎")
            else:
                print(f"\n结论: No-Go - 北向资金无明显增益")
                print(f"  增益幅度: {return_diff * 100:.3f}%")
                print("  建议: 不纳入北向资金指标")

            print("\n第五部分: 情绪开关+北向资金组合效果估算")
            print("-" * 40)

            print("参考result_06数据:")
            print("  B组（仅情绪）: 年化11.66%, 夏普0.34, 最大回撤23.55%")

            if return_diff > 0.002:
                estimated_boost = return_diff * 0.3
                print(f"\n估算增益:")
                print(f"  北向>0日收益提升: {return_diff * 100:.3f}%")
                print(
                    f"  假设情绪开关开仓30%天数，则年化增益约: {estimated_boost * 250 * 100:.2f}%"
                )
                print(f"  预期年化: {11.66 + estimated_boost * 250 * 100:.2f}%")

            print("\n注意事项:")
            print("  1. 北向资金数据自2024-08-18后不再披露")
            print("  2. 当前测试仅基于7个月数据")
            print("  3. 实际效果需在首板低开策略中验证")

        else:
            print("合并后数据为空")
    else:
        print("合并数据为空")
else:
    print("北向数据为空，无法继续分析")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)

print("\n最终建议:")
print("基于相关性分析和收益对比，北向资金指标的有效性取决于:")
print("1. 北向净流入与市场收益的相关性强度")
print("2. 北向净流入>0时是否真的收益更高")
print("3. 实际策略回测验证")
print("\n当前结论为初步分析，建议进一步验证。")
