#!/usr/bin/env python3
"""
prewarm_all.py
一键预热所有数据

包含:
- 元数据（交易日历、证券列表）
- 公司信息
- 日度行情（可选）

使用方法:
    python prewarm_all.py
    python prewarm_all.py --include-daily    # 包含日线数据
    python prewarm_all.py --static-only      # 只预热静态数据
    python prewarm_all.py --force            # 强制更新
"""

import os
import sys
import argparse
from datetime import datetime

from jk2bt.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

_project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


def run_prewarm_all(
    stocks: list = None,
    pool: str = "custom",
    include_static: bool = True,
    include_daily: bool = False,
    force: bool = False,
) -> dict:
    """
    一键预热所有数据。

    参数
    ----
    stocks : 股票代码列表
    pool : 股票池名称
    include_static : 是否预热静态数据（元数据+公司信息）
    include_daily : 是否预热日度数据
    force : 强制更新

    返回
    ----
    dict : 汇总结果
    """
    start_time = datetime.now()

    logger.info("=" * 60)
    logger.info("开始一键预热所有数据")
    logger.info("=" * 60)

    summary = {
        "start_time": start_time.isoformat(),
        "pool": pool,
        "force": force,
        "results": {},
    }

    # 1. 元数据 + 公司信息
    if include_static:
        logger.info("\n[1/2] 预热元数据...")
        try:
            from jk2bt.data.storage.meta_cache_api import prewarm_meta_cache

            meta_result = prewarm_meta_cache(force_update=force)
            summary["results"]["meta"] = meta_result
            logger.info(f"元数据预热完成: {meta_result}")
        except Exception as e:
            logger.error(f"元数据预热失败: {e}")
            summary["results"]["meta"] = {"error": str(e)}

        logger.info("\n[2/2] 预热公司信息...")
        try:
            from tools.offline_data.prewarm_static import run_prewarm_static

            result = run_prewarm_static(stocks=stocks, pool=pool, force=force)
            summary["results"]["company_info"] = result
        except Exception as e:
            logger.error(f"公司信息预热失败: {e}")
            summary["results"]["company_info"] = {"error": str(e)}

    # 2. 日度数据
    if include_daily:
        label = "[3/3]" if include_static else "[1/1]"
        logger.info(f"\n{label} 预热日度数据...")
        try:
            from tools.offline_data.prewarm_daily import run_prewarm_daily

            result = run_prewarm_daily(force=force)
            summary["results"]["daily"] = result
        except Exception as e:
            logger.error(f"日度数据预热失败: {e}")
            summary["results"]["daily"] = {"error": str(e)}

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    summary["end_time"] = end_time.isoformat()
    summary["duration_seconds"] = duration

    # 打印总结
    print("\n" + "=" * 60)
    print("一键预热完成")
    print("=" * 60)
    print(f"总耗时: {duration:.1f} 秒")
    print(f"\n各类数据结果:")
    for category, result in summary["results"].items():
        if "error" in result:
            print(f"  {category}: 失败 - {result['error'][:50]}")
        elif isinstance(result, dict):
            success = result.get("success", 0)
            failed = result.get("failed", 0)
            print(f"  {category}: 成功={success}, 失败={failed}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="一键预热所有数据")
    parser.add_argument("--stocks", nargs="+", help="股票代码列表")
    parser.add_argument("--pool", default="custom", help="股票池名称")
    parser.add_argument("--force", action="store_true", help="强制更新")
    parser.add_argument("--static-only", action="store_true", help="只预热静态数据")
    parser.add_argument("--include-daily", action="store_true", help="包含日线数据")

    args = parser.parse_args()

    run_prewarm_all(
        stocks=args.stocks,
        pool=args.pool,
        force=args.force,
        include_static=not args.static_only or args.static_only,
        include_daily=args.include_daily,
    )


if __name__ == "__main__":
    main()
