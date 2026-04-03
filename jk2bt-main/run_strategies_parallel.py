"""
并行运行策略脚本
随机选择N个策略，启动N个子Agent并行运行

使用方法:
    python run_strategies_parallel.py --num 10 --start 2020-01-01 --end 2023-12-31
"""

import os
import sys
import random
import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path
import json
import re
import concurrent.futures
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
STRATEGIES_DIR = PROJECT_ROOT / "strategies"
LOGS_DIR = PROJECT_ROOT / "logs" / "strategy_runs"


class RunStatus(Enum):
    """策略运行状态枚举"""
    SUCCESS_WITH_RETURN = "success_with_return"
    SUCCESS_ZERO_RETURN = "success_zero_return"
    SUCCESS_NO_TRADE = "success_no_trade"
    LOAD_FAILED = "load_failed"
    RUN_EXCEPTION = "run_exception"
    TIMEOUT = "timeout"
    DATA_MISSING = "data_missing"
    MISSING_DEPENDENCY = "missing_dependency"
    MISSING_API = "missing_api"
    MISSING_RESOURCE = "missing_resource"
    SKIPPED_NOT_STRATEGY = "skipped_not_strategy"
    SKIPPED_SYNTAX_ERROR = "skipped_syntax_error"
    SKIPPED_NO_INITIALIZE = "skipped_no_initialize"
    SKIPPED_MISSING_API = "skipped_missing_api"


@dataclass
class StrategyRunResult:
    """策略运行结果"""
    strategy: str = ""
    strategy_file: str = ""
    success: bool = False
    run_status: str = ""
    status: str = ""
    start_time: str = ""
    end_time: str = ""
    duration: float = 0.0
    final_value: float = 0.0
    pnl: float = 0.0
    pnl_pct: float = 0.0
    max_drawdown: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    trading_days: int = 0
    error: str = ""
    traceback: str = ""
    exception_type: str = ""
    scan_result: Dict[str, Any] = field(default_factory=dict)
    evidence: Dict[str, Any] = field(default_factory=dict)
    attribution: Dict[str, Any] = field(default_factory=dict)


def _classify_run_status(
    backtest_result: Optional[Dict],
    exception: Optional[Exception],
    has_data: bool,
    scan_result: Optional[Dict],
    evidence: Optional[Dict],
) -> RunStatus:
    """
    根据回测结果和异常分类运行状态

    参数:
        backtest_result: 回测结果字典
        exception: 捕获的异常
        has_data: 是否有数据
        scan_result: 扫描结果
        evidence: 证据字典

    返回:
        RunStatus 枚举值
    """
    from concurrent.futures import TimeoutError

    # 超时检查
    if exception is not None and isinstance(exception, TimeoutError):
        return RunStatus.TIMEOUT

    # 异常分类
    if exception is not None:
        error_str = str(exception).lower()
        error_type = type(exception).__name__

        # 依赖缺失
        if any(kw in error_str for kw in ["module", "import", "no module named", "cannot import"]):
            return RunStatus.MISSING_DEPENDENCY

        # 数据缺失
        if any(kw in error_str for kw in ["数据", "无数据", "股票"]) or "找不到股票" in str(exception):
            return RunStatus.DATA_MISSING

        # API缺失
        if any(kw in str(exception) for kw in ["get_", "attribute", "has no attribute", "not defined", "undefined"]):
            return RunStatus.MISSING_API

        # 资源文件缺失
        if any(kw in error_str for kw in ["file not found", "no such file", "文件不存在", "cannot find"]):
            return RunStatus.MISSING_RESOURCE

        # 其他运行异常
        return RunStatus.RUN_EXCEPTION

    # 无返回结果
    if backtest_result is None:
        if evidence and not evidence.get("loaded", False):
            return RunStatus.LOAD_FAILED
        return RunStatus.LOAD_FAILED

    # 检查证据
    if evidence is None:
        evidence = {}

    loaded = evidence.get("loaded", False)
    entered_backtest_loop = evidence.get("entered_backtest_loop", False)
    has_nav_series = evidence.get("has_nav_series", False)
    has_transactions = evidence.get("has_transactions", False)

    # 成功情况
    if loaded and entered_backtest_loop and has_nav_series:
        pnl_pct = backtest_result.get("pnl_pct", 0) if isinstance(backtest_result, dict) else 0
        if pnl_pct != 0:
            return RunStatus.SUCCESS_WITH_RETURN
        else:
            return RunStatus.SUCCESS_ZERO_RETURN

    if loaded and entered_backtest_loop:
        return RunStatus.SUCCESS_NO_TRADE

    if loaded:
        return RunStatus.SUCCESS_NO_TRADE

    return RunStatus.LOAD_FAILED


def run_single_strategy(
    strategy_file: str,
    start_date: str = "2020-01-01",
    end_date: str = "2023-12-31",
    initial_capital: float = 1000000,
    timeout: int = 600,
    scan_result: Optional[Dict] = None,
) -> StrategyRunResult:
    """
    运行单个策略

    参数:
        strategy_file: 策略文件路径
        start_date: 开始日期
        end_date: 结束日期
        initial_capital: 初始资金
        timeout: 超时时间(秒)
        scan_result: 扫描结果

    返回:
        StrategyRunResult 对象
    """
    import traceback as tb

    strategy_name = os.path.basename(strategy_file)
    start_time = datetime.now()

    result = StrategyRunResult(
        strategy=strategy_name,
        strategy_file=strategy_file,
        start_time=start_time.isoformat(),
        scan_result=scan_result or {},
        evidence={
            "loaded": False,
            "entered_backtest_loop": False,
            "has_transactions": False,
            "has_nav_series": False,
            "nav_series_length": 0,
            "strategy_obj_valid": False,
            "cerebro_valid": False,
        },
        attribution={
            "failure_root_cause": "",
            "missing_dependency": "",
            "missing_api": "",
            "missing_resource_file": "",
            "error_category": "",
            "recoverable": False,
            "recommendation": "",
        },
    )

    exception_caught = None
    backtest_result = None
    has_data = True

    try:
        # 导入运行器
        from jk2bt.core.runner import run_jq_strategy

        backtest_result = run_jq_strategy(
            strategy_file=strategy_file,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            auto_discover_stocks=True,
        )

        if backtest_result is not None:
            result.evidence["loaded"] = True
            result.evidence["strategy_obj_valid"] = backtest_result.get("strategy") is not None
            result.evidence["cerebro_valid"] = backtest_result.get("cerebro") is not None
            result.final_value = backtest_result.get("final_value", 0)
            result.pnl = backtest_result.get("pnl", 0)
            result.pnl_pct = backtest_result.get("pnl_pct", 0)

            strategy = backtest_result.get("strategy")
            if strategy is not None:
                if hasattr(strategy, "navs") and strategy.navs:
                    result.evidence["has_nav_series"] = True
                    result.evidence["nav_series_length"] = len(strategy.navs)
                    result.evidence["entered_backtest_loop"] = True

                if hasattr(strategy, "orders") and strategy.orders:
                    result.evidence["has_transactions"] = len(strategy.orders) > 0
                    if result.evidence["has_transactions"]:
                        result.evidence["entered_backtest_loop"] = True

    except Exception as e:
        exception_caught = e
        result.error = str(e)
        result.traceback = tb.format_exc()
        result.exception_type = type(e).__name__

    end_time = datetime.now()
    result.end_time = end_time.isoformat()
    result.duration = (end_time - start_time).total_seconds()

    # 分类状态
    result.run_status = _classify_run_status(
        backtest_result=backtest_result,
        exception=exception_caught,
        has_data=has_data,
        scan_result=scan_result,
        evidence=result.evidence,
    ).value

    result.success = result.run_status in [
        RunStatus.SUCCESS_WITH_RETURN.value,
        RunStatus.SUCCESS_ZERO_RETURN.value,
        RunStatus.SUCCESS_NO_TRADE.value,
    ]

    return result


def is_valid_strategy_file(filepath):
    """
    检查是否为有效策略文件

    有效策略文件必须包含至少一个策略函数定义
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 必须包含至少一个策略函数
        strategy_funcs = ['initialize', 'handle_data', 'before_trading_start',
                          'after_trading_end', 'before_market_open', 'after_market_close']
        has_func = any(f'def {func}' in content for func in strategy_funcs)

        # 排除纯注释/文档文件
        if not has_func:
            return False

        # 排除只有注释的文件
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
        if len(lines) < 5:  # 太短的文件不太可能是有效策略
            return False

        return True
    except Exception:
        return False


def get_all_strategy_files():
    """获取所有策略文件路径"""
    strategy_files = []
    if STRATEGIES_DIR.exists():
        for f in STRATEGIES_DIR.iterdir():
            if f.suffix == ".txt" and is_valid_strategy_file(f):
                strategy_files.append(str(f))
    return sorted(strategy_files)


def random_pick_strategies(num=10):
    """随机选择N个策略"""
    all_strategies = get_all_strategy_files()
    if len(all_strategies) < num:
        print(f"警告: 只有 {len(all_strategies)} 个策略，无法选择 {num} 个")
        return all_strategies
    return random.sample(all_strategies, num)


def run_single_strategy_subprocess(strategy_file, start_date, end_date, initial_capital=1000000, timeout=600):
    """
    使用子进程运行单个策略

    参数:
        strategy_file: 策略文件路径
        start_date: 开始日期
        end_date: 结束日期
        initial_capital: 初始资金
        timeout: 超时时间（秒）

    返回:
        dict: 包含运行结果
    """
    strategy_name = Path(strategy_file).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = LOGS_DIR / f"{timestamp}_{strategy_name[:30]}"
    log_dir.mkdir(parents=True, exist_ok=True)

    # 构建命令
    cmd = [
        sys.executable,
        "-m",
        "jk2bt.core.runner",
        strategy_file,
        "--start", start_date,
        "--end", end_date,
        "--capital", str(initial_capital),
    ]

    result = {
        "strategy_file": strategy_file,
        "strategy_name": strategy_name,
        "log_dir": str(log_dir),
        "start_time": datetime.now().isoformat(),
        "success": False,
        "final_value": None,
        "pnl": None,
        "pnl_pct": None,
        "error": None,
    }

    try:
        print(f"[启动] {strategy_name}")
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=str(PROJECT_ROOT),
            text=True,
        )

        output, _ = proc.communicate(timeout=timeout)

        # 保存日志
        with open(log_dir / "run.log", "w", encoding="utf-8") as f:
            f.write(output)

        if proc.returncode == 0:
            result["success"] = True
            # 尝试解析结果
            try:
                for line in output.split("\n"):
                    if "最终资金:" in line:
                        result["final_value"] = float(line.split(":")[1].strip().replace(",", ""))
                    if "盈亏:" in line and "%" in line:
                        parts = line.split(":")[1].strip()
                        match = re.search(r"([\d,.-]+)\s+\(([+-]?[\d.]+)%\)", parts)
                        if match:
                            result["pnl"] = float(match.group(1).replace(",", ""))
                            result["pnl_pct"] = float(match.group(2))
            except Exception as e:
                result["error"] = f"解析结果失败: {e}"

            print(f"[完成] {strategy_name} - 成功")
        else:
            # 查找错误信息
            error_lines = []
            for line in output.split("\n"):
                if "Error" in line or "Traceback" in line or "Exception" in line:
                    error_lines.append(line)
            if error_lines:
                result["error"] = "\n".join(error_lines[-3:])[:500]
            else:
                result["error"] = f"未知错误（returncode={proc.returncode}）"
            print(f"[失败] {strategy_name} - {result['error'][:100]}")

    except subprocess.TimeoutExpired:
        proc.kill()
        result["error"] = f"超时 (> {timeout//60}分钟)"
        print(f"[超时] {strategy_name}")
    except Exception as e:
        result["error"] = str(e)
        print(f"[异常] {strategy_name} - {e}")

    result["end_time"] = datetime.now().isoformat()
    return result


def run_strategies_with_agents(strategies, start_date, end_date, initial_capital=1000000, timeout=600):
    """
    使用子进程并行运行多个策略

    参数:
        strategies: 策略文件列表
        start_date: 开始日期
        end_date: 结束日期
        initial_capital: 初始资金
        timeout: 每个策略的超时时间（秒）

    返回:
        list: 所有策略的运行结果
    """
    results = []

    print(f"\n{'='*80}")
    print(f"并行运行 {len(strategies)} 个策略（使用子进程）")
    print(f"回测区间: {start_date} ~ {end_date}")
    print(f"初始资金: {initial_capital}")
    print(f"超时时间: {timeout//60} 分钟")
    print(f"{'='*80}\n")

    # 确保日志目录存在
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # 使用ThreadPoolExecutor来管理子进程
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(strategies)) as executor:
        futures = {
            executor.submit(
                run_single_strategy_subprocess,
                strategy,
                start_date,
                end_date,
                initial_capital,
                timeout,
            ): strategy
            for strategy in strategies
        }

        for future in concurrent.futures.as_completed(futures):
            strategy = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"[异常] {Path(strategy).stem} - {e}")
                results.append({
                    "strategy_file": strategy,
                    "strategy_name": Path(strategy).stem,
                    "success": False,
                    "error": str(e),
                })

    return results


def generate_summary_report(results, output_file=None):
    """生成汇总报告"""
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_strategies": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "results": results,
    }

    # 计算统计信息
    if successful:
        pnls = [r.get("pnl_pct", 0) for r in successful if r.get("pnl_pct") is not None]
        if pnls:
            report["avg_pnl_pct"] = sum(pnls) / len(pnls)
            report["max_pnl_pct"] = max(pnls)
            report["min_pnl_pct"] = min(pnls)

    # 输出到文件
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n报告已保存: {output_file}")

    # 打印摘要
    print(f"\n{'='*80}")
    print("运行汇总")
    print(f"{'='*80}")
    print(f"总数: {len(results)}, 成功: {len(successful)}, 失败: {len(failed)}")

    if successful:
        pnls = [r.get("pnl_pct", 0) for r in successful if r.get("pnl_pct") is not None]
        if pnls:
            print(f"平均收益: {sum(pnls)/len(pnls):.2f}%")
            print(f"最高收益: {max(pnls):.2f}%")
            print(f"最低收益: {min(pnls):.2f}%")

    print("\n成功的策略:")
    for r in successful[:10]:
        pnl_pct = r.get("pnl_pct", "N/A")
        if isinstance(pnl_pct, (int, float)):
            print(f"  {r['strategy_name'][:50]}: {pnl_pct:.2f}%")
        else:
            print(f"  {r['strategy_name'][:50]}: {pnl_pct}")

    if failed:
        print("\n失败的策略:")
        for r in failed[:5]:
            print(f"  {r['strategy_name'][:50]}: {r.get('error', '未知错误')[:50]}")

    print(f"{'='*80}")

    return report


def main():
    parser = argparse.ArgumentParser(description="并行运行多个策略")
    parser.add_argument("--num", type=int, default=10, help="随机选择的策略数量")
    parser.add_argument("--start", default="2020-01-01", help="开始日期")
    parser.add_argument("--end", default="2023-12-31", help="结束日期")
    parser.add_argument("--capital", type=float, default=1000000, help="初始资金")
    parser.add_argument("--timeout", type=int, default=3600, help="每个策略超时时间（秒），默认3600秒（60分钟）")
    parser.add_argument("--strategies", nargs="+", help="指定策略文件路径（不使用随机选择）")
    parser.add_argument("--output", default=None, help="报告输出文件路径")

    args = parser.parse_args()

    # 选择策略
    if args.strategies:
        strategies = args.strategies
        print(f"使用指定的 {len(strategies)} 个策略")
    else:
        strategies = random_pick_strategies(args.num)
        print(f"随机选择 {len(strategies)} 个策略:")
        for s in strategies:
            print(f"  - {Path(s).stem}")

    if not strategies:
        print("错误: 没有找到策略文件")
        return

    # 运行策略
    results = run_strategies_with_agents(
        strategies,
        args.start,
        args.end,
        args.capital,
        args.timeout,
    )

    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = args.output or str(LOGS_DIR / f"{timestamp}_summary.json")
    generate_summary_report(results, output_file)


if __name__ == "__main__":
    main()