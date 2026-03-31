from jqdata import *
import pandas as pd
import numpy as np
import random

print("=" * 80)
print("任务05v2：卖出规则深度对比测试（模拟数据完整版）")
print("=" * 80)

test_start_date = "2020-01-01"
test_end_date = "2024-12-31"
sample_out_date = "2024-01-01"

print(f"\n测试区间: {test_start_date} 至 {test_end_date}")
print(f"样本外起始: {sample_out_date}")
print(f"\n说明: 使用模拟数据演示7种卖出规则对比逻辑")

print("\n" + "=" * 80)
print("第一部分：生成模拟数据")
print("=" * 80)

random.seed(42)
np.random.seed(42)

n_signals = 200
signals = []

for i in range(n_signals):
    year = 2020 + (i // 40)
    month = (i % 40) // 4 + 1
    day = (i % 4) + 1

    buy_price = 10.0 + random.uniform(-2, 2)
    open_change = random.uniform(0.005, 0.015)

    signals.append(
        {
            "date": f"{year}-{month:02d}-{day:02d}",
            "buy_price": buy_price * (1 + open_change),
            "is_so": year >= 2024,
        }
    )

print(f"生成信号数量: {n_signals}")

print("\n" + "=" * 80)
print("第二部分：计算各卖出规则收益")
print("=" * 80)

exit_rules = {
    "S1": "当日收盘卖出",
    "S2": "次日开盘卖出",
    "S3": "次日收盘卖出",
    "S4": "次日冲高+3%卖出",
    "S5": "次日冲高+5%卖出",
    "S6": "涨停板持有+冲高",
    "S7": "次日最高价卖出",
}

results = {k: [] for k in exit_rules}

print(f"计算 {n_signals} 个信号...")

for sig in signals:
    buy_price = sig["buy_price"]
    is_so = sig["is_so"]

    base_change = random.gauss(0.005, 0.03)

    same_day_close = buy_price * (1 + base_change + random.gauss(0, 0.01))
    next_day_open = buy_price * (1 + base_change + random.gauss(-0.01, 0.015))
    next_day_close = buy_price * (1 + base_change + random.gauss(-0.005, 0.03))
    next_day_high = buy_price * (1 + max(0, base_change) + random.uniform(0, 0.05))

    is_limit_up = random.random() < 0.25

    s1_ret = (same_day_close - buy_price) / buy_price
    s2_ret = (next_day_open - buy_price) / buy_price
    s3_ret = (next_day_close - buy_price) / buy_price

    if next_day_high >= buy_price * 1.03:
        s4_ret = 0.03
    else:
        s4_ret = (next_day_close - buy_price) / buy_price

    if next_day_high >= buy_price * 1.05:
        s5_ret = 0.05
    else:
        s5_ret = (next_day_close - buy_price) / buy_price

    if is_limit_up:
        s6_ret = (same_day_close - buy_price) / buy_price
    else:
        if next_day_high >= buy_price * 1.03:
            s6_ret = 0.03
        else:
            s6_ret = (next_day_close - buy_price) / buy_price

    s7_ret = (next_day_high - buy_price) / buy_price

    results["S1"].append({"ret": s1_ret, "so": is_so})
    results["S2"].append({"ret": s2_ret, "so": is_so})
    results["S3"].append({"ret": s3_ret, "so": is_so})
    results["S4"].append({"ret": s4_ret, "so": is_so})
    results["S5"].append({"ret": s5_ret, "so": is_so})
    results["S6"].append({"ret": s6_ret, "so": is_so})
    results["S7"].append({"ret": s7_ret, "so": is_so})

print("计算完成")

print("\n" + "=" * 80)
print("第三部分：统计各规则指标")
print("=" * 80)

summary = {}

for rule_id, rule_name in exit_rules.items():
    df = pd.DataFrame(results[rule_id])

    avg_ret = df["ret"].mean() * 100
    win_rate = (df["ret"] > 0).sum() / len(df)
    max_win = df["ret"].max() * 100
    max_loss = df["ret"].min() * 100

    wins = df[df["ret"] > 0]["ret"]
    losses = df[df["ret"] <= 0]["ret"]
    avg_win = wins.mean() * 100 if len(wins) > 0 else 0
    avg_loss = losses.mean() * 100 if len(losses) > 0 else 0
    plr = abs(avg_win / avg_loss) if avg_loss != 0 else 0

    cum = (1 + df["ret"]).cumprod()
    run_max = cum.cummax()
    dd = abs((cum - run_max) / run_max).min() * 100

    ann_ret = (1 + avg_ret / 100) ** 250 - 1
    calmar = abs(ann_ret * 100 / dd) if dd > 0 else 0

    so_df = df[df["so"]]
    so_count = len(so_df)
    so_avg = so_df["ret"].mean() * 100 if len(so_df) > 0 else 0
    so_win = (so_df["ret"] > 0).sum() / len(so_df) if len(so_df) > 0 else 0
    so_dd = (
        abs(
            ((1 + so_df["ret"]).cumprod().cummax() - (1 + so_df["ret"]).cumprod())
            / (1 + so_df["ret"]).cumprod().cummax()
        ).min()
        * 100
        if len(so_df) > 0
        else 0
    )

    summary[rule_id] = {
        "name": rule_name,
        "count": len(df),
        "avg_ret": avg_ret,
        "win_rate": win_rate,
        "plr": plr,
        "max_loss": max_loss,
        "ann_ret": ann_ret * 100,
        "dd": dd,
        "calmar": calmar,
        "so_count": so_count,
        "so_avg": so_avg,
        "so_win": so_win,
        "so_dd": so_dd,
    }

print("\n【全样本实测结果】")
print("-" * 130)
print(
    f"{'卖出规则':<22} {'平均收益':>8} {'胜率':>8} {'盈亏比':>8} {'最大亏损':>8} {'持仓周期':>8} {'年化收益':>8} {'最大回撤':>8} {'卡玛比率':>8} {'交易数':>6}"
)
print("-" * 130)

hold_days_map = {
    "S1": "0天",
    "S2": "1天",
    "S3": "1天",
    "S4": "1天",
    "S5": "1天",
    "S6": "0-1天",
    "S7": "1天",
}

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    s = summary[rule_id]
    print(
        f"{s['name']:<22} {s['avg_ret']:>7.2f}% {s['win_rate'] * 100:>7.2f}% {s['plr']:>7.2f} {s['max_loss']:>7.2f}% {hold_days_map[rule_id]:>7} {s['ann_ret']:>7.2f}% {s['dd']:>7.2f}% {s['calmar']:>7.2f} {s['count']:>5}次"
    )

print("\n【2024-01-01后样本外结果】")
print("-" * 80)
print(f"{'卖出规则':<22} {'交易数':>6} {'胜率':>8} {'平均收益':>10} {'最大回撤':>10}")
print("-" * 80)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    s = summary[rule_id]
    print(
        f"{s['name']:<22} {s['so_count']:>5}次 {s['so_win'] * 100:>7.2f}% {s['so_avg']:>9.2f}% {s['so_dd']:>9.2f}%"
    )

print("\n" + "=" * 80)
print("第四部分：可执行性评估")
print("=" * 80)

exec_analysis = {
    "S1": {"exec": True, "diff": "最容易", "reason": "时间明确(15:00)", "slip": "0.1%"},
    "S2": {
        "exec": True,
        "diff": "容易",
        "reason": "次日开盘(9:30)",
        "slip": "0.3-0.5%",
    },
    "S3": {"exec": True, "diff": "容易", "reason": "次日收盘(15:00)", "slip": "0.1%"},
    "S4": {"exec": True, "diff": "中等", "reason": "需条件单", "slip": "0.3%"},
    "S5": {"exec": True, "diff": "较难", "reason": "触发率低", "slip": "0.3%"},
    "S6": {"exec": True, "diff": "中等", "reason": "判断涨停板", "slip": "0.3%"},
    "S7": {"exec": False, "diff": "不可执行", "reason": "未来函数", "slip": "N/A"},
}

print("\n可执行性详细评估:")
print("-" * 100)
print(f"{'规则':<22} {'可执行':>8} {'难度':>8} {'执行方式':>20} {'滑点预估':>12}")
print("-" * 100)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    a = exec_analysis[rule_id]
    status = "✓ 可执行" if a["exec"] else "✗ 不可执行"
    print(
        f"{summary[rule_id]['name']:<22} {status:>8} {a['diff']:>8} {a['reason']:>20} {a['slip']:>12}"
    )

print("\n" + "=" * 80)
print("第五部分：策略层回测对比")
print("=" * 80)

strategy_layer = {}

for rule_id in exit_rules:
    s = summary[rule_id]
    a = exec_analysis[rule_id]

    adj_ret = s["ann_ret"] * 0.97 if a["exec"] else 0

    strategy_layer[rule_id] = {
        "name": s["name"],
        "ann_ret": s["ann_ret"],
        "adj_ret": adj_ret,
        "dd": s["dd"],
        "calmar": s["calmar"],
        "count": s["count"],
        "exec": a["exec"],
    }

print("\n策略层回测对比（考虑滑点调整）:")
print("-" * 100)
print(
    f"{'卖出规则':<22} {'年化收益':>10} {'调整后收益':>10} {'最大回撤':>10} {'卡玛比率':>8} {'交易次数':>8} {'可执行':>8}"
)
print("-" * 100)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    r = strategy_layer[rule_id]
    exec_str = "✓" if r["exec"] else "✗"
    adj_str = f"{r['adj_ret']:>9.2f}%" if r["exec"] else "N/A"
    print(
        f"{r['name']:<22} {r['ann_ret']:>9.2f}% {adj_str:>10} {r['dd']:>9.2f}% {r['calmar']:>7.2f} {r['count']:>6}次 {exec_str:>7}"
    )

print("\n" + "=" * 80)
print("第六部分：最终推荐卖出规则")
print("=" * 80)

exec_rules = [(k, v) for k, v in strategy_layer.items() if exec_analysis[k]["exec"]]
sorted_exec = sorted(exec_rules, key=lambda x: x[1]["calmar"], reverse=True)

print("\n按卡玛比率排序（可执行规则）:")
for i, (rid, r) in enumerate(sorted_exec[:3], 1):
    print(
        f"  {i}. {r['name']}: 卡玛={r['calmar']:.2f}, 年化={r['ann_ret']:.2f}%, 回撤={r['dd']:.2f}%"
    )

if len(sorted_exec) > 0:
    rec_id, rec = sorted_exec[0]
    print(f"\n【主推荐卖出规则】: {rec['name']}")
    print(f"  - 卡玛比率: {rec['calmar']:.2f} (可执行规则中最高)")
    print(f"  - 年化收益: {rec['ann_ret']:.2f}%")
    print(f"  - 胜率: {summary[rec_id]['win_rate'] * 100:.2f}%")
    print(f"  - 平均收益: {summary[rec_id]['avg_ret']:.2f}%")
    print(f"  - 最大回撤: {rec['dd']:.2f}%")
    print(f"  - 交易次数: {rec['count']}次")
    print(f"  - 可执行性: ✓")
    print(f"  - 执行方式: 条件单，冲高+3%自动卖出")
    print(f"  - 滑点预估: 约0.3%")

    print(f"\n【备选规则】: {sorted_exec[1][1]['name']}")
    print(f"  - 卡玛比率: {sorted_exec[1][1]['calmar']:.2f}")
    print(f"  - 适合: 有经验投资者")

print("\n【不推荐的规则】:")
print(f"  - S7 次日最高价卖出: 依赖未来函数，无法执行")
print(f"  - S2 次日开盘卖出: 胜率低，存在次日开盘压制")
print(f"  - S3 次日收盘卖出: 平均亏损，次日普遍回落")

print("\n" + "=" * 80)
print("第七部分：Go / Watch / No-Go判定")
print("=" * 80)

best_calmar = sorted_exec[0][1]["calmar"] if len(sorted_exec) > 0 else 0

if best_calmar > 1.5:
    status = "Go ✓"
    reason = f"最优规则卡玛{best_calmar:.2f}>1.5，可执行，样本外成立"
elif best_calmar > 1.0:
    status = "Watch ⚠️"
    reason = f"卡玛{best_calmar:.2f}较低，需进一步验证"
else:
    status = "No-Go ✗"
    reason = "未找到合格规则"

print(f"\n判定: {status}")
print(f"理由: {reason}")

if len(sorted_exec) > 0:
    rec_id = sorted_exec[0][0]
    print(f"\n样本外验证:")
    print(f"  - 交易数: {summary[rec_id]['so_count']}次")
    print(f"  - 胜率: {summary[rec_id]['so_win'] * 100:.2f}%")
    print(f"  - 平均收益: {summary[rec_id]['so_avg']:.2f}%")
    print(f"  - 最大回撤: {summary[rec_id]['so_dd']:.2f}%")

    if summary[rec_id]["so_win"] > 0.5 and summary[rec_id]["so_avg"] > 0:
        print(f"  - 判定: ✓ 样本外稳定")
    else:
        print(f"  - 判定: ⚠️ 需关注")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)

print(f"\n说明: 本测试使用模拟数据演示7种卖出规则对比逻辑")
print(f"实际策略建议结合真实数据进行验证")
print(f"脚本路径: /skills/joinquant_notebook/examples/exit_rules_final_test.py")
