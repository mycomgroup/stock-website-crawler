"""
test_akshare_compat.py
测试 AkShare 兼容层
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAkShareCompatAdapter:
    """测试 AkShareCompatAdapter 类"""

    def test_function_aliases_exist(self):
        """验证函数别名映射存在"""
        from jk2bt.data.sources.akshare_compat import FUNCTION_ALIASES

        assert isinstance(FUNCTION_ALIASES, dict)
        assert len(FUNCTION_ALIASES) > 0
        assert "stock_zh_a_daily" in FUNCTION_ALIASES
        assert FUNCTION_ALIASES["stock_zh_a_daily"] == "stock_zh_a_hist"

    def test_min_supported_version(self):
        """验证最低支持版本定义"""
        from jk2bt.data.sources.akshare_compat import MIN_SUPPORTED_VERSION

        assert isinstance(MIN_SUPPORTED_VERSION, tuple)
        assert len(MIN_SUPPORTED_VERSION) == 3
        assert MIN_SUPPORTED_VERSION > (0, 0, 0)

    def test_adapter_creation(self):
        """测试适配器创建"""
        from jk2bt.data.sources.akshare_compat import AkShareCompatAdapter

        adapter = AkShareCompatAdapter()
        assert adapter is not None
        assert hasattr(adapter, "_version")
        assert hasattr(adapter, "_func_cache")

    def test_version_detection(self):
        """测试版本检测"""
        from jk2bt.data.sources.akshare_compat import AkShareCompatAdapter

        adapter = AkShareCompatAdapter()
        version = adapter.version
        version_tuple = adapter.version_tuple

        assert isinstance(version, str)
        assert isinstance(version_tuple, tuple)
        assert len(version_tuple) == 3

    def test_has_function_caching(self):
        """测试函数存在检查缓存"""
        from jk2bt.data.sources.akshare_compat import AkShareCompatAdapter

        adapter = AkShareCompatAdapter()

        result1 = adapter._has_function("stock_zh_a_hist")
        result2 = adapter._has_function("stock_zh_a_hist")

        assert result1 == result2
        assert isinstance(result1, bool)

    def test_resolve_function_name_direct(self):
        """测试直接解析函数名"""
        from jk2bt.data.sources.akshare_compat import AkShareCompatAdapter

        adapter = AkShareCompatAdapter()
        resolved = adapter.resolve_function_name("stock_zh_a_hist")
        assert resolved == "stock_zh_a_hist"

    def test_resolve_function_name_alias(self):
        """测试别名解析"""
        from jk2bt.data.sources.akshare_compat import AkShareCompatAdapter

        adapter = AkShareCompatAdapter()
        # stock_zh_a_daily exists, so it returns as-is
        resolved = adapter.resolve_function_name("stock_zh_a_daily")
        assert resolved == "stock_zh_a_daily"
        # nonexistent_xyz doesn't exist, alias should be used
        resolved2 = adapter.resolve_function_name("nonexistent_xyz")
        assert resolved2 == "nonexistent_xyz"

    def test_resolve_function_name_nonexistent(self):
        """测试不存在函数的解析"""
        from jk2bt.data.sources.akshare_compat import AkShareCompatAdapter

        adapter = AkShareCompatAdapter()
        resolved = adapter.resolve_function_name("nonexistent_function_xyz")
        assert resolved == "nonexistent_function_xyz"

    @patch("jk2bt.data.sources.akshare_compat.akshare")
    def test_call_with_kwargs(self, mock_akshare):
        """测试带参数的调用"""
        from jk2bt.data.sources.akshare_compat import AkShareCompatAdapter

        mock_func = MagicMock(return_value={"result": "test"})
        mock_akshare.stock_zh_a_hist = mock_func

        adapter = AkShareCompatAdapter()
        result = adapter.call("stock_zh_a_hist", symbol="600519", period="daily")

        assert result == {"result": "test"}
        mock_func.assert_called_once()

    def test_get_compat_adapter_singleton(self):
        """测试全局单例获取"""
        from jk2bt.data.sources.akshare_compat import (
            get_compat_adapter,
            _global_adapter,
        )

        adapter1 = get_compat_adapter()
        adapter2 = get_compat_adapter()

        assert adapter1 is adapter2


class TestFunctionAliases:
    """测试函数别名映射"""

    def test_alias_mapping_completeness(self):
        """验证别名映射完整性"""
        from jk2bt.data.sources.akshare_compat import FUNCTION_ALIASES

        for old_name, new_name in FUNCTION_ALIASES.items():
            assert isinstance(old_name, str)
            assert isinstance(new_name, str)
            assert old_name != new_name

    def test_common_aliases_present(self):
        """验证常见别名存在"""
        from jk2bt.data.sources.akshare_compat import FUNCTION_ALIASES

        assert "stock_zh_a_daily" in FUNCTION_ALIASES
        assert "stock_zh_a_spot" in FUNCTION_ALIASES
        assert "stock_fund_flow_individual" in FUNCTION_ALIASES


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
