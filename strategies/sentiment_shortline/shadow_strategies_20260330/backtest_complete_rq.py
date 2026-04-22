"""
影子策略回测 - 完善版 (RiceQuant Notebook)

特性：
1. 正确的资金计算
2. 交易手续费（印花税0.1%，佣金0.025%）
3. 完善的持仓管理
4. 完整的绩效指标（收益率、夏普比率、最大回撤、胜率）
5. 扩大测试范围（1年数据）

运行：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/backtest_complete_rq.py --create-new --timeout-ms 600000
"""

print("=" * 80)
print("影子策略回测 - 完善版")
print("=" * 80)

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

CONFIG = {
    "initial_capital": 100000.0,
    "max_positions": 3,
    "position_size": 0.3,  # 每只30%仓位
    "emotion_threshold": 50,
    "open_change_min": 0.001,
    "open_change_max": 0.03,
    "sell_profit": 0.03,
    "limit_up_sample": 1000,
    "signal_sample": 500,
    "test_start": "2015-01-01",
    "test_end": "2015-12-31",
    # 手续费
    "stamp_tax": 0.001,  # 印花税（卖出）
    "commission": 0.00025,  # 佣金（买卖双向）
}

print(f"\n配置参数:")
print(f"  初始资金: {CONFIG['initial_capital']:,.0f}元")
print(f"  测试时间: {CONFIG['test_start']} 至 {CONFIG['test_end']}")
print(f"  最大持仓: {CONFIG['max_positions']}只")
print(f"  单仓比例: {CONFIG['position_size'] * 100:.0f}%")
print(
    f"  手续费: 印花税{CONFIG['stamp_tax'] * 100:.1f}% + 佣金{CONFIG['commission'] * 100:.3f}%"
)


class BacktestEngine:
    def __init__(self):
        self.cash = CONFIG["initial_capital"]
        self.positions = {}  # {stock: {shares, buy_price, buy_date}}
        self.trades = []  # 交易记录
        self.daily_values = []  # 每日资产

    def calculate_position_value(self, stock, price):
        """计算持仓市值"""
        if stock in self.positions:
            return self.positions[stock]["shares"] * price
        return 0

    def calculate_total_value(self, date, all_stocks, all_dates):
        """计算总资产"""
        total = self.cash
        for stock in list(self.positions.keys()):
            try:
                df = get_price(
                    stock,
                    start_date=date,
                    end_date=date,
                    frequency="1d",
                    fields=["close"],
                )
                if df is not None and len(df) > 0:
                    price = df["close"].iloc[-1]
                    total += price * self.positions[stock]["shares"]
            except:
                pass
        return total

    def buy(self, stock, price, date):
        """买入"""
        # 计算买入金额（目标仓位）
        total_value = self.calculate_total_value(date, [], [])
        target_amount = total_value * CONFIG["position_size"]

        # 实际可用现金
        available_cash = min(target_amount, self.cash)

        # 计算股数（100股整数）
        shares = int(available_cash / price / 100) * 100

        if shares <= 0:
            return False

        cost = shares * price
        commission = cost * CONFIG["commission"]
        total_cost = cost + commission

        if total_cost > self.cash:
            return False

        self.cash -= total_cost
        self.positions[stock] = {
            "shares": shares,
            "buy_price": price,
            "buy_date": date,
            "cost": total_cost,
        }

        self.trades.append(
            {
                "date": date,
                "stock": stock,
                "action": "buy",
                "price": price,
                "shares": shares,
                "amount": cost,
                "commission": commission,
            }
        )

        return True

    def sell(self, stock, price, date, reason):
        """卖出"""
        if stock not in self.positions:
            return False

        pos = self.positions[stock]
        shares = pos["shares"]

        revenue = shares * price
        commission = revenue * CONFIG["commission"]
        stamp_tax = revenue * CONFIG["stamp_tax"]
        total_revenue = revenue - commission - stamp_tax

        self.cash += total_revenue

        profit = total_revenue - pos["cost"]
        profit_pct = (price - pos["buy_price"]) / pos["buy_price"]
        hold_days = (
            datetime.strptime(date, "%Y-%m-%d")
            - datetime.strptime(pos["buy_date"], "%Y-%m-%d")
        ).days

        self.trades.append(
            {
                "date": date,
                "stock": stock,
                "action": "sell",
                "price": price,
                "shares": shares,
                "revenue": revenue,
                "commission": commission,
                "stamp_tax": stamp_tax,
                "profit": profit,
                "profit_pct": profit_pct,
                "hold_days": hold_days,
                "reason": reason,
            }
        )

        del self.positions[stock]
        return True


def get_all_stocks():
    try:
        ins = all_instruments(type="CS")
        return list(ins.order_book_id)
    except Exception as e:
        print(f"获取股票失败: {e}")
        return []


def get_prev_date(date, dates):
    s = str(date)[:10]
    for i, d in enumerate(dates):
        if str(d)[:10] == s and i > 0:
            return str(dates[i - 1])[:10]
    return None


def count_limit_ups(date, stocks, dates):
    prev = get_prev_date(date, dates)
    if not prev:
        return 0, 0

    cnt, tested = 0, 0
    for s in stocks[: CONFIG["limit_up_sample"]]:
        try:
            df = get_price(
                s, start_date=prev, end_date=date, frequency="1d", fields=["close"]
            )
            if df is not None and len(df) >= 2:
                if df["close"].iloc[0] > 0:
                    pct = (df["close"].iloc[-1] - df["close"].iloc[0]) / df[
                        "close"
                    ].iloc[0]
                    if pct >= 0.095:
                        cnt += 1
                    tested += 1
        except:
            pass
    return cnt, tested


def check_signal(stock, date, dates):
    prev = get_prev_date(date, dates)
    if not prev:
        return None

    try:
        df = get_price(
            stock,
            start_date=prev,
            end_date=date,
            frequency="1d",
            fields=["close", "open", "high"],
        )
        if df is None or len(df) < 2:
            return None

        prev_close = df["close"].iloc[0]
        open_p = df["open"].iloc[-1]
        high_p = df["high"].iloc[-1]

        if prev_close <= 0:
            return None

        open_chg = (open_p - prev_close) / prev_close

        if (
            open_chg <= CONFIG["open_change_min"]
            or open_chg >= CONFIG["open_change_max"]
        ):
            return None

        if high_p > open_p:
            return {"open": open_p, "chg": open_chg}
        return None
    except:
        return None


print("\n" + "=" * 80)
print("步骤1: 获取基础数据")
print("=" * 80)

stocks = get_all_stocks()
all_dates = list(get_trading_dates(CONFIG["test_start"], CONFIG["test_end"]))
test_dates = [str(d)[:10] for d in all_dates]

print(f"\n股票总数: {len(stocks)}")
print(f"交易日数: {len(test_dates)}天")
print(f"时间范围: {test_dates[0]} 至 {test_dates[-1]}")

if not stocks or not test_dates:
    print("\n无法获取数据，请确保在 RiceQuant Notebook 环境运行")
else:
    print("\n" + "=" * 80)
    print("步骤2: 开始回测")
    print("=" * 80)

    engine = BacktestEngine()

    for i, date in enumerate(test_dates):
        # 1. 计算涨停数量
        limit_up, tested = count_limit_ups(date, stocks, all_dates)
        emotion_ok = limit_up >= CONFIG["emotion_threshold"]

        status = "✓" if emotion_ok else "✗"
        print(f"\n[{date}] 涨停{limit_up:3d}/{tested:4d} {status}", end="")

        # 2. 情绪达标时生成信号
        if emotion_ok:
            signals = []
            for s in stocks[: CONFIG["signal_sample"]]:
                sig = check_signal(s, date, all_dates)
                if sig:
                    signals.append({"stock": s, "open": sig["open"], "chg": sig["chg"]})

            print(f" 信号{len(signals):3d}个", end="")

            # 3. 买入逻辑
            if signals and len(engine.positions) < CONFIG["max_positions"]:
                sig = signals[0]
                stock = sig["stock"]
                price = sig["open"]

                if engine.buy(stock, price, date):
                    pos = engine.positions[stock]
                    print(f" → 买入{stock}@{price:.2f}x{pos['shares']}")
                else:
                    print()
            else:
                print()
        else:
            print()

        # 4. 卖出逻辑
        for stock in list(engine.positions.keys()):
            pos = engine.positions[stock]
            if date <= pos["buy_date"]:
                continue

            try:
                df = get_price(
                    stock,
                    start_date=date,
                    end_date=date,
                    frequency="1d",
                    fields=["close"],
                )
                if df is not None and len(df) > 0:
                    curr_price = df["close"].iloc[-1]
                    profit_pct = (curr_price - pos["buy_price"]) / pos["buy_price"]

                    should_sell = False
                    reason = ""

                    if profit_pct >= CONFIG["sell_profit"]:
                        should_sell = True
                        reason = "止盈"
                    elif date > pos["buy_date"]:
                        should_sell = True
                        reason = "尾盘"

                    if should_sell:
                        if engine.sell(stock, curr_price, date, reason):
                            t = engine.trades[-1]
                            print(
                                f"        → 卖出{stock}@{curr_price:.2f} {reason} {profit_pct * 100:+.1f}%"
                            )
            except:
                pass

        # 5. 记录每日资产
        total_value = engine.calculate_total_value(date, stocks, all_dates)
        engine.daily_values.append(
            {
                "date": date,
                "cash": engine.cash,
                "positions_value": total_value - engine.cash,
                "total": total_value,
            }
        )

        # 6. 定期报告
        if (i + 1) % 50 == 0:
            print(f"\n{'=' * 80}")
            print(
                f"进度: {i + 1}/{len(test_dates)} ({(i + 1) / len(test_dates) * 100:.1f}%)"
            )
            print(f"总资产: {total_value:,.2f}")
            print(f"持仓数: {len(engine.positions)}")
            print(f"交易数: {len([t for t in engine.trades if t['action'] == 'buy'])}")
            print(f"{'=' * 80}")

    # 清仓
    print("\n" + "=" * 80)
    print("步骤3: 清仓剩余持仓")
    print("=" * 80)

    last_date = test_dates[-1]
    for stock in list(engine.positions.keys()):
        try:
            df = get_price(
                stock,
                start_date=last_date,
                end_date=last_date,
                frequency="1d",
                fields=["close"],
            )
            if df is not None:
                price = df["close"].iloc[-1]
                if engine.sell(stock, price, last_date, "清仓"):
                    t = engine.trades[-1]
                    print(
                        f"  清仓 {stock}@{price:.2f} 收益{t['profit_pct'] * 100:+.1f}%"
                    )
        except:
            pass

    # 计算绩效
    print("\n" + "=" * 80)
    print("步骤4: 绩效分析")
    print("=" * 80)

    buys = [t for t in engine.trades if t["action"] == "buy"]
    sells = [t for t in engine.trades if t["action"] == "sell"]

    final_value = (
        engine.daily_values[-1]["total"]
        if engine.daily_values
        else CONFIG["initial_capital"]
    )
    total_return = (final_value - CONFIG["initial_capital"]) / CONFIG["initial_capital"]

    print(f"\n【资金绩效】")
    print(f"  初始资金: {CONFIG['initial_capital']:,.2f}元")
    print(f"  最终资金: {final_value:,.2f}元")
    print(f"  总收益率: {total_return * 100:+.2f}%")
    print(f"  总盈亏额: {final_value - CONFIG['initial_capital']:+.2f}元")

    # 手续费统计
    total_commission = sum([t.get("commission", 0) for t in engine.trades])
    total_tax = sum([t.get("stamp_tax", 0) for t in engine.trades])
    print(f"\n【交易成本】")
    print(f"  佣金总额: {total_commission:.2f}元")
    print(f"  印花税总额: {total_tax:.2f}元")
    print(f"  总成本: {total_commission + total_tax:.2f}元")

    print(f"\n【交易统计】")
    print(f"  买入次数: {len(buys)}")
    print(f"  卖出次数: {len(sells)}")

    if sells:
        wins = [t for t in sells if t.get("profit", 0) > 0]
        losses = [t for t in sells if t.get("profit", 0) <= 0]

        win_rate = len(wins) / len(sells)
        avg_profit_pct = np.mean([t["profit_pct"] for t in sells])
        avg_hold_days = np.mean([t["hold_days"] for t in sells])

        print(f"  胜率: {win_rate * 100:.1f}% ({len(wins)}/{len(sells)})")
        print(f"  平均收益率: {avg_profit_pct * 100:+.2f}%")
        print(f"  平均持仓天数: {avg_hold_days:.1f}天")

        if wins:
            print(f"  平均盈利: {np.mean([t['profit_pct'] for t in wins]) * 100:+.2f}%")
        if losses:
            print(
                f"  平均亏损: {np.mean([t['profit_pct'] for t in losses]) * 100:+.2f}%"
            )

    # 计算风险指标
    if len(engine.daily_values) > 1:
        values = [v["total"] for v in engine.daily_values]
        returns = [
            (values[i] - values[i - 1]) / values[i - 1] for i in range(1, len(values))
        ]

        # 最大回撤
        max_drawdown = 0
        peak = values[0]
        for v in values:
            if v > peak:
                peak = v
            dd = (peak - v) / peak
            if dd > max_drawdown:
                max_drawdown = dd

        # 年化收益率
        days = len(engine.daily_values)
        years = days / 252
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0

        # 夏普比率（假设无风险利率3%）
        if len(returns) > 1 and np.std(returns) > 0:
            sharpe = (np.mean(returns) * 252 - 0.03) / (np.std(returns) * np.sqrt(252))
        else:
            sharpe = 0

        print(f"\n【风险指标】")
        print(f"  最大回撤: {max_drawdown * 100:.2f}%")
        print(f"  年化收益率: {annual_return * 100:.2f}%")
        print(f"  夏普比率: {sharpe:.2f}")

    print("\n" + "=" * 80)
    print("回测完成")
    print("=" * 80)
