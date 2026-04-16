import multiprocessing
import os

import pandas as pd
import pytest

from parquet_cache.schema_validator import SchemaValidationError
from parquet_cache.writer import AtomicWriter


class TestAtomicWriterBasic:
    def test_write_basic(self, tmp_dir, sample_stock_data):
        writer = AtomicWriter(tmp_dir)
        path = writer.write(
            "stock_daily",
            "daily",
            sample_stock_data,
            partition_by="date",
            partition_value="2024-04-01",
        )
        assert path.exists()
        assert path.suffix == ".parquet"
        assert ".tmp" not in str(path)

    def test_write_meta(self, tmp_dir):
        writer = AtomicWriter(tmp_dir)
        df = pd.DataFrame(
            {
                "symbol": ["600519"],
                "name": ["贵州茅台"],
            }
        )
        path = writer.write_meta("securities", df)
        assert path.exists()
        assert path.name == "securities.parquet"

    def test_write_meta_overwrite(self, tmp_dir):
        writer = AtomicWriter(tmp_dir)
        df1 = pd.DataFrame({"symbol": ["600519"], "name": ["A"]})
        df2 = pd.DataFrame({"symbol": ["000001"], "name": ["B"]})
        path1 = writer.write_meta("securities", df1)
        path2 = writer.write_meta("securities", df2)
        assert path1 == path2
        result = pd.read_parquet(path2)
        assert len(result) == 1
        assert result["symbol"].iloc[0] == "000001"


class TestAtomicWriterAtomicity:
    def test_no_tmp_file_left(self, tmp_dir, sample_stock_data):
        writer = AtomicWriter(tmp_dir)
        writer.write(
            "stock_daily",
            "daily",
            sample_stock_data,
            partition_by="date",
            partition_value="2024-04-01",
        )
        partition_path = tmp_dir / "daily" / "stock_daily" / "date=2024-04-01"
        tmp_files = list(partition_path.glob("*.tmp"))
        assert len(tmp_files) == 0


class TestAtomicWriterConcurrency:
    def _worker_write(self, base_dir, worker_id):
        writer = AtomicWriter(base_dir)
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
        writer.write(
            "stock_daily",
            "daily",
            df,
            partition_by="date",
            partition_value="2024-04-01",
        )

    def test_multiprocess_concurrent_write(self, tmp_dir):
        processes = []
        for i in range(2):
            p = multiprocessing.Process(target=self._worker_write, args=(tmp_dir, i))
            processes.append(p)
            p.start()
        for p in processes:
            p.join(timeout=30)
        for p in processes:
            assert p.exitcode == 0
        partition_path = tmp_dir / "daily" / "stock_daily" / "date=2024-04-01"
        parquet_files = list(partition_path.glob("*.parquet"))
        assert len(parquet_files) == 2


class TestAtomicWriterValidation:
    def test_schema_validation_failure(self, tmp_dir):
        writer = AtomicWriter(tmp_dir)
        df = pd.DataFrame(
            {
                "symbol": ["600519"],
                "close": [1800.0],
            }
        )
        schema = {"symbol": "string", "date": "date", "close": "float64"}
        with pytest.raises(SchemaValidationError):
            writer.write(
                "stock_daily",
                "daily",
                df,
                partition_by="date",
                partition_value="2024-04-01",
                schema=schema,
            )


class TestAtomicWriterEmpty:
    def test_write_empty_dataframe(self, tmp_dir):
        writer = AtomicWriter(tmp_dir)
        df = pd.DataFrame()
        path = writer.write(
            "stock_daily",
            "daily",
            df,
            partition_by="date",
            partition_value="2024-04-01",
        )
        assert path.exists()
        result = pd.read_parquet(path)
        assert len(result) == 0
