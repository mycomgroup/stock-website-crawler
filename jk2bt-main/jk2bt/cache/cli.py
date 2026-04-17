from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

from .aggregator import Aggregator, run_aggregation
from .manager import CacheManager, get_cache_manager
from .config import CacheConfig
from .registry import DEFAULT_REGISTRY


def _parse_where(conditions: list[str] | None) -> dict[str, Any]:
    if not conditions:
        return {}
    result: dict[str, Any] = {}
    for cond in conditions:
        if ">=" in cond:
            key, value = cond.split(">=", 1)
            result[key.strip()] = (">=", value.strip())
        elif "<=" in cond:
            key, value = cond.split("<=", 1)
            result[key.strip()] = ("<=", value.strip())
        elif "=" in cond:
            key, value = cond.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def _format_output(df: pd.DataFrame, fmt: str) -> None:
    if fmt == "json":
        print(df.to_json(orient="records", indent=2, default_handler=str))
    elif fmt == "csv":
        print(df.to_csv(index=False))
    elif fmt == "table":
        _print_table(df)


def _print_table(df: pd.DataFrame) -> None:
    if df.empty:
        print("(empty)")
        return
    print(df.to_string(index=False, max_rows=50))


def _size_human(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    if size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def cmd_status(args: argparse.Namespace) -> None:
    manager = get_cache_manager(base_dir=args.base_dir)
    stats = manager.get_stats()

    total_files = sum(t["file_count"] for t in stats["tables"].values())
    total_size = sum(t["size_mb"] * 1024 * 1024 for t in stats["tables"].values())

    print(f"Cache directory: {args.base_dir}")
    print(f"Total files: {total_files}")
    print(f"Total size: {_size_human(int(total_size))}")
    print(f"Memory cache size: {stats['memory_cache_size']}")
    print(f"Memory cache hit rate: {stats['memory_cache_hit_rate']:.2%}")
    print()

    tables = stats["tables"]
    if args.table:
        tables = {k: v for k, v in tables.items() if k == args.table}

    if tables:
        print(f"{'Table':<30} {'Files':>8} {'Size':>12}")
        print("-" * 52)
        for name, info in sorted(tables.items()):
            size_bytes = int(info["size_mb"] * 1024 * 1024)
            print(f"{name:<30} {info['file_count']:>8} {_size_human(size_bytes):>12}")

    aggregator = Aggregator(args.base_dir)
    agg_status = {}
    for table_name in tables:
        try:
            agg_status[table_name] = aggregator.get_aggregation_status(table_name)
        except KeyError:
            continue

    if agg_status:
        print()
        print("Aggregation status:")
        for name, s in sorted(agg_status.items()):
            print(
                f"  {name}: {s['aggregated_partitions']}/{s['total_partitions']} aggregated, "
                f"{s['total_raw_files']} raw files"
            )


def cmd_aggregate(args: argparse.Namespace) -> None:
    tables = [args.table] if args.table else None
    result = run_aggregation(
        base_dir=args.base_dir,
        tables=tables,
        priority=args.priority,
        cleanup=not args.no_cleanup,
    )

    if result["aggregated"]:
        print("Aggregated:")
        for name, count in result["aggregated"].items():
            print(f"  {name}: {count} partitions")
    else:
        print("No tables needed aggregation.")

    if result["cleaned_files"] > 0:
        print(f"Cleaned up {result['cleaned_files']} expired files.")


def cmd_query(args: argparse.Namespace) -> None:
    manager = get_cache_manager(base_dir=args.base_dir)
    where = _parse_where(args.where)
    columns = [c.strip() for c in args.columns.split(",")] if args.columns else None

    df = manager.get(
        table=args.table,
        where=where if where else None,
        columns=columns,
        limit=args.limit,
    )

    if df is None or df.empty:
        print("No data found.")
        return

    if args.limit and len(df) > args.limit:
        df = df.head(args.limit)

    _format_output(df, args.format)


def cmd_put(args: argparse.Namespace) -> None:
    manager = get_cache_manager(base_dir=args.base_dir)
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"Error: file not found: {file_path}")
        sys.exit(1)

    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(file_path)
    elif suffix == ".parquet":
        df = pd.read_parquet(file_path)
    else:
        print(f"Error: unsupported file format: {suffix}")
        sys.exit(1)

    result = manager.put(
        table=args.table,
        data=df,
        partition_value=args.partition_value,
    )
    print(f"Wrote {len(df)} rows to {args.table}")
    if result:
        print(f"Path: {result}")


def cmd_invalidate(args: argparse.Namespace) -> None:
    manager = get_cache_manager(base_dir=args.base_dir)

    if args.all:
        deleted = manager.invalidate(table=args.table)
        print(f"Invalidated all cache for {args.table}, deleted {deleted} files.")
    else:
        where = _parse_where(args.where)
        deleted = manager.invalidate(
            table=args.table,
            where=where if where else None,
        )
        print(f"Invalidated {deleted} files for {args.table}.")


def cmd_list(args: argparse.Namespace) -> None:
    registry = DEFAULT_REGISTRY
    tables = registry.list_all()

    if args.priority:
        tables = {k: v for k, v in tables.items() if v.priority == args.priority}
    if args.layer:
        tables = {k: v for k, v in tables.items() if v.storage_layer == args.layer}

    if not tables:
        print("No tables found.")
        return

    print(
        f"{'Table':<30} {'Priority':<10} {'Layer':<12} "
        f"{'Partition':<15} {'TTL(h)':<8} {'Agg':<5}"
    )
    print("-" * 82)
    for name, tdef in sorted(tables.items()):
        print(
            f"{name:<30} {tdef.priority:<10} {tdef.storage_layer:<12} "
            f"{(tdef.partition_by or 'none'):<15} {tdef.ttl_hours:<8} "
            f"{'Y' if tdef.aggregation_enabled else 'N':<5}"
        )


def cmd_cleanup(args: argparse.Namespace) -> None:
    aggregator = Aggregator(args.base_dir)

    if args.dry_run:
        print(f"Dry run: would clean up files older than {args.retention_hours} hours.")
        print(f"Cache directory: {args.base_dir}")
        return

    deleted = aggregator.cleanup(retention_hours=args.retention_hours)
    print(f"Cleaned up {deleted} expired files.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="parquet-cache",
        description="Parquet Cache CLI",
    )
    parser.add_argument("--base-dir", default="data_cache/cache", help="缓存根目录")

    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="查看缓存状态")
    status_parser.add_argument("--table", help="指定表名")

    agg_parser = subparsers.add_parser("aggregate", help="执行聚合")
    agg_parser.add_argument("--table", help="指定表名")
    agg_parser.add_argument("--priority", choices=["P0", "P1", "P2", "P3"])
    agg_parser.add_argument("--no-cleanup", action="store_true")

    query_parser = subparsers.add_parser("query", help="查询缓存")
    query_parser.add_argument("table", help="表名")
    query_parser.add_argument(
        "--where", action="append", help="过滤条件 (key=value, key>=value)"
    )
    query_parser.add_argument("--columns", help="选择的列（逗号分隔）")
    query_parser.add_argument("--limit", type=int)
    query_parser.add_argument(
        "--format", choices=["json", "csv", "table"], default="table"
    )

    put_parser = subparsers.add_parser("put", help="从文件写入缓存")
    put_parser.add_argument("table", help="表名")
    put_parser.add_argument("file", help="CSV 或 Parquet 文件路径")
    put_parser.add_argument("--partition-value", help="分区值")

    inv_parser = subparsers.add_parser("invalidate", help="使缓存过期")
    inv_parser.add_argument("table", help="表名")
    inv_parser.add_argument("--where", action="append")
    inv_parser.add_argument("--all", action="store_true")

    list_parser = subparsers.add_parser("list", help="列出所有表")
    list_parser.add_argument("--priority", choices=["P0", "P1", "P2", "P3"])
    list_parser.add_argument("--layer", choices=["daily", "minute", "meta", "snapshot"])

    clean_parser = subparsers.add_parser("cleanup", help="清理过期文件")
    clean_parser.add_argument("--retention-hours", type=int, default=24)
    clean_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    commands = {
        "status": cmd_status,
        "aggregate": cmd_aggregate,
        "query": cmd_query,
        "put": cmd_put,
        "invalidate": cmd_invalidate,
        "list": cmd_list,
        "cleanup": cmd_cleanup,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
