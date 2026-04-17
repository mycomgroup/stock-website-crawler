"""
test_meta_cache_api.py
测试元数据缓存 API
"""

import pytest
from unittest.mock import patch, MagicMock


class TestMetaCacheApiImports:
    """测试 API 导入"""

    def test_import_functions(self):
        """测试导入函数"""
        from jk2bt.data.storage.meta_cache_api import (
            get_trade_days_from_cache,
            get_securities_from_cache,
            get_security_info_from_cache,
            prewarm_meta_cache,
            check_meta_cache_status,
        )

        assert callable(get_trade_days_from_cache)
        assert callable(get_securities_from_cache)
        assert callable(get_security_info_from_cache)
        assert callable(prewarm_meta_cache)
        assert callable(check_meta_cache_status)


class TestGetTradeDaysFromCache:
    """测试 get_trade_days_from_cache 函数"""

    @patch("jk2bt.data.storage.meta_cache_api._ensure_initialized")
    @patch("jk2bt.data.storage.meta_cache_api.get_cache_manager")
    def test_function_exists(self, mock_cache_mgr, mock_init):
        """测试函数存在"""
        from jk2bt.data.storage.meta_cache_api import get_trade_days_from_cache

        assert callable(get_trade_days_from_cache)

    @patch("jk2bt.data.storage.meta_cache_api._ensure_initialized")
    @patch("jk2bt.data.storage.meta_cache_api.get_cache_manager")
    def test_returns_list(self, mock_cache_mgr, mock_init):
        """测试返回列表"""
        mock_instance = MagicMock()
        mock_cache_mgr.return_value = mock_instance
        mock_instance.get.return_value = MagicMock(empty=False)

        from jk2bt.data.storage.meta_cache_api import get_trade_days_from_cache

        result = get_trade_days_from_cache()
        assert isinstance(result, list)


class TestGetSecuritiesFromCache:
    """测试 get_securities_from_cache 函数"""

    @patch("jk2bt.data.storage.meta_cache_api._ensure_initialized")
    @patch("jk2bt.data.storage.meta_cache_api.get_cache_manager")
    def test_function_exists(self, mock_cache_mgr, mock_init):
        """测试函数存在"""
        from jk2bt.data.storage.meta_cache_api import get_securities_from_cache

        assert callable(get_securities_from_cache)


class TestGetSecurityInfoFromCache:
    """测试 get_security_info_from_cache 函数"""

    @patch("jk2bt.data.storage.meta_cache_api._ensure_initialized")
    @patch("jk2bt.data.storage.meta_cache_api.get_cache_manager")
    def test_function_exists(self, mock_cache_mgr, mock_init):
        """测试函数存在"""
        from jk2bt.data.storage.meta_cache_api import get_security_info_from_cache

        assert callable(get_security_info_from_cache)


class TestPrewarmMetaCache:
    """测试 prewarm_meta_cache 函数"""

    @patch("jk2bt.data.storage.meta_cache_api._ensure_initialized")
    @patch("jk2bt.data.storage.meta_cache_api.get_trade_days_from_cache")
    @patch("jk2bt.data.storage.meta_cache_api.get_securities_from_cache")
    def test_function_exists(self, mock_securities, mock_days, mock_init):
        """测试函数存在"""
        from jk2bt.data.storage.meta_cache_api import prewarm_meta_cache

        assert callable(prewarm_meta_cache)


class TestCheckMetaCacheStatus:
    """测试 check_meta_cache_status 函数"""

    @patch("jk2bt.data.storage.meta_cache_api._ensure_initialized")
    @patch("jk2bt.data.storage.meta_cache_api.get_cache_manager")
    def test_function_exists(self, mock_cache_mgr, mock_init):
        """测试函数存在"""
        from jk2bt.data.storage.meta_cache_api import check_meta_cache_status

        assert callable(check_meta_cache_status)

    @patch("jk2bt.data.storage.meta_cache_api._ensure_initialized")
    @patch("jk2bt.data.storage.meta_cache_api.get_cache_manager")
    def test_returns_dict(self, mock_cache_mgr, mock_init):
        """测试返回字典"""
        mock_instance = MagicMock()
        mock_cache_mgr.return_value = mock_instance
        mock_instance.get.return_value = MagicMock()

        from jk2bt.data.storage.meta_cache_api import check_meta_cache_status

        result = check_meta_cache_status()
        assert isinstance(result, dict)


class TestMetaCacheInitializer:
    """测试元数据缓存初始化器"""

    def test_meta_initializer_exists(self):
        """测试 _meta_initializer 存在"""
        from jk2bt.data.storage.meta_cache_api import _meta_initializer

        assert _meta_initializer is not None

    def test_ensure_initialized_exists(self):
        """测试 _ensure_initialized 函数存在"""
        from jk2bt.data.storage.meta_cache_api import _ensure_initialized

        assert callable(_ensure_initialized)


class TestFunctionSignatures:
    """测试函数签名"""

    def test_get_trade_days_from_cache_signature(self):
        """测试 get_trade_days_from_cache 签名"""
        from jk2bt.data.storage.meta_cache_api import get_trade_days_from_cache
        import inspect

        sig = inspect.signature(get_trade_days_from_cache)
        params = list(sig.parameters.keys())
        assert "force_update" in params
        assert "use_duckdb" in params

    def test_get_securities_from_cache_signature(self):
        """测试 get_securities_from_cache 签名"""
        from jk2bt.data.storage.meta_cache_api import get_securities_from_cache
        import inspect

        sig = inspect.signature(get_securities_from_cache)
        params = list(sig.parameters.keys())
        assert "types" in params
        assert "force_update" in params
        assert "use_duckdb" in params

    def test_get_security_info_from_cache_signature(self):
        """测试 get_security_info_from_cache 签名"""
        from jk2bt.data.storage.meta_cache_api import get_security_info_from_cache
        import inspect

        sig = inspect.signature(get_security_info_from_cache)
        params = list(sig.parameters.keys())
        assert "code" in params
        assert "force_update" in params
        assert "use_duckdb" in params

    def test_prewarm_meta_cache_signature(self):
        """测试 prewarm_meta_cache 签名"""
        from jk2bt.data.storage.meta_cache_api import prewarm_meta_cache
        import inspect

        sig = inspect.signature(prewarm_meta_cache)
        params = list(sig.parameters.keys())
        assert "force_update" in params
        assert "include_trade_days" in params
        assert "include_securities" in params


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
