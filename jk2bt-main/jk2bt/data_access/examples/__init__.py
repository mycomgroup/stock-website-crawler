"""
src/data_access/examples/__init__.py
数据访问层使用示例。
"""

from .usage_example import (
    example_get_data_source,
    example_get_daily_data,
    example_get_index_stocks,
    example_get_trading_days,
    example_get_money_flow,
    example_use_mock_data_source,
    example_inject_mock_data,
    example_cache_management,
    example_health_check,
    example_complete_workflow,
)

__all__ = [
    "example_get_data_source",
    "example_get_daily_data",
    "example_get_index_stocks",
    "example_get_trading_days",
    "example_get_money_flow",
    "example_use_mock_data_source",
    "example_inject_mock_data",
    "example_cache_management",
    "example_health_check",
    "example_complete_workflow",
]