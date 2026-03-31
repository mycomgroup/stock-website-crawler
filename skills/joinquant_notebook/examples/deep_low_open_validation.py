from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

"""
任务09v2：深度低开专项验证
深度低开：-5%~-3%
目标：判断是否应该删除或保留
"""


def classify_open_type(open_pct):
    if 0.5 <= open_pct <= 1.5:
        return "假弱高开"
    elif -3.0 <= open_pct < -1.0:
        return "真低开A"
    elif -1.0 <= open_pct < 0.0:
        return "真低开B"
    elif 0.0 <= open_pct < 0.5:
        return "边界A_平开附近"
    elif -5.0 <= open_pct < -3.0:
        return "边界B_深度低开"
    elif 1.5 <= open_pct <= 2.5:
        return "边界C_微高开"
    else:
        return "其他"


print("开始深度低开专项验证分析...")
print("=" * 80)

signals_by_year = {}
total_zt_by_year = {}

years = [2021, 2022, 2023, 2024]

for year in years:
    print(f"\n处理 {year} 年数据...")
    year_signals = []
    year_zt_count = 0

    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    all_dates = list(get_trade_days(end_date=end_date, count=250))
    test_dates = [str(d) for d in all_dates if str(d).startswith(str(year))]

    print(f"{year}年交易日数：{len(test_dates)}")

    for i in range(1, len(test_dates)):
        prev_date = test_dates[i - 1]
        curr_date = test_dates[i]

        if i % 20 == 0:
            print(f"  进度：{i}/{len(test_dates)} ({i / len(test_dates) * 100:.1f}%)")

        try:
            all_stocks = get_all_securities("stock", prev_date).index.tolist()

            price_prev = get_price(
                all_stocks,
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )

            if price_prev.empty:
                continue

            limit_stocks = price_prev[
                abs(price_prev["close"] - price_prev["high_limit"])
                / price_prev["high_limit"]
                < 0.01
            ]["code"].tolist()

            year_zt_count += len(limit_stocks)

            if len(limit_stocks) == 0:
                continue

            price_curr = get_price(
                limit_stocks,
                end_date=curr_date,
                count=1,
                fields=["open", "close", "high", "high_limit"],
                panel=False,
            )

            if price_curr.empty:
                continue

            q = query(
                valuation.code,
                valuation.circulating_market_cap,
            ).filter(valuation.code.in_(limit_stocks))

            val_data = get_fundamentals(q, date=curr_date)

            if val_data.empty:
                continue

            for stock in limit_stocks:
                try:
                    prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                    curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                    prev_close = float(prev_row["close"])
                    curr_open = float(curr_row["open"])
                    curr_close = float(curr_row["close"])
                    curr_high = float(curr_row["high"])

                    open_pct = (curr_open - prev_close) / prev_close * 100

                    if -10 <= open_pct <= 10:
                        val_row = val_data[val_data["code"] == stock]
                        if len(val_row) == 0:
                            continue

                        market_cap = float(val_row["circulating_market_cap"].iloc[0])

                        if not (50 <= market_cap <= 150):
                            continue

                        prices_15d = get_price(
                            stock,
                            end_date=prev_date,
                            count=15,
                            fields=["close"],
                            panel=False,
                        )

                        if len(prices_15d) < 10:
                            continue

                        high_15d = float(prices_15d["close"].max())
                        low_15d = float(prices_15d["close"].min())

                        if high_15d == low_15d:
                            continue

                        position = (prev_close - low_15d) / (high_15d - low_15d)

                        if position > 0.30:
                            continue

                        lb_data_2d = get_price(
                            stock,
                            end_date=prev_date,
                            count=2,
                            fields=["close", "high_limit"],
                            panel=False,
                        )

                        if len(lb_data_2d) >= 2:
                            prev_prev_close = float(lb_data_2d["close"].iloc[0])
                            prev_prev_limit = float(lb_data_2d["high_limit"].iloc[0])

                            if (
                                abs(prev_prev_close - prev_prev_limit) / prev_prev_limit
                                < 0.01
                            ):
                                continue

                        intra_return = (curr_close - curr_open) / curr_open * 100
                        max_return = (curr_high - curr_open) / curr_open * 100

                        year_signals.append(
                            {
                                "date": curr_date,
                                "stock": stock,
                                "open_pct": open_pct,
                                "intra_return": intra_return,
                                "max_return": max_return,
                                "open_type": classify_open_type(open_pct),
                                "is_win": intra_return > 0,
                                "market_cap": market_cap,
                                "position": position,
                            }
                        )
                except Exception as e:
                    continue
        except Exception as e:
            continue

    signals_by_year[year] = year_signals
    total_zt_by_year[year] = year_zt_count

    if len(year_signals) > 0:
        df = pd.DataFrame(year_signals)
        deep_low = df[df["open_type"] == "边界B_深度低开"]
        print(f"  {year}年深度低开样本数：{len(deep_low)}")
    else:
        print(f"  {year}年无信号")

print("\n" + "=" * 80)
print("汇总统计")
print("=" * 80)

all_signals = []
for year, sigs in signals_by_year.items():
    all_signals.extend(sigs)

if len(all_signals) == 0:
    print("未找到任何首板信号")
else:
    df_all = pd.DataFrame(all_signals)

    print(f"\n总涨停板天数：")
    for year, zt_count in total_zt_by_year.items():
        print(f"  {year}年：{zt_count}")

    print(f"\n筛选后首板信号总数：{len(df_all)}")

    type_stats_all = []

    for open_type in df_all["open_type"].unique():
        if open_type == "其他":
            continue

        subset = df_all[df_all["open_type"] == open_type]

        stats = {
            "open_type": open_type,
            "count": len(subset),
            "avg_open_pct": subset["open_pct"].mean(),
            "avg_intra_return": subset["intra_return"].mean(),
            "avg_max_return": subset["max_return"].mean(),
            "win_rate": subset["is_win"].sum() / len(subset) * 100,
            "min_open_pct": subset["open_pct"].min(),
            "max_open_pct": subset["open_pct"].max(),
        }

        type_stats_all.append(stats)

    results_df_all = pd.DataFrame(type_stats_all)
    results_df_all = results_df_all.sort_values("avg_max_return", ascending=False)

    print("\n结构分组收益对比 (2021-2024全周期)")
    print("=" * 80)
    print(results_df_all.to_string(index=False))

    print("\n" + "=" * 80)
    print("深度低开专项分析")
    print("=" * 80)

    deep_low_all = df_all[df_all["open_type"] == "边界B_深度低开"]

    if len(deep_low_all) > 0:
        print(f"\n深度低开总样本数：{len(deep_low_all)}")
        print(f"平均开盘涨跌幅：{deep_low_all['open_pct'].mean():.2f}%")
        print(f"平均日内收益：{deep_low_all['intra_return'].mean():.2f}%")
        print(f"平均最高收益：{deep_low_all['max_return'].mean():.2f}%")
        print(f"胜率：{deep_low_all['is_win'].sum() / len(deep_low_all) * 100:.1f}%")
        print(
            f"开盘涨跌幅范围：{deep_low_all['open_pct'].min():.2f}% ~ {deep_low_all['open_pct'].max():.2f}%"
        )

        print("\n深度低开各年份样本数：")
        for year in years:
            year_deep = deep_low_all[
                deep_low_all["date"].astype(str).str.startswith(str(year))
            ]
            print(f"  {year}年：{len(year_deep)}个")
            if len(year_deep) > 0:
                print(f"    日内收益均值：{year_deep['intra_return'].mean():.2f}%")
                print(
                    f"    胜率：{year_deep['is_win'].sum() / len(year_deep) * 100:.1f}%"
                )

        print("\n深度低开收益分布：")
        print(
            f"  正收益数量：{deep_low_all[deep_low_all['intra_return'] > 0].shape[0]}个"
        )
        print(
            f"  负收益数量：{deep_low_all[deep_low_all['intra_return'] <= 0].shape[0]}个"
        )
        print(f"  最大收益：{deep_low_all['intra_return'].max():.2f}%")
        print(f"  最大亏损：{deep_low_all['intra_return'].min():.2f}%")

        print("\n深度低开与其他结构对比：")
        for open_type in results_df_all["open_type"].unique():
            if open_type == "边界B_深度低开":
                continue
            type_data = results_df_all[results_df_all["open_type"] == open_type].iloc[0]
            print(f"\n  {open_type}：")
            print(f"    样本数：{type_data['count']}个")
            print(f"    日内收益：{type_data['avg_intra_return']:.2f}%")
            print(f"    胜率：{type_data['win_rate']:.1f}%")

    print("\n" + "=" * 80)
    print("2024-01-01后样本外结果")
    print("=" * 80)

    df_2024 = df_all[df_all["date"].astype(str).str.startswith("2024")]

    if len(df_2024) > 0:
        type_stats_2024 = []

        for open_type in df_2024["open_type"].unique():
            if open_type == "其他":
                continue

            subset = df_2024[df_2024["open_type"] == open_type]

            stats = {
                "open_type": open_type,
                "count": len(subset),
                "avg_open_pct": subset["open_pct"].mean(),
                "avg_intra_return": subset["intra_return"].mean(),
                "avg_max_return": subset["max_return"].mean(),
                "win_rate": subset["is_win"].sum() / len(subset) * 100,
            }

            type_stats_2024.append(stats)

        results_df_2024 = pd.DataFrame(type_stats_2024)
        results_df_2024 = results_df_2024.sort_values(
            "avg_intra_return", ascending=False
        )

        print("\n2024年结构分组收益对比")
        print("=" * 80)
        print(results_df_2024.to_string(index=False))

        deep_low_2024 = df_2024[df_2024["open_type"] == "边界B_深度低开"]

        if len(deep_low_2024) > 0:
            print(f"\n2024年深度低开样本数：{len(deep_low_2024)}")
            print(f"日内收益均值：{deep_low_2024['intra_return'].mean():.2f}%")
            print(
                f"胜率：{deep_low_2024['is_win'].sum() / len(deep_low_2024) * 100:.1f}%"
            )

    print("\n" + "=" * 80)
    print("最终判定")
    print("=" * 80)

    if len(deep_low_all) >= 30:
        avg_return = deep_low_all["intra_return"].mean()
        win_rate = deep_low_all["is_win"].sum() / len(deep_low_all) * 100

        print(f"\n深度低开样本数：{len(deep_low_all)}个（≥30）")
        print(f"平均日内收益：{avg_return:.2f}%")
        print(f"胜率：{win_rate:.1f}%")

        if avg_return > 0.5 and win_rate > 45:
            print("\n判定：推荐保留")
            print("理由：样本充足，收益正，胜率合理，可作为备选版本")
        elif avg_return > 0 or win_rate > 45:
            print("\n判定：建议保留")
            print("理由：样本充足，有改进空间，可通过筛选优化")
        else:
            print("\n判定：建议删除")
            print("理由：样本充足但收益太差，负收益或胜率过低")
    else:
        print(f"\n深度低开样本数：{len(deep_low_all)}个（<30）")
        print("判定：暂不删除，需补充更多样本")
        print("理由：样本不足，无法做出可靠判断")

    output_file = "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output/deep_low_open_validation.json"

    os.makedirs(
        "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook/output",
        exist_ok=True,
    )

    output_data = {
        "timestamp": datetime.now().isoformat(),
        "total_signals": len(df_all),
        "deep_low_count": len(deep_low_all),
        "deep_low_avg_return": float(deep_low_all["intra_return"].mean())
        if len(deep_low_all) > 0
        else None,
        "deep_low_win_rate": float(
            deep_low_all["is_win"].sum() / len(deep_low_all) * 100
        )
        if len(deep_low_all) > 0
        else None,
        "results_all": results_df_all.to_dict("records"),
        "results_2024": results_df_2024.to_dict("records") if len(df_2024) > 0 else [],
        "yearly_stats": {
            str(year): {
                "total_zt": total_zt_by_year.get(year, 0),
                "signals": len(signals_by_year.get(year, [])),
            }
            for year in years
        },
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存至: {output_file}")

print("\n分析完成！")
