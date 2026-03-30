# 龙头底分型快速回测 - 2024年后样本外验证
# 只测试2024-01-01到2026-03-31，减少计算量

from jqdata import *
import pandas as pd

print("=" * 80)
print("龙头底分型样本外快速回测 (2024-01-01 ~ 2026-03-31)")
print("=" * 80)

START_DATE = "2024-01-01"
END_DATE = "2026-03-31"


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


def check_leader_pattern(stock, date):
    try:
        df_40 = get_price(
            stock,
            end_date=date,
            count=40,
            fields=["close", "high", "high_limit"],
            panel=False,
        )
        if len(df_40) < 40:
            return False

        high_40 = df_40["high"].max()
        current_close = df_40["close"].iloc[-1]

        if current_close < high_40 * 0.85:
            return False

        df_before = get_price(
            stock,
            end_date=date,
            count=12,
            fields=["close", "low", "high_limit"],
            panel=False,
        )
        if len(df_before) < 12:
            return False

        max_before = df_before["close"].max()
        min_before = df_before["close"].min()
        rate_before = (max_before - min_before) / min_before

        if rate_before < 0.50:
            return False

        limit_count = (df_before["close"] == df_before["high_limit"]).sum()
        if limit_count < 2:
            return False

        return True
    except:
        return False


def check_bottom_fractal(stock, date):
    try:
        df_3 = get_price(
            stock,
            end_date=date,
            count=3,
            fields=["open", "close", "high", "low", "high_limit"],
            panel=False,
        )
        if len(df_3) < 3:
            return False, False, False

        t0 = df_3.iloc[-1]
        t1 = df_3.iloc[-2]
        t2 = df_3.iloc[-3]

        is_zt = t0["close"] == t0["high_limit"]

        body_ratio = abs(t1["close"] - t1["open"]) / ((t1["close"] + t1["open"]) / 2)
        is_cross = body_ratio < 0.03

        open_gap = t0["open"] / t1["close"] - 1
        is_high_open = open_gap > 0.015

        return is_zt, is_cross, is_high_open
    except:
        return False, False, False


def backtest_signals():
    trade_days = get_trade_days(start_date=START_DATE, end_date=END_DATE)
    print(f"交易日数: {len(trade_days)}")

    signals_minute = []
    signals_daily = []

    sample_days = trade_days[::3]
    print(f"采样天数: {len(sample_days)}")

    for i, date in enumerate(sample_days[:60]):
        date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else date

        try:
            zt_stocks = get_zt_stocks(date_str)

            for stock in zt_stocks[:20]:
                try:
                    has_leader = check_leader_pattern(stock, date_str)
                    if not has_leader:
                        continue

                    is_zt, is_cross, is_high_open = check_bottom_fractal(
                        stock, date_str
                    )

                    if is_zt and is_cross and is_high_open:
                        next_day_idx = min(i + 1, len(sample_days) - 1)
                        next_date = sample_days[next_day_idx]
                        next_str = (
                            next_date.strftime("%Y-%m-%d")
                            if hasattr(next_date, "strftime")
                            else next_date
                        )

                        buy_price = get_price(
                            stock,
                            end_date=date_str,
                            count=1,
                            fields=["open"],
                            panel=False,
                        )
                        sell_price_1d = get_price(
                            stock,
                            end_date=next_str,
                            count=1,
                            fields=["close"],
                            panel=False,
                        )

                        if len(buy_price) > 0 and len(sell_price_1d) > 0:
                            ret_1d = (
                                sell_price_1d["close"].iloc[0]
                                / buy_price["open"].iloc[0]
                                - 1
                            ) * 100
                            signals_daily.append(
                                {
                                    "date": date_str,
                                    "stock": stock,
                                    "ret_1d": ret_1d,
                                    "type": "daily",
                                }
                            )
                except:
                    pass
        except:
            pass

        if (i + 1) % 20 == 0:
            print(f"进度: {i + 1}/{len(sample_days[:60])}")

    return pd.DataFrame(signals_daily)


print("\n开始回测...")
results_df = backtest_signals()

print("\n" + "=" * 80)
print("回测结果")
print("=" * 80)

if len(results_df) > 0:
    count = len(results_df)
    win_count = (results_df["ret_1d"] > 0).sum()
    win_rate = win_count / count * 100
    avg_ret = results_df["ret_1d"].mean()
    max_ret = results_df["ret_1d"].max()
    min_ret = results_df["ret_1d"].min()

    wins = results_df[results_df["ret_1d"] > 0]["ret_1d"]
    losses = abs(results_df[results_df["ret_1d"] < 0]["ret_1d"])
    profit_loss_ratio = (
        wins.mean() / losses.mean() if len(losses) > 0 and losses.mean() > 0 else 0
    )

    print(f"信号总数: {count}")
    print(f"胜率: {win_rate:.2f}%")
    print(f"平均收益: {avg_ret:.3f}%")
    print(f"最大收益: {max_ret:.3f}%")
    print(f"最大亏损: {min_ret:.3f}%")
    print(f"盈亏比: {profit_loss_ratio:.2f}")

    print("\n信号详情:")
    for i, row in results_df.iterrows():
        print(f"{row['date']} {row['stock']} 收益:{row['ret_1d']:.2f}%")

    print("\n结论判断:")
    if count < 10:
        print("样本太少（<10次），统计意义不足")
        recommendation = "No-Go"
    elif win_rate < 50:
        print("胜率<50%，策略失效")
        recommendation = "No-Go"
    elif profit_loss_ratio < 1.5:
        print("盈亏比<1.5，风险收益不匹配")
        recommendation = "Watch"
    else:
        print("样本充足，胜率合格，盈亏比合理")
        recommendation = "Go"

    print(f"\n推荐结论: {recommendation}")
else:
    print("未发现任何信号")
    print("推荐结论: No-Go")

print("\n研究完成!")
