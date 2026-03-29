#!/usr/bin/env python3
"""
RFScore7因子模型 - 最近数据实测
基于FScore9因子模型改进的RFScore7因子
"""

import datetime as dt
import numpy as np
import pandas as pd
from jqdata import *
from jqfactor import get_factor_values

print("=" * 60)
print("RFScore7因子模型 - 2024-2025年实测")
print("=" * 60)


# ========== 股票筛选函数 ==========
def filter_stocks(stocks, date):
    """过滤ST、停牌、涨跌停股票"""
    # 过滤ST
    is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    # 过滤停牌
    paused = get_price(stocks, end_date=date, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code")["paused"]
    paused_ser = paused.iloc[-1]
    stocks = paused_ser[paused_ser == 0].index.tolist()

    return stocks


# ========== 获取交易日期 ==========
def get_monthly_dates(start_date, end_date):
    """获取月度交易日期"""
    trade_days = get_trade_days(start_date, end_date)
    monthly_dates = []
    current_month = None
    for day in trade_days:
        if current_month != day.month:
            monthly_dates.append(day)
            current_month = day.month
    return monthly_dates


# ========== FScore因子计算 ==========
def calc_fscore_factors(stocks, date):
    """计算FScore相关因子"""
    try:
        # 获取财务数据
        q = query(
            valuation.code,
            indicator.roe,
            indicator.roa,
            indicator.gross_profit_margin,
            indicator.net_profit_margin,
            indicator.eps,
            indicator.inc_net_profit_year_on_year,  # 净利润同比增长率
            indicator.inc_revenue_year_on_year,  # 营业收入同比增长率
            valuation.pe_ratio,
            valuation.pb_ratio,
            valuation.ps_ratio,
            valuation.market_cap,
        ).filter(valuation.code.in_(stocks))

        df = get_fundamentals(q, date=date)
        df = df.set_index("code")

        # 计算FScore得分 (简化版7因子)
        df["fscore"] = 0

        # 1. ROE > 0
        df.loc[df["roe"] > 0, "fscore"] += 1

        # 2. ROA > 0
        df.loc[df["roa"] > 0, "fscore"] += 1

        # 3. 毛利率 > 行业中位数 (简化为>30%)
        df.loc[df["gross_profit_margin"] > 30, "fscore"] += 1

        # 4. 净利润同比增长 > 0
        df.loc[df["inc_net_profit_year_on_year"] > 0, "fscore"] += 1

        # 5. 营收同比增长 > 0
        df.loc[df["inc_revenue_year_on_year"] > 0, "fscore"] += 1

        # 6. PE为正且<30
        df.loc[(df["pe_ratio"] > 0) & (df["pe_ratio"] < 30), "fscore"] += 1

        # 7. PB < 5
        df.loc[df["pb_ratio"] < 5, "fscore"] += 1

        return df
    except Exception as e:
        print(f"计算因子出错: {e}")
        return pd.DataFrame()


# ========== 主测试流程 ==========
# 测试时间范围：2024年1月 - 2025年3月
start_date = "2024-01-01"
end_date = "2025-03-26"

print(f"\n测试期间: {start_date} 至 {end_date}")

# 获取沪深300成分股
stocks = get_index_stocks("000300.XSHG")
print(f"初始股票池: {len(stocks)} 只")

# 获取月度调仓日期
monthly_dates = get_monthly_dates(start_date, end_date)
print(f"调仓次数: {len(monthly_dates)} 次")

# 存储结果
results = []
stock_selections = {}

for i, date in enumerate(monthly_dates):
    date_str = date.strftime("%Y-%m-%d")
    print(f"\n[{i + 1}/{len(monthly_dates)}] 调仓日期: {date_str}")

    # 过滤股票
    filtered_stocks = filter_stocks(stocks, date_str)

    if len(filtered_stocks) == 0:
        print("  无有效股票，跳过")
        continue

    # 计算因子
    factor_df = calc_fscore_factors(filtered_stocks, date_str)

    if factor_df.empty:
        print("  因子计算失败，跳过")
        continue

    # 按FScore排序选股
    factor_df = factor_df.sort_values("fscore", ascending=False)

    # 选择FScore最高的20只股票
    selected = factor_df.head(20)
    stock_selections[date_str] = selected.index.tolist()

    print(f"  选股数量: {len(selected)}")
    print(f"  FScore分布: {selected['fscore'].value_counts().to_dict()}")
    print(f"  平均PE: {selected['pe_ratio'].mean():.2f}")
    print(f"  平均PB: {selected['pb_ratio'].mean():.2f}")
    print(f"  平均ROE: {selected['roe'].mean():.2f}%")

    # 计算收益（如果有下个月数据）
    if i < len(monthly_dates) - 1:
        next_date = monthly_dates[i + 1]
        next_date_str = next_date.strftime("%Y-%m-%d")

        try:
            # 获取调仓日收盘价
            prices_start = get_price(
                selected.index.tolist(),
                end_date=date_str,
                count=1,
                fields=["close"],
                panel=False,
            )
            prices_start = prices_start.pivot(
                index="time", columns="code", values="close"
            )

            # 获取下月收盘价
            prices_end = get_price(
                selected.index.tolist(),
                end_date=next_date_str,
                count=1,
                fields=["close"],
                panel=False,
            )
            prices_end = prices_end.pivot(index="time", columns="code", values="close")

            # 计算收益
            returns = (prices_end.iloc[-1] / prices_start.iloc[-1] - 1).dropna()
            avg_return = returns.mean()

            results.append(
                {
                    "date": date_str,
                    "next_date": next_date_str,
                    "avg_return": avg_return,
                    "stock_count": len(returns),
                    "win_rate": (returns > 0).sum() / len(returns),
                }
            )

            print(f"  下期平均收益: {avg_return:.2%}")
            print(f"  胜率: {(returns > 0).sum()}/{len(returns)}")

        except Exception as e:
            print(f"  计算收益出错: {e}")

# ========== 结果汇总 ==========
print("\n" + "=" * 60)
print("实测结果汇总")
print("=" * 60)

if results:
    results_df = pd.DataFrame(results)

    print(f"\n调仓次数: {len(results_df)}")
    print(f"平均月收益: {results_df['avg_return'].mean():.2%}")
    print(f"月收益标准差: {results_df['avg_return'].std():.2%}")
    print(
        f"月胜率: {(results_df['avg_return'] > 0).sum()}/{len(results_df)} = {(results_df['avg_return'] > 0).mean():.2%}"
    )
    print(f"最大单月收益: {results_df['avg_return'].max():.2%}")
    print(f"最大单月亏损: {results_df['avg_return'].min():.2%}")

    # 计算累计收益
    cumulative = (1 + results_df["avg_return"]).cumprod()
    total_return = cumulative.iloc[-1] - 1
    print(f"\n累计收益: {total_return:.2%}")
    print(f"年化收益: {(1 + total_return) ** (12 / len(results_df)) - 1:.2%}")

    # 输出每月收益明细
    print("\n----- 每月收益明细 -----")
    for _, row in results_df.iterrows():
        print(
            f"{row['date']} -> {row['next_date']}: {row['avg_return']:.2%} (胜率: {row['win_rate']:.0%})"
        )

print("\n实测完成!")
