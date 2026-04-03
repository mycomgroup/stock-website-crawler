"""
validation/validator.py
数据验证执行器
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import json
import os

from .config import ValidationConfig
from .data_collector import DataCollector, LocalDataSource, JQNotebookSource
from .comparison_engine import ComparisonEngine, ComparisonSummary

logger = logging.getLogger(__name__)


@dataclass
class ValidationReport:
    """验证报告"""

    config: Dict
    timestamp: str
    summaries: Dict[str, ComparisonSummary] = field(default_factory=dict)
    overall_match_rate: float = 0.0
    total_comparisons: int = 0
    total_matched: int = 0

    def to_dict(self) -> Dict:
        return {
            "config": self.config,
            "timestamp": self.timestamp,
            "overall_match_rate": self.overall_match_rate,
            "total_comparisons": self.total_comparisons,
            "total_matched": self.total_matched,
            "summaries": {k: v.to_dict() for k, v in self.summaries.items()},
        }

    def save_json(self, filepath: str):
        """保存为 JSON"""
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info(f"报告已保存: {filepath}")


class DataValidator:
    """数据验证执行器"""

    def __init__(self, config: ValidationConfig = None):
        self.config = config or ValidationConfig()
        self.collector = DataCollector(self.config)
        self.engine = ComparisonEngine(self.config.tolerance)

    def validate_valuation(self, stocks: List[str] = None,
                          dates: List[str] = None) -> ComparisonSummary:
        """验证估值数据"""
        stocks = stocks or self.config.stocks
        dates = dates or [self.config.end_date]

        all_results = []

        for date in dates:
            logger.info(f"验证估值数据: {date}")

            # 获取本地数据
            local_df = self.collector.local_source.get_valuation_data(stocks, date)

            # JQ 数据需要预先获取
            # 这里假设 JQ 数据已通过 notebook 获取并保存
            jq_result_file = f"validation_results/jq_valuation_{date}.json"
            jq_df = pd.DataFrame()

            if os.path.exists(jq_result_file):
                with open(jq_result_file, "r", encoding="utf-8") as f:
                    jq_data = json.load(f)
                jq_df = pd.DataFrame(jq_data)

            if local_df.empty:
                logger.warning(f"本地估值数据为空: {date}")
                continue

            if jq_df.empty:
                logger.warning(f"JQ 估值数据为空: {date}，请先运行 JQ Notebook 采集数据")
                continue

            # 对比
            summary = self.engine.compare_valuation(local_df, jq_df)
            all_results.append(summary)

        # 合并结果
        if len(all_results) == 1:
            return all_results[0]

        # 汇总多日结果
        combined = ComparisonSummary(data_type="valuation")
        for s in all_results:
            combined.total_stocks += s.total_stocks
            combined.matched_stocks += s.matched_stocks
            combined.total_fields += s.total_fields
            combined.matched_fields += s.matched_fields
            combined.stock_results.extend(s.stock_results)

        if combined.total_stocks > 0:
            combined.match_rate = combined.matched_stocks / combined.total_stocks * 100

        return combined

    def validate_trade_status(self, stocks: List[str] = None,
                             dates: List[str] = None) -> ComparisonSummary:
        """验证交易状态数据"""
        stocks = stocks or self.config.stocks
        dates = dates or [self.config.end_date]

        all_results = []

        for date in dates:
            logger.info(f"验证交易状态数据: {date}")

            # 获取本地数据
            local_df = self.collector.local_source.get_trade_status(stocks, date)

            # JQ 数据
            jq_result_file = f"validation_results/jq_trade_status_{date}.json"
            jq_df = pd.DataFrame()

            if os.path.exists(jq_result_file):
                with open(jq_result_file, "r", encoding="utf-8") as f:
                    jq_data = json.load(f)
                jq_df = pd.DataFrame(jq_data)

            if local_df.empty:
                logger.warning(f"本地交易状态数据为空: {date}")
                continue

            if jq_df.empty:
                logger.warning(f"JQ 交易状态数据为空: {date}")
                continue

            # 对比
            summary = self.engine.compare_trade_status(local_df, jq_df)
            all_results.append(summary)

        # 合并结果
        if len(all_results) == 1:
            return all_results[0]

        combined = ComparisonSummary(data_type="trade_status")
        for s in all_results:
            combined.total_stocks += s.total_stocks
            combined.matched_stocks += s.matched_stocks
            combined.total_fields += s.total_fields
            combined.matched_fields += s.matched_fields
            combined.stock_results.extend(s.stock_results)

        if combined.total_stocks > 0:
            combined.match_rate = combined.matched_stocks / combined.total_stocks * 100

        return combined

    def validate_factors(self, stocks: List[str] = None,
                        dates: List[str] = None,
                        factors: List[str] = None) -> ComparisonSummary:
        """验证因子数据"""
        stocks = stocks or self.config.stocks
        dates = dates or [self.config.end_date]
        factors = factors or ["momentum_20", "volatility_20"]

        all_results = []

        for date in dates:
            logger.info(f"验证因子数据: {date}")

            # 获取本地数据
            local_df = self.collector.local_source.get_factor_data(stocks, date, factors)

            # JQ 数据
            jq_result_file = f"validation_results/jq_factors_{date}.json"
            jq_df = pd.DataFrame()

            if os.path.exists(jq_result_file):
                with open(jq_result_file, "r", encoding="utf-8") as f:
                    jq_data = json.load(f)
                jq_df = pd.DataFrame(jq_data)

            if local_df.empty:
                logger.warning(f"本地因子数据为空: {date}")
                continue

            if jq_df.empty:
                logger.warning(f"JQ 因子数据为空: {date}")
                continue

            # 对比
            summary = self.engine.compare_factors(local_df, jq_df)
            all_results.append(summary)

        # 合并结果
        if len(all_results) == 1:
            return all_results[0]

        combined = ComparisonSummary(data_type="factors")
        for s in all_results:
            combined.total_stocks += s.total_stocks
            combined.matched_stocks += s.matched_stocks
            combined.total_fields += s.total_fields
            combined.matched_fields += s.matched_fields
            combined.stock_results.extend(s.stock_results)

        if combined.total_stocks > 0:
            combined.match_rate = combined.matched_stocks / combined.total_stocks * 100

        return combined

    def run_full_validation(self, stocks: List[str] = None,
                           start_date: str = None,
                           end_date: str = None,
                           data_types: List[str] = None) -> ValidationReport:
        """
        运行全量验证

        Args:
            stocks: 股票列表
            start_date: 开始日期
            end_date: 结束日期
            data_types: 数据类型列表

        Returns:
            ValidationReport
        """
        stocks = stocks or self.config.stocks
        start_date = start_date or self.config.start_date
        end_date = end_date or self.config.end_date
        data_types = data_types or self.config.data_types

        # 获取日期列表
        dates = self.config.get_dates()
        dates = [d for d in dates if start_date <= d <= end_date]

        logger.info(f"开始全量验证: {len(stocks)} 只股票, {len(dates)} 天, {len(data_types)} 种数据类型")

        report = ValidationReport(
            config={
                "stocks": stocks,
                "start_date": start_date,
                "end_date": end_date,
                "data_types": data_types,
            },
            timestamp=datetime.now().isoformat(),
        )

        total_comparisons = 0
        total_matched = 0

        for data_type in data_types:
            logger.info(f"验证数据类型: {data_type}")

            if data_type == "valuation":
                summary = self.validate_valuation(stocks, dates)
            elif data_type == "trade_status":
                summary = self.validate_trade_status(stocks, dates)
            elif data_type == "factors":
                summary = self.validate_factors(stocks, dates)
            else:
                logger.warning(f"未知数据类型: {data_type}")
                continue

            report.summaries[data_type] = summary

            total_comparisons += summary.total_stocks
            total_matched += summary.matched_stocks

        report.total_comparisons = total_comparisons
        report.total_matched = total_matched

        if total_comparisons > 0:
            report.overall_match_rate = total_matched / total_comparisons * 100

        logger.info(f"验证完成: 总体匹配率 {report.overall_match_rate:.2f}%")

        return report

    def generate_jq_collector_scripts(self, output_dir: str = "validation_results"):
        """
        生成 JQ Notebook 数据采集脚本

        用于在 JoinQuant Notebook 中执行，采集对比数据
        """
        os.makedirs(output_dir, exist_ok=True)

        stocks = self.config.stocks
        dates = self.config.get_dates()

        # 估值数据采集脚本
        valuation_script = '''
# 估值数据采集脚本
# 在 JoinQuant Notebook 中运行

import json
from jqdata import *

stocks = %s
dates = %s

all_results = []

for date in dates:
    print(f"采集日期: {date}")
    for stock in stocks:
        try:
            q = query(valuation).filter(valuation.code == stock)
            df = get_fundamentals(q, date)
            if df is not None and not df.empty:
                row = df.iloc[0]
                all_results.append({
                    "code": stock,
                    "date": date,
                    "pe": float(row["pe_ratio"]) if pd.notna(row.get("pe_ratio")) else None,
                    "pb": float(row["pb_ratio"]) if pd.notna(row.get("pb_ratio")) else None,
                    "market_cap": float(row["market_cap"]) if pd.notna(row.get("market_cap")) else None,
                    "circulating_market_cap": float(row["circulating_market_cap"]) if pd.notna(row.get("circulating_market_cap")) else None,
                })
        except Exception as e:
            print(f"Error {stock}: {e}")

print("=== VALUATION RESULT ===")
print(json.dumps(all_results, ensure_ascii=False))
''' % (stocks, dates)

        with open(f"{output_dir}/jq_collect_valuation.py", "w", encoding="utf-8") as f:
            f.write(valuation_script)

        # 交易状态采集脚本
        trade_status_script = '''
# 交易状态数据采集脚本
# 在 JoinQuant Notebook 中运行

import json
from jqdata import *

stocks = %s
dates = %s

all_results = []

for date in dates:
    print(f"采集日期: {date}")
    current_data = get_current_data(stocks, date)
    for stock in stocks:
        try:
            data = current_data[stock]
            all_results.append({
                "code": stock,
                "date": date,
                "high_limit": float(data.high_limit) if data.high_limit else None,
                "low_limit": float(data.low_limit) if data.low_limit else None,
                "is_st": bool(data.is_st),
                "paused": bool(data.paused),
            })
        except Exception as e:
            print(f"Error {stock}: {e}")

print("=== TRADE STATUS RESULT ===")
print(json.dumps(all_results, ensure_ascii=False))
''' % (stocks, dates)

        with open(f"{output_dir}/jq_collect_trade_status.py", "w", encoding="utf-8") as f:
            f.write(trade_status_script)

        logger.info(f"JQ 采集脚本已生成: {output_dir}/")
        logger.info("请在 JoinQuant Notebook 中执行这些脚本，并将结果保存为 JSON 文件")