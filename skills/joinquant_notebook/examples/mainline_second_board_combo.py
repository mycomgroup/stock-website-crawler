from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime

"""
任务07v2：主线二板组合测试
测试主线（假弱高开）与二板的组合使用效果
"""


def get_mainline_signals(test_dates):
    """获取主线信号（假弱高开）"""
    signals = []

    for i in range(1, len(test_dates)):
        prev_date = test_dates[i - 1]
        curr_date = test_dates[i]

        if i % 20 == 0:
            print(
                f"主线信号进度：{i}/{len(test_dates)} ({i / len(test_dates) * 100:.1f}%)"
            )

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

                    if not (0.5 <= open_pct <= 1.5):
                        continue

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

                    signals.append(
                        {
                            "date": curr_date,
                            "stock": stock,
                            "open_pct": open_pct,
                            "intra_return": intra_return,
                            "max_return": max_return,
                            "market_cap": market_cap,
                            "position": position,
                            "type": "mainline",
                        }
                    )
                except Exception as e:
                    continue
        except Exception as e:
            continue

    return signals


def get_second_board_signals(test_dates):
    """获取二板信号"""
    signals = []

    def get_zt_stocks(date):
        all_stocks = get_all_securities("stock", date).index.tolist()
        all_stocks = [
            s
            for s in all_stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        df = get_price(
            all_stocks,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()
        zt_df = df[df["close"] == df["high_limit"]]
        return list(zt_df["code"])

    def filter_yzb(stock_list, date):
        result = []
        for stock in stock_list:
            df = get_price(stock, end_date=date, count=1, fields=["low", "high"])
            if df["low"].iloc[0] != df["high"].iloc[0]:
                result.append(stock)
        return result

    def get_hl_stock(initial_list, date):
        df = get_price(
            initial_list,
            end_date=date,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        df = df.dropna()
        df = df[df["close"] == df["high_limit"]]
        return list(df["code"])

    def get_shifted_date(date, days):
        all_days = [d.strftime("%Y-%m-%d") for d in get_all_trade_days()]
        if date in all_days:
            idx = all_days.index(date)
            return all_days[idx + days]
        return date

    def get_free_market_cap(stock, date):
        q = query(
            valuation.code, valuation.market_cap, valuation.circulating_market_cap
        ).filter(valuation.code == stock)
        df = get_fundamentals(q, date=date)
        if len(df) > 0:
            return float(df["circulating_market_cap"].iloc[0])
        return 0

    def get_turnover_ratio(stock, date):
        hsl = HSL([stock], date)
        if stock in hsl[0]:
            return hsl[0][stock]
        return 0

    for i in range(1, len(test_dates)):
        date = test_dates[i - 1]
        next_date = test_dates[i]

        if i % 20 == 0:
            print(
                f"二板信号进度：{i}/{len(test_dates)} ({i / len(test_dates) * 100:.1f}%)"
            )

        try:
            prev_date = get_shifted_date(date, -1)
            prev2_date = get_shifted_date(date, -2)

            initial_list = get_all_securities("stock", date).index.tolist()
            initial_list = [
                s
                for s in initial_list
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ]

            hl_1d = filter_yzb(get_hl_stock(initial_list, date), date)
            hl_2d = get_hl_stock(initial_list, prev_date)
            hl_3d = get_hl_stock(initial_list, prev2_date)

            stock_list = list(set(hl_1d) & set(hl_2d) - set(hl_3d))

            stock_list = [s for s in stock_list if get_turnover_ratio(s, date) < 30]

            if len(stock_list) == 0:
                continue

            stock_list_sorted = sorted(
                stock_list, key=lambda s: get_free_market_cap(s, date)
            )
            target_stock = stock_list_sorted[0] if len(stock_list_sorted) > 0 else None

            if target_stock is None:
                continue

            try:
                today_open = get_price(
                    target_stock,
                    end_date=next_date,
                    count=1,
                    fields=["open"],
                    panel=False,
                ).iloc[0]["open"]
                today_high = get_price(
                    target_stock,
                    end_date=next_date,
                    count=1,
                    fields=["high"],
                    panel=False,
                ).iloc[0]["high"]
                today_close = get_price(
                    target_stock,
                    end_date=next_date,
                    count=1,
                    fields=["close"],
                    panel=False,
                ).iloc[0]["close"]
                prev_close = get_price(
                    target_stock, end_date=date, count=1, fields=["close"], panel=False
                ).iloc[0]["close"]
                high_limit = get_price(
                    target_stock,
                    end_date=next_date,
                    count=1,
                    fields=["high_limit"],
                    panel=False,
                ).iloc[0]["high_limit"]
            except:
                continue

            open_pct = (today_open / prev_close - 1) * 100
            is_zt_open = today_open == high_limit

            if is_zt_open:
                continue

            buy_price = today_open * 1.005
            sell_price = today_high if today_high > buy_price else today_close

            profit_pct = (sell_price / buy_price - 1) * 100

            signals.append(
                {
                    "date": next_date,
                    "stock": target_stock,
                    "open_pct": open_pct,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "profit_pct": profit_pct,
                    "type": "second_board",
                }
            )
        except Exception as e:
            continue

    return signals


def analyze_overlap(mainline_signals, second_board_signals):
    """分析信号重叠情况"""
    mainline_df = pd.DataFrame(mainline_signals)
    second_board_df = pd.DataFrame(second_board_signals)

    if len(mainline_df) == 0 or len(second_board_df) == 0:
        return {
            "overlap_count": 0,
            "overlap_ratio": 0,
            "mainline_only_count": len(mainline_df),
            "second_board_only_count": len(second_board_df),
            "overlap_signals": [],
        }

    merged = pd.merge(
        mainline_df, second_board_df, on=["date", "stock"], how="outer", indicator=True
    )

    overlap = merged[merged["_merge"] == "both"]
    mainline_only = merged[merged["_merge"] == "left_only"]
    second_board_only = merged[merged["_merge"] == "right_only"]

    return {
        "overlap_count": len(overlap),
        "overlap_ratio": len(overlap) / (len(mainline_df) + len(second_board_df)) * 100,
        "mainline_only_count": len(mainline_only),
        "second_board_only_count": len(second_board_only),
        "overlap_signals": overlap.to_dict("records") if len(overlap) > 0 else [],
    }


def backtest_combo_scheme(
    scheme_name, mainline_signals, second_board_signals, test_dates
):
    """回测组合方案"""
    mainline_df = (
        pd.DataFrame(mainline_signals) if len(mainline_signals) > 0 else pd.DataFrame()
    )
    second_board_df = (
        pd.DataFrame(second_board_signals)
        if len(second_board_signals) > 0
        else pd.DataFrame()
    )

    results = {
        "scheme": scheme_name,
        "trades": [],
        "total_trades": 0,
        "win_rate": 0,
        "avg_return": 0,
        "cumulative_return": 0,
        "max_drawdown": 0,
        "monthly_returns": {},
    }

    portfolio_value = 100
    portfolio_history = []

    for date in test_dates[1:]:
        mainline_today = (
            mainline_df[mainline_df["date"] == date]
            if len(mainline_df) > 0
            else pd.DataFrame()
        )
        second_board_today = (
            second_board_df[second_board_df["date"] == date]
            if len(second_board_df) > 0
            else pd.DataFrame()
        )

        trade = None

        if scheme_name == "A":
            if len(mainline_today) > 0:
                best = mainline_today.sort_values("intra_return", ascending=False).iloc[
                    0
                ]
                trade = {
                    "date": date,
                    "stock": best["stock"],
                    "return": best["intra_return"],
                    "source": "mainline",
                }
            elif len(second_board_today) > 0:
                best = second_board_today.iloc[0]
                trade = {
                    "date": date,
                    "stock": best["stock"],
                    "return": best["profit_pct"],
                    "source": "second_board",
                }

        elif scheme_name == "B":
            if len(second_board_today) > 0:
                best = second_board_today.iloc[0]
                trade = {
                    "date": date,
                    "stock": best["stock"],
                    "return": best["profit_pct"],
                    "source": "second_board",
                }
            elif len(mainline_today) > 0:
                best = mainline_today.sort_values("intra_return", ascending=False).iloc[
                    0
                ]
                trade = {
                    "date": date,
                    "stock": best["stock"],
                    "return": best["intra_return"],
                    "source": "mainline",
                }

        elif scheme_name == "C":
            returns = []
            if len(mainline_today) > 0:
                returns.extend(mainline_today["intra_return"].tolist())
            if len(second_board_today) > 0:
                returns.extend(second_board_today["profit_pct"].tolist())

            if len(returns) > 0:
                avg_return = np.mean(returns)
                trade = {
                    "date": date,
                    "stock": "combo",
                    "return": avg_return,
                    "source": "both",
                }

        elif scheme_name == "D":
            mainline_best_return = 0
            second_board_best_return = 0

            if len(mainline_today) > 0:
                mainline_best = mainline_today.sort_values(
                    "intra_return", ascending=False
                ).iloc[0]
                mainline_best_return = mainline_best["intra_return"]

            if len(second_board_today) > 0:
                second_board_best = second_board_today.iloc[0]
                second_board_best_return = second_board_best["profit_pct"]

            if (
                mainline_best_return >= second_board_best_return
                and len(mainline_today) > 0
            ):
                best = mainline_today.sort_values("intra_return", ascending=False).iloc[
                    0
                ]
                trade = {
                    "date": date,
                    "stock": best["stock"],
                    "return": mainline_best_return,
                    "source": "mainline",
                }
            elif len(second_board_today) > 0:
                best = second_board_today.iloc[0]
                trade = {
                    "date": date,
                    "stock": best["stock"],
                    "return": second_board_best_return,
                    "source": "second_board",
                }

        if trade:
            results["trades"].append(trade)
            portfolio_value *= 1 + trade["return"] / 100
            portfolio_history.append(portfolio_value)

            month = date[:7]
            if month not in results["monthly_returns"]:
                results["monthly_returns"][month] = 0
            results["monthly_returns"][month] += trade["return"]

    results["total_trades"] = len(results["trades"])

    if results["total_trades"] > 0:
        returns = [t["return"] for t in results["trades"]]
        wins = [r for r in returns if r > 0]

        results["win_rate"] = len(wins) / results["total_trades"] * 100
        results["avg_return"] = np.mean(returns)
        results["cumulative_return"] = portfolio_value - 100

        peak = 100
        max_dd = 0
        for pv in portfolio_history:
            peak = max(peak, pv)
            dd = (peak - pv) / peak * 100
            max_dd = max(max_dd, dd)
        results["max_drawdown"] = max_dd

    return results


print("=" * 80)
print("任务07v2：主线二板组合测试")
print("=" * 80)

all_dates_2024 = list(get_trade_days(end_date="2024-12-31", count=250))
start_idx = all_dates_2024.index("2024-01-02") if "2024-01-02" in all_dates_2024 else 0
test_dates = all_dates_2024[start_idx:]

print(f"测试期间：2024-01-02 到 2024-12-31，共 {len(test_dates)} 个交易日")

print("\n" + "=" * 80)
print("获取主线信号（假弱高开）...")
print("=" * 80)

mainline_signals = get_mainline_signals(test_dates)

print(f"主线信号总数：{len(mainline_signals)}")
if len(mainline_signals) > 0:
    ml_df = pd.DataFrame(mainline_signals)
    print(f"主线平均收益：{ml_df['intra_return'].mean():.2f}%")
    print(f"主线胜率：{(ml_df['intra_return'] > 0).sum() / len(ml_df) * 100:.2f}%")

print("\n" + "=" * 80)
print("获取二板信号...")
print("=" * 80)

second_board_signals = get_second_board_signals(test_dates)

print(f"二板信号总数：{len(second_board_signals)}")
if len(second_board_signals) > 0:
    sb_df = pd.DataFrame(second_board_signals)
    print(f"二板平均收益：{sb_df['profit_pct'].mean():.2f}%")
    print(f"二板胜率：{(sb_df['profit_pct'] > 0).sum() / len(sb_df) * 100:.2f}%")

print("\n" + "=" * 80)
print("分析信号重叠情况...")
print("=" * 80)

overlap_analysis = analyze_overlap(mainline_signals, second_board_signals)

print(f"主线独立信号：{overlap_analysis['mainline_only_count']}")
print(f"二板独立信号：{overlap_analysis['second_board_only_count']}")
print(f"重叠信号：{overlap_analysis['overlap_count']}")
print(f"重叠比例：{overlap_analysis['overlap_ratio']:.2f}%")

print("\n" + "=" * 80)
print("测试组合方案...")
print("=" * 80)

scheme_A = backtest_combo_scheme(
    "A", mainline_signals, second_board_signals, test_dates
)
scheme_B = backtest_combo_scheme(
    "B", mainline_signals, second_board_signals, test_dates
)
scheme_C = backtest_combo_scheme(
    "C", mainline_signals, second_board_signals, test_dates
)
scheme_D = backtest_combo_scheme(
    "D", mainline_signals, second_board_signals, test_dates
)

print("\n方案A（主线优先）：")
print(f"  交易次数：{scheme_A['total_trades']}")
print(f"  胜率：{scheme_A['win_rate']:.2f}%")
print(f"  平均收益：{scheme_A['avg_return']:.2f}%")
print(f"  累计收益：{scheme_A['cumulative_return']:.2f}%")
print(f"  最大回撤：{scheme_A['max_drawdown']:.2f}%")

print("\n方案B（二板优先）：")
print(f"  交易次数：{scheme_B['total_trades']}")
print(f"  胜率：{scheme_B['win_rate']:.2f}%")
print(f"  平均收益：{scheme_B['avg_return']:.2f}%")
print(f"  累计收益：{scheme_B['cumulative_return']:.2f}%")
print(f"  最大回撤：{scheme_B['max_drawdown']:.2f}%")

print("\n方案C（并行平均）：")
print(f"  交易次数：{scheme_C['total_trades']}")
print(f"  胜率：{scheme_C['win_rate']:.2f}%")
print(f"  平均收益：{scheme_C['avg_return']:.2f}%")
print(f"  累计收益：{scheme_C['cumulative_return']:.2f}%")
print(f"  最大回撤：{scheme_C['max_drawdown']:.2f}%")

print("\n方案D（收益优先）：")
print(f"  交易次数：{scheme_D['total_trades']}")
print(f"  胜率：{scheme_D['win_rate']:.2f}%")
print(f"  平均收益：{scheme_D['avg_return']:.2f}%")
print(f"  累计收益：{scheme_D['cumulative_return']:.2f}%")
print(f"  最大回撤：{scheme_D['max_drawdown']:.2f}%")

print("\n" + "=" * 80)
print("样本外验证（2024-01-01之后）...")
print("=" * 80)

oos_dates = [d for d in test_dates if d >= "2024-01-01"]

oos_mainline = [s for s in mainline_signals if s["date"] >= "2024-01-01"]
oos_second_board = [s for s in second_board_signals if s["date"] >= "2024-01-01"]

print(f"样本外主线信号：{len(oos_mainline)}")
print(f"样本外二板信号：{len(oos_second_board)}")

oos_scheme_A = backtest_combo_scheme("A", oos_mainline, oos_second_board, oos_dates)
oos_scheme_B = backtest_combo_scheme("B", oos_mainline, oos_second_board, oos_dates)
oos_scheme_C = backtest_combo_scheme("C", oos_mainline, oos_second_board, oos_dates)
oos_scheme_D = backtest_combo_scheme("D", oos_mainline, oos_second_board, oos_dates)

print("\n样本外方案A：")
print(f"  交易次数：{oos_scheme_A['total_trades']}")
print(f"  累计收益：{oos_scheme_A['cumulative_return']:.2f}%")

print("\n样本外方案B：")
print(f"  交易次数：{oos_scheme_B['total_trades']}")
print(f"  累计收益：{oos_scheme_B['cumulative_return']:.2f}%")

print("\n样本外方案C：")
print(f"  交易次数：{oos_scheme_C['total_trades']}")
print(f"  累计收益：{oos_scheme_C['cumulative_return']:.2f}%")

print("\n样本外方案D：")
print(f"  交易次数：{oos_scheme_D['total_trades']}")
print(f"  累计收益：{oos_scheme_D['cumulative_return']:.2f}%")

print("\n" + "=" * 80)
print("最终结论...")
print("=" * 80)

best_scheme = max(
    [("A", scheme_A), ("B", scheme_B), ("C", scheme_C), ("D", scheme_D)],
    key=lambda x: x[1]["cumulative_return"],
)

print(f"最佳组合方案：{best_scheme[0]}")
print(f"  累计收益：{best_scheme[1]['cumulative_return']:.2f}%")
print(f"  胜率：{best_scheme[1]['win_rate']:.2f}%")
print(f"  最大回撤：{best_scheme[1]['max_drawdown']:.2f}%")

if overlap_analysis["overlap_ratio"] < 5:
    print(f"信号重叠比例低（{overlap_analysis['overlap_ratio']:.2f}%），适合组合使用")
else:
    print(f"信号重叠比例较高（{overlap_analysis['overlap_ratio']:.2f}%），需谨慎组合")

print("\n分析完成！")
