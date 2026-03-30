#!/usr/bin/env python3
"""
RFScore PB10 策略对比 - Notebook 版本

在 JoinQuant Notebook 中运行，无时间限制
手动模拟回测流程

参数：
- 时间范围：2021-01-01 至 2025-03-28
- 初始资金：100000
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")

print("=" * 70)
print("RFScore PB10 策略对比 - Notebook 版本")
print("=" * 70)
print(f"回测时间：2021-01-01 至 2025-03-28")
print(f"初始资金：100000")
print("=" * 70)

# ============================================================================
# 1. 定义 RFScore 因子
# ============================================================================


def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))


class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa",
        "roa_4",
        "net_operate_cash_flow",
        "net_operate_cash_flow_1",
        "net_operate_cash_flow_2",
        "net_operate_cash_flow_3",
        "total_assets",
        "total_assets_1",
        "total_assets_2",
        "total_assets_3",
        "total_assets_4",
        "total_assets_5",
        "total_non_current_liability",
        "total_non_current_liability_1",
        "gross_profit_margin",
        "gross_profit_margin_4",
        "operating_revenue",
        "operating_revenue_4",
    ]

    def calc(self, data):
        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1

        cfo_sum = (
            data["net_operate_cash_flow"]
            + data["net_operate_cash_flow_1"]
            + data["net_operate_cash_flow_2"]
            + data["net_operate_cash_flow_3"]
        )
        ta_ttm = (
            data["total_assets"]
            + data["total_assets_1"]
            + data["total_assets_2"]
            + data["total_assets_3"]
        ) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - roa * 0.01

        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)

        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1

        turnover = (
            data["operating_revenue"]
            / (data["total_assets"] + data["total_assets_1"]).mean()
        )
        turnover_1 = (
            data["operating_revenue_4"]
            / (data["total_assets_4"] + data["total_assets_5"]).mean()
        )
        delta_turn = turnover / turnover_1 - 1

        indicator_tuple = (
            roa,
            delta_roa,
            ocfoa,
            accrual,
            delta_leveler,
            delta_margin,
            delta_turn,
        )
        self.basic = pd.concat(indicator_tuple).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = [
            "ROA",
            "DELTA_ROA",
            "OCFOA",
            "ACCRUAL",
            "DELTA_LEVELER",
            "DELTA_MARGIN",
            "DELTA_TURN",
        ]
        self.fscore = self.basic.apply(sign).sum(axis=1)


# ============================================================================
# 2. 原始策略逻辑（简化版）
# ============================================================================


class OriginalStrategy:
    """原始策略 - 基于 breadth 和 trend 择时"""

    def __init__(self):
        self.ipo_days = 180
        self.base_hold_num = 20
        self.reduced_hold_num = 10
        self.breadth_reduce = 0.25
        self.breadth_stop = 0.15
        self.primary_pb_group = 1
        self.reduced_pb_group = 2

    def get_universe(self, watch_date):
        """获取股票池"""
        hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
        zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
        stocks = list(hs300 | zz500)
        stocks = [s for s in stocks if not s.startswith("688")]

        sec = get_all_securities(types=["stock"], date=watch_date)
        sec = sec.loc[sec.index.intersection(stocks)]
        sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=self.ipo_days)]
        stocks = sec.index.tolist()

        is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()

        paused = get_price(
            stocks, end_date=watch_date, count=1, fields="paused", panel=False
        )
        paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
        stocks = paused[paused == 0].index.tolist()

        return stocks

    def calc_market_state(self, watch_date):
        """计算市场状态"""
        hs300 = get_index_stocks("000300.XSHG", date=watch_date)
        prices = get_price(
            hs300, end_date=watch_date, count=20, fields=["close"], panel=False
        )
        close = prices.pivot(index="time", columns="code", values="close")
        breadth = float((close.iloc[-1] > close.mean()).mean())

        idx = get_price("000300.XSHG", end_date=watch_date, count=20, fields=["close"])
        idx_close = float(idx["close"].iloc[-1])
        idx_ma20 = float(idx["close"].mean())
        trend_on = idx_close > idx_ma20

        return {"breadth": breadth, "trend_on": trend_on}

    def calc_rfscore_table(self, stocks, watch_date):
        """计算因子表"""
        factor = RFScore()
        calc_factors(stocks, [factor], start_date=watch_date, end_date=watch_date)

        df = factor.basic.copy()
        df["RFScore"] = factor.fscore

        val = get_valuation(
            stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1
        )
        val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
        df = df.join(val, how="left")

        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna(subset=["RFScore", "pb_ratio"])
        df["pb_group"] = (
            pd.qcut(
                df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
            )
            + 1
        )

        return df

    def choose_stocks(self, watch_date, hold_num):
        """选股"""
        stocks = self.get_universe(watch_date)
        df = self.calc_rfscore_table(stocks, str(watch_date))

        primary = df[
            (df["RFScore"] == 7) & (df["pb_group"] <= self.primary_pb_group)
        ].copy()
        primary = primary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        picks = primary.index.tolist()

        if len(picks) < hold_num:
            secondary = df[
                (df["RFScore"] >= 6) & (df["pb_group"] <= self.reduced_pb_group)
            ].copy()
            secondary = secondary.sort_values(
                ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
                ascending=[False, False, False, False, False, True],
            )
            for code in secondary.index.tolist():
                if code not in picks:
                    picks.append(code)
                if len(picks) >= hold_num:
                    break

        return picks[:hold_num], df

    def should_trade(self, watch_date):
        """判断是否应该交易"""
        state = self.calc_market_state(watch_date)

        if state["breadth"] < self.breadth_stop and not state["trend_on"]:
            return 0, state  # 清仓
        elif state["breadth"] < self.breadth_reduce and not state["trend_on"]:
            return self.reduced_hold_num, state  # 减仓
        else:
            return self.base_hold_num, state  # 正常持仓


# ============================================================================
# 3. 增强策略逻辑（简化版）
# ============================================================================


class EnhancedStrategy:
    """增强策略 - 添加情绪开关和风控"""

    def __init__(self):
        self.ipo_days = 180
        self.primary_pb_group = 1
        self.reduced_pb_group = 2

        # 四档仓位
        self.base_hold_num = 15
        self.defensive_hold_num = 12
        self.bottom_hold_num = 10
        self.extreme_hold_num = 0

        self.breadth_defensive = 0.40
        self.breadth_bottom = 0.25
        self.breadth_extreme = 0.15

    def calc_sentiment(self, date):
        """计算情绪指标"""
        try:
            all_stocks = get_all_securities("stock", date=date).index.tolist()
            all_stocks = [
                s for s in all_stocks if s[0] != "4" and s[0] != "8" and s[:2] != "68"
            ]

            sample = all_stocks[:500]
            df = get_price(
                sample,
                end_date=date,
                count=1,
                fields=["close", "high_limit", "low_limit"],
                panel=False,
            )
            df = df.dropna()

            hl_count = len(df[df["close"] == df["high_limit"]])
            ll_count = len(df[df["close"] == df["low_limit"]])

            score = 50

            if hl_count > 80:
                score += 20
            elif hl_count > 50:
                score += 10
            elif hl_count > 30:
                score += 5
            elif hl_count < 15:
                score -= 15
            elif hl_count < 25:
                score -= 5

            ratio = hl_count / max(ll_count, 1)
            if ratio > 5:
                score += 15
            elif ratio > 2:
                score += 5
            elif ratio < 0.5:
                score -= 15
            elif ratio < 1:
                score -= 5

            sentiment_score = max(0, min(100, score))

            if score >= 75:
                sentiment_state = 4
            elif score >= 60:
                sentiment_state = 3
            elif score >= 45:
                sentiment_state = 2
            elif score >= 30:
                sentiment_state = 1
            else:
                sentiment_state = 0

            return {
                "hl_count": hl_count,
                "ll_count": ll_count,
                "sentiment_score": sentiment_score,
                "sentiment_state": sentiment_state,
            }
        except:
            return {"hl_count": 0, "sentiment_score": 50, "sentiment_state": 2}

    def calc_breadth_trend(self, date):
        """计算广度和趋势"""
        hs300 = get_index_stocks("000300.XSHG", date=date)
        prices = get_price(
            hs300, end_date=date, count=20, fields=["close"], panel=False
        )
        close = prices.pivot(index="time", columns="code", values="close")
        breadth = float((close.iloc[-1] > close.mean()).mean())

        idx = get_price("000300.XSHG", end_date=date, count=20, fields=["close"])
        idx_close = float(idx["close"].iloc[-1])
        idx_ma20 = float(idx["close"].mean())
        trend_on = idx_close > idx_ma20

        return breadth, trend_on

    def get_target_hold_num(self, date):
        """获取目标持仓数"""
        breadth, trend_on = self.calc_breadth_trend(date)

        if breadth < self.breadth_extreme:
            return self.extreme_hold_num, breadth, trend_on
        elif breadth < self.breadth_bottom:
            return self.bottom_hold_num, breadth, trend_on
        elif breadth < self.breadth_defensive and not trend_on:
            return self.defensive_hold_num, breadth, trend_on
        else:
            return self.base_hold_num, breadth, trend_on

    def get_position_ratio(self, sentiment_state):
        """获取仓位比例"""
        ratios = {4: 1.0, 3: 0.8, 2: 0.6, 1: 0.3, 0: 0.0}
        return ratios.get(sentiment_state, 0.6)

    def get_universe(self, watch_date):
        """获取股票池（同原始策略）"""
        hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
        zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
        stocks = list(hs300 | zz500)
        stocks = [s for s in stocks if not s.startswith("688")]

        sec = get_all_securities(types=["stock"], date=watch_date)
        sec = sec.loc[sec.index.intersection(stocks)]
        sec = sec[sec["start_date"] <= watch_date - pd.Timedelta(days=self.ipo_days)]
        stocks = sec.index.tolist()

        is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()

        paused = get_price(
            stocks, end_date=watch_date, count=1, fields="paused", panel=False
        )
        paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
        stocks = paused[paused == 0].index.tolist()

        return stocks

    def calc_rfscore_table(self, stocks, watch_date):
        """计算因子表（同原始策略）"""
        factor = RFScore()
        calc_factors(stocks, [factor], start_date=watch_date, end_date=watch_date)

        df = factor.basic.copy()
        df["RFScore"] = factor.fscore

        val = get_valuation(
            stocks, end_date=watch_date, fields=["pb_ratio", "pe_ratio"], count=1
        )
        val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
        df = df.join(val, how="left")

        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna(subset=["RFScore", "pb_ratio"])
        df["pb_group"] = (
            pd.qcut(
                df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
            )
            + 1
        )

        return df

    def choose_stocks(self, watch_date, hold_num):
        """选股"""
        stocks = self.get_universe(watch_date)
        if len(stocks) < 10:
            return [], pd.DataFrame()

        df = self.calc_rfscore_table(stocks, str(watch_date))

        primary = df[
            (df["RFScore"] == 7) & (df["pb_group"] <= self.primary_pb_group)
        ].copy()
        primary = primary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        picks = primary.index.tolist()

        if len(picks) < hold_num:
            secondary = df[
                (df["RFScore"] >= 6) & (df["pb_group"] <= self.reduced_pb_group)
            ].copy()
            secondary = secondary.sort_values(
                ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
                ascending=[False, False, False, False, False, True],
            )
            for code in secondary.index.tolist():
                if code not in picks:
                    picks.append(code)
                if len(picks) >= hold_num:
                    break

        return picks[:hold_num], df

    def should_trade(self, watch_date):
        """判断是否应该交易"""
        # 四档仓位
        base_hold_num, breadth, trend_on = self.get_target_hold_num(watch_date)

        # 情绪开关
        sentiment = self.calc_sentiment(watch_date)
        sentiment_ratio = self.get_position_ratio(sentiment["sentiment_state"])

        # 综合仓位
        adjusted_hold_num = int(base_hold_num * sentiment_ratio)

        return adjusted_hold_num, {
            "breadth": breadth,
            "trend_on": trend_on,
            "sentiment": sentiment,
        }


# ============================================================================
# 4. 回测引擎
# ============================================================================


class BacktestEngine:
    """手动回测引擎"""

    def __init__(self, strategy, start_date, end_date, initial_capital=100000):
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital

        self.cash = initial_capital
        self.positions = {}  # {stock: {'amount': x, 'cost': y}}
        self.daily_values = []

def run(self):
        """运行回测"""
        trade_days = get_trade_days(self.start_date, self.end_date)
        # 转换为字符串格式
        trade_days = [str(d) if hasattr(d, 'strftime') else d for d in trade_days]
        total_days = len(trade_days)
        
        print(f"\n回测天数：{total_days}")
        print(f"开始日期：{trade_days[0]}")
        print(f"结束日期：{trade_days[-1]}")
        
        # 每月调仓（简化：每月第一个交易日）
        monthly_dates = []
        for i, date in enumerate(trade_days):
            date_str = str(date) if hasattr(date, 'strftime') else date
            prev_date_str = str(trade_days[i-1]) if i > 0 and hasattr(trade_days[i-1], 'strftime') else (trade_days[i-1] if i > 0 else "")
            if i == 0 or date_str[:7] != prev_date_str[:7]:
                monthly_dates.append(date_str)

        print(f"调仓日期数：{len(monthly_dates)}")

        for i, date in enumerate(trade_days):
            # 计算当日资产价值
            total_value = self.cash

            for stock, pos in self.positions.items():
                try:
                    price_df = get_price(
                        stock, end_date=date, count=1, fields=["close"], panel=False
                    )
                    if price_df.empty:
                        continue
                    price = float(price_df["close"].iloc[-1])
                    total_value += pos["amount"] * price
                except:
                    pass

            self.daily_values.append(
                {
                    "date": date,
                    "cash": self.cash,
                    "positions": len(self.positions),
                    "total_value": total_value,
                    "return": (total_value - self.initial_capital)
                    / self.initial_capital
                    * 100,
                }
            )

            # 调仓日
            if date in monthly_dates:
                self.rebalance(date)

            if i % 100 == 0:
                print(
                    f"进度：{i + 1}/{total_days}, 持仓数：{len(self.positions)}, 总价值：{total_value:.0f}"
                )

        return self.daily_values

def rebalance(self, date):
        """调仓"""
        date_str = str(date) if hasattr(date, 'strftime') else date
        try:
            hold_num, state = self.strategy.should_trade(date_str)
            
            if hold_num == 0:
                # 清仓
                for stock in list(self.positions.keys()):
                    try:
                        price_df = get_price(stock, end_date=date_str, count=1, fields=["close"], panel=False)
                        if not price_df.empty:
                            price = float(price_df["close"].iloc[-1])
                            self.cash += self.positions[stock]["amount"] * price
                            del self.positions[stock]
                    except:
                        pass
                return
            
            # 选股
            target_stocks, _ = self.strategy.choose_stocks(date_str, hold_num)

            if len(target_stocks) == 0:
                return

            # 清仓不在目标池的股票
            for stock in list(self.positions.keys()):
                if stock not in target_stocks:
                    try:
                        price_df = get_price(
                            stock, end_date=date, count=1, fields=["close"], panel=False
                        )
                        if not price_df.empty:
                            price = float(price_df["close"].iloc[-1])
                            self.cash += self.positions[stock]["amount"] * price
                            del self.positions[stock]
                    except:
                        pass

            # 计算当前总价值
            total_value = self.cash
            for stock, pos in self.positions.items():
                try:
                    price_df = get_price(
                        stock, end_date=date, count=1, fields=["close"], panel=False
                    )
                    if not price_df.empty:
                        price = float(price_df["close"].iloc[-1])
                        total_value += pos["amount"] * price
                except:
                    pass

            # 分配资金
            target_value_per_stock = total_value / len(target_stocks)

            # 买入目标股票
            for stock in target_stocks:
                try:
                    price_df = get_price(
                        stock, end_date=date, count=1, fields=["close"], panel=False
                    )
                    if price_df.empty:
                        continue

                    price = float(price_df["close"].iloc[-1])

                    # 如果已持仓，先检查是否需要调整
                    if stock in self.positions:
                        current_value = self.positions[stock]["amount"] * price
                        if (
                            abs(current_value - target_value_per_stock)
                            < target_value_per_stock * 0.1
                        ):
                            continue  # 差异小于10%，不调整

                        # 卖出多余部分
                        self.cash += self.positions[stock]["amount"] * price
                        del self.positions[stock]

                    # 买入
                    amount = int(target_value_per_stock / price / 100) * 100
                    if amount >= 100 and self.cash >= amount * price:
                        self.cash -= amount * price
                        self.positions[stock] = {"amount": amount, "cost": price}

                except Exception as e:
                    continue

        except Exception as e:
            print(f"调仓失败 {date_str}: {e}")

    def summary(self):
        """回测摘要"""
        if len(self.daily_values) == 0:
            return None

        df = pd.DataFrame(self.daily_values)

        # 总收益
        total_return = df["return"].iloc[-1]

        # 年化收益
        years = len(df) / 252
        annual_return = (
            (df["total_value"].iloc[-1] / self.initial_capital - 1) / years * 100
        )

        # 最大回撤
        peak = df["total_value"].expanding(min_periods=1).max()
        drawdown = (df["total_value"] - peak) / peak
        max_drawdown = drawdown.min() * 100

        # 夏普比率（简化）
        daily_returns = df["total_value"].pct_change().dropna()
        if daily_returns.std() > 0:
            sharpe = daily_returns.mean() / daily_returns.std() * np.sqrt(252)
        else:
            sharpe = 0

# 胜率（每日收益>0的比例）
        win_days = len(daily_returns[daily_returns > 0])
        total_trade_days = len(daily_returns)
        win_rate = win_days / total_trade_days * 100
        
        # 计算调仓次数
        trade_count = 0
        prev_month = None
        for d in df["date"]:
            d_str = str(d)
            month = d_str[:7]
            if prev_month and month != prev_month:
                trade_count += 1
            prev_month = month
        
        return {
            "total_return": total_return,
            "annual_return": annual_return,
            "max_drawdown": max_drawdown,
            "sharpe": sharpe,
            "win_rate": win_rate,
            "trade_count": trade_count,
            "final_value": df["total_value"].iloc[-1],
            "daily_values": df
        }


# ============================================================================
# 5. 运行对比
# ============================================================================

print("\n开始运行原始策略...")
original_strategy = OriginalStrategy()
original_engine = BacktestEngine(original_strategy, "2021-01-01", "2025-03-28", 100000)
original_values = original_engine.run()
original_summary = original_engine.summary()

print("\n原始策略结果：")
if original_summary:
    print(f"  总收益：{original_summary['total_return']:.2f}%")
    print(f"  年化收益：{original_summary['annual_return']:.2f}%")
    print(f"  最大回撤：{original_summary['max_drawdown']:.2f}%")
    print(f"  夏普比率：{original_summary['sharpe']:.2f}")
    print(f"  胜率：{original_summary['win_rate']:.1f}%")
else:
    print("  无有效结果")

print("\n开始运行增强策略...")
enhanced_strategy = EnhancedStrategy()
enhanced_engine = BacktestEngine(enhanced_strategy, "2021-01-01", "2025-03-28", 100000)
enhanced_values = enhanced_engine.run()
enhanced_summary = enhanced_engine.summary()

print("\n增强策略结果：")
if enhanced_summary:
    print(f"  总收益：{enhanced_summary['total_return']:.2f}%")
    print(f"  年化收益：{enhanced_summary['annual_return']:.2f}%")
    print(f"  最大回撤：{enhanced_summary['max_drawdown']:.2f}%")
    print(f"  夏普比率：{enhanced_summary['sharpe']:.2f}")
    print(f"  胜率：{enhanced_summary['win_rate']:.1f}%")
else:
    print("  无有效结果")

# ============================================================================
# 6. 对比分析
# ============================================================================

print("\n" + "=" * 70)
print("策略对比")
print("=" * 70)

if original_summary and enhanced_summary:
    print(f"\n{'指标':<15} {'原始策略':<20} {'增强策略':<20} {'差异':<15}")
    print("-" * 70)

    metrics = [
        ("总收益", original_summary["total_return"], enhanced_summary["total_return"]),
        (
            "年化收益",
            original_summary["annual_return"],
            enhanced_summary["annual_return"],
        ),
        (
            "最大回撤",
            original_summary["max_drawdown"],
            enhanced_summary["max_drawdown"],
        ),
        ("夏普比率", original_summary["sharpe"], enhanced_summary["sharpe"]),
        ("胜率", original_summary["win_rate"], enhanced_summary["win_rate"]),
    ]

    for name, orig, enh in metrics:
        diff = enh - orig
        print(f"{name:<15} {orig:.2f}%{'':<12} {enh:.2f}%{'':<12} {diff:.2f}%")

    print("\n结论：")
    if enhanced_summary["annual_return"] > original_summary["annual_return"]:
        print("  ✓ 增强策略年化收益更高")
    if enhanced_summary["max_drawdown"] < original_summary["max_drawdown"]:
        print("  ✓ 增强策略回撤更小")
    if enhanced_summary["sharpe"] > original_summary["sharpe"]:
        print("  ✓ 增强策略夏普比率更高")

# ============================================================================
# 7. 保存结果
# ============================================================================

print("\n保存结果...")

result_data = {
    "original": original_summary if original_summary else {},
    "enhanced": enhanced_summary if enhanced_summary else {},
}

import json

result_file = "/Users/fengzhi/Downloads/git/testlixingren/strategies/enhanced/notebook_comparison_result.json"
with open(result_file, "w") as f:
    json.dump(result_data, f, indent=2)

print(f"结果已保存到：{result_file}")

print("\n" + "=" * 70)
print("完成！")
print("=" * 70)
