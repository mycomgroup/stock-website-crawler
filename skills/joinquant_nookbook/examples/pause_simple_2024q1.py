from jqdata import *
import numpy as np
import json

print("=" * 50)
print("主线停手机制测试 - 2024Q1简化版")
print("=" * 50)

start_date = "2024-01-01"
end_date = "2024-03-31"
print(f"测试区间: {start_date} 至 {end_date}")

days = list(get_trade_days(start_date, end_date))
print(f"交易日数: {len(days)}")

trades = []
print("\n阶段1: 获取交易信号...")

for i in range(1, min(len(days), 30)):
    date = str(days[i])
    prev = str(days[i - 1])

    if i % 5 == 0:
        print(f"进度: {date}")

    try:
        stocks = get_all_securities("stock", date).index.tolist()[:300]
        stocks = [s for s in stocks if s[:2] != "68"]

        df_prev = get_price(
            stocks,
            end_date=prev,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        if df_prev.empty:
            continue

        hl = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()

        if len(hl) > 0:
            df_today = get_price(
                hl[:30],
                end_date=date,
                frequency="daily",
                fields=["open", "close"],
                count=1,
                panel=False,
            )

            if not df_today.empty:
                df_today = df_today.dropna()

                ratio_threshold = 1.01
                signals = df_today[
                    df_today["open"] / df_today["close"].shift(1) >= ratio_threshold
                ]

                if len(signals) > 0:
                    ret = (
                        (signals["close"] - signals["open"]) / signals["open"]
                    ).mean()

                    trades.append(
                        {
                            "date": date,
                            "return_pct": float(ret) * 100,
                            "is_win": ret > 0,
                        }
                    )

    except:
        pass

print(f"\n交易总数: {len(trades)}")

if len(trades) > 0:
    print("\n阶段2: 统计连亏...")

    consecutive_losses = []
    loss_count = 0

    for trade in trades:
        if not trade["is_win"]:
            loss_count += 1
        else:
            if loss_count > 0:
                consecutive_losses.append(loss_count)
            loss_count = 0

    if loss_count > 0:
        consecutive_losses.append(loss_count)

    if len(consecutive_losses) > 0:
        print(f"连亏事件数: {len(consecutive_losses)}")
        print(f"最大连亏: {max(consecutive_losses)}")
        print(f"平均连亏: {np.mean(consecutive_losses):.2f}")

    print("\n阶段3: 计算回撤...")

    equity = 100000
    peak = equity
    max_dd = 0

    for trade in trades:
        equity = equity * (1 + trade["return_pct"] / 100)
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak * 100
        if dd > max_dd:
            max_dd = dd

    print(f"最大回撤: {max_dd:.2f}%")

    total_ret = sum([t["return_pct"] for t in trades])
    win_rate = sum([1 for t in trades if t["is_win"]]) / len(trades) * 100

    print(f"总收益: {total_ret:.2f}%")
    print(f"胜率: {win_rate:.1f}%")

    print("\n阶段4: 测试停手机制...")

    def test_pause(trades, rule):
        paused = []
        pause_counter = 0
        loss_count = 0

        for trade in trades:
            if pause_counter > 0:
                pause_counter -= 1
                continue

            paused.append(trade)

            if not trade["is_win"]:
                loss_count += 1
            else:
                loss_count = 0

            if rule == "pause_3":
                if loss_count >= 3:
                    pause_counter = 3
                    loss_count = 0

        return paused

    no_pause = trades
    pause_3 = test_pause(trades, "pause_3")

    def calc_metrics(trades_list):
        returns = [t["return_pct"] for t in trades_list]
        total = sum(returns)

        equity = 100000
        peak = equity
        max_dd = 0

        for r in returns:
            equity = equity * (1 + r / 100)
            if equity > peak:
                peak = equity
            dd = (peak - equity) / peak * 100
            if dd > max_dd:
                max_dd = dd

        calmar = total / max_dd if max_dd > 0 else 999

        return {"return": total, "dd": max_dd, "calmar": calmar, "count": len(returns)}

    m1 = calc_metrics(no_pause)
    m2 = calc_metrics(pause_3)

    print("\n对比:")
    print(
        f"无停手: 收益{m1['return']:.2f}%, 回撤{m1['dd']:.2f}%, 卡玛{m1['calmar']:.2f}, 交易{m1['count']}"
    )
    print(
        f"连亏3停: 收益{m2['return']:.2f}%, 回撤{m2['dd']:.2f}%, 卡玛{m2['calmar']:.2f}, 交易{m2['count']}, 休息{len(trades) - m2['count']}天"
    )

    dd_improve = (m1["dd"] - m2["dd"]) / m1["dd"] * 100 if m1["dd"] > 0 else 0
    ret_change = (
        (m2["return"] - m1["return"]) / m1["return"] * 100 if m1["return"] != 0 else 0
    )

    print(f"\n回撤改善: {dd_improve:.1f}%")
    print(f"收益变化: {ret_change:.1f}%")

    result = {
        "trades_count": len(trades),
        "max_consecutive_loss": max(consecutive_losses) if consecutive_losses else 0,
        "max_dd_pct": max_dd,
        "no_pause": m1,
        "pause_3": m2,
        "dd_improve_pct": dd_improve,
        "ret_change_pct": ret_change,
    }

    print("\n保存结果...")
    with open(
        "/Users/fengzhi/Downloads/git/testlixingren/output/joinquant_pause_2024q1.json",
        "w",
    ) as f:
        json.dump(result, f, indent=2)
    print("完成")

else:
    print("无交易数据")

print("\n=" * 50)
print("测试完成")
print("=" * 50)
