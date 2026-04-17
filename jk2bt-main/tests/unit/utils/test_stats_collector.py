"""
test_stats_collector.py
单元测试 - 统计收集器模块

测试场景覆盖:
1. RequestStats 请求统计
2. CacheStats 缓存统计
3. StatsCollector 单例收集器
4. 导出功能 (JSON/CSV)
5. 便捷函数
"""

import os
import json
import csv
import pytest
from unittest.mock import patch, MagicMock

from jk2bt.logging import (
    RequestStats,
    CacheStats,
    StatsCollector,
    get_stats_collector,
    reset_stats_collector,
)


@pytest.fixture(autouse=True)
def reset_collector():
    """每个测试前重置 StatsCollector 单例"""
    StatsCollector.reset_instance()
    yield
    StatsCollector.reset_instance()


class TestRequestStats:
    """测试 RequestStats"""

    def test_initial_state(self):
        stats = RequestStats()
        assert stats.total_requests == 0
        assert stats.successful_requests == 0
        assert stats.failed_requests == 0
        assert stats.total_duration_ms == 0.0
        assert stats.errors == {}
        assert stats.min_duration_ms is None
        assert stats.max_duration_ms is None

    def test_avg_duration_empty(self):
        stats = RequestStats()
        assert stats.avg_duration_ms == 0.0

    def test_success_rate_empty(self):
        stats = RequestStats()
        assert stats.success_rate == 0.0

    def test_error_rate_empty(self):
        stats = RequestStats()
        assert stats.error_rate == 0.0

    def test_to_dict_empty(self):
        stats = RequestStats()
        d = stats.to_dict()
        assert d["total_requests"] == 0
        assert d["avg_duration_ms"] == 0.0
        assert "errors" not in d

    def test_record_success(self):
        stats = RequestStats()
        stats.total_requests = 1
        stats.successful_requests = 1
        stats.total_duration_ms = 100.0
        stats.min_duration_ms = 100.0
        stats.max_duration_ms = 100.0
        assert stats.avg_duration_ms == 100.0
        assert stats.success_rate == 1.0
        assert stats.error_rate == 0.0

    def test_record_failure_with_error(self):
        stats = RequestStats()
        stats.total_requests = 1
        stats.failed_requests = 1
        stats.total_duration_ms = 50.0
        stats.min_duration_ms = 50.0
        stats.max_duration_ms = 50.0
        stats.errors["TimeoutError"] = 1
        assert stats.success_rate == 0.0
        assert stats.error_rate == 1.0

    def test_to_dict_with_errors(self):
        stats = RequestStats()
        stats.total_requests = 2
        stats.successful_requests = 1
        stats.failed_requests = 1
        stats.total_duration_ms = 150.0
        stats.min_duration_ms = 50.0
        stats.max_duration_ms = 100.0
        stats.errors["TimeoutError"] = 1
        d = stats.to_dict()
        assert "errors" in d
        assert d["errors"]["TimeoutError"] == 1
        assert d["avg_duration_ms"] == 75.0
        assert d["min_duration_ms"] == 50.0
        assert d["max_duration_ms"] == 100.0

    def test_success_rate_calculation(self):
        stats = RequestStats()
        stats.total_requests = 10
        stats.successful_requests = 7
        stats.failed_requests = 3
        assert stats.success_rate == 0.7
        assert stats.error_rate == 0.3


class TestCacheStats:
    """测试 CacheStats"""

    def test_initial_state(self):
        stats = CacheStats()
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.total_requests == 0

    def test_hit_rate_empty(self):
        stats = CacheStats()
        assert stats.hit_rate == 0.0

    def test_hit_rate_full(self):
        stats = CacheStats()
        stats.hits = 10
        assert stats.hit_rate == 1.0

    def test_hit_rate_partial(self):
        stats = CacheStats()
        stats.hits = 3
        stats.misses = 7
        assert stats.hit_rate == 0.3

    def test_to_dict(self):
        stats = CacheStats()
        stats.hits = 5
        stats.misses = 5
        d = stats.to_dict()
        assert d["hits"] == 5
        assert d["misses"] == 5
        assert d["total_requests"] == 10
        assert d["hit_rate"] == 0.5


class TestStatsCollectorSingleton:
    """测试 StatsCollector 单例模式"""

    def test_singleton_returns_same_instance(self):
        s1 = StatsCollector.get_instance()
        s2 = StatsCollector.get_instance()
        assert s1 is s2

    def test_reset_instance_creates_new(self):
        s1 = StatsCollector.get_instance()
        StatsCollector.reset_instance()
        s2 = StatsCollector.get_instance()
        assert s1 is not s2

    def test_get_stats_collector_function(self):
        collector = get_stats_collector()
        assert isinstance(collector, StatsCollector)


class TestStatsCollectorRecordRequest:
    """测试 StatsCollector 记录请求"""

    def test_record_single_success(self):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        stats = collector.get_source_stats("akshare")
        assert stats["total_requests"] == 1
        assert stats["successful_requests"] == 1
        assert stats["failed_requests"] == 0
        assert stats["avg_duration_ms"] == 100.0

    def test_record_single_failure(self):
        collector = StatsCollector.get_instance()
        collector.record_request(
            "akshare", 50.0, success=False, error_type="TimeoutError"
        )
        stats = collector.get_source_stats("akshare")
        assert stats["total_requests"] == 1
        assert stats["failed_requests"] == 1
        assert "errors" in stats
        assert stats["errors"]["TimeoutError"] == 1

    def test_record_multiple_requests(self):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        collector.record_request("akshare", 200.0, success=True)
        collector.record_request("akshare", 50.0, success=False, error_type="Error")
        stats = collector.get_source_stats("akshare")
        assert stats["total_requests"] == 3
        assert stats["successful_requests"] == 2
        assert stats["failed_requests"] == 1
        assert stats["min_duration_ms"] == 50.0
        assert stats["max_duration_ms"] == 200.0
        assert stats["avg_duration_ms"] == pytest.approx(116.67, rel=0.01)

    def test_record_multiple_sources(self):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        collector.record_request("tushare", 200.0, success=True)
        assert collector.get_source_stats("akshare")["total_requests"] == 1
        assert collector.get_source_stats("tushare")["total_requests"] == 1

    def test_record_without_error_type(self):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=False)
        stats = collector.get_source_stats("akshare")
        assert "errors" not in stats

    def test_unknown_source_returns_empty(self):
        collector = StatsCollector.get_instance()
        assert collector.get_source_stats("unknown") == {}


class TestStatsCollectorCacheStats:
    """测试 StatsCollector 缓存统计"""

    def test_record_cache_hit(self):
        collector = StatsCollector.get_instance()
        collector.record_cache_hit("daily_cache")
        stats = collector.get_cache_stats("daily_cache")
        assert stats["hits"] == 1
        assert stats["misses"] == 0

    def test_record_cache_miss(self):
        collector = StatsCollector.get_instance()
        collector.record_cache_miss("daily_cache")
        stats = collector.get_cache_stats("daily_cache")
        assert stats["hits"] == 0
        assert stats["misses"] == 1

    def test_mixed_hits_and_misses(self):
        collector = StatsCollector.get_instance()
        for _ in range(3):
            collector.record_cache_hit("cache1")
        for _ in range(7):
            collector.record_cache_miss("cache1")
        stats = collector.get_cache_stats("cache1")
        assert stats["hits"] == 3
        assert stats["misses"] == 7
        assert stats["hit_rate"] == 0.3

    def test_unknown_cache_returns_empty(self):
        collector = StatsCollector.get_instance()
        assert collector.get_cache_stats("unknown") == {}


class TestStatsCollectorGetAllStats:
    """测试 StatsCollector 获取所有统计"""

    def test_empty_stats(self):
        collector = StatsCollector.get_instance()
        all_stats = collector.get_all_stats()
        assert "request_stats" in all_stats
        assert "cache_stats" in all_stats
        assert "summary" in all_stats
        assert all_stats["summary"]["total_requests"] == 0
        assert all_stats["summary"]["overall_success_rate"] == 0.0
        assert all_stats["summary"]["cache_hit_rate"] == 0.0

    def test_summary_with_requests(self):
        collector = StatsCollector.get_instance()
        collector.record_request("src1", 100.0, success=True)
        collector.record_request("src1", 200.0, success=False)
        all_stats = collector.get_all_stats()
        summary = all_stats["summary"]
        assert summary["total_requests"] == 2
        assert summary["total_success"] == 1
        assert summary["total_failed"] == 1
        assert summary["overall_success_rate"] == 0.5
        assert summary["avg_duration_ms"] == 150.0

    def test_summary_with_cache(self):
        collector = StatsCollector.get_instance()
        collector.record_cache_hit("cache1")
        collector.record_cache_miss("cache1")
        all_stats = collector.get_all_stats()
        summary = all_stats["summary"]
        assert summary["cache_hits"] == 1
        assert summary["cache_misses"] == 1
        assert summary["cache_hit_rate"] == 0.5


class TestStatsCollectorSummaryText:
    """测试 StatsCollector 摘要文本"""

    def test_summary_text_format(self):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        text = collector.get_summary_text()
        assert "JK2BT Stats Summary" in text
        assert "Total Requests:" in text
        assert "Success Rate:" in text
        assert "Avg Duration:" in text
        assert "Cache Hit Rate:" in text

    def test_summary_text_with_cache(self):
        collector = StatsCollector.get_instance()
        collector.record_cache_hit("daily_cache")
        text = collector.get_summary_text()
        assert "Cache Stats:" in text
        assert "daily_cache" in text

    def test_summary_text_empty(self):
        collector = StatsCollector.get_instance()
        text = collector.get_summary_text()
        assert "Total Requests:    0" in text


class TestStatsCollectorExport:
    """测试 StatsCollector 导出功能"""

    def test_export_json(self, tmp_path):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        filepath = str(tmp_path / "stats.json")
        collector.export_json(filepath)
        with open(filepath, "r") as f:
            data = json.load(f)
        assert "request_stats" in data
        assert "akshare" in data["request_stats"]
        assert "exported_at" in data

    def test_export_csv(self, tmp_path):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        collector.record_request(
            "akshare", 50.0, success=False, error_type="TimeoutError"
        )
        output_dir = str(tmp_path / "csv_output")
        collector.export_csv(output_dir)
        filepath = os.path.join(output_dir, "akshare_stats.csv")
        assert os.path.exists(filepath)
        with open(filepath, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) > 1
        assert rows[0] == ["metric", "value"]

    def test_export_csv_creates_directory(self, tmp_path):
        collector = StatsCollector.get_instance()
        collector.record_request("src1", 100.0, success=True)
        output_dir = str(tmp_path / "nested" / "dir" / "output")
        collector.export_csv(output_dir)
        assert os.path.exists(output_dir)


class TestStatsCollectorReset:
    """测试 StatsCollector 重置"""

    def test_reset_clears_all_stats(self):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        collector.record_cache_hit("cache1")
        collector.reset()
        all_stats = collector.get_all_stats()
        assert all_stats["summary"]["total_requests"] == 0
        assert all_stats["summary"]["cache_hits"] == 0
        assert collector.get_source_stats("akshare") == {}
        assert collector.get_cache_stats("cache1") == {}


class TestStatsCollectorLogging:
    """测试 StatsCollector 日志功能"""

    def test_print_summary_force(self):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        with patch.object(stats_module, "logger") as mock_logger:
            collector.print_summary(force=True)
            mock_logger.info.assert_called_once()

    def test_print_summary_no_force(self):
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        with patch.object(stats_module, "logger") as mock_logger:
            collector.print_summary(force=False)
            mock_logger.debug.assert_called_once()

    def test_log_summary_with_custom_logger(self):
        mock_logger = MagicMock()
        collector = StatsCollector.get_instance()
        collector.record_request("akshare", 100.0, success=True)
        collector.log_summary(logger=mock_logger)
        mock_logger.log.assert_called_once()


class TestResetStatsCollectorFunction:
    """测试 reset_stats_collector 函数"""

    def test_reset_function(self):
        s1 = get_stats_collector()
        reset_stats_collector()
        s2 = get_stats_collector()
        assert s1 is not s2
