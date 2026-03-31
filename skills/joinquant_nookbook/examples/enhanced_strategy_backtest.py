#!/usr/bin/env python3
"""
增强策略 Notebook 回测
对比原始策略 vs 增强策略（情绪开关 + 四档仓位 + 风控）
"""

from jqdata import *
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

print("=" * 70)
print("增强策略 Notebook 回测")
print("回测时间：2021-01-01 至 2025-03-28")
print("初始资金：100000")
print("=" * 70)

# 参数设置
START_DATE = "2021-01-01"
END_DATE = "2025-03-28"
INITIAL_CAPITAL = 100000
IPO_DAYS = 180


def get_trade_months(start_date, end_date):
    """获取交易日列表（每月第一个交易日）"""
    all_days = get_trade_days(start_date, end_date)
    months = {}
    for d in all_days:
        month_key = d[:7]
        if month_key not in months:
            months[month_key] = d
    return sorted(months.values())


def get_stock_universe(date_str):
    """获取股票池：沪深300 + 中证500"""
    hs300 = set(get_index_stocks("000300.XSHG", date=date_str))
    zz500 = set(get_index_stocks("000905.XSHG", date=date_str))
    stocks = list(hs300 | zz500)
    stocks = [s for s in stocks if not s.startswith("688")]

    # 过滤新股
    threshold = (
        datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=IPO_DAYS)
    ).strftime("%Y-%m-%d")
    sec = get_all_securities(types=["stock"], date=date_str)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= threshold]
    stocks = sec.index.tolist()

    # 过滤 ST
    is_st = get_extras("is_st", stocks, end_date=date_str, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    return stocks


def select_stocks_base(date_str, hold_num=20):
    """基础选股：ROA > 0 + PB 最低 10%"""
    stocks = get_stock_universe(date_str)
    if len(stocks) < 10:
        return []

    # 获取基本面数据
    q = query(valuation.code, valuation.pb_ratio, indicator.roa).filter(
        valuation.code.in_(stocks)
    )

    df = get_fundamentals(q, date=date_str)
    df = df.dropna()
    df = df[df["roa"] > 0]

    if len(df) == 0:
        return []

    # PB 分组
    df["pb_group"] = (
        pd.qcut(
            df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop"
        )
        + 1
    )

    # 选择 PB 最低 10% 且 ROA > 0
    selected = df[df["pb_group"] <= 1].sort_values("roa", ascending=False)

    return selected["code"].tolist()[:hold_num]


def calc_breadth(date_str):
    """计算市场广度：沪深300 站上 MA20 的比例"""
    hs300 = get_index_stocks("000300.XSHG", date=date_str)

    above_ma20 = 0
    total = 0

    for stock in hs300[:100]:  # 采样前100只
        try:
            prices = get_price(
                stock, end_date=date_str, count=20, fields="close", panel=False
            )
            if len(prices) < 20:
                continue
            ma20 = prices["close"].mean()
            close = prices["close"].iloc[-1]
            if close > ma20:
                above_ma20 += 1
            total += 1
        except:
            continue

    return above_ma20 / max(total, 1)


def calc_sentiment(date_str):
    """计算情绪指标：涨停数"""
    all_stocks = get_all_securities("stock", date=date_str).index.tolist()
    sample = [
        s for s in all_stocks if s[0] not in ["4", "8"] and not s.startswith("68")
    ][:500]

    try:
        df = get_price(
            sample,
            end_date=date_str,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
        )
        df = df.dropna()
        hl_count = len(df[df["close"] >= df["high_limit"] * 0.995])
        return hl_count
    except:
        return 0


def select_stocks_enhanced(date_str, hold_num=15):
    """增强选股：加入广度和情绪判断"""
    breadth = calc_breadth(date_str)
    sentiment = calc_sentiment(date_str)

    # 四档仓位
    if breadth < 0.15:
        actual_hold = 0
        reason = "清仓（极端）"
    elif breadth < 0.25:
        actual_hold = 10
        reason = "底部"
    elif breadth < 0.40 and sentiment < 20:
        actual_hold = 8
        reason = "减仓（情绪弱）"
    else:
        actual_hold = hold_num
        reason = "正常"

    if actual_hold == 0:
        return [], breadth, sentiment, reason

    stocks = select_stocks_base(date_str, actual_hold)
    return stocks, breadth, sentiment, reason


def calc_monthly_return(stocks, start_date, next_date):
    """计算月度收益"""
    if not stocks:
        return 0.0

    returns = []
    for stock in stocks:
        try:
            p1 = get_price(
                stock, end_date=start_date, count=1, fields="close", panel=False
            )
            p2 = get_price(
                stock, end_date=next_date, count=1, fields="close", panel=False
            )
            if not p1.empty and not p2.empty:
                ret = (
                    float(p2["close"].iloc[-1]) - float(p1["close"].iloc[-1])
                ) / float(p1["close"].iloc[-1])
                returns.append(ret)
        except:
            continue

    return np.mean(returns) if returns else 0.0


# 主回测
trade_months = get_trade_months(START_DATE, END_DATE)
print(f"\n测试月份数: {len(trade_months)}")

# 原始策略结果
print("\n" + "=" * 70)
print("原始策略回测")
print("=" * 70)

base_returns = []
base_trades = 0

for i, month_start in enumerate(trade_months):
    month_end = trade_months[i + 1] if i + 1 < len(trade_months) else END_DATE

    stocks = select_stocks_base(month_start, 20)
    if stocks:
        ret = calc_monthly_return(stocks, month_start, month_end)
        base_returns.append(ret)
        base_trades += 1

        print(f"[{i + 1}/{len(trade_months)}] {month_start}")
        print(f"  选中: {len(stocks)} 只, 收益: {ret * 100:.2f}%")

# 增强策略结果
print("\n" + "=" * 70)
print("增强策略回测")
print("=" * 70)

enhanced_returns = []
enhanced_trades = 0
skip_months = []

for i, month_start in enumerate(trade_months):
    month_end = trade_months[i + 1] if i + 1 < len(trade_months) else END_DATE

    stocks, breadth, sentiment, reason = select_stocks_enhanced(month_start, 15)

    print(f"[{i + 1}/{len(trade_months)}] {month_start}")
    print(f"  广度: {breadth:.2f}, 情绪(涨停): {sentiment}, 决策: {reason}")

    if stocks:
        ret = calc_monthly_return(stocks, month_start, month_end)
        enhanced_returns.append(ret)
        enhanced_trades += 1
        print(f"  选中: {len(stocks)} 只, 收益: {ret * 100:.2f}%")
    else:
        skip_months.append(month_start)
        enhanced_returns.append(0.0)
        print(f"  清仓观望")

# 统计分析
print("\n" + "=" * 70)
print("策略对比结果")
print("=" * 70)


def calc_stats(returns):
    """计算统计指标"""
    if not returns:
        return {"total": 0, "avg": 0, "sharpe": 0, "win_rate": 0, "max_dd": 0}

    total = (1 + pd.Series(returns)).prod() - 1
    avg = np.mean(returns)
    std = np.std(returns) if len(returns) > 1 else 0.01
    sharpe = avg / std * np.sqrt(12) if std > 0 else 0
    win_rate = sum(1 for r in returns if r > 0) / len(returns)

    # 最大回撤
    cum = (1 + pd.Series(returns)).cumprod()
    running_max = cum.cummax()
    dd = (cum - running_max) / running_max
    max_dd = dd.min()

    return {
        "total": total * 100,
        "avg": avg * 100,
        "sharpe": sharpe,
        "win_rate": win_rate * 100,
        "max_dd": max_dd * 100,
    }


base_stats = calc_stats(base_returns)
enhanced_stats = calc_stats(enhanced_returns)

print(f"\n{'指标':<20} {'原始策略':<20} {'增强策略':<20} {'差异':<15}")
print("-" * 75)
print(
    f"{'累计收益':<20} {base_stats['total']:.2f}%{'':<15} {enhanced_stats['total']:.2f}%{'':<15} {enhanced_stats['total'] - base_stats['total']:+.2f}%"
)
print(
    f"{'月均收益':<20} {base_stats['avg']:.2f}%{'':<15} {enhanced_stats['avg']:.2f}%{'':<15} {enhanced_stats['avg'] - base_stats['avg']:+.2f}%"
)
print(
    f"{'夏普比率':<20} {base_stats['sharpe']:.2f}{'':<17} {enhanced_stats['sharpe']:.2f}{'':<17} {enhanced_stats['sharpe'] - base_stats['sharpe']:+.2f}"
)
print(
    f"{'胜率':<20} {base_stats['win_rate']:.1f}%{'':<15} {enhanced_stats['win_rate']:.1f}%{'':<15} {enhanced_stats['win_rate'] - base_stats['win_rate']:+.1f}%"
)
print(
    f"{'最大回撤':<20} {base_stats['max_dd']:.2f}%{'':<15} {enhanced_stats['max_dd']:.2f}%{'':<15} {enhanced_stats['max_dd'] - base_stats['max_dd']:+.2f}%"
)
print(f"{'交易次数':<20} {base_trades}{'':<18} {enhanced_trades}{'':<18}")

print(f"\n增强策略清仓月份: {len(skip_months)} 次")
if skip_months:
    print(f"清仓月份: {skip_months[:5]}{'...' if len(skip_months) > 5 else ''}")

# 结论
print("\n" + "=" * 70)
print("结论")
print("=" * 70)

if enhanced_stats["sharpe"] > base_stats["sharpe"]:
    print("✓ 增强策略夏普比率更高，风险调整后收益更好")
if enhanced_stats["win_rate"] > base_stats["win_rate"]:
    print("✓ 增强策略胜率更高")
if enhanced_stats["max_dd"] > base_stats["max_dd"]:
    print("✓ 增强策略最大回撤更小")
if len(skip_months) > 0:
    print(f"✓ 增强策略在 {len(skip_months)} 个极端月份清仓避险")

# 保存结果
result = {
    "test_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "period": {"start": START_DATE, "end": END_DATE},
    "base_strategy": {
        "returns": base_returns,
        "stats": base_stats,
        "trades": base_trades,
    },
    "enhanced_strategy": {
        "returns": enhanced_returns,
        "stats": enhanced_stats,
        "trades": enhanced_trades,
        "skip_months": skip_months,
    },
}

# 尝试保存
try:
    output_path = "/Users/fengzhi/Downloads/git/testlixingren/output/enhanced_backtest_result.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n结果已保存: {output_path}")
except Exception as e:
    print(f"\n保存结果失败: {e}")
