"""
tests/comparison/run_comparison.py
数据比较主执行脚本

协调数据收集、比较分析、可视化、报告生成的完整流程。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import argparse
import sys
import warnings

# 导入比较框架模块
from .config import (
    SAMPLE_STOCKS, SAMPLE_INDEXES,
    START_DATE, END_DATE,
    COMPARISON_CONFIG, OUTPUT_DIR,
)
from .data_collector import DataCollector, generate_jq_data_template
from .comparator import DataComparator, quick_compare
from .statistics_analyzer import StatisticsAnalyzer, compare_distribution
from .visualizer import DataVisualizer
from .report_generator import ReportGenerator, generate_summary_csv


class ComparisonRunner:
    """
    数据比较执行器

    协调完整的比较流程。

    使用方式:
        runner = ComparisonRunner()
        runner.run_full_comparison(jq_data_path='jq_export_data.json')
    """

    def __init__(
        self,
        sample_stocks: Optional[List[str]] = None,
        sample_indexes: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        output_dir: Optional[str] = None,
        config: Optional[Dict] = None,
    ):
        """
        初始化执行器。

        Parameters
        ----------
        sample_stocks : list, optional
            样本股票
        sample_indexes : list, optional
            样本指数
        start_date : str, optional
            开始日期
        end_date : str, optional
            结束日期
        output_dir : str, optional
            输出目录
        config : dict, optional
            自定义配置
        """
        self.sample_stocks = sample_stocks or SAMPLE_STOCKS
        self.sample_indexes = sample_indexes or SAMPLE_INDEXES
        self.start_date = start_date or START_DATE
        self.end_date = end_date or END_DATE
        self.output_dir = Path(output_dir or OUTPUT_DIR)
        self.config = config or COMPARISON_CONFIG

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 初始化各模块
        self.collector = DataCollector(
            sample_stocks=self.sample_stocks,
            sample_indexes=self.sample_indexes,
            start_date=self.start_date,
            end_date=self.end_date,
            output_dir=str(self.output_dir),
        )
        self.comparator = DataComparator()
        self.statistics_analyzer = StatisticsAnalyzer()
        self.visualizer = DataVisualizer()
        self.report_generator = ReportGenerator(output_dir=str(self.output_dir))

    def run_full_comparison(
        self,
        jq_data_path: Optional[str] = None,
        data_types: Optional[List[str]] = None,
        generate_report: bool = True,
        generate_plots: bool = True,
    ) -> Dict:
        """
        运行完整比较流程。

        Parameters
        ----------
        jq_data_path : str, optional
            JQ 数据文件路径
        data_types : list, optional
            要比较的数据类型: ['price', 'valuation', 'financial', 'component']
        generate_report : bool
            是否生成 HTML 报告
        generate_plots : bool
            是否生成可视化图表

        Returns
        -------
        Dict
            比较结果摘要
        """
        data_types = data_types or ['price', 'valuation', 'component']

        all_comparison_results = {}
        all_statistics_results = {}
        all_component_results = {}

        print("=" * 60)
        print("jk2bt vs JoinQuant 数据比较")
        print("=" * 60)
        print(f"样本股票: {len(self.sample_stocks)} 只")
        print(f"样本指数: {len(self.sample_indexes)} 个")
        print(f"时间范围: {self.start_date} ~ {self.end_date}")
        print(f"输出目录: {self.output_dir}")
        print("=" * 60)

        # 1. 行情数据比较
        if 'price' in data_types:
            print("\n[1/4] 行情数据比较...")
            price_results = self._compare_price_data(jq_data_path)
            if price_results:
                all_comparison_results.update(price_results['comparison'])
                all_statistics_results.update(price_results['statistics'])

        # 2. 估值数据比较
        if 'valuation' in data_types:
            print("\n[2/4] 估值数据比较...")
            valuation_results = self._compare_valuation_data(jq_data_path)
            if valuation_results:
                all_comparison_results.update(valuation_results['comparison'])
                all_statistics_results.update(valuation_results['statistics'])

        # 3. 财务数据比较
        if 'financial' in data_types:
            print("\n[3/4] 财务数据比较...")
            financial_results = self._compare_financial_data(jq_data_path)
            if financial_results:
                all_comparison_results.update(financial_results['comparison'])
                all_statistics_results.update(financial_results['statistics'])

        # 4. 成分股比较
        if 'component' in data_types:
            print("\n[4/4] 成分股比较...")
            component_results = self._compare_components(jq_data_path)
            if component_results:
                all_component_results = component_results

        # 5. 生成可视化
        if generate_plots and all_comparison_results:
            print("\n[5/6] 生成可视化图表...")
            self._generate_plots(all_comparison_results, all_statistics_results)

        # 6. 生成报告
        if generate_report:
            print("\n[6/6] 生成报告...")
            report_path = self.report_generator.generate_report(
                comparison_results=all_comparison_results,
                statistics_results=all_statistics_results,
                component_results=all_component_results,
                output_path=str(self.output_dir / "comparison_report.html"),
            )
            print(f"报告已保存: {report_path}")

            # 生成 CSV 摘要
            csv_path = generate_summary_csv(
                all_comparison_results,
                str(self.output_dir / "comparison_summary.csv"),
            )
            print(f"CSV 摘要已保存: {csv_path}")

        # 计算总体结果
        overall_pass = self._calculate_overall_pass(
            all_comparison_results,
            all_statistics_results,
            all_component_results,
        )

        print("\n" + "=" * 60)
        print(f"比较完成！总体状态: {'✓ 通过' if overall_pass else '✗ 失败'}")
        print("=" * 60)

        return {
            "comparison": all_comparison_results,
            "statistics": all_statistics_results,
            "component": all_component_results,
            "overall_pass": overall_pass,
            "output_dir": str(self.output_dir),
        }

    def _compare_price_data(
        self,
        jq_data_path: Optional[str] = None,
    ) -> Optional[Dict]:
        """比较行情数据"""
        try:
            # 收集 jk2bt 数据
            jk2bt_data = self.collector.collect_jk2bt_price_data()

            if not jk2bt_data:
                warnings.warn("未能收集到 jk2bt 行情数据")
                return None

            # 保存 jk2bt 数据
            self.collector.save_jk2bt_data(jk2bt_data, 'jk2bt_price_data', format='pickle')

            # 加载 JQ 数据
            if jq_data_path:
                jq_data = self.collector.load_jq_data(jq_data_path, 'price')
            else:
                print("  未提供 JQ 数据文件，使用 jk2bt 数据自检模式")
                jq_data = jk2bt_data  # 自检模式：比较自身数据

            # 合并对齐
            jk2bt_df, jq_df = self.collector.align_data(jk2bt_data, jq_data, 'price')

            if jk2bt_df.empty or jq_df.empty:
                warnings.warn("数据对齐后为空")
                return None

            print(f"  jk2bt 数据: {len(jk2bt_df)} 行")
            print(f"  JQ 数据: {len(jq_df)} 行")

            # 数值比较
            comparison_results = self.comparator.compare_dataframes(
                jk2bt_df, jq_df,
                compare_columns=['open', 'high', 'low', 'close', 'volume', 'money'],
            )

            # 统计分析
            statistics_results = self.statistics_analyzer.batch_analyze(
                jk2bt_df, jq_df,
                columns=['open', 'high', 'low', 'close', 'volume', 'money'],
            )

            # 打印摘要
            summary = self.comparator.generate_summary(comparison_results)
            print("\n  行情数据比较摘要:")
            print(summary.to_string(index=False))

            return {
                'comparison': comparison_results,
                'statistics': statistics_results,
            }

        except Exception as e:
            print(f"  行情数据比较失败: {e}")
            return None

    def _compare_valuation_data(
        self,
        jq_data_path: Optional[str] = None,
    ) -> Optional[Dict]:
        """比较估值数据"""
        try:
            # 收集 jk2bt 数据
            jk2bt_data = self.collector.collect_jk2bt_valuation_data()

            if not jk2bt_data:
                warnings.warn("未能收集到 jk2bt 估值数据")
                return None

            # 加载 JQ 数据
            if jq_data_path:
                jq_data = self.collector.load_jq_data(jq_data_path, 'valuation')
            else:
                print("  未提供 JQ 数据文件，使用自检模式")
                jq_data = jk2bt_data

            # 合并对齐
            jk2bt_df, jq_df = self.collector.align_data(jk2bt_data, jq_data, 'valuation')

            if jk2bt_df.empty or jq_df.empty:
                warnings.warn("数据对齐后为空")
                return None

            print(f"  jk2bt 数据: {len(jk2bt_df)} 行")
            print(f"  JQ 数据: {len(jq_df)} 行")

            # 数值比较
            comparison_results = self.comparator.compare_dataframes(
                jk2bt_df, jq_df,
                compare_columns=['pe', 'pb', 'market_cap', 'circulating_market_cap', 'turnover_ratio'],
            )

            # 统计分析
            statistics_results = self.statistics_analyzer.batch_analyze(
                jk2bt_df, jq_df,
                columns=['pe', 'pb', 'market_cap', 'circulating_market_cap', 'turnover_ratio'],
            )

            # 打印摘要
            summary = self.comparator.generate_summary(comparison_results)
            print("\n  估值数据比较摘要:")
            print(summary.to_string(index=False))

            return {
                'comparison': comparison_results,
                'statistics': statistics_results,
            }

        except Exception as e:
            print(f"  估值数据比较失败: {e}")
            return None

    def _compare_financial_data(
        self,
        jq_data_path: Optional[str] = None,
    ) -> Optional[Dict]:
        """比较财务数据"""
        try:
            # 收集 jk2bt 数据
            jk2bt_data = self.collector.collect_jk2bt_financial_data()

            if not jk2bt_data:
                warnings.warn("未能收集到 jk2bt 财务数据")
                return None

            # 加载 JQ 数据
            if jq_data_path:
                jq_data = self.collector.load_jq_data(jq_data_path, 'financial')
            else:
                print("  未提供 JQ 数据文件，使用自检模式")
                jq_data = jk2bt_data

            # 合并对齐
            jk2bt_df, jq_df = self.collector.align_data(jk2bt_data, jq_data, 'financial')

            if jk2bt_df.empty or jq_df.empty:
                warnings.warn("数据对齐后为空")
                return None

            print(f"  jk2bt 数据: {len(jk2bt_df)} 行")
            print(f"  JQ 数据: {len(jq_df)} 行")

            # 获取共同列
            common_cols = list(set(jk2bt_df.columns) & set(jq_df.columns))
            numeric_cols = [c for c in common_cols if pd.api.types.is_numeric_dtype(jk2bt_df[c])]

            if not numeric_cols:
                warnings.warn("没有共同的可比较数值列")
                return None

            # 数值比较
            comparison_results = self.comparator.compare_dataframes(
                jk2bt_df, jq_df,
                compare_columns=numeric_cols[:10],  # 限制比较前10个数值列
            )

            # 统计分析
            statistics_results = self.statistics_analyzer.batch_analyze(
                jk2bt_df, jq_df,
                columns=numeric_cols[:10],
            )

            # 打印摘要
            summary = self.comparator.generate_summary(comparison_results)
            print("\n  财务数据比较摘要:")
            print(summary.to_string(index=False))

            return {
                'comparison': comparison_results,
                'statistics': statistics_results,
            }

        except Exception as e:
            print(f"  财务数据比较失败: {e}")
            return None

    def _compare_components(
        self,
        jq_data_path: Optional[str] = None,
    ) -> Optional[Dict]:
        """比较成分股"""
        try:
            # 收集 jk2bt 数据
            jk2bt_data = self.collector.collect_jk2bt_index_components()

            if not jk2bt_data:
                warnings.warn("未能收集到 jk2bt 成分股数据")
                return None

            print(f"  收集到 {len(jk2bt_data)} 个指数的成分股")

            # 加载 JQ 数据
            if jq_data_path:
                jq_data = self.collector.load_jq_component_data(jq_data_path)
            else:
                print("  未提供 JQ 数据文件，使用自检模式")
                jq_data = jk2bt_data

            # 比较
            results = {}
            for index in self.sample_indexes:
                jk2bt_stocks = jk2bt_data.get(index, [])
                jq_stocks = jq_data.get(index, [])

                if jk2bt_stocks or jq_stocks:
                    result = self.comparator.compare_component_lists(
                        jk2bt_stocks, jq_stocks, index
                    )
                    results[index] = result

                    print(f"\n  {index}:")
                    print(f"    jk2bt: {len(jk2bt_stocks)} 只")
                    print(f"    JQ: {len(jq_stocks)} 只")
                    print(f"    匹配率: {result['match_rate']:.2%}")

            return results

        except Exception as e:
            print(f"  成分股比较失败: {e}")
            return None

    def _generate_plots(
        self,
        comparison_results: Dict,
        statistics_results: Dict,
    ) -> None:
        """生成可视化图表"""
        try:
            # 生成比较结果热力图
            heatmap_path = self.output_dir / 'comparison_heatmap.png'
            self.visualizer.plot_summary_heatmap(
                comparison_results,
                save_path=str(heatmap_path),
            )
            print(f"  热力图已保存: {heatmap_path}")

            # 生成统计特征对比图
            stats_path = self.output_dir / 'statistics_comparison.png'
            self.visualizer.plot_statistics_comparison(
                statistics_results,
                save_path=str(stats_path),
            )
            print(f"  统计对比图已保存: {stats_path}")

        except Exception as e:
            print(f"  可视化生成失败: {e}")

        finally:
            # 关闭图表
            self.visualizer.close()

    def _calculate_overall_pass(
        self,
        comparison_results: Dict,
        statistics_results: Dict,
        component_results: Dict,
    ) -> bool:
        """计算总体是否通过"""
        # 数值比较通过率
        if comparison_results:
            comparison_pass_rate = sum(
                1 for r in comparison_results.values() if r.pass_rate > 0.95
            ) / len(comparison_results)
        else:
            comparison_pass_rate = 1.0

        # 统计检验通过率
        if statistics_results:
            stats_pass_rate = sum(
                1 for r in statistics_results.values() if r.overall_pass
            ) / len(statistics_results)
        else:
            stats_pass_rate = 1.0

        # 成分股通过率
        if component_results:
            component_pass_rate = sum(
                1 for r in component_results.values() if r.get('pass', False)
            ) / len(component_results)
        else:
            component_pass_rate = 1.0

        # 综合判断：各项都通过率 >= 80%
        return (
            comparison_pass_rate >= 0.8 and
            stats_pass_rate >= 0.8 and
            component_pass_rate >= 0.8
        )


def run_comparison_cli():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='jk2bt vs JoinQuant 数据比较工具')

    parser.add_argument(
        '--jq-data',
        type=str,
        default=None,
        help='JQ 数据文件路径 (JSON/CSV/Pickle)',
    )

    parser.add_argument(
        '--data-types',
        type=str,
        nargs='+',
        default=['price', 'valuation', 'component'],
        choices=['price', 'valuation', 'financial', 'component'],
        help='要比较的数据类型',
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='输出目录',
    )

    parser.add_argument(
        '--start-date',
        type=str,
        default=START_DATE,
        help='开始日期',
    )

    parser.add_argument(
        '--end-date',
        type=str,
        default=END_DATE,
        help='结束日期',
    )

    parser.add_argument(
        '--no-report',
        action='store_true',
        help='不生成 HTML 报告',
    )

    parser.add_argument(
        '--no-plot',
        action='store_true',
        help='不生成可视化图表',
    )

    parser.add_argument(
        '--generate-template',
        action='store_true',
        help='生成 JQ 数据导出模板',
    )

    args = parser.parse_args()

    # 生成模板模式
    if args.generate_template:
        template_path = generate_jq_data_template(args.output_dir or OUTPUT_DIR)
        print(f"JQ 数据导出模板已生成: {template_path}")
        print("\n请在 JoinQuant 平台运行模板脚本导出数据，然后将导出的数据文件")
        print("通过 --jq-data 参数传入进行比较。")
        return

    # 正常比较模式
    runner = ComparisonRunner(
        start_date=args.start_date,
        end_date=args.end_date,
        output_dir=args.output_dir,
    )

    results = runner.run_full_comparison(
        jq_data_path=args.jq_data,
        data_types=args.data_types,
        generate_report=not args.no_report,
        generate_plots=not args.no_plot,
    )

    # 返回状态码
    sys.exit(0 if results.get('overall_pass', False) else 1)


def quick_comparison(
    stock: str = None,
    start_date: str = None,
    end_date: str = None,
) -> Tuple[bool, pd.DataFrame]:
    """
    快速比较单个股票数据。

    Parameters
    ----------
    stock : str
        股票代码
    start_date : str
        开始日期
    end_date : str
        结束日期

    Returns
    -------
    Tuple[bool, DataFrame]
        (是否通过, 比较摘要)
    """
    stock = stock or SAMPLE_STOCKS[0]
    start_date = start_date or START_DATE
    end_date = end_date or END_DATE

    runner = ComparisonRunner(
        sample_stocks=[stock],
        start_date=start_date,
        end_date=end_date,
    )

    results = runner.run_full_comparison(
        data_types=['price'],
        generate_report=False,
        generate_plots=False,
    )

    return results.get('overall_pass', False), results


if __name__ == '__main__':
    run_comparison_cli()