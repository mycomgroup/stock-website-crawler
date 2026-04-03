#!/usr/bin/env python3
"""
RFScore v2.0 完整模拟回测 - Notebook格式
手动实现回测循环，测试2024-01至2024-12完整一年
"""

from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy.stats import linregress

print("=" * 80)
print("RFScore v2.0 完整模拟回测")
print("回测区间: 2024-01-01 至 2024-12-31")
print("初始资金: 1,000,000")
print("=" * 80)

# ============================================================================
# RFScore因子定义
# ============================================================================


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

        def sign(ser):
            return ser.apply(lambda x: np.where(x > 0, 1, 0))

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
# 辅助函数
# ============================================================================


def get_universe(watch_date):
    hs300 = set(get_index_stocks("000300.XSHG", date=watch_date))
    zz500 = set(get_index_stocks("000905.XSHG", date=watch_date))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]
    sec = get_all_securities(types=["stock"], date=watch_date)
    sec = sec.loc[sec.index.intersection(stocks)]
    cutoff = (pd.Timestamp(watch_date) - pd.Timedelta(days=180)).date()
    sec = sec[sec["start_date"].apply(lambda x: x <= cutoff)]
    stocks = sec.index.tolist()
    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()
    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()
    return stocks


def calc_rfscore_table(stocks, watch_date):
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


def choose_stocks(watch_date, hold_num):
    stocks = get_universe(watch_date)
    df = calc_rfscore_table(stocks[:500], str(watch_date))
    primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= 1)].copy()
    primary = primary.sort_values(
        ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
        ascending=[False, False, False, False, False, True],
    )
    picks = primary.index.tolist()
    if len(picks) < hold_num:
        secondary = df[(df["RFScore"] >= 6) & (df["pb_group"] <= 2)].copy()
        secondary = secondary.sort_values(
            ["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
            ascending=[False, False, False, False, False, True],
        )
        for code in secondary.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
    if len(picks) < hold_num:
        fallback = df.sort_values(
            ["RFScore", "ROA", "OCFOA", "pb_ratio"],
            ascending=[False, False, False, True],
        )
        for code in fallback.index.tolist():
            if code not in picks:
                picks.append(code)
            if len(picks) >= hold_num:
                break
    return picks[:hold_num]


def calc_breadth(watch_date):
    try:
        hs300 = get_index_stocks("000300.XSHG", date=watch_date)
        prices = get_price(
            hs300, end_date=watch_date, count=20, fields=["close"], panel=False
        )
        close = prices.pivot(index="time", columns="code", values="close")
        return float((close.iloc[-1] > close.mean()).mean())
    except:
        return 0.5


def calc_rsrs(watch_date, slope_series):
    try:
        prices = get_price(
            "000300.XSHG",
            end_date=watch_date,
            fields=["high", "low"],
            count=18,
            panel=False,
        )
        high = prices["high"].values
        low = prices["low"].values
        if len(high) < 18:
            return "NEUTRAL", 0.0
        slope, intercept, r_value, _, _ = linregress(low, high)
        r2 = r_value**2
        slope_series.append(slope)
        if len(slope_series) > 600:
            slope_series.pop(0)
        if len(slope_series) < 50:
            return "NEUTRAL", 0.0
        mean = np.mean(slope_series)
        std = np.std(slope_series)
        zscore = (slope - mean) / std
        rsrs = zscore * slope * r2
        if rsrs > 0.7:
            return "BULLISH", rsrs
        elif rsrs < -0.7:
            return "BEARISH", rsrs
        return "NEUTRAL", rsrs
    except:
        return "NEUTRAL", 0.0


# ============================================================================
# 回测主循环
# ============================================================================

print("\n【步骤1】获取月度调仓日期")
print("-" * 60)

start_date = "2024-01-01"
end_date = "2024-12-31"

trade_days = get_trade_days(start_date, end_date)
monthly_dates = []
current_month = None
for day in trade_days:
    if current_month != day.month:
        monthly_dates.append(day)
        current_month = day.month

print(f"  调仓次数: {len(monthly_dates)}")
print(f"  调仓日期: {[str(d) for d in monthly_dates]}")

print("\n【步骤2】执行回测")
print("-" * 60)

initial_capital = 1000000
capital = initial_capital
positions = {}  # stock -> (amount, cost_price)
slope_series = []
monthly_returns = []
monthly_states = []

for i, rebal_date in enumerate(monthly_dates):
    print(f"\n[{i + 1}/{len(monthly_dates)}] 调仓日期: {rebal_date}")

    # 计算上月收益（如果有持仓）
    if positions and i > 0:
        prev_rebal = monthly_dates[i - 1]
        # 计算从上次调仓到本次调仓的收益
        stock_list = list(positions.keys())
        try:
            prices_start = get_price(
                stock_list,
                end_date=str(prev_rebal),
                count=1,
                fields=["close"],
                panel=False,
            )
            prices_end = get_price(
                stock_list,
                end_date=str(rebal_date),
                count=1,
                fields=["close"],
                panel=False,
            )

            if len(prices_start) > 0 and len(prices_end) > 0:
                p_start = prices_start.pivot(
                    index="time", columns="code", values="close"
                ).iloc[-1]
                p_end = prices_end.pivot(
                    index="time", columns="code", values="close"
                ).iloc[-1]

                total_value = 0
                for stock, (amount, cost) in positions.items():
                    if stock in p_end.index:
                        total_value += amount * p_end[stock]

                month_return = (total_value - capital) / capital if capital > 0 else 0
                monthly_returns.append(month_return)
                capital = total_value
                print(f"  上月收益: {month_return:.2%} | 当前资金: {capital:,.0f}")
        except Exception as e:
            print(f"  计算收益出错: {e}")

    # 计算市场状态
    breadth = calc_breadth(rebal_date)
    rsrs_signal, rsrs_value = calc_rsrs(rebal_date, slope_series)

    # 仓位决策
    if breadth < 0.15:
        position_ratio, target_hold = 0.0, 0
    elif breadth < 0.25:
        position_ratio, target_hold = 0.5, 10
    elif breadth < 0.35:
        position_ratio, target_hold = 0.75, 15
    else:
        position_ratio, target_hold = 1.0, 20

    if rsrs_signal == "BEARISH":
        position_ratio *= 0.7
        target_hold = max(int(target_hold * 0.7), 5)
    elif rsrs_signal == "BULLISH":
        position_ratio = min(position_ratio * 1.1, 1.0)

    target_hold = max(target_hold, 5) if position_ratio > 0 else 0

    monthly_states.append(
        {
            "date": str(rebal_date),
            "breadth": breadth,
            "rsrs_signal": rsrs_signal,
            "rsrs_value": rsrs_value,
            "position_ratio": position_ratio,
            "target_hold": target_hold,
        }
    )

    print(f"  市场宽度: {breadth:.1%}")
    print(f"  RSRS信号: {rsrs_signal} (值: {rsrs_value:.2f})")
    print(f"  建议仓位: {position_ratio:.0%} | 目标持仓: {target_hold}只")

    # 选股
    if target_hold > 0:
        try:
            target_stocks = choose_stocks(rebal_date, target_hold)
            print(f"  实际选出: {len(target_stocks)}只")
            if target_stocks:
                print(f"  前3只: {target_stocks[:3]}")
        except Exception as e:
            print(f"  选股出错: {e}")
            target_stocks = []
    else:
        target_stocks = []
        print(f"  空仓")

    # 模拟调仓
    if target_stocks:
        invest_amount = capital * position_ratio
        per_stock = invest_amount / len(target_stocks)

        # 清仓不在目标中的股票
        for stock in list(positions.keys()):
            if stock not in target_stocks:
                del positions[stock]

        # 买入目标股票
        positions = {}
        for stock in target_stocks:
            try:
                price_data = get_price(
                    stock,
                    end_date=str(rebal_date),
                    count=1,
                    fields=["close"],
                    panel=False,
                )
                if len(price_data) > 0:
                    price = price_data["close"].iloc[-1]
                    if price > 0:
                        amount = int(per_stock / price / 100) * 100
                        if amount >= 100:
                            positions[stock] = (amount, price)
            except:
                pass

        print(f"  投入资金: {invest_amount:,.0f} | 持仓: {len(positions)}只")

print("\n" + "=" * 80)
print("【回测结果汇总】")
print("=" * 80)

# 计算最终价值
if positions:
    last_date = monthly_dates[-1]
    stock_list = list(positions.keys())
    try:
        prices_end = get_price(
            stock_list, end_date="2024-12-31", count=1, fields=["close"], panel=False
        )
        p_end = prices_end.pivot(index="time", columns="code", values="close").iloc[-1]

        final_value = 0
        for stock, (amount, cost) in positions.items():
            if stock in p_end.index:
                final_value += amount * p_end[stock]
            else:
                final_value += amount * cost

        total_return = (final_value - initial_capital) / initial_capital
    except:
        final_value = capital
        total_return = (final_value - initial_capital) / initial_capital
else:
    final_value = capital
    total_return = (final_value - initial_capital) / initial_capital

print(f"\n  初始资金: {initial_capital:,.0f}")
print(f"  最终资金: {final_value:,.0f}")
print(f"  总收益率: {total_return:.2%}")
print(f"  调仓次数: {len(monthly_dates)}")

if monthly_returns:
    monthly_returns_arr = np.array(monthly_returns)
    print(f"\n  月度收益统计:")
    print(f"    平均月收益: {monthly_returns_arr.mean():.2%}")
    print(f"    月收益标准差: {monthly_returns_arr.std():.2%}")
    print(
        f"    月胜率: {(monthly_returns_arr > 0).sum()}/{len(monthly_returns_arr)} = {(monthly_returns_arr > 0).mean():.0%}"
    )
    print(f"    最大月收益: {monthly_returns_arr.max():.2%}")
    print(f"    最大月亏损: {monthly_returns_arr.min():.2%}")

    # 年化收益
    annual_return = (1 + total_return) ** (12 / len(monthly_returns)) - 1
    # 年化波动
    annual_vol = monthly_returns_arr.std() * np.sqrt(12)
    # 夏普比率
    sharpe = annual_return / annual_vol if annual_vol > 0 else 0
    # 最大回撤
    cumulative = np.cumprod(1 + monthly_returns_arr)
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    print(f"\n  年化指标:")
    print(f"    年化收益: {annual_return:.2%}")
    print(f"    年化波动: {annual_vol:.2%}")
    print(f"    夏普比率: {sharpe:.2f}")
    print(f"    最大回撤: {max_drawdown:.2%}")

print("\n【月度状态记录】")
print("-" * 60)
print(f"  {'日期':<15} {'宽度':>8} {'RSRS':>10} {'仓位':>8} {'持仓':>6}")
print(f"  {'-' * 15} {'-' * 8} {'-' * 10} {'-' * 8} {'-' * 6}")
for state in monthly_states:
    print(
        f"  {state['date']:<15} {state['breadth']:>7.1%} {state['rsrs_signal']:>10} {state['position_ratio']:>7.0%} {state['target_hold']:>4}只"
    )

print("\n" + "=" * 80)
print("回测完成!")
print("=" * 80)
