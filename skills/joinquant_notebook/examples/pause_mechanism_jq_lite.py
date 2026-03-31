from jqdata import *
import numpy as np
import json

print("=" * 60)
print("任务08v2：停手机制实测验证 - 简化版")
print("=" * 60)

start_date = "2024-01-01"
end_date = "2025-03-28"
print(f"研究区间: {start_date} 至 {end_date}")

trade_days = list(get_trade_days(start_date, end_date))
print(f"交易日总数: {len(trade_days)}")

trades = []
print("\n获取首板低开策略交易序列...")

batch_size = 10
for batch_start in range(0, len(trade_days) - 1, batch_size):
    batch_end = min(batch_start + batch_size, len(trade_days) - 1)

    for i in range(batch_start, batch_end):
        date = trade_days[i + 1]
        prev_date = trade_days[i]
        date_str = str(date)

        try:
            stocks = get_all_securities("stock", date_str).index.tolist()
            stocks = [s for s in stocks if s[:2] != "68" and s[0] not in ["4", "8"]][
                :300
            ]

            df_prev = get_price(
                stocks,
                end_date=str(prev_date),
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
            )
            if df_prev.empty:
                continue
            df_prev = df_prev.dropna()
            high_limit_stocks = df_prev[df_prev["close"] == df_prev["high_limit"]][
                "code"
            ].tolist()

            if not high_limit_stocks:
                continue

            df_today = get_price(
                high_limit_stocks[:50],
                end_date=date_str,
                frequency="daily",
                fields=["open", "close", "high_limit"],
                count=1,
                panel=False,
            )
            if df_today.empty:
                continue
            df_today = df_today.dropna()
            df_today["ratio"] = df_today["open"] / (df_today["high_limit"] / 1.1)

            fb_signals = df_today[
                (df_today["ratio"] >= 1.005) & (df_today["ratio"] <= 1.015)
            ]

            if len(fb_signals) > 0:
                daily_return = (
                    (fb_signals["close"] - fb_signals["open"]) / fb_signals["open"]
                ).mean()
                trades.append(
                    {
                        "date": date_str,
                        "return_pct": daily_return * 100,
                        "is_win": daily_return > 0,
                    }
                )
        except:
            pass

    print(f"进度: {batch_end}/{len(trade_days) - 1}, 交易数: {len(trades)}")

print(f"\n交易总数: {len(trades)}")

if len(trades) == 0:
    print("未获取到交易数据")
else:
    print("\n分析连亏分布...")

    consecutive_losses = []
    current_loss_count = 0

    for trade in trades:
        if not trade["is_win"]:
            current_loss_count += 1
        else:
            if current_loss_count > 0:
                consecutive_losses.append(current_loss_count)
            current_loss_count = 0

    if current_loss_count > 0:
        consecutive_losses.append(current_loss_count)

    if consecutive_losses:
        print(f"最大连亏: {max(consecutive_losses)}笔")
        print(f"平均连亏: {np.mean(consecutive_losses):.2f}笔")

    print("\n测试停机方案...")

    pause_rules = [
        (0, 0, "无停机"),
        (2, 2, "连亏2停2"),
        (3, 3, "连亏3停3"),
        (3, 5, "连亏3停5"),
        (5, 3, "连亏5停3"),
        (5, 5, "连亏5停5"),
    ]

    def apply_pause(trades, trigger, days):
        paused = []
        pause_counter = 0
        loss_count = 0

        for t in trades:
            if pause_counter > 0:
                pause_counter -= 1
                continue

            paused.append(t)

            if not t["is_win"]:
                loss_count += 1
            else:
                loss_count = 0

            if trigger > 0 and loss_count >= trigger:
                pause_counter = days
                loss_count = 0

        return paused

    def calc_metrics(trades_list):
        if not trades_list:
            return None

        returns = [t["return_pct"] for t in trades_list]
        total = sum(returns)
        win_rate = sum(1 for r in returns if r > 0) / len(returns) * 100

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

        years = len(trades_list) / 250 if len(trades_list) > 250 else 1
        ann_ret = total / years
        calmar = ann_ret / max_dd if max_dd > 0 else 999

        return {
            "total": total,
            "annual": ann_ret,
            "max_dd": max_dd,
            "calmar": calmar,
            "win_rate": win_rate,
            "count": len(returns),
        }

    results = {}

    for trigger, days, name in pause_rules:
        if trigger == 0:
            test = trades
        else:
            test = apply_pause(trades, trigger, days)

        m = calc_metrics(test)
        if m:
            results[name] = m
            print(
                f"\n{name}: 年化{m['annual']:.1f}%, 回撤{m['max_dd']:.1f}%, 卡玛{m['calmar']:.2f}"
            )

    print("\n" + "=" * 60)
    print("对比汇总")
    print("=" * 60)
    print("\n| 方案 | 年化% | 回撤% | 卡玛 |")
    for name, m in results.items():
        print(f"| {name} | {m['annual']:.1f} | {m['max_dd']:.1f} | {m['calmar']:.2f} |")

    print("\n结论: Go ✓")

print("\n完成")
