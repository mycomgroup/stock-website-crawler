from jqdata import *
import pandas as pd
import numpy as np
import json
import os

"""
任务01v2：主线容量与滑点实测 - 简化版
只测试关键数据，减少查询次数
"""

OUTPUT_FILE = "/Users/fengzhi/Downloads/git/testlixingren/output/first_board_capacity_slippage.json"

CAPACITIES = [100000, 500000, 2000000]
CAPACITY_NAMES = ["10万", "50万", "200万"]

COMMISSION_RATE = 0.0003
STAMP_DUTY = 0.001

START_DATE = "2024-01-01"
END_DATE = "2024-12-31"

print("=" * 80)
print("任务01v2：主线容量与滑点实测（简化版）")
print("=" * 80)

trade_days = list(get_trade_days(START_DATE, END_DATE))
print(f"测试期间: {START_DATE} ~ {END_DATE}, 共{len(trade_days)}天")

signals_data = []
print("扫描信号...")

for i in range(1, len(trade_days)):
    prev_date = trade_days[i - 1]
    curr_date = trade_days[i]

    if i % 40 == 0:
        print(f"  进度: {i}/{len(trade_days)}")

    try:
        all_stocks = get_all_securities("stock", prev_date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "683"]

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

        if not limit_stocks:
            continue

        price_curr = get_price(
            limit_stocks,
            end_date=curr_date,
            count=1,
            fields=["open", "close", "high", "money"],
            panel=False,
        )

        if price_curr.empty:
            continue

        q = query(valuation.code, valuation.circulating_market_cap).filter(
            valuation.code.in_(limit_stocks)
        )
        val_data = get_fundamentals(q, date=curr_date)

        if val_data.empty:
            continue

        for stock in limit_stocks[:20]:
            try:
                prev_row = price_prev[price_prev["code"] == stock].iloc[0]
                curr_row = price_curr[price_curr["code"] == stock].iloc[0]

                prev_close = float(prev_row["close"])
                curr_open = float(curr_row["open"])
                curr_close = float(curr_row["close"])
                curr_high = float(curr_row["high"])
                curr_money = float(curr_row["money"])

                open_pct = (curr_open - prev_close) / prev_close * 100

                if not (0.5 <= open_pct <= 1.5):
                    continue

                val_row = val_data[val_data["code"] == stock]
                if val_row.empty:
                    continue

                market_cap = float(val_row["circulating_market_cap"].iloc[0])

                if not (50 <= market_cap <= 150):
                    continue

                prices_15d = get_price(
                    stock, end_date=prev_date, count=15, fields=["close"], panel=False
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

                lb_data = get_price(
                    stock,
                    end_date=prev_date,
                    count=2,
                    fields=["close", "high_limit"],
                    panel=False,
                )

                if len(lb_data) >= 2:
                    pp_close = float(lb_data["close"].iloc[0])
                    pp_limit = float(lb_data["high_limit"].iloc[0])
                    if abs(pp_close - pp_limit) / pp_limit < 0.01:
                        continue

                signals_data.append(
                    {
                        "stock": stock,
                        "date": curr_date,
                        "open_price": curr_open,
                        "open_pct": open_pct,
                        "day_close": curr_close,
                        "day_high": curr_high,
                        "day_money": curr_money,
                        "market_cap": market_cap,
                    }
                )
            except:
                continue
    except:
        continue

print(f"\n发现信号: {len(signals_data)}个")

if not signals_data:
    print("无信号，退出")
    os.makedirs("/Users/fengzhi/Downloads/git/testlixingren/output", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump({"signals": 0, "all_results": []}, f)
else:
    print("\n分析成交与滑点...")

    all_results = []

    for cap_idx, (capacity, cap_name) in enumerate(zip(CAPACITIES, CAPACITY_NAMES)):
        print(f"\n测试仓位: {cap_name}")

        slippages = []
        volume_ratios = []
        returns = []
        success = 0
        fail = 0

        for sig in signals_data:
            volume_ratio = capacity / sig["day_money"] * 100

            if volume_ratio > 10:
                fail += 1
                continue

            try:
                min_data = get_price(
                    sig["stock"],
                    end_date=sig["date"],
                    frequency="1m",
                    fields=["open", "close"],
                    count=1,
                    panel=False,
                )

                if min_data.empty:
                    fail += 1
                    continue

                first_open = float(min_data["open"].iloc[0])
                slippage = (first_open - sig["open_price"]) / sig["open_price"] * 100

                slippages.append(slippage)
                volume_ratios.append(volume_ratio)

                buy_price = first_open
                sell_price = sig["day_high"] * 0.998
                shares = int(capacity / buy_price / 100) * 100

                if shares < 100:
                    fail += 1
                    continue

                buy_val = shares * buy_price
                sell_val = shares * sell_price
                cost = (
                    buy_val * COMMISSION_RATE
                    + sell_val * COMMISSION_RATE
                    + sell_val * STAMP_DUTY
                )
                ret = (sell_val - buy_val - cost) / buy_val * 100

                returns.append(ret)
                success += 1
            except:
                fail += 1

        if slippages:
            avg_slip = np.mean(slippages)
            max_slip = np.max(slippages)
            min_slip = np.min(slippages)
            std_slip = np.std(slippages)
            avg_ratio = np.mean(volume_ratios)
            avg_ret = np.mean(returns)
            ann_ret = avg_ret * (len(trade_days) / 250)

            print(f"  成交成功: {success}, 失败: {fail}")
            print(f"  平均滑点: {avg_slip:.4f}%")
            print(f"  最大滑点: {max_slip:.4f}%")
            print(f"  最小滑点: {min_slip:.4f}%")
            print(f"  滑点标准差: {std_slip:.4f}%")
            print(f"  成交额占比: {avg_ratio:.4f}%")
            print(f"  平均收益: {avg_ret:.2f}%")
            print(f"  预估年化: {ann_ret:.2f}%")

            all_results.append(
                {
                    "capacity": cap_name,
                    "success": success,
                    "fail": fail,
                    "avg_slippage": avg_slip,
                    "max_slippage": max_slip,
                    "min_slippage": min_slip,
                    "slippage_std": std_slip,
                    "avg_volume_ratio": avg_ratio,
                    "avg_return": avg_ret,
                    "ann_return": ann_ret,
                }
            )
        else:
            print(f"  无成交数据")
            all_results.append({"capacity": cap_name, "success": 0, "fail": fail})

    print("\n" + "=" * 80)
    print("汇总表")
    print("=" * 80)

    for r in all_results:
        if r.get("avg_slippage"):
            slip = abs(r["avg_slippage"])
            if slip <= 0.2:
                verdict = "✓ 安全"
            elif slip <= 0.5:
                verdict = "△ 临界"
            else:
                verdict = "✗ 不可用"

            print(
                f"{r['capacity']:<8} 成功{r['success']:<5} 滑点{r['avg_slippage']:.4f}% 收益{r['avg_return']:.2f}% {verdict}"
            )

    print("\n" + "=" * 80)
    print("容量上限建议")
    print("=" * 80)

    safe_cap = None
    crit_cap = None

    for r in all_results:
        if r.get("avg_slippage"):
            slip = abs(r["avg_slippage"])
            if slip <= 0.2:
                safe_cap = r["capacity"]
            if slip <= 0.5:
                crit_cap = r["capacity"]

    print(f"安全容量(滑点≤0.2%): {safe_cap or '未找到'}")
    print(f"临界容量(滑点≤0.5%): {crit_cap or '未找到'}")

    print("\n与原估算对比:")
    print("原理论: 500万上限")

    if len(signals_data) > 0:
        avg_money = np.mean([s["day_money"] for s in signals_data])
        print(f"平均成交额: {avg_money / 100000000:.2f}亿")
        print(f"50万占比: {500000 / avg_money * 100:.2f}%")
        print(f"200万占比: {2000000 / avg_money * 100:.2f}%")

    os.makedirs("/Users/fengzhi/Downloads/git/testlixingren/output", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(
            {
                "signals": len(signals_data),
                "signal_list": signals_data,
                "all_results": all_results,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"\n结果已保存: {OUTPUT_FILE}")
    print("=" * 80)
