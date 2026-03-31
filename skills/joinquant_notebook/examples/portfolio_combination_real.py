# -*- coding: utf-8 -*-
"""
任务07：组合策略真实回测
使用两个通过验证的策略：首板低开 + 弱转强竞价
"""

import numpy as np
import pandas as pd
from jqdata import *

print("=" * 60)
print("任务07：组合策略真实回测")
print("策略：首板低开 + 弱转强竞价")
print("=" * 60)

# 测试日期范围
start_date = "2024-01-01"
end_date = "2024-06-30"  # 先测试半年
initial_capital = 100000

# 获取交易日
trade_days = list(get_trade_days(start_date, end_date))
print(f"\n测试区间: {start_date} ~ {end_date}")
print(f"交易日数: {len(trade_days)}")

# 存储每日净值
daily_nav = {
    "date": [],
    "first_board_nav": [],
    "weak_to_strong_nav": [],
    "equal_weight_nav": [],
    "risk_parity_nav": [],
}


# 模拟账户
class SimAccount:
    def __init__(self, initial_capital):
        self.cash = initial_capital
        self.positions = {}  # {stock: {'shares': x, 'cost': y}}
        self.nav_history = []

    def get_nav(self, date):
        nav = self.cash
        for stock, pos in self.positions.items():
            try:
                price = get_price(
                    stock,
                    end_date=date,
                    frequency="daily",
                    fields=["close"],
                    count=1,
                    panel=False,
                )
                if not price.empty:
                    nav += pos["shares"] * float(price["close"].iloc[-1])
            except:
                pass
        return nav

    def buy(self, stock, amount, price):
        shares = int(amount / price)
        if shares > 0 and self.cash >= shares * price:
            self.positions[stock] = {"shares": shares, "cost": price}
            self.cash -= shares * price
            return True
        return False

    def sell_all(self, stock, price):
        if stock in self.positions:
            shares = self.positions[stock]["shares"]
            self.cash += shares * price
            del self.positions[stock]
            return True
        return False


# 创建模拟账户
acc_first_board = SimAccount(initial_capital)
acc_weak_to_strong = SimAccount(initial_capital)
acc_equal = SimAccount(initial_capital)
acc_risk_parity = SimAccount(initial_capital)


# 策略信号函数
def get_first_board_signals(date):
    """首板低开信号"""
    try:
        prev_date = get_trade_days("2020-01-01", date)[-2]

        # 基础股票池
        initial_list = get_all_securities("stock", date).index.tolist()
        initial_list = [
            s for s in initial_list if s[:2] != "68" and s[0] not in ["4", "8"]
        ]

        # 昨日涨停
        df = get_price(
            initial_list,
            end_date=prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        if df.empty:
            return []
        df = df.dropna()
        hl_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()

        if not hl_stocks:
            return []

        # 今日开盘价
        today_df = get_price(
            hl_stocks,
            end_date=date,
            frequency="daily",
            fields=["open", "high_limit"],
            count=1,
            panel=False,
        )
        if today_df.empty:
            return []
        today_df = today_df.dropna()
        today_df["open_ratio"] = today_df["open"] / (today_df["high_limit"] / 1.1)

        # 假弱高开 0.5%-1.5%
        signals = today_df[
            (today_df["open_ratio"] > 1.005) & (today_df["open_ratio"] < 1.015)
        ]["code"].tolist()

        return signals[:3]  # 最多3只
    except Exception as e:
        return []


def get_weak_to_strong_signals(date):
    """弱转强竞价信号"""
    try:
        trade_dates = list(get_trade_days("2020-01-01", date))
        prev_date = trade_dates[-2]
        prev_date_2 = trade_dates[-3]
        prev_date_3 = trade_dates[-4]

        # 基础股票池
        initial_list = get_all_securities("stock", date).index.tolist()
        initial_list = [
            s for s in initial_list if s[:2] != "68" and s[0] not in ["4", "8"]
        ]

        # 昨日涨停
        df = get_price(
            initial_list,
            end_date=prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        if df.empty:
            return []
        df = df.dropna()
        hl_stocks = df[df["close"] == df["high_limit"]]["code"].tolist()

        if not hl_stocks:
            return []

        # 排除前两日涨停
        df_2 = get_price(
            initial_list,
            end_date=prev_date_2,
            frequency="daily",
            fields=["high", "high_limit"],
            count=1,
            panel=False,
        )
        prev_hl = (
            df_2[df_2["high"] == df_2["high_limit"]]["code"].tolist()
            if not df_2.empty
            else []
        )

        df_3 = get_price(
            initial_list,
            end_date=prev_date_3,
            frequency="daily",
            fields=["high", "high_limit"],
            count=1,
            panel=False,
        )
        prev_hl2 = (
            df_3[df_3["high"] == df_3["high_limit"]]["code"].tolist()
            if not df_3.empty
            else []
        )

        hl_stocks = [s for s in hl_stocks if s not in set(prev_hl + prev_hl2)]

        if not hl_stocks:
            return []

        # 今日数据
        today_df = get_price(
            hl_stocks,
            end_date=date,
            frequency="daily",
            fields=["open", "high_limit", "money"],
            count=1,
            panel=False,
        )
        if today_df.empty:
            return []
        today_df = today_df.dropna()
        today_df["open_ratio"] = today_df["open"] / (today_df["high_limit"] / 1.1)

        # 高开0-6% + 成交额>5亿
        filtered = today_df[
            (today_df["open_ratio"] > 1.0)
            & (today_df["open_ratio"] < 1.06)
            & (today_df["money"] > 5e8)
        ]

        if filtered.empty:
            return []

        return filtered["code"].tolist()[:3]
    except Exception as e:
        return []


# 每日模拟回测
print("\n开始回测...")

for i, date in enumerate(trade_days):
    if i % 20 == 0:
        print(f"进度: {date}")

    try:
        # 获取当日收盘价用于卖出
        daily_prices = {}

        # 获取信号
        fb_signals = get_first_board_signals(date)
        wts_signals = get_weak_to_strong_signals(date)

        # 获取开盘价
        all_signals = list(set(fb_signals + wts_signals))
        if all_signals:
            open_df = get_price(
                all_signals,
                end_date=date,
                frequency="daily",
                fields=["open", "close"],
                count=1,
                panel=False,
            )
            for _, row in open_df.iterrows():
                daily_prices[row["code"]] = {"open": row["open"], "close": row["close"]}

        # === 首板低开策略 ===
        # 卖出持仓
        for stock in list(acc_first_board.positions.keys()):
            if stock in daily_prices:
                acc_first_board.sell_all(stock, daily_prices[stock]["close"])

        # 买入新信号
        for stock in fb_signals:
            if stock in daily_prices and daily_prices[stock]["open"] > 0:
                amount = acc_first_board.cash * 0.3  # 单只30%仓位
                acc_first_board.buy(stock, amount, daily_prices[stock]["open"])

        # === 弱转强策略 ===
        for stock in list(acc_weak_to_strong.positions.keys()):
            if stock in daily_prices:
                acc_weak_to_strong.sell_all(stock, daily_prices[stock]["close"])

        for stock in wts_signals:
            if stock in daily_prices and daily_prices[stock]["open"] > 0:
                amount = acc_weak_to_strong.cash * 0.3
                acc_weak_to_strong.buy(stock, amount, daily_prices[stock]["open"])

        # === 等权组合 ===
        for stock in list(acc_equal.positions.keys()):
            if stock in daily_prices:
                acc_equal.sell_all(stock, daily_prices[stock]["close"])

        all_buy = fb_signals + wts_signals
        for stock in all_buy:
            if stock in daily_prices and daily_prices[stock]["open"] > 0:
                amount = acc_equal.cash * 0.25
                acc_equal.buy(stock, amount, daily_prices[stock]["open"])

        # === 风险平价组合 ===
        for stock in list(acc_risk_parity.positions.keys()):
            if stock in daily_prices:
                acc_risk_parity.sell_all(stock, daily_prices[stock]["close"])

        # 风险平价: 首板60%, 弱转强40%
        for stock in fb_signals:
            if stock in daily_prices and daily_prices[stock]["open"] > 0:
                amount = acc_risk_parity.cash * 0.4
                acc_risk_parity.buy(stock, amount, daily_prices[stock]["open"])

        for stock in wts_signals:
            if stock in daily_prices and daily_prices[stock]["open"] > 0:
                amount = acc_risk_parity.cash * 0.2
                acc_risk_parity.buy(stock, amount, daily_prices[stock]["open"])

        # 记录净值
        daily_nav["date"].append(date)
        daily_nav["first_board_nav"].append(acc_first_board.get_nav(date))
        daily_nav["weak_to_strong_nav"].append(acc_weak_to_strong.get_nav(date))
        daily_nav["equal_weight_nav"].append(acc_equal.get_nav(date))
        daily_nav["risk_parity_nav"].append(acc_risk_parity.get_nav(date))

    except Exception as e:
        print(f"Error on {date}: {e}")

# 转为DataFrame
df_nav = pd.DataFrame(daily_nav)
print(f"\n有效交易日: {len(df_nav)}")


# 计算收益指标
def calc_metrics(nav_series):
    nav_series = pd.Series(nav_series)
    returns = nav_series.pct_change().dropna()

    total_return = (nav_series.iloc[-1] / nav_series.iloc[0] - 1) * 100
    annual_return = total_return * (250 / len(nav_series))

    # 最大回撤
    cummax = nav_series.cummax()
    drawdown = (nav_series - cummax) / cummax
    max_dd = drawdown.min() * 100

    # 夏普比率
    if returns.std() > 0:
        sharpe = returns.mean() / returns.std() * np.sqrt(250)
    else:
        sharpe = 0

    # 卡玛比率
    calmar = annual_return / abs(max_dd) if max_dd != 0 else 0

    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "max_drawdown": max_dd,
        "sharpe": sharpe,
        "calmar": calmar,
    }


print("\n" + "=" * 60)
print("回测结果")
print("=" * 60)

print("\n1. 首板低开策略:")
fb_metrics = calc_metrics(df_nav["first_board_nav"].tolist())
print(f"   总收益: {fb_metrics['total_return']:.2f}%")
print(f"   年化收益: {fb_metrics['annual_return']:.2f}%")
print(f"   最大回撤: {fb_metrics['max_drawdown']:.2f}%")
print(f"   夏普比率: {fb_metrics['sharpe']:.2f}")
print(f"   卡玛比率: {fb_metrics['calmar']:.2f}")

print("\n2. 弱转强竞价策略:")
wts_metrics = calc_metrics(df_nav["weak_to_strong_nav"].tolist())
print(f"   总收益: {wts_metrics['total_return']:.2f}%")
print(f"   年化收益: {wts_metrics['annual_return']:.2f}%")
print(f"   最大回撤: {wts_metrics['max_drawdown']:.2f}%")
print(f"   夏普比率: {wts_metrics['sharpe']:.2f}")
print(f"   卡玛比率: {wts_metrics['calmar']:.2f}")

print("\n3. 等权组合:")
eq_metrics = calc_metrics(df_nav["equal_weight_nav"].tolist())
print(f"   总收益: {eq_metrics['total_return']:.2f}%")
print(f"   年化收益: {eq_metrics['annual_return']:.2f}%")
print(f"   最大回撤: {eq_metrics['max_drawdown']:.2f}%")
print(f"   夏普比率: {eq_metrics['sharpe']:.2f}")
print(f"   卡玛比率: {eq_metrics['calmar']:.2f}")

print("\n4. 风险平价组合:")
rp_metrics = calc_metrics(df_nav["risk_parity_nav"].tolist())
print(f"   总收益: {rp_metrics['total_return']:.2f}%")
print(f"   年化收益: {rp_metrics['annual_return']:.2f}%")
print(f"   最大回撤: {rp_metrics['max_drawdown']:.2f}%")
print(f"   夏普比率: {rp_metrics['sharpe']:.2f}")
print(f"   卡玛比率: {rp_metrics['calmar']:.2f}")

# 计算相关性
print("\n" + "=" * 60)
print("策略相关性分析")
print("=" * 60)

fb_returns = pd.Series(df_nav["first_board_nav"]).pct_change().dropna()
wts_returns = pd.Series(df_nav["weak_to_strong_nav"]).pct_change().dropna()

if len(fb_returns) > 0 and len(wts_returns) > 0:
    correlation = fb_returns.corr(wts_returns)
    print(f"\n首板低开 vs 弱转强竞价 相关性: {correlation:.4f}")

# 最终结论
print("\n" + "=" * 60)
print("最终结论")
print("=" * 60)

best_single = max([fb_metrics, wts_metrics], key=lambda x: x["calmar"])
best_single_name = "首板低开" if best_single == fb_metrics else "弱转强竞价"

print(f"\n1. 最强单策略: {best_single_name}")
print(f"   卡玛比率: {best_single['calmar']:.2f}")

print(f"\n2. 等权组合 vs 单策略:")
print(f"   组合卡玛: {eq_metrics['calmar']:.2f} vs 单策略: {best_single['calmar']:.2f}")
if eq_metrics["calmar"] > best_single["calmar"]:
    print("   结论: 组合优于单策略")
else:
    print("   结论: 组合不如单策略")

print(f"\n3. 风险平价组合 vs 单策略:")
print(f"   组合卡玛: {rp_metrics['calmar']:.2f} vs 单策略: {best_single['calmar']:.2f}")
if rp_metrics["calmar"] > best_single["calmar"]:
    print("   结论: 组合优于单策略")
else:
    print("   结论: 组合不如单策略")

print("\n4. Go/Watch/No-Go:")
if (
    eq_metrics["calmar"] > best_single["calmar"]
    or rp_metrics["calmar"] > best_single["calmar"]
):
    print("   **Go** - 组合有效")
else:
    print("   **No-Go** - 暂不做组合，先做单策略")

print("\n" + "=" * 60)
print("回测完成")
print("=" * 60)
