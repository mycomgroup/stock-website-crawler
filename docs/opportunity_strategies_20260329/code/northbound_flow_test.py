from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("北向资金流向指标深挖测试")
print("=" * 60)
print("时间范围: 2024-01-01 至 2024-08-17")
print("说明: 北向资金买卖数据自2024-08-18后不再披露")
print("=" * 60)

START_DATE = "2024-01-01"
END_DATE = "2024-08-17"
BENCHMARK = "000300.XSHG"

trade_days = get_trade_days(start_date=START_DATE, end_date=END_DATE)
print(f"测试天数: {len(trade_days)} 个交易日")

print("\n第一部分: 获取北向资金数据")
print("-" * 40)

northbound_data = []
for day in trade_days:
    try:
        q = query(finance.STK_ML_QUOTA).filter(
            finance.STK_ML_QUOTA.day == day,
            finance.STK_ML_QUOTA.link_id.in_([310001, 310002]),
        )
        df = finance.run_query(q)

        if len(df) > 0:
            buy_total = df["buy_amount"].sum()
            sell_total = df["sell_amount"].sum()
            net_flow = buy_total - sell_total

            northbound_data.append(
                {
                    "date": day,
                    "buy_amount": buy_total,
                    "sell_amount": sell_total,
                    "net_flow": net_flow,
                    "sum_amount": df["sum_amount"].sum(),
                }
            )
    except Exception as e:
        continue

nb_df = pd.DataFrame(northbound_data)
nb_df["date"] = pd.to_datetime(nb_df["date"])
nb_df = nb_df.sort_values("date")

nb_df["net_flow_5d_ma"] = nb_df["net_flow"].rolling(5).mean()
nb_df["net_flow_cumulative"] = nb_df["net_flow"].cumsum()

print(f"北向资金数据条数: {len(nb_df)}")
print(f"北向净流入均值: {nb_df['net_flow'].mean() / 1e8:.2f}亿")
print(f"北向净流入累计: {nb_df['net_flow_cumulative'].iloc[-1] / 1e8:.2f}亿")

print("\n第二部分: 计算情绪指标（涨停家数+连板数）")
print("-" * 40)

sentiment_data = []
for day in trade_days:
    try:
        stocks = get_all_securities(types=["stock"], date=day)
        prices = get_price(
            list(stocks.index),
            end_date=day,
            count=2,
            fields=["close", "high_limit", "low_limit"],
            panel=False,
        )

        if len(prices) == 0:
            continue

        prev_close = prices[prices["time"] == prices["time"].unique()[0]]
        today_data = prices[prices["time"] == prices["time"].unique()[1]]

        today_data = today_data[today_data["close"] == today_data["high_limit"]]
        zt_count = len(today_data)

        max_lianban = 1
        if zt_count > 0:
            zt_stocks = today_data["code"].tolist()
            for stock in zt_stocks:
                stock_prices = get_price(
                    stock,
                    end_date=day,
                    count=10,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                if len(stock_prices) >= 2:
                    lianban_count = 0
                    for i in range(len(stock_prices) - 1, 0, -1):
                        if (
                            stock_prices.iloc[i]["close"]
                            == stock_prices.iloc[i]["high_limit"]
                        ):
                            lianban_count += 1
                        else:
                            break
                    max_lianban = max(max_lianban, lianban_count)

        sentiment_data.append(
            {"date": day, "zt_count": zt_count, "max_lianban": max_lianban}
        )
    except Exception as e:
        continue

sent_df = pd.DataFrame(sentiment_data)
sent_df["date"] = pd.to_datetime(sent_df["date"])

print(f"情绪数据条数: {len(sent_df)}")
print(f"涨停家数均值: {sent_df['zt_count'].mean():.1f}")
print(f"最高连板均值: {sent_df['max_lianban'].mean():.1f}")

print("\n第三部分: 合并数据")
print("-" * 40)

merged_df = pd.merge(sent_df, nb_df, on="date", how="inner")
merged_df = merged_df.sort_values("date")

print(f"合并数据条数: {len(merged_df)}")

merged_df["sentiment_switch"] = (
    (merged_df["zt_count"] >= 30) & (merged_df["max_lianban"] >= 2)
).astype(int)

merged_df["northbound_positive"] = (merged_df["net_flow"] > 0).astype(int)
merged_df["northbound_5d_positive"] = (merged_df["net_flow_5d_ma"] > 0).astype(int)

merged_df["switch_A"] = merged_df["sentiment_switch"]
merged_df["switch_B1"] = (
    merged_df["sentiment_switch"] & merged_df["northbound_positive"]
)
merged_df["switch_B2"] = (
    merged_df["sentiment_switch"] & merged_df["northbound_5d_positive"]
)

print("\n开关触发统计:")
print(
    f"  A组（原始情绪）: 开仓天数={merged_df['switch_A'].sum()}, 比例={merged_df['switch_A'].mean() * 100:.1f}%"
)
print(
    f"  B1组（情绪+北向净流入>0）: 开仓天数={merged_df['switch_B1'].sum()}, 比例={merged_df['switch_B1'].mean() * 100:.1f}%"
)
print(
    f"  B2组（情绪+北向5日MA>0）: 开仓天数={merged_df['switch_B2'].sum()}, 比例={merged_df['switch_B2'].mean() * 100:.1f}%"
)

print("\n第四部分: 首板低开策略回测")
print("-" * 40)


def run_first_board_low_open_strategy(switch_column, merged_data):
    daily_returns = []
    position = 0
    entry_price = 0

    for idx, row in merged_data.iterrows():
        date = row["date"]
        switch = row[switch_column]

        try:
            stocks = get_all_securities(types=["stock"], date=date)

            prev_date = date - timedelta(days=1)
            if prev_date not in merged_data["date"].values:
                continue

            prev_prices = get_price(
                list(stocks.index),
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )

            zt_stocks_prev = prev_prices[
                prev_prices["close"] == prev_prices["high_limit"]
            ]["code"].tolist()

            if len(zt_stocks_prev) == 0:
                continue

            today_open = get_price(
                zt_stocks_prev,
                end_date=date,
                count=1,
                fields=["open", "close"],
                panel=False,
            )

            if len(today_open) == 0:
                continue

            prev_close_prices = prev_prices[
                prev_prices["code"].isin(today_open["code"].tolist())
            ]
            prev_close_dict = dict(
                zip(prev_close_prices["code"], prev_close_prices["close"])
            )

            candidates = []
            for _, price_row in today_open.iterrows():
                code = price_row["code"]
                if code in prev_close_dict:
                    open_pct = (price_row["open"] / prev_close_dict[code] - 1) * 100

                    if -1.0 <= open_pct <= 0.0:
                        candidates.append(
                            {
                                "code": code,
                                "open_pct": open_pct,
                                "close": price_row["close"],
                            }
                        )

            if len(candidates) > 0 and switch == 1:
                best = candidates[0]
                daily_return = best["close"] / best["open"] - 1
                daily_returns.append(
                    {"date": date, "return": daily_return, "code": best["code"]}
                )
        except Exception as e:
            continue

    return pd.DataFrame(daily_returns)


print("\n运行A组（原始情绪）...")
returns_A = run_first_board_low_open_strategy("switch_A", merged_df)

print("\n运行B1组（情绪+北向净流入>0）...")
returns_B1 = run_first_board_low_open_strategy("switch_B1", merged_df)

print("\n运行B2组（情绪+北向5日MA>0）...")
returns_B2 = run_first_board_low_open_strategy("switch_B2", merged_df)

print("\n第五部分: 回测结果对比")
print("=" * 60)


def calculate_metrics(returns_df):
    if len(returns_df) == 0:
        return {
            "样本数": 0,
            "平均收益": "N/A",
            "胜率": "N/A",
            "累计收益": "N/A",
            "年化收益": "N/A",
            "夏普比率": "N/A",
            "最大回撤": "N/A",
        }

    avg_return = returns_df["return"].mean()
    win_rate = (returns_df["return"] > 0).mean()
    cumulative_return = returns_df["return"].sum()

    returns_df["cumulative"] = returns_df["return"].cumsum()
    returns_df["peak"] = returns_df["cumulative"].cummax()
    returns_df["drawdown"] = returns_df["cumulative"] - returns_df["peak"]
    max_drawdown = returns_df["drawdown"].min()

    annual_return = avg_return * 250

    std_return = returns_df["return"].std()
    sharpe = annual_return / (std_return * np.sqrt(250)) if std_return > 0 else 0

    return {
        "样本数": len(returns_df),
        "平均收益": f"{avg_return * 100:.2f}%",
        "胜率": f"{win_rate * 100:.1f}%",
        "累计收益": f"{cumulative_return * 100:.2f}%",
        "年化收益": f"{annual_return * 100:.2f}%",
        "夏普比率": f"{sharpe:.2f}",
        "最大回撤": f"{max_drawdown * 100:.2f}%",
    }


metrics_A = calculate_metrics(returns_A)
metrics_B1 = calculate_metrics(returns_B1)
metrics_B2 = calculate_metrics(returns_B2)

print("\n指标对比表:")
print("-" * 80)
print(
    f"{'指标':<15} {'A组（原始情绪）':<20} {'B1组（+北向净流入）':<20} {'B2组（+北向5日MA）':<20}"
)
print("-" * 80)

for key in metrics_A.keys():
    print(f"{key:<15} {metrics_A[key]:<20} {metrics_B1[key]:<20} {metrics_B2[key]:<20}")

print("\n第六部分: 结论")
print("=" * 60)

if len(returns_A) > 0 and len(returns_B1) > 0:
    avg_A = returns_A["return"].mean()
    avg_B1 = returns_B1["return"].mean()
    avg_B2 = returns_B2["return"].mean()

    improvement_B1 = avg_B1 - avg_A
    improvement_B2 = avg_B2 - avg_A

    print(f"\n增益分析:")
    print(f"  B1组 vs A组: 平均收益提升 {improvement_B1 * 100:.2f}%")
    print(f"  B2组 vs A组: 平均收益提升 {improvement_B2 * 100:.2f}%")

    if improvement_B1 > 0.001 or improvement_B2 > 0.001:
        print("\n结论: Go - 北向资金指标有增益")
        print("建议: 采用B1或B2方案")
    elif improvement_B1 < -0.001 or improvement_B2 < -0.001:
        print("\n结论: No-Go - 北向资金指标为负贡献")
        print("建议: 不纳入北向资金指标")
    else:
        print("\n结论: Watch - 北向资金指标无明显增益")
        print("建议: 继续观察，暂不纳入")
else:
    print("\n警告: 数据不足，无法得出结论")

print("\n第七部分: 北向资金有效性分析")
print("-" * 40)

merged_df["return_available"] = merged_df["date"].isin(
    returns_A["date"].values if len(returns_A) > 0 else []
)

if merged_df["return_available"].sum() > 0:
    valid_dates = merged_df[merged_df["return_available"]].copy()

    correlation_zt_nb = valid_dates["zt_count"].corr(valid_dates["net_flow"])
    correlation_return_nb = (
        returns_A["return"].corr(
            merged_df[merged_df["date"].isin(returns_A["date"])]["net_flow"].values
        )
        if len(returns_A) > 0
        else 0
    )

    print(f"涨停家数与北向净流入相关性: {correlation_zt_nb:.3f}")
    print(f"日内收益与北向净流入相关性: {correlation_return_nb:.3f}")

    high_sentiment = merged_df[merged_df["sentiment_switch"] == 1]
    nb_positive_high_sent = high_sentiment["northbound_positive"].mean()

    print(f"情绪开仓时北向净流入>0比例: {nb_positive_high_sent * 100:.1f}%")

    if nb_positive_high_sent > 0.5:
        print("  北向资金与情绪指标一致度高，可作辅助验证")
    else:
        print("  北向资金与情绪指标一致性较低，需谨慎使用")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)

print("\n关键发现:")
print(f"1. 北向数据可用期: {START_DATE} 至 {END_DATE} ({len(nb_df)}天)")
print(f"2. A组样本数: {metrics_A['样本数']}")
print(f"3. B1组样本数: {metrics_B1['样本数']}")
print(f"4. B2组样本数: {metrics_B2['样本数']}")
