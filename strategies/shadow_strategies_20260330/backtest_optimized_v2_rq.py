"""
影子策略回测 - 优化版 (RiceQuant Notebook)

优化项：
1. 每天最多买入1次
2. 只选最强信号（按开盘涨幅排序）
3. 每天收盘前强制平仓（T+1策略）
4. 单票全仓（避免仓位分散）
5. 严格止盈止损

运行：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/backtest_optimized_v2_rq.py --create-new --timeout-ms 300000
"""

print("=" * 80)
print("影子策略回测 - 优化版")
print("=" * 80)

import numpy as np

CONFIG = {
    "initial": 100000.0,
    "emotion_th": 50,  # 涨停阈值
    "open_min": 0.001,  # 最小开盘涨幅 0.1%
    "open_max": 0.03,  # 最大开盘涨幅 3%
    "sell_profit": 0.03,  # 止盈 3%
    "sell_loss": -0.02,  # 止损 -2%
    "max_daily_buy": 1,  # 每天最多买入1次
    "max_positions": 1,  # 最多持有1只
    "stamp_tax": 0.001,  # 印花税
    "commission": 0.00025,  # 佣金
}

print(f"\n优化策略参数:")
print(f"  情绪阈值: 涨停>={CONFIG['emotion_th']}只")
print(f"  开盘涨幅: {CONFIG['open_min'] * 100:.1f}% - {CONFIG['open_max'] * 100:.0f}%")
print(
    f"  止盈: +{CONFIG['sell_profit'] * 100:.0f}% | 止损: {CONFIG['sell_loss'] * 100:.0f}%"
)
print(f"  交易规则: T+1，每天最多{CONFIG['max_daily_buy']}笔买入")
print(f"  持仓上限: {CONFIG['max_positions']}只")


class OptimizedEngine:
    def __init__(self):
        self.cash = CONFIG["initial"]
        self.position = None  # 只持有一只
        self.trades = []
        self.values = []
        self.daily_stats = []

    def buy(self, stock, price, date, open_chg):
        """买入 - 全仓单票"""
        if self.position:
            return False  # 已有持仓

        # 计算可买股数（全仓）
        shares = int(self.cash / price / 100) * 100

        if shares <= 0:
            return False

        cost = shares * price
        fee = cost * CONFIG["commission"]
        total_cost = cost + fee

        if total_cost > self.cash:
            return False

        self.cash -= total_cost
        self.position = {
            "stock": stock,
            "shares": shares,
            "buy_price": price,
            "buy_date": date,
            "open_chg": open_chg,
            "cost": total_cost,
        }

        self.trades.append(
            {
                "date": date,
                "stock": stock,
                "action": "buy",
                "price": price,
                "shares": shares,
                "cost": cost,
                "fee": fee,
                "open_chg": open_chg,
            }
        )

        return True

    def sell(self, price, date, reason):
        """卖出"""
        if not self.position:
            return None

        p = self.position
        rev = p["shares"] * price
        fee = rev * CONFIG["commission"]
        tax = rev * CONFIG["stamp_tax"]
        net_rev = rev - fee - tax

        profit = net_rev - p["cost"]
        profit_pct = (price - p["buy_price"]) / p["buy_price"]

        self.cash += net_rev

        self.trades.append(
            {
                "date": date,
                "stock": p["stock"],
                "action": "sell",
                "price": price,
                "shares": p["shares"],
                "profit": profit,
                "profit_pct": profit_pct,
                "reason": reason,
                "hold_days": 1,  # T+1
            }
        )

        result = {
            "stock": p["stock"],
            "profit": profit,
            "profit_pct": profit_pct,
            "reason": reason,
        }

        self.position = None
        return result

    def get_total_value(self, date):
        """计算总资产"""
        total = self.cash
        if self.position:
            try:
                df = get_price(
                    self.position["stock"],
                    start_date=date,
                    end_date=date,
                    frequency="1d",
                    fields=["close"],
                )
                if df is not None and len(df) > 0:
                    total += df["close"].iloc[-1] * self.position["shares"]
            except:
                pass
        return total


def get_prev_date(date, dates):
    s = str(date)[:10]
    for i, d in enumerate(dates):
        if str(d)[:10] == s and i > 0:
            return str(dates[i - 1])[:10]
    return None


def count_limit_ups(date, stocks, dates):
    """统计涨停数量"""
    prev = get_prev_date(date, dates)
    if not prev:
        return 0

    cnt = 0
    for s in stocks[:1000]:  # 测试前1000只
        try:
            df = get_price(
                s, start_date=prev, end_date=date, frequency="1d", fields=["close"]
            )
            if df is not None and len(df) >= 2:
                prev_c = df["close"].iloc[0]
                if prev_c > 0:
                    pct = (df["close"].iloc[-1] - prev_c) / prev_c
                    if pct >= 0.095:
                        cnt += 1
        except:
            pass
    return cnt


def find_best_signal(stocks, date, dates):
    """找到最佳信号（按开盘涨幅排序）"""
    prev = get_prev_date(date, dates)
    if not prev:
        return None

    best_signal = None
    best_chg = 0

    for s in stocks[:500]:  # 在前500只中找
        try:
            df = get_price(
                s,
                start_date=prev,
                end_date=date,
                frequency="1d",
                fields=["close", "open", "high"],
            )
            if df is None or len(df) < 2:
                continue

            prev_c = df["close"].iloc[0]
            open_p = df["open"].iloc[-1]
            high_p = df["high"].iloc[-1]

            if prev_c <= 0:
                continue

            chg = (open_p - prev_c) / prev_c

            # 条件：开盘涨幅在范围内，且最高价>开盘价
            if (
                chg > CONFIG["open_min"]
                and chg < CONFIG["open_max"]
                and high_p > open_p
            ):
                if chg > best_chg:  # 选开盘涨幅最大的
                    best_chg = chg
                    best_signal = {"stock": s, "open_price": open_p, "open_chg": chg}
        except:
            pass

    return best_signal


print("\n获取数据...")
try:
    stocks = list(all_instruments(type="CS").order_book_id)
except:
    stocks = []

dates = [str(d)[:10] for d in list(get_trading_dates("2015-05-01", "2015-06-30"))]

print(f"股票: {len(stocks)}, 交易日: {len(dates)}")

if stocks and dates:
    eng = OptimizedEngine()

    print("\n开始回测...")
    print("-" * 80)

    for i, date in enumerate(dates):
        # 1. 检查情绪
        limit_up = count_limit_ups(date, stocks, dates)
        emotion_ok = limit_up >= CONFIG["emotion_th"]

        status = "✓" if emotion_ok else "✗"
        print(f"[{date}] 涨停{limit_up:3d} {status}", end="")

        # 2. 情绪达标且有持仓，检查是否卖出
        if eng.position:
            p = eng.position
            try:
                df = get_price(
                    p["stock"],
                    start_date=date,
                    end_date=date,
                    frequency="1d",
                    fields=["close"],
                )
                if df is not None and len(df) > 0:
                    curr_price = df["close"].iloc[-1]
                    profit_pct = (curr_price - p["buy_price"]) / p["buy_price"]

                    # 卖出条件：止盈、止损、或T+1尾盘
                    should_sell = False
                    reason = ""

                    if profit_pct >= CONFIG["sell_profit"]:
                        should_sell = True
                        reason = "止盈"
                    elif profit_pct <= CONFIG["sell_loss"]:
                        should_sell = True
                        reason = "止损"
                    elif date > p["buy_date"]:  # T+1，次日必须卖
                        should_sell = True
                        reason = "T+1尾盘"

                    if should_sell:
                        result = eng.sell(curr_price, date, reason)
                        if result:
                            print(
                                f" → 卖出{result['stock']}@{curr_price:.2f} {reason} {result['profit_pct'] * 100:+.1f}%"
                            )
                        else:
                            print()
                    else:
                        print(f" 持仓{p['stock']} {profit_pct * 100:+.1f}%")
                else:
                    print(f" 持仓{p['stock']} (无价格)")
            except Exception as e:
                print(f" 持仓{p['stock']} (错误: {str(e)[:20]})")

        # 3. 情绪达标且无持仓，尝试买入
        elif emotion_ok and not eng.position:
            signal = find_best_signal(stocks, date, dates)

            if signal:
                print(
                    f" 最佳信号{signal['stock']} 开盘+{signal['open_chg'] * 100:.2f}%",
                    end="",
                )

                if eng.buy(
                    signal["stock"], signal["open_price"], date, signal["open_chg"]
                ):
                    print(f" → 买入")
                else:
                    print(f" (买入失败)")
            else:
                print(f" 无有效信号")
        else:
            if not emotion_ok:
                print(f" 情绪不足")
            else:
                print()

        # 4. 记录每日资产
        total = eng.get_total_value(date)
        eng.values.append(total)
        eng.daily_stats.append(
            {
                "date": date,
                "total": total,
                "cash": eng.cash,
                "has_position": eng.position is not None,
            }
        )

        # 5. 定期报告
        if (i + 1) % 20 == 0:
            sells = [t for t in eng.trades if t["action"] == "sell"]
            wins = [t for t in sells if t["profit"] > 0]
            win_rate = len(wins) / len(sells) if sells else 0

            print(f"\n{'=' * 80}")
            print(
                f"进度: {i + 1}/{len(dates)} | 资产: {total:,.0f} | 胜率: {win_rate * 100:.0f}%"
            )
            print(f"{'=' * 80}")

    # 最后清仓
    print("\n" + "=" * 80)
    print("最后清仓...")
    print("=" * 80)

    if eng.position:
        try:
            df = get_price(
                eng.position["stock"],
                start_date=dates[-1],
                end_date=dates[-1],
                frequency="1d",
                fields=["close"],
            )
            if df is not None:
                result = eng.sell(df["close"].iloc[-1], dates[-1], "结束清仓")
                if result:
                    print(
                        f"  清仓 {result['stock']} 收益{result['profit_pct'] * 100:+.1f}%"
                    )
        except:
            pass

    # 绩效统计
    print("\n" + "=" * 80)
    print("回测结果")
    print("=" * 80)

    final_value = eng.get_total_value(dates[-1])
    total_return = (final_value - CONFIG["initial"]) / CONFIG["initial"]

    sells = [t for t in eng.trades if t["action"] == "sell"]
    buys = [t for t in eng.trades if t["action"] == "buy"]

    print(f"\n【资金绩效】")
    print(f"  初始资金: {CONFIG['initial']:,.0f}元")
    print(f"  最终资金: {final_value:,.2f}元")
    print(f"  总收益率: {total_return * 100:+.2f}%")
    print(f"  总盈亏额: {final_value - CONFIG['initial']:+.2f}元")

    # 交易成本
    total_fee = sum([t.get("fee", 0) for t in eng.trades])
    total_tax = sum([t.get("tax", 0) for t in eng.trades if t["action"] == "sell"])
    print(f"\n【交易成本】")
    print(f"  佣金: {total_fee:.2f}元")
    print(f"  印花税: {total_tax:.2f}元")
    print(f"  总成本: {total_fee + total_tax:.2f}元")

    print(f"\n【交易统计】")
    print(f"  买入: {len(buys)}次 | 卖出: {len(sells)}次")

    if sells:
        wins = [t for t in sells if t["profit"] > 0]
        losses = [t for t in sells if t["profit"] <= 0]

        win_rate = len(wins) / len(sells)
        avg_ret = np.mean([t["profit_pct"] for t in sells])

        print(f"  胜率: {win_rate * 100:.1f}% ({len(wins)}/{len(sells)})")
        print(f"  平均收益率: {avg_ret * 100:+.2f}%")

        if wins:
            print(f"  平均盈利: {np.mean([t['profit_pct'] for t in wins]) * 100:+.2f}%")
        if losses:
            print(
                f"  平均亏损: {np.mean([t['profit_pct'] for t in losses]) * 100:+.2f}%"
            )

    # 风险指标
    if len(eng.values) > 1:
        rets = [
            (eng.values[i] - eng.values[i - 1]) / eng.values[i - 1]
            for i in range(1, len(eng.values))
        ]

        # 最大回撤
        peak = eng.values[0]
        max_dd = 0
        for v in eng.values:
            if v > peak:
                peak = v
            dd = (peak - v) / peak
            if dd > max_dd:
                max_dd = dd

        # 夏普
        if np.std(rets) > 0:
            sharpe = (np.mean(rets) * 252 - 0.03) / (np.std(rets) * np.sqrt(252))
        else:
            sharpe = 0

        print(f"\n【风险指标】")
        print(f"  最大回撤: {max_dd * 100:.2f}%")
        print(f"  夏普比率: {sharpe:.2f}")

    print("\n" + "=" * 80)
    print("优化版回测完成")
    print("=" * 80)
