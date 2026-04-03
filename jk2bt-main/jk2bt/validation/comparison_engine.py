"""
validation/comparison_engine.py
数据对比引擎
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ComparisonResult:
    """单个字段对比结果"""

    field_name: str
    local_value: Any
    jq_value: Any
    tolerance: float
    is_match: bool
    diff_pct: float = 0.0
    diff_abs: float = 0.0
    note: str = ""

    def to_dict(self) -> Dict:
        return {
            "field_name": self.field_name,
            "local_value": self.local_value,
            "jq_value": self.jq_value,
            "tolerance": self.tolerance,
            "is_match": self.is_match,
            "diff_pct": self.diff_pct,
            "diff_abs": self.diff_abs,
            "note": self.note,
        }


@dataclass
class StockComparisonResult:
    """单只股票对比结果"""

    code: str
    date: str
    data_type: str
    field_results: List[ComparisonResult] = field(default_factory=list)
    is_match: bool = True
    match_rate: float = 100.0

    def to_dict(self) -> Dict:
        return {
            "code": self.code,
            "date": self.date,
            "data_type": self.data_type,
            "is_match": self.is_match,
            "match_rate": self.match_rate,
            "field_results": [r.to_dict() for r in self.field_results],
        }


@dataclass
class ComparisonSummary:
    """对比汇总结果"""

    data_type: str
    total_stocks: int = 0
    total_fields: int = 0
    matched_stocks: int = 0
    matched_fields: int = 0
    match_rate: float = 0.0
    stock_results: List[StockComparisonResult] = field(default_factory=list)
    field_stats: Dict[str, Dict] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "data_type": self.data_type,
            "total_stocks": self.total_stocks,
            "total_fields": self.total_fields,
            "matched_stocks": self.matched_stocks,
            "matched_fields": self.matched_fields,
            "match_rate": self.match_rate,
            "stock_results": [r.to_dict() for r in self.stock_results],
            "field_stats": self.field_stats,
        }


class ComparisonEngine:
    """数据对比引擎"""

    def __init__(self, tolerance_config: Dict[str, float] = None):
        """
        Args:
            tolerance_config: 字段容差配置 {"pe_ratio": 0.01, ...}
        """
        self.tolerance_config = tolerance_config or {
            "pe": 0.01,
            "pe_ttm": 0.01,
            "pb": 0.01,
            "ps": 0.01,
            "market_cap": 0.01,
            "circulating_market_cap": 0.01,
            "high_limit": 0.01,
            "low_limit": 0.01,
            "is_st": 0.0,  # 精确匹配
            "paused": 0.0,  # 精确匹配
            "momentum_20": 0.05,
            "volatility_20": 0.05,
        }

    def get_tolerance(self, field_name: str) -> float:
        """获取字段容差"""
        return self.tolerance_config.get(field_name, 0.01)

    def compare_value(self, local_val: Any, jq_val: Any, field_name: str) -> ComparisonResult:
        """
        对比单个值

        Args:
            local_val: 本地值
            jq_val: JQ值
            field_name: 字段名

        Returns:
            ComparisonResult
        """
        tolerance = self.get_tolerance(field_name)

        # 处理 None 值
        if local_val is None and jq_val is None:
            return ComparisonResult(
                field_name=field_name,
                local_value=local_val,
                jq_value=jq_val,
                tolerance=tolerance,
                is_match=True,
                note="两者均为 None",
            )

        if local_val is None or jq_val is None:
            return ComparisonResult(
                field_name=field_name,
                local_value=local_val,
                jq_value=jq_val,
                tolerance=tolerance,
                is_match=False,
                note=f"值缺失: local={local_val}, jq={jq_val}",
            )

        # 布尔值精确匹配
        if isinstance(local_val, bool) or isinstance(jq_val, bool):
            is_match = bool(local_val) == bool(jq_val)
            return ComparisonResult(
                field_name=field_name,
                local_value=local_val,
                jq_value=jq_val,
                tolerance=tolerance,
                is_match=is_match,
                note="布尔值精确匹配" if is_match else "布尔值不匹配",
            )

        # 数值比较
        try:
            local_num = float(local_val)
            jq_num = float(jq_val)

            # 绝对差异
            diff_abs = abs(local_num - jq_num)

            # 相对差异（百分比）
            if jq_num != 0:
                diff_pct = abs(local_num - jq_num) / abs(jq_num) * 100
            else:
                diff_pct = 0.0 if local_num == 0 else 100.0

            # 判断是否匹配
            if tolerance == 0:
                # 精确匹配
                is_match = diff_abs < 0.001
            elif tolerance < 1:
                # 百分比容差
                is_match = diff_pct <= tolerance * 100
            else:
                # 绝对值容差
                is_match = diff_abs <= tolerance

            return ComparisonResult(
                field_name=field_name,
                local_value=local_num,
                jq_value=jq_num,
                tolerance=tolerance,
                is_match=is_match,
                diff_pct=diff_pct,
                diff_abs=diff_abs,
                note="匹配" if is_match else f"差异 {diff_pct:.2f}%",
            )

        except (ValueError, TypeError):
            # 非数值，字符串比较
            is_match = str(local_val) == str(jq_val)
            return ComparisonResult(
                field_name=field_name,
                local_value=local_val,
                jq_value=jq_val,
                tolerance=tolerance,
                is_match=is_match,
                note="字符串匹配" if is_match else "字符串不匹配",
            )

    def compare_row(self, local_row: pd.Series, jq_row: pd.Series,
                    fields: List[str]) -> StockComparisonResult:
        """
        对比单行数据（单只股票）

        Args:
            local_row: 本地数据行
            jq_row: JQ数据行
            fields: 要对比的字段列表

        Returns:
            StockComparisonResult
        """
        code = local_row.get("code", jq_row.get("code", "unknown"))
        date = local_row.get("date", jq_row.get("date", "unknown"))

        results = []
        matched_count = 0

        for field in fields:
            local_val = local_row.get(field)
            jq_val = jq_row.get(field)

            result = self.compare_value(local_val, jq_val, field)
            results.append(result)

            if result.is_match:
                matched_count += 1

        match_rate = matched_count / len(fields) * 100 if fields else 0

        return StockComparisonResult(
            code=code,
            date=date,
            data_type="mixed",
            field_results=results,
            is_match=matched_count == len(fields),
            match_rate=match_rate,
        )

    def compare_dataframe(self, local_df: pd.DataFrame, jq_df: pd.DataFrame,
                          key_columns: List[str] = None,
                          compare_columns: List[str] = None) -> ComparisonSummary:
        """
        对比两个 DataFrame

        Args:
            local_df: 本地数据
            jq_df: JQ数据
            key_columns: 键列（用于匹配行）
            compare_columns: 要对比的列

        Returns:
            ComparisonSummary
        """
        key_columns = key_columns or ["code", "date"]
        compare_columns = compare_columns or [
            col for col in local_df.columns
            if col not in key_columns and col in jq_df.columns
        ]

        summary = ComparisonSummary(data_type="dataframe")

        # 按键列合并
        local_indexed = local_df.set_index(key_columns)
        jq_indexed = jq_df.set_index(key_columns)

        # 获取共同的键
        common_keys = local_indexed.index.intersection(jq_indexed.index)
        summary.total_stocks = len(common_keys)
        summary.total_fields = len(compare_columns)

        # 逐行对比
        for key in common_keys:
            local_row = local_indexed.loc[key]
            jq_row = jq_indexed.loc[key]

            if isinstance(local_row, pd.DataFrame):
                local_row = local_row.iloc[0]
            if isinstance(jq_row, pd.DataFrame):
                jq_row = jq_row.iloc[0]

            result = self.compare_row(local_row, jq_row, compare_columns)
            summary.stock_results.append(result)

            if result.is_match:
                summary.matched_stocks += 1

            summary.matched_fields += sum(1 for r in result.field_results if r.is_match)

        # 计算匹配率
        if summary.total_stocks > 0:
            summary.match_rate = summary.matched_stocks / summary.total_stocks * 100

        # 字段统计
        for field in compare_columns:
            field_results = [
                r for sr in summary.stock_results
                for r in sr.field_results if r.field_name == field
            ]
            matched = sum(1 for r in field_results if r.is_match)
            summary.field_stats[field] = {
                "total": len(field_results),
                "matched": matched,
                "match_rate": matched / len(field_results) * 100 if field_results else 0,
                "avg_diff_pct": np.mean([r.diff_pct for r in field_results if r.diff_pct > 0]) if field_results else 0,
            }

        return summary

    def compare_valuation(self, local_df: pd.DataFrame, jq_df: pd.DataFrame) -> ComparisonSummary:
        """对比估值数据"""
        compare_columns = ["pe", "pe_ttm", "pb", "ps", "market_cap", "circulating_market_cap"]
        available_columns = [col for col in compare_columns if col in local_df.columns and col in jq_df.columns]

        return self.compare_dataframe(local_df, jq_df, compare_columns=available_columns)

    def compare_trade_status(self, local_df: pd.DataFrame, jq_df: pd.DataFrame) -> ComparisonSummary:
        """对比交易状态数据"""
        compare_columns = ["high_limit", "low_limit", "is_st", "paused"]
        available_columns = [col for col in compare_columns if col in local_df.columns and col in jq_df.columns]

        return self.compare_dataframe(local_df, jq_df, compare_columns=available_columns)

    def compare_factors(self, local_df: pd.DataFrame, jq_df: pd.DataFrame) -> ComparisonSummary:
        """对比因子数据"""
        key_columns = ["code", "date"]
        compare_columns = [col for col in local_df.columns
                          if col not in key_columns and col in jq_df.columns]

        return self.compare_dataframe(local_df, jq_df, compare_columns=compare_columns)