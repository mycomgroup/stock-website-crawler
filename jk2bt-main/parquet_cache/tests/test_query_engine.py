import pandas as pd
import pytest

from parquet_cache.partition_manager import PartitionManager
from parquet_cache.query_engine import QueryEngine
from parquet_cache.writer import AtomicWriter


class TestQueryEngineBasic:
    def test_basic_query(self, tmp_dir, sample_stock_data):
        writer = AtomicWriter(tmp_dir)
        writer.write(
            "stock_daily",
            "daily",
            sample_stock_data,
            partition_by="date",
            partition_value="2024-04-01",
        )
        engine = QueryEngine(tmp_dir)
        result = engine.query("stock_daily", "daily", partition_by="date")
        assert result is not None
        assert len(result) > 0

    def test_no_data_returns_none(self, tmp_dir):
        engine = QueryEngine(tmp_dir)
        result = engine.query("nonexistent", "daily")
        assert result is None


class TestQueryEngineWhere:
    def _setup_data(self, tmp_dir):
        writer = AtomicWriter(tmp_dir)
        df = pd.DataFrame(
            {
                "symbol": ["600519", "000001", "600519"],
                "date": pd.to_datetime(["2024-04-01", "2024-04-01", "2024-04-02"]).date,
                "open": [1800.0, 15.5, 1810.0],
                "high": [1820.0, 15.8, 1830.0],
                "low": [1790.0, 15.3, 1800.0],
                "close": [1815.0, 15.6, 1825.0],
                "volume": [1000000.0, 5000000.0, 1200000.0],
                "amount": [1.8e9, 7.8e7, 2.2e9],
                "adjust": ["qfq", "qfq", "qfq"],
            }
        )
        for pv in ["2024-04-01", "2024-04-02"]:
            part = df[df["date"] == pd.to_datetime(pv).date()]
            writer.write(
                "stock_daily",
                "daily",
                part,
                partition_by="date",
                partition_value=pv,
            )

    def test_where_equal(self, tmp_dir):
        self._setup_data(tmp_dir)
        engine = QueryEngine(tmp_dir)
        result = engine.query(
            "stock_daily", "daily", partition_by="date", where={"symbol": "600519"}
        )
        assert result is not None
        assert all(result["symbol"] == "600519")

    def test_where_range(self, tmp_dir):
        self._setup_data(tmp_dir)
        engine = QueryEngine(tmp_dir)
        result = engine.query(
            "stock_daily",
            "daily",
            partition_by="date",
            where={"close": (1800.0, 1820.0)},
        )
        assert result is not None
        assert all((result["close"] >= 1800.0) & (result["close"] <= 1820.0))

    def test_where_in(self, tmp_dir):
        self._setup_data(tmp_dir)
        engine = QueryEngine(tmp_dir)
        result = engine.query(
            "stock_daily",
            "daily",
            partition_by="date",
            where={"symbol": ["600519", "000001"]},
        )
        assert result is not None
        assert set(result["symbol"].unique()) == {"600519", "000001"}


class TestQueryEngineColumns:
    def _setup_data(self, tmp_dir):
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

    def test_columns_selection(self, tmp_dir):
        self._setup_data(tmp_dir)
        engine = QueryEngine(tmp_dir)
        result = engine.query(
            "stock_daily", "daily", partition_by="date", columns=["symbol", "close"]
        )
        assert result is not None
        assert list(result.columns) == ["symbol", "close"]


class TestQueryEngineOrderLimit:
    def _setup_data(self, tmp_dir):
        writer = AtomicWriter(tmp_dir)
        df = pd.DataFrame(
            {
                "symbol": ["600519", "000001", "600000"],
                "date": pd.to_datetime(["2024-04-01", "2024-04-01", "2024-04-01"]).date,
                "open": [1800.0, 15.5, 10.0],
                "high": [1820.0, 15.8, 10.5],
                "low": [1790.0, 15.3, 9.8],
                "close": [1815.0, 15.6, 10.2],
                "volume": [1000000.0, 5000000.0, 3000000.0],
                "amount": [1.8e9, 7.8e7, 3.0e7],
                "adjust": ["qfq", "qfq", "qfq"],
            }
        )
        writer.write(
            "stock_daily",
            "daily",
            df,
            partition_by="date",
            partition_value="2024-04-01",
        )

    def test_order_by_limit(self, tmp_dir):
        self._setup_data(tmp_dir)
        engine = QueryEngine(tmp_dir)
        result = engine.query(
            "stock_daily",
            "daily",
            partition_by="date",
            order_by=["close DESC"],
            limit=2,
        )
        assert result is not None
        assert len(result) == 2
        assert result["close"].iloc[0] >= result["close"].iloc[1]


class TestQueryEngineAggregation:
    def _setup_data_with_agg(self, tmp_dir):
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
        pm = PartitionManager(tmp_dir)
        agg_path = pm.aggregated_path("stock_daily", "daily", "date", "2024-04-01")
        agg_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(agg_path)

    def test_aggregated_layer_preferred(self, tmp_dir):
        self._setup_data_with_agg(tmp_dir)
        engine = QueryEngine(tmp_dir)
        result = engine.query(
            "stock_daily", "daily", partition_by="date", prefer_aggregated=True
        )
        assert result is not None
        assert len(result) > 0


class TestQueryEngineExists:
    def _setup_data(self, tmp_dir):
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

    def test_exists_returns_true(self, tmp_dir):
        self._setup_data(tmp_dir)
        engine = QueryEngine(tmp_dir)
        assert engine.exists("stock_daily", "daily", partition_by="date") is True

    def test_exists_returns_false(self, tmp_dir):
        engine = QueryEngine(tmp_dir)
        assert engine.exists("nonexistent", "daily") is False


class TestQueryEngineCount:
    def _setup_data(self, tmp_dir):
        writer = AtomicWriter(tmp_dir)
        df = pd.DataFrame(
            {
                "symbol": ["600519", "000001"],
                "date": pd.to_datetime(["2024-04-01", "2024-04-01"]).date,
                "open": [1800.0, 15.5],
                "high": [1820.0, 15.8],
                "low": [1790.0, 15.3],
                "close": [1815.0, 15.6],
                "volume": [1000000.0, 5000000.0],
                "amount": [1.8e9, 7.8e7],
                "adjust": ["qfq", "qfq"],
            }
        )
        writer.write(
            "stock_daily",
            "daily",
            df,
            partition_by="date",
            partition_value="2024-04-01",
        )

    def test_count(self, tmp_dir):
        self._setup_data(tmp_dir)
        engine = QueryEngine(tmp_dir)
        cnt = engine.count("stock_daily", "daily", partition_by="date")
        assert cnt == 2
