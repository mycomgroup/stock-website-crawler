#!/usr/bin/env python3
"""
prewarm_monthly.py
预热月度数据

数据类型:
- 指数成分股
- 指数权重
- 宏观指标

建议更新周期: 每月首日
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

from tools.offline_data.utils.progress import ProgressTracker
from tools.offline_data.utils.report import PrewarmReport

DEFAULT_INDEXES = ["000300.XSHG", "000905.XSHG", "000016.XSHG", "000852.XSHG", "399006.XSHE"]


def prewarm_index_components(indexes: list, force: bool = False) -> dict:
    """预热指数成分股和权重"""
    logger.info("=" * 60)
    logger.info("预热指数成分股...")
    logger.info("=" * 60)
    
    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}
    
    try:
        from jk2bt.market_data.index_components import (
            get_index_components,
            get_index_weights,
        )
        
        progress = ProgressTracker(len(indexes), "指数成分")
        progress.start()
        
        for index in indexes:
            try:
                df = get_index_components(index, force_update=force)
                if not df.empty:
                    result["success"] += 1
                    progress.update(success=True)
                else:
                    result["skipped"] += 1
                    progress.update(success=True, skipped=True)
            except Exception as e:
                result["failed"] += 1
                result["errors"].append(f"{index}: {e}")
                progress.update(success=False)
            
            time.sleep(0.5)
        
        progress.finish()
    
    except Exception as e:
        logger.error(f"预热指数成分失败: {e}")
        result["errors"].append(str(e))
    
    return result


def prewarm_macro_data(force: bool = False) -> dict:
    """预热宏观数据"""
    logger.info("=" * 60)
    logger.info("预热宏观数据...")
    logger.info("=" * 60)
    
    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}
    
    indicators = ["gdp", "cpi", "ppi"]
    
    try:
        from jk2bt.finance_data.macro import get_macro_data
        
        progress = ProgressTracker(len(indicators), "宏观数据")
        progress.start()
        
        for indicator in indicators:
            try:
                df = get_macro_data(indicator, force_update=force)
                if not df.empty:
                    result["success"] += 1
                    progress.update(success=True)
                else:
                    result["skipped"] += 1
                    progress.update(success=True, skipped=True)
            except Exception as e:
                result["failed"] += 1
                result["errors"].append(f"{indicator}: {e}")
                progress.update(success=False)
            
            time.sleep(0.5)
        
        progress.finish()
    
    except Exception as e:
        logger.error(f"预热宏观数据失败: {e}")
        result["errors"].append(str(e))
    
    return result


def run_prewarm_monthly(
    indexes: list = None,
    force: bool = False,
    include_components: bool = True,
    include_macro: bool = True,
) -> dict:
    """执行月度数据预热"""
    if indexes is None:
        indexes = DEFAULT_INDEXES
    
    report = PrewarmReport()
    summary = {"indexes": indexes}
    
    if include_components:
        result = prewarm_index_components(indexes, force)
        report.set_summary("index_components", result)
        summary["index_components"] = result
    
    if include_macro:
        result = prewarm_macro_data(force)
        report.set_summary("macro", result)
        summary["macro"] = result
    
    report_file = report.generate()
    logger.info(f"报告已保存: {report_file}")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="预热月度数据")
    parser.add_argument("--indexes", nargs="+", help="指数代码列表")
    parser.add_argument("--force", action="store_true", help="强制更新")
    parser.add_argument("--no-components", action="store_true", help="跳过指数成分")
    parser.add_argument("--no-macro", action="store_true", help="跳过宏观数据")
    
    args = parser.parse_args()
    
    summary = run_prewarm_monthly(
        indexes=args.indexes,
        force=args.force,
        include_components=not args.no_components,
        include_macro=not args.no_macro,
    )
    
    print("\n月度数据预热完成")


if __name__ == "__main__":
    main()
