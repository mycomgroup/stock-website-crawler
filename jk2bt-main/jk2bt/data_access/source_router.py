"""Multi-source data router with automatic failover.

Adapted from akshare-one-enhanced for jk2bt project.
Provides automatic failover across multiple data sources.
"""

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import pandas as pd

logger = logging.getLogger(__name__)


class EmptyDataPolicy(Enum):
    """Policy for handling empty results."""

    STRICT = "strict"
    RELAXED = "relaxed"
    BEST_EFFORT = "best_effort"


@dataclass
class ExecutionResult:
    """Result of a multi-source execution."""

    success: bool
    data: Optional[pd.DataFrame]
    source: Optional[str]
    error: Optional[str]
    attempts: int
    error_details: Optional[List[Tuple[str, str]]] = None
    is_empty: bool = False
    is_fallback: bool = False
    sources_tried: List[Dict[str, Any]] = field(default_factory=list)


def _try_import_stats_collector():
    """Lazily import StatsCollector to avoid circular dependency."""
    try:
        from .stats_collector import get_stats_collector

        return get_stats_collector()
    except (ImportError, AttributeError):
        return None


class SourceHealthMonitor:
    """Monitor health of data sources with simple circuit breaker."""

    _ERROR_THRESHOLD = 5
    _DISABLE_DURATION = 300

    def __init__(self):
        self._status: Dict[str, Dict[str, Any]] = {}

    def record_result(
        self, source: str, success: bool, error: Optional[str] = None
    ) -> None:
        if source not in self._status:
            self._status[source] = {
                "available": True,
                "last_error": None,
                "error_count": 0,
            }
        status = self._status[source]
        if success:
            status["available"] = True
            status["error_count"] = 0
            status["last_error"] = None
        else:
            status["error_count"] += 1
            status["last_error"] = error
            if status["error_count"] >= self._ERROR_THRESHOLD:
                status["available"] = False
                status["disabled_at"] = time.time()
                logger.warning("数据源 %s 被临时禁用（错误次数过多）", source)

    def is_available(self, source: str) -> bool:
        if source not in self._status:
            return True
        status = self._status[source]
        if not status["available"]:
            disabled_at = status.get("disabled_at")
            if disabled_at is not None:
                elapsed = time.time() - disabled_at
                if elapsed > self._DISABLE_DURATION:
                    status["available"] = True
                    status["error_count"] = 0
                    logger.info("数据源 %s 已恢复", source)
        return status["available"]

    def get_status(self) -> Dict[str, Dict[str, Any]]:
        import copy

        return copy.deepcopy(self._status)


class MultiSourceRouter:
    """Routes data requests across multiple sources with automatic failover.

    Accepts a list of (name, callable) tuples. Each callable should return
    a pandas DataFrame or raise an exception on failure.
    """

    def __init__(
        self,
        providers: List[Tuple[str, Callable]],
        required_columns: Optional[List[str]] = None,
        min_rows: int = 0,
        policy: EmptyDataPolicy = EmptyDataPolicy.STRICT,
        cache_provider: Optional[Callable] = None,
    ):
        self.providers = list(providers)
        if cache_provider is not None:
            self.providers.append(("__cache__", cache_provider))
        self.required_columns = required_columns or []
        self.min_rows = min_rows
        self.policy = policy
        self._health = SourceHealthMonitor()
        self._stats: Dict[str, Any] = {
            "total_calls": 0,
            "successes": 0,
            "failures": 0,
            "empty_results": 0,
            "fallbacks": 0,
            "source_stats": {},
        }

    def execute(self, **kwargs) -> ExecutionResult:
        """Execute data fetch across providers with automatic failover.

        Tries each provider in order until one returns valid data.
        """
        self._stats["total_calls"] += 1
        error_details: List[Tuple[str, str]] = []
        sources_tried: List[Dict[str, Any]] = []
        last_result: Optional[pd.DataFrame] = None
        last_source: Optional[str] = None
        last_empty: bool = False

        for name, func in self.providers:
            if not self._health.is_available(name):
                logger.debug("Provider %s is unavailable, skipping", name)
                continue

            source_info = {
                "name": name,
                "attempted": False,
                "success": False,
                "error": None,
                "elapsed": 0.0,
            }
            source_info["attempted"] = True
            start = time.time()

            try:
                logger.debug("Trying provider: %s", name)
                data = func(**kwargs)
                elapsed = time.time() - start
                source_info["elapsed"] = elapsed
                self._health.record_result(name, success=True)

                if data is None or (isinstance(data, pd.DataFrame) and data.empty):
                    logger.debug("Provider %s returned empty data", name)
                    source_info["success"] = True
                    sources_tried.append(source_info)
                    last_result = data if isinstance(data, pd.DataFrame) else None
                    last_source = name
                    last_empty = True
                    continue

                if not self._validate_result(data):
                    logger.debug("Provider %s returned invalid data", name)
                    source_info["error"] = "validation_failed"
                    sources_tried.append(source_info)
                    continue

                is_fallback = len(sources_tried) > 0 or name == "__cache__"
                self._update_stats(
                    name,
                    success=True,
                    empty=False,
                    fallback=is_fallback,
                    duration_ms=elapsed * 1000,
                )
                source_info["success"] = True
                sources_tried.append(source_info)

                return ExecutionResult(
                    success=True,
                    data=data,
                    source=name,
                    error=None,
                    attempts=len(sources_tried),
                    error_details=error_details,
                    is_empty=False,
                    is_fallback=is_fallback,
                    sources_tried=sources_tried,
                )

            except Exception as e:
                elapsed = time.time() - start
                source_info["elapsed"] = elapsed
                source_info["error"] = str(e)
                sources_tried.append(source_info)
                error_details.append((name, str(e)))
                logger.warning("Provider %s failed: %s", name, e)
                self._health.record_result(name, success=False, error=str(e))
                self._update_stats(
                    name,
                    success=False,
                    empty=False,
                    fallback=False,
                    duration_ms=elapsed * 1000,
                    error_type=type(e).__name__,
                )

        # No provider returned valid data
        if last_empty and self.policy in (
            EmptyDataPolicy.BEST_EFFORT,
            EmptyDataPolicy.RELAXED,
        ):
            is_fallback = len(sources_tried) > 1 or last_source == "__cache__"
            self._update_stats(
                last_source, success=True, empty=True, fallback=is_fallback
            )
            return ExecutionResult(
                success=True,
                data=last_result,
                source=last_source,
                error="all_providers_returned_empty"
                if self.policy == EmptyDataPolicy.RELAXED
                else None,
                attempts=len(sources_tried),
                error_details=error_details,
                is_empty=True,
                is_fallback=is_fallback,
                sources_tried=sources_tried,
            )

        self._stats["failures"] += 1
        error_msg = (
            "all_providers_failed" if not last_empty else "all_providers_returned_empty"
        )
        return ExecutionResult(
            success=False,
            data=None,
            source=None,
            error=error_msg,
            attempts=len(sources_tried),
            error_details=error_details,
            is_empty=last_empty,
            is_fallback=False,
            sources_tried=sources_tried,
        )

    def _validate_result(self, data: pd.DataFrame) -> bool:
        """Validate that the result meets requirements."""
        if not isinstance(data, pd.DataFrame):
            return False
        if len(data) < self.min_rows:
            return False
        for col in self.required_columns:
            if col not in data.columns:
                return False
        return True

    def _update_stats(
        self,
        source: str,
        success: bool,
        empty: bool,
        fallback: bool,
        duration_ms: float = 0.0,
        error_type: str = None,
    ) -> None:
        """Update internal statistics and report to global StatsCollector."""
        if success:
            self._stats["successes"] += 1
        if empty:
            self._stats["empty_results"] += 1
        if fallback:
            self._stats["fallbacks"] += 1

        if source:
            if source not in self._stats["source_stats"]:
                self._stats["source_stats"][source] = {
                    "successes": 0,
                    "failures": 0,
                    "empty": 0,
                }
            if success:
                self._stats["source_stats"][source]["successes"] += 1
            else:
                self._stats["source_stats"][source]["failures"] += 1
            if empty:
                self._stats["source_stats"][source]["empty"] += 1

        # Report to global StatsCollector
        stats = _try_import_stats_collector()
        if stats is not None:
            stats.record_request(source, duration_ms, success, error_type=error_type)

    def get_stats(self) -> Dict[str, Any]:
        """Return current statistics."""
        return dict(self._stats)


def create_simple_router(
    callables: Dict[str, Callable],
    required_columns: Optional[List[str]] = None,
    min_rows: int = 0,
    policy: EmptyDataPolicy = EmptyDataPolicy.STRICT,
    cache_provider: Optional[Callable] = None,
) -> MultiSourceRouter:
    """Create a MultiSourceRouter from a dict of {name: callable}.

    Args:
        callables: Dict mapping source names to callable functions.
        required_columns: List of column names that must be present.
        min_rows: Minimum number of rows required.
        policy: Policy for handling empty results.
        cache_provider: Optional cache provider callable.

    Returns:
        A configured MultiSourceRouter instance.
    """
    providers = [(name, func) for name, func in callables.items()]
    return MultiSourceRouter(
        providers=providers,
        required_columns=required_columns,
        min_rows=min_rows,
        policy=policy,
        cache_provider=cache_provider,
    )
