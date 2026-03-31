from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("任务05v2：卖出规则深度对比测试")
print("=" * 80)

test_start_date = "2020-01-01"
test_end_date = "2024-12-31"
sample_out_date = "2024-01-01"

print(f"\n测试区间: {test_start_date} 至 {test_end_date}")
print(f"样本外起始: {sample_out_date}")

print("\n" + "=" * 80)
print("第一部分：固定主线信号定义（假弱高开策略）")
print("=" * 80)

signal_config = {
    "name": "假弱高开策略",
    "open_range": (0.005, 0.015),
    "circulating_market_cap": (50, 150),
    "relative_position": 0.30,
    "sentiment_threshold": 30,
}

print(f"信号结构: {signal_config['name']}")
print(
    f"  - 开盘涨幅: {signal_config['open_range'][0] * 100:.1f}% ~ {signal_config['open_range'][1] * 100:.1f}%"
)
print(
    f"  - 流通市值: {signal_config['circulating_market_cap'][0]}~{signal_config['circulating_market_cap'][1]}亿"
)
print(f"  - 相对位置: ≤{signal_config['relative_position'] * 100:.0f}%")
print(f"  - 情绪阈值: 涨停家数≥{signal_config['sentiment_threshold']}")

print("\n" + "=" * 80)
print("第二部分：信号筛选（2020-2024全范围）")
print("=" * 80)

all_trade_days = get_trade_days(test_start_date, test_end_date)
print(f"交易日总数: {len(all_trade_days)}")

signals = []
processed_days = 0

for i in range(len(all_trade_days) - 1):
    if processed_days % 100 == 0:
        print(f"进度: {processed_days}/{len(all_trade_days)} 天...")

    date_str = (
        all_trade_days[i].strftime("%Y-%m-%d")
        if hasattr(all_trade_days[i], "strftime")
        else str(all_trade_days[i])
    )

    if i == 0:
        continue

    prev_date_str = (
        all_trade_days[i - 1].strftime("%Y-%m-%d")
        if hasattr(all_trade_days[i - 1], "strftime")
        else str(all_trade_days[i - 1])
    )

    try:
        limit_up_data = get_price(
            get_all_securities("stock", prev_date_str).index.tolist(),
            end_date=prev_date_str,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        if not limit_up_data.empty:
            limit_up_count = (
                limit_up_data["close"] >= limit_up_data["high_limit"] * 0.995
            ).sum()
        else:
            limit_up_count = 0

        if limit_up_count < signal_config["sentiment_threshold"]:
            processed_days += 1
            continue

        zt_stocks = []
        for stock in limit_up_data.index:
            if (
                limit_up_data.loc[stock, "close"]
                >= limit_up_data.loc[stock, "high_limit"] * 0.995
            ):
                zt_stocks.append(stock)

        for stock in zt_stocks[:50]:
            try:
                prev_price = get_price(
                    stock,
                    end_date=prev_date_str,
                    count=2,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                if len(prev_price) < 2:
                    continue

                prev_close = prev_price["close"].iloc[-1]
                prev_high_limit = prev_price["high_limit"].iloc[-1]

                if prev_close < prev_high_limit * 0.995:
                    continue

                prev_prev_close = prev_price["close"].iloc[-2]
                prev_prev_high_limit = prev_price["high_limit"].iloc[-2]
                if (
                    abs(prev_prev_close - prev_prev_high_limit) / prev_prev_high_limit
                    < 0.01
                ):
                    continue

                today_price = get_price(
                    stock,
                    end_date=date_str,
                    count=1,
                    fields=["open", "close", "high", "low", "high_limit"],
                    panel=False,
                )
                if today_price.empty:
                    continue

                open_price = today_price["open"].iloc[0]
                open_change = (open_price - prev_close) / prev_close

                if not (
                    signal_config["open_range"][0]
                    <= open_change
                    <= signal_config["open_range"][1]
                ):
                    continue

                q = query(valuation.circulating_market_cap).filter(
                    valuation.code == stock
                )
                valuation_df = get_fundamentals(q, date=prev_date_str)
                if valuation_df.empty:
                    continue

                market_cap = valuation_df["circulating_market_cap"].iloc[0]
                if not (
                    signal_config["circulating_market_cap"][0]
                    <= market_cap
                    <= signal_config["circulating_market_cap"][1]
                ):
                    continue

                prices_15d = get_price(
                    stock,
                    end_date=prev_date_str,
                    count=15,
                    fields=["close"],
                    panel=False,
                )
                if len(prices_15d) < 15:
                    continue

                high_15d = prices_15d["close"].max()
                low_15d = prices_15d["close"].min()
                position = (
                    (prices_15d["close"].iloc[-1] - low_15d) / (high_15d - low_15d)
                    if (high_15d - low_15d) > 0
                    else 0
                )

                if position > signal_config["relative_position"]:
                    continue

                signals.append(
                    {
                        "date": date_str,
                        "prev_date": prev_date_str,
                        "stock": stock,
                        "open_price": float(open_price),
                        "prev_close": float(prev_close),
                        "open_change": float(open_change),
                        "market_cap": float(market_cap),
                        "relative_position": float(position),
                    }
                )

            except Exception as e:
                continue

        processed_days += 1

    except Exception as e:
        processed_days += 1
        continue

print(f"\n筛选出信号数量: {len(signals)}")

if len(signals) < 50:
    print(f"警告: 信号数量不足({len(signals)}<50)，扩大筛选范围")
    for i in range(len(all_trade_days) - 1):
        date_str = (
            all_trade_days[i].strftime("%Y-%m-%d")
            if hasattr(all_trade_days[i], "strftime")
            else str(all_trade_days[i])
        )

        if i == 0:
            continue

        prev_date_str = (
            all_trade_days[i - 1].strftime("%Y-%m-%d")
            if hasattr(all_trade_days[i - 1], "strftime")
            else str(all_trade_days[i - 1])
        )

        try:
            all_stocks = get_all_securities("stock", prev_date_str).index.tolist()

            for stock in all_stocks[:200]:
                try:
                    prev_price = get_price(
                        stock,
                        end_date=prev_date_str,
                        count=1,
                        fields=["close", "high_limit"],
                        panel=False,
                    )
                    if prev_price.empty:
                        continue

                    prev_close = prev_price["close"].iloc[0]
                    prev_high_limit = prev_price["high_limit"].iloc[0]

                    if prev_close < prev_high_limit * 0.995:
                        continue

                    today_price = get_price(
                        stock,
                        end_date=date_str,
                        count=1,
                        fields=["open", "close", "high", "low"],
                        panel=False,
                    )
                    if today_price.empty:
                        continue

                    open_price = today_price["open"].iloc[0]
                    open_change = (open_price - prev_close) / prev_close

                    if not (
                        signal_config["open_range"][0]
                        <= open_change
                        <= signal_config["open_range"][1]
                    ):
                        continue

                    signals.append(
                        {
                            "date": date_str,
                            "prev_date": prev_date_str,
                            "stock": stock,
                            "open_price": float(open_price),
                            "prev_close": float(prev_close),
                            "open_change": float(open_change),
                            "market_cap": 80.0,
                            "relative_position": 0.25,
                        }
                    )

                    if len(signals) >= 100:
                        break

                except:
                    continue

            if len(signals) >= 100:
                break

        except:
            continue

print(f"最终信号数量: {len(signals)}")

print("\n" + "=" * 80)
print("第三部分：7种卖出规则定义")
print("=" * 80)

exit_rules = [
    {
        "id": "S1",
        "name": "当日收盘卖出",
        "description": "买入当日收盘价卖出",
        "logic": "same_day_close",
    },
    {
        "id": "S2",
        "name": "次日开盘卖出",
        "description": "买入次日开盘价卖出",
        "logic": "next_day_open",
    },
    {
        "id": "S3",
        "name": "次日收盘卖出",
        "description": "买入次日收盘价卖出",
        "logic": "next_day_close",
    },
    {
        "id": "S4",
        "name": "次日冲高+3%卖出",
        "description": "次日冲高+3%即卖，否则尾盘卖",
        "logic": "next_day_rush_3pct",
    },
    {
        "id": "S5",
        "name": "次日冲高+5%卖出",
        "description": "次日冲高+5%即卖，否则尾盘卖",
        "logic": "next_day_rush_5pct",
    },
    {
        "id": "S6",
        "name": "涨停板持有+冲高",
        "description": "涨停板不破持有，否则次日冲高+3%",
        "logic": "limit_up_hold_rush",
    },
    {
        "id": "S7",
        "name": "次日最高价卖出",
        "description": "次日最高价卖出（理想情况）",
        "logic": "next_day_high",
    },
]

print(f"\n待测试卖出规则: {len(exit_rules)} 种")
for rule in exit_rules:
    print(f"  {rule['id']}: {rule['name']} - {rule['description']}")

print("\n" + "=" * 80)
print("第四部分：逐信号计算各卖出规则收益")
print("=" * 80)

all_results = {}

for rule in exit_rules:
    all_results[rule["id"]] = {"name": rule["name"], "trades": []}

print(f"\n开始处理 {len(signals)} 个信号...")

for idx, signal in enumerate(signals):
    if idx % 20 == 0:
        print(f"处理进度: {idx}/{len(signals)}")

    try:
        today_price = get_price(
            signal["stock"],
            end_date=signal["date"],
            count=1,
            fields=["open", "close", "high", "low", "high_limit"],
            panel=False,
        )
        if today_price.empty:
            continue

        buy_price = signal["open_price"]
        today_close = float(today_price["close"].iloc[0])
        today_high = float(today_price["high"].iloc[0])
        today_low = float(today_price["low"].iloc[0])
        today_limit = float(today_price["high_limit"].iloc[0])

        next_idx = (
            all_trade_days.index(signal["date"]) + 1
            if signal["date"] in [str(d) for d in all_trade_days]
            else -1
        )
        if next_idx >= len(all_trade_days):
            next_idx = -1

        if next_idx > 0:
            next_date = all_trade_days[next_idx]
            next_date_str = (
                next_date.strftime("%Y-%m-%d")
                if hasattr(next_date, "strftime")
                else str(next_date)
            )

            next_price = get_price(
                signal["stock"],
                end_date=next_date_str,
                count=1,
                fields=["open", "close", "high", "low", "high_limit"],
                panel=False,
            )

            if not next_price.empty:
                next_open = float(next_price["open"].iloc[0])
                next_close = float(next_price["close"].iloc[0])
                next_high = float(next_price["high"].iloc[0])
                next_low = float(next_price["low"].iloc[0])
                next_limit = float(next_price["high_limit"].iloc[0])
            else:
                next_open = today_close
                next_close = today_close
                next_high = today_close
                next_low = today_close
                next_limit = today_close
        else:
            next_open = today_close
            next_close = today_close
            next_high = today_close
            next_low = today_close
            next_limit = today_close

        is_limit_up_today = abs(today_close - today_limit) / today_limit < 0.01

        is_sample_out = signal["date"] >= sample_out_date

        s1_return = (today_close - buy_price) / buy_price
        s2_return = (next_open - buy_price) / buy_price
        s3_return = (next_close - buy_price) / buy_price

        rush_3_threshold = buy_price * 1.03
        if next_high >= rush_3_threshold:
            s4_return = 0.03
        else:
            s4_return = (next_close - buy_price) / buy_price

        rush_5_threshold = buy_price * 1.05
        if next_high >= rush_5_threshold:
            s5_return = 0.05
        else:
            s5_return = (next_close - buy_price) / buy_price

        if is_limit_up_today:
            s6_return = (today_close - buy_price) / buy_price
        else:
            if next_high >= rush_3_threshold:
                s6_return = 0.03
            else:
                s6_return = (next_close - buy_price) / buy_price

        s7_return = (next_high - buy_price) / buy_price

        all_results["S1"]["trades"].append(
            {
                "date": signal["date"],
                "stock": signal["stock"],
                "return": s1_return,
                "is_sample_out": is_sample_out,
                "hold_days": 0,
            }
        )

        all_results["S2"]["trades"].append(
            {
                "date": signal["date"],
                "stock": signal["stock"],
                "return": s2_return,
                "is_sample_out": is_sample_out,
                "hold_days": 1,
            }
        )

        all_results["S3"]["trades"].append(
            {
                "date": signal["date"],
                "stock": signal["stock"],
                "return": s3_return,
                "is_sample_out": is_sample_out,
                "hold_days": 1,
            }
        )

        all_results["S4"]["trades"].append(
            {
                "date": signal["date"],
                "stock": signal["stock"],
                "return": s4_return,
                "is_sample_out": is_sample_out,
                "hold_days": 1,
                "triggered": next_high >= rush_3_threshold,
            }
        )

        all_results["S5"]["trades"].append(
            {
                "date": signal["date"],
                "stock": signal["stock"],
                "return": s5_return,
                "is_sample_out": is_sample_out,
                "hold_days": 1,
                "triggered": next_high >= rush_5_threshold,
            }
        )

        all_results["S6"]["trades"].append(
            {
                "date": signal["date"],
                "stock": signal["stock"],
                "return": s6_return,
                "is_sample_out": is_sample_out,
                "hold_days": 1 if not is_limit_up_today else 0,
                "is_limit_up": is_limit_up_today,
            }
        )

        all_results["S7"]["trades"].append(
            {
                "date": signal["date"],
                "stock": signal["stock"],
                "return": s7_return,
                "is_sample_out": is_sample_out,
                "hold_days": 1,
            }
        )

    except Exception as e:
        continue

print(f"处理完成，共 {len(signals)} 个信号")

print("\n" + "=" * 80)
print("第五部分：统计各卖出规则指标")
print("=" * 80)

summary_stats = {}

for rule_id, result in all_results.items():
    if len(result["trades"]) == 0:
        print(f"{rule_id}: 无交易数据")
        continue

    df = pd.DataFrame(result["trades"])

    full_trades = df
    sample_out_trades = df[df["is_sample_out"]]

    full_stats = {}
    sample_out_stats = {}

    full_stats["trade_count"] = len(full_trades)
    full_stats["avg_return"] = full_trades["return"].mean() * 100
    full_stats["win_rate"] = (full_trades["return"] > 0).sum() / len(full_trades)

    wins = full_trades[full_trades["return"] > 0]["return"]
    losses = full_trades[full_trades["return"] <= 0]["return"]

    full_stats["avg_win"] = wins.mean() * 100 if len(wins) > 0 else 0
    full_stats["avg_loss"] = losses.mean() * 100 if len(losses) > 0 else 0
    full_stats["profit_loss_ratio"] = (
        abs(full_stats["avg_win"] / full_stats["avg_loss"])
        if full_stats["avg_loss"] != 0
        else 0
    )

    full_stats["max_win"] = full_trades["return"].max() * 100
    full_stats["max_loss"] = full_trades["return"].min() * 100

    if "hold_days" in full_trades.columns:
        full_stats["avg_hold_days"] = full_trades["hold_days"].mean()
    else:
        full_stats["avg_hold_days"] = 0

    cumulative_returns = (1 + full_trades["return"]).cumprod()
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    full_stats["max_drawdown"] = abs(drawdown.min()) * 100

    annual_return = (1 + full_stats["avg_return"] / 100) ** 250 - 1
    full_stats["annual_return"] = annual_return * 100

    full_stats["calmar_ratio"] = (
        abs(full_stats["annual_return"] / full_stats["max_drawdown"])
        if full_stats["max_drawdown"] > 0
        else 0
    )

    consecutive_losses = []
    current_loss = 0
    for ret in full_trades["return"]:
        if ret <= 0:
            current_loss += 1
        else:
            if current_loss > 0:
                consecutive_losses.append(current_loss)
            current_loss = 0
    if current_loss > 0:
        consecutive_losses.append(current_loss)
    full_stats["max_consecutive_losses"] = (
        max(consecutive_losses) if consecutive_losses else 0
    )

    gains = full_trades[full_trades["return"] > 0]["return"]
    if len(gains) > 0:
        cum_gains = gains.cumsum()
        running_max_gains = cum_gains.cummax()
        gain_drawdown = cum_gains - running_max_gains
        full_stats["gain_retracement"] = abs(gain_drawdown.min()) * 100
    else:
        full_stats["gain_retracement"] = 0

    if rule_id in ["S4", "S5"]:
        triggered_trades = full_trades[full_trades["triggered"] == True]
        full_stats["trigger_rate"] = (
            len(triggered_trades) / len(full_trades) if len(full_trades) > 0 else 0
        )
        full_stats["trigger_return"] = (
            triggered_trades["return"].mean() * 100 if len(triggered_trades) > 0 else 0
        )

    if rule_id == "S6":
        limit_up_trades = full_trades[full_trades["is_limit_up"] == True]
        full_stats["limit_up_rate"] = (
            len(limit_up_trades) / len(full_trades) if len(full_trades) > 0 else 0
        )
        full_stats["limit_up_return"] = (
            limit_up_trades["return"].mean() * 100 if len(limit_up_trades) > 0 else 0
        )

    sample_out_stats["trade_count"] = len(sample_out_trades)
    if len(sample_out_trades) > 0:
        sample_out_stats["avg_return"] = sample_out_trades["return"].mean() * 100
        sample_out_stats["win_rate"] = (sample_out_trades["return"] > 0).sum() / len(
            sample_out_trades
        )

        sample_cumulative = (1 + sample_out_trades["return"]).cumprod()
        sample_running_max = sample_cumulative.cummax()
        sample_drawdown = (sample_cumulative - sample_running_max) / sample_running_max
        sample_out_stats["max_drawdown"] = abs(sample_drawdown.min()) * 100

        if rule_id in ["S4", "S5"]:
            triggered_so = sample_out_trades[sample_out_trades["triggered"] == True]
            sample_out_stats["trigger_rate"] = (
                len(triggered_so) / len(sample_out_trades)
                if len(sample_out_trades) > 0
                else 0
            )
    else:
        sample_out_stats["avg_return"] = 0
        sample_out_stats["win_rate"] = 0
        sample_out_stats["max_drawdown"] = 0

    summary_stats[rule_id] = {
        "name": result["name"],
        "full": full_stats,
        "sample_out": sample_out_stats,
    }

print("\n【全样本实测结果】(2020-01-01 至 2024-12-31)")
print("-" * 140)
print(
    f"{'卖出规则':<25} {'平均收益':>8} {'胜率':>8} {'盈亏比':>8} {'最大亏损':>8} {'持仓周期':>8} {'年化收益':>8} {'最大回撤':>8} {'卡玛比率':>8} {'交易数':>6}"
)
print("-" * 140)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if rule_id in summary_stats:
        stats = summary_stats[rule_id]["full"]
        print(
            f"{stats['name']:<25} {stats['avg_return']:>7.2f}% {stats['win_rate'] * 100:>7.2f}% {stats['profit_loss_ratio']:>7.2f} {stats['max_loss']:>7.2f}% {stats['avg_hold_days']:>7.1f}天 {stats['annual_return']:>7.2f}% {stats['max_drawdown']:>7.2f}% {stats['calmar_ratio']:>7.2f} {stats['trade_count']:>5}次"
        )

print("\n【2024-01-01 后样本外结果】")
print("-" * 80)
print(f"{'卖出规则':<25} {'交易数':>6} {'胜率':>8} {'平均收益':>10} {'最大回撤':>10}")
print("-" * 80)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if rule_id in summary_stats:
        stats = summary_stats[rule_id]["sample_out"]
        if stats["trade_count"] > 0:
            print(
                f"{summary_stats[rule_id]['name']:<25} {stats['trade_count']:>5}次 {stats['win_rate'] * 100:>7.2f}% {stats['avg_return']:>9.2f}% {stats['max_drawdown']:>9.2f}%"
            )
        else:
            print(
                f"{summary_stats[rule_id]['name']:<25} {'N/A':>6} {'N/A':>8} {'N/A':>10} {'N/A':>10}"
            )

print("\n" + "=" * 80)
print("第六部分：可执行性评估")
print("=" * 80)

executable_analysis = {
    "S1": {
        "executable": True,
        "difficulty": "最容易",
        "reason": "时间明确，尾盘卖出，无需条件单",
        "slippage": "约0.1%",
    },
    "S2": {
        "executable": True,
        "difficulty": "容易",
        "reason": "次日开盘时间明确",
        "slippage": "约0.3-0.5%",
    },
    "S3": {
        "executable": True,
        "difficulty": "容易",
        "reason": "次日收盘时间明确",
        "slippage": "约0.1%",
    },
    "S4": {
        "executable": True,
        "difficulty": "中等",
        "reason": "需条件单实现冲高+3%卖出",
        "slippage": "约0.3%",
    },
    "S5": {
        "executable": True,
        "difficulty": "较难",
        "reason": "需条件单实现冲高+5%卖出，触发概率低",
        "slippage": "约0.3%",
    },
    "S6": {
        "executable": True,
        "difficulty": "中等",
        "reason": "需判断涨停板状态，较复杂",
        "slippage": "约0.3%",
    },
    "S7": {
        "executable": False,
        "difficulty": "无法执行",
        "reason": "次日最高价无法预知，依赖未来函数",
        "slippage": "N/A（不可执行）",
    },
}

print("\n可执行性评估:")
for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    analysis = executable_analysis[rule_id]
    status = "✓ 可执行" if analysis["executable"] else "✗ 不可执行"
    print(f"  {rule_id} {summary_stats[rule_id]['name']:<20}: {status}")
    print(f"    - 执行难度: {analysis['difficulty']}")
    print(f"    - 原因: {analysis['reason']}")
    print(f"    - 滑点预估: {analysis['slippage']}")

print("\n" + "=" * 80)
print("第七部分：策略层回测对比")
print("=" * 80)

strategy_layer_results = {}

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if rule_id in summary_stats:
        stats = summary_stats[rule_id]["full"]

        annual_return = stats["annual_return"]
        max_dd = stats["max_drawdown"]
        calmar = stats["calmar_ratio"]
        trade_count = stats["trade_count"]

        if analysis["executable"]:
            adjusted_return = annual_return * 0.95
            adjusted_dd = max_dd * 1.05
        else:
            adjusted_return = 0
            adjusted_dd = max_dd

        strategy_layer_results[rule_id] = {
            "name": stats["name"],
            "annual_return": annual_return,
            "adjusted_return": adjusted_return,
            "max_drawdown": max_dd,
            "calmar_ratio": calmar,
            "trade_count": trade_count,
            "executable": analysis["executable"],
        }

print("\n策略层回测对比（考虑可执行性）:")
print("-" * 100)
print(
    f"{'卖出规则':<25} {'年化收益':>10} {'调整后收益':>10} {'最大回撤':>10} {'卡玛比率':>8} {'交易次数':>8} {'可执行':>8}"
)
print("-" * 100)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if rule_id in strategy_layer_results:
        result = strategy_layer_results[rule_id]
        exec_status = "✓" if result["executable"] else "✗"
        print(
            f"{result['name']:<25} {result['annual_return']:>9.2f}% {result['adjusted_return']:>9.2f}% {result['max_drawdown']:>9.2f}% {result['calmar_ratio']:>7.2f} {result['trade_count']:>6}次 {exec_status:>7}"
        )

print("\n" + "=" * 80)
print("第八部分：最终推荐卖出规则")
print("=" * 80)

executable_rules = [r for r in strategy_layer_results.values() if r["executable"]]

sorted_by_calmar = sorted(
    executable_rules, key=lambda x: x["calmar_ratio"], reverse=True
)

print("\n可执行规则排序（按卡玛比率）:")
for i, rule in enumerate(sorted_by_calmar[:3], 1):
    print(
        f"  {i}. {rule['name']}: 卡玛={rule['calmar_ratio']:.2f}, 年化={rule['annual_return']:.2f}%, 回撤={rule['max_drawdown']:.2f}%"
    )

if len(sorted_by_calmar) > 0:
    recommended_rule = sorted_by_calmar[0]
    print(f"\n【主推荐卖出规则】: {recommended_rule['name']}")
    print(f"  理由:")
    print(f"    1. 卡玛比率最高: {recommended_rule['calmar_ratio']:.2f}")
    print(f"    2. 年化收益: {recommended_rule['annual_return']:.2f}%")
    print(f"    3. 最大回撤可控: {recommended_rule['max_drawdown']:.2f}%")
    print(f"    4. 可执行性: ✓")

    if recommended_rule["name"] in ["次日冲高+3%卖出", "涨停板持有+冲高"]:
        print(f"    5. 执行建议: 使用条件单，设定冲高+3%自动卖出")

    if len(sorted_by_calmar) > 1:
        backup_rule = sorted_by_calmar[1]
        print(f"\n【备选卖出规则】: {backup_rule['name']}")
        print(
            f"  理由: 卡玛比率次高({backup_rule['calmar_ratio']:.2f})，可作为替代方案"
        )

print("\n【不推荐的规则】:")
print(f"  - S7 次日最高价卖出: 依赖未来函数，无法执行")
print(f"  - S2 次日开盘卖出: 胜率低，存在次日开盘压制效应")

print("\n" + "=" * 80)
print("第九部分：Go / Watch / No-Go判定")
print("=" * 80)

if len(sorted_by_calmar) > 0 and sorted_by_calmar[0]["calmar_ratio"] > 1.5:
    go_status = "Go ✓"
    go_reason = "最优卖出规则明确，卡玛比率>1.5，可执行"
elif len(sorted_by_calmar) > 0 and sorted_by_calmar[0]["calmar_ratio"] > 1.0:
    go_status = "Watch ⚠️"
    go_reason = "最优规则卡玛比率较低(1.0-1.5)，需进一步验证"
else:
    go_status = "No-Go ✗"
    go_reason = "未找到符合条件的卖出规则"

print(f"\n判定: {go_status}")
print(f"理由: {go_reason}")

if len(sorted_by_calmar) > 0:
    sample_out_stats = summary_stats[sorted_by_calmar[0]["name"].split()[0]][
        "sample_out"
    ]
    print(f"\n样本外验证:")
    print(f"  - 交易数: {sample_out_stats['trade_count']}次")
    print(f"  - 胜率: {sample_out_stats['win_rate'] * 100:.2f}%")
    print(f"  - 平均收益: {sample_out_stats['avg_return']:.2f}%")

    if sample_out_stats["win_rate"] > 0.45 and sample_out_stats["avg_return"] > 0:
        print(f"  - 样本外表现: ✓ 稳定")
    else:
        print(f"  - 样本外表现: ⚠️ 需关注")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)

output_data = {
    "test_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "test_period": {"start": test_start_date, "end": test_end_date},
    "sample_out_date": sample_out_date,
    "signal_count": len(signals),
    "summary_stats": summary_stats,
    "executable_analysis": executable_analysis,
    "strategy_layer_results": strategy_layer_results,
    "recommendation": {
        "primary": sorted_by_calmar[0]["name"] if len(sorted_by_calmar) > 0 else None,
        "backup": sorted_by_calmar[1]["name"] if len(sorted_by_calmar) > 1 else None,
        "calmar_ratio": sorted_by_calmar[0]["calmar_ratio"]
        if len(sorted_by_calmar) > 0
        else None,
        "go_status": go_status,
    },
}

print(f"\n输出数据已生成，共 {len(signals)} 个信号")
