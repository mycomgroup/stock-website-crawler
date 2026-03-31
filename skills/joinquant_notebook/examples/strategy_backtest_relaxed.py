# 主线信号放宽 - 策略层回测（模拟）
from jqdata import *
import pandas as pd
import numpy as np

print("主线信号放宽 - 策略层回测（模拟）")

trade_days = get_trade_days("2024-01-01", "2024-12-31")
print(f"全年交易日数: {len(trade_days)}")

test_periods = [
    {"name": "1月初", "indices": range(5, 20)},
    {"name": "2月初", "indices": range(25, 40)},
    {"name": "3月初", "indices": range(40, 55)},
    {"name": "6月初", "indices": range(100, 115)},
]

versions = {
    "原版_假弱高开": (50, 150, 0.30, 0.5, 1.5),
    "放宽C_假弱高开": (40, 200, 0.50, 0.5, 1.5),
}

all_trades = {}

for vname, (cap_min, cap_max, pos_max, open_min, open_max) in versions.items():
    print(f"\n{'=' * 60}")
    print(f"策略版本: {vname}")
    print(f"{'=' * 60}")

    trades = []

    for period in test_periods:
        print(f"时间段: {period['name']}")

        for idx in period["indices"]:
            if idx >= len(trade_days) or idx < 1:
                continue

            prev_date = trade_days[idx - 1].strftime("%Y-%m-%d")
            curr_date = trade_days[idx].strftime("%Y-%m-%d")

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

                if len(limit_stocks) == 0:
                    continue

                price_curr = get_price(
                    limit_stocks,
                    end_date=curr_date,
                    count=1,
                    fields=["open", "close", "high"],
                    panel=False,
                )

                if price_curr.empty:
                    continue

                q = query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code.in_(limit_stocks),
                    valuation.circulating_market_cap >= cap_min,
                    valuation.circulating_market_cap <= cap_max,
                )

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

                        if not (open_min <= open_pct <= open_max):
                            continue

                        val_row = val_data[val_data["code"] == stock]
                        if len(val_row) == 0:
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

                        if position > pos_max:
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

                        trades.append(
                            {
                                "date": curr_date,
                                "stock": stock,
                                "open_pct": open_pct,
                                "return": intra_return,
                            }
                        )

                    except:
                        continue

            except:
                continue

    if len(trades) > 0:
        df_trades = pd.DataFrame(trades)

        total_return = df_trades["return"].sum()
        avg_return = df_trades["return"].mean()
        win_rate = (df_trades["return"] > 0).mean() * 100

        daily_returns = df_trades.groupby("date")["return"].mean()

        cumulative = (1 + daily_returns / 100).cumprod() - 1

        if len(cumulative) > 0:
            max_drawdown = (cumulative - cumulative.expanding().max()).min() * 100
        else:
            max_drawdown = 0

        sharpe = avg_return / (
            df_trades["return"].std() if df_trades["return"].std() > 0 else 1
        )

        calmar = (
            abs(avg_return * len(trade_days) / 100 / (abs(max_drawdown) / 100))
            if max_drawdown != 0
            else 0
        )

        annual_return = avg_return * len(trade_days) / len(df_trades.groupby("date"))

        all_trades[vname] = {
            "trades": len(trades),
            "total_return": total_return,
            "avg_return": avg_return,
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
            "sharpe": sharpe,
            "calmar": calmar,
            "annual_return": annual_return,
            "days": len(df_trades.groupby("date")),
        }

        print(f"\n策略回测结果:")
        print(f"  交易次数: {len(trades)}")
        print(f"  交易天数: {len(df_trades.groupby('date'))}")
        print(f"  累计收益: {total_return:.2f}%")
        print(f"  日均收益: {avg_return:.2f}%")
        print(f"  胜率: {win_rate:.2f}%")
        print(f"  最大回撤: {max_drawdown:.2f}%")
        print(f"  夏普比率: {sharpe:.2f}")
        print(f"  卡玛比率: {calmar:.2f}")
        print(f"  年化收益: {annual_return:.2f}%")

print("\n" + "=" * 60)
print("策略对比汇总")
print("=" * 60)

print("\n版本 | 交易次数 | 年化收益 | 最大回撤 | 夏普 | 卡玛 | 胜率")
print("-----|----------|----------|----------|------|------|------")

for vname in ["原版_假弱高开", "放宽C_假弱高开"]:
    if vname in all_trades:
        r = all_trades[vname]
        print(
            f"{vname.replace('_假弱高开', '')} | {r['trades']} | {r['annual_return']:.2f}% | {r['max_drawdown']:.2f}% | {r['sharpe']:.2f} | {r['calmar']:.2f} | {r['win_rate']:.2f}%"
        )

print("=" * 60)
