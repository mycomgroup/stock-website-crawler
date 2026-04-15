#!/usr/bin/env python
# coding: utf-8
"""
因子自动搜索主程序
不断尝试新的因子组合，找到最优解
"""

import os
import sys
import json
import csv
import time
from datetime import datetime
from typing import List, Set, Tuple

# 添加当前目录到 path
sys.path.append(os.path.dirname(__file__))

from combination_generator import CombinationGenerator
from evaluator import (
    fetch_data,
    fill_nan_by_date,
    evaluate_factor_combination,
)
from factor_categories import (
    FACTOR_CATEGORIES,
    get_factor_category,
    calculate_diversity_score,
)


# ==================== 配置区 ====================

# 完整因子池（所有类别）
ALL_FACTORS_LIST = []
for category, factors in FACTOR_CATEGORIES.items():
    ALL_FACTORS_LIST.extend(factors)

# 去重
ALL_FACTORS_LIST = list(set(ALL_FACTORS_LIST))

# 已有的高分因子组合（种子）
EXISTING_XX = [
    [
        "inventory_turnover_rate",
        "sales_to_price_ratio",
        "share_turnover_monthly",
        "natural_log_of_market_cap",
    ],
    ["size", "roe_ttm", "TVSTD20", "current_asset_turnover_rate"],
    ["TVMA6", "financial_expense_ttm"],
    ["VOL10", "circulating_market_cap", "single_day_VPT_12"],
    ["money_flow_20", "adjusted_profit_to_total_profit"],
    ["super_quick_ratio", "cube_of_size", "cfo_to_ev"],
]

# 搜索参数
MAX_ITERATIONS = 100  # 最大迭代次数
CONVERGE_THRESHOLD = 1.5  # 进入收敛期的分数阈值
NO_IMPROVE_PATIENCE = 20  # 连续无提升的最大次数
DATA_START_DATE = "2025-01-01"
DATA_END_DATE = "2024-04-15"

# 输出目录
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


# ==================== 主程序 ====================


def load_tried_combinations() -> Set[Tuple[str, ...]]:
    """加载已尝试的组合"""
    tried_file = os.path.join(RESULTS_DIR, "tried_combinations.json")
    if os.path.exists(tried_file):
        with open(tried_file, "r") as f:
            data = json.load(f)
            return set(tuple(item) for item in data)
    return set()


def save_tried_combinations(tried: Set[Tuple[str, ...]]):
    """保存已尝试的组合"""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tried_file = os.path.join(RESULTS_DIR, "tried_combinations.json")
    with open(tried_file, "w") as f:
        json.dump([list(item) for item in tried], f)


def save_score_history(results: List[dict]):
    """保存评分历史"""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    history_file = os.path.join(RESULTS_DIR, "scores_history.csv")

    with open(history_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "iteration",
                "total_score",
                "long_short_return",
                "top_sharpe",
                "ic_mean",
                "icir",
                "ic_win_rate",
                "monotonicity",
                "return_volatility",
                "diversity",
                "strategy",
                "factors",
                "categories",
                "mse",
                "r2",
            ]
        )
        for r in results:
            m = r.get("metrics", {})
            categories = ",".join(
                [f"{f}({r.get('categories', {}).get(f, '?')})" for f in r["factors"]]
            )
            writer.writerow(
                [
                    r["iteration"],
                    r["total_score"],
                    m.get("long_short_return", ""),
                    m.get("top_sharpe", ""),
                    m.get("ic_mean", ""),
                    m.get("icir", ""),
                    m.get("ic_win_rate", ""),
                    m.get("monotonicity", ""),
                    m.get("return_volatility", ""),
                    m.get("diversity", ""),
                    r["strategy"],
                    ",".join(r["factors"]),
                    categories,
                    r.get("mse", ""),
                    r.get("r2", ""),
                ]
            )
        for r in results:
            categories = ",".join(
                [f"{f}({r.get('categories', {}).get(f, '?')})" for f in r["factors"]]
            )
            writer.writerow(
                [
                    r["iteration"],
                    r["adjusted_score"],
                    r.get("base_score", ""),
                    r.get("diversity", ""),
                    r["strategy"],
                    ",".join(r["factors"]),
                    categories,
                    r.get("mse", ""),
                    r.get("r2", ""),
                ]
            )


def save_best_factors(results: List[dict]):
    """保存最优因子组合"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "best_factors.py")

    sorted_results = sorted(results, key=lambda x: x["total_score"], reverse=True)

    with open(output_file, "w") as f:
        f.write("# 最优因子组合（按综合得分排序）\n")
        f.write("xx = []\n\n")
        for r in sorted_results[:20]:
            factors_str = ", ".join([f"'{x}'" for x in r["factors"]])
            m = r.get("metrics", {})
            f.write(
                f"xx.append([{factors_str}])  # total_score = {r['total_score']:.4f}, long_short = {m.get('long_short_return', 0):.4f}, ic = {m.get('ic_mean', 0):.4f}, diversity = {m.get('diversity', 0):.4f}\n"
            )


def print_progress(iteration, score, best_score, strategy, factors, metrics=None):
    """打印进度"""
    print(f"\n{'=' * 60}")
    print(f"Iteration: {iteration}")
    print(f"Strategy: {strategy}")
    print(f"Factors: {factors}")
    if metrics:
        cats = [get_factor_category(f) for f in factors]
        print(f"Categories: {cats}")
        print(f"\n--- 分项指标 ---")
        print(f"分层多空收益: {metrics.get('long_short_return', 0):.4f}")
        print(f"顶层夏普比率: {metrics.get('top_sharpe', 0):.4f}")
        print(f"IC均值: {metrics.get('ic_mean', 0):.4f}")
        print(f"ICIR: {metrics.get('icir', 0):.4f}")
        print(f"IC胜率: {metrics.get('ic_win_rate', 0):.4f}")
        print(f"分层单调性: {metrics.get('monotonicity', 0):.4f}")
        print(f"收益波动率: {metrics.get('return_volatility', 0):.4f}")
        print(f"类别分散度: {metrics.get('diversity', 0):.4f}")
    print(f"\n综合得分: {score:.4f}")
    print(f"当前最优: {best_score:.4f}")
    print(f"{'=' * 60}")


def main():
    print("因子自动搜索程序启动")
    print(f"因子池大小: {len(ALL_FACTORS_LIST)}")
    print(f"种子组合数: {len(EXISTING_XX)}")
    print(f"最大迭代次数: {MAX_ITERATIONS}")

    # 创建输出目录
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 加载已尝试的组合
    tried_combinations = load_tried_combinations()

    # 初始化组合生成器
    generator = CombinationGenerator(
        factor_pool=ALL_FACTORS_LIST,
        existing_combinations=EXISTING_XX,
        tried_combinations=tried_combinations,
    )

    # 获取数据（只获取一次）
    print("\n正在获取数据...")
    all_factors_for_fetch = list(
        set([item for sublist in EXISTING_XX for item in sublist] + ALL_FACTORS_LIST)
    )
    train_data, test_data = fetch_data(
        all_factors_for_fetch,
        start_date=DATA_START_DATE,
        end_date=DATA_END_DATE,
    )

    # 填充 NaN
    print("\n正在处理数据...")
    columns_to_fill = [col for col in ALL_FACTORS_LIST if col in train_data.columns]
    train_data = fill_nan_by_date(train_data, columns_to_fill)
    test_data = fill_nan_by_date(test_data, columns_to_fill)

    X_train = train_data[ALL_FACTORS_LIST]
    X_test = test_data[ALL_FACTORS_LIST]
    y_train = train_data["pchg"]
    y_test = test_data["pchg"]

    # 搜索循环
    results = []
    best_score = -float("inf")
    best_combo = None
    no_improve_count = 0

    print("\n开始搜索...")

    for iteration in range(1, MAX_ITERATIONS + 1):
        # 生成候选组合
        combo, strategy = generator.generate()

        if combo is None:
            print("无新组合可尝试，搜索结束")
            break

        # 评估
        try:
            score, details = evaluate_factor_combination(
                combo, X_train, X_test, y_train, y_test
            )
        except Exception as e:
            print(f"评估失败: {e}")
            continue

        # 记录结果
        result = {
            "iteration": iteration,
            "total_score": score,
            "strategy": strategy,
            "factors": combo,
            "mse": details.get("mse"),
            "r2": details.get("r2"),
            "coefficients": details.get("coefficients"),
            "intercept": details.get("intercept"),
            "categories": details.get("categories"),
            "metrics": details.get("metrics"),
        }
        results.append(result)

        # 更新最优解
        if score > best_score:
            best_score = score
            best_combo = combo
            no_improve_count = 0
            print_progress(
                iteration, score, best_score, strategy, combo, details.get("metrics")
            )
            print("🎉 新最优解！")
        else:
            no_improve_count += 1

        # 更新生成器
        generator.update_best(combo, score, threshold=CONVERGE_THRESHOLD)

        # 定期保存
        if iteration % 5 == 0:
            save_tried_combinations(generator.tried_combinations)
            save_score_history(results)
            save_best_factors(results)

        # 打印进度摘要
        if iteration % 10 == 0:
            stats = generator.get_stats()
            print(f"\n--- 进度摘要 (Iteration {iteration}) ---")
            print(f"阶段: {stats['phase']}")
            print(f"已尝试: {stats['tried_count']} 组合")
            print(f"当前最优: {best_score:.4f}")
            print(f"连续无提升: {no_improve_count}")

        # 检查停止条件
        if no_improve_count >= NO_IMPROVE_PATIENCE:
            print(f"\n连续 {NO_IMPROVE_PATIENCE} 次无提升，搜索结束")
            break

    # 最终保存
    save_tried_combinations(generator.tried_combinations)
    save_score_history(results)
    save_best_factors(results)

    # 打印最终结果
    print("\n" + "=" * 60)
    print("搜索完成！")
    print(f"最终最优分数: {best_score:.4f}")
    print(f"最优因子组合: {best_combo}")
    print(f"总尝试次数: {len(results)}")
    print("=" * 60)

    # 输出 xx.append 格式
    print("\n\n最优因子组合（xx.append 格式）:")
    sorted_results = sorted(results, key=lambda x: x["total_score"], reverse=True)
    for r in sorted_results[:10]:
        factors_str = ", ".join([f"'{x}'" for x in r["factors"]])
        m = r.get("metrics", {})
        print(
            f"xx.append([{factors_str}])  # total_score = {r['total_score']:.4f}, long_short = {m.get('long_short_return', 0):.4f}, ic = {m.get('ic_mean', 0):.4f}"
        )


if __name__ == "__main__":
    main()
