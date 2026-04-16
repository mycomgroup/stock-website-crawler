#!/usr/bin/env python3
"""从 DuckDB 导出数据到 parquet_cache 格式

Usage:
    python tools/migrate_duckdb_to_parquet.py                    # 迁移所有表
    python tools/migrate_duckdb_to_parquet.py --tables stock_daily etf_daily
    python tools/migrate_duckdb_to_parquet.py --dry-run          # 只统计不写入
    python tools/migrate_duckdb_to_parquet.py --verify           # 对比迁移前后数据
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import duckdb
import pandas as pd

from parquet_cache import get_cache_manager
from parquet_cache.schema_validator import normalize_date_columns

# DuckDB 文件到 parquet_cache 表的映射
# 格式: {db_path: [(duckdb_table_name, parquet_table_name), ...]}
DB_TABLE_MAP = {
    "data/market.db": [
        ("stock_daily", "stock_daily"),
        ("etf_daily", "etf_daily"),
        ("index_daily", "index_daily"),
        ("lof_daily", "etf_daily"),  # LOF 复用 ETF 表
        ("stock_minute", "stock_minute"),
        ("etf_minute", "etf_minute"),
    ],
    "data/meta.db": [
        ("trade_days", "trade_calendar"),
        ("securities", "securities"),
        ("security_info", "company_info"),
    ],
    "data/dividend.db": [("dividend", "dividend")],
    "data/shareholder.db": [
        ("top10_shareholders", "holder"),
        ("top10_float_shareholders", "holder"),
        ("shareholder_num", "holder"),
        ("shareholder_structure", "holder"),
    ],
    "data/share_change.db": [("share_change", "share_change")],
    "data/unlock.db": [
        ("unlock_data", "unlock"),
        ("unlock_calendar", "unlock"),
    ],
    "data/macro.db": [("macro", "macro_data"), ("macro_data", "macro_data")],
    "data/company_info.db": [
        ("company_info", "company_info"),
        ("status_change", "status_change"),
    ],
    "data/index_components.db": [
        ("index_components", "index_components"),
        ("index_weights", "index_components"),
        ("index_history", "index_components"),
    ],
    "data/conversion_bond.db": [
        ("cb_list", "conversion_bond_daily"),
        ("cb_daily", "conversion_bond_daily"),
        ("conversion_bond", "conversion_bond_daily"),
    ],
    "data/industry_sw.db": [
        ("sw_industry_list", "industry_list"),
        ("industry_sw", "industry_components"),
    ],
    "data/option.db": [
        ("option_list", "option_daily"),
        ("option_daily", "option_daily"),
        ("option_greeks", "option_daily"),
        ("option", "option_daily"),
    ],
}

# 字段名映射: DuckDB -> parquet_cache
COLUMN_RENAME_MAP = {
    "dividend": {
        "code": "symbol",
        "board_plan_pub_date": "announce_date",
        "bonus_ratio_rmb": "dividend_cash",
        "bonus_share_ratio": "dividend_stock",
        "ex_dividend_date": "ex_date",
        "transfer_ratio": "transfer_ratio",
        "record_date": "record_date",
    },
    "holder": {
        "code": "symbol",
        "shareholder_name": "holder_name",
        "hold_amount": "hold_count",
        "shareholder_type": "holder_type",
        "report_date": "report_date",
    },
    "share_change": {
        "code": "symbol",
        "change_date": "announce_date",
        "change_amount": "total_shares",
        "hold_amount_after": "circulating_shares",
    },
    "unlock": {
        "code": "symbol",
        "unlock_amount": "unlock_count",
        "unlock_date": "unlock_date",
    },
    "macro_data": {
        "yoy": "change_pct",
    },
    "company_info": {
        "code": "symbol",
        "company_name": "name",
        # "establish_date" -> skip, table already has list_date
    },
    "status_change": {
        "code": "symbol",
        "status_date": "status_date",
        "status_type": "status_type",
        "reason": "reason",
    },
    "securities": {
        "jq_code": "symbol",
        "name": "name",
        "type": "type",
        "start_date": "list_date",
        "end_date": "delist_date",
    },
}

# 目标表需要的列
TARGET_COLUMNS = {
    "stock_daily": [
        "symbol",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
        "adjust",
    ],
    "etf_daily": ["symbol", "date", "open", "high", "low", "close", "volume", "amount"],
    "index_daily": [
        "symbol",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
    ],
    "stock_minute": [
        "symbol",
        "datetime",
        "period",
        "adjust",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
    ],
    "etf_minute": [
        "symbol",
        "datetime",
        "period",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
    ],
    "dividend": [
        "symbol",
        "announce_date",
        "dividend_cash",
        "dividend_stock",
        "record_date",
        "ex_date",
    ],
    "holder": [
        "symbol",
        "report_date",
        "holder_name",
        "hold_count",
        "hold_ratio",
        "holder_type",
    ],
    "share_change": [
        "symbol",
        "announce_date",
        "total_shares",
        "circulating_shares",
        "change_type",
    ],
    "unlock": [
        "symbol",
        "announce_date",
        "unlock_date",
        "unlock_count",
        "unlock_ratio",
        "unlock_type",
    ],
    "macro_data": ["indicator", "date", "value", "change_pct"],
    "company_info": ["symbol", "name", "industry", "area", "list_date", "market"],
    "status_change": ["symbol", "status_date", "status_type", "reason"],
    "trade_calendar": ["date", "is_trading_day"],
    "securities": ["symbol", "name", "type", "list_date", "delist_date", "exchange"],
    "index_components": ["index_code", "date", "symbol", "weight"],
    "conversion_bond_daily": [
        "symbol",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
    ],
    "industry_list": ["industry_code", "industry_name", "source"],
    "industry_components": ["industry_code", "date", "symbol", "industry_name"],
    "option_daily": [
        "symbol",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "open_interest",
    ],
}

PARTITION_COLUMNS = {
    "stock_daily": "date",
    "etf_daily": "date",
    "index_daily": "date",
    "stock_minute": "week",
    "etf_minute": "week",
    "dividend": "announce_date",
    "holder": "report_date",
    "share_change": "announce_date",
    "unlock": "announce_date",
    "macro_data": None,
    "company_info": None,
    "status_change": None,
    "trade_calendar": None,
    "securities": None,
    "index_components": "date",
    "conversion_bond_daily": "date",
    "industry_list": None,
    "industry_components": "date",
    "option_daily": "date",
}


def migrate_table(
    conn, cache, duckdb_table: str, parquet_table: str, dry_run: bool = False
) -> int:
    """迁移单个表"""
    try:
        tables_in_db = conn.execute("SHOW TABLES").fetchdf()
        available_tables = tables_in_db.iloc[:, 0].tolist()
    except Exception:
        available_tables = []

    if duckdb_table not in available_tables:
        return 0

    df = conn.execute(f"SELECT * FROM {duckdb_table}").fetchdf()
    original_count = len(df)

    if df.empty:
        return 0

    # 字段名映射
    rename_map = COLUMN_RENAME_MAP.get(parquet_table, {})
    if rename_map:
        # 先删除目标列中已存在的列（避免重命名后产生重复列）
        for old_col, new_col in rename_map.items():
            if old_col in df.columns and new_col in df.columns and old_col != new_col:
                df = df.drop(columns=[old_col])
        df = df.rename(columns=rename_map)

    # datetime -> date 转换（日线数据）
    if "datetime" in df.columns and parquet_table in (
        "stock_daily",
        "etf_daily",
        "index_daily",
    ):
        df["date"] = pd.to_datetime(df["datetime"]).dt.date
        df = df.drop(columns=["datetime"])

    # 分钟线 week 分区计算
    if "datetime" in df.columns and parquet_table in ("stock_minute", "etf_minute"):
        df["datetime"] = pd.to_datetime(df["datetime"])
        year = df["datetime"].dt.year.astype(str)
        week = df["datetime"].dt.isocalendar().week.astype(str).str.zfill(2)
        df["week"] = year + "-W" + week

    # 确保目标列存在
    target_cols = TARGET_COLUMNS.get(parquet_table, [])
    if target_cols:
        for col in target_cols:
            if col not in df.columns:
                if col == "is_trading_day":
                    df[col] = True  # trade_days 都是交易日
                else:
                    df[col] = None
        df = df[[c for c in target_cols if c in df.columns]]

    # 类型转换：确保 date 列是 date 类型而非 datetime
    date_cols = [c for c in df.columns if "date" in c.lower() or c == "datetime"]
    for col in date_cols:
        if col in df.columns:
            try:
                # 处理全为 null 的情况
                if df[col].isna().all():
                    df[col] = df[col].astype(object)
                else:
                    df[col] = pd.to_datetime(df[col]).dt.date
            except Exception:
                pass

    # bool 类型转换
    if "is_trading_day" in df.columns:
        df["is_trading_day"] = df["is_trading_day"].astype(bool)

    # float 类型转换
    float_cols = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
        "weight",
        "hold_count",
        "hold_ratio",
        "unlock_count",
        "unlock_ratio",
        "dividend_cash",
        "dividend_stock",
        "total_shares",
        "circulating_shares",
        "change_pct",
        "value",
        "open_interest",
        "net_flow",
        "buy_amount",
        "sell_amount",
        "main_net_inflow",
        "super_large_net_inflow",
        "large_net_inflow",
        "medium_net_inflow",
        "small_net_inflow",
        "pe",
        "pb",
        "ps",
        "roe",
        "net_profit",
        "revenue",
        "market_cap",
        "circulating_cap",
        "price",
        "change_pct",
        "turnover_rate",
    ]
    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if dry_run:
        print(f"  [DRY-RUN] {duckdb_table} -> {parquet_table}: {original_count} 条")
        return original_count

    # 按分区写入
    partition_col = PARTITION_COLUMNS.get(parquet_table)
    if partition_col and partition_col in df.columns:
        groups = df.groupby(partition_col)
        for value, group in groups:
            cache.put(parquet_table, group, partition_value=str(value))
    else:
        cache.put(parquet_table, df)

    print(f"  {duckdb_table} -> {parquet_table}: {original_count} 条")
    return original_count


def verify_table(conn, cache, duckdb_table: str, parquet_table: str) -> dict:
    """对比迁移前后数据"""
    result = {
        "table": parquet_table,
        "duckdb_count": 0,
        "parquet_count": 0,
        "match": False,
    }

    try:
        tables_in_db = conn.execute("SHOW TABLES").fetchdf()
        available_tables = tables_in_db.iloc[:, 0].tolist()
    except Exception:
        available_tables = []

    if duckdb_table in available_tables:
        df_duckdb = conn.execute(
            f"SELECT COUNT(*) as cnt FROM {duckdb_table}"
        ).fetchdf()
        result["duckdb_count"] = int(df_duckdb["cnt"].iloc[0])

    try:
        df_parquet = cache.get(parquet_table)
        if df_parquet is not None and not df_parquet.empty:
            result["parquet_count"] = len(df_parquet)
    except Exception as e:
        result["error"] = str(e)

    result["match"] = result["duckdb_count"] == result["parquet_count"]
    return result


def main():
    parser = argparse.ArgumentParser(
        description="从 DuckDB 导出数据到 parquet_cache 格式"
    )
    parser.add_argument("--dry-run", action="store_true", help="只统计不写入")
    parser.add_argument("--verify", action="store_true", help="对比迁移前后数据")
    parser.add_argument("--tables", nargs="*", help="指定要迁移的表名")
    parser.add_argument("--db", type=str, help="指定 DuckDB 文件路径")
    args = parser.parse_args()

    cache = get_cache_manager(base_dir=str(project_root / "data" / "cache"))

    if args.db:
        db_files = [args.db]
    else:
        db_files = list(DB_TABLE_MAP.keys())

    total_migrated = 0
    total_records = 0

    for db_path in db_files:
        full_path = project_root / db_path
        if not full_path.exists():
            print(f"跳过: {db_path} 不存在")
            continue

        print(f"\n处理 {db_path}...")
        conn = duckdb.connect(str(full_path), read_only=True)

        target_tables = DB_TABLE_MAP.get(db_path, [])
        if args.tables:
            target_tables = [t for t in target_tables if t in args.tables]

        if args.verify:
            print(f"  验证模式:")
            for duckdb_table, parquet_table in target_tables:
                result = verify_table(conn, cache, duckdb_table, parquet_table)
                status = "OK" if result["match"] else "MISMATCH"
                print(
                    f"    {duckdb_table} -> {parquet_table}: "
                    f"DuckDB={result['duckdb_count']}, "
                    f"Parquet={result['parquet_count']} [{status}]"
                )
        else:
            for duckdb_table, parquet_table in target_tables:
                if args.tables and parquet_table not in args.tables:
                    continue
                count = migrate_table(
                    conn, cache, duckdb_table, parquet_table, dry_run=args.dry_run
                )
                if count > 0:
                    total_migrated += 1
                    total_records += count

        conn.close()

    if not args.verify:
        mode = "[DRY-RUN] " if args.dry_run else ""
        print(f"\n{mode}迁移完成: {total_migrated} 个表, {total_records} 条记录")


if __name__ == "__main__":
    main()
