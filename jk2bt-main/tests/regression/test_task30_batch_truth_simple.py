#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 30: 跑批真值重跑与策略语义抽检（单进程版本）
基于当前代码重新跑一轮真实策略样本
"""

import os
import sys
import json
import time
import traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))

from run_strategies_parallel import RunStatus
from jk2bt.strategy.scanner import StrategyScanner
from jk2bt.core.runner import run_jq_strategy


def run_single_strategy_simple(
    strategy_file: str,
    start_date: str,
    end_date: str,
    initial_capital: float,
    scan_result: dict,
):
    """运行单个策略（简化版本，不使用多进程）"""
    pass

    strategy_name = os.path.basename(strategy_file)

    result = {
        "strategy": strategy_name,
        "strategy_file": strategy_file,
        "success": False,
        "run_status": RunStatus.LOAD_FAILED.value,
        "status": "",
        "start_time": datetime.now().isoformat(),
        "end_time": "",
        "duration": 0,
        "final_value": 0,
        "pnl": 0,
        "pnl_pct": 0,
        "max_drawdown": 0,
        "annual_return": 0,
        "sharpe_ratio": 0,
        "trading_days": 0,
        "error": "",
        "traceback": "",
        "scan_result": scan_result,
        "exception_type": "",
        "evidence": {
            "loaded": False,
            "entered_backtest_loop": False,
            "has_transactions": False,
            "has_nav_series": False,
            "nav_series_length": 0,
            "strategy_obj_valid": False,
            "cerebro_valid": False,
        },
        "attribution": {
            "failure_root_cause": "",
            "missing_dependency": "",
            "missing_api": "",
            "missing_resource_file": "",
            "error_category": "",
            "recoverable": False,
            "recommendation": "",
        },
    }

    if scan_result and not scan_result.get("is_executable", True):
        result["run_status"] = RunStatus.SKIPPED_NOT_STRATEGY.value
        result["status"] = scan_result.get("error_message", "策略不可执行")
        result["error"] = scan_result.get("error_message", "")
        return result

    start_time = time.time()
    exception_caught = None
    backtest_result = None
    has_data = True

    try:
        if not os.path.exists(strategy_file):
            raise FileNotFoundError(f"策略文件不存在: {strategy_file}")

        print(f"    正在运行: {strategy_name}")

        backtest_result = run_jq_strategy(
            strategy_file=strategy_file,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            auto_discover_stocks=True,
        )

        if backtest_result is None:
            result["run_status"] = RunStatus.LOAD_FAILED.value
            result["status"] = "加载失败 - 无返回结果"
            result["evidence"]["loaded"] = False
            result["attribution"]["failure_root_cause"] = (
                "策略未返回backtest_result对象"
            )
            result["attribution"]["error_category"] = "load_failure"
        else:
            result["evidence"]["loaded"] = True
            result["evidence"]["strategy_obj_valid"] = (
                backtest_result.get("strategy") is not None
            )
            result["evidence"]["cerebro_valid"] = (
                backtest_result.get("cerebro") is not None
            )

            result["final_value"] = backtest_result.get("final_value", 0)
            result["pnl"] = backtest_result.get("pnl", 0)
            result["pnl_pct"] = backtest_result.get("pnl_pct", 0)

            strategy_obj = backtest_result.get("strategy")

            has_navs = False
            try:
                if strategy_obj is not None:
                    has_navs = (
                        hasattr(strategy_obj, "navs")
                        and strategy_obj.navs is not None
                        and len(strategy_obj.navs) > 0
                    )
                if has_navs:
                    result["evidence"]["has_nav_series"] = True
                    result["evidence"]["nav_series_length"] = len(strategy_obj.navs)
                    result["evidence"]["entered_backtest_loop"] = True
            except Exception:
                has_navs = False
                result["evidence"]["has_nav_series"] = False

            cerebro = backtest_result.get("cerebro")
            try:
                if cerebro and hasattr(cerebro.broker, "transactions"):
                    trans_count = len(cerebro.broker.transactions)
                    result["evidence"]["has_transactions"] = trans_count > 0
                    if trans_count > 0:
                        result["evidence"]["entered_backtest_loop"] = True
                        print(f"      交易记录数: {trans_count}")
            except Exception:
                result["evidence"]["has_transactions"] = False

            if not has_navs:
                has_data = False

            if strategy_obj is not None and has_navs:
                import pandas as pd

                nav_series = pd.Series(strategy_obj.navs)

                cummax = nav_series.cummax()
                drawdown = (nav_series - cummax) / cummax
                max_drawdown = drawdown.min()

                days = len(nav_series)
                annual_return = (
                    (result["final_value"] / initial_capital) ** (252 / days) - 1
                    if days > 0
                    else 0
                )

                returns = nav_series.pct_change().dropna()
                sharpe = (
                    returns.mean() / returns.std() * (252**0.5)
                    if returns.std() > 0
                    else 0
                )

                result["max_drawdown"] = float(max_drawdown)
                result["annual_return"] = float(annual_return)
                result["sharpe_ratio"] = float(sharpe)
                result["trading_days"] = days

            print(f"      最终资金: {result['final_value']:,.2f}")
            print(f"      收益率: {result['pnl_pct']:.2f}%")
            print(f"      净值长度: {result['evidence']['nav_series_length']}")

    except Exception as e:
        exception_caught = e
        error_str = str(e)
        error_type = type(e).__name__

        result["error"] = error_str
        result["traceback"] = traceback.format_exc()
        result["exception_type"] = error_type

        print(f"      ✗ 异常: {error_type}: {error_str[:100]}")

        result["attribution"]["error_category"] = "runtime_exception"

        if "数据" in error_str or "无数据" in error_str or "股票" in error_str:
            result["run_status"] = RunStatus.DATA_MISSING.value
            result["status"] = "数据缺失导致跳过"
            result["attribution"]["failure_root_cause"] = "数据缺失"
            result["attribution"]["error_category"] = "data_missing"
            result["attribution"]["recoverable"] = True
            result["attribution"]["recommendation"] = (
                "补充缺失的数据文件或调整回测时间段"
            )

        elif any(
            dep in error_str.lower()
            for dep in ["module", "import", "no module named", "cannot import"]
        ):
            result["run_status"] = RunStatus.MISSING_DEPENDENCY.value
            result["status"] = "依赖缺失"
            result["attribution"]["failure_root_cause"] = "Python依赖包缺失"
            result["attribution"]["missing_dependency"] = error_str
            result["attribution"]["error_category"] = "dependency_missing"
            result["attribution"]["recoverable"] = True
            result["attribution"]["recommendation"] = (
                "安装缺失的Python包: pip install <package>"
            )

        elif any(
            api in error_str
            for api in [
                "get_",
                "attribute",
                "has no attribute",
                "not defined",
                "undefined",
            ]
        ):
            if scan_result and scan_result.get("missing_apis"):
                result["run_status"] = RunStatus.MISSING_API.value
                result["status"] = f"API缺失: {', '.join(scan_result['missing_apis'])}"
                result["attribution"]["failure_root_cause"] = "聚宽API未实现"
                result["attribution"]["missing_api"] = ", ".join(
                    scan_result["missing_apis"]
                )
                result["attribution"]["error_category"] = "api_missing"
                result["attribution"]["recoverable"] = True
                result["attribution"]["recommendation"] = (
                    "在utility中实现缺失的API或修改策略代码"
                )
            else:
                result["run_status"] = RunStatus.MISSING_API.value
                result["status"] = f"API/属性缺失: {error_type}"
                result["attribution"]["failure_root_cause"] = "API或属性未实现/未定义"
                result["attribution"]["missing_api"] = error_str
                result["attribution"]["error_category"] = "api_missing"
                result["attribution"]["recoverable"] = True
                result["attribution"]["recommendation"] = (
                    "检查策略使用的API是否在utility中已实现"
                )

        elif any(
            res in error_str.lower()
            for res in ["file not found", "no such file", "文件不存在", "cannot find"]
        ):
            result["run_status"] = RunStatus.MISSING_RESOURCE.value
            result["status"] = "资源文件缺失"
            result["attribution"]["failure_root_cause"] = "外部资源文件缺失"
            result["attribution"]["missing_resource_file"] = error_str
            result["attribution"]["error_category"] = "resource_missing"
            result["attribution"]["recoverable"] = True
            result["attribution"]["recommendation"] = "补充缺失的数据文件或调整策略代码"

        else:
            result["run_status"] = RunStatus.RUN_EXCEPTION.value
            result["status"] = f"运行异常: {error_type}"
            result["attribution"]["failure_root_cause"] = (
                f"{error_type}: {error_str[:100]}"
            )
            result["attribution"]["error_category"] = "runtime_exception"
            result["attribution"]["recoverable"] = False
            result["attribution"]["recommendation"] = (
                "查看详细错误日志，分析具体异常原因"
            )

    finally:
        end_time = time.time()
        duration = end_time - start_time
        result["end_time"] = datetime.now().isoformat()
        result["duration"] = round(duration, 2)

        if backtest_result is not None and exception_caught is None:
            if (
                result["evidence"]["loaded"]
                and result["evidence"]["entered_backtest_loop"]
            ):
                if result["evidence"]["has_nav_series"]:
                    if result.get("pnl_pct", 0) != 0:
                        result["run_status"] = RunStatus.SUCCESS_WITH_RETURN.value
                        result["success"] = True
                        result["status"] = "运行成功有收益"
                    else:
                        result["run_status"] = RunStatus.SUCCESS_ZERO_RETURN.value
                        result["success"] = True
                        result["status"] = "运行成功零收益"
                else:
                    result["run_status"] = RunStatus.SUCCESS_NO_TRADE.value
                    result["success"] = True
                    result["status"] = "运行成功无交易"
            else:
                result["run_status"] = RunStatus.SUCCESS_NO_TRADE.value
                result["success"] = True
                result["status"] = "运行成功无交易"

        status_mark = "✓" if result["success"] else "✗"
        print(f"      {status_mark} 完成: {result['status']} ({result['run_status']})")

    return result


def select_test_samples():
    """选择多样化的测试样本"""
    strategy_dir = "jkcode/jkcode"

    test_samples = {
        "likely_success": [
            "03 一个简单而持续稳定的懒人超额收益策略.txt",
        ],
        "likely_no_trade": [
            "04 红利搬砖，年化29%.txt",
            "04 高股息低市盈率高增长的价投策略.txt",
        ],
        "likely_missing_api": [
            "01 龙回头3.0回测速度优化版.txt",
            "02 7年40倍绩优低价超跌缩量小盘 扩容到50只.txt",
        ],
        "likely_syntax_error": [
            "100 配套资料说明.txt",
        ],
        "likely_complex_strategy": [
            "01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt",
            "03 多策略融合-80倍.txt",
        ],
    }

    strategy_files = []
    categories = {}

    for category, samples in test_samples.items():
        for sample in samples:
            path = os.path.join(strategy_dir, sample)
            if os.path.exists(path):
                strategy_files.append(path)
                categories[sample] = category

    return strategy_files, categories


def semantic_check(result):
    """对成功样本进行语义抽检"""
    checks = {
        "loaded": result.get("evidence", {}).get("loaded", False),
        "entered_backtest_loop": result.get("evidence", {}).get(
            "entered_backtest_loop", False
        ),
        "has_transactions": result.get("evidence", {}).get("has_transactions", False),
        "has_nav_series": result.get("evidence", {}).get("has_nav_series", False),
        "nav_series_length": result.get("evidence", {}).get("nav_series_length", 0),
        "strategy_obj_valid": result.get("evidence", {}).get(
            "strategy_obj_valid", False
        ),
        "cerebro_valid": result.get("evidence", {}).get("cerebro_valid", False),
    }

    semantic_status = "unknown"

    if (
        checks["loaded"]
        and checks["entered_backtest_loop"]
        and checks["has_nav_series"]
    ):
        if checks["has_transactions"] and checks["nav_series_length"] > 0:
            if result.get("pnl_pct", 0) != 0:
                semantic_status = "real_success_with_return"
            else:
                semantic_status = "real_success_zero_return"
        else:
            semantic_status = "real_success_no_trade"
    elif checks["loaded"] and not checks["entered_backtest_loop"]:
        semantic_status = "pseudo_success_no_loop"
    elif not checks["loaded"]:
        semantic_status = "pseudo_success_not_loaded"

    return checks, semantic_status


def analyze_results(summary, categories):
    """分析结果并生成报告"""
    results = summary.get("results", [])

    analysis = {
        "total": len(results),
        "categories": {},
        "semantic_checks": {},
        "status_distribution": {},
        "attribution": {},
    }

    for status, count in summary["summary"]["status_counts"].items():
        analysis["status_distribution"][status] = count

    for result in results:
        strategy_name = result["strategy"]
        category = categories.get(strategy_name, "unknown")
        run_status = result.get("run_status", "unknown")

        if category not in analysis["categories"]:
            analysis["categories"][category] = []
        analysis["categories"][category].append(
            {
                "strategy": strategy_name,
                "run_status": run_status,
                "success": result.get("success", False),
                "pnl_pct": result.get("pnl_pct", 0),
            }
        )

        if result.get("success", False):
            checks, semantic_status = semantic_check(result)
            analysis["semantic_checks"][strategy_name] = {
                "checks": checks,
                "semantic_status": semantic_status,
                "pnl_pct": result.get("pnl_pct", 0),
                "nav_length": checks["nav_series_length"],
            }

        attribution = result.get("attribution", {})
        if attribution.get("failure_root_cause"):
            analysis["attribution"][strategy_name] = {
                "root_cause": attribution.get("failure_root_cause", ""),
                "error_category": attribution.get("error_category", ""),
                "recoverable": attribution.get("recoverable", False),
                "recommendation": attribution.get("recommendation", ""),
            }

    return analysis


def main():
    print("=" * 80)
    print("Task 30: 跑批真值重跑与策略语义抽检（单进程版本）")
    print("=" * 80)
    print(f"时间: {datetime.now().isoformat()}")
    print()

    strategy_files, categories = select_test_samples()

    print(f"选择测试样本数: {len(strategy_files)}")
    print("\n样本分类:")
    for category, samples in categories.items():
        print(f"  {samples}: {category}")
    print()

    scanner = StrategyScanner()
    print("开始策略扫描...")

    scan_results_map = {}
    executable_files = []
    skipped_files = []

    for strategy_file in strategy_files:
        scan_result = scanner.scan_file(strategy_file)
        scan_results_map[strategy_file] = {
            "status": scan_result.status.value,
            "is_executable": scan_result.is_executable,
            "has_initialize": scan_result.has_initialize,
            "has_handle": scan_result.has_handle,
            "missing_apis": scan_result.missing_apis,
            "error_message": scan_result.error_message,
        }

        if scan_result.is_executable:
            executable_files.append(strategy_file)
            print(f"  ✓ {os.path.basename(strategy_file)}")
        else:
            skipped_files.append(strategy_file)
            print(f"  ✗ {os.path.basename(strategy_file)}: {scan_result.error_message}")

    print(f"\n扫描完成: 可执行 {len(executable_files)}，跳过 {len(skipped_files)}")
    print()

    print("开始运行策略...")
    print()

    results = []

    for i, strategy_file in enumerate(executable_files, 1):
        print(f"[{i}/{len(executable_files)}] {os.path.basename(strategy_file)}")

        scan_result_dict = scan_results_map.get(strategy_file, {})

        result = run_single_strategy_simple(
            strategy_file=strategy_file,
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
            scan_result=scan_result_dict,
        )

        results.append(result)
        print()

    for skipped_file in skipped_files:
        scan_result = scan_results_map.get(skipped_file, {})
        results.append(
            {
                "strategy": os.path.basename(skipped_file),
                "strategy_file": skipped_file,
                "success": False,
                "run_status": RunStatus.SKIPPED_NOT_STRATEGY.value,
                "status": scan_result.get("error_message", "策略不可执行"),
                "duration": 0,
                "scan_result": scan_result,
                "evidence": {
                    "loaded": False,
                    "entered_backtest_loop": False,
                    "has_transactions": False,
                    "has_nav_series": False,
                    "nav_series_length": 0,
                    "strategy_obj_valid": False,
                    "cerebro_valid": False,
                },
                "attribution": {
                    "failure_root_cause": scan_result.get(
                        "error_message", "策略不可执行"
                    ),
                    "error_category": "scan_rejected",
                    "recoverable": False,
                    "recommendation": "检查策略文件是否符合策略格式要求",
                },
            }
        )

    status_counts = {}
    for r in results:
        rs = r.get("run_status", "unknown")
        status_counts[rs] = status_counts.get(rs, 0) + 1

    success_with_return = status_counts.get(RunStatus.SUCCESS_WITH_RETURN.value, 0)
    success_zero_return = status_counts.get(RunStatus.SUCCESS_ZERO_RETURN.value, 0)
    success_no_trade = status_counts.get(RunStatus.SUCCESS_NO_TRADE.value, 0)
    total_success = success_with_return + success_zero_return + success_no_trade

    load_failed = status_counts.get(RunStatus.LOAD_FAILED.value, 0)
    run_exception = status_counts.get(RunStatus.RUN_EXCEPTION.value, 0)
    timeout_count = status_counts.get(RunStatus.TIMEOUT.value, 0)
    data_missing = status_counts.get(RunStatus.DATA_MISSING.value, 0)
    missing_dependency = status_counts.get(RunStatus.MISSING_DEPENDENCY.value, 0)
    missing_api = status_counts.get(RunStatus.MISSING_API.value, 0)
    missing_resource = status_counts.get(RunStatus.MISSING_RESOURCE.value, 0)
    skipped_not_strategy = status_counts.get(RunStatus.SKIPPED_NOT_STRATEGY.value, 0)
    total_failed = len(results) - total_success

    recoverable_failures = 0
    for r in results:
        if r.get("attribution", {}).get("recoverable", False):
            recoverable_failures += 1

    summary = {
        "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().isoformat(),
        "scan_summary": {
            "total": len(strategy_files),
            "executable": len(executable_files),
            "skipped": len(skipped_files),
            "details": scan_results_map,
        },
        "summary": {
            "input_total": len(strategy_files),
            "run_total": len(executable_files),
            "skipped_total": len(skipped_files),
            "success_with_return": success_with_return,
            "success_zero_return": success_zero_return,
            "success_no_trade": success_no_trade,
            "success_total": total_success,
            "load_failed": load_failed,
            "run_exception": run_exception,
            "timeout": timeout_count,
            "data_missing": data_missing,
            "missing_dependency": missing_dependency,
            "missing_api": missing_api,
            "missing_resource": missing_resource,
            "skipped_not_strategy": skipped_not_strategy,
            "failed_total": total_failed,
            "recoverable_failures": recoverable_failures,
            "unrecoverable_failures": total_failed - recoverable_failures,
            "status_counts": status_counts,
        },
        "results": results,
    }

    print("=" * 80)
    print("结果分析")
    print("=" * 80)

    analysis = analyze_results(summary, categories)

    print(f"\n总策略数: {analysis['total']}")
    print(f"\n状态分布:")
    for status, count in analysis["status_distribution"].items():
        print(f"  {status}: {count}")

    print(f"\n按预期分类的结果:")
    for category, results_list in analysis["categories"].items():
        print(f"\n  {category} ({len(results_list)}个):")
        for r in results_list:
            status_mark = "✓" if r["success"] else "✗"
            print(
                f"    {status_mark} {r['strategy']} - {r['run_status']} - 收益率: {r['pnl_pct']:.2f}%"
            )

    if analysis["semantic_checks"]:
        print(f"\n成功样本语义抽检:")
        for strategy, check_data in analysis["semantic_checks"].items():
            print(f"\n  {strategy}:")
            print(f"    语义状态: {check_data['semantic_status']}")
            print(f"    收益率: {check_data['pnl_pct']:.2f}%")
            print(f"    净值长度: {check_data['nav_length']}")
            checks = check_data["checks"]
            print(f"    证据:")
            for key, value in checks.items():
                print(f"      {key}: {value}")

    if analysis["attribution"]:
        print(f"\n失败样本归因分析:")
        for strategy, attr_data in analysis["attribution"].items():
            print(f"\n  {strategy}:")
            print(f"    根本原因: {attr_data['root_cause']}")
            print(f"    错误类别: {attr_data['error_category']}")
            print(f"    可恢复: {attr_data['recoverable']}")
            if attr_data["recommendation"]:
                print(f"    建议: {attr_data['recommendation']}")

    print("\n" + "=" * 80)
    print("验证完成")
    print("=" * 80)

    output_dir = "docs/0330_result"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "task30_batch_truth_and_replay_result.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "summary": summary,
                "analysis": analysis,
                "categories": categories,
                "timestamp": datetime.now().isoformat(),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )
    print(f"\n结果已保存到: {output_file}")

    return summary, analysis


if __name__ == "__main__":
    summary, analysis = main()
