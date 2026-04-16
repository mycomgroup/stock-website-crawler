#!/usr/bin/env python3
"""
setup.py - ML弱因子搜索实验初始化（独立实现）

目标：
1) 初始化实验目录
2) 从200个因子中预筛选120个优质因子
3) 生成防过拟合版 strategy.py 模板（包含预筛选后的因子）
4) 运行 baseline
5) 生成 search_notes.md / program.md
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from factor_categories import FACTOR_TO_CATEGORY, calculate_diversity_score

AUTORESEARCH_DIR = Path(__file__).parent
TEMPLATE_FILE = AUTORESEARCH_DIR / "strategy_template.py"


def _load_template() -> str:
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(f"策略模板文件不存在: {TEMPLATE_FILE}")
    return TEMPLATE_FILE.read_text(encoding="utf-8")


def _load_all_factors() -> list[str]:
    """加载所有200个因子"""
    try:
        from skills.autoresearch_ml_joinquant_factor.factor_categories import (
            FACTOR_CATEGORIES,
        )
    except Exception:
        import importlib.util
        import sys

        root = Path(__file__).resolve().parent
        module_path = root / "factor_categories.py"
        spec = importlib.util.spec_from_file_location("factor_categories", module_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["factor_categories"] = mod
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        FACTOR_CATEGORIES = mod.FACTOR_CATEGORIES

    factors: list[str] = []
    for group in FACTOR_CATEGORIES.values():
        factors.extend(group)

    seen: set[str] = set()
    dedup: list[str] = []
    for f in factors:
        if f not in seen:
            dedup.append(f)
            seen.add(f)
    return dedup


def prescreen_factors_simple(
    all_factors: list[str],
    target_count: int = 120,
    min_diversity: float = 0.5
) -> list[str]:
    """
    简化的因子预筛选：从200个因子中筛选出120个
    
    由于在初始化时没有历史数据，我们使用以下策略：
    1. 确保因子类别多样性（每个类别至少选一定数量）
    2. 优先选择常见的重要因子
    3. 避免过度集中在某一类别
    """
    if len(all_factors) <= target_count:
        return all_factors
    
    # 按类别分组因子
    factor_by_category = {}
    for factor in all_factors:
        category = FACTOR_TO_CATEGORY.get(factor, "unknown")
        if category not in factor_by_category:
            factor_by_category[category] = []
        factor_by_category[category].append(factor)
    
    # 计算每个类别应该选择的最小因子数量
    # 确保每个类别至少有1个因子，但不超过其因子数量的50%
    category_min_counts = {}
    for category, factors in factor_by_category.items():
        # 每个类别至少1个，最多不超过因子数量的30%
        min_count = max(1, min(5, int(len(factors) * 0.3)))
        category_min_counts[category] = min_count
    
    # 计算最小总数
    total_min = sum(category_min_counts.values())
    
    # 如果最小总数已经超过目标数量，需要调整
    if total_min > target_count:
        # 按比例缩减
        scale = target_count / total_min
        for category in category_min_counts:
            category_min_counts[category] = max(1, int(category_min_counts[category] * scale))
        total_min = sum(category_min_counts.values())
    
    # 第一轮：选择每个类别的最小数量
    selected_factors = []
    for category, factors in factor_by_category.items():
        min_count = category_min_counts.get(category, 1)
        # 选择该类别中的前min_count个因子
        selected_factors.extend(factors[:min_count])
    
    # 如果已经达到或超过目标数量，返回前target_count个
    if len(selected_factors) >= target_count:
        selected_factors = selected_factors[:target_count]
        diversity = calculate_diversity_score(selected_factors)
        print(f"[预筛选] 从 {len(all_factors)} 个因子中筛选出 {len(selected_factors)} 个因子")
        print(f"[预筛选] 多样性得分: {diversity:.3f}")
        return selected_factors
    
    # 第二轮：按类别大小比例分配剩余名额
    remaining_slots = target_count - len(selected_factors)
    category_weights = {}
    
    for category, factors in factor_by_category.items():
        # 已经选过的数量
        already_selected = len([f for f in selected_factors if FACTOR_TO_CATEGORY.get(f) == category])
        # 还可以选择的数量
        available = len(factors) - already_selected
        if available > 0:
            # 权重 = 类别大小 * (1 - 已选比例)
            selected_ratio = already_selected / len(factors) if len(factors) > 0 else 0
            weight = len(factors) * (1 - selected_ratio)
            category_weights[category] = weight
    
    total_weight = sum(category_weights.values())
    
    if total_weight > 0:
        for category, weight in category_weights.items():
            # 按权重比例分配名额
            allocate = max(1, int(remaining_slots * weight / total_weight))
            factors = factor_by_category[category]
            
            # 已经选过的
            already_selected = [f for f in selected_factors if FACTOR_TO_CATEGORY.get(f) == category]
            available_factors = [f for f in factors if f not in already_selected]
            
            # 选择因子
            to_select = min(allocate, len(available_factors))
            selected_factors.extend(available_factors[:to_select])
    
    # 如果还不够，从所有剩余因子中按类别均匀选择
    if len(selected_factors) < target_count:
        remaining = [f for f in all_factors if f not in selected_factors]
        need = target_count - len(selected_factors)
        
        # 按类别分组剩余因子
        remaining_by_category = {}
        for factor in remaining:
            category = FACTOR_TO_CATEGORY.get(factor, "unknown")
            if category not in remaining_by_category:
                remaining_by_category[category] = []
            remaining_by_category[category].append(factor)
        
        # 轮询选择，确保多样性
        while len(selected_factors) < target_count and remaining:
            for category, factors in remaining_by_category.items():
                if factors:
                    selected_factors.append(factors.pop(0))
                    if len(selected_factors) >= target_count:
                        break
                if len(selected_factors) >= target_count:
                    break
    
    # 确保不重复且数量正确
    selected_factors = list(dict.fromkeys(selected_factors))
    selected_factors = selected_factors[:target_count]
    
    # 计算多样性得分
    diversity = calculate_diversity_score(selected_factors)
    print(f"[预筛选] 从 {len(all_factors)} 个因子中筛选出 {len(selected_factors)} 个因子")
    print(f"[预筛选] 多样性得分: {diversity:.3f}")
    
    # 输出类别分布
    category_counts = {}
    for factor in selected_factors:
        category = FACTOR_TO_CATEGORY.get(factor, "unknown")
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("[预筛选] 类别分布:")
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} 个因子")
    
    return selected_factors


DEFAULT_SEED_FACTORS = [
    ["size", "roe_ttm", "momentum", "liquidity"],
    ["sales_to_price_ratio", "cfo_to_ev", "cube_of_size"],
    ["TVSTD20", "VOL20", "residual_volatility"],
]


def _default_dates() -> tuple[str, str]:
    today = datetime.today()
    end = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    start = (today - timedelta(days=365 * 6 + 30)).strftime("%Y-%m-%d")
    return start, end


DEFAULT_START, DEFAULT_END = _default_dates()


def parse_seed_factors(seed_factors: str | None) -> list[list[str]]:
    if not seed_factors:
        return DEFAULT_SEED_FACTORS
    try:
        parsed = ast.literal_eval(seed_factors)
        if isinstance(parsed, list) and parsed:
            return parsed
    except Exception:
        pass
    print("[警告] seed-factors 解析失败，回退默认值")
    return DEFAULT_SEED_FACTORS


def generate_search_notes(
    seed_factors: list[list[str]],
    start_date: str,
    end_date: str,
    pool: str,
    baseline: float,
    top_k: int,
) -> str:
    top = seed_factors[0] if seed_factors else []
    top_k_seed = seed_factors[: max(1, top_k)]
    lines = []
    for i, factors in enumerate(top_k_seed, start=1):
        score = baseline if i == 1 else 0.0
        lines.append(f"| {i} | {score:.4f} | {factors} | seed | 0 |")
    pool_table = "\n".join(lines) if lines else "| 1 | 0.0000 | [] | seed | 0 |"
    return f"""## 当前状态
- best_score: {baseline:.4f}
- best_factors: {top}
- current_iter: 0
- top_k: {top_k}

## 回测配置
- 日期范围: {start_date} ~ {end_date}
- 选股池: {pool}

## 风险守则
- [x] 因子去相关后再组合
- [x] 标签严格使用 t -> t+1 对齐
- [x] 动态缩放必须平滑
- [x] 交易成本必须入分数

## 多策略池（Top-K）
| rank | score | factors | source | iter |
|------|-------|---------|--------|------|
{pool_table}

## 搜索地图

### 已验证有效（keep）
（初始化为空）

### 已验证无效（rollback）
（初始化为空）

### 待探索方向
- [ ] 从高分组合变异，替换单个因子
- [ ] 随机采样新组合（多样性优先）
- [ ] 频率优先采样
- [ ] 组合不同类别因子（分散度优先）

## 最近一轮候选结果
| idx | score | factors | success |
|-----|-------|---------|---------|
"""


def run_baseline(strategy_file: Path, notebook_dir: str | None):
    from notebook_executor import execute_strategy

    print("[baseline] start")
    result = execute_strategy(
        str(strategy_file), timeout_ms=600_000, notebook_dir=notebook_dir
    )
    if result.get("success"):
        return float(result.get("score", 0.0)), result
    print(f"[baseline] failed: {result.get('error')}")
    return 0.0, result


def main():
    parser = argparse.ArgumentParser(description="初始化 ML 弱因子 JoinQuant 实验目录")
    parser.add_argument("--name", required=True, help="实验名称")
    parser.add_argument(
        "--start-date", default=DEFAULT_START, help=f"默认 {DEFAULT_START}"
    )
    parser.add_argument("--end-date", default=DEFAULT_END, help=f"默认 {DEFAULT_END}")
    parser.add_argument(
        "--pool",
        default="small",
        choices=["small", "HS300", "ZZ500", "ZZ800"],
        help="选股池",
    )
    parser.add_argument("--seed-factors", default=None, help="二维列表字符串")
    parser.add_argument("--notebook-dir", default=None, help="joinquant notebook 目录")
    
    # 新增参数：是否启用因子预筛选
    parser.add_argument(
        "--prescreen",
        action="store_true",
        default=True,
        help="启用因子预筛选（200→120）"
    )
    parser.add_argument(
        "--target-factors",
        type=int,
        default=120,
        help="预筛选后保留的因子数量（默认120）"
    )

    parser.add_argument(
        "--ic-window", type=int, default=26, help="IC rolling窗口（周频约半年）"
    )
    parser.add_argument(
        "--cluster-count", type=int, default=20, help="聚类簇数（预留参数）"
    )
    parser.add_argument("--weight-smooth", type=float, default=0.8, help="权重平滑系数")
    parser.add_argument("--buy-cost-bps", type=float, default=15.0, help="买入成本bp")
    parser.add_argument("--sell-cost-bps", type=float, default=15.0, help="卖出成本bp")
    parser.add_argument("--slippage-bps", type=float, default=5.0, help="滑点bp")
    parser.add_argument("--top-k", type=int, default=5, help="保留前K组策略")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d")
    exp_name = f"strategy_autoresearch_ml_factor_{args.name}_{ts}"
    exp_dir = AUTORESEARCH_DIR / exp_name

    if exp_dir.exists():
        print(f"[错误] 目录已存在: {exp_dir}")
        sys.exit(1)

    exp_dir.mkdir(parents=True)
    subprocess.run(["git", "init"], cwd=str(exp_dir), capture_output=True)

    # 步骤1：加载所有因子并进行预筛选
    print("[setup] 加载所有因子...")
    all_factors = _load_all_factors()
    print(f"[setup] 共加载 {len(all_factors)} 个因子")
    
    if args.prescreen:
        print(f"[setup] 开始因子预筛选（目标: {args.target_factors} 个）...")
        screened_factors = prescreen_factors_simple(
            all_factors, 
            target_count=args.target_factors
        )
        print(f"[setup] 预筛选完成: {len(all_factors)} → {len(screened_factors)} 个因子")
        
        # 使用预筛选后的因子作为种子
        seeds = [screened_factors]
    else:
        # 使用默认种子因子
        seeds = parse_seed_factors(args.seed_factors)
        print(f"[setup] 使用默认种子因子: {len(seeds[0])} 个因子")

    # 步骤2：生成策略文件
    strategy_file = exp_dir / "strategy.py"
    strategy_content = _load_template()
    
    # 使用预筛选后的因子替换模板中的 {factors}
    strategy_content = strategy_content.replace("{factors}", repr(seeds[0]))
    strategy_content = strategy_content.replace("{start_date}", args.start_date)
    strategy_content = strategy_content.replace("{end_date}", args.end_date)
    strategy_content = strategy_content.replace("{pool}", args.pool)
    strategy_content = strategy_content.replace("{ic_window}", str(args.ic_window))
    strategy_content = strategy_content.replace(
        "{cluster_count}", str(args.cluster_count)
    )
    strategy_content = strategy_content.replace(
        "{weight_smooth}", str(args.weight_smooth)
    )
    strategy_content = strategy_content.replace(
        "{buy_cost_bps}", str(args.buy_cost_bps)
    )
    strategy_content = strategy_content.replace(
        "{sell_cost_bps}", str(args.sell_cost_bps)
    )
    strategy_content = strategy_content.replace(
        "{slippage_bps}", str(args.slippage_bps)
    )
    strategy_file.write_text(strategy_content, encoding="utf-8")

    subprocess.run(["git", "add", "strategy.py"], cwd=str(exp_dir), capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "iter_0000_baseline: init ml weak-factor strategy"],
        cwd=str(exp_dir),
        capture_output=True,
    )

    # 步骤3：复制程序文档
    src_program = AUTORESEARCH_DIR / "program.md"
    if src_program.exists():
        (exp_dir / "program.md").write_text(
            src_program.read_text(encoding="utf-8"), encoding="utf-8"
        )

    # 步骤4：运行baseline
    baseline_score, baseline_result = run_baseline(strategy_file, args.notebook_dir)

    # 步骤5：生成搜索笔记
    notes = generate_search_notes(
        seeds,
        args.start_date,
        args.end_date,
        args.pool,
        baseline_score,
        max(1, args.top_k),
    )
    (exp_dir / "search_notes.md").write_text(notes, encoding="utf-8")

    # 步骤6：保存种子配置
    (exp_dir / "seed_config.json").write_text(
        json.dumps(
            {
                "seed_factors": seeds,
                "all_factors_count": len(all_factors),
                "screened_factors_count": len(seeds[0]) if args.prescreen else None,
                "prescreen_enabled": args.prescreen,
                "target_factors": args.target_factors,
                "start_date": args.start_date,
                "end_date": args.end_date,
                "pool": args.pool,
                "ic_window": args.ic_window,
                "cluster_count": args.cluster_count,
                "weight_smooth": args.weight_smooth,
                "buy_cost_bps": args.buy_cost_bps,
                "sell_cost_bps": args.sell_cost_bps,
                "slippage_bps": args.slippage_bps,
                "top_k": max(1, args.top_k),
                "baseline_result": baseline_result,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # 步骤7：初始化策略池
    init_pool = []
    for i, combo in enumerate(seeds[: max(1, args.top_k)], start=1):
        init_pool.append(
            {
                "rank": i,
                "score": baseline_score if i == 1 else 0.0,
                "factors": combo,
                "source": "prescreen" if args.prescreen else "seed",
                "iter": 0,
            }
        )
    (exp_dir / "strategy_pool.json").write_text(
        json.dumps(init_pool, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 步骤8：保存预筛选报告
    if args.prescreen:
        prescreen_report = {
            "total_factors": len(all_factors),
            "screened_factors": len(seeds[0]),
            "screened_factor_list": seeds[0],
            "screening_method": "simple_diversity_based",
            "target_count": args.target_factors,
            "timestamp": datetime.now().isoformat(),
        }
        (exp_dir / "prescreen_report.json").write_text(
            json.dumps(prescreen_report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[setup] 预筛选报告已保存: {exp_dir}/prescreen_report.json")

    print("[setup] 完成")
    print(f"[setup] 实验目录: {exp_dir}")
    print(f"[setup] 策略文件: {strategy_file}")
    print(f"[setup] 使用因子数量: {len(seeds[0])}")
    if args.prescreen:
        print(f"[setup] 预筛选比例: {len(seeds[0])}/{len(all_factors)} = {len(seeds[0])/len(all_factors)*100:.1f}%")


if __name__ == "__main__":
    main()