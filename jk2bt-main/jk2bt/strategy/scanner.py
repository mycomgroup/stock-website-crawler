"""
策略扫描器模块
用于在运行策略前检查策略的可执行性

功能:
1. 识别策略是否包含initialize函数
2. 检测明显未实现的API依赖
3. 区分策略文件与研究文档/配套资料
4. 预扫描避免运行无效策略
"""

import os
import re
import ast
import logging
from typing import Dict, List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass

# 获取logger
logger = logging.getLogger(__name__)


class StrategyStatus(Enum):
    """策略扫描状态"""

    VALID = "valid"
    NO_INITIALIZE = "no_initialize"
    MISSING_API = "missing_api"
    NOT_STRATEGY = "not_strategy"
    SYNTAX_ERROR = "syntax_error"
    EMPTY_FILE = "empty_file"


@dataclass
class ScanResult:
    """扫描结果"""

    file_path: str
    file_name: str
    status: StrategyStatus
    has_initialize: bool
    has_handle: bool
    missing_apis: List[str]
    error_message: str
    is_executable: bool
    details: Dict


class StrategyScanner:
    """策略扫描器"""

    _KNOWN_APIS = {
        "get_price",
        "get_fundamentals",
        "get_all_securities",
        "get_security_info",
        "get_current_data",
        "get_index_weights",
        "get_index_stocks",
        "get_factor_values",
        "history",
        "attribute_history",
        "order",
        "order_target",
        "order_value",
        "order_target_value",
        "run_daily",
        "run_weekly",
        "run_monthly",
        "get_all_trade_days",
        "get_extras",
        "get_bars",
        "get_billboard_list",
        "get_industry_classify",
        "get_industry_stocks",
        "get_all_industry_stocks",
        "get_stock_industry",
        "get_industry_daily",
        "get_industry_performance",
        "get_market_breadth",
        "get_north_money_flow",
        "get_north_money_daily",
        "get_north_money_holdings",
        "get_north_money_stock_flow",
        "compute_north_money_signal",
        "compute_rsrs",
        "compute_rsrs_signal",
        "get_rsrs_for_index",
        "get_current_rsrs_signal",
        "compute_crowding_ratio",
        "compute_gisi",
        "compute_fed_model",
        "compute_graham_index",
        "compute_below_net_ratio",
        "compute_new_high_ratio",
        "get_all_sentiment_indicators",
        "query",
        "valuation",
        "income",
        "balance",
        "cash_flow",
        "indicator",
        "finance",
        "set_option",
        "set_benchmark",
        "set_slippage",
        "set_order_cost",
        "g",
        "log",
        "context",
        "portfolio",
        "position",
        "universe",
        "subportfolio",
        "current_dt",
        "previous_date",
        "transform_date",
        "prepare_stock_list",
        "get_hl_stock",
        "get_continue_count_df",
        "get_relative_position_df",
        "filter_paused_stocks",
        "filter_st_stocks",
        "filter_limit_up_stocks",
        "filter_limit_down_stocks",
        "get_sharpe_ratio",
        "get_sortino_ratio",
        "get_calmar_ratio",
        "get_information_ratio",
        "get_max_drawdown",
        "get_max_drawdown_length",
        "get_alpha",
        "get_beta",
        "normalize_data",
        "winsorize",
        "neutralize",
        "standardlize",
    }

    _UNIMPLEMENTED_APIS = {
        "get_margin_stocks",
        "get_margin_info",
        "get_future_contracts",
        "get_dominant_contract",
        "get_contract_multiplier",
        "get_cash_flow",
        "get_call_info",
        "get_ticks",
        "get_trade_info",
        "get_trading_dates",
        "get_dividends",
        "get_splits",
        "get_interest_rate",
        "get_yield_curve",
        "get_bond_prices",
        "get_bond_yield",
        "get_option_pricing",
        "get_volatility_surface",
        "get_credit_data",
        "get_macro_data",
        "get_company_info",
        "get_shareholder_info",
        "get_board_info",
        "get_institutional_holdings",
        "get insider_trades",
    }

    _NON_STRATEGY_PATTERNS = [
        r".*\.ipynb$",
        r".*\.md$",
        r".*README.*",
        r".*研究.*",
        r".*说明.*",
        r".*教程.*",
        r".*test.*",
        r".*tests.*",
        r".*_test.*",
        r".*文档.*",
        r".*笔记.*",
        r".*备份.*",
        r".*\.bak$",
        r".*\.old$",
        r".*notes.*",
        r".*note.*",
        r".*非策略.*",
        r".*配套资料.*",
    ]

    _STRATEGY_REQUIRED_PATTERNS = [
        r"def\s+initialize\s*\(",
        r"def\s+handle_data\s*\(",
        r"def\s+before_trading_start\s*\(",
        r"def\s+after_trading_end\s*\(",
        r"def\s+handle_",
        r"def\s+trading_",
        r"run_daily\s*\(",
        r"run_weekly\s*\(",
        r"run_monthly\s*\(",
    ]

    def __init__(self):
        self._cache: Dict[str, ScanResult] = {}

    def is_strategy_file(self, file_path: str) -> bool:
        """判断文件是否可能是策略文件"""
        file_name = os.path.basename(file_path)

        for pattern in self._NON_STRATEGY_PATTERNS:
            if re.match(pattern, file_name, re.IGNORECASE):
                return False

        ext = os.path.splitext(file_name)[1].lower()
        if ext not in (".txt", ".py"):
            return False

        return True

    def scan_file(self, file_path: str) -> ScanResult:
        """扫描单个策略文件"""
        if file_path in self._cache:
            return self._cache[file_path]

        file_name = os.path.basename(file_path)

        if not os.path.exists(file_path):
            result = ScanResult(
                file_path=file_path,
                file_name=file_name,
                status=StrategyStatus.NOT_STRATEGY,
                has_initialize=False,
                has_handle=False,
                missing_apis=[],
                error_message="文件不存在",
                is_executable=False,
                details={},
            )
            self._cache[file_path] = result
            return result

        if not self.is_strategy_file(file_path):
            result = ScanResult(
                file_path=file_path,
                file_name=file_name,
                status=StrategyStatus.NOT_STRATEGY,
                has_initialize=False,
                has_handle=False,
                missing_apis=[],
                error_message="非策略文件（研究文档/配套资料）",
                is_executable=False,
                details={"reason": "file_pattern_excluded"},
            )
            self._cache[file_path] = result
            return result

        code = None
        encodings = ["utf-8", "gbk", "gb2312", "latin-1"]
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    code = f.read()
                break
            except UnicodeDecodeError:
                continue

        if code is None:
            result = ScanResult(
                file_path=file_path,
                file_name=file_name,
                status=StrategyStatus.NOT_STRATEGY,
                has_initialize=False,
                has_handle=False,
                missing_apis=[],
                error_message="无法解码文件",
                is_executable=False,
                details={},
            )
            self._cache[file_path] = result
            return result

        if "\x00" in code:
            code = code.replace("\x00", "")

        if not code.strip():
            result = ScanResult(
                file_path=file_path,
                file_name=file_name,
                status=StrategyStatus.EMPTY_FILE,
                has_initialize=False,
                has_handle=False,
                missing_apis=[],
                error_message="空文件",
                is_executable=False,
                details={},
            )
            self._cache[file_path] = result
            return result

        has_initialize = bool(re.search(r"def\s+initialize\s*\(", code))
        has_handle = bool(
            re.search(
                r"def\s+(handle_|trading_|before_trading_start|after_trading_end)", code
            )
        )

        try:
            tree = ast.parse(code)
            defined_funcs = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    defined_funcs.append(node.name)

            called_funcs = []
            imported_names = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        called_funcs.append(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        called_funcs.append(node.func.attr)
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_names.append(alias.name)
                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        imported_names.append(node.module)
                    for alias in node.names:
                        imported_names.append(alias.name)

        except SyntaxError as e:
            result = ScanResult(
                file_path=file_path,
                file_name=file_name,
                status=StrategyStatus.SYNTAX_ERROR,
                has_initialize=False,
                has_handle=False,
                missing_apis=[],
                error_message=f"语法错误: {e.msg} (行 {e.lineno})",
                is_executable=False,
                details={"syntax_error": str(e)},
            )
            self._cache[file_path] = result
            return result

        missing_apis = []
        for func in called_funcs:
            if func in self._UNIMPLEMENTED_APIS:
                missing_apis.append(func)

        for pattern in self._STRATEGY_REQUIRED_PATTERNS:
            if re.search(pattern, code):
                break
        else:
            if not re.search(r"def\s+\w+\s*\(", code):
                result = ScanResult(
                    file_path=file_path,
                    file_name=file_name,
                    status=StrategyStatus.NOT_STRATEGY,
                    has_initialize=False,
                    has_handle=False,
                    missing_apis=missing_apis,
                    error_message="无策略函数定义",
                    is_executable=False,
                    details={"defined_funcs": defined_funcs},
                )
                self._cache[file_path] = result
                return result

        status = StrategyStatus.VALID
        if not has_initialize:
            status = StrategyStatus.NO_INITIALIZE
        elif missing_apis:
            status = StrategyStatus.MISSING_API

        is_executable = (
            has_initialize
            and (
                has_handle or bool(re.search(r"run_(daily|weekly|monthly)\s*\(", code))
            )
            and not missing_apis
        )

        result = ScanResult(
            file_path=file_path,
            file_name=file_name,
            status=status,
            has_initialize=has_initialize,
            has_handle=has_handle,
            missing_apis=missing_apis,
            error_message="" if status == StrategyStatus.VALID else f"{status.value}",
            is_executable=is_executable,
            details={
                "defined_funcs": defined_funcs,
                "called_funcs": list(set(called_funcs)),
                "imported_names": imported_names,
                "code_lines": len(code.splitlines()),
            },
        )
        self._cache[file_path] = result
        return result

    def scan_directory(
        self, directory: str, pattern: str = "*.txt"
    ) -> Dict[str, List[ScanResult]]:
        """扫描目录下的所有策略文件"""
        import glob

        files = glob.glob(os.path.join(directory, pattern))
        results = {
            "valid": [],
            "no_initialize": [],
            "missing_api": [],
            "not_strategy": [],
            "syntax_error": [],
            "empty_file": [],
            "all": [],
        }

        for file_path in sorted(files):
            result = self.scan_file(file_path)
            results["all"].append(result)
            results[result.status.value].append(result)

        return results

    def get_executable_strategies(
        self, directory: str, pattern: str = "*.txt"
    ) -> List[str]:
        """获取可执行策略文件列表"""
        scan_results = self.scan_directory(directory, pattern)
        return [r.file_path for r in scan_results["all"] if r.is_executable]

    def print_summary(self, scan_results: Dict[str, List[ScanResult]]) -> None:
        """打印扫描结果摘要"""
        total = len(scan_results["all"])
        executable = len([r for r in scan_results["all"] if r.is_executable])

        logger.info("=" * 80)
        logger.info("策略扫描结果摘要")
        logger.info("=" * 80)
        logger.info(f"总文件数: {total}")
        logger.info(f"可执行策略: {executable}")
        logger.info("-" * 40)

        for status, results in scan_results.items():
            if status == "all":
                continue
            if results:
                logger.info(f"{status}: {len(results)}")
                for r in results[:5]:
                    logger.info(f"  - {r.file_name}: {r.error_message or 'OK'}")
                    if r.missing_apis:
                        logger.info(f"    缺失API: {', '.join(r.missing_apis)}")
                if len(results) > 5:
                    logger.info(f"  ... 共 {len(results)} 个")

        logger.info("=" * 80)


def quick_scan_strategy(file_path: str) -> Tuple[bool, str]:
    """快速扫描策略文件，返回是否可执行及原因"""
    scanner = StrategyScanner()
    result = scanner.scan_file(file_path)
    return result.is_executable, result.error_message or "OK"


def batch_scan_strategies(
    directory: str, pattern: str = "*.txt"
) -> Dict[str, List[str]]:
    """批量扫描策略目录"""
    scanner = StrategyScanner()
    results = scanner.scan_directory(directory, pattern)

    return {
        "executable": [r.file_path for r in results["all"] if r.is_executable],
        "invalid": [r.file_path for r in results["all"] if not r.is_executable],
        "not_strategy": [r.file_path for r in results["not_strategy"]],
        "syntax_error": [r.file_path for r in results["syntax_error"]],
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="策略扫描器")
    parser.add_argument("--dir", default="jkcode/jkcode", help="策略目录")
    parser.add_argument("--pattern", default="*.txt", help="文件匹配模式")
    parser.add_argument("--verbose", action="store_true", help="详细输出")

    args = parser.parse_args()

    scanner = StrategyScanner()
    results = scanner.scan_directory(args.dir, args.pattern)

    scanner.print_summary(results)

    if args.verbose:
        logger.info("可执行策略详情:")
        for r in results["valid"]:
            logger.info(f"{r.file_name}:")
            logger.info(f"  initialize: {r.has_initialize}")
            logger.info(f"  handle函数: {r.has_handle}")
            logger.info(f"  定义函数: {r.details.get('defined_funcs', [])}")
