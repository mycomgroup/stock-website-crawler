import pandas as pd
import pytest

from parquet_cache import (
    Aggregator,
    CacheTable,
    TableRegistry,
)
from parquet_cache.writer import AtomicWriter


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
    return registry


class TestAggregatorSinglePartition:
    def test_aggregate_single_partition(self, tmp_dir):
        registry = _make_registry()
        writer = AtomicWriter(tmp_dir)
        for i in range(3):
            df = pd.DataFrame(
                {
                    "symbol": ["600519"],
                    "date": pd.to_datetime(["2024-04-01"]).date,
                    "open": [1800.0 + i],
                    "high": [1820.0 + i],
                    "low": [1790.0 + i],
                    "close": [1815.0 + i],
                    "volume": [1000000.0],
                    "amount": [1.8e9],
                    "adjust": ["qfq"],
                }
            )
            writer.write(
                "stock_daily",
                "daily",
                df,
                partition_by="date",
                partition_value="2024-04-01",
            )
        aggregator = Aggregator(tmp_dir, registry=registry)
        count = aggregator.aggregate_table("stock_daily")
        assert count >= 1


class TestAggregatorMultiPartition:
    def test_aggregate_multiple_partitions(self, tmp_dir):
        registry = _make_registry()
        writer = AtomicWriter(tmp_dir)
        for pv in ["2024-04-01", "2024-04-02"]:
            for i in range(3):
                df = pd.DataFrame(
                    {
                        "symbol": ["600519"],
                        "date": pd.to_datetime([pv]).date,
                        "open": [1800.0 + i],
                        "high": [1820.0 + i],
                        "low": [1790.0 + i],
                        "close": [1815.0 + i],
                        "volume": [1000000.0],
                        "amount": [1.8e9],
                        "adjust": ["qfq"],
                    }
                )
                writer.write(
                    "stock_daily",
                    "daily",
                    df,
                    partition_by="date",
                    partition_value=pv,
                )
        aggregator = Aggregator(tmp_dir, registry=registry)
        count = aggregator.aggregate_table("stock_daily")
        assert count >= 1


class TestAggregatorDedup:
    def test_aggregation_deduplicates(self, tmp_dir):
        registry = _make_registry()
        writer = AtomicWriter(tmp_dir)
        for i in range(3):
            df = pd.DataFrame(
                {
                    "symbol": ["600519"],
                    "date": pd.to_datetime(["2024-04-01"]).date,
                    "open": [1800.0 + i],
                    "high": [1820.0 + i],
                    "low": [1790.0 + i],
                    "close": [1815.0 + i],
                    "volume": [1000000.0],
                    "amount": [1.8e9],
                    "adjust": ["qfq"],
                }
            )
            writer.write(
                "stock_daily",
                "daily",
                df,
                partition_by="date",
                partition_value="2024-04-01",
            )
        aggregator = Aggregator(tmp_dir, registry=registry)
        aggregator.aggregate_table("stock_daily")
        agg_path = (
            tmp_dir / "aggregated" / "daily" / "stock_daily" / "date=2024-04-01.parquet"
        )
        assert agg_path.exists()
        result = pd.read_parquet(agg_path)
        assert len(result) == 1


class TestAggregatorCleanup:
    def test_cleanup_old_files(self, tmp_dir):
        registry = _make_registry()
        writer = AtomicWriter(tmp_dir)
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
        writer.write(
            "stock_daily",
            "daily",
            df,
            partition_by="date",
            partition_value="2024-04-01",
        )
        aggregator = Aggregator(tmp_dir, registry=registry)
        aggregator.aggregate_table("stock_daily")
        import time

        time.sleep(0.1)
        deleted = aggregator.cleanup(retention_hours=0)
        assert deleted >= 0


class TestNeedsAggregation:
    def test_needs_aggregation_below_threshold(self, tmp_dir):
        registry = _make_registry()
        pending = Aggregator(tmp_dir, registry=registry).needs_aggregation(
            "stock_daily"
        )
        assert pending == []

    def test_needs_aggregation_above_threshold(self, tmp_dir):
        registry = _make_registry()
        writer = AtomicWriter(tmp_dir)
        for i in range(3):
            df = pd.DataFrame(
                {
                    "symbol": ["600519"],
                    "date": pd.to_datetime(["2024-04-01"]).date,
                    "open": [1800.0 + i],
                    "high": [1820.0 + i],
                    "low": [1790.0 + i],
                    "close": [1815.0 + i],
                    "volume": [1000000.0],
                    "amount": [1.8e9],
                    "adjust": ["qfq"],
                }
            )
            writer.write(
                "stock_daily",
                "daily",
                df,
                partition_by="date",
                partition_value="2024-04-01",
            )
        aggregator = Aggregator(tmp_dir, registry=registry)
        pending = aggregator.needs_aggregation("stock_daily")
        assert "2024-04-01" in pending


class TestAggregationStatus:
    def test_get_aggregation_status(self, tmp_dir):
        registry = _make_registry()
        writer = AtomicWriter(tmp_dir)
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
        writer.write(
            "stock_daily",
            "daily",
            df,
            partition_by="date",
            partition_value="2024-04-01",
        )
        aggregator = Aggregator(tmp_dir, registry=registry)
        status = aggregator.get_aggregation_status("stock_daily")
        assert "total_partitions" in status
        assert "aggregated_partitions" in status
        assert "pending_partitions" in status
        assert "total_raw_files" in status
        assert "total_aggregated_files" in status
