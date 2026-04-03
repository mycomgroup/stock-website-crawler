#!/usr/bin/env python3
"""
prewarm_weekly.py
预热周度数据

数据类型:
- 限售解禁 (STK_RESTRICTED_RELEASE)
- 股东变动 (STK_SHAREHOLDER_CHANGE)

建议更新周期: 每周一
"""

import os
import sys
import argparse
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from tools.offline_data.utils.stock_pool import get_stock_pool
from tools.offline_data.utils.progress import ProgressTracker
from tools.offline_data.utils.report import PrewarmReport


def prewarm_unlock_data(stocks: list, force: bool = False) -> dict:
    """预热限售解禁数据"""
    logger.info("=" * 60)
    logger.info("预热限售解禁数据...")
    logger.info("=" * 60)
    
    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}
    
    try:
        from jk2bt.finance_data.unlock import get_unlock_schedule
        
        progress = ProgressTracker(len(stocks), "解禁数据")
        progress.start()
        
        for stock in stocks:
            try:
                df = get_unlock_schedule(stock, force_update=force)
                if not df.empty:
                    result["success"] += 1
                    progress.update(success=True)
                else:
                    result["skipped"] += 1
                    progress.update(success=True, skipped=True)
            except Exception as e:
                result["failed"] += 1
                result["errors"].append(f"{stock}: {e}")
                progress.update(success=False)
            
            time.sleep(0.3)
        
        progress.finish()
    
    except Exception as e:
        logger.error(f"预热解禁数据失败: {e}")
        result["errors"].append(str(e))
    
    return result


def prewarm_share_change(stocks: list, force: bool = False) -> dict:
    """预热股东变动数据"""
    logger.info("=" * 60)
    logger.info("预热股东变动数据...")
    logger.info("=" * 60)
    
    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}
    
    try:
        from jk2bt.finance_data.share_change import get_share_change
        
        progress = ProgressTracker(len(stocks), "股东变动")
        progress.start()
        
        for stock in stocks:
            try:
                df = get_share_change(stock, force_update=force)
                if not df.empty:
                    result["success"] += 1
                    progress.update(success=True)
                else:
                    result["skipped"] += 1
                    progress.update(success=True, skipped=True)
            except Exception as e:
                result["failed"] += 1
                result["errors"].append(f"{stock}: {e}")
                progress.update(success=False)
            
            time.sleep(0.3)
        
        progress.finish()
    
    except Exception as e:
        logger.error(f"预热股东变动失败: {e}")
        result["errors"].append(str(e))
    
    return result


def run_prewarm_weekly(
    stocks: list = None,
    pool: str = "custom",
    force: bool = False,
    include_unlock: bool = True,
    include_share_change: bool = True,
) -> dict:
    """执行周度数据预热"""
    if stocks is None:
        stocks = get_stock_pool(pool)
    
    logger.info(f"股票池: {len(stocks)} 只")
    
    report = PrewarmReport()
    summary = {"total_stocks": len(stocks)}
    
    if include_unlock:
        result = prewarm_unlock_data(stocks, force)
        report.set_summary("unlock", result)
        summary["unlock"] = result
    
    if include_share_change:
        result = prewarm_share_change(stocks, force)
        report.set_summary("share_change", result)
        summary["share_change"] = result
    
    report_file = report.generate()
    logger.info(f"报告已保存: {report_file}")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="预热周度数据")
    parser.add_argument("--stocks", nargs="+", help="股票代码列表")
    parser.add_argument("--pool", default="custom", help="股票池名称")
    parser.add_argument("--force", action="store_true", help="强制更新")
    
    args = parser.parse_args()
    
    summary = run_prewarm_weekly(
        stocks=args.stocks,
        pool=args.pool,
        force=args.force,
    )
    
    print("\n周度数据预热完成")


if __name__ == "__main__":
    main()
