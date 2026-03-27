#!/usr/bin/env python3
"""
因子库整理与回测评估框架实测
"""

import pandas as pd
import numpy as np
from jqdata import *
from jqfactor import get_all_factors

print("=" * 60)
print("因子库整理与回测评估框架 - 2024-2025实测")
print("=" * 60)

# ========== 1. 获取因子库 ==========
print("\n----- 聚宽因子库统计 -----")
all_factors = get_all_factors()
category_counts = all_factors["category"].value_counts()
print(f"因子总数: {len(all_factors)}")
print("\n分类统计:")
print(category_counts)

# ========== 2. 单因子有效性测试 ==========
print("\n----- 单因子有效性测试 -----")


def test_factor_validity(factor_name, start_date="2024-01-01", end_date="2025-03-26"):
    """测试单个因子的有效性"""
    try:
        # 获取股票池
        stocks = get_index_stocks("000300.XSHG")

        # 过滤ST和停牌
        is_st = get_extras("is_st", stocks, end_date=start_date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()

        # 获取因子数据
        from jqfactor import get_factor_values

        factor_data = get_factor_values(
            stocks, factor_name, start_date=start_date, end_date=end_date, count=100
        )

        if factor_data.empty:
            return None

        # 获取价格数据计算收益
        price_data = get_price(
            stocks,
            start_date=start_date,
            end_date=end_date,
            fields=["close"],
            panel=False,
        )
        price_pivot = price_data.pivot(index="time", columns="code", values="close")

        # 计算未来收益
        forward_returns = price_pivot.pct_change().shift(-1)

        # 对齐数据
        common_dates = factor_data.index.intersection(forward_returns.index)
        common_stocks = factor_data.columns.intersection(forward_returns.columns)

        if len(common_dates) < 10 or len(common_stocks) < 10:
            return None

        factor_aligned = factor_data.loc[common_dates, common_stocks]
        return_aligned = forward_returns.loc[common_dates, common_stocks]

        # 计算IC
        ic_series = factor_aligned.corrwith(return_aligned, axis=1)

        return {
            "factor": factor_name,
            "ic_mean": ic_series.mean(),
            "ic_std": ic_series.std(),
            "ic_ir": ic_series.mean() / ic_series.std() if ic_series.std() > 0 else 0,
            "ic_positive_rate": (ic_series > 0).sum() / len(ic_series),
        }
    except Exception as e:
        return None


# 测试代表性因子
test_factors = [
    "roe",
    "roa",
    "pe_ratio",
    "pb_ratio",
    "market_cap",
    "gross_profit_margin",
    "net_profit_margin",
    "eps",
]

valid_results = []
for factor in test_factors:
    result = test_factor_validity(factor)
    if result:
        valid_results.append(result)
        print(
            f"{factor}: IC均值={result['ic_mean']:.4f}, IC_IR={result['ic_ir']:.4f}, 胜率={result['ic_positive_rate']:.2%}"
        )

# ========== 3. 多因子组合测试 ==========
print("\n----- 多因子组合测试 -----")


def multi_factor_test(start_date="2024-01-01", end_date="2025-03-26"):
    """多因子组合测试"""
    stocks = get_index_stocks("000300.XSHG")

    # 过滤股票
    is_st = get_extras("is_st", stocks, end_date=start_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    # 获取财务数据
    q = query(
        valuation.code,
        indicator.roe,
        indicator.roa,
        indicator.gross_profit_margin,
        indicator.net_profit_margin,
        valuation.pe_ratio,
        valuation.pb_ratio,
        valuation.market_cap,
    ).filter(valuation.code.in_(stocks))

    df = get_fundamentals(q, date=start_date)
    df = df.set_index("code")

    # 标准化处理
    for col in ["roe", "roa", "gross_profit_margin", "net_profit_margin"]:
        df[f"{col}_score"] = (df[col] - df[col].mean()) / df[col].std()

    for col in ["pe_ratio", "pb_ratio"]:
        df[f"{col}_score"] = -(df[col] - df[col].mean()) / df[col].std()  # 越低越好

    # 计算综合得分
    df["total_score"] = (
        df["roe_score"]
        + df["roa_score"]
        + df["gross_profit_margin_score"]
        + df["net_profit_margin_score"]
        + df["pe_ratio_score"]
        + df["pb_ratio_score"]
    ) / 6

    # 选择得分最高的20只
    selected = df.nlargest(20, "total_score")

    print(f"选股数量: {len(selected)}")
    print(f"平均ROE: {selected['roe'].mean():.2f}%")
    print(f"平均PE: {selected['pe_ratio'].mean():.2f}")
    print(f"平均PB: {selected['pb_ratio'].mean():.2f}")

    return selected


selected_stocks = multi_factor_test()

# ========== 4. 行业分布分析 ==========
print("\n----- 选股行业分布 -----")
try:
    # 获取行业信息
    industry_info = {}
    for stock in selected_stocks.index[:10]:  # 取前10只分析
        stock_industry = get_industry(stock, date="2024-01-02")
        if stock_industry and stock in stock_industry:
            sw_l1 = stock_industry[stock].get("sw_l1", {}).get("industry_name", "未知")
            industry_info[stock] = sw_l1

    industry_df = pd.DataFrame.from_dict(
        industry_info, orient="index", columns=["行业"]
    )
    print(industry_df)
    print(f"\n行业分布:")
    print(industry_df["行业"].value_counts())
except Exception as e:
    print(f"行业分析出错: {e}")

print("\n" + "=" * 60)
print("实测完成!")
print("=" * 60)
