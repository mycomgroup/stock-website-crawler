import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from jk2bt.utils.paths import resolve_cache_path


@dataclass
class TableConfig:
    partition_by: str | None = None
    ttl_hours: int = 0
    compaction_threshold: int = 20
    aggregation_enabled: bool = True


@dataclass
class CacheConfig:
    base_dir: str = resolve_cache_path("data_cache/cache")
    memory_cache_max_items: int = 5000
    memory_cache_default_ttl_seconds: int = 3600
    compression: str = "snappy"
    row_group_size: int = 100_000
    aggregation_enabled: bool = True
    aggregation_schedule: str = "daily"
    lock_dir: str = ""
    duckdb_read_only: bool = True
    duckdb_threads: int = 4
    duckdb_memory_limit: str = "4GB"
    cleanup_retention_hours: int = 24
    log_level: str = "INFO"
    tables: dict[str, TableConfig] = field(default_factory=dict)

    @classmethod
    def from_json(cls, path: str) -> "CacheConfig":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        tables_data = data.pop("tables", {})
        tables = {name: TableConfig(**cfg) for name, cfg in tables_data.items()}

        return cls(**data, tables=tables)

    def to_dict(self) -> dict:
        return {
            "base_dir": self.base_dir,
            "memory_cache_max_items": self.memory_cache_max_items,
            "memory_cache_default_ttl_seconds": self.memory_cache_default_ttl_seconds,
            "compression": self.compression,
            "row_group_size": self.row_group_size,
            "aggregation_enabled": self.aggregation_enabled,
            "aggregation_schedule": self.aggregation_schedule,
            "lock_dir": self.lock_dir,
            "duckdb_read_only": self.duckdb_read_only,
            "duckdb_threads": self.duckdb_threads,
            "duckdb_memory_limit": self.duckdb_memory_limit,
            "cleanup_retention_hours": self.cleanup_retention_hours,
            "log_level": self.log_level,
            "tables": {
                name: {
                    "partition_by": cfg.partition_by,
                    "ttl_hours": cfg.ttl_hours,
                    "compaction_threshold": cfg.compaction_threshold,
                    "aggregation_enabled": cfg.aggregation_enabled,
                }
                for name, cfg in self.tables.items()
            },
        }

    def get_table_config(self, table_name: str) -> TableConfig:
        return self.tables.get(table_name, TableConfig())

    @property
    def lock_dir_path(self) -> Path:
        if self.lock_dir:
            return Path(self.lock_dir)
        return Path(self.base_dir) / "_locks"

    @property
    def aggregated_dir(self) -> Path:
        return Path(self.base_dir) / "aggregated"


def _apply_env_overrides(config: CacheConfig) -> CacheConfig:
    base_dir = os.environ.get("PARQUET_CACHE_BASE_DIR")
    if base_dir:
        config.base_dir = base_dir

    max_items = os.environ.get("PARQUET_CACHE_MAX_ITEMS")
    if max_items:
        config.memory_cache_max_items = int(max_items)

    log_level = os.environ.get("PARQUET_CACHE_LOG_LEVEL")
    if log_level:
        config.log_level = log_level

    return config


def _make_default_tables() -> dict[str, TableConfig]:
    common = {"partition_by": "date", "ttl_hours": 0, "compaction_threshold": 20}
    return {
        "stock_daily": TableConfig(**common),
        "etf_daily": TableConfig(**common),
        "index_daily": TableConfig(**common),
        "finance_indicator": TableConfig(
            partition_by="report_date",
            ttl_hours=2160,
            compaction_threshold=5,
        ),
        "securities": TableConfig(
            partition_by=None, ttl_hours=0, compaction_threshold=0
        ),
        "trade_calendar": TableConfig(
            partition_by=None, ttl_hours=0, compaction_threshold=0
        ),
    }


DEFAULT_CONFIG = _apply_env_overrides(CacheConfig(tables=_make_default_tables()))
