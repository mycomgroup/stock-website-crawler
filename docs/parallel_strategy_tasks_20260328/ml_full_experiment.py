# -*- coding: utf-8 -*-
"""
ML多因子Walk-Forward完整实验
=============================
测试多种场景：
1. 弱因子信号（真实情况模拟）
2. 无因子信号（纯随机基线）
3. 不同训练窗口对比
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ml_walkforward_validation import MLWalkForwardValidator, format_results


def generate_data_with_signal(n_months=60, n_stocks=300, signal_strength=0.02, seed=42):
    """生成带因子信号的数据"""
    np.random.seed(seed)

    dates = pd.date_range("2019-01-01", periods=n_months, freq="ME")
    stocks = [f"STOCK_{i:04d}" for i in range(n_stocks)]

    monthly_data = {}

    for idx, date in enumerate(dates):
        feat = pd.DataFrame(
            np.random.randn(n_stocks, 14),
            index=stocks,
            columns=[
                "EP",
                "BP",
                "SP",
                "CFP",
                "pe_ratio",
                "pb_ratio",
                "ps_ratio",
                "pcf_ratio",
                "roe",
                "roa",
                "gross_profit_margin",
                "net_profit_to_total_revenue",
                "inc_net_profit_year_on_year",
                "inc_revenue_year_on_year",
            ],
        )

        feat["market_cap"] = np.random.lognormal(15, 1.5, n_stocks)
        feat["log_market_cap"] = np.log(feat["market_cap"])

        # 收益率 = 随机噪声 + 因子信号
        base_return = np.random.randn(n_stocks) * 0.1
        factor_signal = signal_strength * (feat["EP"] + feat["BP"] + feat["roe"])
        returns = base_return + factor_signal

        label = (returns > returns.median()).astype(int)

        monthly_data[idx] = {
            "feat": feat,
            "label": label,
            "ret": pd.Series(returns, index=stocks),
            "date": date,
        }

    return monthly_data


def run_scenario(scenario_name, monthly_data, train_months=12):
    """运行单个场景"""
    print(f"\n{'=' * 60}")
    print(f"场景: {scenario_name}")
    print(f"{'=' * 60}")

    validator = MLWalkForwardValidator(
        train_months=train_months, hold_n=20, cost=0.001, top_pct=0.3
    )

    results_df, raw_results = validator.run_validation(monthly_data)
    return results_df, raw_results


def main():
    print("=" * 70)
    print("ML多因子Walk-Forward 完整实验")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    all_results = {}

    # 场景1: 强因子信号 (signal=0.03)
    print("\n>>> 生成场景1: 强因子信号")
    data_strong = generate_data_with_signal(n_months=60, signal_strength=0.03)
    results_strong, _ = run_scenario("强因子信号 (signal=0.03)", data_strong)
    all_results["强因子信号"] = results_strong

    # 场景2: 弱因子信号 (signal=0.01)
    print("\n>>> 生成场景2: 弱因子信号")
    data_weak = generate_data_with_signal(n_months=60, signal_strength=0.01)
    results_weak, _ = run_scenario("弱因子信号 (signal=0.01)", data_weak)
    all_results["弱因子信号"] = results_weak

    # 场景3: 无因子信号 (纯随机)
    print("\n>>> 生成场景3: 无因子信号 (纯随机)")
    data_random = generate_data_with_signal(n_months=60, signal_strength=0.0)
    results_random, _ = run_scenario("无因子信号 (纯随机)", data_random)
    all_results["无因子信号"] = results_random

    # 场景4: 短训练窗口 (6个月)
    print("\n>>> 生成场景4: 短训练窗口")
    data_short = generate_data_with_signal(n_months=48, signal_strength=0.02)
    results_short, _ = run_scenario("短训练窗口 (6个月)", data_short, train_months=6)
    all_results["短训练窗口"] = results_short

    # 场景5: 长训练窗口 (24个月)
    print("\n>>> 生成场景5: 长训练窗口")
    data_long = generate_data_with_signal(n_months=60, signal_strength=0.02)
    results_long, _ = run_scenario("长训练窗口 (24个月)", data_long, train_months=24)
    all_results["长训练窗口"] = results_long

    # 汇总所有结果
    print("\n" + "=" * 70)
    print("【实验汇总】")
    print("=" * 70)

    summary_data = []
    for scenario, df in all_results.items():
        for model in df.index:
            summary_data.append(
                {
                    "场景": scenario,
                    "模型": model,
                    "年化收益": df.loc[model, "年化收益"],
                    "最大回撤": df.loc[model, "最大回撤"],
                    "夏普比率": df.loc[model, "夏普比率"],
                    "月胜率": df.loc[model, "月胜率"],
                }
            )

    summary_df = pd.DataFrame(summary_data)

    # 按场景输出
    for scenario in all_results.keys():
        print(f"\n--- {scenario} ---")
        scenario_df = all_results[scenario].copy()
        formatted = format_results(scenario_df)
        print(formatted.to_string())

    # 模型稳定性分析
    print("\n" + "=" * 70)
    print("【模型跨场景稳定性分析】")
    print("=" * 70)

    stability_data = []
    for model in ["逻辑回归", "SVM", "随机森林", "XGBoost"]:
        model_sharpes = []
        for scenario, df in all_results.items():
            if model in df.index:
                model_sharpes.append(df.loc[model, "夏普比率"])

        if model_sharpes:
            stability_data.append(
                {
                    "模型": model,
                    "夏普均值": np.mean(model_sharpes),
                    "夏普标准差": np.std(model_sharpes),
                    "夏普最小值": np.min(model_sharpes),
                    "夏普最大值": np.max(model_sharpes),
                    "变异系数": np.std(model_sharpes) / np.abs(np.mean(model_sharpes))
                    if np.mean(model_sharpes) != 0
                    else np.inf,
                }
            )

    stability_df = pd.DataFrame(stability_data).set_index("模型")
    print(stability_df.to_string())

    # 最终结论
    print("\n" + "=" * 70)
    print("【最终结论】")
    print("=" * 70)

    best_model = stability_df["夏普均值"].idxmax()
    worst_model = stability_df["夏普均值"].idxmin()
    most_stable = stability_df["变异系数"].idxmin()

    print(
        f"夏普最高的模型: {best_model} (均值={stability_df.loc[best_model, '夏普均值']:.3f})"
    )
    print(
        f"夏普最低的模型: {worst_model} (均值={stability_df.loc[worst_model, '夏普均值']:.3f})"
    )
    print(
        f"最稳定的模型: {most_stable} (变异系数={stability_df.loc[most_stable, '变异系数']:.3f})"
    )

    # 无信号场景的检验
    no_signal_sharpes = []
    for model in ["逻辑回归", "SVM", "随机森林", "XGBoost"]:
        if model in all_results["无因子信号"].index:
            no_signal_sharpes.append(all_results["无因子信号"].loc[model, "夏普比率"])

    avg_no_signal_sharpe = np.mean(no_signal_sharpes)
    print(f"\n无信号场景平均夏普: {avg_no_signal_sharpe:.3f}")
    if abs(avg_no_signal_sharpe) < 0.5:
        print("→ 框架验证通过：无信号时夏普接近0")
    else:
        print("→ 警告：无信号时夏普偏离0，可能存在框架问题")

    return summary_df, stability_df, all_results


if __name__ == "__main__":
    summary_df, stability_df, all_results = main()
