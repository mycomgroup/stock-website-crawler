"""
RFScore7 + PB 市场适应性分析 - 米筐 Notebook 版本 (修正版)

使用 get_factor API 获取财务数据
"""

import numpy as np
import pandas as pd
from datetime import datetime

print("=" * 70)
print("RFScore7 + PB 市场适应性分析 (米筐)")
print("运行时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 70)


def get_monthly_dates(start_date, end_date):
    """获取月度调仓日期"""
    dates = get_trading_dates(start_date, end_date)
    result, last_m = [], None
    for d in dates:
        if d.month != last_m:
            result.append(d)
            last_m = d.month
    return result


def get_universe():
    """获取股票池：沪深300 + 中证500"""
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stocks = list(set(hs300 + zz500))
        return stocks[:300]  # 限制数量加快测试
    except:
        return []


def calc_rfscore7(stocks, date_str):
    """计算 RFScore7 因子 - 使用 get_factor API"""
    try:
        # 使用 get_factor 获取因子数据
        factors = [
            "pe_ratio",
            "pb_ratio",
            "market_cap",
            "roa",
            "roe",
            "gross_profit_margin",
            "net_profit_margin",
            "net_profit_yoy",
            "or_yoy",
        ]

        df = get_factor(stocks, factors, start_date=date_str, end_date=date_str)

        if df is None or df.empty:
            return pd.DataFrame()

        # 获取最新数据
        if "date" in df.columns:
            df = df.groupby("order_book_id").last().reset_index()

        # 计算得分
        df["score"] = 0
        if "roe" in df.columns:
            df.loc[df["roe"] > 0, "score"] += 1
        if "roa" in df.columns:
            df.loc[df["roa"] > 0, "score"] += 1
        if "gross_profit_margin" in df.columns:
            median_gpm = df["gross_profit_margin"].median()
            df.loc[df["gross_profit_margin"] > median_gpm, "score"] += 1
        if "net_profit_margin" in df.columns:
            df.loc[df["net_profit_margin"] > 0, "score"] += 1
        if "net_profit_yoy" in df.columns:
            df.loc[df["net_profit_yoy"] > 0, "score"] += 1
        if "or_yoy" in df.columns:
            df.loc[df["or_yoy"] > 0, "score"] += 1
        if "pe_ratio" in df.columns:
            df.loc[df["pe_ratio"] > 0, "score"] += 1

        return df
    except Exception as e:
        print(f"计算因子出错: {e}")
        return pd.DataFrame()


def get_market_state():
    """获取市场状态"""
    try:
        # 获取沪深300成分股
        hs300 = index_components("000300.XSHG")[:50]

        # 计算市场宽度
        above_ma20 = 0
        valid_count = 0

        for stock in hs300:
            try:
                bars = history_bars(stock, 20, "1d", "close", include_now=True)
                if bars is not None and len(bars) >= 20:
                    ma20 = np.mean(bars)
                    if bars[-1] > ma20:
                        above_ma20 += 1
                    valid_count += 1
            except:
                continue

        breadth = above_ma20 / valid_count if valid_count > 0 else 0.5

        # 获取沪深300指数趋势
        idx_bars = history_bars("000300.XSHG", 20, "1d", "close", include_now=True)
        if idx_bars is not None and len(idx_bars) >= 20:
            trend_on = idx_bars[-1] > np.mean(idx_bars)
        else:
            trend_on = True

        return {"breadth": breadth, "trend_on": trend_on}
    except:
        return {"breadth": 0.5, "trend_on": True}


def classify_regime(state):
    """分类市场状态"""
    b = state["breadth"]
    t = state["trend_on"]

    if t and b > 0.5:
        return "牛市"
    elif t and b > 0.35:
        return "震荡偏强"
    elif t:
        return "弱势反弹"
    elif not t and b > 0.3:
        return "震荡"
    elif not t and b > 0.2:
        return "震荡偏弱"
    else:
        return "熊市"


def run_backtest(start_date, end_date, pb_pct=10, hold_n=15):
    """运行回测"""
    dates = get_monthly_dates(start_date, end_date)
    print(f"\n测试区间: {start_date} ~ {end_date}")
    print(f"调仓次数: {len(dates) - 1}")

    records = []

    for i, d in enumerate(dates[:-1]):
        date_str = d.strftime("%Y-%m-%d")

        try:
            # 获取市场状态
            state = get_market_state()
            regime = classify_regime(state)

            # 获取股票池
            stocks = get_universe()
            if not stocks:
                continue

            # 计算因子
            df = calc_rfscore7(stocks, date_str)
            if df.empty:
                continue

            # PB 过滤
            if pb_pct is not None and "pb_ratio" in df.columns:
                pb_thresh = df["pb_ratio"].quantile(pb_pct / 100)
                df = df[df["pb_ratio"] <= pb_thresh]

            # 选股
            if "order_book_id" in df.columns:
                selected = df.nlargest(hold_n, "score")["order_book_id"].tolist()
            else:
                selected = df.nlargest(hold_n, "score").index.tolist()

            if not selected:
                continue

            # 计算收益 (使用历史数据模拟)
            rets = []
            for stock in selected:
                try:
                    bars = history_bars(stock, 20, "1d", "close", include_now=True)
                    if bars is not None and len(bars) >= 2:
                        ret = bars[-1] / bars[0] - 1
                        rets.append(ret)
                except:
                    continue

            if rets:
                avg_ret = np.mean(rets)

                # 基准收益
                idx_bars = history_bars(
                    "000300.XSHG", 20, "1d", "close", include_now=True
                )
                bench_ret = (
                    (idx_bars[-1] / idx_bars[0] - 1)
                    if idx_bars is not None and len(idx_bars) >= 2
                    else 0
                )

                records.append(
                    {
                        "date": date_str,
                        "regime": regime,
                        "breadth": state["breadth"],
                        "strategy_ret": avg_ret,
                        "benchmark_ret": bench_ret,
                        "excess_ret": avg_ret - bench_ret,
                        "stock_count": len(rets),
                    }
                )

                print(
                    f"[{i + 1}/{len(dates) - 1}] {date_str} | {regime:8s} | 宽度:{state['breadth']:.2f} | 策略:{avg_ret:6.2%} | 基准:{bench_ret:6.2%} | 股票:{len(rets)}"
                )

        except Exception as e:
            print(f"[{i + 1}] {date_str} 出错: {e}")
            continue

    return pd.DataFrame(records)


# ============ 运行测试 ============
print("\n" + "=" * 70)
print("【开始回测】")
print("=" * 70)

# 测试 PB10%
df_pb10 = run_backtest("2024-01-01", "2025-06-30", pb_pct=10, hold_n=15)

if not df_pb10.empty:
    print("\n" + "=" * 70)
    print("【结果汇总】")
    print("=" * 70)

    # 按市场状态汇总
    print("\n--- 各市场环境表现 ---")
    regimes = ["牛市", "震荡偏强", "弱势反弹", "震荡", "震荡偏弱", "熊市"]
    for regime in regimes:
        sub = df_pb10[df_pb10["regime"] == regime]
        if len(sub) < 1:
            continue
        s_ret = sub["strategy_ret"].mean()
        b_ret = sub["benchmark_ret"].mean()
        excess = sub["excess_ret"].mean()
        win = (sub["strategy_ret"] > 0).mean()
        print(
            f"  {regime:10s}: 月数={len(sub):2d} 策略={s_ret:6.2%} 基准={b_ret:6.2%} 超额={excess:6.2%} 胜率={win:.0%}"
        )

    # 总体统计
    print("\n--- 总体统计 ---")
    total_ret = (1 + df_pb10["strategy_ret"]).prod() - 1
    bench_ret = (1 + df_pb10["benchmark_ret"]).prod() - 1
    months = len(df_pb10)
    ann_ret = (1 + total_ret) ** (12 / months) - 1 if months > 0 else 0

    print(f"  测试月数: {months}")
    print(f"  累计收益: {total_ret:.2%}")
    print(f"  年化收益: {ann_ret:.2%}")
    print(f"  基准收益: {bench_ret:.2%}")
    print(f"  超额收益: {total_ret - bench_ret:.2%}")
    print(f"  月胜率: {(df_pb10['strategy_ret'] > 0).mean():.0%}")
    print(f"  最大单月亏损: {df_pb10['strategy_ret'].min():.2%}")
    print(f"  最大单月盈利: {df_pb10['strategy_ret'].max():.2%}")

    # 当前市场状态
    print("\n--- 当前市场状态 ---")
    today_state = get_market_state()
    today_regime = classify_regime(today_state)
    print(f"  市场宽度: {today_state['breadth']:.2%}")
    print(f"  趋势状态: {'向上' if today_state['trend_on'] else '向下'}")
    print(f"  市场环境: {today_regime}")

    # 操作建议
    print("\n--- 操作建议 ---")
    if today_state["breadth"] >= 0.35 and today_state["trend_on"]:
        print("  ✅ 满仓: 市场环境良好")
    elif today_state["breadth"] >= 0.25:
        print("  ⚠️ 半仓: 市场环境一般")
    else:
        print("  ❌ 空仓: 市场环境较差")

else:
    print("回测数据为空，请检查")

print("\n=== 测试完成 ===")
