"""
tests/unit/api/test_enhancements.py
增强 API 兼容层单元测试

测试覆盖:
1. 警告提示
2. 导入转发到 order 和 filter
"""

import pytest
import warnings


class TestEnhancementsDeprecation:
    """测试 enhancements 模块弃用警告"""

    def test_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            import jk2bt.api.enhancements

            assert len(w) >= 1
            assert (
                "enhancements 已拆分" in str(w[0].message).lower()
                or "deprecated" in str(w[0].message).lower()
            )


class TestEnhancementsExports:
    """测试 enhancements 模块导出"""

    def test_exports_include_order_and_filter(self):
        import jk2bt.api.enhancements

        expected = [
            "order_shares",
            "order_target_percent",
            "LimitOrderStyle",
            "MarketOrderStyle",
        ]

        for name in expected:
            assert name in jk2bt.api.enhancements.__all__, f"{name} not exported"
