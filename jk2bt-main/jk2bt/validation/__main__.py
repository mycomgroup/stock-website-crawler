#!/usr/bin/env python
"""
jk2bt 数据验证命令行工具

用法:
    python -m jk2bt.validation [options]

示例:
    # 使用默认配置运行验证
    python -m jk2bt.validation

    # 指定股票和日期
    python -m jk2bt.validation --stocks 600519.XSHG,000858.XSHE --start 2024-01-01 --end 2024-03-31

    # 使用配置文件
    python -m jk2bt.validation --config validation_config.yaml

    # 只生成 JQ 采集脚本
    python -m jk2bt.validation --generate-scripts
"""

import argparse
import logging
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from jk2bt.validation.config import ValidationConfig
from jk2bt.validation.validator import DataValidator
from jk2bt.validation.report_generator import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="jk2bt 数据验证工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                                    # 使用默认配置
  %(prog)s --stocks 600519.XSHG,000858.XSHE   # 指定股票
  %(prog)s --start 2024-01-01 --end 2024-03-31  # 指定日期范围
  %(prog)s --generate-scripts                 # 生成 JQ 采集脚本
  %(prog)s --config validation_config.yaml    # 使用配置文件
        """
    )

    parser.add_argument(
        "--config", "-c",
        help="配置文件路径 (YAML 或 JSON)"
    )
    parser.add_argument(
        "--stocks", "-s",
        help="股票代码列表，逗号分隔"
    )
    parser.add_argument(
        "--start",
        help="开始日期 (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end",
        help="结束日期 (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--data-types",
        help="数据类型，逗号分隔 (valuation,trade_status,factors)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="validation_results",
        help="输出目录 (默认: validation_results)"
    )
    parser.add_argument(
        "--generate-scripts",
        action="store_true",
        help="只生成 JoinQuant Notebook 采集脚本"
    )
    parser.add_argument(
        "--validate-local",
        action="store_true",
        help="只验证本地数据（不对比 JQ）"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # 加载配置
    if args.config:
        config = ValidationConfig.from_file(args.config)
    else:
        config = ValidationConfig()

    # 命令行参数覆盖配置
    if args.stocks:
        config.stocks = args.stocks.split(",")
    if args.start:
        config.start_date = args.start
    if args.end:
        config.end_date = args.end
    if args.data_types:
        config.data_types = args.data_types.split(",")
    config.output_dir = args.output_dir

    # 创建验证器
    validator = DataValidator(config)
    reporter = ReportGenerator(config.output_dir)

    # 只生成脚本
    if args.generate_scripts:
        logger.info("生成 JoinQuant Notebook 采集脚本...")
        validator.generate_jq_collector_scripts(config.output_dir)
        logger.info("完成！请在 JoinQuant Notebook 中执行生成的脚本。")
        return

    # 验证本地数据
    if args.validate_local:
        logger.info("验证本地数据...")
        for data_type in config.data_types:
            if data_type == "valuation":
                df = validator.collector.local_source.get_valuation_data(
                    config.stocks, config.end_date
                )
            elif data_type == "trade_status":
                df = validator.collector.local_source.get_trade_status(
                    config.stocks, config.end_date
                )
            else:
                continue

            logger.info(f"\n{data_type} 数据预览:")
            print(df.head(10))
            print(f"\n总计 {len(df)} 条记录")
        return

    # 运行全量验证
    logger.info("=" * 60)
    logger.info("开始数据验证")
    logger.info("=" * 60)
    logger.info(f"股票数: {len(config.stocks)}")
    logger.info(f"日期范围: {config.start_date} ~ {config.end_date}")
    logger.info(f"数据类型: {config.data_types}")
    logger.info("=" * 60)

    # 检查是否有 JQ 数据
    jq_data_exists = False
    for data_type in config.data_types:
        jq_file = f"{config.output_dir}/jq_{data_type}_{config.end_date}.json"
        if os.path.exists(jq_file):
            jq_data_exists = True
            break

    if not jq_data_exists:
        logger.warning("=" * 60)
        logger.warning("未找到 JoinQuant 数据文件！")
        logger.warning("请先执行以下步骤:")
        logger.warning("1. 运行: python -m jk2bt.validation --generate-scripts")
        logger.warning("2. 在 JoinQuant Notebook 中执行生成的脚本")
        logger.warning("3. 将结果保存为 JSON 文件到 validation_results/ 目录")
        logger.warning("=" * 60)

        # 生成脚本
        validator.generate_jq_collector_scripts(config.output_dir)
        return

    # 运行验证
    report = validator.run_full_validation()

    # 生成报告
    reporter.generate_markdown_report(report)
    reporter.generate_diff_detail(report)
    reporter.print_console_summary(report)

    # 保存 JSON
    report.save_json(f"{config.output_dir}/validation_result.json")

    logger.info("验证完成！")


if __name__ == "__main__":
    main()