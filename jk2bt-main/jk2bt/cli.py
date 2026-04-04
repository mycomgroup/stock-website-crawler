"""
jk2bt CLI 入口点
提供统一的命令行工具入口

命令:
    jk2bt-run          - 运行聚宽策略
    jk2bt-prewarm      - 预热数据样本（默认股票池）
    jk2bt-validate     - 验证缓存状态

使用方法:
    jk2bt-run strategy.txt --start 2023-01-01 --end 2023-12-31
    jk2bt-prewarm --start 2023-01-01 --end 2023-12-31
    jk2bt-validate
"""

import sys
import os
import argparse
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def run_strategy_main():
    """
    jk2bt-run 命令入口
    运行聚宽策略文件
    """
    from jk2bt.core.runner import run_jq_strategy

    parser = argparse.ArgumentParser(
        prog="jk2bt-run",
        description="运行聚宽策略文件进行本地回测"
    )
    parser.add_argument(
        "strategy_file",
        help="策略文件路径 (.txt 或 .py)"
    )
    parser.add_argument(
        "--start",
        default="2020-01-01",
        help="回测开始日期 (默认: 2020-01-01)"
    )
    parser.add_argument(
        "--end",
        default="2023-12-31",
        help="回测结束日期 (默认: 2023-12-31)"
    )
    parser.add_argument(
        "--capital",
        type=float,
        default=1000000,
        help="初始资金 (默认: 1000000)"
    )
    parser.add_argument(
        "--stocks",
        nargs="+",
        help="指定股票池 (可选，默认自动发现)"
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="离线模式，仅使用缓存数据"
    )
    parser.add_argument(
        "--frequency",
        default="daily",
        choices=["daily", "1m", "5m", "15m", "30m", "60m"],
        help="数据频率 (默认: daily)"
    )

    args = parser.parse_args()

    result = run_jq_strategy(
        strategy_file=args.strategy_file,
        start_date=args.start,
        end_date=args.end,
        initial_capital=args.capital,
        stock_pool=args.stocks,
        use_cache_only=args.offline,
        frequency=args.frequency,
    )

    if result is None:
        sys.exit(1)

    return result


def prewarm_main():
    """
    jk2bt-prewarm 命令入口
    预热数据样本
    """
    # 添加 tools 目录到 sys.path 以导入 prewarm_data
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tools_path = os.path.join(project_root, "tools", "data")
    if tools_path not in sys.path:
        sys.path.insert(0, tools_path)

    # 动态导入 prewarm_data 模块
    import importlib.util
    prewarm_path = os.path.join(tools_path, "prewarm_data.py")
    spec = importlib.util.spec_from_file_location("prewarm_data", prewarm_path)
    prewarm_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prewarm_module)

    parser = argparse.ArgumentParser(
        prog="jk2bt-prewarm",
        description="预热数据样本，支持默认股票池或自定义股票池"
    )
    parser.add_argument(
        "--stocks",
        nargs="+",
        help="股票池 (可选)"
    )
    parser.add_argument(
        "--etfs",
        nargs="+",
        help="ETF池 (可选)"
    )
    parser.add_argument(
        "--indexes",
        nargs="+",
        help="指数池 (可选)"
    )
    parser.add_argument(
        "--start",
        default="2023-01-01",
        help="开始日期 (默认: 2023-01-01)"
    )
    parser.add_argument(
        "--end",
        default="2023-12-31",
        help="结束日期 (默认: 2023-12-31)"
    )
    parser.add_argument(
        "--adjust",
        default="qfq",
        help="复权方式 (默认: qfq)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制更新，跳过已存在缓存"
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        default=True,
        help="使用默认样本股票池 (默认启用)"
    )

    args = parser.parse_args()

    # 使用默认样本池
    stock_pool = args.stocks
    etf_pool = args.etfs
    index_pool = args.indexes

    if args.sample or (not stock_pool and not etf_pool and not index_pool):
        if not stock_pool:
            stock_pool = prewarm_module.DEFAULT_SAMPLE_STOCKS
        if not etf_pool:
            etf_pool = prewarm_module.DEFAULT_SAMPLE_ETFS
        if not index_pool:
            index_pool = prewarm_module.DEFAULT_SAMPLE_INDEXES

    summary = prewarm_module.run_prewarm(
        stock_pool=stock_pool,
        etf_pool=etf_pool,
        index_pool=index_pool,
        start_date=args.start,
        end_date=args.end,
        adjust=args.adjust,
        force_update=args.force,
    )

    prewarm_module.print_summary(summary)

    return summary


def validate_cache_main():
    """
    jk2bt-validate 命令入口
    验证缓存状态
    """
    from jk2bt.db.cache_status import get_cache_manager

    parser = argparse.ArgumentParser(
        prog="jk2bt-validate",
        description="验证数据缓存状态"
    )
    parser.add_argument(
        "--stocks",
        nargs="+",
        help="验证指定股票池的缓存完整性"
    )
    parser.add_argument(
        "--start",
        default="2023-01-01",
        help="验证开始日期 (默认: 2023-01-01)"
    )
    parser.add_argument(
        "--end",
        default="2023-12-31",
        help="验证结束日期 (默认: 2023-12-31)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出"
    )

    args = parser.parse_args()

    cache_manager = get_cache_manager()

    print("=" * 60)
    print("缓存状态报告")
    print("=" * 60)

    # 获取整体摘要
    summary = cache_manager.get_cache_summary()

    print(f"\n缓存统计:")
    print(f"  股票数据: {summary['stock_count']} 只")
    print(f"  ETF数据: {summary['etf_count']} 只")
    print(f"  指数数据: {summary['index_count']} 只")
    print(f"  总记录数: {summary['total_records']}")

    # 检查元数据
    meta_status = cache_manager.check_meta_cache()
    print(f"\n元数据状态:")
    print(f"  交易日历: {'OK' if meta_status['trade_days'] else 'MISSING'}")
    print(f"  证券信息: {'OK' if meta_status['securities'] else 'MISSING'}")

    if meta_status['index_weights']:
        print(f"  指数权重: {list(meta_status['index_weights'].keys())}")

    # 如果指定了股票池，验证完整性
    if args.stocks:
        print(f"\n股票池缓存验证 ({len(args.stocks)} 只):")
        is_valid, report = cache_manager.validate_cache_for_offline(
            args.stocks, args.start, args.end
        )

        if is_valid:
            print(f"  状态: VALID - 所有股票缓存完整")
        else:
            print(f"  状态: INVALID")
            if report['missing_stocks']:
                print(f"  缺失股票: {report['missing_stocks']}")
            if report['incomplete_stocks']:
                print(f"  不完整股票:")
                for item in report['incomplete_stocks']:
                    print(f"    {item['symbol']}: {item['min_date']} ~ {item['max_date']}")

    print("=" * 60)

    if args.json:
        import json
        output = {
            "summary": summary,
            "meta_status": meta_status,
        }
        if args.stocks:
            is_valid, report = cache_manager.validate_cache_for_offline(
                args.stocks, args.start, args.end
            )
            output["validation"] = {
                "is_valid": is_valid,
                "report": report,
            }
        print(json.dumps(output, indent=2))

    return summary


# 入口点函数映射
ENTRY_POINTS = {
    "run": run_strategy_main,
    "prewarm": prewarm_main,
    "validate": validate_cache_main,
}


if __name__ == "__main__":
    # 支持直接运行: python -m jk2bt.cli <command>
    if len(sys.argv) < 2:
        print("使用方法: python -m jk2bt.cli <command>")
        print("可用命令: run, prewarm, validate")
        sys.exit(1)

    command = sys.argv[1]
    sys.argv = sys.argv[1:]  # 移除 cli 模块名

    if command in ENTRY_POINTS:
        ENTRY_POINTS[command]()
    else:
        print(f"未知命令: {command}")
        print("可用命令: run, prewarm, validate")
        sys.exit(1)