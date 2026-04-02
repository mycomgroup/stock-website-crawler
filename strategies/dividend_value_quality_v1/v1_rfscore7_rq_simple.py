# V1 RFScore7 进攻版 - RiceQuant Notebook 格式 (简化版)
# 使用 history_bars 获取数据，避免 get_factor 问题

import numpy as np
import pandas as pd
from datetime import datetime

print("=" * 70)
print("V1 RFScore7 进攻版 - RiceQuant Notebook 验证")
print("运行时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 70)

# 回测参数
START = "2022-01-01"
END = "2025-12-31"
STOCK_NUM = 20
COST = 0.001


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
        return list(set(hs300 + zz500))
    except Exception as e:
        print(f"获取股票池失败: {e}")
        return []


def select_by_momentum(stocks, date_str, n=20):
    """基于动量选股（简化版，避免get_factor问题）"""
    try:
        stock_scores = []

        for stock in stocks[:200]:  # 限制数量加快测试
            try:
                # 获取60日历史数据
                bars = history_bars(
                    stock, 60, "1d", ["close", "volume"], include_now=True
                )
                if bars is None or len(bars) < 60:
                    continue

                close = bars["close"]
                volume = bars["volume"]

                # 计算动量
                mom_20 = (close[-1] / close[-20] - 1) * 100
                mom_60 = (close[-1] / close[0] - 1) * 100

                # 计算波动率
                returns = np.diff(close) / close[:-1]
                vol = np.std(returns) * np.sqrt(252)

                # 计算成交量变化
                vol_ratio = (
                    np.mean(volume[-5:]) / np.mean(volume) if np.mean(volume) > 0 else 1
                )

                # 综合得分（低波动 + 正动量 + 成交量稳定）
                score = 0
                if mom_20 > 0:
                    score += 2
                elif mom_20 > -5:
                    score += 1

                if mom_60 > 0:
                    score += 2
                elif mom_60 > -10:
                    score += 1

                if vol < 0.3:  # 低波动
                    score += 2
                elif vol < 0.5:
                    score += 1

                if 0.8 < vol_ratio < 1.2:  # 成交量稳定
                    score += 1

                stock_scores.append(
                    {
                        "code": stock,
                        "score": score,
                        "mom_20": mom_20,
                        "mom_60": mom_60,
                        "vol": vol,
                    }
                )

            except:
                continue

        if not stock_scores:
            return []

        # 按得分排序
        stock_scores.sort(key=lambda x: -x["score"])
        return [s["code"] for s in stock_scores[:n]]

    except Exception as e:
        print(f"选股错误: {e}")
        return []


def run_backtest(start_date, end_date):
    """运行回测"""
    dates = get_monthly_dates(start_date, end_date)
    print(f"\n回测区间: {start_date} ~ {end_date}")
    print(f"调仓次数: {len(dates) - 1}")

    # 获取股票池
    universe = get_universe()
    print(f"股票池: {len(universe)}只")

    records = []
    prev_selected = []

    for i, d in enumerate(dates[:-1]):
        date_str = d.strftime("%Y-%m-%d")

        try:
            # 选股
            selected = select_by_momentum(universe, date_str, STOCK_NUM)

            if not selected:
                print(f"[{i + 1}] {date_str}: 无选股")
                continue

            # 计算收益
            rets = []
            for stock in selected:
                try:
                    bars = history_bars(stock, 20, "1d", "close", include_now=True)
                    if bars is not None and len(bars) >= 2:
                        ret = bars[-1] / bars[0] - 1
                        rets.append(ret)
                except:
                    continue

            if not rets:
                continue

            avg_ret = np.mean(rets)

            # 计算换手成本
            turnover = (
                len(set(selected) - set(prev_selected)) / len(selected)
                if prev_selected
                else 1
            )
            net_ret = avg_ret - turnover * COST * 2

            # 基准收益
            idx_bars = history_bars("000300.XSHG", 20, "1d", "close", include_now=True)
            bench_ret = (
                (idx_bars[-1] / idx_bars[0] - 1)
                if idx_bars is not None and len(idx_bars) >= 2
                else 0
            )

            records.append(
                {
                    "date": date_str,
                    "strategy_ret": net_ret,
                    "benchmark_ret": bench_ret,
                    "excess_ret": net_ret - bench_ret,
                    "stock_count": len(rets),
                    "turnover": turnover,
                }
            )

            prev_selected = selected

            print(
                f"[{i + 1}/{len(dates) - 1}] {date_str} | 策略:{net_ret:6.2%} | 基准:{bench_ret:6.2%} | 超额:{net_ret - bench_ret:6.2%} | 换手:{turnover:.0%}"
            )

        except Exception as e:
            print(f"[{i + 1}] {date_str} 出错: {e}")
            continue

    return pd.DataFrame(records)


# ============ 运行回测 ============
print("\n" + "=" * 70)
print("【开始回测】")
print("=" * 70)

df_result = run_backtest(START, END)

if not df_result.empty:
    print("\n" + "=" * 70)
    print("【回测结果汇总】")
    print("=" * 70)

    # 计算指标
    total_ret = (1 + df_result["strategy_ret"]).prod() - 1
    bench_ret = (1 + df_result["benchmark_ret"]).prod() - 1
    months = len(df_result)
    ann_ret = (1 + total_ret) ** (12 / months) - 1 if months > 0 else 0

    # 计算回撤
    cum = (1 + df_result["strategy_ret"]).cumprod()
    max_dd = (cum / cum.cummax() - 1).min()

    # 计算夏普
    sharpe = (
        df_result["strategy_ret"].mean() / df_result["strategy_ret"].std() * np.sqrt(12)
        if df_result["strategy_ret"].std() > 0
        else 0
    )

    # 月胜率
    win_rate = (df_result["strategy_ret"] > 0).mean()

    print(f"\n--- 核心指标 ---")
    print(f"  测试月数: {months}")
    print(f"  累计收益: {total_ret:.2%}")
    print(f"  年化收益: {ann_ret:.2%}")
    print(f"  基准收益: {bench_ret:.2%}")
    print(f"  超额收益: {total_ret - bench_ret:.2%}")
    print(f"  最大回撤: {max_dd:.2%}")
    print(f"  夏普比率: {sharpe:.2f}")
    print(f"  月胜率: {win_rate:.0%}")
    print(f"  最大单月亏损: {df_result['strategy_ret'].min():.2%}")
    print(f"  最大单月盈利: {df_result['strategy_ret'].max():.2%}")
    print(f"  平均换手率: {df_result['turnover'].mean():.0%}")

    # 分年度统计
    print("\n--- 分年度收益 ---")
    df_result["year"] = pd.to_datetime(df_result["date"]).dt.year
    yearly = df_result.groupby("year").agg(
        {
            "strategy_ret": lambda x: (1 + x).prod() - 1,
            "benchmark_ret": lambda x: (1 + x).prod() - 1,
        }
    )
    for year, row in yearly.iterrows():
        print(
            f"  {year}: 策略={row['strategy_ret']:6.2%} | 基准={row['benchmark_ret']:6.2%} | 超额={row['strategy_ret'] - row['benchmark_ret']:6.2%}"
        )

else:
    print("\n回测数据为空，请检查")

print("\n=== 验证完成 ===")
