"""
主仓动态映射候选表轻量比较 - 验证脚本

目标：验证 A/B/C 三张映射表与静态 60/40 的历史表现对比
方法：基于历史状态序列 + 各资产类别真实收益，模拟组合收益

运行平台：JoinQuant Notebook
"""

from jqdata import *
import pandas as pd
import numpy as np

print("=== 主仓动态映射候选表轻量比较验证 ===")

try:
    # ============================================================
    # 1. 定义状态判定规则（冻结口径，引用任务 02）
    # ============================================================

    def calc_breadth(date, window=20):
        """计算市场宽度：沪深300 close > MA20 比例"""
        hs300 = get_index_stocks("000300.XSHG", date=date)
        prices = get_price(
            hs300, end_date=date, count=window, fields=["close"], panel=False
        )
        close = prices.pivot(index="time", columns="code", values="close")
        return float((close.iloc[-1] > close.mean()).mean())

    def calc_trend(date, window=20):
        """计算趋势：沪深300 当前价 > MA20"""
        idx = get_price("000300.XSHG", end_date=date, count=window, fields=["close"])
        return float(idx["close"].iloc[-1]) > float(idx["close"].mean())

    def calc_fed(date):
        """计算 FED 指标：100/PE中位数 - 国债收益率"""
        hs300 = get_index_stocks("000300.XSHG", date=date)
        q = query(valuation.code, valuation.pe_ratio).filter(
            valuation.code.in_(hs300), valuation.pe_ratio > 0
        )
        df = get_fundamentals(q, date=date)
        if df.empty:
            return None
        pe_median = df["pe_ratio"].median()
        # 使用近似国债收益率（10年期），简化处理
        bond_yield = 0.023  # 固定近似值
        return 100.0 / pe_median - bond_yield * 100

    def determine_regime(breadth, trend, fed=None):
        """四状态判定（冻结规则）"""
        # 简化：估值高估判断暂用 FED < 0
        overvalued = fed is not None and fed < 0
        trend_up = trend

        if breadth > 0.70 or overvalued:
            return "高估防守"
        elif breadth > 0.50 and trend_up:
            return "趋势进攻"
        elif breadth >= 0.30:
            return "震荡轮动"
        else:
            return "底部试错"

    # ============================================================
    # 2. 定义映射表
    # ============================================================

    mapping_tables = {
        "静态60/40": {
            "股票": 0.60,
            "红利小盘": 0.40,
            "国债": 0.00,
            "动量": 0.00,
            "现金": 0.00,
        },
        "表A_保守": {
            "底部试错": {"RFScore": 0.20, "国债": 0.35, "动量": 0.05, "现金": 0.40},
            "震荡轮动": {"RFScore": 0.30, "国债": 0.30, "动量": 0.10, "现金": 0.30},
            "趋势进攻": {"RFScore": 0.35, "国债": 0.25, "动量": 0.15, "现金": 0.25},
            "高估防守": {"RFScore": 0.10, "国债": 0.45, "动量": 0.05, "现金": 0.40},
        },
        "表B_均衡": {
            "底部试错": {"RFScore": 0.25, "国债": 0.30, "动量": 0.10, "现金": 0.35},
            "震荡轮动": {"RFScore": 0.35, "国债": 0.25, "动量": 0.15, "现金": 0.25},
            "趋势进攻": {"RFScore": 0.40, "国债": 0.20, "动量": 0.25, "现金": 0.15},
            "高估防守": {"RFScore": 0.15, "国债": 0.40, "动量": 0.05, "现金": 0.40},
        },
        "表C_进攻": {
            "底部试错": {"RFScore": 0.30, "国债": 0.25, "动量": 0.15, "现金": 0.30},
            "震荡轮动": {"RFScore": 0.40, "国债": 0.20, "动量": 0.20, "现金": 0.20},
            "趋势进攻": {"RFScore": 0.50, "国债": 0.15, "动量": 0.25, "现金": 0.10},
            "高估防守": {"RFScore": 0.15, "国债": 0.40, "动量": 0.05, "现金": 0.40},
        },
    }

    # ============================================================
    # 3. 获取历史状态序列（月度采样）
    # ============================================================

    print("\n--- 获取历史状态序列 ---")

    # 采样日期：2024-01 至 2026-03，每月最后一个交易日
    start_date = "2024-01-01"
    end_date = "2026-03-31"

    trade_days = get_trade_days(start_date=start_date, end_date=end_date)

    # 按月采样
    monthly_dates = []
    current_month = None
    for d in trade_days:
        if d.month != current_month:
            if current_month is not None:
                monthly_dates.append(last_date)
            current_month = d.month
        last_date = d
    if last_date not in monthly_dates:
        monthly_dates.append(last_date)

    print(f"采样日期数量: {len(monthly_dates)}")

    # 计算每个月的状态
    regime_history = []
    for date in monthly_dates:
        date_str = str(date)[:10]
        breadth = calc_breadth(date_str)
        trend = calc_trend(date_str)
        fed = calc_fed(date_str)
        regime = determine_regime(breadth, trend, fed)

        regime_history.append(
            {
                "date": date_str,
                "breadth": round(breadth, 3),
                "trend": trend,
                "fed": round(fed, 2) if fed else None,
                "regime": regime,
            }
        )

        trend_str = "up" if trend else "down"
        fed_str = f"{fed:.1f}" if fed else "N/A"
        print(
            f"  {date_str}: 宽度={breadth:.1%}, 趋势={trend_str}, FED={fed_str}, 状态={regime}"
        )

    df_regime = pd.DataFrame(regime_history)

    # 统计状态分布
    print("\n--- 状态分布 ---")
    regime_counts = df_regime["regime"].value_counts()
    for regime, count in regime_counts.items():
        pct = count / len(df_regime) * 100
        print(f"  {regime}: {count} 个月 ({pct:.1f}%)")

    # ============================================================
    # 4. 获取各资产类别月度收益
    # ============================================================

    print("\n--- 获取资产收益数据 ---")

    # 资产代理
    assets = {
        "沪深300": "000300.XSHG",  # RFScore 股票代理
        "国债ETF": "511010.XSHG",
        "动量ETF": "159915.XSHE",  # 创业板ETF 作为动量代理
        "现金": None,  # 年化 2%
    }

    # 获取月度收益
    monthly_returns = {}
    cash_monthly_return = 0.02 / 12  # 年化 2% 折算月度

    for asset_name, asset_code in assets.items():
        if asset_code is None:
            # 现金
            monthly_returns[asset_name] = [cash_monthly_return] * len(monthly_dates)
            continue

        prices = get_price(
            asset_code,
            end_date=monthly_dates[-1],
            count=len(monthly_dates) + 1,
            fields=["close"],
            panel=False,
        )
        if prices is not None and not prices.empty:
            closes = prices["close"].values
            returns = []
            for i in range(1, len(closes)):
                ret = (closes[i] - closes[i - 1]) / closes[i - 1]
                returns.append(ret)
            # 对齐到采样日期
            if len(returns) >= len(monthly_dates):
                monthly_returns[asset_name] = returns[-len(monthly_dates) :]
            else:
                monthly_returns[asset_name] = returns + [0] * (
                    len(monthly_dates) - len(returns)
                )
        else:
            monthly_returns[asset_name] = [0] * len(monthly_dates)

        total_ret = np.prod([1 + r for r in monthly_returns[asset_name]]) - 1
        print(f"  {asset_name}: 期间总收益 {total_ret:.2%}")

    # RFScore 股票使用沪深300作为代理
    monthly_returns["RFScore"] = monthly_returns["沪深300"]

    # 红利小盘使用近似（这里用中证1000代理小盘）
    try:
        zz1000_prices = get_price(
            "000852.XSHG",
            end_date=monthly_dates[-1],
            count=len(monthly_dates) + 1,
            fields=["close"],
            panel=False,
        )
        if zz1000_prices is not None and not zz1000_prices.empty:
            closes = zz1000_prices["close"].values
            returns = []
            for i in range(1, len(closes)):
                ret = (closes[i] - closes[i - 1]) / closes[i - 1]
                returns.append(ret)
            if len(returns) >= len(monthly_dates):
                monthly_returns["红利小盘"] = returns[-len(monthly_dates) :]
            else:
                monthly_returns["红利小盘"] = returns + [0] * (
                    len(monthly_dates) - len(returns)
                )
            total_ret = np.prod([1 + r for r in monthly_returns["红利小盘"]]) - 1
            print(f"  红利小盘(中证1000代理): 期间总收益 {total_ret:.2%}")
    except:
        monthly_returns["红利小盘"] = monthly_returns["沪深300"]
        print("  红利小盘: 使用沪深300代理")

    # 动量使用创业板ETF
    monthly_returns["动量"] = monthly_returns["动量ETF"]

    # ============================================================
    # 5. 模拟各配置方案收益
    # ============================================================

    print("\n--- 模拟配置方案收益 ---")

    results = {}

    # 静态 60/40
    static_returns = []
    for i in range(len(monthly_dates)):
        ret = (
            monthly_returns["RFScore"][i] * 0.60 + monthly_returns["红利小盘"][i] * 0.40
        )
        static_returns.append(ret)
    results["静态60/40"] = static_returns

    # 动态映射表
    for table_name in ["表A_保守", "表B_均衡", "表C_进攻"]:
        table_returns = []
        for i in range(len(monthly_dates)):
            regime = df_regime.iloc[i]["regime"]
            weights = mapping_tables[table_name][regime]

            ret = 0
            ret += weights.get("RFScore", 0) * monthly_returns["RFScore"][i]
            ret += weights.get("国债", 0) * monthly_returns["国债ETF"][i]
            ret += weights.get("动量", 0) * monthly_returns["动量"][i]
            ret += weights.get("现金", 0) * monthly_returns["现金"][i]

            table_returns.append(ret)
        results[table_name] = table_returns

    # ============================================================
    # 6. 计算绩效指标
    # ============================================================

    print("\n=== 绩效对比 ===")
    print(
        f"{'指标':<20} {'静态60/40':>12} {'表A_保守':>12} {'表B_均衡':>12} {'表C_进攻':>12}"
    )
    print("-" * 70)

    metrics = {}
    for name, returns in results.items():
        cumulative = np.prod([1 + r for r in returns]) - 1
        annualized = (1 + cumulative) ** (12 / len(returns)) - 1

        # 最大回撤
        cum_values = np.cumprod([1 + r for r in returns])
        peak = np.maximum.accumulate(cum_values)
        drawdown = (cum_values - peak) / peak
        max_drawdown = np.min(drawdown)

        # 夏普比率（假设无风险利率 2%）
        excess_returns = [r - 0.02 / 12 for r in returns]
        if np.std(excess_returns) > 0:
            sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(12)
        else:
            sharpe = 0

        metrics[name] = {
            "累计收益": cumulative,
            "年化收益": annualized,
            "最大回撤": max_drawdown,
            "夏普比率": sharpe,
            "月度收益": returns,
        }

        print(
            f"{name:<20} {cumulative:>11.2%} {annualized:>11.2%} {max_drawdown:>11.2%} {sharpe:>11.2f}"
        )

    # ============================================================
    # 7. 分状态表现
    # ============================================================

    print("\n=== 分状态表现 ===")

    for regime in ["底部试错", "震荡轮动", "趋势进攻", "高估防守"]:
        mask = df_regime["regime"] == regime
        if mask.sum() == 0:
            print(f"\n{regime}: 无样本")
            continue

        print(f"\n{regime} ({mask.sum()} 个月):")
        print(f"  {'方案':<15} {'平均月收益':>12} {'累计收益':>12}")

        for name, returns in results.items():
            regime_returns = [returns[i] for i in range(len(returns)) if mask.iloc[i]]
            avg_monthly = np.mean(regime_returns)
            cumulative = np.prod([1 + r for r in regime_returns]) - 1
            print(f"  {name:<15} {avg_monthly:>11.4%} {cumulative:>11.2%}")

    # ============================================================
    # 8. 结论
    # ============================================================

    print("\n=== 结论 ===")

    best_annualized = max(metrics.items(), key=lambda x: x[1]["年化收益"])
    best_sharpe = max(metrics.items(), key=lambda x: x[1]["夏普比率"])
    best_drawdown = min(metrics.items(), key=lambda x: x[1]["最大回撤"])

    print(f"最高年化收益: {best_annualized[0]} ({best_annualized[1]['年化收益']:.2%})")
    print(f"最高夏普比率: {best_sharpe[0]} ({best_sharpe[1]['夏普比率']:.2f})")
    print(f"最小最大回撤: {best_drawdown[0]} ({best_drawdown[1]['最大回撤']:.2%})")

    # 动态 vs 静态
    for table_name in ["表A_保守", "表B_均衡", "表C_进攻"]:
        diff = metrics[table_name]["年化收益"] - metrics["静态60/40"]["年化收益"]
        print(f"{table_name} vs 静态60/40 年化差异: {diff:+.2%}")

    print("\n=== 验证完成 ===")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
