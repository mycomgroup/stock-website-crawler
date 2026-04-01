"""
三档仓位调节测试 - A组 vs B组对比（简化版）
时间范围：2025-01-01 至 2025-12-31（最近1年）
"""

from jqdata import *
import pandas as pd

print("=" * 80)
print("三档仓位调节对比测试 - 简化版")
print("=" * 80)
print("时间：2025全年（共约250个交易日）")

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

trade_days_list = get_trade_days(START_DATE, END_DATE)
print(f"交易日: {len(trade_days_list)}天")

results_a = {
    "trades": [],
    "return": 0,
    "wins": 0,
    "total": 0,
    "days_open": 0,
    "days_close": 0,
}
results_b = {
    "trades": [],
    "return": 0,
    "wins": 0,
    "total": 0,
    "days_full": 0,
    "days_half": 0,
    "days_close": 0,
}


def get_sentiment_a(zt_count, lianban):
    return 1.0 if zt_count >= 30 and lianban >= 3 else 0.0


def get_sentiment_b(zt_count, lianban):
    if zt_count > 50 and lianban > 5:
        return 1.0, "full"
    elif 30 <= zt_count <= 50 and 3 <= lianban <= 5:
        return 0.5, "half"
    return 0.0, "close"


for i, date in enumerate(trade_days_list[:250]):
    if i % 10 == 0:
        print(f"[{i + 1}/250] {date}")

    try:
        prev_date = get_trade_days(end_date=date, count=2)[0]
        all_stocks = [
            s
            for s in get_all_securities("stock", date).index
            if s[0] not in ["4", "8", "6"]
        ]

        df = get_price(
            all_stocks,
            end_date=prev_date,
            frequency="daily",
            fields=["paused", "close", "high_limit"],
            count=1,
            panel=False,
            fill_paused=False,
        )
        df = df.dropna()
        df = df[df.paused == 0]
        zt = df[df.close == df.high_limit].code.tolist()
        zt_cnt = len(zt)

        lianban = 0
        if zt_cnt > 0:
            df_lb = get_price(
                zt[:15],
                end_date=prev_date,
                frequency="daily",
                fields=["close", "high_limit"],
                count=4,
                panel=False,
                fill_paused=False,
            )
            for s in zt[:15]:
                sdf = df_lb[df_lb.code == s].sort_values("time", ascending=False)
                cnt = 0
                for _, r in sdf.iterrows():
                    if abs(r.close - r.high_limit) < 0.01:
                        cnt += 1
                    else:
                        break
                lianban = max(lianban, cnt)

        pos_a = get_sentiment_a(zt_cnt, lianban)
        pos_b, pos_type_b = get_sentiment_b(zt_cnt, lianban)

        if pos_a == 1.0:
            results_a["days_open"] += 1
        else:
            results_a["days_close"] += 1

        if pos_type_b == "full":
            results_b["days_full"] += 1
        elif pos_type_b == "half":
            results_b["days_half"] += 1
        else:
            results_b["days_close"] += 1

        if pos_a == 0.0 and pos_b == 0.0:
            continue

        if zt_cnt == 0:
            continue

        first_board = zt
        prev_prev = (
            get_trade_days(end_date=prev_date, count=2)[0]
            if len(get_trade_days(end_date=prev_date, count=2)) >= 2
            else None
        )
        if prev_prev:
            df_pp = get_price(
                zt[:30],
                end_date=prev_prev,
                frequency="daily",
                fields=["close", "high_limit"],
                count=1,
                panel=False,
                fill_paused=False,
            )
            if len(df_pp) > 0:
                prev_zt = df_pp[df_pp.close == df_pp.high_limit].code.tolist()
                first_board = [s for s in zt if s not in prev_zt]

        if not first_board:
            continue

        df_today = get_price(
            first_board[:15],
            end_date=date,
            frequency="daily",
            fields=["open", "paused"],
            count=1,
            panel=False,
            fill_paused=False,
        )

        targets = []
        for s in first_board[:15]:
            sd = df_today[df_today.code == s]
            if len(sd) == 0:
                continue
            open_p = sd.iloc[0]["open"]
            paused = sd.iloc[0].get("paused", 0)
            if paused == 1:
                continue

            prev_c = get_price(
                s,
                end_date=prev_date,
                frequency="daily",
                fields=["close"],
                count=1,
                panel=False,
            )
            if len(prev_c) == 0:
                continue
            prev_close = prev_c.iloc[0].close

            if prev_close <= 0:
                continue

            pct = (open_p - prev_close) / prev_close
            if -0.05 <= pct <= -0.01:
                targets.append(s)

        if not targets:
            continue

        targets = targets[:3]
        next_date = get_trade_days(start_date=date, count=2)[-1]

        df_next = get_price(
            targets,
            end_date=next_date,
            frequency="daily",
            fields=["open"],
            count=1,
            panel=False,
        )

        for s in targets:
            buy = df_today[df_today.code == s].iloc[0].open
            sell = (
                df_next[df_next.code == s].iloc[0].open
                if len(df_next[df_next.code == s]) > 0
                else None
            )

            if sell is None:
                continue

            ret = (sell - buy) / buy * 100

            results_a["trades"].append(
                {"date": date, "stock": s, "ret": ret * pos_a, "pos": pos_a}
            )
            results_a["return"] += ret * pos_a
            results_a["total"] += 1
            if ret * pos_a > 0:
                results_a["wins"] += 1

            results_b["trades"].append(
                {"date": date, "stock": s, "ret": ret * pos_b, "pos": pos_type_b}
            )
            results_b["return"] += ret * pos_b
            results_b["total"] += 1
            if ret * pos_b > 0:
                results_b["wins"] += 1

    except Exception as e:
        if i % 20 == 0:
            print(f"  Error at {date}: {str(e)[:50]}")
        continue

print(f"\n{'=' * 80}")
print("回测结果对比")
print(f"{'=' * 80}")

print(f"\n【A组：开关式】")
print(f"交易次数: {results_a['total']}")
print(f"胜率: {results_a['wins'] / max(results_a['total'], 1) * 100:.2f}%")
print(f"累计收益: {results_a['return']:.2f}%")
print(
    f"开仓天数: {results_a['days_open']}天 ({results_a['days_open'] / 250 * 100:.1f}%)"
)
print(
    f"空仓天数: {results_a['days_close']}天 ({results_a['days_close'] / 250 * 100:.1f}%)"
)

print(f"\n【B组：三档仓位】")
print(f"交易次数: {results_b['total']}")
print(f"胜率: {results_b['wins'] / max(results_b['total'], 1) * 100:.2f}%")
print(f"累计收益: {results_b['return']:.2f}%")
print(
    f"满仓天数: {results_b['days_full']}天 ({results_b['days_full'] / 250 * 100:.1f}%)"
)
print(
    f"半仓天数: {results_b['days_half']}天 ({results_b['days_half'] / 250 * 100:.1f}%)"
)
print(
    f"空仓天数: {results_b['days_close']}天 ({results_b['days_close'] / 250 * 100:.1f}%)"
)

print(f"\n【对比结论】")
if results_a["total"] > 0 and results_b["total"] > 0:
    print(f"收益差异: B组比A组 {results_b['return'] - results_a['return']:+.2f}%")
    print(
        f"胜率差异: B组比A组 {(results_b['wins'] / results_b['total'] - results_a['wins'] / results_a['total']) * 100:+.2f}%"
    )

    if results_b["return"] > results_a["return"]:
        print(f"结论: 三档仓位优于开关式 ✓")
    else:
        print(f"结论: 三档仓位未优于开关式 ✗")

print(f"\n{'=' * 80}")
