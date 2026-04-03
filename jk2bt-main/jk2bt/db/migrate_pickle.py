"""
db/migrate_pickle.py
Pickle 缓存迁移工具 - 将所有 pickle 文件迁移到 DuckDB。

使用方式:
    # 迁移所有 pickle
    python -m src.db.migrate_pickle --all

    # 仅迁移元数据
    python -m src.db.migrate_pickle --meta

    # 仅迁移特定目录
    python -m src.db.migrate_pickle --dir meta_cache
"""

import os
import glob
import json
import logging
import argparse
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

from .unified_cache import UnifiedCacheManager, TableSchema
from .cache_config import META_SCHEMAS, DOMAIN_DB_MAPPING

logger = logging.getLogger(__name__)


def find_pickle_files(base_dir: str, pattern: str = "**/*.pkl") -> List[str]:
    """查找所有 pickle 文件"""
    pkl_files = glob.glob(os.path.join(base_dir, pattern), recursive=True)
    return [f for f in pkl_files if os.path.isfile(f)]


def migrate_trade_days(pickle_file: str, cache: UnifiedCacheManager) -> bool:
    """迁移交易日历"""
    try:
        df = pd.read_pickle(pickle_file)
        if df is None or df.empty:
            logger.warning(f"交易日历文件为空: {pickle_file}")
            return False

        if isinstance(df, pd.DatetimeIndex):
            df = pd.DataFrame({"date": df.strftime("%Y-%m-%d")})
        elif isinstance(df, list):
            df = pd.DataFrame(
                {
                    "date": [
                        d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
                        for d in df
                    ]
                }
            )
        elif hasattr(df, "index"):
            if isinstance(df.index, pd.DatetimeIndex):
                df = pd.DataFrame({"date": df.index.strftime("%Y-%m-%d")})

        if "date" not in df.columns:
            if df.columns[0] in ["trade_date", "datetime", "日期"]:
                df = df.rename(columns={df.columns[0]: "date"})

        df["date"] = pd.to_datetime(df["date"]).dt.date

        cache.set("meta", "trade_days", df)
        logger.info(f"迁移交易日历成功: {len(df)} 条")
        return True
    except Exception as e:
        logger.error(f"迁移交易日历失败: {e}")
        return False


def migrate_securities(pickle_file: str, cache: UnifiedCacheManager) -> bool:
    """迁移证券列表"""
    try:
        df = pd.read_pickle(pickle_file)
        if df is None or df.empty:
            logger.warning(f"证券列表文件为空: {pickle_file}")
            return False

        col_map = {
            "display_name": ["display_name", "name", "名称"],
            "start_date": ["start_date", "上市日期", "start"],
            "end_date": ["end_date", "退市日期", "end"],
            "type": ["type", "证券类型"],
        }

        result_df = pd.DataFrame()
        result_df["code"] = (
            df.index
            if hasattr(df, "index") and not isinstance(df.index, pd.RangeIndex)
            else df.get("code", df.get("symbol", df.iloc[:, 0]))
        )

        for new_col, old_cols in col_map.items():
            for old_col in old_cols:
                if old_col in df.columns:
                    result_df[new_col] = df[old_col]
                    break

        if "type" not in result_df.columns:
            result_df["type"] = "stock"

        if "start_date" in result_df.columns:
            result_df["start_date"] = pd.to_datetime(
                result_df["start_date"], errors="coerce"
            ).dt.date
        if "end_date" in result_df.columns:
            result_df["end_date"] = pd.to_datetime(
                result_df["end_date"], errors="coerce"
            ).dt.date

        cache.set("meta", "securities", result_df)
        logger.info(f"迁移证券列表成功: {len(result_df)} 条")
        return True
    except Exception as e:
        logger.error(f"迁移证券列表失败: {e}")
        return False


def migrate_security_info(pickle_file: str, cache: UnifiedCacheManager) -> bool:
    """迁移证券详细信息"""
    try:
        data = pd.read_pickle(pickle_file)
        if data is None:
            logger.warning(f"证券信息文件为空: {pickle_file}")
            return False

        basename = os.path.basename(pickle_file)
        code = basename.replace("security_info_", "").replace(".pkl", "")

        if isinstance(data, dict):
            info_json = json.dumps(data, ensure_ascii=False, default=str)
        elif isinstance(data, pd.DataFrame):
            info_json = data.to_json(orient="records", date_format="iso")
        else:
            info_json = json.dumps(str(data), ensure_ascii=False)

        df = pd.DataFrame(
            [
                {
                    "code": code,
                    "info_json": info_json,
                    "update_time": datetime.now(),
                }
            ]
        )

        cache.set("meta", "security_info", df)
        logger.info(f"迁移证券信息成功: {code}")
        return True
    except Exception as e:
        logger.error(f"迁移证券信息失败: {e}")
        return False


def migrate_index_weights(pickle_file: str, cache: UnifiedCacheManager) -> bool:
    """迁移指数权重"""
    try:
        df = pd.read_pickle(pickle_file)
        if df is None or df.empty:
            logger.warning(f"指数权重文件为空: {pickle_file}")
            return False

        basename = os.path.basename(pickle_file)
        index_code = basename.replace("_weights.pkl", "")

        result_df = pd.DataFrame()

        if isinstance(df, dict):
            result_df = pd.DataFrame(
                [
                    {"index_code": index_code, "stock_code": k, "weight": v}
                    for k, v in df.items()
                ]
            )
        elif isinstance(df, pd.DataFrame):
            result_df["index_code"] = index_code
            if "weight" in df.columns:
                result_df["stock_code"] = (
                    df.index if hasattr(df, "index") else df.iloc[:, 0]
                )
                result_df["weight"] = df["weight"]
            else:
                result_df["stock_code"] = (
                    df.index if hasattr(df, "index") else df.iloc[:, 0]
                )
                result_df["weight"] = df.iloc[:, 0]

        result_df["update_date"] = datetime.now().date()
        result_df["update_time"] = datetime.now()

        cache.set("index_components", "index_weights", result_df)
        logger.info(f"迁移指数权重成功: {index_code} -> {len(result_df)} 条")
        return True
    except Exception as e:
        logger.error(f"迁移指数权重失败: {e}")
        return False


def migrate_meta_cache(cache_dir: str, cache: UnifiedCacheManager) -> Dict[str, int]:
    """迁移 meta_cache 目录"""
    results = {"trade_days": 0, "securities": 0, "security_info": 0, "errors": 0}

    if not os.path.exists(cache_dir):
        logger.warning(f"缓存目录不存在: {cache_dir}")
        return results

    pkl_files = find_pickle_files(cache_dir)
    logger.info(f"发现 {len(pkl_files)} 个 pickle 文件")

    for pkl_file in pkl_files:
        basename = os.path.basename(pkl_file)

        if basename == "trade_days.pkl":
            if migrate_trade_days(pkl_file, cache):
                results["trade_days"] += 1
            else:
                results["errors"] += 1

        elif basename.startswith("securities_"):
            if migrate_securities(pkl_file, cache):
                results["securities"] += 1
            else:
                results["errors"] += 1

        elif basename.startswith("security_info_"):
            if migrate_security_info(pkl_file, cache):
                results["security_info"] += 1
            else:
                results["errors"] += 1

    return results


def migrate_index_cache(cache_dir: str, cache: UnifiedCacheManager) -> Dict[str, int]:
    """迁移 index_cache 目录"""
    results = {"index_weights": 0, "errors": 0}

    if not os.path.exists(cache_dir):
        logger.warning(f"缓存目录不存在: {cache_dir}")
        return results

    pkl_files = find_pickle_files(cache_dir)

    for pkl_file in pkl_files:
        basename = os.path.basename(pkl_file)

        if basename.endswith("_weights.pkl"):
            if migrate_index_weights(pkl_file, cache):
                results["index_weights"] += 1
            else:
                results["errors"] += 1

    return results


def migrate_all_pickle(base_dir: str = None) -> Dict[str, Dict]:
    """迁移所有 pickle 缓存"""
    if base_dir is None:
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    cache = UnifiedCacheManager.get_instance()

    for domain, config in DOMAIN_DB_MAPPING.items():
        db_path = os.path.join(base_dir, config["db_path"])
        cache.register_db(domain, db_path, config["schemas"])

    results = {}

    meta_cache_dir = os.path.join(
        base_dir, "src", "cache", "meta_cache"
    )
    if os.path.exists(meta_cache_dir):
        results["meta"] = migrate_meta_cache(meta_cache_dir, cache)

    index_cache_dir = os.path.join(
        base_dir, "src", "cache", "index_cache"
    )
    if os.path.exists(index_cache_dir):
        results["index"] = migrate_index_cache(index_cache_dir, cache)

    cache_base_dir = os.path.join(base_dir, "cache")
    if os.path.exists(cache_base_dir):
        meta_cache_dir2 = os.path.join(cache_base_dir, "meta_cache")
        if os.path.exists(meta_cache_dir2):
            r = migrate_meta_cache(meta_cache_dir2, cache)
            if "meta" not in results:
                results["meta"] = r
            else:
                for k, v in r.items():
                    results["meta"][k] = results["meta"].get(k, 0) + v

        index_cache_dir2 = os.path.join(cache_base_dir, "index_cache")
        if os.path.exists(index_cache_dir2):
            r = migrate_index_cache(index_cache_dir2, cache)
            if "index" not in results:
                results["index"] = r
            else:
                for k, v in r.items():
                    results["index"][k] = results["index"].get(k, 0) + v

    return results


def verify_migration(cache: UnifiedCacheManager) -> Dict[str, Dict]:
    """验证迁移结果"""
    results = {}

    adapter = cache.get_adapter("meta")
    if adapter:
        results["meta"] = {
            "trade_days": adapter.count("trade_days"),
            "securities": adapter.count("securities"),
            "security_info": adapter.count("security_info"),
        }

    adapter = cache.get_adapter("index_components")
    if adapter:
        results["index_components"] = {
            "index_weights": adapter.count("index_weights"),
        }

    return results


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="Pickle 缓存迁移工具")
    parser.add_argument("--all", action="store_true", help="迁移所有 pickle")
    parser.add_argument("--meta", action="store_true", help="仅迁移元数据")
    parser.add_argument("--index", action="store_true", help="仅迁移指数权重")
    parser.add_argument("--verify", action="store_true", help="验证迁移结果")
    parser.add_argument("--base-dir", type=str, help="项目根目录")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    if args.verify:
        cache = UnifiedCacheManager.get_instance()
        from .cache_config import init_default_cache

        init_default_cache()
        results = verify_migration(cache)
        print("\n迁移验证结果:")
        for domain, counts in results.items():
            print(f"\n{domain}:")
            for table, count in counts.items():
                print(f"  {table}: {count} 条")
        return

    if args.all or args.meta or args.index:
        print("开始迁移 pickle 缓存到 DuckDB...")
        results = migrate_all_pickle(args.base_dir)

        print("\n迁移完成:")
        total_success = 0
        total_errors = 0

        for domain, r in results.items():
            print(f"\n{domain}:")
            for k, v in r.items():
                if k == "errors":
                    total_errors += v
                    print(f"  错误: {v}")
                else:
                    total_success += v
                    print(f"  {k}: {v} 个文件")

        print(f"\n总计: 成功 {total_success} 个, 失败 {total_errors} 个")

        print("\n验证迁移结果...")
        cache = UnifiedCacheManager.get_instance()
        verify_results = verify_migration(cache)
        for domain, counts in verify_results.items():
            print(f"\n{domain} 数据库:")
            for table, count in counts.items():
                print(f"  {table}: {count} 条记录")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
