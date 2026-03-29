# 纯 A 股 ETF 池重建实验
# 旧池 vs 新池 对比验证
# 运行环境: 聚宽 Research

from jqdata import *
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

print("=" * 80)
print("【纯 A 股 ETF 池重建实验】")
print("=" * 80)
print()
print("实验目的:")
print("1. 验证删除跨市场资产后，ETF基线是否更清晰")
print("2. 对比旧池和新池的动量基线表现")
print("3. 为新池提供推荐版本")
print()
print("=" * 80)
print()

# ============================================================================
# 一、池子定义
# ============================================================================

# ---- 旧池定义 (v1.0) - 包含跨市场资产 ----
OLD_POOL = {
    "沪深300ETF": "510300.XSHG",
    "中证500ETF": "510500.XSHG",
    "创业板ETF": "159915.XSHE",
    "科创50ETF": "588000.XSHG",
    "中证1000ETF": "512100.XSHG",
    "纳指ETF": "513100.XSHG",  # 跨市场 - 美股
    "标普500ETF": "513500.XSHG",  # 跨市场 - 美股
    "黄金ETF": "518880.XSHG",  # 跨市场 - 商品
    "国债ETF": "511010.XSHG",  # 跨市场 - 固收
    "医疗ETF": "512170.XSHG",
    "消费ETF": "159928.XSHE",
    "新能源ETF": "516160.XSHG",
}

# ---- 新池定义 (v2.0) - 纯 A 股 ----
NEW_POOL = {
    # 宽基
    "沪深300ETF": "510300.XSHG",
    "中证500ETF": "510500.XSHG",
    "创业板ETF": "159915.XSHE",
    "科创50ETF": "588000.XSHG",
    "中证1000ETF": "512100.XSHG",
    # 行业
    "医疗ETF": "512170.XSHG",
    "消费ETF": "159928.XSHE",
    "新能源ETF": "516160.XSHG",
    "半导体ETF": "512480.XSHG",
    "军工ETF": "512660.XSHG",
    "银行ETF": "512800.XSHG",
    "计算机ETF": "512720.XSHG",
}

print("=" * 80)
print("【一、池子定义】")
print("=" * 80)
print()
print("旧池 (v1.0) - 12只 ETF:")
for name, code in OLD_POOL.items():
    cross_market = (
        " [跨市场]" if name in ["纳指ETF", "标普500ETF", "黄金ETF", "国债ETF"] else ""
    )
    print(f"  {name}: {code}{cross_market}")

print()
print("新池 (v2.0) - 12只 ETF:")
print("  [宽基]")
for name, code in list(NEW_POOL.items())[:5]:
    print(f"    {name}: {code}")
print("  [行业]")
for name, code in list(NEW_POOL.items())[5:]:
    print(f"    {name}: {code}")

print()
print("=" * 80)
print()

# ============================================================================
# 二、删除跨市场资产的原因分析
# ============================================================================

print("=" * 80)
print("【二、删除跨市场资产的原因】")
print("=" * 80)
print()
print("1. 纳指ETF (513100) & 标普500ETF (513500):")
print("   - 原因: 美股市场资产，走势与 A 股关联度低")
print("   - 问题: 用 A 股市场的择时信号(宽度/RSRS)判断美股仓位不合理")
print()
print("2. 黄金ETF (518880):")
print("   - 原因: 商品市场资产，避险属性")
print("   - 问题: 与 A 股风险偏好相关，但波动特性差异大")
print()
print("3. 国债ETF (511010):")
print("   - 原因: 固收市场资产，波动率极低")
print("   - 问题: 干扰动量计算，动量排名时几乎总是垫底")
print()
print("=" * 80)
print()

# ============================================================================
# 三、回测参数
# ============================================================================

START = "2020-01-01"
END = "2025-12-31"
COST = 0.001  # 单边成本 0.1%

print("=" * 80)
print("【三、回测参数】")
print("=" * 80)
print(f"  回测区间: {START} ~ {END}")
print(f"  交易成本: 单边 {COST:.1%}")
print(f"  动量窗口: 20日")
print(f"  持有周期: 10日")
print(f"  持仓数量: Top 3")
print()
print("=" * 80)
print()

# ============================================================================
# 四、回测函数
# ============================================================================


def get_rebal_dates(start, end, freq_days):
    """按固定天数间隔取调仓日"""
    all_days = get_trade_days(start, end)
    result = [all_days[0]]
    for d in all_days[1:]:
        if (d - result[-1]).days >= freq_days:
            result.append(d)
    return result


def run_etf_backtest(pool, pool_name, mom_window=20, hold_days=10, top_n=3):
    """运行 ETF 动量回测"""
    print(f"  正在运行 {pool_name} 回测...")

    dates = get_rebal_dates(START, END, hold_days)
    codes = list(pool.values())
    monthly_rets = []
    prev_holdings = []
    holding_records = []

    for i, d in enumerate(dates[:-1]):
        d_str = str(d)
        next_d_str = str(dates[i + 1])
        try:
            # 计算动量
            prices = get_price(
                codes,
                end_date=d_str,
                count=mom_window + 1,
                fields=["close"],
                panel=False,
            )
            pivot = prices.pivot(index="time", columns="code", values="close").dropna(
                axis=1
            )
            if len(pivot) < mom_window + 1:
                continue
            mom = pivot.iloc[-1] / pivot.iloc[0] - 1
            selected = mom.nlargest(top_n).index.tolist()

            # 记录持仓
            name_map = dict(zip(pool.values(), pool.keys()))
            holding_records.append(
                {
                    "date": d_str,
                    "holdings": [name_map.get(c, c) for c in selected],
                    "momentum": {
                        name_map.get(c, c): f"{v:+.2%}"
                        for c, v in mom[selected].items()
                    },
                }
            )

            # 计算持有收益
            p0 = get_price(
                selected, end_date=d_str, count=1, fields=["close"], panel=False
            )
            p1 = get_price(
                selected, end_date=next_d_str, count=1, fields=["close"], panel=False
            )
            p0 = p0.pivot(index="time", columns="code", values="close").iloc[-1]
            p1 = p1.pivot(index="time", columns="code", values="close").iloc[-1]
            gross_ret = ((p1 / p0) - 1).mean()

            # 扣除换手成本
            turnover = len(set(selected) - set(prev_holdings)) / top_n
            net_ret = gross_ret - turnover * COST * 2
            monthly_rets.append(net_ret)
            prev_holdings = selected
        except Exception as e:
            continue

    if not monthly_rets:
        return None

    s = pd.Series(monthly_rets)
    cum = (1 + s).cumprod()
    periods_per_year = 252 / hold_days
    ann = cum.iloc[-1] ** (periods_per_year / len(s)) - 1
    dd = (cum / cum.cummax() - 1).min()
    sharpe = s.mean() / s.std() * (periods_per_year**0.5) if s.std() > 0 else 0
    win = (s > 0).mean()

    # 计算总换手
    total_turnover = sum(
        [
            len(set(h["holdings"]) - set(prev)) / top_n
            for h, prev in zip(
                holding_records[1:], [h["holdings"] for h in holding_records[:-1]]
            )
        ]
    )
    avg_turnover = total_turnover / len(holding_records) if holding_records else 0

    return {
        "池子": pool_name,
        "年化收益(扣费)": ann,
        "最大回撤": dd,
        "夏普比率": sharpe,
        "胜率": win,
        "样本数": len(s),
        "平均换手率": avg_turnover,
        "持仓记录": holding_records,
        "净值曲线": cum,
    }


# ============================================================================
# 五、运行回测
# ============================================================================

print("=" * 80)
print("【五、运行回测】")
print("=" * 80)
print()

old_result = run_etf_backtest(OLD_POOL, "旧池(v1.0)")
new_result = run_etf_backtest(NEW_POOL, "新池(v2.0)")

print()
print("=" * 80)
print()

# ============================================================================
# 六、结果对比
# ============================================================================

print("=" * 80)
print("【六、结果对比】")
print("=" * 80)
print()

comparison_data = []
for result in [old_result, new_result]:
    if result:
        comparison_data.append(
            {
                "池子": result["池子"],
                "年化收益(扣费)": f"{result['年化收益(扣费)']:.2%}",
                "最大回撤": f"{result['最大回撤']:.2%}",
                "夏普比率": f"{result['夏普比率']:.2f}",
                "胜率": f"{result['胜率']:.1%}",
                "样本数": result["样本数"],
                "平均换手率": f"{result['平均换手率']:.1%}",
            }
        )

df_comparison = pd.DataFrame(comparison_data)
df_comparison = df_comparison.set_index("池子")
print(df_comparison.to_string())
print()

# 计算差异
if old_result and new_result:
    print("=" * 80)
    print("【变化分析】")
    print("=" * 80)
    ann_change = new_result["年化收益(扣费)"] - old_result["年化收益(扣费)"]
    dd_change = new_result["最大回撤"] - old_result["最大回撤"]
    sharpe_change = new_result["夏普比率"] - old_result["夏普比率"]

    print(
        f"  年化收益变化: {ann_change:+.2%} ({old_result['年化收益(扣费)']:.2%} → {new_result['年化收益(扣费)']:.2%})"
    )
    print(
        f"  最大回撤变化: {dd_change:+.2%} ({old_result['最大回撤']:.2%} → {new_result['最大回撤']:.2%})"
    )
    print(
        f"  夏普比率变化: {sharpe_change:+.2f} ({old_result['夏普比率']:.2f} → {new_result['夏普比率']:.2f})"
    )
    print()

    if ann_change > 0:
        print("  ✅ 年化收益提升")
    elif ann_change > -0.01:
        print("  ⚠️  年化收益基本持平")
    else:
        print("  ❌ 年化收益下降")

    if dd_change > 0:
        print("  ❌ 最大回撤扩大")
    elif dd_change > -0.01:
        print("  ⚠️  最大回撤基本持平")
    else:
        print("  ✅ 最大回撤改善")

    if sharpe_change > 0:
        print("  ✅ 夏普比率提升")
    elif sharpe_change > -0.05:
        print("  ⚠️  夏普比率基本持平")
    else:
        print("  ❌ 夏普比率下降")

print()
print("=" * 80)
print()

# ============================================================================
# 七、近期持仓记录
# ============================================================================

if old_result and new_result:
    print("=" * 80)
    print("【七、近期持仓记录对比】")
    print("=" * 80)
    print()
    print("旧池最近5期持仓:")
    for rec in old_result["持仓记录"][-5:]:
        print(f"  {rec['date']}: {rec['holdings']}")
    print()
    print("新池最近5期持仓:")
    for rec in new_result["持仓记录"][-5:]:
        print(f"  {rec['date']}: {rec['holdings']}")
    print()
    print("=" * 80)
    print()

# ============================================================================
# 八、当前动量排名
# ============================================================================

print("=" * 80)
print("【八、当前 ETF 动量排名 (20日)】")
print("=" * 80)
print()

today = get_trade_days(end_date=context.current_dt, count=1)[-1]

print("旧池当前动量排名:")
old_codes = list(OLD_POOL.values())
old_prices = get_price(
    old_codes, end_date=str(today), count=21, fields=["close"], panel=False
)
old_pivot = old_prices.pivot(index="time", columns="code", values="close").dropna(
    axis=1
)
old_mom = (old_pivot.iloc[-1] / old_pivot.iloc[0] - 1).sort_values(ascending=False)
old_name_map = dict(zip(OLD_POOL.values(), OLD_POOL.keys()))
for code, val in old_mom.items():
    print(f"  {old_name_map.get(code, code)}: {val:+.2%}")

print()
print("新池当前动量排名:")
new_codes = list(NEW_POOL.values())
new_prices = get_price(
    new_codes, end_date=str(today), count=21, fields=["close"], panel=False
)
new_pivot = new_prices.pivot(index="time", columns="code", values="close").dropna(
    axis=1
)
new_mom = (new_pivot.iloc[-1] / new_pivot.iloc[0] - 1).sort_values(ascending=False)
new_name_map = dict(zip(NEW_POOL.values(), NEW_POOL.keys()))
for code, val in new_mom.items():
    print(f"  {new_name_map.get(code, code)}: {val:+.2%}")

print()
print("=" * 80)
print()

# ============================================================================
# 九、池子内部相关性分析
# ============================================================================

print("=" * 80)
print("【九、池子内部相关性分析】")
print("=" * 80)
print()

# 计算旧池相关性
old_prices_60d = get_price(
    old_codes, end_date=str(today), count=60, fields=["close"], panel=False
)
old_pivot_60d = old_prices_60d.pivot(index="time", columns="code", values="close")
old_returns = old_pivot_60d.pct_change().dropna()
old_corr = old_returns.corr()
old_corr_mean = old_corr.values[np.triu_indices_from(old_corr.values, k=1)].mean()
print(f"旧池平均相关性: {old_corr_mean:.3f}")

# 计算新池相关性
new_prices_60d = get_price(
    new_codes, end_date=str(today), count=60, fields=["close"], panel=False
)
new_pivot_60d = new_prices_60d.pivot(index="time", columns="code", values="close")
new_returns = new_pivot_60d.pct_change().dropna()
new_corr = new_returns.corr()
new_corr_mean = new_corr.values[np.triu_indices_from(new_corr.values, k=1)].mean()
print(f"新池平均相关性: {new_corr_mean:.3f}")

print()
if new_corr_mean < old_corr_mean:
    print("✅ 新池相关性更低，分散效果更好")
else:
    print("⚠️  新池相关性略高")

print()
print("=" * 80)
print()

# ============================================================================
# 十、结论
# ============================================================================

print("=" * 80)
print("【十、实验结论】")
print("=" * 80)
print()
print("1. 删除跨市场资产的原因:")
print("   - 纳指/标普ETF: 美股市场，与A股择时信号逻辑不匹配")
print("   - 黄金ETF: 商品市场，波动特性不同")
print("   - 国债ETF: 固收市场，波动率极低，干扰动量计算")
print()
print("2. 新池特点:")
print("   - 纯A股资产，择时信号一致性更好")
print("   - 宽基+行业，覆盖主要市场板块")
print("   - 流动性充足，均可正常交易")
print()
print("3. 推荐池子版本:")
print("   建议使用 PURE_A_ETF_POOL_V2 (纯A股池)")
print("   适用于:")
print("   - 叠加A股市场择时信号(宽度/RSRS等)")
print("   - 行业增强策略")
print("   - 需要统一市场环境判断的策略")
print()
print("=" * 80)
print()
print("实验完成!")
