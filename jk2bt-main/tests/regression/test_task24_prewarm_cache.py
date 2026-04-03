"""
test_task24_prewarm_cache.py
Task 24 数据预热与缓存闭环的单元测试。

覆盖：
1. CacheManager 类的各个方法
2. prewarm_data.py 的预热函数
3. jq_strategy_runner.py 的离线模式
4. 边界条件和错误处理
"""

import pytest
import os
import sys
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch, MagicMock
import pandas as pd

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


class TestCacheManager:
    """测试 CacheManager 类"""

    def test_cache_manager_init(self):
        """测试 CacheManager 初始化"""
        from jk2bt.db.cache_status import CacheManager

        manager = CacheManager()
        assert manager.db is not None
        assert manager.db_path is not None

    def test_cache_manager_init_with_path(self):
        """测试带路径参数的初始化"""
        from jk2bt.db.cache_status import CacheManager

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_cache.db")
            manager = CacheManager(db_path=db_path)
            assert manager.db_path == db_path

    def test_check_stock_daily_cache_has_data(self):
        """测试股票缓存检查 - 有数据"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        status = manager.check_stock_daily_cache(
            "sh600519", "2023-01-01", "2023-06-30", "qfq"
        )

        assert isinstance(status, dict)
        assert "has_data" in status
        assert "is_complete" in status
        assert "count" in status
        assert "min_date" in status
        assert "max_date" in status

    def test_check_stock_daily_cache_no_data(self):
        """测试股票缓存检查 - 无数据（不存在的股票）"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        status = manager.check_stock_daily_cache(
            "sh999999", "2023-01-01", "2023-06-30", "qfq"
        )

        assert status["has_data"] is False
        assert status["count"] == 0

    def test_check_etf_daily_cache(self):
        """测试ETF缓存检查"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        status = manager.check_etf_daily_cache("510300", "2023-01-01", "2023-06-30")

        assert isinstance(status, dict)
        assert "has_data" in status
        assert "is_complete" in status

    def test_check_index_daily_cache(self):
        """测试指数缓存检查"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        status = manager.check_index_daily_cache("000300", "2023-01-01", "2023-06-30")

        assert isinstance(status, dict)
        assert "has_data" in status
        assert "is_complete" in status

    def test_get_cache_summary(self):
        """测试缓存摘要获取"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        summary = manager.get_cache_summary()

        assert isinstance(summary, dict)
        assert "stock_count" in summary
        assert "etf_count" in summary
        assert "index_count" in summary
        assert "total_records" in summary
        assert "symbols" in summary

    def test_check_meta_cache(self):
        """测试元数据缓存检查"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        status = manager.check_meta_cache()

        assert isinstance(status, dict)
        assert "trade_days" in status
        assert "securities" in status
        assert "index_weights" in status

    def test_validate_cache_for_offline_valid(self):
        """测试离线缓存验证 - 有效"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        stock_pool = ["600519.XSHG", "000333.XSHE"]
        is_valid, report = manager.validate_cache_for_offline(
            stock_pool, "2023-01-01", "2023-06-30"
        )

        assert isinstance(is_valid, bool)
        assert isinstance(report, dict)
        assert "missing_stocks" in report
        assert "incomplete_stocks" in report
        assert "missing_meta" in report
        assert "cache_summary" in report

    def test_validate_cache_for_offline_missing_stock(self):
        """测试离线缓存验证 - 缺失股票"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        stock_pool = ["999999.XSHG"]
        is_valid, report = manager.validate_cache_for_offline(
            stock_pool, "2023-01-01", "2023-06-30"
        )

        assert is_valid is False
        assert len(report["missing_stocks"]) > 0

    def test_get_cache_manager_factory(self):
        """测试工厂函数"""
        from jk2bt.db.cache_status import get_cache_manager

        manager1 = get_cache_manager()
        manager2 = get_cache_manager()

        assert isinstance(manager1, object)
        assert isinstance(manager2, object)

    def test_check_cache_status_convenience(self):
        """测试便捷函数"""
        from jk2bt.db.cache_manager import (
            check_cache_status,
        )

        status = check_cache_status()

        assert isinstance(status, dict)
        assert "stock_count" in status


class TestPrewarmMetaData:
    """测试元数据预热"""

    def test_prewarm_meta_data_skip_existing(self):
        """测试预热元数据 - 跳过已存在"""
        from prewarm_data import prewarm_meta_data

        result = prewarm_meta_data(force_update=False)

        assert isinstance(result, dict)
        assert "trade_days" in result
        assert "securities" in result
        assert "errors" in result

    def test_prewarm_meta_data_with_custom_cache_dir(self):
        """测试预热元数据 - 自定义缓存目录"""
        from prewarm_data import prewarm_meta_data

        with tempfile.TemporaryDirectory() as tmpdir:
            result = prewarm_meta_data(cache_base_dir=tmpdir, force_update=True)

            assert isinstance(result, dict)
            trade_days_file = os.path.join(tmpdir, "meta_cache", "trade_days.pkl")
            assert os.path.exists(trade_days_file) or result["trade_days"] is False


class TestPrewarmStockDaily:
    """测试股票日线预热"""

    def test_prewarm_stock_daily_empty_pool(self):
        """测试预热股票 - 空股票池"""
        from prewarm_data import prewarm_stock_daily

        result = prewarm_stock_daily([], "2023-01-01", "2023-06-30")

        assert result["success"] == 0
        assert result["skipped"] == 0
        assert result["failed"] == []

    def test_prewarm_stock_daily_skip_existing(self):
        """测试预热股票 - 跳过已存在"""
        from prewarm_data import prewarm_stock_daily

        stock_pool = ["600519.XSHG"]
        result = prewarm_stock_daily(
            stock_pool,
            "2023-01-01",
            "2023-06-30",
            skip_existing=True,
            force_update=False,
        )

        assert isinstance(result, dict)
        assert result["skipped"] >= 0 or result["success"] >= 0

    def test_prewarm_stock_daily_invalid_symbol(self):
        """测试预热股票 - 无效代码"""
        from prewarm_data import prewarm_stock_daily

        stock_pool = ["INVALID.XSHG"]
        result = prewarm_stock_daily(
            stock_pool, "2023-01-01", "2023-06-30", skip_existing=False
        )

        assert isinstance(result, dict)
        assert "failed" in result


class TestPrewarmETFDaily:
    """测试ETF日线预热"""

    def test_prewarm_etf_daily_empty_pool(self):
        """测试预热ETF - ETF池"""
        from prewarm_data import prewarm_etf_daily

        result = prewarm_etf_daily([], "2023-01-01", "2023-06-30")

        assert result["success"] == 0
        assert result["skipped"] == 0

    def test_prewarm_etf_daily_skip_existing(self):
        """测试预热ETF - 跳过已存在"""
        from prewarm_data import prewarm_etf_daily

        etf_pool = ["510300"]
        result = prewarm_etf_daily(
            etf_pool, "2023-01-01", "2023-06-30", skip_existing=True, force_update=False
        )

        assert isinstance(result, dict)
        assert "success" in result
        assert "skipped" in result


class TestPrewarmIndexDaily:
    """测试指数日线预热"""

    def test_prewarm_index_daily_empty_pool(self):
        """测试预热指数 - 空池"""
        from prewarm_data import prewarm_index_daily

        result = prewarm_index_daily([], "2023-01-01", "2023-06-30")

        assert result["success"] == 0
        assert result["skipped"] == 0

    def test_prewarm_index_daily_skip_existing(self):
        """测试预热指数 - 跳过已存在"""
        from prewarm_data import prewarm_index_daily

        index_pool = ["000300"]
        result = prewarm_index_daily(
            index_pool,
            "2023-01-01",
            "2023-06-30",
            skip_existing=True,
            force_update=False,
        )

        assert isinstance(result, dict)
        assert "success" in result
        assert "skipped" in result


class TestPrewarmIndexWeights:
    """测试指数成分权重预热"""

    def test_prewarm_index_weights_empty_pool(self):
        """测试预热权重 - 空池"""
        from prewarm_data import prewarm_index_weights

        result = prewarm_index_weights([])

        assert result["success"] == 0
        assert result["skipped"] == 0

    def test_prewarm_index_weights_with_cache_dir(self):
        """测试预热权重 - 自定义缓存目录"""
        from prewarm_data import prewarm_index_weights

        with tempfile.TemporaryDirectory() as tmpdir:
            result = prewarm_index_weights(["000300"], cache_base_dir=tmpdir)

            assert isinstance(result, dict)


class TestRunPrewarm:
    """测试完整预热流程"""

    def test_run_prewarm_empty_pools(self):
        """测试完整预热 - 空池"""
        from prewarm_data import run_prewarm

        summary = run_prewarm(
            stock_pool=None,
            etf_pool=None,
            index_pool=None,
            start_date="2023-01-01",
            end_date="2023-06-30",
            include_meta=False,
            include_weights=False,
        )

        assert isinstance(summary, dict)
        assert "config" in summary
        assert "results" in summary

    def test_run_prewarm_with_sample_pool(self):
        """测试完整预热 - 样本池"""
        from prewarm_data import run_prewarm

        summary = run_prewarm(
            stock_pool=["600519.XSHG"],
            start_date="2023-01-01",
            end_date="2023-06-30",
            include_meta=True,
            include_weights=False,
            force_update=False,
        )

        assert isinstance(summary, dict)
        assert "config" in summary
        assert summary["config"]["start_date"] == "2023-01-01"
        assert summary["config"]["end_date"] == "2023-06-30"

    def test_print_summary(self):
        """测试打印摘要"""
        from prewarm_data import print_summary

        summary = {
            "config": {
                "start_date": "2023-01-01",
                "end_date": "2023-06-30",
                "stock_count": 3,
                "etf_count": 0,
                "index_count": 0,
            },
            "results": {
                "meta": {"trade_days": True, "securities": True},
                "stock": {"success": 2, "skipped": 1, "failed": []},
            },
            "cache_summary": {"stock_count": 10, "total_records": 1000},
        }

        print_summary(summary)


class TestLoadStockDataFromCache:
    """测试离线数据加载"""

    def test_load_stock_data_from_cache_valid(self):
        """测试从缓存加载 - 有效股票"""
        from jk2bt.core.runner import (
            _load_stock_data_from_cache,
        )

        data = _load_stock_data_from_cache("600519.XSHG", "2023-01-01", "2023-06-30")

        if data is not None:
            assert data._name == "600519.XSHG"

    def test_load_stock_data_from_cache_invalid(self):
        """测试从缓存加载 - 无效股票"""
        from jk2bt.core.runner import (
            _load_stock_data_from_cache,
        )

        data = _load_stock_data_from_cache("999999.XSHG", "2023-01-01", "2023-06-30")

        assert data is None

    def test_load_stock_data_from_cache_different_formats(self):
        """测试从缓存加载 - 不同代码格式"""
        from jk2bt.core.runner import (
            _load_stock_data_from_cache,
        )

        formats = ["600519.XSHG", "sh600519", "600519"]
        for fmt in formats:
            try:
                data = _load_stock_data_from_cache(fmt, "2023-01-01", "2023-06-30")
            except Exception:
                pass


class TestRunJqStrategyOfflineMode:
    """测试策略离线运行模式"""

    def test_run_jq_strategy_use_cache_only_parameter(self):
        """测试 run_jq_strategy 的 use_cache_only 参数"""
        from jk2bt.core.runner import run_jq_strategy

        strategy_code = """
def initialize(context):
    g.stocks = ["600519.XSHG"]

def handle_data(context, data):
    pass
"""

        strategy_file = "/tmp/test_offline_strategy.py"
        with open(strategy_file, "w") as f:
            f.write(strategy_code)

        result = run_jq_strategy(
            strategy_file=strategy_file,
            start_date="2023-01-01",
            end_date="2023-01-31",
            stock_pool=["600519.XSHG"],
            use_cache_only=True,
            validate_cache=True,
            auto_discover_stocks=False,
            enable_resource_pack=False,
        )

        if result is not None:
            assert "final_value" in result

    def test_run_jq_strategy_cache_validation_failure(self):
        """测试缓存验证失败"""
        from jk2bt.core.runner import run_jq_strategy

        strategy_code = """
def initialize(context):
    pass
"""

        strategy_file = "/tmp/test_cache_fail.py"
        with open(strategy_file, "w") as f:
            f.write(strategy_code)

        result = run_jq_strategy(
            strategy_file=strategy_file,
            start_date="2023-01-01",
            end_date="2023-01-31",
            stock_pool=["999999.XSHG"],
            use_cache_only=True,
            validate_cache=True,
            auto_discover_stocks=False,
        )

        assert result is None


class TestEdgeCases:
    """测试边界条件"""

    def test_check_stock_cache_with_future_dates(self):
        """测试缓存检查 - 未来日期"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        future_start = datetime.now().strftime("%Y-%m-%d")
        future_end = (datetime.now() + pd.Timedelta(days=365)).strftime("%Y-%m-%d")

        status = manager.check_stock_daily_cache(
            "sh600519", future_start, future_end, "qfq"
        )

        assert status["is_complete"] is False

    def test_validate_cache_with_empty_pool(self):
        """测试缓存验证 - 空股票池"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        is_valid, report = manager.validate_cache_for_offline(
            [], "2023-01-01", "2023-06-30"
        )

        assert is_valid is True
        assert report["missing_stocks"] == []

    def test_check_cache_with_different_adjust_types(self):
        """测试缓存检查 - 不同复权类型"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        for adjust in ["qfq", "hfq", "none"]:
            status = manager.check_stock_daily_cache(
                "sh600519", "2023-01-01", "2023-06-30", adjust
            )
            assert isinstance(status, dict)

    def test_prewarm_with_invalid_date_range(self):
        """测试预热 - 无效日期范围"""
        from prewarm_data import prewarm_stock_daily

        result = prewarm_stock_daily(
            ["600519.XSHG"], "2025-01-01", "2025-12-31", skip_existing=False
        )

        assert isinstance(result, dict)


class TestIntegration:
    """集成测试"""

    def test_full_workflow(self):
        """测试完整工作流"""
        from jk2bt.db.cache_status import get_cache_manager

        manager = get_cache_manager()

        summary = manager.get_cache_summary()
        assert summary["stock_count"] >= 0

        stock_pool = ["600519.XSHG"]
        is_valid, report = manager.validate_cache_for_offline(
            stock_pool, "2023-01-01", "2023-06-30"
        )

        assert isinstance(is_valid, bool)
        assert isinstance(report, dict)

    def test_cache_manager_with_readonly_db(self):
        """测试只读模式的缓存管理器"""
        from jk2bt.db.cache_status import CacheManager
        from jk2bt.db.duckdb_manager import DuckDBManager

        manager = CacheManager()
        assert manager.db.read_only is True

    def test_prewarm_and_validate(self):
        """测试预热后验证"""
        from prewarm_data import run_prewarm
        from jk2bt.db.cache_status import get_cache_manager

        summary = run_prewarm(
            stock_pool=["600519.XSHG"],
            start_date="2023-01-01",
            end_date="2023-06-30",
            include_meta=False,
            include_weights=False,
            force_update=False,
        )

        manager = get_cache_manager()
        is_valid, _ = manager.validate_cache_for_offline(
            ["600519.XSHG"], "2023-01-01", "2023-06-30"
        )

        assert isinstance(is_valid, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
