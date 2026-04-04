"""
prewarm_data.py
数据预热脚本 - 批量预加载日线策略所需数据。

功能：
1. 预热股票/ETF日线数据
2. 预热交易日历
3. 预热证券基础信息
4. 预热常见基础面数据
5. 支持指定股票池和时间范围
6. 支持"缓存已存在则跳过"

使用方法：
    python prewarm_data.py --stocks 600519.XSHG 000858.XSHE --start 2023-01-01 --end 2023-12-31
    python prewarm_data.py --sample-pool沪深300 --start 2022-01-01 --end 2024-12-31
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from typing import List, Dict, Optional
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from jk2bt.db.cache_status import (
    CacheManager,
    get_cache_manager,
)
from jk2bt.db.duckdb_manager import DuckDBManager
from jk2bt.market_data.stock import get_stock_daily
from jk2bt.market_data.etf import get_etf_daily
from jk2bt.market_data.index import get_index_daily

DEFAULT_SAMPLE_STOCKS = [
    "600519.XSHG",  # 贵州茅台
    "000858.XSHE",  # 五粮液
    "000333.XSHE",  # 美的集团
    "600036.XSHG",  # 招商银行
    "601318.XSHG",  # 中国平安
    "000001.XSHE",  # 平安银行
    "601166.XSHG",  # 兴业银行
    "600000.XSHG",  # 浦发银行
    "000002.XSHE",  # 万科A
    "601398.XSHG",  # 工商银行
]

DEFAULT_SAMPLE_ETFS = [
    "510300",  # 沪深300ETF
    "510050",  # 上证50ETF
    "159915",  # 创业板ETF
    "512880",  # 证券ETF
]

DEFAULT_SAMPLE_INDEXES = [
    "000300",  # 沪深300
    "000905",  # 中证500
    "000016",  # 上证50
]


def prewarm_meta_data(cache_base_dir: str = None, force_update: bool = False) -> Dict:
    """
    预热元数据：交易日历、证券信息。

    Returns:
        Dict: 预热结果统计
    """
    logger.info("=" * 60)
    logger.info("预热元数据...")
    logger.info("=" * 60)

    if cache_base_dir is None:
        # 从统一配置获取缓存目录
        try:
            from jk2bt.utils.config import get_config
            config = get_config()
            cache_base_dir = config.cache.cache_dir
        except Exception:
            # fallback 到原有逻辑（向后兼容）
            utility_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cache_base_dir = os.path.join(utility_dir, "cache")

    result = {"trade_days": False, "securities": False, "errors": []}

    meta_cache_dir = os.path.join(cache_base_dir, "meta_cache")
    os.makedirs(meta_cache_dir, exist_ok=True)

    trade_days_file = os.path.join(meta_cache_dir, "trade_days.pkl")

    if not force_update and os.path.exists(trade_days_file):
        logger.info("  交易日历: 缓存已存在，跳过")
        result["trade_days"] = True
    else:
        try:
            logger.info("  交易日历: 从网络下载...")
            import akshare as ak

            df = ak.tool_trade_date_hist_sina()
            df.to_pickle(trade_days_file)
            logger.info(f"  交易日历: 成功缓存 {len(df)} 条记录")
            result["trade_days"] = True
        except Exception as e:
            logger.error(f"  交易日历: 下载失败 - {e}")
            result["errors"].append(f"trade_days: {e}")

    securities_file = os.path.join(
        meta_cache_dir, f"securities_{datetime.now().strftime('%Y%m%d')}.pkl"
    )

    if not force_update and os.path.exists(securities_file):
        logger.info("  证券信息: 缓存已存在，跳过")
        result["securities"] = True
    else:
        try:
            logger.info("  证券信息: 从网络下载...")
            import akshare as ak

            df = ak.stock_info_a_code_name()
            df["code"] = df["code"].apply(
                lambda x: (
                    "sz" + x
                    if x.startswith(("0", "3"))
                    else ("sh" + x if x.startswith("6") else x)
                )
            )
            df.to_pickle(securities_file)
            logger.info(f"  证券信息: 成功缓存 {len(df)} 条记录")
            result["securities"] = True
        except Exception as e:
            logger.error(f"  证券信息: 下载失败 - {e}")
            result["errors"].append(f"securities: {e}")

    return result


def prewarm_stock_daily(
    stock_pool: List[str],
    start_date: str,
    end_date: str,
    adjust: str = "qfq",
    skip_existing: bool = True,
    force_update: bool = False,
) -> Dict:
    """
    预热股票日线数据。

    Returns:
        Dict: {'success': int, 'skipped': int, 'failed': List[str], 'errors': List[str]}
    """
    logger.info("=" * 60)
    logger.info(f"预热股票日线数据: {len(stock_pool)}只, {start_date} ~ {end_date}")
    logger.info("=" * 60)

    result = {"success": 0, "skipped": 0, "failed": [], "errors": []}

    cache_manager = get_cache_manager()

    for i, stock in enumerate(stock_pool, 1):
        ak_code = stock
        if stock.endswith(".XSHG"):
            ak_code = "sh" + stock[:6]
        elif stock.endswith(".XSHE"):
            ak_code = "sz" + stock[:6]
        elif not stock.startswith("sh") and not stock.startswith("sz"):
            ak_code = ("sh" if stock.startswith("6") else "sz") + stock.zfill(6)

        logger.info(f"  [{i}/{len(stock_pool)}] {stock} ({ak_code})")

        if skip_existing and not force_update:
            status = cache_manager.check_stock_daily_cache(
                ak_code, start_date, end_date, adjust
            )
            if status["is_complete"]:
                logger.info(f"    缓存已存在且完整，跳过")
                result["skipped"] += 1
                continue

        try:
            df = get_stock_daily(
                ak_code, start_date, end_date, force_update=True, adjust=adjust
            )
            if df is not None and not df.empty:
                logger.info(f"    成功: {len(df)} 条记录")
                result["success"] += 1
            else:
                logger.warning(f"    失败: 无数据")
                result["failed"].append(stock)
        except Exception as e:
            logger.error(f"    失败: {e}")
            result["failed"].append(stock)
            result["errors"].append(f"{stock}: {e}")

        time.sleep(0.3)

    return result


def prewarm_etf_daily(
    etf_pool: List[str],
    start_date: str,
    end_date: str,
    skip_existing: bool = True,
    force_update: bool = False,
) -> Dict:
    """
    预热ETF日线数据。

    Returns:
        Dict: 预热结果统计
    """
    logger.info("=" * 60)
    logger.info(f"预热ETF日线数据: {len(etf_pool)}只, {start_date} ~ {end_date}")
    logger.info("=" * 60)

    result = {"success": 0, "skipped": 0, "failed": [], "errors": []}

    cache_manager = get_cache_manager()

    for i, etf in enumerate(etf_pool, 1):
        logger.info(f"  [{i}/{len(etf_pool)}] {etf}")

        if skip_existing and not force_update:
            status = cache_manager.check_etf_daily_cache(etf, start_date, end_date)
            if status["is_complete"]:
                logger.info(f"    缓存已存在且完整，跳过")
                result["skipped"] += 1
                continue

        try:
            df = get_etf_daily(etf, start_date, end_date, force_update=True)
            if df is not None and not df.empty:
                logger.info(f"    成功: {len(df)} 条记录")
                result["success"] += 1
            else:
                logger.warning(f"    失败: 无数据")
                result["failed"].append(etf)
        except Exception as e:
            logger.error(f"    失败: {e}")
            result["failed"].append(etf)
            result["errors"].append(f"{etf}: {e}")

        time.sleep(0.3)

    return result


def prewarm_index_daily(
    index_pool: List[str],
    start_date: str,
    end_date: str,
    skip_existing: bool = True,
    force_update: bool = False,
) -> Dict:
    """
    预热指数日线数据。

    Returns:
        Dict: 预热结果统计
    """
    logger.info("=" * 60)
    logger.info(f"预热指数日线数据: {len(index_pool)}只, {start_date} ~ {end_date}")
    logger.info("=" * 60)

    result = {"success": 0, "skipped": 0, "failed": [], "errors": []}

    cache_manager = get_cache_manager()

    for i, index in enumerate(index_pool, 1):
        logger.info(f"  [{i}/{len(index_pool)}] {index}")

        if skip_existing and not force_update:
            status = cache_manager.check_index_daily_cache(index, start_date, end_date)
            if status["is_complete"]:
                logger.info(f"    缓存已存在且完整，跳过")
                result["skipped"] += 1
                continue

        try:
            df = get_index_daily(index, start_date, end_date, force_update=True)
            if df is not None and not df.empty:
                logger.info(f"    成功: {len(df)} 条记录")
                result["success"] += 1
            else:
                logger.warning(f"    失败: 无数据")
                result["failed"].append(index)
        except Exception as e:
            logger.error(f"    失败: {e}")
            result["failed"].append(index)
            result["errors"].append(f"{index}: {e}")

        time.sleep(0.3)

    return result


def prewarm_index_weights(
    index_pool: List[str],
    cache_base_dir: str = None,
    force_update: bool = False,
) -> Dict:
    """
    预热指数成分权重数据。

    Returns:
        Dict: 预热结果统计
    """
    logger.info("=" * 60)
    logger.info(f"预热指数成分权重: {len(index_pool)}只")
    logger.info("=" * 60)

    if cache_base_dir is None:
        # 从统一配置获取缓存目录
        try:
            from jk2bt.utils.config import get_config
            config = get_config()
            cache_base_dir = config.cache.cache_dir
        except Exception:
            # fallback 到原有逻辑（向后兼容）
            utility_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            cache_base_dir = os.path.join(utility_dir, "cache")

    result = {"success": 0, "skipped": 0, "failed": [], "errors": []}

    index_cache_dir = os.path.join(cache_base_dir, "index_cache")
    os.makedirs(index_cache_dir, exist_ok=True)

    for i, index in enumerate(index_pool, 1):
        index_num = index.zfill(6)
        cache_file = os.path.join(index_cache_dir, f"{index_num}_weights.pkl")

        logger.info(f"  [{i}/{len(index_pool)}] {index}")

        if not force_update and os.path.exists(cache_file):
            mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if (datetime.now() - mtime).days < 7:
                logger.info(f"    缓存已存在且新鲜，跳过")
                result["skipped"] += 1
                continue

        try:
            import akshare as ak

            df = ak.index_stock_cons_weight_csindex(symbol=index_num)
            if df is not None and not df.empty:
                df.to_pickle(cache_file)
                logger.info(f"    成功: {len(df)} 条记录")
                result["success"] += 1
            else:
                logger.warning(f"    失败: 无数据")
                result["failed"].append(index)
        except Exception as e:
            logger.error(f"    失败: {e}")
            result["failed"].append(index)
            result["errors"].append(f"{index}: {e}")

        time.sleep(0.3)

    return result


def run_prewarm(
    stock_pool: List[str] = None,
    etf_pool: List[str] = None,
    index_pool: List[str] = None,
    start_date: str = "2023-01-01",
    end_date: str = "2023-12-31",
    adjust: str = "qfq",
    skip_existing: bool = True,
    force_update: bool = False,
    include_meta: bool = True,
    include_weights: bool = True,
) -> Dict:
    """
    执行完整的数据预热流程。

    Returns:
        Dict: 预热结果汇总
    """
    logger.info("=" * 60)
    logger.info("开始数据预热流程")
    logger.info(f"时间范围: {start_date} ~ {end_date}")
    logger.info(f"复权方式: {adjust}")
    logger.info("=" * 60)

    summary = {
        "start_time": datetime.now().isoformat(),
        "config": {
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust,
            "stock_count": len(stock_pool or []),
            "etf_count": len(etf_pool or []),
            "index_count": len(index_pool or []),
        },
        "results": {},
    }

    if include_meta:
        meta_result = prewarm_meta_data(force_update=force_update)
        summary["results"]["meta"] = meta_result

    if stock_pool:
        stock_result = prewarm_stock_daily(
            stock_pool, start_date, end_date, adjust, skip_existing, force_update
        )
        summary["results"]["stock"] = stock_result

    if etf_pool:
        etf_result = prewarm_etf_daily(
            etf_pool, start_date, end_date, skip_existing, force_update
        )
        summary["results"]["etf"] = etf_result

    if index_pool:
        index_result = prewarm_index_daily(
            index_pool, start_date, end_date, skip_existing, force_update
        )
        summary["results"]["index"] = index_result

        if include_weights:
            weights_result = prewarm_index_weights(
                index_pool, force_update=force_update
            )
            summary["results"]["weights"] = weights_result

    summary["end_time"] = datetime.now().isoformat()

    cache_manager = get_cache_manager()
    summary["cache_summary"] = cache_manager.get_cache_summary()

    return summary


def print_summary(summary: Dict):
    """打印预热结果摘要"""
    print("\n" + "=" * 60)
    print("数据预热完成")
    print("=" * 60)

    print(f"\n配置:")
    print(
        f"  时间范围: {summary['config']['start_date']} ~ {summary['config']['end_date']}"
    )
    print(f"  股票池: {summary['config']['stock_count']}只")
    print(f"  ETF池: {summary['config']['etf_count']}只")
    print(f"  指数池: {summary['config']['index_count']}只")

    print(f"\n结果:")
    if "meta" in summary["results"]:
        meta = summary["results"]["meta"]
        print(f"  元数据:")
        print(f"    交易日历: {'✓' if meta['trade_days'] else '✗'}")
        print(f"    证券信息: {'✓' if meta['securities'] else '✗'}")

    if "stock" in summary["results"]:
        stock = summary["results"]["stock"]
        print(f"  股票日线:")
        print(f"    成功: {stock['success']}")
        print(f"    跳过: {stock['skipped']}")
        print(f"    失败: {len(stock['failed'])}")

    if "etf" in summary["results"]:
        etf = summary["results"]["etf"]
        print(f"  ETF日线:")
        print(f"    成功: {etf['success']}")
        print(f"    跳过: {etf['skipped']}")
        print(f"    失败: {len(etf['failed'])}")

    if "index" in summary["results"]:
        index = summary["results"]["index"]
        print(f"  指数日线:")
        print(f"    成功: {index['success']}")
        print(f"    跳过: {index['skipped']}")
        print(f"    失败: {len(index['failed'])}")

    cache = summary.get("cache_summary", {})
    print(f"\n缓存统计:")
    print(f"  股票数据: {cache.get('stock_count', 0)}只")
    print(f"  ETF数据: {cache.get('etf_count', 0)}只")
    print(f"  指数数据: {cache.get('index_count', 0)}只")
    print(f"  总记录数: {cache.get('total_records', 0)}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="数据预热脚本")
    parser.add_argument("--stocks", nargs="+", help="股票池")
    parser.add_argument("--etfs", nargs="+", help="ETF池")
    parser.add_argument("--indexes", nargs="+", help="指数池")
    parser.add_argument("--start", default="2023-01-01", help="开始日期")
    parser.add_argument("--end", default="2023-12-31", help="结束日期")
    parser.add_argument("--adjust", default="qfq", help="复权方式")
    parser.add_argument("--force", action="store_true", help="强制更新")
    parser.add_argument("--sample", action="store_true", help="使用样本股票池")

    args = parser.parse_args()

    stock_pool = args.stocks
    etf_pool = args.etfs
    index_pool = args.indexes

    if args.sample:
        if not stock_pool:
            stock_pool = DEFAULT_SAMPLE_STOCKS
        if not etf_pool:
            etf_pool = DEFAULT_SAMPLE_ETFS
        if not index_pool:
            index_pool = DEFAULT_SAMPLE_INDEXES

    summary = run_prewarm(
        stock_pool=stock_pool,
        etf_pool=etf_pool,
        index_pool=index_pool,
        start_date=args.start,
        end_date=args.end,
        adjust=args.adjust,
        force_update=args.force,
    )

    print_summary(summary)

    return summary


if __name__ == "__main__":
    main()
