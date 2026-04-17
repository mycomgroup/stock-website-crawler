import multiprocessing
import time

import pandas as pd
import pytest

from jk2bt.cache import (
    Aggregator,
    CacheManager,
    CacheTable,
    TableRegistry,
    reset_cache_manager,
)
from .writer import AtomicWriter


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
            aggregation_enabled=True,
            compaction_threshold=2,
        )
    )
    registry.register(
        CacheTable(
            name="etf_daily",
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
            },
            primary_key=["symbol", "date"],
            storage_layer="daily",
            aggregation_enabled=True,
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
    registry.register(
        CacheTable(
            name="spot_snapshot",
            partition_by="date",
            ttl_hours=168,
            schema={
                "symbol": "string",
                "date": "date",
                "price": "float64",
                "change_pct": "float64",
                "volume": "float64",
                "amount": "float64",
                "turnover_rate": "float64",
                "pe": "float64",
                "pb": "float64",
                "market_cap": "float64",
            },
            primary_key=["symbol", "date"],
            compaction_threshold=1,
            storage_layer="snapshot",
            priority="P0",
            aggregation_enabled=True,
        )
    )
    return registry


class TestIntegrationFullWorkflow:
    def test_put_aggregate_get(self, tmp_dir):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        stock_data = pd.DataFrame(
            {
                "symbol": ["600519", "600519", "600519"],
                "date": pd.to_datetime(["2024-04-01", "2024-04-01", "2024-04-01"]).date,
                "open": [1800.0, 1805.0, 1810.0],
                "high": [1820.0, 1825.0, 1830.0],
                "low": [1790.0, 1795.0, 1800.0],
                "close": [1815.0, 1820.0, 1825.0],
                "volume": [1000000.0, 1100000.0, 1200000.0],
                "amount": [1.8e9, 1.9e9, 2.0e9],
                "adjust": ["qfq", "qfq", "qfq"],
            }
        )
        cm.put("stock_daily", stock_data, partition_value="2024-04-01")
        result = cm.get("stock_daily", where={"symbol": "600519"})
        assert result is not None
        assert len(result) > 0
        aggregator = Aggregator(tmp_dir, registry=registry)
        aggregator.aggregate_table("stock_daily")
        result_after_agg = cm.get("stock_daily", where={"symbol": "600519"})
        assert result_after_agg is not None
        assert len(result_after_agg) == 1


class TestIntegrationConcurrentPut:
    def _worker_put(self, base_dir, worker_id):
        registry = _make_registry()
        cm = CacheManager(base_dir=base_dir, registry=registry)
        df = pd.DataFrame(
            {
                "symbol": [f"worker{worker_id}"],
                "date": pd.to_datetime(["2024-04-01"]).date,
                "open": [100.0],
                "high": [101.0],
                "low": [99.0],
                "close": [100.5],
                "volume": [1000.0],
                "amount": [100000.0],
                "adjust": ["qfq"],
            }
        )
        cm.put("stock_daily", df, partition_value="2024-04-01")

    def test_multiprocess_put_single_get(self, tmp_dir):
        processes = []
        for i in range(2):
            p = multiprocessing.Process(target=self._worker_put, args=(str(tmp_dir), i))
            processes.append(p)
            p.start()
        for p in processes:
            p.join(timeout=30)
        for p in processes:
            assert p.exitcode == 0
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        result = cm.get("stock_daily")
        assert result is not None
        assert len(result) == 2


class TestIntegrationMultipleRounds:
    def test_put_aggregate_cleanup_cycle(self, tmp_dir):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        aggregator = Aggregator(tmp_dir, registry=registry)
        for round_idx in range(2):
            for pv in ["2024-04-01", "2024-04-02"]:
                df = pd.DataFrame(
                    {
                        "symbol": ["600519"],
                        "date": pd.to_datetime([pv]).date,
                        "open": [1800.0 + round_idx],
                        "high": [1820.0 + round_idx],
                        "low": [1790.0 + round_idx],
                        "close": [1815.0 + round_idx],
                        "volume": [1000000.0],
                        "amount": [1.8e9],
                        "adjust": ["qfq"],
                    }
                )
                cm.put("stock_daily", df, partition_value=pv)
            aggregator.aggregate_table("stock_daily")
        time.sleep(0.1)
        aggregator.cleanup(retention_hours=0)
        result = cm.get("stock_daily")
        assert result is not None


class TestIntegrationDifferentTableTypes:
    def test_daily_table(self, tmp_dir):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        df = pd.DataFrame(
            {
                "symbol": ["600519"],
                "date": pd.to_datetime(["2024-04-01"]).date,
                "open": [1800.0],
                "high": [1820.0],
                "low": [1790.0],
                "close": [1815.0],
                "volume": [1000000.0],
                "amount": [1.8e9],
                "adjust": ["qfq"],
            }
        )
        cm.put("stock_daily", df, partition_value="2024-04-01")
        result = cm.get("stock_daily")
        assert result is not None

    def test_meta_table(self, tmp_dir):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        df = pd.DataFrame(
            {
                "symbol": ["600519"],
                "name": ["贵州茅台"],
            }
        )
        cm.put("securities", df)
        result = cm.get("securities")
        assert result is not None
        assert len(result) == 1

    def test_snapshot_table(self, tmp_dir):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        df = pd.DataFrame(
            {
                "symbol": ["600519"],
                "date": pd.to_datetime(["2024-04-01"]).date,
                "price": [1815.0],
                "change_pct": [1.5],
                "volume": [1000000.0],
                "amount": [1.8e9],
                "turnover_rate": [0.5],
                "pe": [30.0],
                "pb": [10.0],
                "market_cap": [2.2e12],
            }
        )
        cm.put("spot_snapshot", df, partition_value="2024-04-01")
        result = cm.get("spot_snapshot")
        assert result is not None

    def test_etf_table(self, tmp_dir):
        registry = _make_registry()
        cm = CacheManager(base_dir=str(tmp_dir), registry=registry)
        df = pd.DataFrame(
            {
                "symbol": ["510300"],
                "date": pd.to_datetime(["2024-04-01"]).date,
                "open": [3.8],
                "high": [3.85],
                "low": [3.78],
                "close": [3.82],
                "volume": [10000000.0],
                "amount": [3.82e7],
            }
        )
        cm.put("etf_daily", df, partition_value="2024-04-01")
        result = cm.get("etf_daily")
        assert result is not None
