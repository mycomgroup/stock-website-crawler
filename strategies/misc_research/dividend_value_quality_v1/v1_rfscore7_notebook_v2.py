# V1 RFScore7 进攻版 - RiceQuant Notebook 格式 (修正版)
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
    try:
        # 中证800股票池 - RiceQuant格式
        stocks_300 = index_components("000300.XSHG")
        stocks_500 = index_components("000905.XSHG")
        stocks = list(set(stocks_300 + stocks_500))

        if len(stocks) == 0:
            print("  无股票数据")
            return []

        print(f"  股票池: {len(stocks)}只")

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

        df = get_fundamentals(q, entry_date=date)

        if df is None or len(df) == 0:
            print("  无基本面数据")
            return []

        print(f"  PB低20%筛选: {len(df)}只")

        # 按ROA排序
        df = df.sort_values("roa", ascending=False)

        result = df["code"].tolist()[:n]
        print(f"  最终选股: {len(result)}只")

        return result

    except Exception as e:
        print(f"  选股错误: {e}")
        import traceback

        traceback.print_exc()
        return []


def run_backtest(dates):
    """运行回测"""
    rets = []
    prev = []

    for i, d in enumerate(dates[:-1]):
        d_str = d.strftime("%Y-%m-%d")
        next_d_str = dates[i + 1].strftime("%Y-%m-%d")

        print(f"\n{d_str}:")

        try:
            # 选股
            selected = select_rfscore7(d_str, STOCK_NUM)

            if len(selected) == 0:
                print("  跳过: 无选股")
                continue

            # 获取价格 - RiceQuant格式
            p0_dict = {}
            p1_dict = {}

            for stock in selected:
                try:
                    bars0 = history_bars(stock, 1, "1d", "close", dt=d_str)
                    bars1 = history_bars(stock, 1, "1d", "close", dt=next_d_str)
                    if bars0 is not None and len(bars0) > 0:
                        p0_dict[stock] = bars0[-1]
                    if bars1 is not None and len(bars1) > 0:
                        p1_dict[stock] = bars1[-1]
                except:
                    continue

            if len(p0_dict) == 0 or len(p1_dict) == 0:
                print("  跳过: 无价格数据")
                continue

            # 计算收益
            common_stocks = set(p0_dict.keys()) & set(p1_dict.keys())
            if len(common_stocks) == 0:
                print("  跳过: 无共同股票")
                continue

            rets_list = []
            for stock in common_stocks:
                ret = (p1_dict[stock] / p0_dict[stock]) - 1
                rets_list.append(ret)

            ret = np.mean(rets_list)

            # 计算换手成本
            turnover = len(set(selected) - set(prev)) / len(selected)
            net_ret = ret - turnover * COST * 2

            rets.append(net_ret)
            prev = selected

            print(f"  收益: {net_ret:.2%} (换手率: {turnover:.0%})")

        except Exception as e:
            print(f"  错误: {e}")
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
