#!/usr/bin/env python3
"""
prewarm_static.py
预热公司基本信息（季度更新）

建议使用核心模块的 prewarm_company_info_cache() 批量预热。

使用方法:
    python prewarm_static.py
    python prewarm_static.py --pool core
    python prewarm_static.py --stocks 600519.XSHG 000858.XSHE
    python prewarm_static.py --force
"""

import os
import sys
import argparse

from jk2bt.logging import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

_project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import jk2bt

from tools.offline_data.utils.stock_pool import get_stock_pool


def run_prewarm_static(
    stocks: list = None,
    pool: str = "custom",
    force: bool = False,
) -> dict:
    """
    执行公司信息预热。

    返回: 汇总结果字典
    """
    if stocks is None:
        stocks = get_stock_pool(pool)

    logger.info(f"股票池: {len(stocks)} 只")
    logger.info(f"强制更新: {force}")

    summary = {"total_stocks": len(stocks), "force": force}

    try:
        from jk2bt.data.finance.company_info import prewarm_company_info_cache

        cache_result = prewarm_company_info_cache(stocks, use_duckdb=True)
        success = sum(1 for v in cache_result.values() if v)
        failed = sum(1 for v in cache_result.values() if not v)

        summary["company_info"] = {
            "success": success,
            "failed": failed,
            "errors": [],
        }

        logger.info(f"公司信息预热完成: 成功={success}, 失败={failed}")

    except Exception as e:
        logger.error(f"预热公司信息失败: {e}")
        summary["company_info"] = {
            "success": 0,
            "failed": len(stocks),
            "errors": [str(e)],
        }

    return summary


def main():
    parser = argparse.ArgumentParser(description="预热公司基本信息")
    parser.add_argument("--stocks", nargs="+", help="股票代码列表")
    parser.add_argument(
        "--pool", default="custom", help="股票池名称 (custom/core/extended)"
    )
    parser.add_argument("--force", action="store_true", help="强制更新")

    args = parser.parse_args()

    summary = run_prewarm_static(
        stocks=args.stocks,
        pool=args.pool,
        force=args.force,
    )

    print("\n" + "=" * 60)
    print("公司信息预热完成")
    print("=" * 60)
    result = summary.get("company_info", {})
    print(f"成功={result.get('success', 0)}, 失败={result.get('failed', 0)}")


if __name__ == "__main__":
    main()
