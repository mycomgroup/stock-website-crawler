from jqdata import *
import pandas as pd
import numpy as np


def initialize(context):
    set_option("use_real_price", True)
    log.set_level("order", "error")

    g.test_start = "2022-01-01"
    g.test_end = "2024-12-31"
    g.sample_out_date = "2024-01-01"

    g.open_range = (-0.01, 0.02)
    g.max_signals = 300

    g.signals = []
    g.results = {"S1": [], "S2": [], "S3": [], "S4": [], "S5": [], "S6": [], "S7": []}

    run_daily(run_backtest, time="09:00")


def run_backtest(context):
    if g.signals:
        return

    log.info("=" * 80)
    log.info("任务05v2：卖出规则深度对比测试（策略编辑器版）")
    log.info("=" * 80)

    log.info("测试区间: %s 至 %s" % (g.test_start, g.test_end))
    log.info(
        "开盘范围: %.1f%% 至 %.1f%%" % (g.open_range[0] * 100, g.open_range[1] * 100)
    )

    all_days = get_trade_days(g.test_start, g.test_end)
    log.info("交易日数: %d" % len(all_days))

    log.info("开始筛选信号...")

    processed = 0
    for i in range(len(all_days) - 1):
        if processed >= g.max_signals:
            log.info("达到最大信号数 %d，停止筛选" % g.max_signals)
            break

        if i % 5 != 0:
            continue

        date = all_days[i]
        date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)

        if i == 0:
            continue

        prev_date = all_days[i - 1]
        prev_date_str = (
            prev_date.strftime("%Y-%m-%d")
            if hasattr(prev_date, "strftime")
            else str(prev_date)
        )

        try:
            stocks = get_all_securities("stock", prev_date_str).index.tolist()
            stocks = [
                s
                for s in stocks
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ]

            if len(stocks) == 0:
                continue

            prices = get_price(
                stocks[:500],
                end_date=prev_date_str,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
                skip_paused=True,
            )

            if prices.empty:
                continue

            zt_stocks = prices[prices["close"] >= prices["high_limit"] * 0.99][
                "code"
            ].tolist()

            if len(zt_stocks) == 0:
                continue

            for stock in zt_stocks[:30]:
                try:
                    prev_close = float(
                        prices.loc[prices["code"] == stock, "close"].iloc[0]
                    )

                    next_price = get_price(
                        stock,
                        end_date=date_str,
                        count=1,
                        fields=["open", "close", "high", "low", "high_limit"],
                        panel=False,
                    )

                    if next_price.empty:
                        continue

                    open_price = float(next_price["open"].iloc[0])
                    open_change = (open_price - prev_close) / prev_close

                    if g.open_range[0] <= open_change <= g.open_range[1]:
                        g.signals.append(
                            {
                                "date": date_str,
                                "stock": stock,
                                "buy_price": open_price,
                                "open_change": open_change,
                            }
                        )
                        processed += 1

                        if processed >= g.max_signals:
                            break

                except Exception as e:
                    continue

        except Exception as e:
            continue

    log.info("筛选出信号数: %d" % len(g.signals))

    if len(g.signals) < 20:
        log.warn("信号数量不足 %d，建议调整参数" % len(g.signals))

    log.info("开始计算卖出规则收益...")

    for idx, sig in enumerate(g.signals):
        if idx % 50 == 0:
            log.info("进度: %d/%d" % (idx, len(g.signals)))

        buy_price = sig["buy_price"]
        stock = sig["stock"]
        date_str = sig["date"]

        try:
            today_price = get_price(
                stock,
                end_date=date_str,
                count=1,
                fields=["close", "high", "high_limit"],
                panel=False,
            )

            if today_price.empty:
                continue

            same_close = float(today_price["close"].iloc[0])
            today_high = float(today_price["high"].iloc[0])
            today_limit = float(today_price["high_limit"].iloc[0])
            is_limit_up = abs(same_close - today_limit) / today_limit < 0.01

            day_idx = -1
            for j, d in enumerate(all_days):
                ds = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
                if ds == date_str:
                    day_idx = j
                    break

            if day_idx > 0 and day_idx < len(all_days) - 1:
                next_date = all_days[day_idx + 1]
                next_date_str = (
                    next_date.strftime("%Y-%m-%d")
                    if hasattr(next_date, "strftime")
                    else str(next_date)
                )

                next_price = get_price(
                    stock,
                    end_date=next_date_str,
                    count=1,
                    fields=["open", "close", "high"],
                    panel=False,
                )

                if not next_price.empty:
                    next_open = float(next_price["open"].iloc[0])
                    next_close = float(next_price["close"].iloc[0])
                    next_high = float(next_price["high"].iloc[0])
                else:
                    next_open = same_close
                    next_close = same_close
                    next_high = same_close
            else:
                next_open = same_close
                next_close = same_close
                next_high = same_close

            is_so = date_str >= g.sample_out_date

            g.results["S1"].append(
                {
                    "ret": (same_close - buy_price) / buy_price,
                    "so": is_so,
                    "open_change": sig["open_change"],
                }
            )

            g.results["S2"].append(
                {
                    "ret": (next_open - buy_price) / buy_price,
                    "so": is_so,
                    "open_change": sig["open_change"],
                }
            )

            g.results["S3"].append(
                {
                    "ret": (next_close - buy_price) / buy_price,
                    "so": is_so,
                    "open_change": sig["open_change"],
                }
            )

            if next_high >= buy_price * 1.03:
                s4_ret = 0.03
            else:
                s4_ret = (next_close - buy_price) / buy_price
            g.results["S4"].append(
                {"ret": s4_ret, "so": is_so, "open_change": sig["open_change"]}
            )

            if next_high >= buy_price * 1.05:
                s5_ret = 0.05
            else:
                s5_ret = (next_close - buy_price) / buy_price
            g.results["S5"].append(
                {"ret": s5_ret, "so": is_so, "open_change": sig["open_change"]}
            )

            if is_limit_up:
                s6_ret = (same_close - buy_price) / buy_price
            else:
                if next_high >= buy_price * 1.03:
                    s6_ret = 0.03
                else:
                    s6_ret = (next_close - buy_price) / buy_price
            g.results["S6"].append(
                {"ret": s6_ret, "so": is_so, "open_change": sig["open_change"]}
            )

            g.results["S7"].append(
                {
                    "ret": (next_high - buy_price) / buy_price,
                    "so": is_so,
                    "open_change": sig["open_change"],
                }
            )

        except Exception as e:
            continue

    log.info("计算完成，有效信号数: %d" % len(g.results["S1"]))

    output_results()


def output_results():
    log.info("=" * 80)
    log.info("统计结果")
    log.info("=" * 80)

    rule_names = {
        "S1": "当日收盘",
        "S2": "次日开盘",
        "S3": "次日收盘",
        "S4": "冲高+3%",
        "S5": "冲高+5%",
        "S6": "涨停持有",
        "S7": "次日最高(理论)",
    }

    log.info("【全样本结果】")
    log.info(
        "%-15s %8s %8s %8s %8s %8s %6s"
        % ("规则", "平均收益", "胜率", "盈亏比", "年化", "卡玛", "交易数")
    )
    log.info("-" * 80)

    summary = {}

    for rid in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
        if len(g.results[rid]) == 0:
            continue

        df = pd.DataFrame(g.results[rid])

        avg = df["ret"].mean() * 100
        win = (df["ret"] > 0).sum() / len(df)

        wins = df[df["ret"] > 0]["ret"]
        losses = df[df["ret"] <= 0]["ret"]
        avg_win = wins.mean() * 100 if len(wins) > 0 else 0
        avg_loss = losses.mean() * 100 if len(losses) > 0 else 0
        plr = abs(avg_win / avg_loss) if avg_loss != 0 else 0

        cum = (1 + df["ret"]).cumprod()
        dd = abs((cum - cum.cummax()) / cum.cummax()).min() * 100
        ann = (1 + avg / 100) ** 250 - 1
        calmar = abs(ann * 100 / dd) if dd > 0 else 0

        so_df = df[df["so"]]
        so_avg = so_df["ret"].mean() * 100 if len(so_df) > 0 else 0
        so_win = (so_df["ret"] > 0).sum() / len(so_df) if len(so_df) > 0 else 0

        summary[rid] = {
            "name": rule_names[rid],
            "avg": avg,
            "win": win,
            "plr": plr,
            "ann": ann * 100,
            "calmar": calmar,
            "count": len(df),
            "so_avg": so_avg,
            "so_win": so_win,
            "so_count": len(so_df),
        }

        log.info(
            "%-15s %7.2f%% %7.2f%% %7.2f %7.2f%% %7.2f %5d"
            % (rule_names[rid], avg, win * 100, plr, ann * 100, calmar, len(df))
        )

    log.info("")
    log.info("【2024+样本外】")
    log.info("%-15s %6s %8s %10s" % ("规则", "交易数", "胜率", "平均收益"))
    log.info("-" * 60)

    for rid in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
        s = summary.get(rid, {})
        if s.get("so_count", 0) > 0:
            log.info(
                "%-15s %5d %7.2f%% %9.2f%%"
                % (s["name"], s["so_count"], s["so_win"] * 100, s["so_avg"])
            )

    log.info("")
    log.info("【开盘涨幅分组】")
    log.info(
        "%-12s %6s %8s %8s %8s" % ("开盘类型", "交易数", "S4收益", "S7收益", "S4胜率")
    )
    log.info("-" * 60)

    open_groups = {
        "深度低开": (-0.01, 0.0),
        "平开": (0.0, 0.005),
        "假弱高开": (0.005, 0.015),
        "真高开": (0.015, 0.02),
    }

    for group_name, (low, high) in open_groups.items():
        s4_results = [r for r in g.results["S4"] if low <= r["open_change"] < high]
        s7_results = [r for r in g.results["S7"] if low <= r["open_change"] < high]

        if len(s4_results) > 0:
            s4_avg = np.mean([r["ret"] for r in s4_results]) * 100
            s4_win = sum(1 for r in s4_results if r["ret"] > 0) / len(s4_results) * 100
        else:
            s4_avg = 0
            s4_win = 0

        if len(s7_results) > 0:
            s7_avg = np.mean([r["ret"] for r in s7_results]) * 100
        else:
            s7_avg = 0

        count = len([s for s in g.signals if low <= s["open_change"] < high])

        log.info(
            "%-12s %5d %7.2f%% %7.2f%% %7.2f%%"
            % (group_name, count, s4_avg, s7_avg, s4_win)
        )

    log.info("")
    log.info("【推荐规则】")
    exec_rules = [(k, v) for k, v in summary.items() if k != "S7"]
    sorted_rules = sorted(exec_rules, key=lambda x: x[1]["calmar"], reverse=True)

    if len(sorted_rules) > 0:
        rec_id, rec = sorted_rules[0]
        log.info("主推荐: %s" % rec["name"])
        log.info("  卡玛: %.2f" % rec["calmar"])
        log.info("  胜率: %.1f%%" % (rec["win"] * 100))
        log.info("  年化: %.2f%%" % rec["ann"])
        log.info("  交易数: %d" % rec["count"])

    status = (
        "Go ✓"
        if len(sorted_rules) > 0 and sorted_rules[0][1]["calmar"] > 1.5
        else "Watch ⚠️"
    )
    log.info("")
    log.info("判定: %s" % status)
    log.info("=" * 80)


def handle_data(context, data):
    pass
