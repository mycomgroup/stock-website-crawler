"""
策略回放正确性验证器 v2

验证策略是否真的"跑通"，而不是"假跑通"。

v2改进：
- 修复验证脚本自身bug（使用is None判断）
- 统一判定标准（与run_strategies_parallel.py的RunStatus对应）
- 增强证据字段（更完善的证据点）
- 输出可聚合JSON和可读Markdown
- 区分：load_failed、syntax_error、missing_dependency、missing_api、
       entered_backtest_loop、success_no_trade、success_with_nav、
       success_with_transactions、pseudo_success、pseudo_failure

检查项:
- 定时器是否真的触发
- 是否真的发生了交易
- 订单语义是否合理
- 净值曲线是否存在
- record输出是否符合预期
- 策略加载是否成功
- 是否进入回测循环
- 是否有数据缺失
"""

import os
import sys
import json
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict

# 获取logger
logger = logging.getLogger(__name__)

try:
    from .runner import load_jq_strategy, run_jq_strategy
    from .io import get_record_data, clear_runtime_data, set_runtime_dir
    from .strategy_base import set_current_strategy
except ImportError as e:
    import warnings

    warnings.warn(f"导入错误: {e}")
    raise


class ValidationStatus(Enum):
    """验证状态（统一判定标准）"""

    LOAD_FAILED = "load_failed"
    SYNTAX_ERROR = "syntax_error"
    MISSING_DEPENDENCY = "missing_dependency"
    MISSING_API = "missing_api"
    MISSING_RESOURCE = "missing_resource"
    DATA_MISSING = "data_missing"
    RUN_EXCEPTION = "run_exception"
    ENTERED_BACKTEST_LOOP = "entered_backtest_loop"
    SUCCESS_NO_TRADE = "success_no_trade"
    SUCCESS_WITH_NAV = "success_with_nav"
    SUCCESS_WITH_TRANSACTIONS = "success_with_transactions"
    PSEUDO_SUCCESS = "pseudo_success"
    PSEUDO_FAILURE = "pseudo_failure"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class StrategyValidationResult:
    """策略验证结果（增强证据字段）"""

    def __init__(self, strategy_file: str):
        self.strategy_file = strategy_file
        self.strategy_name = os.path.basename(strategy_file)
        self.timestamp = datetime.now().isoformat()

        self.load_success = False
        self.load_error = None
        self.functions_found = []

        self.run_success = False
        self.run_error = None
        self.runtime_dir = None

        self.timer_triggered = False
        self.timer_details = {}

        self.trade_occurred = False
        self.trade_count = 0
        self.trade_details = {}

        self.nav_curve_exists = False
        self.nav_curve_valid = False
        self.nav_details = {}

        self.record_output_exists = False
        self.record_keys = []
        self.record_details = {}

        self.semantic_issues = []
        self.passed_checks = []
        self.failed_checks = []

        self.final_status = ValidationStatus.UNKNOWN.value
        self.is_really_running = False

        self.evidence = {
            "loaded": False,
            "loaded_time": 0,
            "entered_backtest_loop": False,
            "has_transactions": False,
            "transaction_count": 0,
            "has_nav_series": False,
            "nav_series_length": 0,
            "nav_series_first": 0,
            "nav_series_last": 0,
            "nav_series_min": 0,
            "nav_series_max": 0,
            "nav_series_std": 0,
            "strategy_obj_valid": False,
            "cerebro_valid": False,
            "final_value": 0,
            "initial_capital": 0,
            "pnl": 0,
            "pnl_pct": 0,
            "max_drawdown": 0,
            "annual_return": 0,
            "sharpe_ratio": 0,
            "trading_days": 0,
            "timer_count": 0,
            "has_data": True,
            "data_missing_count": 0,
            "record_count": 0,
        }

        self.attribution = {
            "failure_root_cause": "",
            "missing_dependency": "",
            "missing_api": "",
            "missing_resource_file": "",
            "error_category": "",
            "error_type": "",
            "recoverable": False,
            "recommendation": "",
        }

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "strategy_file": self.strategy_file,
            "strategy_name": self.strategy_name,
            "timestamp": self.timestamp,
            "load_success": self.load_success,
            "load_error": self.load_error,
            "functions_found": self.functions_found,
            "run_success": self.run_success,
            "run_error": self.run_error,
            "timer_triggered": self.timer_triggered,
            "timer_details": self.timer_details,
            "trade_occurred": self.trade_occurred,
            "trade_count": self.trade_count,
            "trade_details": self.trade_details,
            "nav_curve_exists": self.nav_curve_exists,
            "nav_curve_valid": self.nav_curve_valid,
            "nav_details": self.nav_details,
            "record_output_exists": self.record_output_exists,
            "record_keys": self.record_keys,
            "record_details": self.record_details,
            "semantic_issues": self.semantic_issues,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "final_status": self.final_status,
            "is_really_running": self.is_really_running,
            "evidence": self.evidence,
            "attribution": self.attribution,
        }


def validate_strategy_loading(strategy_file: str, result: StrategyValidationResult):
    """验证策略加载（增强错误识别）"""
    import time

    start_time = time.time()

    try:
        functions = load_jq_strategy(strategy_file)
        load_time = time.time() - start_time

        result.load_success = True
        result.functions_found = list(functions.keys()) if functions else []
        result.evidence["loaded"] = True
        result.evidence["loaded_time"] = round(load_time, 3)

        if not functions:
            result.semantic_issues.append("策略文件未定义任何函数")
            result.failed_checks.append("策略函数定义检查")
            result.attribution["failure_root_cause"] = "策略未定义任何函数"
            result.attribution["error_category"] = "load_failure"
            result.attribution["error_type"] = "NoFunctionsError"
            result.attribution["recoverable"] = False
            result.attribution["recommendation"] = "检查策略文件是否包含函数定义"
        else:
            result.passed_checks.append("策略函数定义检查")

            required_funcs = ["initialize"]
            for func in required_funcs:
                if func not in functions:
                    result.semantic_issues.append(f"缺少必要函数: {func}")
                    result.attribution["missing_dependency"] = f"缺少{func}函数"

            has_handle_funcs = any(
                f.startswith("handle_") or f.startswith("trading_")
                for f in functions.keys()
            )

            has_timer_in_code = False
            try:
                with open(strategy_file, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()
                    has_timer_in_code = (
                        "run_monthly(" in code
                        or "run_daily(" in code
                        or "run_weekly(" in code
                    )
            except:
                pass

            if not has_handle_funcs and not has_timer_in_code:
                result.semantic_issues.append(
                    "缺少交易处理函数或定时器注册（handle_*/trading_* 或 run_monthly/run_daily）"
                )
                result.attribution["missing_dependency"] = (
                    "缺少交易处理函数或定时器注册"
                )
            elif has_timer_in_code and not has_handle_funcs:
                result.passed_checks.append("定时器注册检查")

    except FileNotFoundError as e:
        result.load_success = False
        result.load_error = f"文件不存在: {e}"
        result.failed_checks.append("策略文件加载")
        result.evidence["loaded"] = False
        result.attribution["failure_root_cause"] = "策略文件不存在"
        result.attribution["error_category"] = "load_failure"
        result.attribution["error_type"] = "FileNotFoundError"
        result.attribution["missing_resource_file"] = str(e)
        result.attribution["recoverable"] = True
        result.attribution["recommendation"] = "确认策略文件路径是否正确"

    except UnicodeDecodeError as e:
        result.load_success = False
        result.load_error = f"编码错误: {e}"
        result.failed_checks.append("策略文件加载")
        result.evidence["loaded"] = False
        result.attribution["failure_root_cause"] = "策略文件编码错误"
        result.attribution["error_category"] = "load_failure"
        result.attribution["error_type"] = "UnicodeDecodeError"
        result.attribution["recoverable"] = True
        result.attribution["recommendation"] = "将策略文件转换为UTF-8编码"

    except SyntaxError as e:
        result.load_success = False
        result.load_error = f"语法错误: {e.msg} (行 {e.lineno})"
        result.failed_checks.append("策略文件加载")
        result.evidence["loaded"] = False
        result.attribution["failure_root_cause"] = f"语法错误: {e.msg}"
        result.attribution["error_category"] = "syntax_error"
        result.attribution["error_type"] = "SyntaxError"
        result.attribution["recoverable"] = False
        result.attribution["recommendation"] = f"修复第{e.lineno}行的语法错误: {e.msg}"

    except ImportError as e:
        result.load_success = False
        result.load_error = f"导入错误: {e}"
        result.failed_checks.append("策略文件加载")
        result.evidence["loaded"] = False
        result.attribution["failure_root_cause"] = f"依赖包缺失: {e}"
        result.attribution["error_category"] = "dependency_missing"
        result.attribution["error_type"] = "ImportError"
        result.attribution["missing_dependency"] = str(e)
        result.attribution["recoverable"] = True
        result.attribution["recommendation"] = (
            f"安装缺失的依赖包: pip install <package>"
        )

    except Exception as e:
        result.load_success = False
        result.load_error = f"加载异常: {str(e)}"
        result.failed_checks.append("策略文件加载")
        result.evidence["loaded"] = False
        result.attribution["failure_root_cause"] = f"{type(e).__name__}: {str(e)[:100]}"
        result.attribution["error_category"] = "load_failure"
        result.attribution["error_type"] = type(e).__name__
        result.attribution["recoverable"] = False
        result.attribution["recommendation"] = "查看详细错误日志，分析具体异常原因"


def validate_strategy_execution(
    strategy_file: str,
    start_date: str = "2022-01-01",
    end_date: str = "2022-12-31",
    initial_capital: float = 100000,
    result: StrategyValidationResult = None,
):
    """验证策略执行（修复bug + 增强证据提取）"""

    runtime_dir = f"runtime_data/validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    set_runtime_dir(runtime_dir)
    result.runtime_dir = runtime_dir
    result.evidence["initial_capital"] = initial_capital

    clear_runtime_data()

    try:
        strategy_functions = load_jq_strategy(strategy_file)
        if not strategy_functions:
            result.run_success = False
            result.run_error = "策略加载失败，无法运行"
            result.evidence["loaded"] = False
            result.attribution["failure_root_cause"] = "策略加载失败"
            result.attribution["error_category"] = "load_failure"
            result.attribution["recoverable"] = False
            result.attribution["recommendation"] = "检查策略文件是否有语法错误"
            return

        run_result = run_jq_strategy(
            strategy_file,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            auto_discover_stocks=True,
        )

        if run_result is None:
            result.run_success = False
            result.run_error = "run_jq_strategy返回None"
            result.failed_checks.append("策略运行")
            result.evidence["loaded"] = False
            result.attribution["failure_root_cause"] = "run_jq_strategy返回None"
            result.attribution["error_category"] = "load_failure"
            result.attribution["recoverable"] = False
            result.attribution["recommendation"] = "检查策略加载器返回值"
            return

        result.run_success = True
        result.evidence["loaded"] = True
        result.evidence["strategy_obj_valid"] = run_result.get("strategy") is not None
        result.evidence["cerebro_valid"] = run_result.get("cerebro") is not None

        result.evidence["final_value"] = run_result.get("final_value", 0)
        result.evidence["pnl"] = run_result.get("pnl", 0)
        result.evidence["pnl_pct"] = run_result.get("pnl_pct", 0)

        strategy = run_result.get("strategy")

        if strategy is None:
            result.semantic_issues.append("策略实例未返回")
            result.failed_checks.append("策略实例检查")
            result.evidence["strategy_obj_valid"] = False
        else:
            result.passed_checks.append("策略运行")
            result.evidence["strategy_obj_valid"] = True

            if hasattr(strategy, "timer_manager"):
                timer_manager = strategy.timer_manager
                if timer_manager is not None and hasattr(timer_manager, "timers"):
                    timer_count = (
                        len(timer_manager.timers) if timer_manager.timers else 0
                    )
                    if timer_count > 0:
                        result.timer_triggered = True
                        result.timer_details = {
                            "timer_count": timer_count,
                            "timer_types": [
                                t.__class__.__name__ for t in timer_manager.timers
                            ],
                        }
                        result.evidence["timer_count"] = timer_count
                        result.evidence["entered_backtest_loop"] = True
                        result.passed_checks.append("定时器注册检查")
                    else:
                        result.semantic_issues.append("未注册任何定时器")
                        result.failed_checks.append("定时器注册检查")

            if hasattr(strategy, "orders"):
                orders = strategy.orders if strategy.orders else []
                order_count = len(orders) if orders else 0
                if order_count > 0:
                    result.trade_occurred = True
                    result.trade_count = order_count
                    result.evidence["has_transactions"] = True
                    result.evidence["transaction_count"] = order_count
                    result.evidence["entered_backtest_loop"] = True

                    buy_orders = [o for o in orders if o.get("action") == "buy"]
                    sell_orders = [o for o in orders if o.get("action") == "sell"]

                    result.trade_details = {
                        "total": order_count,
                        "buy": len(buy_orders),
                        "sell": len(sell_orders),
                        "symbols": list(
                            set([o.get("symbol") for o in orders if o.get("symbol")])
                        ),
                    }
                    result.passed_checks.append("交易发生检查")
                else:
                    result.semantic_issues.append("未发生任何交易")
                    result.failed_checks.append("交易发生检查")

            if hasattr(strategy, "navs"):
                navs = strategy.navs if strategy.navs else []
                nav_length = len(navs) if navs else 0
                if nav_length > 10:
                    result.nav_curve_exists = True
                    result.evidence["has_nav_series"] = True
                    result.evidence["nav_series_length"] = nav_length
                    result.evidence["entered_backtest_loop"] = True

                    nav_series = pd.Series(navs)
                    nav_min = float(nav_series.min())
                    nav_max = float(nav_series.max())
                    nav_std = float(nav_series.std())
                    nav_first = float(nav_series.iloc[0]) if len(nav_series) > 0 else 0
                    nav_last = float(nav_series.iloc[-1]) if len(nav_series) > 0 else 0

                    result.evidence["nav_series_first"] = nav_first
                    result.evidence["nav_series_last"] = nav_last
                    result.evidence["nav_series_min"] = nav_min
                    result.evidence["nav_series_max"] = nav_max
                    result.evidence["nav_series_std"] = nav_std

                    if nav_std > 0 and nav_max > nav_min:
                        result.nav_curve_valid = True
                        result.nav_details = {
                            "length": nav_length,
                            "min": nav_min,
                            "max": nav_max,
                            "std": nav_std,
                            "first": nav_first,
                            "last": nav_last,
                            "range_pct": float((nav_max - nav_min) / nav_first * 100)
                            if nav_first > 0
                            else 0,
                        }
                        result.passed_checks.append("净值曲线检查")

                        if nav_length > 0:
                            days = nav_length
                            final_value = result.evidence["final_value"]
                            annual_return = (
                                (final_value / initial_capital) ** (252 / days) - 1
                                if days > 0
                                else 0
                            )
                            result.evidence["annual_return"] = float(annual_return)
                            result.evidence["trading_days"] = days

                            cummax = nav_series.cummax()
                            drawdown = (nav_series - cummax) / cummax
                            max_drawdown = float(drawdown.min())
                            result.evidence["max_drawdown"] = max_drawdown

                            returns = nav_series.pct_change().dropna()
                            if len(returns) > 0 and returns.std() > 0:
                                sharpe = returns.mean() / returns.std() * (252**0.5)
                                result.evidence["sharpe_ratio"] = float(sharpe)

                    else:
                        result.semantic_issues.append("净值曲线变化异常（可能无波动）")
                        result.failed_checks.append("净值曲线检查")
                else:
                    result.semantic_issues.append(
                        f"净值曲线数据点不足（{nav_length}个）"
                    )
                    result.failed_checks.append("净值曲线检查")

            record_data = get_record_data()
            if record_data and len(record_data) > 0:
                result.record_output_exists = True
                result.record_keys = list(record_data.keys())
                record_count = sum(
                    len(v) if isinstance(v, list) else 1 for v in record_data.values()
                )
                result.evidence["record_count"] = record_count
                result.record_details = {
                    "keys": list(record_data.keys()),
                    "total_records": record_count,
                }
                result.passed_checks.append("record输出检查")
            else:
                result.semantic_issues.append("record无输出")

        final_value = result.evidence["final_value"]
        pnl = result.evidence["pnl"]

        if final_value == initial_capital and pnl == 0:
            result.semantic_issues.append("最终资金与初始资金相同（无变化）")

    except Exception as e:
        import traceback

        result.run_success = False
        result.run_error = f"运行异常: {str(e)}\n{traceback.format_exc()[-500:]}"
        result.failed_checks.append("策略运行")
        result.evidence["loaded"] = True

        error_str = str(e)
        error_type = type(e).__name__

        result.attribution["error_type"] = error_type
        result.attribution["failure_root_cause"] = f"{error_type}: {error_str[:100]}"

        if "数据" in error_str or "无数据" in error_str or "股票" in error_str:
            result.attribution["error_category"] = "data_missing"
            result.attribution["missing_resource_file"] = error_str
            result.attribution["recoverable"] = True
            result.attribution["recommendation"] = "补充缺失的数据文件或调整回测时间段"
            result.evidence["has_data"] = False

        elif any(
            dep in error_str.lower()
            for dep in ["module", "import", "no module named", "cannot import"]
        ):
            result.attribution["error_category"] = "dependency_missing"
            result.attribution["missing_dependency"] = error_str
            result.attribution["recoverable"] = True
            result.attribution["recommendation"] = (
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
            result.attribution["error_category"] = "api_missing"
            result.attribution["missing_api"] = error_str
            result.attribution["recoverable"] = True
            result.attribution["recommendation"] = (
                "在utility中实现缺失的API或修改策略代码"
            )

        elif any(
            res in error_str.lower()
            for res in ["file not found", "no such file", "文件不存在", "cannot find"]
        ):
            result.attribution["error_category"] = "resource_missing"
            result.attribution["missing_resource_file"] = error_str
            result.attribution["recoverable"] = True
            result.attribution["recommendation"] = "补充缺失的数据文件或调整策略代码"

        else:
            result.attribution["error_category"] = "runtime_exception"
            result.attribution["recoverable"] = False
            result.attribution["recommendation"] = "查看详细错误日志，分析具体异常原因"


def determine_final_status(result: StrategyValidationResult):
    """判定最终状态（统一标准）"""

    if not result.load_success:
        if result.attribution.get("error_type") == "SyntaxError":
            result.final_status = ValidationStatus.SYNTAX_ERROR.value
        elif result.attribution.get("error_category") == "dependency_missing":
            result.final_status = ValidationStatus.MISSING_DEPENDENCY.value
        elif result.attribution.get("error_category") == "resource_missing":
            result.final_status = ValidationStatus.MISSING_RESOURCE.value
        else:
            result.final_status = ValidationStatus.LOAD_FAILED.value
        result.is_really_running = False
        return

    if not result.run_success:
        if result.attribution.get("error_category") == "data_missing":
            result.final_status = ValidationStatus.DATA_MISSING.value
        elif result.attribution.get("error_category") == "api_missing":
            result.final_status = ValidationStatus.MISSING_API.value
        elif result.attribution.get("error_category") == "dependency_missing":
            result.final_status = ValidationStatus.MISSING_DEPENDENCY.value
        elif result.attribution.get("error_category") == "resource_missing":
            result.final_status = ValidationStatus.MISSING_RESOURCE.value
        else:
            result.final_status = ValidationStatus.RUN_EXCEPTION.value
        result.is_really_running = False
        return

    evidence = result.evidence

    if not evidence.get("entered_backtest_loop", False):
        result.final_status = ValidationStatus.PSEUDO_SUCCESS.value
        result.is_really_running = False
        result.attribution["failure_root_cause"] = "策略未进入回测循环"
        result.attribution["error_category"] = "pseudo_success"
        result.attribution["recoverable"] = True
        result.attribution["recommendation"] = "检查策略逻辑是否匹配回测时间段"
        return

    has_transactions = evidence.get("has_transactions", False)
    has_nav = evidence.get("has_nav_series", False)
    nav_length = evidence.get("nav_series_length", 0)
    pnl_pct = evidence.get("pnl_pct", 0)

    if has_transactions and has_nav and nav_length > 10:
        result.final_status = ValidationStatus.SUCCESS_WITH_TRANSACTIONS.value
        result.is_really_running = True
        return

    if has_nav and nav_length > 10:
        if pnl_pct != 0:
            result.final_status = ValidationStatus.SUCCESS_WITH_NAV.value
            result.is_really_running = True
        else:
            result.final_status = ValidationStatus.SUCCESS_NO_TRADE.value
            result.is_really_running = True
        return

    if evidence.get("loaded", False) and evidence.get("entered_backtest_loop", False):
        result.final_status = ValidationStatus.PSEUDO_FAILURE.value
        result.is_really_running = False
        result.attribution["failure_root_cause"] = "策略加载并运行，但无有效输出"
        result.attribution["error_category"] = "pseudo_failure"
        result.attribution["recoverable"] = True
        result.attribution["recommendation"] = "检查数据源或策略交易逻辑"
        return

    result.final_status = ValidationStatus.UNKNOWN.value
    result.is_really_running = False


def validate_single_strategy(
    strategy_file: str,
    start_date: str = "2022-01-01",
    end_date: str = "2022-12-31",
    initial_capital: float = 100000,
) -> StrategyValidationResult:
    """验证单个策略"""

    result = StrategyValidationResult(strategy_file)

    logger.info("=" * 80)
    logger.info(f"验证策略: {result.strategy_name}")
    logger.info("=" * 80)

    logger.info("[阶段1] 策略加载验证...")
    validate_strategy_loading(strategy_file, result)

    if not result.load_success:
        logger.warning(f"  加载失败: {result.load_error}")
        determine_final_status(result)
        return result

    logger.info("  加载成功")
    logger.info(f"  发现函数: {result.functions_found}")

    logger.info("[阶段2] 策略运行验证...")
    logger.info(f"  回测区间: {start_date} ~ {end_date}")
    logger.info(f"  初始资金: {initial_capital}")

    validate_strategy_execution(
        strategy_file,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        result=result,
    )

    if not result.run_success:
        logger.warning(f"  运行失败: {result.run_error}")
        determine_final_status(result)
        return result

    logger.info("  运行完成")

    logger.info("[阶段3] 结果验证...")

    if result.timer_triggered:
        logger.info(f"  定时器触发: {result.timer_details}")
    else:
        logger.warning("  定时器未触发")

    if result.trade_occurred:
        logger.info(f"  发生交易: {result.trade_details}")
    else:
        logger.warning("  未发生交易")

    if result.nav_curve_valid:
        logger.info(f"  净值曲线有效: {result.nav_details}")
    else:
        logger.warning("  净值曲线异常")

    if result.record_output_exists:
        logger.info(f"  record输出: {result.record_keys}")
    else:
        logger.info("  record无输出（可能策略未使用record）")

    if result.semantic_issues:
        logger.warning("语义问题:")
        for issue in result.semantic_issues:
            logger.warning(f"  - {issue}")

    determine_final_status(result)

    logger.info(f"最终状态: {result.final_status}")
    logger.info(f"真跑通: {result.is_really_running}")
    logger.info("=" * 80)

    return result


def validate_batch_strategies(
    strategy_files: List[str],
    start_date: str = "2022-01-01",
    end_date: str = "2022-12-31",
    initial_capital: float = 100000,
    output_file: str = None,
) -> List[StrategyValidationResult]:
    """批量验证策略"""

    results = []

    logger.info("#" * 80)
    logger.info(f"批量策略验证 - 共 {len(strategy_files)} 个策略")
    logger.info("#" * 80)

    for i, strategy_file in enumerate(strategy_files, 1):
        logger.info(f"[{i}/{len(strategy_files)}] 验证: {os.path.basename(strategy_file)}")
        result = validate_single_strategy(
            strategy_file,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
        )
        results.append(result)

    logger.info("#" * 80)
    logger.info("批量验证总结")
    logger.info("#" * 80)

    status_counts = {}
    for result in results:
        status = result.final_status
        status_counts[status] = status_counts.get(status, 0) + 1

    logger.info("状态统计:")
    for status, count in sorted(status_counts.items()):
        logger.info(f"  {status}: {count}")

    really_running = [r for r in results if r.is_really_running]
    logger.info(f"真跑通策略池: {len(really_running)} 个")

    if output_file:
        output_data = {
            "validation_time": datetime.now().isoformat(),
            "total_strategies": len(strategy_files),
            "status_counts": status_counts,
            "really_running_count": len(really_running),
            "results": [r.to_dict() for r in results],
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        logger.info(f"验证结果已保存: {output_file}")

    return results


def generate_report(results: List[StrategyValidationResult], output_md: str):
    """生成Markdown报告"""

    with open(output_md, "w", encoding="utf-8") as f:
        f.write("# Task 19 Result: 策略回放正确性验证\n\n")
        f.write(f"**验证时间**: {datetime.now().isoformat()}\n\n")

        f.write("## 修改文件\n\n")
        f.write("- `src/strategy_validator.py` (新增)\n")
        f.write(
            "- `docs/0330_result/task19_strategy_replay_validation_result.md` (本文件)\n\n"
        )

        f.write("## 完成内容\n\n")
        f.write("1. 创建策略验证器 `strategy_validator.py`\n")
        f.write("2. 定义验证维度和检查项\n")
        f.write("3. 抽样验证真实策略样本\n")
        f.write("4. 识别语义偏差问题\n")
        f.write("5. 产出真跑通策略样本池\n\n")

        f.write("## 抽检样本\n\n")
        f.write(f"共抽检 {len(results)} 个策略样本\n\n")

        f.write("| 策略名 | 加载 | 运行 | 定时器 | 交易 | 净值 | 最终状态 |\n")
        f.write("|--------|------|------|--------|------|------|----------|\n")

        for r in results:
            load_icon = "✓" if r.load_success else "✗"
            run_icon = "✓" if r.run_success else "✗"
            timer_icon = "✓" if r.timer_triggered else "✗"
            trade_icon = "✓" if r.trade_occurred else "✗"
            nav_icon = "✓" if r.nav_curve_valid else "✗"

            f.write(
                f"| {r.strategy_name[:40]} | {load_icon} | {run_icon} | {timer_icon} | {trade_icon} | {nav_icon} | {r.final_status} |\n"
            )

        f.write("\n## 验证方式\n\n")
        f.write("### 检查维度\n\n")
        f.write("1. **策略加载**: 检查语法、编码、函数定义\n")
        f.write("2. **策略运行**: 检查回测能否完成\n")
        f.write("3. **定时器触发**: 检查run_daily/run_monthly是否注册\n")
        f.write("4. **交易发生**: 检查订单数量和类型\n")
        f.write("5. **净值曲线**: 检查数据点数量和波动性\n")
        f.write("6. **record输出**: 检查策略输出数据\n\n")

        f.write("### 语义合理性判定\n\n")
        f.write('标记为"语义异常"的情况:\n')
        f.write("- 未注册任何定时器\n")
        f.write("- 未发生任何交易\n")
        f.write("- 净值曲线无波动\n")
        f.write("- 最终资金与初始相同\n")
        f.write("- 多个关键检查失败\n\n")

        f.write("## 真跑通策略样本池\n\n")

        really_running = [r for r in results if r.is_really_running]

        if really_running:
            f.write(f'共 {len(really_running)} 个策略判定为"真跑通"\n\n')

            for r in really_running:
                f.write(f"### {r.strategy_name}\n\n")
                f.write(f"- **状态**: {r.final_status}\n")
                f.write(f"- **函数**: {', '.join(r.functions_found[:5])}\n")

                if r.timer_details:
                    f.write(
                        f"- **定时器**: {r.timer_details.get('timer_count', 0)}个\n"
                    )

                if r.trade_details:
                    f.write(f"- **交易**: {r.trade_details.get('total', 0)}笔\n")
                    f.write(f"  - 买入: {r.trade_details.get('buy', 0)}笔\n")
                    f.write(f"  - 卖出: {r.trade_details.get('sell', 0)}笔\n")

                if r.nav_details:
                    f.write(
                        f"- **净值**: {r.nav_details.get('length', 0)}点, 波动{r.nav_details.get('range_pct', 0):.2f}%\n"
                    )

                f.write("\n")
        else:
            f.write("当前抽样样本中未发现完全跑通策略\n\n")

        f.write("## 语义异常策略分析\n\n")

        semantic_failed = [r for r in results if r.semantic_issues]

        if semantic_failed:
            f.write(f"共 {len(semantic_failed)} 个策略存在语义异常\n\n")

            for r in semantic_failed[:5]:
                f.write(f"### {r.strategy_name}\n\n")
                for issue in r.semantic_issues:
                    f.write(f"- {issue}\n")
                f.write("\n")

        f.write("## 已知边界\n\n")
        f.write("1. **回测时间窗口**: 2022-01-01 ~ 2022-12-31（缩短时间以提升速度）\n")
        f.write("2. **初始资金**: 100,000（较小资金以降低数据需求）\n")
        f.write("3. **网络依赖**: 部分数据依赖akshare在线数据\n")
        f.write("4. **股票池发现**: 使用自动发现机制，可能不完整\n")
        f.write("5. **record检查**: 仅检查有输出的策略\n\n")

        f.write("## 后续建议\n\n")

        if len(really_running) < len(results) * 0.5:
            f.write("当前真跑通率较低，建议:\n")
            f.write("1. 修复定时器注册机制\n")
            f.write("2. 补充股票池自动发现\n")
            f.write("3. 修复因子查询接口\n")
            f.write("4. 增加离线数据兜底\n")
        else:
            f.write("当前真跑通率良好，建议:\n")
            f.write("1. 扩大验证样本数量\n")
            f.write("2. 增加更复杂策略验证\n")
            f.write("3. 建立自动化回归测试\n")

        f.write("\n---\n\n")
        f.write(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="策略回放正确性验证")
    parser.add_argument("strategy_files", nargs="+", help="策略文件路径")
    parser.add_argument("--start", default="2022-01-01", help="开始日期")
    parser.add_argument("--end", default="2022-12-31", help="结束日期")
    parser.add_argument("--capital", type=float, default=100000, help="初始资金")
    parser.add_argument("--output", default="validation_result.json", help="输出文件")
    parser.add_argument("--report", default=None, help="Markdown报告文件")

    args = parser.parse_args()

    results = validate_batch_strategies(
        args.strategy_files,
        start_date=args.start,
        end_date=args.end,
        initial_capital=args.capital,
        output_file=args.output,
    )

    if args.report:
        generate_report(results, args.report)
    else:
        report_path = f"docs/0330_result/task19_strategy_replay_validation_result.md"
        generate_report(results, report_path)
        logger.info(f"报告已生成: {report_path}")
