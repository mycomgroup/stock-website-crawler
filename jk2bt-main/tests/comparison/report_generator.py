"""
tests/comparison/report_generator.py
报告生成模块

生成 HTML 格式的比较报告。
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import os


class ReportGenerator:
    """
    报告生成器

    生成包含比较结果、统计分析和差异详情的 HTML 报告。

    使用方式:
        generator = ReportGenerator()
        generator.generate_report(comparison_results, statistics_results, 'report.html')
    """

    def __init__(self, output_dir: str = "./comparison_results"):
        """
        初始化报告生成器。

        Parameters
        ----------
        output_dir : str
            输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(
        self,
        comparison_results: Dict,
        statistics_results: Dict,
        component_results: Optional[Dict] = None,
        output_path: Optional[str] = None,
        title: str = "jk2bt vs JoinQuant 数据比较报告",
    ) -> str:
        """
        生成 HTML 报告。

        Parameters
        ----------
        comparison_results : Dict
            数据比较结果
        statistics_results : Dict
            统计分析结果
        component_results : Dict, optional
            成分股比较结果
        output_path : str, optional
            输出路径
        title : str
            报告标题

        Returns
        -------
        str
            报告文件路径
        """
        if output_path is None:
            output_path = str(self.output_dir / "comparison_report.html")

        # 计算总体统计
        overall_stats = self._calculate_overall_stats(comparison_results, statistics_results)

        # 生成各部分 HTML
        summary_html = self._generate_summary_section(overall_stats)
        comparison_html = self._generate_comparison_section(comparison_results)
        statistics_html = self._generate_statistics_section(statistics_results)
        component_html = self._generate_component_section(component_results) if component_results else ""
        diff_details_html = self._generate_diff_details_section(comparison_results)

        # 组装完整 HTML
        html_content = self._get_html_template().format(
            title=title,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            summary_section=summary_html,
            comparison_section=comparison_html,
            statistics_section=statistics_html,
            component_section=component_html,
            diff_details_section=diff_details_html,
        )

        # 保存
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_path

    def _calculate_overall_stats(
        self,
        comparison_results: Dict,
        statistics_results: Dict,
    ) -> Dict:
        """计算总体统计"""
        all_results = list(comparison_results.values())

        total_fields = len(all_results)
        total_count = sum(r.total_count for r in all_results)
        total_match = sum(r.match_count for r in all_results)
        total_diff = sum(r.diff_count for r in all_results)

        overall_pass_rate = total_match / total_count if total_count > 0 else 1.0

        # 统计分析通过率
        stat_pass_count = sum(1 for r in statistics_results.values() if r.overall_pass)
        stat_pass_rate = stat_pass_count / len(statistics_results) if statistics_results else 1.0

        return {
            "total_fields": total_fields,
            "total_count": total_count,
            "total_match": total_match,
            "total_diff": total_diff,
            "overall_pass_rate": overall_pass_rate,
            "stat_pass_rate": stat_pass_rate,
        }

    def _generate_summary_section(self, stats: Dict) -> str:
        """生成摘要部分"""
        pass_class = "pass" if stats["overall_pass_rate"] > 0.95 else "fail"

        return f"""
        <div class="summary">
            <h2>📊 比较摘要</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <span class="stat-label">比较字段数</span>
                    <span class="stat-value">{stats['total_fields']}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">数据点总数</span>
                    <span class="stat-value">{stats['total_count']:,}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">匹配数据点</span>
                    <span class="stat-value">{stats['total_match']:,}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">差异数据点</span>
                    <span class="stat-value">{stats['total_diff']:,}</span>
                </div>
            </div>
            <div class="overall-result {pass_class}">
                <h3>总体通过率: {stats['overall_pass_rate']:.2%}</h3>
                <p>统计检验通过率: {stats['stat_pass_rate']:.2%}</p>
            </div>
        </div>
        """

    def _generate_comparison_section(self, results: Dict) -> str:
        """生成比较结果部分"""
        if not results:
            return "<p>无比较数据</p>"

        rows = []
        for field, result in results.items():
            row_class = "pass" if result.pass_rate > 0.95 else "fail"
            rows.append(f"""
                <tr class="{row_class}">
                    <td>{result.field}</td>
                    <td>{result.data_type}</td>
                    <td>{result.total_count:,}</td>
                    <td>{result.match_count:,}</td>
                    <td>{result.diff_count:,}</td>
                    <td>{result.nan_diff_count}</td>
                    <td class="rate">{result.pass_rate:.2%}</td>
                    <td>{result.max_rel_diff:.4f}</td>
                    <td>{result.mean_rel_diff:.6f}</td>
                    <td>{result.tolerance:.4f}</td>
                    <td class="status">{"✓" if result.pass_rate > 0.95 else "✗"}</td>
                </tr>
            """)

        return f"""
        <div class="section">
            <h2>📈 数据比较结果</h2>
            <table>
                <thead>
                    <tr>
                        <th>字段</th>
                        <th>类型</th>
                        <th>总数</th>
                        <th>匹配数</th>
                        <th>差异数</th>
                        <th>NaN差异</th>
                        <th>通过率</th>
                        <th>最大误差</th>
                        <th>平均误差</th>
                        <th>容忍度</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows)}
                </tbody>
            </table>
        </div>
        """

    def _generate_statistics_section(self, results: Dict) -> str:
        """生成统计分析部分"""
        if not results:
            return "<p>无统计数据</p>"

        rows = []
        for field, result in results.items():
            # 统计量通过率
            stat_pass = sum(1 for v in result.statistics.values() if v.get("pass", True))
            stat_total = len(result.statistics)

            row_class = "pass" if result.overall_pass else "fail"
            rows.append(f"""
                <tr class="{row_class}">
                    <td>{field}</td>
                    <td>{result.statistics.get('mean', {}).get('rel_diff', 0):.4f}</td>
                    <td>{result.statistics.get('std', {}).get('rel_diff', 0):.4f}</td>
                    <td>{result.ks_test.get('pvalue', 0):.4f}</td>
                    <td>{result.correlation.get('pearson', 0):.4f}</td>
                    <td>{result.correlation.get('spearman', 0):.4f}</td>
                    <td class="status">{"✓" if result.overall_pass else "✗"}</td>
                </tr>
            """)

        return f"""
        <div class="section">
            <h2>📊 统计分析结果</h2>
            <table>
                <thead>
                    <tr>
                        <th>字段</th>
                        <th>均值差异</th>
                        <th>标准差差异</th>
                        <th>KS检验p值</th>
                        <th>Pearson相关</th>
                        <th>Spearman相关</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows)}
                </tbody>
            </table>
        </div>
        """

    def _generate_component_section(self, results: Optional[Dict]) -> str:
        """生成成分股比较部分"""
        if not results:
            return ""

        rows = []
        for name, data in results.items():
            row_class = "pass" if data.get("pass", False) else "fail"
            rows.append(f"""
                <tr class="{row_class}">
                    <td>{name}</td>
                    <td>{data.get('jk2bt_count', 0)}</td>
                    <td>{data.get('jq_count', 0)}</td>
                    <td>{data.get('common_count', 0)}</td>
                    <td class="rate">{data.get('match_rate', 0):.2%}</td>
                    <td class="status">{"✓" if data.get("pass", False) else "✗"}</td>
                </tr>
            """)

        return f"""
        <div class="section">
            <h2>📋 成分股比较结果</h2>
            <table>
                <thead>
                    <tr>
                        <th>指数/板块</th>
                        <th>jk2bt数量</th>
                        <th>JQ数量</th>
                        <th>共同数量</th>
                        <th>匹配率</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows)}
                </tbody>
            </table>
        </div>
        """

    def _generate_diff_details_section(self, results: Dict) -> str:
        """生成差异详情部分"""
        details_html = ""

        for field, result in results.items():
            if not result.details.empty and len(result.details) > 0:
                details_sample = result.details.head(20)  # 限制显示数量
                details_html += f"""
                <div class="detail-item">
                    <h3>{field} 差异示例 (前20条)</h3>
                    {details_sample.to_html(index=False, classes='detail-table')}
                </div>
                """

        if not details_html:
            details_html = "<p class='no-diff'>无明显差异</p>"

        return f"""
        <div class="section">
            <h2>🔍 差异详情</h2>
            {details_html}
        </div>
        """

    def _get_html_template(self) -> str:
        """获取 HTML 模板"""
        return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 24px;
            margin-bottom: 10px;
        }}
        .header .timestamp {{
            opacity: 0.8;
            font-size: 14px;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            font-size: 18px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .summary {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-item {{
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .stat-label {{
            display: block;
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }}
        .stat-value {{
            display: block;
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        .overall-result {{
            text-align: center;
            padding: 15px;
            border-radius: 8px;
        }}
        .overall-result.pass {{
            background: #d4edda;
            color: #155724;
        }}
        .overall-result.fail {{
            background: #f8d7da;
            color: #721c24;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        tr.pass {{
            background: #f0fff0;
        }}
        tr.fail {{
            background: #fff0f0;
        }}
        .rate {{
            font-weight: bold;
        }}
        .status {{
            text-align: center;
            font-size: 18px;
        }}
        .detail-item {{
            margin-bottom: 20px;
        }}
        .detail-item h3 {{
            font-size: 14px;
            margin-bottom: 10px;
            color: #666;
        }}
        .detail-table {{
            font-size: 12px;
        }}
        .no-diff {{
            text-align: center;
            color: #666;
            padding: 20px;
        }}
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p class="timestamp">生成时间: {timestamp}</p>
        </div>
        <div class="content">
            {summary_section}
            {comparison_section}
            {statistics_section}
            {component_section}
            {diff_details_section}
        </div>
    </div>
</body>
</html>
        """


def generate_summary_csv(
    comparison_results: Dict,
    output_path: str,
) -> str:
    """
    生成摘要 CSV 文件。

    Parameters
    ----------
    comparison_results : Dict
        比较结果
    output_path : str
        输出路径

    Returns
    -------
    str
        文件路径
    """
    data = []
    for field, result in comparison_results.items():
        data.append(result.to_dict())

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return output_path