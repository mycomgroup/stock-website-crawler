#!/usr/bin/env python3
"""
问财公式回测自动研究系统 - 单次迭代执行器 (A/B/C/D pipeline)

对 formula_config.json 执行一次变异，然后依次执行：
A. 方向确认（recent_6m / recent_12m）
B. 粗搜索（受限变异）
C. 邻域稳健测试
D. 多窗口确认（recent_6m / recent_12m / prior_12m / full_24m）
"""

import argparse
import copy
import json
import math
import random
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from scorer import (
    ParsedMetrics,
    calculate_complexity,
    calculate_robust_score_multi_window,
    calculate_score,
    calculate_score_delta,
    check_hard_constraints,
    classify_direction_status,
    parse_backtest_result,
)
from formula_mutator import (
    ConditionTemplateEngine,
    MUTATION_TYPES,
    mutate,
    record_mutation_reward,
    validate_config,
)
from formula_executor import run_backtest_windows

from tree_profile import load_tree_profile_from_dir, get_primary_families, get_secondary_families, check_promotion_rules, get_param_penalty, is_param_preferred
from condition_catalog import get_addable_conditions


WINDOWS_RECENT = ["recent_6m", "recent_12m"]
WINDOWS_FULL = ["recent_6m", "recent_12m", "prior_12m", "full_24m"]
TSV_HEADER = "iter\tbacktest_id\tstatus\tannual_return\tmax_drawdown\tsharpe\tscore\tdecision\tmutation\trobust_score\trecent6\trecent12\tprior12\tfull24\tsensitivity\ttrade_count\tcomplexity\treason\n"
A_VALUE_COARSE_MUTATIONS = ["coarse_threshold_adjust", "adjust_max_positions", "simplify_formula"]
A_VALUE_FINE_MUTATIONS = ["fine_threshold_adjust", "adjust_max_positions", "simplify_formula"]
SKILL_ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def git_commit(base: Path, message: str) -> bool:
    try:
        subprocess.run(["git", "add", "."], cwd=base, check=True, capture_output=True)
        result = subprocess.run(["git", "commit", "-m", message], cwd=base, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            return False
        print(f"[git] commit 失败: {result.stderr}", flush=True)
        return False
    except subprocess.CalledProcessError as e:
        print(f"[git] add 失败: {e}", flush=True)
        return False
    except Exception as e:
        print(f"[git] 异常: {e}", flush=True)
        return False


def git_restore(base: Path, filename: str) -> bool:
    try:
        result = subprocess.run(["git", "checkout", "HEAD", filename], cwd=base, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"[git] restore 失败: {e}", flush=True)
        return False


def append_tsv(base: Path, row: dict) -> None:
    tsv = base / "iterations.tsv"
    write_header = not tsv.exists()
    line = (
        "\t".join(
            [
                str(row.get("iter", "")),
                str(row.get("backtest_id", "")),
                str(row.get("status", "")),
                f"{row.get('annual_return', 0):.4f}",
                f"{row.get('max_drawdown', 0):.4f}",
                f"{row.get('sharpe', 0):.4f}",
                f"{row.get('score', 0):.6f}",
                str(row.get("decision", "")),
                str(row.get("mutation", "")),
                f"{row.get('robust_score', 0):.6f}",
                f"{row.get('recent6', 0):.6f}",
                f"{row.get('recent12', 0):.6f}",
                f"{row.get('prior12', 0):.6f}",
                f"{row.get('full24', 0):.6f}",
                f"{row.get('sensitivity', 0):.4f}",
                str(row.get("trade_count", "")),
                str(row.get("complexity", "")),
                str(row.get("reason", "")),
            ]
        )
        + "\n"
    )
    with open(tsv, "a", encoding="utf-8") as f:
        if write_header:
            f.write(TSV_HEADER)
        f.write(line)


def build_metrics_snapshot(metrics: ParsedMetrics) -> dict:
    return {
        "annual_return": metrics.annual_return,
        "max_drawdown": metrics.max_drawdown,
        "sortino": metrics.sortino,
        "information_ratio": metrics.information_ratio,
        "win_rate": metrics.win_rate,
        "trade_count": metrics.trade_count,
        "sharpe": metrics.sharpe,
        "avg_holding_days": metrics.avg_holding_days,
    }


def infer_recommendation(direction_status: str, stable_param_ranges: dict) -> str:
    if direction_status == "INACTIVE":
        return "停止深挖，当前方向近期失效。"
    if stable_param_ranges:
        return "继续跟踪 champion，并优先在稳定参数带内微调。"
    if direction_status == "WATCH":
        return "保持观察，只做有限粗搜索，不扩展复杂条件。"
    return "方向仍活着，继续粗搜索。"


def update_state(
    state: dict,
    base: Path,
    iter_n: int,
    decision: str,
    score: float,
    robust_score: Optional[float] = None,
    extra_updates: Optional[dict] = None,
) -> None:
    state["current_iter"] = iter_n + 1
    state["last_update"] = datetime.now().isoformat()

    if decision == "keep":
        state["champion_score"] = score
        if robust_score is not None:
            state["champion_robust_score"] = robust_score
        state["consecutive_failures"] = 0
    elif decision in {"rollback", "crash"}:
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1

    if extra_updates:
        state.update(extra_updates)

    save_json(base / "state.json", state)


def compute_sensitivity_score(neighbor_scores: list[float]) -> float:
    if len(neighbor_scores) < 2:
        return 0.0

    mean_score = sum(neighbor_scores) / len(neighbor_scores)
    if abs(mean_score) < 0.01:
        mean_score = 0.01

    variance = sum((s - mean_score) ** 2 for s in neighbor_scores) / len(neighbor_scores)
    std_score = math.sqrt(variance)
    return std_score / abs(mean_score)


def normalize_number(value: float):
    rounded = round(value, 4)
    if abs(rounded - round(rounded)) < 1e-9:
        return int(round(rounded))
    return rounded


def replace_last_numeric_token(clause: str, new_value: float) -> str:
    matches = list(re.finditer(r"\d+(?:\.\d+)?", clause))
    if not matches:
        return clause
    last = matches[-1]
    replacement = str(normalize_number(new_value))
    return clause[: last.start()] + replacement + clause[last.end() :]


def is_a_value_experiment(base: Path) -> bool:
    return "trees/A_value/" in str(base)


def choose_mutation_type(base: Path, state: dict, requested_type: Optional[str], tree_name: Optional[str] = None) -> Optional[str]:
    """选择变异类型，基于树配置和当前状态进行上下文感知选择"""
    if requested_type:
        return requested_type
    
    phase = state.get("phase", "coarse_search")
    
    if tree_name:
        profile = load_tree_profile_from_dir(tree_name)
        if profile:
            primary = get_primary_families(profile)
            secondary = get_secondary_families(profile)
            allowed = profile.get("search_space", {}).get("allowed_actions", [])
            
            action_map = {
                "add": "add_formula_condition",
                "remove": "remove_formula_condition",
                "replace": "replace_formula_condition",
                "sort": "adjust_formula_sort",
                "coarse_adjust": "coarse_threshold_adjust",
                "fine_adjust": "fine_threshold_adjust",
            }
            
            allowed_mutation_types = [action_map.get(a, a) for a in allowed if a in action_map]
            
            if not allowed_mutation_types:
                allowed_mutation_types = ["coarse_threshold_adjust", "fine_threshold_adjust", "add_formula_condition"]
            
            if phase == "coarse_search":
                preferred = ["coarse_threshold_adjust", "add_formula_condition", "replace_formula_condition", "adjust_formula_sort"]
            else:
                preferred = ["fine_threshold_adjust", "replace_formula_condition", "adjust_formula_sort", "simplify_formula"]
            
            candidates = [m for m in allowed_mutation_types if m in preferred]
            if not candidates:
                candidates = allowed_mutation_types
            
            return random.choice(candidates)
    
    if not is_a_value_experiment(base):
        return None
    
    pool = A_VALUE_COARSE_MUTATIONS if phase == "coarse_search" else A_VALUE_FINE_MUTATIONS
    return random.choice(pool)


def combine_mutation_summary(user_summary: str, mutation_desc: str) -> str:
    user_summary = (user_summary or "").strip()
    if not user_summary:
        return mutation_desc
    if user_summary == mutation_desc:
        return mutation_desc
    return f"{user_summary} | {mutation_desc}"


def extract_numeric_formula_map(config: dict) -> dict[str, dict]:
    engine = ConditionTemplateEngine()
    numeric_map = {}
    for idx, clause in enumerate(config.get("formula", [])):
        parsed = engine.parse_condition(clause)
        if parsed and "value" in parsed:
            numeric_map[parsed["condition_name"]] = {
                "idx": idx,
                "clause": clause,
                "value": parsed["value"],
                "condition_name": parsed["condition_name"],
            }
    return numeric_map


def detect_changed_targets(old_config: dict, new_config: dict) -> list[dict]:
    engine = ConditionTemplateEngine()
    old_numeric = extract_numeric_formula_map(old_config)
    new_numeric = extract_numeric_formula_map(new_config)
    targets = []

    for condition_name, info in new_numeric.items():
        old_info = old_numeric.get(condition_name)
        if old_info and abs(old_info["value"] - info["value"]) > 1e-9:
            step = engine.get_step_size(condition_name, fine_tuning=True)
            targets.append(
                {
                    "kind": "formula",
                    "label": f"formula:{condition_name}",
                    "idx": info["idx"],
                    "name": condition_name,
                    "current": info["value"],
                    "step": step,
                    "clause": info["clause"],
                }
            )

    for param in ["maxPositions", "takeProfit", "stopLoss", "trailingStopLoss"]:
        old_val = old_config.get(param)
        new_val = new_config.get(param)
        if old_val != new_val and new_val is not None:
            step = {
                "maxPositions": 2,
                "takeProfit": 5,
                "stopLoss": 2,
                "trailingStopLoss": 2,
            }.get(param, 1)
            targets.append(
                {
                    "kind": "param",
                    "label": param,
                    "name": param,
                    "current": new_val,
                    "step": step,
                }
            )

    return targets


def build_neighbor_configs(champion_config: dict, candidate_config: dict) -> list[tuple[str, float, dict, float]]:
    engine = ConditionTemplateEngine()
    targets = detect_changed_targets(champion_config, candidate_config)
    neighbor_configs: list[tuple[str, float, dict, float]] = []
    seen = set()

    def add_neighbor(label: str, value: float, config: dict, current: float) -> None:
        key = json.dumps(config, sort_keys=True, ensure_ascii=False)
        if key in seen:
            return
        seen.add(key)
        neighbor_configs.append((label, value, config, current))

    for target in targets:
        if target["kind"] == "formula":
            template = engine.INDICATOR_TEMPLATES.get(target["name"], {})
            low, high = template.get("range", [0, 9999])
            step = max(float(target.get("step", 1)), 0.1)
            for delta in (-step, step):
                new_value = max(low, min(high, float(target["current"]) + delta))
                if abs(new_value - float(target["current"])) < 1e-9:
                    continue
                neighbor = copy.deepcopy(candidate_config)
                formula = list(neighbor.get("formula", []))
                formula[target["idx"]] = replace_last_numeric_token(target["clause"], new_value)
                neighbor["formula"] = formula
                add_neighbor(target["label"], normalize_number(new_value), neighbor, target["current"])
        else:
            param = target["name"]
            current = float(target["current"])
            if param == "maxPositions":
                candidate_values = sorted({5, 6, 8, 10, int(current), max(4, int(current) - 2), int(current) + 2})
                for value in candidate_values:
                    if value == int(current):
                        continue
                    neighbor = copy.deepcopy(candidate_config)
                    neighbor[param] = value
                    add_neighbor(param, value, neighbor, current)
            else:
                for delta in (-float(target["step"]), float(target["step"])):
                    value = current + delta
                    floor = 0 if param == "trailingStopLoss" else 1
                    value = max(floor, value)
                    if abs(value - current) < 1e-9:
                        continue
                    neighbor = copy.deepcopy(candidate_config)
                    neighbor[param] = normalize_number(value)
                    add_neighbor(param, normalize_number(value), neighbor, current)

    if neighbor_configs:
        return neighbor_configs

    # 没识别到本轮核心改动时，回退到保守的参数邻域
    base_take_profit = candidate_config.get("takeProfit", 20)
    base_stop_loss = candidate_config.get("stopLoss", 10)
    base_trailing_stop = candidate_config.get("trailingStopLoss", 6)
    base_max_positions = candidate_config.get("maxPositions", 8)

    for param, current, deltas in [
        ("takeProfit", float(base_take_profit), [-5, 5]),
        ("stopLoss", float(base_stop_loss), [-2, 2]),
        ("trailingStopLoss", float(base_trailing_stop), [-2, 2]),
    ]:
        for delta in deltas:
            value = max(0 if param == "trailingStopLoss" else 1, current + delta)
            neighbor = copy.deepcopy(candidate_config)
            neighbor[param] = normalize_number(value)
            add_neighbor(param, normalize_number(value), neighbor, current)

    for value in sorted({5, 6, 8, 10, int(base_max_positions)}):
        if value == int(base_max_positions):
            continue
        neighbor = copy.deepcopy(candidate_config)
        neighbor["maxPositions"] = value
        add_neighbor("maxPositions", value, neighbor, float(base_max_positions))

    return neighbor_configs


def build_window_score_map(metrics_by_window: dict[str, ParsedMetrics], config: dict) -> dict[str, float]:
    complexity = calculate_complexity(config)
    return {
        window_name: calculate_score(metrics, complexity=complexity, config=config)
        for window_name, metrics in metrics_by_window.items()
    }


def stage1_direction_check(
    config: dict,
    base: Path,
    iter_id: str,
    baseline_scores: dict,
) -> tuple[bool, str, str, dict, dict, dict]:
    print(f"[iter_{iter_id}] [STAGE A] Direction Check - recent_6m / recent_12m", flush=True)
    results = run_backtest_windows(config, windows=WINDOWS_RECENT, experiment_dir=base)

    metrics_by_window = {}
    for window_name in WINDOWS_RECENT:
        metrics = parse_backtest_result(results.get(window_name, {}), window_name=window_name)
        metrics_by_window[window_name] = metrics

    score_map = build_window_score_map(metrics_by_window, config)
    direction_status, direction_reason, env_slack = classify_direction_status(
        score_map.get("recent_6m", 0.0),
        score_map.get("recent_12m", 0.0),
        baseline_scores,
    )

    print(
        f"[iter_{iter_id}] [STAGE A] recent_6m={score_map.get('recent_6m', 0):.4f} "
        f"recent_12m={score_map.get('recent_12m', 0):.4f} status={direction_status} slack={env_slack:.4f}",
        flush=True,
    )

    should_continue = direction_status != "INACTIVE"
    return should_continue, direction_status, direction_reason, results, metrics_by_window, score_map


def compute_stable_param_ranges(anchor_score: float, probes: list[dict]) -> dict:
    if not probes:
        return {}

    neighbor_slack = max(0.15, 0.12 * abs(anchor_score))
    grouped: dict[str, list[dict]] = {}
    for probe in probes:
        if probe["score"] >= anchor_score - neighbor_slack:
            grouped.setdefault(probe["label"], []).append(probe)

    ranges = {}
    for label, entries in grouped.items():
        current = entries[0]["current"]
        values = [entry["value"] for entry in entries] + [current]
        key = label.replace("formula:", "")
        ranges[key] = {
            "kind": "formula_threshold" if label.startswith("formula:") else "parameter",
            "lower": normalize_number(min(values)),
            "upper": normalize_number(max(values)),
            "current": normalize_number(current),
            "tested": len(entries),
        }
    return ranges


def stage2_sensitivity_probe(
    champion_config: dict,
    candidate_config: dict,
    base: Path,
    iter_id: str,
    anchor_score: float,
) -> tuple[bool, float, list[float], dict, str]:
    print(f"[iter_{iter_id}] [STAGE C] Sensitivity Probe - 测试邻域参数", flush=True)
    neighbor_configs = build_neighbor_configs(champion_config, candidate_config)

    if not neighbor_configs:
        return True, 0.0, [], {}, "无邻域配置可测试，暂按通过"

    probes = []
    neighbor_scores = []
    for label, value, neighbor_config, current in neighbor_configs:
        if not validate_config(neighbor_config):
            continue
        try:
            result = run_backtest_windows(neighbor_config, windows=["recent_12m"], experiment_dir=base).get("recent_12m", {})
            metrics = parse_backtest_result(result, window_name="recent_12m")
            score = calculate_score(metrics, complexity=calculate_complexity(neighbor_config), config=neighbor_config)
            neighbor_scores.append(score)
            probes.append({"label": label, "value": value, "score": score, "current": current})
            print(f"[iter_{iter_id}] [STAGE C] {label}={value}: score={score:.4f}", flush=True)
        except Exception as e:
            print(f"[iter_{iter_id}] [STAGE C] {label}={value} 回测失败: {e}", flush=True)

    if len(neighbor_scores) < 3:
        stable_ranges = compute_stable_param_ranges(anchor_score, probes)
        return True, 0.0, neighbor_scores, stable_ranges, "邻域样本不足，暂按通过"

    sensitivity = compute_sensitivity_score(neighbor_scores)
    neighbor_slack = max(0.15, 0.12 * abs(anchor_score))
    floor_slack = max(0.25, 0.20 * abs(anchor_score))
    good_ratio = sum(1 for s in neighbor_scores if s >= anchor_score - neighbor_slack) / len(neighbor_scores)
    floor_ok = min(neighbor_scores) >= anchor_score - floor_slack
    is_stable = good_ratio >= 0.6 and floor_ok and sensitivity <= 0.6

    stable_ranges = compute_stable_param_ranges(anchor_score, probes) if is_stable else {}
    reason = (
        f"good_ratio={good_ratio:.2f}, floor_ok={floor_ok}, sensitivity={sensitivity:.4f}, "
        f"anchor={anchor_score:.4f}"
    )
    print(f"[iter_{iter_id}] [STAGE C] {reason} stable={is_stable}", flush=True)
    return is_stable, sensitivity, neighbor_scores, stable_ranges, reason


def stage3_multi_window_confirm(
    config: dict,
    base: Path,
    iter_id: str,
    neighbor_scores: list[float],
) -> tuple[dict, dict, dict, float, Optional[ParsedMetrics], float]:
    print(f"[iter_{iter_id}] [STAGE D] Multi-Window Confirm - 运行完整多窗口回测", flush=True)
    results_by_window = run_backtest_windows(config, windows=WINDOWS_FULL, experiment_dir=base)

    metrics_by_window = {}
    for window_name in WINDOWS_FULL:
        metrics = parse_backtest_result(results_by_window.get(window_name, {}), window_name=window_name)
        metrics_by_window[window_name] = metrics
        print(
            f"[iter_{iter_id}] [STAGE D] {window_name}: annual={metrics.annual_return:.2%} "
            f"dd={metrics.max_drawdown:.2%} trades={metrics.trade_count}",
            flush=True,
        )

    score_map = build_window_score_map(metrics_by_window, config)
    robust_score = calculate_robust_score_multi_window(metrics_by_window, neighbor_scores=neighbor_scores, config=config)
    primary_metrics = metrics_by_window.get("recent_12m") or metrics_by_window.get("recent_6m")
    primary_score = score_map.get("recent_12m", score_map.get("recent_6m", 0.0))

    print(
        f"[iter_{iter_id}] [STAGE D] robust_score={robust_score:.4f} primary_score={primary_score:.4f}",
        flush=True,
    )
    return results_by_window, metrics_by_window, score_map, robust_score, primary_metrics, primary_score


def decide_keep_rollback_robust(
    new_robust_score: float,
    champion_robust_score: float,
    new_single_score: float,
    champion_single_score: float,
    config: dict,
    champion_config: Optional[dict],
    epsilon_absolute: float = 0.15,
    epsilon_relative: float = 0.03,
) -> tuple[str, str]:
    if champion_robust_score in (float("-inf"), -1e308):
        return "keep", "first version, automatically champion"

    score_diff = new_robust_score - champion_robust_score
    relative_diff = score_diff / abs(champion_robust_score) if champion_robust_score != 0 else 0.0
    if score_diff >= epsilon_absolute or relative_diff >= epsilon_relative:
        return "keep", (
            f"robust_score {new_robust_score:.4f} > champion {champion_robust_score:.4f} "
            f"(diff={score_diff:.4f}, relative={relative_diff:.2%})"
        )

    new_complexity = calculate_complexity(config)
    champion_complexity = calculate_complexity(champion_config or {}) if champion_config else 10**9
    if new_complexity < champion_complexity and abs(score_diff) < epsilon_absolute and new_single_score >= champion_single_score - 0.02:
        return "keep", (
            f"scores close and new config simpler ({new_complexity} < {champion_complexity})"
        )

    return "rollback", f"robust_score {new_robust_score:.4f} <= champion {champion_robust_score:.4f} (diff={score_diff:.4f})"


def resolve_experiment_base(base_arg: str) -> Path:
    raw = Path(base_arg).expanduser()
    candidates = []
    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.append((Path.cwd() / raw).resolve())
        candidates.append((SKILL_ROOT / raw).resolve())

    seen = set()
    unique_candidates = []
    for candidate in candidates:
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            unique_candidates.append(candidate)

    for candidate in unique_candidates:
        if (candidate / "state.json").exists() and (candidate / "formula_config.json").exists():
            return candidate

    return unique_candidates[0] if unique_candidates else raw


def main() -> None:
    parser = argparse.ArgumentParser(description="问财公式回测单次迭代执行器")
    parser.add_argument("--base", required=True, help="实验目录路径（含 state.json 和 formula_config.json）")
    parser.add_argument("--mutation-summary", required=True, help="本轮变异的描述（人类可读）")
    parser.add_argument(
        "--mutation-type",
        default=None,
        help=f"变异类型（可选），不指定时随机选择。可选值: {', '.join(MUTATION_TYPES)}",
    )
    args = parser.parse_args()

    base = resolve_experiment_base(args.base)
    state_path = base / "state.json"
    formula_config_path = base / "formula_config.json"
    if not state_path.exists() or not formula_config_path.exists():
        print(f"[ERROR] 缺少 state.json 或 formula_config.json: {base}", flush=True)
        print(f"[ERROR] 原始 --base 参数: {args.base}", flush=True)
        sys.exit(2)

    state = load_json(state_path)
    champion_config = load_json(formula_config_path)
    iter_n = state.get("current_iter", 1)
    iter_id = f"{iter_n:04d}"

    tree_name = None
    base_str = str(base)
    for tree_candidate in ["A_value", "B_quality_growth", "C_small_cap", "D_mispricing_reversal",
                           "E_technical_trend", "F_fund_flow", "G_event_driven", "H_composite", "I_portfolio_risk"]:
        if f"trees/{tree_candidate}" in base_str:
            tree_name = tree_candidate
            break

    print(f"[iter_{iter_id}] 开始迭代", flush=True)

    champion_score = float(state.get("champion_score", float("-inf")))
    champion_robust_score = float(state.get("champion_robust_score", float("-inf")))
    baseline_scores = state.get("baseline_window_scores") or {
        "recent_6m": state.get("champion_windows", {}).get("recent_6m", {}).get("score", 0.0),
        "recent_12m": state.get("champion_windows", {}).get("recent_12m", {}).get("score", 0.0),
    }

    champion_metrics_data = state.get("champion_metrics", {})
    champion_metrics = None
    if champion_metrics_data:
        champion_metrics = ParsedMetrics(
            status="completed",
            backtest_id="",
            total_return=champion_metrics_data.get("annual_return", 0.0),
            annual_return=champion_metrics_data.get("annual_return", 0.0),
            max_drawdown=champion_metrics_data.get("max_drawdown", 0.0),
            sharpe=champion_metrics_data.get("sharpe", 0.0),
            sortino=champion_metrics_data.get("sortino", 0.0),
            information_ratio=champion_metrics_data.get("information_ratio", 0.0),
            win_rate=champion_metrics_data.get("win_rate", 0.0),
            trade_count=champion_metrics_data.get("trade_count", 0),
            max_positions=champion_config.get("maxPositions", 0),
            daily_buy_count=champion_config.get("dailyBuyCount", 0),
            avg_holding_days=champion_metrics_data.get("avg_holding_days", 0.0),
            window_name="recent_12m",
        )

    metrics = None
    robust_score = 0.0
    sensitivity = 0.0
    backtest_id = ""
    score = 0.0
    score_map = {"recent_6m": 0.0, "recent_12m": 0.0, "prior_12m": 0.0, "full_24m": 0.0}
    stable_param_ranges = {}
    direction_status = state.get("direction_status", "UNKNOWN")
    reason = ""
    mutation_type = choose_mutation_type(base, state, args.mutation_type, tree_name)
    actual_mutation_type = mutation_type or "random"

    try:
        new_config, mutation_desc, actual_mutation_type = mutate(champion_config, mutation_type, tree_name=tree_name)
        mutation_record = combine_mutation_summary(args.mutation_summary, mutation_desc)
        print(f"[iter_{iter_id}] 变异描述: {mutation_record}", flush=True)

        if new_config == champion_config:
            append_tsv(
                base,
                {
                    "iter": iter_id,
                    "status": "no_change",
                    "decision": "rollback",
                    "mutation": mutation_record,
                    "reason": "mutation produced no effective change",
                },
            )
            update_state(state, base, iter_n, "rollback", champion_score, champion_robust_score)
            sys.exit(1)

        if not validate_config(new_config):
            print(f"[iter_{iter_id}] [ERROR] 变异后的配置不合法", flush=True)
            sys.exit(2)

        save_json(formula_config_path, new_config)
        print(f"[iter_{iter_id}] formula_config.json 已更新为新配置（待验证）", flush=True)

        stage1_pass, direction_status, stage1_reason, stage1_results, _, recent_score_map = stage1_direction_check(
            new_config,
            base,
            iter_id,
            baseline_scores,
        )
        score_map.update(recent_score_map)

        stage1_primary = parse_backtest_result(stage1_results.get("recent_12m", {}), window_name="recent_12m")
        if not stage1_pass:
            git_restore(base, "formula_config.json")
            append_tsv(
                base,
                {
                    "iter": iter_id,
                    "backtest_id": stage1_results.get("recent_12m", {}).get("backtest_id", ""),
                    "status": "stage_a_fail",
                    "annual_return": stage1_primary.annual_return,
                    "max_drawdown": stage1_primary.max_drawdown,
                    "sharpe": stage1_primary.sharpe,
                    "score": score_map.get("recent_12m", 0.0),
                    "decision": "rollback",
                    "mutation": mutation_record,
                    "robust_score": 0.0,
                    "recent6": score_map.get("recent_6m", 0.0),
                    "recent12": score_map.get("recent_12m", 0.0),
                    "sensitivity": 0.0,
                    "trade_count": stage1_primary.trade_count,
                    "complexity": calculate_complexity(new_config),
                    "reason": f"{direction_status}: {stage1_reason}",
                },
            )
            update_state(
                state,
                base,
                iter_n,
                "rollback",
                champion_score,
                champion_robust_score,
                extra_updates={
                    "stop_reason": "direction inactive candidate" if state.get("consecutive_failures", 0) + 1 >= 8 else state.get("stop_reason", ""),
                },
            )
            print(f"[iter_{iter_id}] rollback — {direction_status}: {stage1_reason}", flush=True)
            sys.exit(1)

        is_stable, sensitivity, neighbor_scores, stable_param_ranges, stage2_reason = stage2_sensitivity_probe(
            champion_config,
            new_config,
            base,
            iter_id,
            score_map.get("recent_12m", 0.0),
        )
        if not is_stable:
            git_restore(base, "formula_config.json")
            append_tsv(
                base,
                {
                    "iter": iter_id,
                    "backtest_id": stage1_results.get("recent_12m", {}).get("backtest_id", ""),
                    "status": "stage_c_fail",
                    "annual_return": stage1_primary.annual_return,
                    "max_drawdown": stage1_primary.max_drawdown,
                    "sharpe": stage1_primary.sharpe,
                    "score": score_map.get("recent_12m", 0.0),
                    "decision": "rollback",
                    "mutation": mutation_record,
                    "robust_score": 0.0,
                    "recent6": score_map.get("recent_6m", 0.0),
                    "recent12": score_map.get("recent_12m", 0.0),
                    "sensitivity": sensitivity,
                    "trade_count": stage1_primary.trade_count,
                    "complexity": calculate_complexity(new_config),
                    "reason": stage2_reason,
                },
            )
            update_state(state, base, iter_n, "rollback", champion_score, champion_robust_score)
            print(f"[iter_{iter_id}] rollback — {stage2_reason}", flush=True)
            sys.exit(1)

        results_by_window, metrics_by_window, full_score_map, robust_score, metrics, score = stage3_multi_window_confirm(
            new_config,
            base,
            iter_id,
            neighbor_scores,
        )
        score_map.update(full_score_map)

        for window_result in results_by_window.values():
            if isinstance(window_result, dict) and window_result.get("backtest_id"):
                backtest_id = window_result.get("backtest_id", "")
                break

        profile = load_tree_profile_from_dir(tree_name) if tree_name else None
        if profile and not check_promotion_rules(new_config.get("formula", []), profile):
            decision = "rollback"
            reason = f"未满足 {tree_name} 的 promotion_rules"
        else:
            hard_pass, _, hard_reason = check_hard_constraints(
                metrics_by_window,
                champion_robust_score=champion_robust_score,
                config=new_config,
            )
            if not hard_pass:
                decision = "rollback"
                reason = hard_reason
            else:
                param_penalty = 0.0
                if profile:
                    for param in ["maxPositions", "takeProfit", "stopLoss", "trailingStopLoss"]:
                        if param in new_config:
                            param_penalty += get_param_penalty(profile, param, new_config[param])
                    param_penalty *= 0.05

                adjusted_robust_score = robust_score - param_penalty
                adjusted_champion_robust = champion_robust_score

                decision, reason = decide_keep_rollback_robust(
                    new_robust_score=adjusted_robust_score,
                    champion_robust_score=adjusted_champion_robust,
                    new_single_score=score,
                    champion_single_score=champion_score,
                    config=new_config,
                    champion_config=champion_config,
                    epsilon_absolute=0.15,
                    epsilon_relative=0.03,
                )

                if param_penalty > 0.01:
                    reason = f"{reason} (param_penalty={param_penalty:.3f})"

        reward_base = champion_robust_score if champion_robust_score not in (float("-inf"), -1e308) else champion_score
        reward_score = robust_score if champion_robust_score not in (float("-inf"), -1e308) else score
        record_mutation_reward(actual_mutation_type, calculate_score_delta(reward_score, reward_base))

        complexity = calculate_complexity(new_config)
        param_penalty_display = 0.0
        if profile:
            for param in ["maxPositions", "takeProfit", "stopLoss", "trailingStopLoss"]:
                if param in new_config:
                    param_penalty_display += get_param_penalty(profile, param, new_config[param])
            param_penalty_display *= 0.05

        print(
            f"[iter_{iter_id}] score={score:.4f} robust_score={robust_score:.4f} "
            f"param_penalty={param_penalty_display:.3f} "
            f"champion_score={champion_score:.4f} champion_robust={champion_robust_score:.4f} "
            f"direction={direction_status} sensitivity={sensitivity:.4f}",
            flush=True,
        )
        print(f"[iter_{iter_id}] 决策: {decision} — {reason}", flush=True)

        append_tsv(
            base,
            {
                "iter": iter_id,
                "backtest_id": backtest_id,
                "status": metrics.status if metrics else "unknown",
                "annual_return": metrics.annual_return if metrics else 0.0,
                "max_drawdown": metrics.max_drawdown if metrics else 0.0,
                "sharpe": metrics.sharpe if metrics else 0.0,
                "score": score,
                "decision": decision,
                "mutation": mutation_record,
                "robust_score": robust_score,
                "recent6": score_map.get("recent_6m", 0.0),
                "recent12": score_map.get("recent_12m", 0.0),
                "prior12": score_map.get("prior_12m", 0.0),
                "full24": score_map.get("full_24m", 0.0),
                "sensitivity": sensitivity,
                "trade_count": metrics.trade_count if metrics else 0,
                "complexity": complexity,
                "reason": reason,
            },
        )

        if decision == "keep":
            window_snapshot = {
                window_name: {
                    "score": score_map.get(window_name, 0.0),
                    **build_metrics_snapshot(metrics_by_window[window_name]),
                }
                for window_name in WINDOWS_FULL
            }
            next_phase = "fine_search" if direction_status == "ACTIVE" and stable_param_ranges else state.get("phase", "coarse_search")
            update_state(
                state,
                base,
                iter_n,
                "keep",
                score,
                robust_score,
                extra_updates={
                    "direction_status": direction_status,
                    "direction_reason": stage1_reason,
                    "phase": next_phase,
                    "champion_metrics": build_metrics_snapshot(metrics),
                    "champion_windows": window_snapshot,
                    "stable_param_ranges": stable_param_ranges,
                    "last_keep_reason": reason,
                    "last_mutation_type": actual_mutation_type,
                    "final_recommendation": infer_recommendation(direction_status, stable_param_ranges),
                    "stop_reason": "",
                    "param_penalty": param_penalty_display,
                },
            )

            git_msg = (
                f"keep: iter_{iter_id} score={score:.4f} robust={robust_score:.4f} "
                f"direction={direction_status} sensitivity={sensitivity:.4f}\n{mutation_record}"
            )
            git_commit(base, git_msg)
            print(f"[iter_{iter_id}] keep — 新 champion score={score:.4f} robust={robust_score:.4f}", flush=True)
            sys.exit(0)

        git_restore(base, "formula_config.json")
        update_state(
            state,
            base,
            iter_n,
            "rollback",
            champion_score,
            champion_robust_score,
            extra_updates={
                "stop_reason": "连续失败较多，建议暂停自动探索。" if state.get("consecutive_failures", 0) + 1 >= 8 else state.get("stop_reason", ""),
            },
        )
        print(f"[iter_{iter_id}] rollback — {reason}（不 commit）", flush=True)
        sys.exit(1)

    except Exception as e:
        crash_reason = f"{type(e).__name__}: {e}"
        print(f"[iter_{iter_id}] [CRASH] {crash_reason}", flush=True)

        try:
            append_tsv(
                base,
                {
                    "iter": iter_id,
                    "backtest_id": backtest_id,
                    "status": "crash",
                    "annual_return": metrics.annual_return if metrics else 0.0,
                    "max_drawdown": metrics.max_drawdown if metrics else 0.0,
                    "sharpe": metrics.sharpe if metrics else 0.0,
                    "score": score,
                    "decision": "crash",
                    "mutation": args.mutation_summary,
                    "robust_score": robust_score,
                    "recent6": score_map.get("recent_6m", 0.0),
                    "recent12": score_map.get("recent_12m", 0.0),
                    "prior12": score_map.get("prior_12m", 0.0),
                    "full24": score_map.get("full_24m", 0.0),
                    "sensitivity": sensitivity,
                    "trade_count": metrics.trade_count if metrics else 0,
                    "complexity": calculate_complexity(load_json(formula_config_path)) if formula_config_path.exists() else 0,
                    "reason": crash_reason,
                },
            )
        except Exception as write_err:
            print(f"[iter_{iter_id}] [CRASH] 写 crash 记录失败: {write_err}", flush=True)

        try:
            git_restore(base, "formula_config.json")
        except Exception:
            pass

        try:
            update_state(
                state,
                base,
                iter_n,
                "crash",
                champion_score,
                champion_robust_score,
                extra_updates={"stop_reason": crash_reason},
            )
        except Exception as state_err:
            print(f"[iter_{iter_id}] [CRASH] 更新 state.json 失败: {state_err}", flush=True)

        sys.exit(2)


if __name__ == "__main__":
    main()
