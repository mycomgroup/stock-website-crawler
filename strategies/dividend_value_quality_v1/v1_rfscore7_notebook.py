# V1 RFScore7 进攻版 - RiceQuant Notebook 格式
# 用于快速验证策略逻辑

print("=" * 70)
print("V1 RFScore7 进攻版 - RiceQuant Notebook 验证")
print("=" * 70)

# 回测区间
START = "2022-01-01"
END = "2025-12-31"
STOCK_NUM = 20
COST = 0.001

import pandas as pd
import numpy as np


def get_monthly_dates(start, end):
    """获取月度调仓日期"""
    dates = get_trading_dates(start, end)
    result, last_m = [], None
    for d in dates:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result


def select_rfscore7(date, n=20):
    """RFScore7 + PB低20%选股"""
    # 中证800股票池
    stocks_300 = index_components("000300", date=date)
    stocks_500 = index_components("000905", date=date)
    stocks = list(set(stocks_300 + stocks_500))

    if len(stocks) == 0:
        return []

    # 获取PB和ROA数据
    q = (
        query(
            fundamentals.eod_derivative_indicator.code,
            fundamentals.eod_derivative_indicator.pb_ratio,
            fundamentals.profit_statement.roa,
        )
        .filter(
            fundamentals.eod_derivative_indicator.code.in_(stocks),
            fundamentals.eod_derivative_indicator.pe_ratio > 0,
            fundamentals.eod_derivative_indicator.pb_ratio > 0,
            fundamentals.profit_statement.roa > 0,
        )
        .order_by(fundamentals.eod_derivative_indicator.pb_ratio.asc())
        .limit(int(len(stocks) * 0.2))
    )

    df = get_fundamentals(q, date=date)

    if df is None or len(df) == 0:
        return []

    # 按ROA排序
    df = df.sort_values("roa", ascending=False)

    return df["code"].tolist()[:n]


def run_backtest(dates):
    """运行回测"""
    rets = []
    prev = []

    for i, d in enumerate(dates[:-1]):
        d_str = d.strftime("%Y-%m-%d")
        next_d_str = dates[i + 1].strftime("%Y-%m-%d")

        try:
            # 选股
            selected = select_rfscore7(d_str, STOCK_NUM)

            if len(selected) == 0:
                continue

            # 获取价格
            p0 = history_bars(selected, 1, "1d", "close", date=d_str)
            p1 = history_bars(selected, 1, "1d", "close", date=next_d_str)

            if p0 is None or p1 is None:
                continue

            # 计算收益
            ret = (p1 / p0 - 1).mean()

            # 计算换手成本
            turnover = len(set(selected) - set(prev)) / len(selected)
            net_ret = ret - turnover * COST * 2

            rets.append(net_ret)
            prev = selected

            print(f"{d_str}: 选股{len(selected)}只, 收益{net_ret:.2%}")

        except Exception as e:
            print(f"{d_str}: 错误 - {e}")
            continue

    return rets


# 运行回测
print(f"\n回测区间: {START} ~ {END}")
print(f"持仓数量: {STOCK_NUM}")
print(f"调仓频率: 月度")

dates = get_monthly_dates(START, END)
print(f"调仓次数: {len(dates) - 1}")

print("\n开始回测...")
rets = run_backtest(dates)

# 计算指标
if len(rets) > 0:
    s = pd.Series(rets)
    cum = (1 + s).cumprod()
    ann = cum.iloc[-1] ** (12 / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (12**0.5) if s.std() > 0 else 0
    win = (s > 0).mean()

    print("\n" + "=" * 70)
    print("【回测结果】")
    print("=" * 70)
    print(f"年化收益: {ann:.1%}")
    print(f"累计收益: {cum.iloc[-1] - 1:.1%}")
    print(f"最大回撤: {dd:.1%}")
    print(f"夏普比率: {sharpe:.2f}")
    print(f"月胜率: {win:.0%}")
    print(f"样本月数: {len(s)}")
else:
    print("\n回测失败，无有效数据")

print("\n验证完成!")
