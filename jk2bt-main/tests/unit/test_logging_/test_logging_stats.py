"""
Tests for jk2bt/logging/stats.py - Stats Module
"""

import pytest
import tempfile
import os
import json
from jk2bt.logging.stats import (
    RequestStats,
    CacheStats,
    StatsCollector,
    get_stats_collector,
    reset_stats_collector,
)


class TestRequestStats:
    """Test RequestStats class"""

    def setup_method(self):
        self.stats = RequestStats()

    def test_initial_state(self):
        assert self.stats.total_requests == 0
        assert self.stats.successful_requests == 0
        assert self.stats.failed_requests == 0
        assert self.stats.avg_duration_ms == 0.0

    def test_avg_duration_no_requests(self):
        assert self.stats.avg_duration_ms == 0.0

    def test_success_rate_no_requests(self):
        assert self.stats.success_rate == 0.0

    def test_error_rate_no_requests(self):
        assert self.stats.error_rate == 0.0

    def test_record_successful_request(self):
        self.stats.total_requests = 1
        self.stats.successful_requests = 1
        self.stats.total_duration_ms = 100.0

        assert self.stats.success_rate == 1.0
        assert self.stats.avg_duration_ms == 100.0

    def test_record_failed_request(self):
        self.stats.total_requests = 2
        self.stats.successful_requests = 1
        self.stats.failed_requests = 1

        assert self.stats.error_rate == 0.5

    def test_to_dict(self):
        self.stats.total_requests = 10
        self.stats.successful_requests = 8
        self.stats.failed_requests = 2
        self.stats.total_duration_ms = 1000.0
        self.stats.min_duration_ms = 50.0
        self.stats.max_duration_ms = 200.0
        self.stats.errors = {"timeout": 1, "network": 1}

        d = self.stats.to_dict()
        assert d["total_requests"] == 10
        assert d["successful_requests"] == 8
        assert d["success_rate"] == 0.8


class TestCacheStats:
    """Test CacheStats class"""

    def setup_method(self):
        self.stats = CacheStats()

    def test_initial_state(self):
        assert self.stats.hits == 0
        assert self.stats.misses == 0
        assert self.stats.total_requests == 0
        assert self.stats.hit_rate == 0.0

    def test_hit_rate_calculation(self):
        self.stats.hits = 80
        self.stats.misses = 20

        assert self.stats.total_requests == 100
        assert self.stats.hit_rate == 0.8

    def test_to_dict(self):
        self.stats.hits = 75
        self.stats.misses = 25

        d = self.stats.to_dict()
        assert d["hits"] == 75
        assert d["misses"] == 25
        assert d["total_requests"] == 100
        assert d["hit_rate"] == 0.75


class TestStatsCollector:
    """Test StatsCollector class"""

    def setup_method(self):
        reset_stats_collector()
        self.collector = get_stats_collector()
        self.collector.reset()

    def teardown_method(self):
        reset_stats_collector()

    def test_singleton(self):
        collector1 = StatsCollector.get_instance()
        collector2 = StatsCollector.get_instance()
        assert collector1 is collector2

    def test_record_request_success(self):
        self.collector.record_request("akshare", 100.0, success=True)
        stats = self.collector.get_source_stats("akshare")

        assert stats["total_requests"] == 1
        assert stats["successful_requests"] == 1
        assert stats["failed_requests"] == 0

    def test_record_request_failure(self):
        self.collector.record_request(
            "akshare", 100.0, success=False, error_type="timeout"
        )
        stats = self.collector.get_source_stats("akshare")

        assert stats["total_requests"] == 1
        assert stats["failed_requests"] == 1
        assert "timeout" in stats["errors"]

    def test_record_cache_hit(self):
        self.collector.record_cache_hit("market_cache")
        stats = self.collector.get_cache_stats("market_cache")

        assert stats["hits"] == 1
        assert stats["misses"] == 0

    def test_record_cache_miss(self):
        self.collector.record_cache_miss("price_cache")
        stats = self.collector.get_cache_stats("price_cache")

        assert stats["hits"] == 0
        assert stats["misses"] == 1

    def test_get_all_stats(self):
        self.collector.record_request("source1", 100.0, success=True)
        self.collector.record_cache_hit("cache1")

        all_stats = self.collector.get_all_stats()
        assert "request_stats" in all_stats
        assert "cache_stats" in all_stats
        assert "summary" in all_stats

    def test_get_summary_text(self):
        self.collector.record_request("test_source", 50.0, success=True)
        self.collector.record_cache_hit("test_cache")

        summary_text = self.collector.get_summary_text()
        assert "JK2BT Stats Summary" in summary_text
        assert "test_source" in summary_text

    def test_reset(self):
        self.collector.record_request("source", 100.0, success=True)
        self.collector.record_cache_hit("cache")

        self.collector.reset()

        assert self.collector.get_source_stats("source") == {}
        assert self.collector.get_cache_stats("cache") == {}

    def test_export_json(self, tmp_path):
        self.collector.record_request("test_source", 100.0, success=True)

        filepath = tmp_path / "stats.json"
        self.collector.export_json(str(filepath))

        assert filepath.exists()
        with open(filepath, "r") as f:
            data = json.load(f)
            assert "request_stats" in data

    def test_export_csv(self, tmp_path):
        self.collector.record_request("test_source", 100.0, success=True)

        self.collector.export_csv(str(tmp_path))

        csv_file = tmp_path / "test_source_stats.csv"
        assert csv_file.exists()


class TestModuleFunctions:
    """Test module-level functions"""

    def setup_method(self):
        reset_stats_collector()

    def teardown_method(self):
        reset_stats_collector()

    def test_get_stats_collector(self):
        collector = get_stats_collector()
        assert isinstance(collector, StatsCollector)

    def test_reset_stats_collector(self):
        collector1 = get_stats_collector()
        collector1.record_request("test", 100.0, success=True)

        reset_stats_collector()
        collector2 = get_stats_collector()

        assert collector1 is not collector2
        assert collector2.get_source_stats("test") == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
