#!/usr/bin/env python3
"""
prewarm_all.py
一键预热所有数据

包含:
- 静态数据（公司信息、行业分类）
- 季度数据（分红、股东）
- 月度数据（指数成分、宏观）
- 周度数据（解禁、股东变动）
- 日度数据（行情）

使用方法:
    python prewarm_all.py
    python prewarm_all.py --skip-daily    # 跳过日线数据
    python prewarm_all.py --static-only   # 只预热静态数据
"""

import os
import sys
import argparse
import logging
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


def run_prewarm_all(
    stocks: list = None,
    pool: str = "custom",
    include_static: bool = True,
    include_quarterly: bool = True,
    include_monthly: bool = True,
    include_weekly: bool = True,
    include_daily: bool = False,
    force: bool = False,
) -> dict:
    """
    一键预热所有数据。
    
    参数
    ----
    stocks : 股票代码列表
    pool : 股票池名称
    include_static : 是否预热静态数据
    include_quarterly : 是否预热季度数据
    include_monthly : 是否预热月度数据
    include_weekly : 是否预热周度数据
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
    
    # 1. 静态数据
    if include_static:
        logger.info("\n[1/5] 预热静态数据...")
        try:
            from tools.offline_data.prewarm_static import run_prewarm_static
            result = run_prewarm_static(stocks=stocks, pool=pool, force=force)
            summary["results"]["static"] = result
        except Exception as e:
            logger.error(f"静态数据预热失败: {e}")
            summary["results"]["static"] = {"error": str(e)}
    
    # 2. 季度数据
    if include_quarterly:
        logger.info("\n[2/5] 预热季度数据...")
        try:
            from tools.offline_data.prewarm_quarterly import run_prewarm_quarterly
            result = run_prewarm_quarterly(stocks=stocks, pool=pool, force=force)
            summary["results"]["quarterly"] = result
        except Exception as e:
            logger.error(f"季度数据预热失败: {e}")
            summary["results"]["quarterly"] = {"error": str(e)}
    
    # 3. 月度数据
    if include_monthly:
        logger.info("\n[3/5] 预热月度数据...")
        try:
            from tools.offline_data.prewarm_monthly import run_prewarm_monthly
            result = run_prewarm_monthly(force=force)
            summary["results"]["monthly"] = result
        except Exception as e:
            logger.error(f"月度数据预热失败: {e}")
            summary["results"]["monthly"] = {"error": str(e)}
    
    # 4. 周度数据
    if include_weekly:
        logger.info("\n[4/5] 预热周度数据...")
        try:
            from tools.offline_data.prewarm_weekly import run_prewarm_weekly
            result = run_prewarm_weekly(stocks=stocks, pool=pool, force=force)
            summary["results"]["weekly"] = result
        except Exception as e:
            logger.error(f"周度数据预热失败: {e}")
            summary["results"]["weekly"] = {"error": str(e)}
    
    # 5. 日度数据
    if include_daily:
        logger.info("\n[5/5] 预热日度数据...")
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
            success = result.get("success", result.get("company_info", {}).get("success", 0))
            failed = result.get("failed", 0)
            print(f"  {category}: 成功={success}, 失败={failed}")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="一键预热所有数据")
    parser.add_argument("--stocks", nargs="+", help="股票代码列表")
    parser.add_argument("--pool", default="custom", help="股票池名称")
    parser.add_argument("--force", action="store_true", help="强制更新")
    parser.add_argument("--static-only", action="store_true", help="只预热静态数据")
    parser.add_argument("--skip-daily", action="store_true", help="跳过日线数据（默认已跳过）")
    parser.add_argument("--include-daily", action="store_true", help="包含日线数据")
    
    args = parser.parse_args()
    
    run_prewarm_all(
        stocks=args.stocks,
        pool=args.pool,
        force=args.force,
        include_static=not args.static_only or args.static_only,
        include_quarterly=not args.static_only,
        include_monthly=not args.static_only,
        include_weekly=not args.static_only,
        include_daily=args.include_daily,
    )


if __name__ == "__main__":
    main()
