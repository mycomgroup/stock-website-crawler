#!/usr/bin/env python3
"""
prewarm_static.py
预热静态数据（季度更新）

数据类型:
- 公司基本信息 (STK_COMPANY_BASIC_INFO)
- 申万行业分类 (STK_INDUSTRY_SW)
- 公司状态变动 (STK_STATUS_CHANGE)

建议更新周期: 每季度初

使用方法:
    python prewarm_static.py
    python prewarm_static.py --pool core
    python prewarm_static.py --stocks 600519.XSHG 000858.XSHE
    python prewarm_static.py --force
"""

import os
import sys
import argparse
import logging
from datetime import datetime
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

_project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# 需要先导入 src
jk2bt.

from tools.offline_data.utils.stock_pool import get_stock_pool, DEFAULT_STOCKS
from tools.offline_data.utils.progress import ProgressTracker
from tools.offline_data.utils.report import PrewarmReport


def prewarm_company_info(stocks: list, force: bool = False) -> dict:
    """
    预热公司基本信息。

    返回: {success: int, failed: int, skipped: int, errors: list}
    """
    logger.info("=" * 60)
    logger.info("预热公司基本信息...")
    logger.info("=" * 60)

    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}

    try:
        from jk2bt.finance_data.company_info import (
            get_company_info,
            prewarm_company_info_cache,
        )

        # 使用批量预热函数
        if hasattr(prewarm_company_info_cache, "__call__"):
            cache_result = prewarm_company_info_cache(stocks, use_duckdb=True)
            result["success"] = sum(1 for v in cache_result.values() if v)
            result["failed"] = sum(1 for v in cache_result.values() if not v)
        else:
            # 回退到逐个获取
            progress = ProgressTracker(len(stocks), "公司信息")
            progress.start()

            for stock in stocks:
                try:
                    df = get_company_info(stock, force_update=force)
                    if not df.empty:
                        result["success"] += 1
                        progress.update(success=True)
                    else:
                        result["failed"] += 1
                        progress.update(success=False)
                except Exception as e:
                    result["failed"] += 1
                    result["errors"].append(f"{stock}: {e}")
                    progress.update(success=False)

                time.sleep(0.3)

            progress.finish()

    except Exception as e:
        logger.error(f"预热公司信息失败: {e}")
        result["errors"].append(str(e))

    return result


def prewarm_industry_sw(stocks: list, force: bool = False) -> dict:
    """
    预热申万行业分类。
    """
    logger.info("=" * 60)
    logger.info("预热申万行业分类...")
    logger.info("=" * 60)

    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}

    try:
        from jk2bt.market_data.industry_sw import (
            get_industry_sw,
            get_industry_sw_batch,
        )

        progress = ProgressTracker(len(stocks), "行业分类")
        progress.start()

        for stock in stocks:
            try:
                df = get_industry_sw(stock, use_cache=not force)
                # 检查是否成功（df 可能是 RobustResult 或 DataFrame）
                if hasattr(df, "success"):
                    # RobustResult 对象
                    if df.success and not df.is_empty():
                        result["success"] += 1
                        progress.update(success=True)
                    else:
                        result["skipped"] += 1
                        progress.update(success=True, skipped=True)
                elif not df.empty:
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
        logger.error(f"预热行业分类失败: {e}")
        result["errors"].append(str(e))

    return result


def prewarm_security_status(stocks: list, force: bool = False) -> dict:
    """
    预热公司状态变动（停牌/复牌信息）。
    """
    logger.info("=" * 60)
    logger.info("预热公司状态变动...")
    logger.info("=" * 60)

    result = {"success": 0, "failed": 0, "skipped": 0, "errors": []}

    try:
        from jk2bt.finance_data.company_info import (
            get_security_status,
        )

        progress = ProgressTracker(len(stocks), "状态变动")
        progress.start()

        for stock in stocks:
            try:
                df = get_security_status(stock, force_update=force)
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
        logger.error(f"预热状态变动失败: {e}")
        result["errors"].append(str(e))

    return result


def run_prewarm_static(
    stocks: list = None,
    pool: str = "custom",
    force: bool = False,
    include_company_info: bool = True,
    include_industry: bool = True,
    include_status: bool = True,
) -> dict:
    """
    执行静态数据预热。

    返回: 汇总结果字典
    """
    if stocks is None:
        stocks = get_stock_pool(pool)

    logger.info(f"股票池: {len(stocks)} 只")
    logger.info(f"强制更新: {force}")

    report = PrewarmReport()
    summary = {"total_stocks": len(stocks), "force": force}

    if include_company_info:
        result = prewarm_company_info(stocks, force)
        report.set_summary("company_info", result)
        summary["company_info"] = result

    if include_industry:
        result = prewarm_industry_sw(stocks, force)
        report.set_summary("industry_sw", result)
        summary["industry_sw"] = result

    if include_status:
        result = prewarm_security_status(stocks, force)
        report.set_summary("security_status", result)
        summary["security_status"] = result

    report_file = report.generate()
    logger.info(f"报告已保存: {report_file}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="预热静态数据")
    parser.add_argument("--stocks", nargs="+", help="股票代码列表")
    parser.add_argument(
        "--pool", default="custom", help="股票池名称 (custom/core/extended)"
    )
    parser.add_argument("--force", action="store_true", help="强制更新")
    parser.add_argument("--no-company", action="store_true", help="跳过公司信息")
    parser.add_argument("--no-industry", action="store_true", help="跳过行业分类")
    parser.add_argument("--no-status", action="store_true", help="跳过状态变动")

    args = parser.parse_args()

    summary = run_prewarm_static(
        stocks=args.stocks,
        pool=args.pool,
        force=args.force,
        include_company_info=not args.no_company,
        include_industry=not args.no_industry,
        include_status=not args.no_status,
    )

    print("\n" + "=" * 60)
    print("预热完成")
    print("=" * 60)
    for key, val in summary.items():
        if isinstance(val, dict):
            print(
                f"{key}: 成功={val.get('success', 0)}, 失败={val.get('failed', 0)}, 跳过={val.get('skipped', 0)}"
            )


if __name__ == "__main__":
    main()
