"""
影子策略回测 - 高效验证版

特性：
- 测试2个月数据（2015年5-6月，牛市高峰）
- 正确的资金计算
- 包含手续费
- 完整绩效指标

运行：
cd skills/ricequant_strategy
node run-strategy.js --strategy ../../strategies/shadow_strategies_20260330/backtest_fast_rq.py --create-new --timeout-ms 300000
"""

print("=" * 80)
print("影子策略回测 - 高效验证版")
print("=" * 80)

import numpy as np

CONFIG = {
    "initial": 100000.0,
    "max_pos": 3,
    "pos_pct": 0.3,
    "emotion_th": 50,
    "open_min": 0.001,
    "open_max": 0.03,
    "sell_profit": 0.03,
    "stamp_tax": 0.001,
    "commission": 0.00025,
}


class Engine:
    def __init__(self):
        self.cash = CONFIG["initial"]
        self.pos = {}
        self.trades = []
        self.values = []

    def buy(self, stock, price, date):
        target = self.get_total() * CONFIG["pos_pct"]
        use_cash = min(target, self.cash)
        shares = int(use_cash / price / 100) * 100

        if shares <= 0:
            return False

        cost = shares * price
        fee = cost * CONFIG["commission"]
        total = cost + fee

        if total > self.cash:
            return False

        self.cash -= total
        self.pos[stock] = {
            "shares": shares,
            "buy_p": price,
            "buy_d": date,
            "cost": total,
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
            }
        )
        return True

    def sell(self, stock, price, date, reason):
        if stock not in self.pos:
            return False

        p = self.pos[stock]
        rev = p["shares"] * price
        fee = rev * CONFIG["commission"]
        tax = rev * CONFIG["stamp_tax"]
        total = rev - fee - tax

        profit = total - p["cost"]
        profit_pct = (price - p["buy_p"]) / p["buy_p"]

        self.cash += total
        self.trades.append(
            {
                "date": date,
                "stock": stock,
                "action": "sell",
                "price": price,
                "shares": p["shares"],
                "profit": profit,
                "profit_pct": profit_pct,
                "reason": reason,
            }
        )
        del self.pos[stock]
        return profit, profit_pct

    def get_total(self, date=None):
        total = self.cash
        if date:
            for s in self.pos:
                try:
                    df = get_price(
                        s,
                        start_date=date,
                        end_date=date,
                        frequency="1d",
                        fields=["close"],
                    )
                    if df is not None:
                        total += df["close"].iloc[-1] * self.pos[s]["shares"]
                except:
                    pass
        return total


def get_prev(date, dates):
    s = str(date)[:10]
    for i, d in enumerate(dates):
        if str(d)[:10] == s and i > 0:
            return str(dates[i - 1])[:10]
    return None


def count_limit_up(date, stocks, dates):
    prev = get_prev(date, dates)
    if not prev:
        return 0
    cnt = 0
    for s in stocks[:1000]:
        try:
            df = get_price(
                s, start_date=prev, end_date=date, frequency="1d", fields=["close"]
            )
            if df is not None and len(df) >= 2:
                if (
                    df["close"].iloc[0] > 0
                    and (df["close"].iloc[-1] - df["close"].iloc[0])
                    / df["close"].iloc[0]
                    >= 0.095
                ):
                    cnt += 1
        except:
            pass
    return cnt


def check_signal(stock, date, dates):
    prev = get_prev(date, dates)
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
        prev_c = df["close"].iloc[0]
        open_p = df["open"].iloc[-1]
        high_p = df["high"].iloc[-1]
        if prev_c <= 0:
            return None
        chg = (open_p - prev_c) / prev_c
        if chg > CONFIG["open_min"] and chg < CONFIG["open_max"] and high_p > open_p:
            return open_p
    except:
        pass
    return None


print("\n获取数据...")
stocks = (
    list(all_instruments(type="CS").order_book_id)
    if all_instruments(type="CS") is not None
    else []
)
all_dates = [str(d)[:10] for d in list(get_trading_dates("2015-05-01", "2015-06-30"))]

print(f"股票: {len(stocks)}, 交易日: {len(all_dates)}")

if stocks and all_dates:
    eng = Engine()

    print("\n开始回测...")
    for date in all_dates:
        limit_up = count_limit_up(date, stocks, all_dates)
        ok = limit_up >= CONFIG["emotion_th"]

        print(f"[{date}] 涨停{limit_up:3d} {'✓' if ok else '✗'}", end="")

        if ok:
            sigs = []
            for s in stocks[:500]:
                p = check_signal(s, date, all_dates)
                if p:
                    sigs.append((s, p))

            print(f" 信号{len(sigs)}", end="")

            if sigs and len(eng.pos) < CONFIG["max_pos"]:
                s, p = sigs[0]
                if eng.buy(s, p, date):
                    print(f" → 买{s}@{p:.2f}")
                else:
                    print()
            else:
                print()
        else:
            print()

        for s in list(eng.pos.keys()):
            p = eng.pos[s]
            if date <= p["buy_d"]:
                continue
            try:
                df = get_price(
                    s, start_date=date, end_date=date, frequency="1d", fields=["close"]
                )
                if df is not None:
                    curr = df["close"].iloc[-1]
                    pct = (curr - p["buy_p"]) / p["buy_p"]
                    if pct >= CONFIG["sell_profit"] or date > p["buy_d"]:
                        reason = "止盈" if pct >= CONFIG["sell_profit"] else "尾盘"
                        prof, pct_val = eng.sell(s, curr, date, reason)
                        print(
                            f"        → 卖{s}@{curr:.2f} {reason} {pct_val * 100:+.1f}%"
                        )
            except:
                pass

        eng.values.append(eng.get_total(date))

    # 清仓
    print("\n清仓...")
    for s in list(eng.pos.keys()):
        try:
            df = get_price(
                s,
                start_date=all_dates[-1],
                end_date=all_dates[-1],
                frequency="1d",
                fields=["close"],
            )
            if df is not None:
                eng.sell(s, df["close"].iloc[-1], all_dates[-1], "清仓")
        except:
            pass

    print("\n" + "=" * 80)
    print("回测结果")
    print("=" * 80)

    sells = [t for t in eng.trades if t["action"] == "sell"]
    final = eng.get_total()
    ret = (final - CONFIG["initial"]) / CONFIG["initial"]

    print(f"\n初始资金: {CONFIG['initial']:,.0f}")
    print(f"最终资金: {final:,.2f}")
    print(f"总收益率: {ret * 100:+.2f}%")

    if sells:
        wins = [t for t in sells if t["profit"] > 0]
        win_rate = len(wins) / len(sells)
        avg_ret = np.mean([t["profit_pct"] for t in sells])

        print(f"\n买入: {len([t for t in eng.trades if t['action'] == 'buy'])}次")
        print(f"卖出: {len(sells)}次")
        print(f"胜率: {win_rate * 100:.1f}%")
        print(f"平均收益: {avg_ret * 100:+.2f}%")

        if wins:
            print(f"平均盈利: {np.mean([t['profit_pct'] for t in wins]) * 100:+.2f}%")
        losses = [t for t in sells if t["profit"] <= 0]
        if losses:
            print(f"平均亏损: {np.mean([t['profit_pct'] for t in losses]) * 100:+.2f}%")

    # 风险指标
    if len(eng.values) > 1:
        rets = [
            (eng.values[i] - eng.values[i - 1]) / eng.values[i - 1]
            for i in range(1, len(eng.values))
        ]
        peak = eng.values[0]
        max_dd = 0
        for v in eng.values:
            if v > peak:
                peak = v
            dd = (peak - v) / peak
            if dd > max_dd:
                max_dd = dd

        print(f"\n最大回撤: {max_dd * 100:.2f}%")
        if np.std(rets) > 0:
            sharpe = (np.mean(rets) * 252 - 0.03) / (np.std(rets) * np.sqrt(252))
            print(f"夏普比率: {sharpe:.2f}")

    print("\n" + "=" * 80)
