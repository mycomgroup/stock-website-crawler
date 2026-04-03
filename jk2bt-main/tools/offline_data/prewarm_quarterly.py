#!/usr/bin/env python3
"""
prewarm_quarterly.py
预热季度数据（财报季后更新）

数据类型:
- 分红送股 (STK_XR_XD)
- 十大股东 (STK_SHAREHOLDER_TOP10)
- 股东户数 (STK_SHAREHOLDER_NUM)

建议更新周期: 财报季后（1/4/7/10月下旬）

使用方法:
    python prewarm_quarterly.py
    python prewarm_quarterly.py --pool core
    python prewarm_quarterly.py --stocks 600519.XSHG --force
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

from tools.offline_data.utils.stock_pool import get_stock_pool
from tools.offline_data.utils.progress import ProgressTracker
from tools.offline_data.utils.report import PrewarmReport


def prewarm_dividend(stocks: list, force: bool = False) -> dict:
    """预热分红送股数据"""
    logger.info("=" * 60)
    logger.info("预热分红送股数据...")
    logger.info("=" * 60)
    
    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}
    
    try:
        from jk2bt.finance_data.dividend import get_dividend_info
        
        progress = ProgressTracker(len(stocks), "分红送股")
        progress.start()
        
        for stock in stocks:
            try:
                df = get_dividend_info(stock, force_update=force)
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
        logger.error(f"预热分红数据失败: {e}")
        result["errors"].append(str(e))
    
    return result


def prewarm_shareholders(stocks: list, force: bool = False) -> dict:
    """预热股东信息"""
    logger.info("=" * 60)
    logger.info("预热股东信息...")
    logger.info("=" * 60)
    
    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}
    
    try:
        from jk2bt.finance_data.shareholder import (
            get_top10_shareholders,
            get_top10_float_shareholders,
            get_shareholder_count,
        )
        
        progress = ProgressTracker(len(stocks), "股东信息")
        progress.start()
        
        for stock in stocks:
            try:
                # 十大股东
                df1 = get_top10_shareholders(stock, force_update=force)
                # 十大流通股东
                df2 = get_top10_float_shareholders(stock, force_update=force)
                # 股东户数
                df3 = get_shareholder_count(stock, force_update=force)
                
                if not df1.empty or not df2.empty or not df3.empty:
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
        logger.error(f"预热股东信息失败: {e}")
        result["errors"].append(str(e))
    
    return result


def run_prewarm_quarterly(
    stocks: list = None,
    pool: str = "custom",
    force: bool = False,
    include_dividend: bool = True,
    include_shareholders: bool = True,
) -> dict:
    """执行季度数据预热"""
    if stocks is None:
        stocks = get_stock_pool(pool)
    
    logger.info(f"股票池: {len(stocks)} 只")
    
    report = PrewarmReport()
    summary = {"total_stocks": len(stocks)}
    
    if include_dividend:
        result = prewarm_dividend(stocks, force)
        report.set_summary("dividend", result)
        summary["dividend"] = result
    
    if include_shareholders:
        result = prewarm_shareholders(stocks, force)
        report.set_summary("shareholders", result)
        summary["shareholders"] = result
    
    report_file = report.generate()
    logger.info(f"报告已保存: {report_file}")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="预热季度数据")
    parser.add_argument("--stocks", nargs="+", help="股票代码列表")
    parser.add_argument("--pool", default="custom", help="股票池名称")
    parser.add_argument("--force", action="store_true", help="强制更新")
    parser.add_argument("--no-dividend", action="store_true", help="跳过分红数据")
    parser.add_argument("--no-shareholders", action="store_true", help="跳过股东数据")
    
    args = parser.parse_args()
    
    summary = run_prewarm_quarterly(
        stocks=args.stocks,
        pool=args.pool,
        force=args.force,
        include_dividend=not args.no_dividend,
        include_shareholders=not args.no_shareholders,
    )
    
    print("\n预热完成")
    for key, val in summary.items():
        if isinstance(val, dict):
            print(f"{key}: 成功={val.get('success', 0)}, 失败={val.get('failed', 0)}")


if __name__ == "__main__":
    main()
