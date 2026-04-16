import pandas as pd
import pytest

from parquet_cache import (
    CacheManager,
    CacheTable,
    TableRegistry,
    get_cache_manager,
    reset_cache_manager,
)


def _make_registry():
    registry = TableRegistry()
    registry.register(
        CacheTable(
            name="stock_daily",
            partition_by="date",
            ttl_hours=0,
            schema={
                "symbol": "string",
                "date": "date",
                "open": "float64",
                "high": "float64",
                "low": "float64",
                "close": "float64",
                "volume": "float64",
                "amount": "float64",
                "adjust": "string",
            },
            primary_key=["symbol", "date", "adjust"],
            storage_layer="daily",
            compaction_threshold=2,
        )
    )
    registry.register(
        CacheTable(
            name="securities",
            partition_by=None,
            ttl_hours=0,
            schema={
                "symbol": "string",
                "name": "string",
            },
            primary_key=["symbol"],
            storage_layer="meta",
            aggregation_enabled=False,
            compaction_threshold=0,
        )
    )
    return registry


class TestCacheManagerPutGet:
    def test_put_and_get(self, tmp_dir, sample_stock_data):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        cm.put("stock_daily", sample_stock_data, partition_value="2024-04-01")
        result = cm.get("stock_daily")
        assert result is not None
        assert len(result) > 0

    def test_get_with_where(self, tmp_dir, sample_stock_data):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        cm.put("stock_daily", sample_stock_data, partition_value="2024-04-01")
        result = cm.get("stock_daily", where={"symbol": "600519"})
        assert result is not None
        assert all(result["symbol"] == "600519")


class TestCacheManagerMemoryCache:
    def test_memory_cache_hit(self, tmp_dir, sample_stock_data):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        cm.put("stock_daily", sample_stock_data, partition_value="2024-04-01")
        result1 = cm.get("stock_daily")
        assert result1 is not None
        assert cm.memory_cache.hit_rate > 0.0

    def test_force_refresh_skips_memory_cache(self, tmp_dir, sample_stock_data):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        cm.put("stock_daily", sample_stock_data, partition_value="2024-04-01")
        _ = cm.get("stock_daily")
        result = cm.get("stock_daily", force_refresh=True)
        assert result is not None


class TestCacheManagerPartitionInfer:
    def test_auto_infer_partition_value(self, tmp_dir, sample_stock_data):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        cm.put("stock_daily", sample_stock_data)
        result = cm.get("stock_daily")
        assert result is not None


class TestCacheManagerInvalidate:
    def test_invalidate(self, tmp_dir, sample_stock_data):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        cm.put("stock_daily", sample_stock_data, partition_value="2024-04-01")
        deleted = cm.invalidate("stock_daily")
        assert deleted >= 0
        result = cm.get("stock_daily")
        assert result is None


class TestCacheManagerExists:
    def test_exists(self, tmp_dir, sample_stock_data):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        assert cm.exists("stock_daily") is False
        cm.put("stock_daily", sample_stock_data, partition_value="2024-04-01")
        assert cm.exists("stock_daily") is True


class TestCacheManagerTableInfo:
    def test_table_info(self, tmp_dir, sample_stock_data):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        cm.put("stock_daily", sample_stock_data, partition_value="2024-04-01")
        info = cm.table_info("stock_daily")
        assert info.name == "stock_daily"
        assert info.file_count >= 1
        assert info.total_size_bytes > 0


class TestCacheManagerStats:
    def test_get_stats(self, tmp_dir, sample_stock_data):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        cm.put("stock_daily", sample_stock_data, partition_value="2024-04-01")
        stats = cm.get_stats()
        assert "memory_cache_size" in stats
        assert "memory_cache_hit_rate" in stats
        assert "tables" in stats
        assert "stock_daily" in stats["tables"]


class TestCacheManagerSingleton:
    def test_get_cache_manager_returns_same_instance(self, tmp_dir):
        reset_cache_manager()
        cm1 = get_cache_manager(base_dir=str(tmp_dir))
        cm2 = get_cache_manager(base_dir=str(tmp_dir))
        assert cm1 is cm2
        reset_cache_manager()
