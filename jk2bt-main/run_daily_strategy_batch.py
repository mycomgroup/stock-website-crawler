#!/usr/bin/env python3
"""
run_daily_strategy_batch.py
批量运行日线股票/ETF策略，建立第一批可靠基线策略白名单

使用方法:
    python run_daily_strategy_batch.py --strategies_dir jkcode/jkcode --output docs/0330_result/task13_white_list.json
"""

import os
import sys
import json
import traceback
from datetime import datetime
import argparse

try:
    from jk2bt.core.runner import run_jq_strategy
except ImportError as e:
    print(f"导入失败: {e}")
    print("请在仓库根目录运行此脚本，或设置 PYTHONPATH")
    sys.exit(1)


def scan_strategy_files(strategies_dir, limit=None):
    """
    扫描策略文件目录，返回txt文件列表

     参数:
         strategies_dir: 策略目录
         limit: 限制扫描数量（用于测试）

     返回:
         list: 策略文件路径列表
    """
    strategy_files = []

    for root, dirs, files in os.walk(strategies_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                strategy_files.append(file_path)

    strategy_files.sort()

    if limit:
        strategy_files = strategy_files[:limit]

    return strategy_files


def detect_strategy_type(strategy_file):
    """
    检测策略类型和依赖

     返回:
         dict: {
             'is_daily': bool,
             'has_minute': bool,
             'has_futures': bool,
             'has_ml': bool,
             'has_file_io': bool,
             'apis_used': list
         }
    """
    try:
        with open(strategy_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except:
        try:
            with open(strategy_file, "r", encoding="gbk", errors="ignore") as f:
                content = f.read()
        except:
            return {
                "is_daily": False,
                "has_minute": True,
                "has_futures": False,
                "has_ml": False,
                "has_file_io": False,
                "apis_used": [],
                "error": "无法读取文件",
            }

    has_minute = False
    minute_patterns = [
        "frequency='1m'",
        "frequency='5m'",
        "frequency='15m'",
        "frequency='30m'",
        "frequency='60m'",
        "unit='1m'",
        "unit='5m'",
        "unit='15m'",
        "get_ticks(",
        "current_price(",
        "分钟级",
        "分钟数据",
        "分钟线",
    ]
    for pattern in minute_patterns:
        if pattern in content:
            has_minute = True
            break

    has_futures = any(
        keyword in content
        for keyword in [
            "期货",
            "future",
            "IF",
            "IC",
            "IH",
            "TF",
            "T",
            "TS",
            "主力合约",
            "get_dominant_contract",
        ]
    )

    has_ml = any(
        keyword in content
        for keyword in [
            "xgboost",
            "XGBoost",
            "sklearn",
            "机器学习",
            "随机森林",
            "RandomForest",
            "SVR",
            "SVR",
            "LSTM",
            "神经网络",
        ]
    )

    has_file_io = any(
        keyword in content
        for keyword in [
            "read_file",
            "write_file",
            "文件读写",
            "load_data",
            "save_data",
            "pickle",
            "csv",
        ]
    )

    apis_used = []
    api_patterns = [
        "get_price",
        "history",
        "attribute_history",
        "get_fundamentals",
        "get_index_weights",
        "get_index_stocks",
        "get_current_data",
        "run_daily",
        "run_monthly",
        "run_weekly",
        "order_target",
        "order_value",
        "order",
        "get_security_info",
        "get_all_securities",
    ]

    for api in api_patterns:
        if api in content:
            apis_used.append(api)

    is_daily = not has_minute and not has_ml and not has_futures

    return {
        "is_daily": is_daily,
        "has_minute": has_minute,
        "has_futures": has_futures,
        "has_ml": has_ml,
        "has_file_io": has_file_io,
        "apis_used": apis_used,
    }


def run_single_strategy(
    strategy_file,
    start_date="2020-01-01",
    end_date="2023-12-31",
    initial_capital=1000000,
):
    """
    运行单个策略并记录结果

     返回:
         dict: {
             'strategy_file': str,
             'strategy_name': str,
             'status': str ('success', 'failed', 'timeout', 'error'),
             'load_success': bool,
             'run_success': bool,
             'final_value': float,
             'pnl': float,
             'pnl_pct': float,
             'trades': int,
             'max_drawdown': float,
             'annual_return': float,
             'sharpe': float,
             'error_message': str,
             'execution_time': float,
             'apis_used': list
         }
    """
    import time

    start_time = time.time()

    result = {
        "strategy_file": strategy_file,
        "strategy_name": os.path.basename(strategy_file),
        "status": "unknown",
        "load_success": False,
        "run_success": False,
        "final_value": 0,
        "pnl": 0,
        "pnl_pct": 0,
        "trades": 0,
        "max_drawdown": 0,
        "annual_return": 0,
        "sharpe": 0,
        "error_message": "",
        "execution_time": 0,
        "apis_used": [],
    }

    strategy_type = detect_strategy_type(strategy_file)
    result["apis_used"] = strategy_type["apis_used"]

    if not strategy_type["is_daily"]:
        result["status"] = "skipped"
        result["error_message"] = (
            f"策略类型不符合日线要求: minute={strategy_type['has_minute']}, ml={strategy_type['has_ml']}"
        )
        return result

    try:
        print(f"\n{'=' * 80}")
        print(f"运行策略: {os.path.basename(strategy_file)}")
        print(f"{'=' * 80}")

        run_result = run_jq_strategy(
            strategy_file=strategy_file,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            auto_discover_stocks=True,
        )

        if run_result is None:
            result["status"] = "failed"
            result["error_message"] = "策略运行返回None"
            return result

        result["load_success"] = True
        result["run_success"] = True
        result["status"] = "success"
        result["final_value"] = run_result["final_value"]
        result["pnl"] = run_result["pnl"]
        result["pnl_pct"] = run_result["pnl_pct"]

        strategy = run_result["strategy"]

        if hasattr(strategy, "navs") and strategy.navs:
            import pandas as pd

            nav_series = pd.Series(strategy.navs)

            cummax = nav_series.cummax()
            drawdown = (nav_series - cummax) / cummax
            result["max_drawdown"] = drawdown.min()

            days = len(nav_series)
            result["annual_return"] = (run_result["final_value"] / initial_capital) ** (
                252 / days
            ) - 1

            returns = nav_series.pct_change().dropna()
            if returns.std() > 0:
                result["sharpe"] = returns.mean() / returns.std() * (252**0.5)

        if hasattr(strategy, "orders"):
            result["trades"] = len(strategy.orders)

    except FileNotFoundError as e:
        result["status"] = "failed"
        result["error_message"] = f"文件不存在: {e}"
    except SyntaxError as e:
        result["status"] = "failed"
        result["error_message"] = f"语法错误: {e}"
    except Exception as e:
        result["status"] = "error"
        result["error_message"] = f"{type(e).__name__}: {str(e)}"

        tb_lines = traceback.format_exc().split("\n")
        result["error_traceback"] = "\n".join(tb_lines[-10:])

    result["execution_time"] = time.time() - start_time

    return result


def run_batch_strategies(
    strategy_files,
    start_date="2020-01-01",
    end_date="2023-12-31",
    initial_capital=1000000,
):
    """
    批量运行策略

     返回:
         dict: {
             'total': int,
             'success': int,
             'failed': int,
             'skipped': int,
             'results': list
         }
    """
    results = []
    stats = {
        "total": len(strategy_files),
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "error": 0,
    }

    for i, strategy_file in enumerate(strategy_files, 1):
        print(f"\n[{i}/{len(strategy_files)}] 处理: {os.path.basename(strategy_file)}")

        result = run_single_strategy(
            strategy_file, start_date, end_date, initial_capital
        )
        results.append(result)

        if result["status"] == "success":
            stats["success"] += 1
        elif result["status"] == "skipped":
            stats["skipped"] += 1
        elif result["status"] == "failed":
            stats["failed"] += 1
        else:
            stats["error"] += 1

    return {"stats": stats, "results": results}


def generate_white_list_report(batch_result, output_file):
    """
    生成白名单报告

     参数:
         batch_result: 批量运行结果
         output_file: 输出文件路径
    """
    successful_strategies = []

    for result in batch_result["results"]:
        if result["status"] == "success":
            successful_strategies.append(
                {
                    "strategy_file": result["strategy_file"],
                    "strategy_name": result["strategy_name"],
                    "final_value": result["final_value"],
                    "pnl_pct": result["pnl_pct"],
                    "annual_return": result["annual_return"],
                    "max_drawdown": result["max_drawdown"],
                    "sharpe": result["sharpe"],
                    "trades": result["trades"],
                    "apis_used": result["apis_used"],
                    "execution_time": result["execution_time"],
                }
            )

    report = {
        "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": batch_result["stats"],
        "white_list": successful_strategies,
        "failed_strategies": [
            {
                "strategy_file": r["strategy_file"],
                "strategy_name": r["strategy_name"],
                "status": r["status"],
                "error_message": r["error_message"],
            }
            for r in batch_result["results"]
            if r["status"] != "success"
        ],
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n白名单报告已保存到: {output_file}")

    return report


def main():
    parser = argparse.ArgumentParser(description="批量运行日线策略并生成白名单")
    parser.add_argument("--strategies_dir", default="jkcode/jkcode", help="策略目录")
    parser.add_argument(
        "--output",
        default="docs/0330_result/task13_white_list.json",
        help="输出报告文件",
    )
    parser.add_argument("--start_date", default="2020-01-01", help="回测开始日期")
    parser.add_argument("--end_date", default="2023-12-31", help="回测结束日期")
    parser.add_argument("--capital", type=float, default=1000000, help="初始资金")
    parser.add_argument(
        "--limit", type=int, default=None, help="限制策略数量（用于测试）"
    )
    parser.add_argument(
        "--use-cache-only", action="store_true", help="离线模式，仅使用本地缓存"
    )
    parser.add_argument("--max-retries", type=int, default=3, help="最大重试次数")
    parser.add_argument("--retry-delay", type=int, default=2, help="重试间隔（秒）")

    args = parser.parse_args()

    print("=" * 80)
    print("Task 13: 日线股票/ETF策略基线跑通")
    print("=" * 80)
    print(f"策略目录: {args.strategies_dir}")
    print(f"输出报告: {args.output}")
    print(f"回测区间: {args.start_date} ~ {args.end_date}")
    print(f"初始资金: {args.capital}")
    if args.use_cache_only:
        print(f"运行模式: 离线模式（仅使用本地缓存）")

    strategy_files = scan_strategy_files(args.strategies_dir, args.limit)

    print(f"\n发现 {len(strategy_files)} 个策略文件")

    batch_result = run_batch_strategies(
        strategy_files,
        start_date=args.start_date,
        end_date=args.end_date,
        initial_capital=args.capital,
    )

    report = generate_white_list_report(batch_result, args.output)

    print("\n" + "=" * 80)
    print("运行总结:")
    print(f"  总数: {batch_result['stats']['total']}")
    print(f"  成功: {batch_result['stats']['success']}")
    print(f"  失败: {batch_result['stats']['failed']}")
    print(f"  跳过: {batch_result['stats']['skipped']}")
    print(f"  错误: {batch_result['stats']['error']}")
    print("=" * 80)

    print(f"\n白名单策略数: {len(report['white_list'])}")

    if report["white_list"]:
        print("\n前5个成功策略:")
        for i, s in enumerate(report["white_list"][:5], 1):
            print(f"{i}. {s['strategy_name']}")
            print(f"   年化收益: {s['annual_return']:.2%}")
            print(f"   最大回撤: {s['max_drawdown']:.2%}")
            print(f"   夏普比率: {s['sharpe']:.2f}")


if __name__ == "__main__":
    main()
