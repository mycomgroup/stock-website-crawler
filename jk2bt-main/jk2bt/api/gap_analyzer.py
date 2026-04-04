"""
jk2bt/api/gap_analyzer.py — API 缺口分析器

用于扫描真实策略，统计 API 使用情况，生成缺失 API 矩阵

功能:
1. 扫描所有策略文件，提取 API 调用
2. 区分 API 支持状态: 已完整支持 / 部分支持 / 仅占位支持 / 完全未支持
3. 统计每个 API 的命中策略数、代表策略样本
4. 生成优先级建议
5. 输出 Markdown 报告和 JSON/CSV 矩阵

注意: 此文件是包内独立实现，不依赖外部 tools 目录
"""

import os
import re
import ast
import json
import csv
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from pathlib import Path
import pandas as pd


@dataclass
class APIUsageInfo:
    """API 使用信息"""

    api_name: str
    support_status: (
        str  # 'fully_supported', 'partial_support', 'placeholder', 'not_supported'
    )
    hit_count: int = 0
    strategies: List[str] = field(default_factory=list)
    priority: str = "low"  # 'high', 'medium', 'low'
    notes: str = ""


class APIGapAnalyzer:
    """API 缺口分析器"""

    def __init__(self):
        self._api_usage: Dict[str, APIUsageInfo] = {}
        self._strategy_api_calls: Dict[str, Set[str]] = {}

        self._fully_supported_apis = {
            "get_price",
            "get_fundamentals",
            "get_all_securities",
            "get_security_info",
            "get_current_data",
            "get_index_weights",
            "get_index_stocks",
            "get_factor_values",
            "get_industry_stocks",
            "get_future_contracts",
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
            "current_dt",
            "record",
            "send_message",
            "read_file",
            "write_file",
            "get_hl_stock",
            "get_continue_count_df",
            "get_relative_position_df",
            "filter_paused_stocks",
            "filter_st_stocks",
            "filter_limit_up_stocks",
            "filter_limit_down_stocks",
            "winsorize",
            "neutralize",
            "standardlize",
        }

        self._partial_supported_apis = {
            "get_billboard_list",
            "get_industry_classify",
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
            "get_sharpe_ratio",
            "get_sortino_ratio",
            "get_calmar_ratio",
            "get_information_ratio",
            "get_max_drawdown",
            "get_max_drawdown_length",
            "get_alpha",
            "get_beta",
            "normalize_data",
        }

        self._placeholder_apis = {
            "get_margin_stocks",
            "get_margin_info",
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
            "get_insider_trades",
            "get_all_industry_stocks",
        }

        self._not_supported_apis = {
            "get_fundamentals_continuously",
            "get_securities_margin_info",
            "get_margincash_stocks",
            "get_margincash_info",
            "get_mtss",
            "get_locked_shares",
            "get_share_num",
            "get_locked_share_num",
            "get_locked_share_unlock_info",
            "get_delist_stocks",
            "get_suspend_stocks",
            "get_ipo_stocks",
            "get_ipo_info",
            "get_ipo_prospectus",
            "get_all_financial_indicators",
            "get_ETF_fund_info",
            "get_ETF_current_data",
            "get_LOF_current_data",
            "get_LOF_fund_info",
            "get_fund_list",
            "get_fund_info",
            "get_fund_manager_info",
            "get_fund_holdings",
            "get_fund_net_value",
            "get_fund_portfolio",
            "get_reits_list",
            "get_reits_info",
        }

    def scan_strategy_file(self, file_path: str) -> Set[str]:
        """扫描单个策略文件，提取 API 调用"""
        if not os.path.exists(file_path):
            return set()

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
            return set()

        if "\x00" in code:
            code = code.replace("\x00", "")

        api_calls = set()

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        api_calls.add(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        api_calls.add(node.func.attr)
        except SyntaxError:
            pattern = r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
            matches = re.findall(pattern, code)
            api_calls = set(matches)

        all_known_apis = (
            self._fully_supported_apis
            | self._partial_supported_apis
            | self._placeholder_apis
            | self._not_supported_apis
        )

        filtered_calls = {api for api in api_calls if api in all_known_apis}

        return filtered_calls

    def scan_all_strategies(
        self, directory: str, pattern: str = "*.txt"
    ) -> Dict[str, Set[str]]:
        """扫描目录下所有策略文件"""
        import glob

        files = glob.glob(os.path.join(directory, pattern))

        for file_path in sorted(files):
            api_calls = self.scan_strategy_file(file_path)
            if api_calls:
                file_name = os.path.basename(file_path)
                self._strategy_api_calls[file_name] = api_calls

                for api in api_calls:
                    if api not in self._api_usage:
                        self._api_usage[api] = APIUsageInfo(
                            api_name=api,
                            support_status=self._get_support_status(api),
                            hit_count=0,
                            strategies=[],
                        )

                    self._api_usage[api].hit_count += 1
                    self._api_usage[api].strategies.append(file_name)

        return self._strategy_api_calls

    def _get_support_status(self, api: str) -> str:
        """获取 API 支持状态"""
        if api in self._fully_supported_apis:
            return "fully_supported"
        elif api in self._partial_supported_apis:
            return "partial_support"
        elif api in self._placeholder_apis:
            return "placeholder"
        elif api in self._not_supported_apis:
            return "not_supported"
        else:
            return "unknown"

    def calculate_priority(self):
        """计算 API 优先级"""
        for api, info in self._api_usage.items():
            if info.support_status == "fully_supported":
                info.priority = "low"
                info.notes = "已完整支持，无需额外工作"
            elif info.support_status == "partial_support":
                if info.hit_count >= 10:
                    info.priority = "high"
                    info.notes = "部分支持且高频使用，需完善"
                elif info.hit_count >= 5:
                    info.priority = "medium"
                    info.notes = "部分支持且中等频使用"
                else:
                    info.priority = "low"
                    info.notes = "部分支持但低频使用"
            elif info.support_status == "placeholder":
                if info.hit_count >= 5:
                    info.priority = "high"
                    info.notes = "仅占位但策略实际使用，需实现"
                elif info.hit_count >= 2:
                    info.priority = "medium"
                    info.notes = "仅占位且有策略使用"
                else:
                    info.priority = "low"
                    info.notes = "仅占位，使用较少"
            elif info.support_status == "not_supported":
                if info.hit_count >= 3:
                    info.priority = "high"
                    info.notes = "完全未支持但有策略使用，需实现"
                elif info.hit_count >= 1:
                    info.priority = "medium"
                    info.notes = "未支持，有少量策略使用"
                else:
                    info.priority = "low"
                    info.notes = "未支持，策略未使用"


def analyze_api_gaps(
    strategy_dir: str = "strategies", output_dir: str = "docs/api_analysis"
):
    """执行完整的 API 缺口分析"""
    analyzer = APIGapAnalyzer()

    print("扫描策略文件...")
    analyzer.scan_all_strategies(strategy_dir, "*.txt")

    print("计算优先级...")
    analyzer.calculate_priority()

    print(f"扫描完成: {len(analyzer._strategy_api_calls)} 个策略, {len(analyzer._api_usage)} 个 API")

    return analyzer


__all__ = ["APIUsageInfo", "APIGapAnalyzer", "analyze_api_gaps"]
