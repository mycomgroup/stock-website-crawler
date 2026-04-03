"""
validation/report_generator.py
报告生成器
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import os

from .comparison_engine import ComparisonSummary, StockComparisonResult
from .validator import ValidationReport

logger = logging.getLogger(__name__)


class ReportGenerator:
    """报告生成器"""

    def __init__(self, output_dir: str = "validation_results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_markdown_report(self, report: ValidationReport,
                                  filename: str = None) -> str:
        """生成 Markdown 报告"""
        filename = filename or f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(self.output_dir, filename)

        lines = []

        # 标题
        lines.append("# jk2bt 数据验证报告")
        lines.append("")
        lines.append(f"**验证时间**: {report.timestamp}")
        lines.append("")

        # 配置信息
        lines.append("## 验证配置")
        lines.append("")
        lines.append(f"- **股票数量**: {len(report.config.get('stocks', []))}")
        lines.append(f"- **日期范围**: {report.config.get('start_date')} ~ {report.config.get('end_date')}")
        lines.append(f"- **数据类型**: {', '.join(report.config.get('data_types', []))}")
        lines.append("")

        # 总体结果
        lines.append("## 总体结果")
        lines.append("")
        lines.append(f"| 指标 | 值 |")
        lines.append(f"|------|-----|")
        lines.append(f"| 总对比数 | {report.total_comparisons} |")
        lines.append(f"| 匹配数 | {report.total_matched} |")
        lines.append(f"| 匹配率 | {report.overall_match_rate:.2f}% |")
        lines.append("")

        # 各数据类型结果
        lines.append("## 详细结果")
        lines.append("")

        for data_type, summary in report.summaries.items():
            lines.append(f"### {data_type}")
            lines.append("")
            lines.append(f"| 指标 | 值 |")
            lines.append(f"|------|-----|")
            lines.append(f"| 股票数 | {summary.total_stocks} |")
            lines.append(f"| 字段数 | {summary.total_fields} |")
            lines.append(f"| 匹配股票数 | {summary.matched_stocks} |")
            lines.append(f"| 匹配字段数 | {summary.matched_fields} |")
            lines.append(f"| 匹配率 | {summary.match_rate:.2f}% |")
            lines.append("")

            # 字段统计
            if summary.field_stats:
                lines.append("**字段统计**:")
                lines.append("")
                lines.append("| 字段 | 总数 | 匹配数 | 匹配率 | 平均差异 |")
                lines.append("|------|------|--------|--------|----------|")

                for field, stats in summary.field_stats.items():
                    lines.append(f"| {field} | {stats['total']} | {stats['matched']} | {stats['match_rate']:.2f}% | {stats.get('avg_diff_pct', 0):.2f}% |")

                lines.append("")

            # 不匹配的股票
            failed_stocks = [s for s in summary.stock_results if not s.is_match]
            if failed_stocks:
                lines.append(f"**不匹配股票 ({len(failed_stocks)} 只)**:")
                lines.append("")

                for stock in failed_stocks[:10]:  # 只显示前10只
                    failed_fields = [r for r in stock.field_results if not r.is_match]
                    field_details = ", ".join([
                        f"{r.field_name}({r.diff_pct:.2f}%)"
                        for r in failed_fields
                    ])
                    lines.append(f"- {stock.code} ({stock.date}): {field_details}")

                if len(failed_stocks) > 10:
                    lines.append(f"- ... 还有 {len(failed_stocks) - 10} 只")

                lines.append("")

        # 结论
        lines.append("## 结论")
        lines.append("")

        if report.overall_match_rate >= 95:
            lines.append("✅ **数据一致性良好** - 匹配率 >= 95%")
        elif report.overall_match_rate >= 80:
            lines.append("⚠️ **数据存在差异** - 匹配率 80% ~ 95%，建议检查差异数据")
        else:
            lines.append("❌ **数据一致性较差** - 匹配率 < 80%，需要排查数据源问题")

        lines.append("")
        lines.append("---")
        lines.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        # 写入文件
        content = "\n".join(lines)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Markdown 报告已生成: {filepath}")
        return filepath

    def generate_diff_detail(self, report: ValidationReport,
                             filename: str = None) -> str:
        """生成差异详情 CSV"""
        filename = filename or f"validation_diff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.output_dir, filename)

        rows = []

        for data_type, summary in report.summaries.items():
            for stock in summary.stock_results:
                for field in stock.field_results:
                    if not field.is_match:
                        rows.append({
                            "data_type": data_type,
                            "code": stock.code,
                            "date": stock.date,
                            "field": field.field_name,
                            "local_value": field.local_value,
                            "jq_value": field.jq_value,
                            "diff_pct": field.diff_pct,
                            "diff_abs": field.diff_abs,
                            "tolerance": field.tolerance,
                        })

        if rows:
            df = pd.DataFrame(rows)
            df.to_csv(filepath, index=False, encoding="utf-8-sig")
            logger.info(f"差异详情已生成: {filepath}")
        else:
            logger.info("无差异，不生成详情文件")

        return filepath

    def generate_summary_table(self, report: ValidationReport) -> str:
        """生成汇总表格字符串"""
        lines = []
        lines.append("| 数据类型 | 股票数 | 匹配率 | 状态 |")
        lines.append("|----------|--------|--------|------|")

        for data_type, summary in report.summaries.items():
            status = "✅" if summary.match_rate >= 95 else ("⚠️" if summary.match_rate >= 80 else "❌")
            lines.append(f"| {data_type} | {summary.total_stocks} | {summary.match_rate:.2f}% | {status} |")

        return "\n".join(lines)

    def print_console_summary(self, report: ValidationReport):
        """打印控制台摘要"""
        print("\n" + "=" * 60)
        print("数据验证结果摘要")
        print("=" * 60)
        print(f"验证时间: {report.timestamp}")
        print(f"总体匹配率: {report.overall_match_rate:.2f}%")
        print("-" * 60)

        for data_type, summary in report.summaries.items():
            print(f"\n{data_type}:")
            print(f"  股票数: {summary.total_stocks}")
            print(f"  匹配率: {summary.match_rate:.2f}%")

            if summary.field_stats:
                print("  字段匹配率:")
                for field, stats in summary.field_stats.items():
                    print(f"    - {field}: {stats['match_rate']:.2f}%")

        print("\n" + "=" * 60)

        if report.overall_match_rate >= 95:
            print("✅ 数据一致性良好")
        elif report.overall_match_rate >= 80:
            print("⚠️ 数据存在差异，建议检查")
        else:
            print("❌ 数据一致性较差，需要排查")

        print("=" * 60 + "\n")