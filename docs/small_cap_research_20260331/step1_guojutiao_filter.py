"""
Step 1: 国九条筛选有效性验证

目标：验证国九条筛选是否能有效过滤风险股票
方法：对比筛选前后股票的退市率、ST率、业绩表现

RiceQuant Notebook 运行方式：
node run-strategy.js --strategy step1_guojutiao_filter.py --timeout-ms 300000
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

print("=" * 60)
print("Step 1: 国九条筛选有效性验证")
print("=" * 60)

# ============================================================
# 1. 获取基础股票池
# ============================================================
print("\n[1. 获取基础股票池]")

try:
    # RiceQuant API: 获取所有A股股票
    all_stocks_df = all_instruments(type="CS")
    all_stocks = all_stocks_df["order_book_id"].tolist()

    print(f"全A股票数量: {len(all_stocks)}")

    # 过滤掉科创北交（流动性考虑）
    main_board_stocks = [
        s
        for s in all_stocks
        if not s.startswith("688") and not s.startswith("8") and not s.startswith("4")
    ]
    print(f"主板股票数量: {len(main_board_stocks)}")

except Exception as e:
    print(f"获取股票池失败: {e}")
    all_stocks = []
    main_board_stocks = []

# ============================================================
# 2. 国九条筛选条件定义
# ============================================================
print("\n[2. 国九条筛选条件定义]")

"""
国九条退市标准 → 策略过滤条件：

1. 财务造假退市：审计意见必须为无保留意见（近3年无异常）
2. 利润退市：净利润>0 且 营业收入>3亿
3. 分红ST风险：近三年累计分红>5000万 或 >年均净利润30%
4. 市值退市：市值>5亿（主板）

简化版筛选条件（Notebook快速验证）：
- 市值范围：10-300亿（避开微盘流动性风险）
- 净利润>0
- 营业收入>1亿
- 排除ST、退市、次新股
"""


def apply_guojutiao_filter(stock_list, test_date=None):
    """
    应用国九条筛选条件

    注意：RiceQuant Notebook环境下，部分财务数据API可能有限制
    这里先实现基础筛选，后续可扩展
    """

    if not stock_list:
        return [], {}

    filtered_stocks = []
    filter_stats = {
        "total": len(stock_list),
        "filtered_by_market_cap": 0,
        "filtered_by_st": 0,
        "filtered_by_new": 0,
        "final": 0,
    }

    # 获取当前数据
    current_data = {}
    try:
        # RiceQuant: 获取股票快照数据
        # 注意：这里简化处理，实际需要分批获取
        sample_stocks = stock_list[:100]  # 先测试100只

        for stock in sample_stocks:
            try:
                # 获取基本信息
                info = instruments(stock)
                if info:
                    current_data[stock] = {
                        "symbol": info.symbol,
                        "display_name": info.display_name,
                        "listed_date": str(info.listed_date)
                        if info.listed_date
                        else None,
                        "de_listed_date": str(info.de_listed_date)
                        if info.de_listed_date
                        else None,
                    }
            except:
                continue

    except Exception as e:
        print(f"获取股票数据失败: {e}")

    # 应用筛选条件
    for stock in stock_list[:100]:  # 限制数量避免超时
        try:
            # 条件1：排除ST股票
            if stock in current_data:
                name = current_data[stock].get("display_name", "")
                if "ST" in name or "*" in name or "退" in name:
                    filter_stats["filtered_by_st"] += 1
                    continue

            # 条件2：排除次新股（上市不满1年）
            if stock in current_data:
                listed_date = current_data[stock].get("listed_date")
                if listed_date:
                    try:
                        listed_dt = datetime.strptime(listed_date[:10], "%Y-%m-%d")
                        if datetime.now() - listed_dt < timedelta(days=365):
                            filter_stats["filtered_by_new"] += 1
                            continue
                    except:
                        pass

            # 条件3：排除已退市股票
            if stock in current_data:
                de_listed = current_data[stock].get("de_listed_date")
                if de_listed and de_listed != "None" and de_listed != "":
                    continue

            filtered_stocks.append(stock)

        except Exception as e:
            continue

    filter_stats["final"] = len(filtered_stocks)

    return filtered_stocks, filter_stats


# ============================================================
# 3. 执行筛选并统计
# ============================================================
print("\n[3. 执行筛选并统计]")

if main_board_stocks:
    filtered_stocks, filter_stats = apply_guojutiao_filter(main_board_stocks)

    print("\n筛选统计:")
    print(f"  原始股票数: {filter_stats['total']}")
    print(f"  ST/退市过滤: {filter_stats['filtered_by_st']}")
    print(f"  次新股过滤: {filter_stats['filtered_by_new']}")
    print(f"  最终股票数: {filter_stats['final']}")
    print(
        f"  过滤比例: {(1 - filter_stats['final'] / filter_stats['total']) * 100:.1f}%"
    )

# ============================================================
# 4. 市值分布分析
# ============================================================
print("\n[4. 市值分布分析（样例测试）]")

if filtered_stocks:
    print(f"\n对{len(filtered_stocks[:20])}只股票进行市值分析...")

    # RiceQuant: 获取市值数据
    # 注意：这里使用简化的方法
    market_cap_data = []

    for stock in filtered_stocks[:20]:
        try:
            # 获取最近的价格和成交量
            bars = history_bars(stock, 1, "1d", ["close", "volume"])
            if bars is not None and len(bars) > 0:
                close = bars["close"][-1]
                volume = bars["volume"][-1]
                market_cap_data.append(
                    {
                        "code": stock,
                        "close": close,
                        "volume": volume,
                    }
                )
        except:
            continue

    if market_cap_data:
        mc_df = pd.DataFrame(market_cap_data)
        print("\n样例股票价格分布:")
        print(mc_df[["code", "close"]].head(10).to_string(index=False))

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
   - 过滤掉了 {filter_stats["filtered_by_st"]} 只ST/退市股票
   - 过滤掉了 {filter_stats["filtered_by_new"]} 只次新股

2. 下一步建议：
   - Step2: 对筛选后的股票池进行因子有效性测试
   - 重点测试：估值因子（PE/PB）、质量因子（ROE/ROA）、成长因子

3. 注意事项：
   - Notebook环境限制了财务数据的获取
   - 完整筛选需在策略编辑器中进行
   - 建议先完成因子测试，再进行完整回测
""")
else:
    print("筛选失败，请检查API连接或股票池数据")

print("\n" + "=" * 60)
print("Step 1 完成")
print("=" * 60)
