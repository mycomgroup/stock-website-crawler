#!/usr/bin/env python3
"""
prewarm_daily.py
预热日度数据

数据类型:
- 股票日线行情
- ETF日线行情
- 指数日线行情

建议更新周期: 每交易日收盘后
"""

import os
import sys
import argparse
import logging
from datetime import datetime, timedelta
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from tools.data.prewarm_data import (
    prewarm_meta_data,
    prewarm_stock_daily,
    prewarm_etf_daily,
    prewarm_index_daily,
    DEFAULT_SAMPLE_STOCKS,
    DEFAULT_SAMPLE_ETFS,
    DEFAULT_SAMPLE_INDEXES,
)


def run_prewarm_daily(
    stocks: list = None,
    etfs: list = None,
    indexes: list = None,
    start_date: str = None,
    end_date: str = None,
    force: bool = False,
    skip_existing: bool = True,
) -> dict:
    """执行日度数据预热"""
    
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    logger.info(f"时间范围: {start_date} ~ {end_date}")
    
    summary = {
        "start_date": start_date,
        "end_date": end_date,
        "force": force,
    }
    
    # 预热元数据
    logger.info("\n" + "=" * 60)
    logger.info("预热元数据...")
    meta_result = prewarm_meta_data(force_update=force)
    summary["meta"] = meta_result
    
    # 预热股票日线
    if stocks:
        logger.info("\n" + "=" * 60)
        stock_result = prewarm_stock_daily(
            stocks, start_date, end_date, 
            skip_existing=skip_existing, force_update=force
        )
        summary["stock_daily"] = stock_result
    
    # 预热ETF日线
    if etfs:
        logger.info("\n" + "=" * 60)
        etf_result = prewarm_etf_daily(
            etfs, start_date, end_date,
            skip_existing=skip_existing, force_update=force
        )
        summary["etf_daily"] = etf_result
    
    # 预热指数日线
    if indexes:
        logger.info("\n" + "=" * 60)
        index_result = prewarm_index_daily(
            indexes, start_date, end_date,
            skip_existing=skip_existing, force_update=force
        )
        summary["index_daily"] = index_result
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="预热日度数据")
    parser.add_argument("--stocks", nargs="+", help="股票代码列表")
    parser.add_argument("--etfs", nargs="+", help="ETF代码列表")
    parser.add_argument("--indexes", nargs="+", help="指数代码列表")
    parser.add_argument("--start", help="起始日期 (YYYY-MM-DD)")
    parser.add_argument("--end", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--force", action="store_true", help="强制更新")
    parser.add_argument("--sample", action="store_true", help="使用样本股票池")
    
    args = parser.parse_args()
    
    stocks = args.stocks
    etfs = args.etfs
    indexes = args.indexes
    
    if args.sample:
        stocks = stocks or DEFAULT_SAMPLE_STOCKS
        etfs = etfs or DEFAULT_SAMPLE_ETFS
        indexes = indexes or DEFAULT_SAMPLE_INDEXES
    
    summary = run_prewarm_daily(
        stocks=stocks,
        etfs=etfs,
        indexes=indexes,
        start_date=args.start,
        end_date=args.end,
        force=args.force,
    )
    
    print("\n" + "=" * 60)
    print("日度数据预热完成")
    print("=" * 60)
    print(f"股票: 成功={summary.get('stock_daily', {}).get('success', 0)}, 跳过={summary.get('stock_daily', {}).get('skipped', 0)}")
    print(f"ETF: 成功={summary.get('etf_daily', {}).get('success', 0)}, 跳过={summary.get('etf_daily', {}).get('skipped', 0)}")
    print(f"指数: 成功={summary.get('index_daily', {}).get('success', 0)}, 跳过={summary.get('index_daily', {}).get('skipped', 0)}")


if __name__ == "__main__":
    main()
