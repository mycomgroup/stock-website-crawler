"""
tests/unit/api/test_missing_apis.py
缺失 API 兼容层单元测试

测试覆盖:
1. 警告提示
2. 导入转发到 finance 和 stats
"""

import pytest
import warnings


class TestMissingApisDeprecation:
    """测试 missing_apis 模块弃用警告"""

    def test_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            import jk2bt.api.missing_apis

            assert len(w) >= 1
            assert (
                "missing_apis 已拆分" in str(w[0].message).lower()
                or "deprecated" in str(w[0].message).lower()
            )


class TestMissingApisExports:
    """测试 missing_apis 模块导出"""

    def test_exports_include_finance(self):
        import jk2bt.api.missing_apis

        expected = [
            "get_locked_shares",
            "get_fund_info",
            "get_fundamentals_continuously",
        ]

        for name in expected:
            assert name in jk2bt.api.missing_apis.__all__, f"{name} not exported"

    def test_exports_include_get_beta(self):
        import jk2bt.api.missing_apis

        assert "get_beta" in jk2bt.api.missing_apis.__all__
