"""
test_source_router.py
单元测试 - 数据源路由模块

测试场景覆盖:
1. EmptyDataPolicy 枚举
2. ExecutionResult 数据类
3. SourceHealthMonitor 健康监控
4. MultiSourceRouter 路由执行
5. create_simple_router 工厂函数
"""

import sys
import time
import importlib.util
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
import pandas as pd

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


# 直接从文件路径加载模块，绕过 jk2bt/__init__.py
def _load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


source_router_path = project_root / "jk2bt" / "data" / "sources" / "router.py"
source_router = _load_module_from_path("source_router", str(source_router_path))

stats_path = project_root / "jk2bt" / "logging" / "stats.py"
stats_module = _load_module_from_path("logging_stats_for_router", str(stats_path))

EmptyDataPolicy = source_router.EmptyDataPolicy
ExecutionResult = source_router.ExecutionResult
SourceHealthMonitor = source_router.SourceHealthMonitor
MultiSourceRouter = source_router.MultiSourceRouter
create_simple_router = source_router.create_simple_router
reset_stats_collector = stats_module.reset_stats_collector


class TestEmptyDataPolicy:
    """测试 EmptyDataPolicy 枚举"""

    def test_strict_policy_value(self):
        assert EmptyDataPolicy.STRICT.value == "strict"

    def test_relaxed_policy_value(self):
        assert EmptyDataPolicy.RELAXED.value == "relaxed"

    def test_best_effort_policy_value(self):
        assert EmptyDataPolicy.BEST_EFFORT.value == "best_effort"


class TestExecutionResult:
    """测试 ExecutionResult 数据类"""

    def test_successful_result(self):
        df = pd.DataFrame({"a": [1, 2]})
        result = ExecutionResult(
            success=True,
            data=df,
            source="test_source",
            error=None,
            attempts=1,
        )
        assert result.success is True
        assert result.data is not None
        assert result.source == "test_source"
        assert result.error is None
        assert result.attempts == 1
        assert result.is_empty is False
        assert result.is_fallback is False
        assert result.sources_tried == []

    def test_failed_result(self):
        result = ExecutionResult(
            success=False,
            data=None,
            source=None,
            error="all_providers_failed",
            attempts=3,
            error_details=[("src1", "error1"), ("src2", "error2")],
        )
        assert result.success is False
        assert result.data is None
        assert result.source is None
        assert result.error == "all_providers_failed"
        assert result.attempts == 3
        assert len(result.error_details) == 2

    def test_empty_result_with_fallback(self):
        result = ExecutionResult(
            success=True,
            data=pd.DataFrame(),
            source="fallback",
            error=None,
            attempts=2,
            is_empty=True,
            is_fallback=True,
        )
        assert result.success is True
        assert result.is_empty is True
        assert result.is_fallback is True


class TestSourceHealthMonitor:
    """测试 SourceHealthMonitor"""

    def test_initial_state(self):
        monitor = SourceHealthMonitor()
        assert monitor.is_available("unknown_source") is True

    def test_record_success(self):
        monitor = SourceHealthMonitor()
        monitor.record_result("src1", success=True)
        status = monitor.get_status()
        assert status["src1"]["available"] is True
        assert status["src1"]["error_count"] == 0

    def test_record_failure_below_threshold(self):
        monitor = SourceHealthMonitor()
        for _ in range(4):
            monitor.record_result("src1", success=False, error="timeout")
        status = monitor.get_status()
        assert status["src1"]["available"] is True
        assert status["src1"]["error_count"] == 4

    def test_record_failure_reaches_threshold(self):
        monitor = SourceHealthMonitor()
        for _ in range(5):
            monitor.record_result("src1", success=False, error="timeout")
        status = monitor.get_status()
        assert status["src1"]["available"] is False
        assert status["src1"]["error_count"] == 5

    def test_source_recovery_after_disable_duration(self):
        monitor = SourceHealthMonitor()
        for _ in range(5):
            monitor.record_result("src1", success=False, error="timeout")
        assert monitor.is_available("src1") is False

        with patch.object(time, "time", return_value=time.time() + 400):
            assert monitor.is_available("src1") is True

    def test_success_resets_error_count(self):
        monitor = SourceHealthMonitor()
        for _ in range(3):
            monitor.record_result("src1", success=False, error="error")
        monitor.record_result("src1", success=True)
        status = monitor.get_status()
        assert status["src1"]["error_count"] == 0
        assert status["src1"]["available"] is True

    def test_get_status_returns_copy(self):
        monitor = SourceHealthMonitor()
        monitor.record_result("src1", success=True)
        status1 = monitor.get_status()
        status1["src1"]["available"] = False
        status2 = monitor.get_status()
        assert status2["src1"]["available"] is True


class TestMultiSourceRouterInit:
    """测试 MultiSourceRouter 初始化"""

    def test_init_with_providers(self):
        providers = [("src1", MagicMock()), ("src2", MagicMock())]
        router = MultiSourceRouter(providers=providers)
        assert len(router.providers) == 2
        assert router.required_columns == []
        assert router.min_rows == 0
        assert router.policy == EmptyDataPolicy.STRICT

    def test_init_with_cache_provider(self):
        cache_func = MagicMock()
        router = MultiSourceRouter(
            providers=[("src1", MagicMock())], cache_provider=cache_func
        )
        assert len(router.providers) == 2
        assert router.providers[1][0] == "__cache__"

    def test_init_with_validation_params(self):
        router = MultiSourceRouter(
            providers=[("src1", MagicMock())],
            required_columns=["open", "close"],
            min_rows=10,
            policy=EmptyDataPolicy.RELAXED,
        )
        assert router.required_columns == ["open", "close"]
        assert router.min_rows == 10
        assert router.policy == EmptyDataPolicy.RELAXED


class TestMultiSourceRouterExecute:
    """测试 MultiSourceRouter.execute"""

    def test_first_provider_succeeds(self):
        df = pd.DataFrame({"open": [10.0], "close": [11.0]})
        mock_func = MagicMock(return_value=df)
        router = MultiSourceRouter(providers=[("src1", mock_func)])
        result = router.execute()
        assert result.success is True
        assert result.source == "src1"
        assert result.data is not None
        assert result.attempts == 1
        assert result.is_fallback is False
        mock_func.assert_called_once()

    def test_first_fails_second_succeeds(self):
        fail_func = MagicMock(side_effect=Exception("connection error"))
        df = pd.DataFrame({"open": [10.0], "close": [11.0]})
        success_func = MagicMock(return_value=df)
        router = MultiSourceRouter(
            providers=[("src1", fail_func), ("src2", success_func)]
        )
        result = router.execute()
        assert result.success is True
        assert result.source == "src2"
        assert result.attempts == 2
        assert result.is_fallback is True

    def test_all_providers_fail(self):
        fail_func1 = MagicMock(side_effect=Exception("error1"))
        fail_func2 = MagicMock(side_effect=Exception("error2"))
        router = MultiSourceRouter(
            providers=[("src1", fail_func1), ("src2", fail_func2)]
        )
        result = router.execute()
        assert result.success is False
        assert result.source is None
        assert result.error == "all_providers_failed"
        assert len(result.error_details) == 2

    def test_provider_returns_none(self):
        none_func = MagicMock(return_value=None)
        df = pd.DataFrame({"open": [10.0]})
        success_func = MagicMock(return_value=df)
        router = MultiSourceRouter(
            providers=[("src1", none_func), ("src2", success_func)]
        )
        result = router.execute()
        assert result.success is True
        assert result.source == "src2"

    def test_provider_returns_empty_dataframe(self):
        empty_func = MagicMock(return_value=pd.DataFrame())
        df = pd.DataFrame({"open": [10.0]})
        success_func = MagicMock(return_value=df)
        router = MultiSourceRouter(
            providers=[("src1", empty_func), ("src2", success_func)]
        )
        result = router.execute()
        assert result.success is True
        assert result.source == "src2"

    def test_unavailable_provider_skipped(self):
        df = pd.DataFrame({"open": [10.0]})
        success_func = MagicMock(return_value=df)
        router = MultiSourceRouter(providers=[("src1", success_func)])
        for _ in range(5):
            router._health.record_result("src1", success=False)
        result = router.execute()
        assert result.success is False

    def test_kwargs_passed_to_provider(self):
        df = pd.DataFrame({"open": [10.0]})
        mock_func = MagicMock(return_value=df)
        router = MultiSourceRouter(providers=[("src1", mock_func)])
        router.execute(symbol="600519", start_date="2023-01-01")
        mock_func.assert_called_once_with(symbol="600519", start_date="2023-01-01")


class TestMultiSourceRouterValidation:
    """测试 MultiSourceRouter 数据验证"""

    def test_validate_with_required_columns(self):
        df = pd.DataFrame({"open": [10.0], "close": [11.0], "volume": [100]})
        mock_func = MagicMock(return_value=df)
        router = MultiSourceRouter(
            providers=[("src1", mock_func)], required_columns=["open", "close"]
        )
        result = router.execute()
        assert result.success is True

    def test_validate_missing_required_columns(self):
        df = pd.DataFrame({"open": [10.0], "high": [11.0]})
        mock_func = MagicMock(return_value=df)
        router = MultiSourceRouter(
            providers=[("src1", mock_func)], required_columns=["open", "close"]
        )
        result = router.execute()
        assert result.success is False

    def test_validate_min_rows(self):
        df = pd.DataFrame({"open": [10.0]})
        mock_func = MagicMock(return_value=df)
        router = MultiSourceRouter(providers=[("src1", mock_func)], min_rows=5)
        result = router.execute()
        assert result.success is False

    def test_validate_meets_min_rows(self):
        df = pd.DataFrame({"open": [10.0, 11.0, 12.0, 13.0, 14.0]})
        mock_func = MagicMock(return_value=df)
        router = MultiSourceRouter(providers=[("src1", mock_func)], min_rows=5)
        result = router.execute()
        assert result.success is True

    def test_validate_non_dataframe(self):
        mock_func = MagicMock(return_value="not a dataframe")
        router = MultiSourceRouter(providers=[("src1", mock_func)])
        result = router.execute()
        assert result.success is False


class TestMultiSourceRouterEmptyDataPolicy:
    """测试空数据策略"""

    def test_strict_policy_all_empty(self):
        empty_func = MagicMock(return_value=pd.DataFrame())
        router = MultiSourceRouter(
            providers=[("src1", empty_func)], policy=EmptyDataPolicy.STRICT
        )
        result = router.execute()
        assert result.success is False
        assert result.is_empty is True

    def test_relaxed_policy_all_empty(self):
        empty_func = MagicMock(return_value=pd.DataFrame())
        router = MultiSourceRouter(
            providers=[("src1", empty_func)], policy=EmptyDataPolicy.RELAXED
        )
        result = router.execute()
        assert result.success is True
        assert result.is_empty is True
        assert result.error == "all_providers_returned_empty"

    def test_best_effort_policy_all_empty(self):
        empty_func = MagicMock(return_value=pd.DataFrame())
        router = MultiSourceRouter(
            providers=[("src1", empty_func)], policy=EmptyDataPolicy.BEST_EFFORT
        )
        result = router.execute()
        assert result.success is True
        assert result.is_empty is True
        assert result.error is None


class TestMultiSourceRouterStats:
    """测试 MultiSourceRouter 统计功能"""

    def test_initial_stats(self):
        router = MultiSourceRouter(providers=[("src1", MagicMock())])
        stats = router.get_stats()
        assert stats["total_calls"] == 0
        assert stats["successes"] == 0
        assert stats["failures"] == 0
        assert stats["empty_results"] == 0
        assert stats["fallbacks"] == 0

    def test_stats_updated_on_success(self):
        df = pd.DataFrame({"open": [10.0]})
        mock_func = MagicMock(return_value=df)
        router = MultiSourceRouter(providers=[("src1", mock_func)])
        router.execute()
        stats = router.get_stats()
        assert stats["total_calls"] == 1
        assert stats["successes"] == 1
        assert "src1" in stats["source_stats"]
        assert stats["source_stats"]["src1"]["successes"] == 1

    def test_stats_updated_on_failure(self):
        reset_stats_collector()
        mock_func = MagicMock(side_effect=Exception("error"))
        router = MultiSourceRouter(providers=[("src1", mock_func)])
        router.execute()
        stats = router.get_stats()
        assert stats["total_calls"] == 1
        assert stats["failures"] == 1
        assert stats["source_stats"]["src1"]["failures"] == 1

    def test_multiple_calls_accumulate_stats(self):
        df = pd.DataFrame({"open": [10.0]})
        mock_func = MagicMock(return_value=df)
        router = MultiSourceRouter(providers=[("src1", mock_func)])
        router.execute()
        router.execute()
        stats = router.get_stats()
        assert stats["total_calls"] == 2
        assert stats["successes"] == 2

    def test_stats_collector_import_error_handled(self):
        df = pd.DataFrame({"open": [10.0]})
        mock_func = MagicMock(return_value=df)
        router = MultiSourceRouter(providers=[("src1", mock_func)])
        # _try_import_stats_collector 在没有 stats_collector 模块时返回 None
        router.execute()
        stats = router.get_stats()
        assert stats["successes"] == 1


class TestCreateSimpleRouter:
    """测试 create_simple_router 工厂函数"""

    def test_create_from_dict(self):
        callables = {"src1": MagicMock(), "src2": MagicMock()}
        router = create_simple_router(callables=callables)
        assert len(router.providers) == 2
        assert isinstance(router, MultiSourceRouter)

    def test_create_with_all_params(self):
        cache_func = MagicMock()
        router = create_simple_router(
            callables={"src1": MagicMock()},
            required_columns=["open"],
            min_rows=1,
            policy=EmptyDataPolicy.BEST_EFFORT,
            cache_provider=cache_func,
        )
        assert router.required_columns == ["open"]
        assert router.min_rows == 1
        assert router.policy == EmptyDataPolicy.BEST_EFFORT
        assert len(router.providers) == 2

    def test_execute_created_router(self):
        df = pd.DataFrame({"open": [10.0]})
        callables = {"src1": MagicMock(return_value=df)}
        router = create_simple_router(callables=callables)
        result = router.execute()
        assert result.success is True
        assert result.source == "src1"
