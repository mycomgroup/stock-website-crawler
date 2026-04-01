"""
三档仓位测试 - 极简版（最近1个月验证）
"""

from jqdata import *
import pandas as pd

print("=" * 60)
print("三档仓位对比测试 - 极简版")
print("=" * 60)

START = "2026-03-01"
END = "2026-03-31"

days = get_trade_days(START, END)
print(f"测试天数: {len(days)}")

result_a = {"ret": 0, "wins": 0, "total": 0, "open_days": 0}
result_b = {"ret": 0, "wins": 0, "total": 0, "full_days": 0, "half_days": 0}

for date in days[:20]:
    print(f"\n{date}")

    prev = get_trade_days(end_date=date, count=2)[0]
    stocks = [
        s
        for s in get_all_securities("stock", date).index
        if s[0] not in ["4", "8", "6"]
    ]

    df = get_price(
        stocks,
        end_date=prev,
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
    print(f"涨停数: {zt_cnt}")

    lianban = 0
    if zt_cnt > 0:
        df_lb = get_price(
            zt[:5],
            end_date=prev,
            frequency="daily",
            fields=["close", "high_limit"],
            count=3,
            panel=False,
        )
        for s in zt[:5]:
            cnt = 0
            for i in range(len(df_lb[df_lb.code == s]) - 1, -1, -1):
                r = df_lb[df_lb.code == s].iloc[i]
                if abs(r.close - r.high_limit) < 0.01:
                    cnt += 1
                else:
                    break
            lianban = max(lianban, cnt)
    print(f"连板数: {lianban}")

    pos_a = 1.0 if zt_cnt >= 30 and lianban >= 3 else 0.0
    pos_b = (
        1.0
        if (zt_cnt > 50 and lianban > 5)
        else (0.5 if (30 <= zt_cnt <= 50 and 3 <= lianban <= 5) else 0.0)
    )

    print(f"A组仓位: {pos_a}")
    print(f"B组仓位: {pos_b}")

    if pos_a > 0:
        result_a["open_days"] += 1
    if pos_b == 1.0:
        result_b["full_days"] += 1
    elif pos_b == 0.5:
        result_b["half_days"] += 1

    if pos_a == 0 and pos_b == 0:
        continue

    if zt_cnt == 0:
        continue

    df_today = get_price(
        zt[:10],
        end_date=date,
        frequency="daily",
        fields=["open", "paused"],
        count=1,
        panel=False,
    )

    targets = []
    for s in zt[:10]:
        if len(df_today[df_today.code == s]) == 0:
            continue
        o = df_today[df_today.code == s].iloc[0].open
        p = df_today[df_today.code == s].iloc[0].paused
        if p == 1:
            continue

        prev_c = (
            get_price(
                s,
                end_date=prev,
                frequency="daily",
                fields=["close"],
                count=1,
                panel=False,
            )
            .iloc[0]
            .close
        )

        pct = (o - prev_c) / prev_c
        if -0.05 <= pct <= -0.01:
            targets.append(s)

    print(f"目标股票: {len(targets)}")

    if not targets:
        continue

    next_d = get_trade_days(start_date=date, count=2)[-1]
    df_next = get_price(
        targets,
        end_date=next_d,
        frequency="daily",
        fields=["open"],
        count=1,
        panel=False,
    )

    for s in targets[:2]:
        buy = df_today[df_today.code == s].iloc[0].open
        sell = df_next[df_next.code == s].iloc[0].open
        ret = (sell - buy) / buy * 100

        print(f"  {s}: 买入{buy:.2f} 卖出{sell:.2f} 收益{ret:.2f}%")

        result_a["ret"] += ret * pos_a
        result_a["total"] += 1
        if ret * pos_a > 0:
            result_a["wins"] += 1

        result_b["ret"] += ret * pos_b
        result_b["total"] += 1
        if ret * pos_b > 0:
            result_b["wins"] += 1

print(f"\n{'=' * 60}")
print("结果对比")
print(f"{'=' * 60}")
print(f"\nA组(开关式):")
print(f"  交易: {result_a['total']}次")
print(f"  胜率: {result_a['wins'] / max(result_a['total'], 1) * 100:.1f}%")
print(f"  收益: {result_a['ret']:.2f}%")
print(f"  开仓天数: {result_a['open_days']}")

print(f"\nB组(三档):")
print(f"  交易: {result_b['total']}次")
print(f"  胜率: {result_b['wins'] / max(result_b['total'], 1) * 100:.1f}%")
print(f"  收益: {result_b['ret']:.2f}%")
print(f"  满仓天数: {result_b['full_days']}")
print(f"  半仓天数: {result_b['half_days']}")

print(f"\n收益差异: {result_b['ret'] - result_a['ret']:+.2f}%")
print(f"{'=' * 60}")
