"""
db/migrate.py
数据迁移工具：将现有的 pickle 缓存文件迁移到 DuckDB。
"""

import os
import glob
import re
import logging
from typing import List, Dict
import pandas as pd

from .parquet_adapter import ParquetAdapter

logger = logging.getLogger(__name__)


def parse_stock_pickle_filename(filename: str) -> Dict[str, str]:
    """
    解析股票 pickle 文件名。

    文件名格式：
    - sh600000_stock_qfq.pkl
    - 600000.XSHG_jq_qfq_daily.pkl
    - sh600519_daily.pkl

    返回
    ----
    dict: {'symbol': 'sh600000', 'adjust': 'qfq'}
    """
    basename = os.path.basename(filename)
    name = basename.replace(".pkl", "")

    parts = name.split("_")

    if len(parts) >= 2:
        symbol = parts[0]

        if not symbol.startswith(("sh", "sz", "60", "00", "30", "68")):
            if len(symbol) == 6 and symbol.isdigit():
                if symbol.startswith(("6", "9")):
                    symbol = "sh" + symbol
                elif symbol.startswith(("0", "3")):
                    symbol = "sz" + symbol

        adjust = "qfq"
        if "hfq" in parts:
            adjust = "hfq"
        elif "none" in parts:
            adjust = "none"

        return {"symbol": symbol, "adjust": adjust}

    return None


def parse_etf_pickle_filename(filename: str) -> Dict[str, str]:
    """
    解析 ETF pickle 文件名。

    文件名格式：
    - 510300.pkl

    返回
    ----
    dict: {'symbol': '510300'}
    """
    basename = os.path.basename(filename)
    name = basename.replace(".pkl", "")

    if name.isdigit() or (len(name) == 6 and name.startswith("51")):
        return {"symbol": name}

    return None


def parse_index_pickle_filename(filename: str) -> Dict[str, str]:
    """
    解析指数 pickle 文件名。

    文件名格式：
    - 000300.pkl

    返回
    ----
    dict: {'symbol': '000300'}
    """
    basename = os.path.basename(filename)
    name = basename.replace(".pkl", "")

    if name.isdigit() or (len(name) == 6):
        return {"symbol": name}

    return None


def migrate_stock_pickles(
    pickle_dir: str = "stock_cache", db: ParquetAdapter = None
) -> int:
    """
    迁移股票 pickle 文件到 Parquet。

    参数
    ----
    pickle_dir : str
        pickle 文件目录
    db : ParquetAdapter
        数据库管理器实例

    返回
    ----
    int
        成功迁移的文件数量
    """
    if db is None:
        db = ParquetAdapter()

    if not os.path.exists(pickle_dir):
        logger.warning(f"pickle 目录不存在: {pickle_dir}")
        return 0

    pkl_files = glob.glob(os.path.join(pickle_dir, "*.pkl"))

    if not pkl_files:
        logger.info(f"未找到股票 pickle 文件: {pickle_dir}")
        return 0

    logger.info(f"开始迁移股票数据：共 {len(pkl_files)} 个文件")
    success_count = 0

    for pkl_file in pkl_files:
        try:
            info = parse_stock_pickle_filename(pkl_file)

            if info is None:
                logger.warning(f"无法解析文件名: {pkl_file}")
                continue

            symbol = info["symbol"]
            adjust = info["adjust"]

            df = pd.read_pickle(pkl_file)

            if df is None or df.empty:
                logger.warning(f"文件为空: {pkl_file}")
                continue

            date_col = None
            for col in ["date", "datetime", "日期"]:
                if col in df.columns:
                    date_col = col
                    break

            if date_col is None:
                logger.warning(f"未找到日期列: {pkl_file}")
                continue

            df = df.copy()
            df["datetime"] = pd.to_datetime(df[date_col])

            cols_map = {
                "开盘": "open",
                "最高": "high",
                "最低": "low",
                "收盘": "close",
                "成交量": "volume",
                "成交额": "amount",
            }

            for old_col, new_col in cols_map.items():
                if old_col in df.columns and new_col not in df.columns:
                    df[new_col] = df[old_col]

            required_cols = ["datetime", "open", "high", "low", "close", "volume"]
            if not all(col in df.columns for col in required_cols):
                logger.warning(f"缺少必要列: {pkl_file}")
                continue

            db.insert_stock_daily(
                symbol,
                df[
                    required_cols + ["amount"]
                    if "amount" in df.columns
                    else required_cols
                ],
                adjust,
            )

            logger.info(f"迁移成功: {pkl_file} -> {symbol} ({adjust})")
            success_count += 1

        except Exception as e:
            logger.error(f"迁移失败 {pkl_file}: {e}")
            continue

    logger.info(f"股票数据迁移完成: {success_count}/{len(pkl_files)} 个文件成功")
    return success_count


def migrate_etf_pickles(
    pickle_dir: str = "etf_cache", db: ParquetAdapter = None
) -> int:
    """
    迁移 ETF pickle 文件到 Parquet。
    """
    if db is None:
        db = ParquetAdapter()

    if not os.path.exists(pickle_dir):
        logger.warning(f"pickle 目录不存在: {pickle_dir}")
        return 0

    pkl_files = glob.glob(os.path.join(pickle_dir, "*.pkl"))

    if not pkl_files:
        logger.info(f"未找到 ETF pickle 文件: {pickle_dir}")
        return 0

    logger.info(f"开始迁移 ETF 数据：共 {len(pkl_files)} 个文件")
    success_count = 0

    for pkl_file in pkl_files:
        try:
            info = parse_etf_pickle_filename(pkl_file)

            if info is None:
                logger.warning(f"无法解析文件名: {pkl_file}")
                continue

            symbol = info["symbol"]

            df = pd.read_pickle(pkl_file)

            if df is None or df.empty:
                logger.warning(f"文件为空: {pkl_file}")
                continue

            date_col = None
            for col in ["date", "datetime", "日期"]:
                if col in df.columns:
                    date_col = col
                    break

            if date_col is None:
                logger.warning(f"未找到日期列: {pkl_file}")
                continue

            df = df.copy()
            df["datetime"] = pd.to_datetime(df[date_col])

            cols_map = {
                "开盘": "open",
                "最高": "high",
                "最低": "low",
                "收盘": "close",
                "成交量": "volume",
                "成交额": "amount",
            }

            for old_col, new_col in cols_map.items():
                if old_col in df.columns and new_col not in df.columns:
                    df[new_col] = df[old_col]

            required_cols = ["datetime", "open", "high", "low", "close", "volume"]
            if not all(col in df.columns for col in required_cols):
                logger.warning(f"缺少必要列: {pkl_file}")
                continue

            db.insert_etf_daily(
                symbol,
                df[
                    required_cols + ["amount"]
                    if "amount" in df.columns
                    else required_cols
                ],
            )

            logger.info(f"迁移成功: {pkl_file} -> {symbol}")
            success_count += 1

        except Exception as e:
            logger.error(f"迁移失败 {pkl_file}: {e}")
            continue

    logger.info(f"ETF 数据迁移完成: {success_count}/{len(pkl_files)} 个文件成功")
    return success_count


def migrate_index_pickles(
    pickle_dir: str = "index_cache", db: ParquetAdapter = None
) -> int:
    """
    迁移指数 pickle 文件到 Parquet。
    """
    if db is None:
        db = ParquetAdapter()

    if not os.path.exists(pickle_dir):
        logger.warning(f"pickle 目录不存在: {pickle_dir}")
        return 0

    pkl_files = glob.glob(os.path.join(pickle_dir, "*.pkl"))

    if not pkl_files:
        logger.info(f"未找到指数 pickle 文件: {pickle_dir}")
        return 0

    logger.info(f"开始迁移指数数据：共 {len(pkl_files)} 个文件")
    success_count = 0

    for pkl_file in pkl_files:
        try:
            info = parse_index_pickle_filename(pkl_file)

            if info is None:
                logger.warning(f"无法解析文件名: {pkl_file}")
                continue

            symbol = info["symbol"]

            df = pd.read_pickle(pkl_file)

            if df is None or df.empty:
                logger.warning(f"文件为空: {pkl_file}")
                continue

            date_col = None
            for col in ["date", "datetime", "日期"]:
                if col in df.columns:
                    date_col = col
                    break

            if date_col is None:
                logger.warning(f"未找到日期列: {pkl_file}")
                continue

            df = df.copy()
            df["datetime"] = pd.to_datetime(df[date_col])

            cols_map = {
                "开盘": "open",
                "最高": "high",
                "最低": "low",
                "收盘": "close",
                "成交量": "volume",
                "成交额": "amount",
            }

            for old_col, new_col in cols_map.items():
                if old_col in df.columns and new_col not in df.columns:
                    df[new_col] = df[old_col]

            required_cols = ["datetime", "open", "high", "low", "close", "volume"]
            if not all(col in df.columns for col in required_cols):
                logger.warning(f"缺少必要列: {pkl_file}")
                continue

            db.insert_index_daily(
                symbol,
                df[
                    required_cols + ["amount"]
                    if "amount" in df.columns
                    else required_cols
                ],
            )

            logger.info(f"迁移成功: {pkl_file} -> {symbol}")
            success_count += 1

        except Exception as e:
            logger.error(f"迁移失败 {pkl_file}: {e}")
            continue

    logger.info(f"指数数据迁移完成: {success_count}/{len(pkl_files)} 个文件成功")
    return success_count


def migrate_meta_pickles(meta_cache_dir: str, db: ParquetAdapter = None) -> int:
    """
    迁移元数据 pickle 文件到 Parquet。
    """
    if db is None:
        db = ParquetAdapter()

    if not os.path.exists(meta_cache_dir):
        logger.warning(f"meta_cache 目录不存在: {meta_cache_dir}")
        return 0

    success_count = 0

    # 迁移 trade_days.pkl
    trade_days_path = os.path.join(meta_cache_dir, "trade_days.pkl")
    if os.path.exists(trade_days_path):
        try:
            df = pd.read_pickle(trade_days_path)
            if df is not None and not df.empty:
                df = df.copy()
                if "trade_date" in df.columns and "date" not in df.columns:
                    df = df.rename(columns={"trade_date": "date"})
                if "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"]).dt.date
                db.cache_manager.put("trade_calendar", df)
                logger.info(f"迁移成功: {trade_days_path} -> trade_calendar")
                success_count += 1
        except Exception as e:
            logger.error(f"迁移失败 {trade_days_path}: {e}")

    # 迁移 securities_YYYYMMDD.pkl
    securities_files = glob.glob(os.path.join(meta_cache_dir, "securities_*.pkl"))
    for pkl_file in securities_files:
        try:
            df = pd.read_pickle(pkl_file)
            if df is None or df.empty:
                continue

            df = df.copy()

            required_cols = [
                "code",
                "jq_code",
                "display_name",
                "name",
                "start_date",
                "end_date",
                "type",
                "update_time",
            ]
            for col in required_cols:
                if col not in df.columns:
                    if col == "jq_code":
                        df[col] = df["code"].apply(
                            lambda x: (
                                x[2:] + ".XSHE"
                                if str(x).startswith("sz")
                                else x[2:] + ".XSHG"
                                if str(x).startswith("sh")
                                else str(x)
                            )
                        )
                    elif col == "display_name":
                        df[col] = df.get("name", "")
                    elif col == "type":
                        df[col] = "stock"
                    elif col == "update_time":
                        df[col] = pd.Timestamp.now()
                    else:
                        df[col] = None

            db.cache_manager.put("securities", df[required_cols])
            logger.info(f"迁移成功: {pkl_file} -> securities")
            success_count += 1
        except Exception as e:
            logger.error(f"迁移失败 {pkl_file}: {e}")

    return success_count


def migrate_index_weights_pickles(
    index_cache_dir: str, db: ParquetAdapter = None
) -> int:
    """
    迁移指数权重 pickle 文件到 Parquet。
    """
    if db is None:
        db = ParquetAdapter()

    if not os.path.exists(index_cache_dir):
        logger.warning(f"index_cache 目录不存在: {index_cache_dir}")
        return 0

    pkl_files = glob.glob(os.path.join(index_cache_dir, "*_weights.pkl"))
    if not pkl_files:
        logger.info(f"未找到指数权重 pickle 文件: {index_cache_dir}")
        return 0

    # 确保 index_weights 表已注册
    registry = db.cache_manager.registry
    if not registry.has("index_weights"):
        from parquet_cache.table_registry import CacheTable

        registry.register(
            CacheTable(
                name="index_weights",
                partition_by=None,
                ttl_hours=0,
                schema={
                    "index_code": "string",
                    "stock_code": "string",
                    "weight": "float64",
                    "update_date": "date",
                    "update_time": "timestamp",
                },
                primary_key=["index_code", "stock_code", "update_date"],
                aggregation_enabled=False,
                compaction_threshold=0,
                storage_layer="meta",
                priority="P2",
            )
        )

    success_count = 0
    for pkl_file in pkl_files:
        try:
            basename = os.path.basename(pkl_file)
            index_code = basename.replace("_weights.pkl", "")

            df = pd.read_pickle(pkl_file)
            if df is None or df.empty:
                continue

            df = df.copy()

            # 列名映射
            col_sources = {
                "stock_code": ["stock_code", "code"],
                "weight": ["weight"],
                "update_date": ["update_date", "date"],
            }

            result = pd.DataFrame()
            result["index_code"] = index_code

            for target, sources in col_sources.items():
                found = False
                for src in sources:
                    if src in df.columns:
                        result[target] = df[src]
                        found = True
                        break
                if not found:
                    if target == "update_date":
                        result[target] = pd.Timestamp.now().date()
                    else:
                        result[target] = None

            if "update_time" not in result.columns:
                result["update_time"] = pd.Timestamp.now()

            db.cache_manager.put("index_weights", result)
            logger.info(f"迁移成功: {pkl_file} -> {index_code}")
            success_count += 1
        except Exception as e:
            logger.error(f"迁移失败 {pkl_file}: {e}")

    return success_count


def auto_migrate(base_dir: str = None) -> Dict[str, int]:
    """
    自动检测并迁移所有 pickle 数据到 DuckDB。

    参数
    ----
    base_dir : str
        项目根目录，默认为当前目录

    返回
    ----
    dict
        各类型迁移结果统计
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    db = ParquetAdapter()

    stock_count = db.count_records("stock_daily")
    etf_count = db.count_records("etf_daily")
    index_count = db.count_records("index_daily")

    if stock_count > 0 or etf_count > 0 or index_count > 0:
        logger.info(
            f"Parquet 已有数据: 股票 {stock_count} 条, ETF {etf_count} 条, 指数 {index_count} 条"
        )
        logger.info("跳过自动迁移（如需强制迁移，请使用手动迁移工具）")
        return {
            "stock": 0,
            "etf": 0,
            "index": 0,
            "meta": 0,
            "index_weights": 0,
            "skipped": True,
        }

    logger.info("开始自动迁移 pickle 数据到 Parquet...")

    results = {
        "stock": 0,
        "etf": 0,
        "index": 0,
        "meta": 0,
        "index_weights": 0,
        "skipped": False,
    }

    stock_dir = os.path.join(base_dir, "stock_cache")
    if os.path.exists(stock_dir):
        results["stock"] = migrate_stock_pickles(stock_dir, db)

    etf_dir = os.path.join(base_dir, "etf_cache")
    if os.path.exists(etf_dir):
        results["etf"] = migrate_etf_pickles(etf_dir, db)

    index_dir = os.path.join(base_dir, "index_cache")
    if os.path.exists(index_dir):
        results["index"] = migrate_index_pickles(index_dir, db)

    meta_dir = os.path.join(base_dir, "meta_cache")
    if os.path.exists(meta_dir):
        results["meta"] = migrate_meta_pickles(meta_dir, db)

    if os.path.exists(index_dir):
        results["index_weights"] = migrate_index_weights_pickles(index_dir, db)

    total = (
        results["stock"]
        + results["etf"]
        + results["index"]
        + results["meta"]
        + results["index_weights"]
    )
    logger.info(f"自动迁移完成: 共迁移 {total} 个文件")
    logger.info(f"  - 股票: {results['stock']} 个")
    logger.info(f"  - ETF: {results['etf']} 个")
    logger.info(f"  - 指数: {results['index']} 个")
    logger.info(f"  - 元数据: {results['meta']} 个")
    logger.info(f"  - 指数权重: {results['index_weights']} 个")

    return results


if __name__ == "__main__":
    from jk2bt.logging import setup_logging, get_logger

    setup_logging()
    logger = get_logger(__name__)

    results = auto_migrate()
    print("\n迁移结果:")
    print(f"股票: {results['stock']} 个文件")
    print(f"ETF: {results['etf']} 个文件")
    print(f"指数: {results['index']} 个文件")
