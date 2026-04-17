"""
test_stats_collector.py
测试统计收集器（兼容层）
"""

import pytest
from unittest.mock import patch, MagicMock


class TestStatsCollectorImport:
    """测试 StatsCollector 导入"""

    def test_import_from_module(self):
        """测试从模块导入"""
        from jk2bt.logging.stats import (
            StatsCollector,
            get_stats_collector,
            reset_stats_collector,
        )

        assert StatsCollector is not None
        assert get_stats_collector is not None
        assert reset_stats_collector is not None

    def test_stats_collector_re_exports(self):
        """测试 StatsCollector 是从 jk2bt.logging.stats 重新导出的"""
        from jk2bt.logging.stats import StatsCollector
        from jk2bt.logging.stats import StatsCollector as OriginalStatsCollector

        assert StatsCollector is OriginalStatsCollector


class TestStatsCollectorForwarding:
    """测试兼容层正确转发到 jk2bt.logging.stats"""

    def test_get_stats_collector_returns_singleton(self):
        """测试获取统计收集器单例"""
        from jk2bt.logging.stats import get_stats_collector

        collector1 = get_stats_collector()
        collector2 = get_stats_collector()
        assert collector1 is collector2

    def test_reset_stats_collector(self):
        """测试重置统计收集器"""
        from jk2bt.logging.stats import (
            reset_stats_collector,
            get_stats_collector,
        )

        reset_stats_collector()
        collector1 = get_stats_collector()
        reset_stats_collector()
        collector2 = get_stats_collector()
        assert collector1 is not None
        assert collector2 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
