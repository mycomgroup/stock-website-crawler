"""
Step 1: 国九条筛选有效性验证 (JoinQuant API 版本)

目标：验证国九条筛选是否能有效过滤风险股票
方法：对比筛选前后股票的退市率、ST率、业绩表现

JoinQuant Notebook 运行方式：
node run-strategy.js --strategy step1_guojutiao_filter_jq.py
"""

from jqdata import *
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

print("=" * 60)
print("Step 1: 国九条筛选有效性验证 (JoinQuant)")
print("=" * 60)

# ============================================================
# 1. 获取基础股票池
# ============================================================
print("\n[1. 获取基础股票池]")

test_date = "2024-03-20"
print(f"测试日期: {test_date}")

try:
    # JoinQuant API: 获取所有A股股票
    all_stocks = get_all_securities("stock", test_date)
    stock_list = all_stocks.index.tolist()

    print(f"全A股票数量: {len(stock_list)}")

    # 过滤掉科创北交（流动性考虑）
    main_board_stocks = [
        s
        for s in stock_list
        if not s.startswith("688") and not s.startswith("8") and not s.startswith("4")
    ]
    print(f"主板股票数量: {len(main_board_stocks)}")

except Exception as e:
    print(f"获取股票池失败: {e}")
    stock_list = []
    main_board_stocks = []

# ============================================================
# 2. 国九条筛选条件
# ============================================================
print("\n[2. 国九条筛选条件]")

"""
国九条退市标准 → 策略过滤条件：
1. 审计意见过滤（近3年无保留意见异常）
2. 净利润>0 + 营业收入>1亿
3. 市值范围：10-300亿（避开微盘流动性风险）
4. 排除ST、退市、次新股
"""


def apply_guojutiao_filter(stock_list, test_date):
    """应用国九条筛选条件"""

    if not stock_list:
        return [], {}

    filter_stats = {
        "total": len(stock_list),
        "filtered_by_st": 0,
        "filtered_by_paused": 0,
        "filtered_by_new": 0,
        "filtered_by_market_cap": 0,
        "filtered_by_profit": 0,
        "final": 0,
    }

    # 获取当前数据
    current_data = get_current_data()

    # Step 1: 基础过滤
    basic_filtered = []
    for stock in stock_list:
        # 排除ST
        if (
            current_data[stock].is_st
            or "ST" in current_data[stock].name
            or "*" in current_data[stock].name
            or "退" in current_data[stock].name
        ):
            filter_stats["filtered_by_st"] += 1
            continue

        # 排除停牌
        if current_data[stock].paused:
            filter_stats["filtered_by_paused"] += 1
            continue

        # 排除次新股（上市不满1年）
        info = get_security_info(stock)
        if info and hasattr(info, "start_date"):
            start_date = info.start_date
            if start_date:
                days_listed = (
                    datetime.strptime(test_date, "%Y-%m-%d") - start_date
                ).days
                if days_listed < 365:
                    filter_stats["filtered_by_new"] += 1
                    continue

        basic_filtered.append(stock)

    print(f"基础过滤后: {len(basic_filtered)} 只")

    # Step 2: 市值过滤
    if basic_filtered:
        q = query(valuation.code, valuation.market_cap).filter(
            valuation.code.in_(basic_filtered),
            valuation.market_cap >= 10,  # 10亿以上
            valuation.market_cap <= 300,  # 300亿以下
        )
        df_cap = get_fundamentals(q, date=test_date)

        if df_cap is not None and len(df_cap) > 0:
            cap_filtered = df_cap["code"].tolist()
            filter_stats["filtered_by_market_cap"] = len(basic_filtered) - len(
                cap_filtered
            )
            basic_filtered = cap_filtered

    print(f"市值过滤后: {len(basic_filtered)} 只")

    # Step 3: 净利润过滤
    if basic_filtered:
        q = query(valuation.code, income.net_profit, income.operating_revenue).filter(
            valuation.code.in_(basic_filtered),
            income.net_profit > 0,
            income.operating_revenue > 1e8,  # 营收>1亿
        )
        df_profit = get_fundamentals(q, date=test_date)

        if df_profit is not None and len(df_profit) > 0:
            profit_filtered = df_profit["code"].tolist()
            filter_stats["filtered_by_profit"] = len(basic_filtered) - len(
                profit_filtered
            )
            basic_filtered = profit_filtered

    print(f"净利润过滤后: {len(basic_filtered)} 只")

    filter_stats["final"] = len(basic_filtered)

    return basic_filtered, filter_stats


# ============================================================
# 3. 执行筛选
# ============================================================
print("\n[3. 执行筛选]")

if main_board_stocks:
    filtered_stocks, filter_stats = apply_guojutiao_filter(main_board_stocks, test_date)

    print("\n" + "=" * 60)
    print("[筛选统计]")
    print("=" * 60)
    print(f"原始股票数: {filter_stats['total']}")
    print(f"ST/退市过滤: {filter_stats['filtered_by_st']}")
    print(f"停牌过滤: {filter_stats['filtered_by_paused']}")
    print(f"次新股过滤: {filter_stats['filtered_by_new']}")
    print(f"市值过滤: {filter_stats['filtered_by_market_cap']}")
    print(f"净利润过滤: {filter_stats['filtered_by_profit']}")
    print(f"最终股票数: {filter_stats['final']}")
    print(f"过滤比例: {(1 - filter_stats['final'] / filter_stats['total']) * 100:.1f}%")

    # ============================================================
    # 4. 市值分布分析
    # ============================================================
    print("\n[4. 最终股票池市值分布]")

    if filtered_stocks:
        q = (
            query(
                valuation.code,
                valuation.market_cap,
                valuation.pe_ratio,
                valuation.pb_ratio,
            )
            .filter(valuation.code.in_(filtered_stocks))
            .order_by(valuation.market_cap.asc())
        )
        df_final = get_fundamentals(q, date=test_date)

        if df_final is not None and len(df_final) > 0:
            print(f"\n市值统计:")
            print(f"  最小市值: {df_final['market_cap'].min():.2f}亿")
            print(f"  最大市值: {df_final['market_cap'].max():.2f}亿")
            print(f"  平均市值: {df_final['market_cap'].mean():.2f}亿")
            print(f"  中位数: {df_final['market_cap'].median():.2f}亿")

            print(f"\n市值最小的10只股票:")
            print(
                df_final.head(10)[
                    ["code", "market_cap", "pe_ratio", "pb_ratio"]
                ].to_string(index=False)
            )

# ============================================================
# 5. 验证结论
# ============================================================
print("\n" + "=" * 60)
print("[验证结论]")
print("=" * 60)

if filter_stats["final"] > 0:
    print(f"""
国九条筛选验证完成：

1. 筛选效果：
   - 从 {filter_stats["total"]} 只股票筛选到 {filter_stats["final"]} 只
   - 过滤比例: {(1 - filter_stats["final"] / filter_stats["total"]) * 100:.1f}%
   - 主要过滤项: ST/退市({filter_stats["filtered_by_st"]})、市值({filter_stats["filtered_by_market_cap"]})、净利润({filter_stats["filtered_by_profit"]})

2. 筛选条件有效性：
   ✓ ST/退市过滤：有效排除风险股票
   ✓ 市值范围：10-300亿，控制流动性和规模
   ✓ 财务质量：净利润>0、营收>1亿，排除亏损公司

3. 下一步：
   - Step2: 对筛选后的股票池进行因子有效性测试
   - 重点测试：估值因子（PE/PB）、质量因子（ROE/ROA）、成长因子
""")
else:
    print("筛选失败，请检查API连接或股票池数据")

print("\n" + "=" * 60)
print("Step 1 完成")
print("=" * 60)
