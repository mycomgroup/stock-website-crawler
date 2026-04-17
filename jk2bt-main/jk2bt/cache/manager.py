import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

from .config import CacheConfig
from .memory import MemoryCache
from .partition import PartitionManager
from .query import QueryEngine
from .registry import CacheTable, TableInfo, TableRegistry, DEFAULT_REGISTRY
from .writer import AtomicWriter

logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(
        self,
        base_dir: str | None = None,
        config: CacheConfig | None = None,
        registry: TableRegistry | None = None,
    ):
        cfg = config or CacheConfig()
        if base_dir:
            cfg.base_dir = base_dir

        self.config = cfg
        self.registry = registry or DEFAULT_REGISTRY
        self.partition_manager = PartitionManager(cfg.base_dir)
        self.writer = AtomicWriter(
            cfg.base_dir,
            compression=cfg.compression,
            row_group_size=cfg.row_group_size,
        )
        self.query_engine = QueryEngine(
            cfg.base_dir,
            threads=cfg.duckdb_threads,
            memory_limit=cfg.duckdb_memory_limit,
        )
        self.memory_cache = MemoryCache(
            max_items=cfg.memory_cache_max_items,
            default_ttl_seconds=cfg.memory_cache_default_ttl_seconds,
        )

    def get(
        self,
        table: str,
        where: dict[str, Any] | None = None,
        columns: list[str] | None = None,
        order_by: list[str] | None = None,
        limit: int | None = None,
        force_refresh: bool = False,
    ) -> pd.DataFrame | None:
        table_def = self.registry.get(table)

        if not force_refresh:
            cache_key = self._make_cache_key(table, where, columns)
            cached = self.memory_cache.get(cache_key)
            if cached is not None:
                logger.debug("Memory cache hit for table=%s key=%s", table, cache_key)
                return cached

        result = self.query_engine.query(
            table,
            table_def.storage_layer,
            partition_by=table_def.partition_by,
            where=where,
            columns=columns,
            order_by=order_by,
            limit=limit,
        )

        if result is not None:
            cache_key = self._make_cache_key(table, where, columns)
            self.memory_cache.put(cache_key, result)
            logger.debug("Query hit for table=%s, wrote to memory cache", table)

        return result if result is not None else pd.DataFrame()

    def put(
        self,
        table: str,
        data: pd.DataFrame,
        partition_value: str | None = None,
    ) -> str:
        table_def = self.registry.get(table)

        if data.empty:
            logger.debug("Empty DataFrame for table=%s, skipping write", table)
            return ""

        pv = partition_value
        if pv is None and table_def.partition_by is not None:
            pv = self._infer_partition_value(table_def, data)

        file_path = self.writer.write(
            table,
            table_def.storage_layer,
            data,
            partition_by=table_def.partition_by,
            partition_value=pv,
            schema=table_def.schema,
            primary_key=table_def.primary_key,
        )

        cache_key = self._make_cache_key(table, None, None)
        self.memory_cache.put(cache_key, data)

        logger.info("Wrote table=%s to %s", table, file_path)
        return str(file_path)

    def invalidate(
        self,
        table: str,
        where: dict[str, Any] | None = None,
    ) -> int:
        table_def = self.registry.get(table)

        if where is not None:
            cache_key = self._make_cache_key(table, where, None)
            self.memory_cache.invalidate(cache_key)

            if table_def.partition_by:
                partitions = self.partition_manager.list_all_partitions(
                    table,
                    table_def.storage_layer,
                    table_def.partition_by,
                )
                files = []
                for pv in partitions:
                    files.extend(
                        self.partition_manager.list_partition_files(
                            table,
                            table_def.storage_layer,
                            table_def.partition_by,
                            pv,
                        )
                    )
            else:
                files = self.partition_manager.list_partition_files(
                    table,
                    table_def.storage_layer,
                    table_def.partition_by,
                )
            deleted = 0
            for f in files:
                if self.partition_manager.remove_file(f):
                    deleted += 1
            logger.info("Invalidated %d files for table=%s", deleted, table)
            return deleted
        else:
            count = self.memory_cache.invalidate()
            if table_def.partition_by:
                partitions = self.partition_manager.list_all_partitions(
                    table,
                    table_def.storage_layer,
                    table_def.partition_by,
                )
                files = []
                for pv in partitions:
                    files.extend(
                        self.partition_manager.list_partition_files(
                            table,
                            table_def.storage_layer,
                            table_def.partition_by,
                            pv,
                        )
                    )
            else:
                files = self.partition_manager.list_partition_files(
                    table,
                    table_def.storage_layer,
                    table_def.partition_by,
                )
            deleted = 0
            for f in files:
                if self.partition_manager.remove_file(f):
                    deleted += 1
            logger.info(
                "Invalidated all cache for table=%s, deleted %d files", table, deleted
            )
            return deleted

    def has_data_range(
        self,
        table: str,
        where: dict[str, Any] | None = None,
        date_col: str = "date",
        start: str | None = None,
        end: str | None = None,
    ) -> bool:
        """检查数据是否覆盖指定日期范围

        类似 DuckDBManager.has_data() 的语义：
        查询 MIN(date) 和 MAX(date)，判断是否覆盖 [start, end]
        """
        result = self.get(table, where=where, columns=[date_col])
        if result is None or result.empty:
            return False

        min_date = pd.to_datetime(result[date_col].min())
        max_date = pd.to_datetime(result[date_col].max())

        if start:
            start_dt = pd.to_datetime(start)
            if min_date > start_dt:
                return False

        if end:
            end_dt = pd.to_datetime(end)
            if max_date < end_dt:
                return False

        return True

    def exists(
        self,
        table: str,
        where: dict[str, Any] | None = None,
    ) -> bool:
        table_def = self.registry.get(table)
        return self.query_engine.exists(
            table,
            table_def.storage_layer,
            partition_by=table_def.partition_by,
            where=where,
        )

    def table_info(self, table: str) -> TableInfo:
        table_def = self.registry.get(table)

        files = self.partition_manager.list_partition_files(
            table,
            table_def.storage_layer,
            table_def.partition_by,
        )
        if not files and table_def.partition_by:
            partitions = self.partition_manager.list_all_partitions(
                table,
                table_def.storage_layer,
                table_def.partition_by,
            )
            for pv in partitions:
                files.extend(
                    self.partition_manager.list_partition_files(
                        table,
                        table_def.storage_layer,
                        table_def.partition_by,
                        pv,
                    )
                )
        file_count = len(files)
        total_size_bytes = sum(f.stat().st_size for f in files) if files else 0

        last_updated = None
        if files:
            mtimes = [f.stat().st_mtime for f in files]
            from datetime import datetime

            last_updated = datetime.fromtimestamp(max(mtimes))

        partitions = self.partition_manager.list_all_partitions(
            table,
            table_def.storage_layer,
            table_def.partition_by,
        )
        partition_count = len(partitions) if table_def.partition_by else 0

        return TableInfo(
            name=table,
            file_count=file_count,
            total_size_bytes=total_size_bytes,
            last_updated=last_updated,
            partition_count=partition_count,
            priority=table_def.priority,
        )

    def list_tables(self) -> list[str]:
        return list(self.registry.list_all().keys())

    def get_stats(self) -> dict:
        tables = {}
        for table_name in self.list_tables():
            table_def = self.registry.get(table_name)
            files = self.partition_manager.list_partition_files(
                table_name,
                table_def.storage_layer,
                table_def.partition_by,
            )
            total_size = sum(f.stat().st_size for f in files) if files else 0
            tables[table_name] = {
                "file_count": len(files),
                "size_mb": round(total_size / (1024 * 1024), 2),
            }

        return {
            "memory_cache_size": self.memory_cache.size,
            "memory_cache_hit_rate": self.memory_cache.hit_rate,
            "tables": tables,
        }

    def _make_cache_key(
        self,
        table: str,
        where: dict[str, Any] | None,
        columns: list[str] | None,
    ) -> str:
        where_hash = hashlib.md5(
            json.dumps(where or {}, sort_keys=True, default=str).encode()
        ).hexdigest()[:8]
        columns_hash = hashlib.md5(
            json.dumps(columns or [], sort_keys=True, default=str).encode()
        ).hexdigest()[:8]
        return f"{table}:{where_hash}:{columns_hash}"

    def _infer_partition_value(
        self,
        table_def: CacheTable,
        data: pd.DataFrame,
    ) -> str | None:
        partition_col = table_def.partition_by
        if partition_col is None or partition_col not in data.columns:
            return None
        first_value = data[partition_col].iloc[0]
        if hasattr(first_value, "strftime"):
            return first_value.strftime("%Y-%m-%d")
        return str(first_value)


_MANAGERS: dict[str | None, CacheManager] = {}


def get_cache_manager(
    base_dir: str | None = None,
    config: CacheConfig | None = None,
) -> CacheManager:
    global _MANAGERS
    key = base_dir
    if key not in _MANAGERS:
        _MANAGERS[key] = CacheManager(base_dir=base_dir, config=config)
    return _MANAGERS[key]


def reset_cache_manager():
    global _MANAGERS
    _MANAGERS.clear()
