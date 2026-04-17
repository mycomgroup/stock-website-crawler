"""
test_zoo.py
因子库总入口模块测试。

测试覆盖：
- get_factor_values_jq 聚宽风格因子查询接口
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestZooModuleImport:
    """测试因子库模块导入。"""

    def test_import_zoo_module(self):
        """测试因子库模块导入。"""
        from jk2bt.analysis.factors import zoo

        assert hasattr(zoo, "get_factor_values_jq")
        assert hasattr(zoo, "global_factor_registry")

    def test_get_factor_values_jq_callable(self):
        """测试get_factor_values_jq可调用。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        assert callable(get_factor_values_jq)


class TestGetFactorValuesJq:
    """测试聚宽风格因子查询接口。"""

    def test_single_security_string(self):
        """测试单证券字符串输入。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        with patch(
            "jk2bt.analysis.factors.zoo.global_factor_registry"
        ) as mock_registry:
            mock_registry.get.return_value = None
            mock_registry.list_factors.return_value = []

            result = get_factor_values_jq("sh600519", "pe_ratio")

            assert isinstance(result, dict)

    def test_multiple_securities_list(self):
        """测试多证券列表输入。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        with patch(
            "jk2bt.analysis.factors.zoo.global_factor_registry"
        ) as mock_registry:
            mock_registry.get.return_value = None
            mock_registry.list_factors.return_value = []

            result = get_factor_values_jq(
                ["sh600519", "sz000001"], ["pe_ratio", "pb_ratio"]
            )

            assert isinstance(result, dict)

    def test_single_factor_string(self):
        """测试单因子字符串输入。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        with patch(
            "jk2bt.analysis.factors.zoo.global_factor_registry"
        ) as mock_registry:
            mock_registry.get.return_value = None
            mock_registry.list_factors.return_value = []

            result = get_factor_values_jq("sh600519", "pe_ratio")

            assert isinstance(result, dict)

    def test_multiple_factors_list(self):
        """测试多因子列表输入。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        with patch(
            "jk2bt.analysis.factors.zoo.global_factor_registry"
        ) as mock_registry:
            mock_registry.get.return_value = None
            mock_registry.list_factors.return_value = []

            result = get_factor_values_jq("sh600519", ["pe_ratio", "pb_ratio", "roe"])

            assert isinstance(result, dict)

    def test_unregistered_factor(self):
        """测试未注册因子。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        with patch(
            "jk2bt.analysis.factors.zoo.global_factor_registry"
        ) as mock_registry:
            mock_registry.get.return_value = None

            result = get_factor_values_jq("sh600519", "nonexistent_factor")

            assert isinstance(result, dict)
            assert "nonexistent_factor" in result

    def test_with_end_date(self):
        """测试带截止日期。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        with patch(
            "jk2bt.analysis.factors.zoo.global_factor_registry"
        ) as mock_registry:
            mock_registry.get.return_value = None
            mock_registry.list_factors.return_value = []

            result = get_factor_values_jq("sh600519", "pe_ratio", end_date="2023-12-31")

            assert isinstance(result, dict)

    def test_with_count(self):
        """测试带count参数。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        with patch(
            "jk2bt.analysis.factors.zoo.global_factor_registry"
        ) as mock_registry:
            mock_registry.get.return_value = None
            mock_registry.list_factors.return_value = []

            result = get_factor_values_jq("sh600519", "pe_ratio", count=10)

            assert isinstance(result, dict)

    def test_with_start_date(self):
        """测试带起始日期。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        with patch(
            "jk2bt.analysis.factors.zoo.global_factor_registry"
        ) as mock_registry:
            mock_registry.get.return_value = None
            mock_registry.list_factors.return_value = []

            result = get_factor_values_jq(
                "sh600519", "pe_ratio", start_date="2023-01-01", end_date="2023-12-31"
            )

            assert isinstance(result, dict)

    def test_force_update(self):
        """测试强制更新参数。"""
        from jk2bt.analysis.factors.zoo import get_factor_values_jq

        with patch(
            "jk2bt.analysis.factors.zoo.global_factor_registry"
        ) as mock_registry:
            mock_registry.get.return_value = None
            mock_registry.list_factors.return_value = []

            result = get_factor_values_jq("sh600519", "pe_ratio", force_update=True)

            assert isinstance(result, dict)


class TestFactorRegistryIntegration:
    """测试因子注册表集成。"""

    def test_registry_in_zoo(self):
        """测试因子注册表在zoo模块中可用。"""
        from jk2bt.analysis.factors.zoo import global_factor_registry

        assert global_factor_registry is not None

    def test_list_factors(self):
        """测试列出所有因子。"""
        from jk2bt.analysis.factors import global_factor_registry

        factors = global_factor_registry.list_factors()
        assert isinstance(factors, list)
        assert len(factors) > 0

    def test_is_registered(self):
        """测试检查因子是否注册。"""
        from jk2bt.analysis.factors import global_factor_registry

        assert global_factor_registry.is_registered("pe_ratio")
        assert global_factor_registry.is_registered("pb_ratio")
        assert not global_factor_registry.is_registered("nonexistent_factor")
