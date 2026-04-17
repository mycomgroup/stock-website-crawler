"""
test_migrate.py
测试数据迁移模块
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import os


class TestParseFunctions:
    """测试解析函数"""

    def test_parse_stock_pickle_filename(self):
        """测试解析股票 pickle 文件名"""
        from jk2bt.data.storage.migrate import parse_stock_pickle_filename

        result = parse_stock_pickle_filename("sh600000_stock_qfq.pkl")
        assert result is not None
        assert result["symbol"] == "sh600000"
        assert result["adjust"] == "qfq"

    def test_parse_stock_pickle_filename_hfq(self):
        """测试解析后复权"""
        from jk2bt.data.storage.migrate import parse_stock_pickle_filename

        result = parse_stock_pickle_filename("sh600000_stock_hfq.pkl")
        assert result["adjust"] == "hfq"

    def test_parse_stock_pickle_filename_none(self):
        """测试解析不复权"""
        from jk2bt.data.storage.migrate import parse_stock_pickle_filename

        result = parse_stock_pickle_filename("sh600000_stock_none.pkl")
        assert result["adjust"] == "none"

    def test_parse_stock_pickle_filename_jq_format(self):
        """测试解析聚宽格式"""
        from jk2bt.data.storage.migrate import parse_stock_pickle_filename

        result = parse_stock_pickle_filename("600000.XSHG_jq_qfq_daily.pkl")
        assert result is not None

    def test_parse_etf_pickle_filename(self):
        """测试解析 ETF pickle 文件名"""
        from jk2bt.data.storage.migrate import parse_etf_pickle_filename

        result = parse_etf_pickle_filename("510300.pkl")
        assert result is not None
        assert result["symbol"] == "510300"

    def test_parse_etf_pickle_filename_invalid(self):
        """测试解析无效 ETF 文件名"""
        from jk2bt.data.storage.migrate import parse_etf_pickle_filename

        result = parse_etf_pickle_filename("invalid_file.pkl")
        assert result is None

    def test_parse_index_pickle_filename(self):
        """测试解析指数 pickle 文件名"""
        from jk2bt.data.storage.migrate import parse_index_pickle_filename

        result = parse_index_pickle_filename("000300.pkl")
        assert result is not None
        assert result["symbol"] == "000300"

    def test_parse_index_pickle_filename_invalid(self):
        """测试解析无效指数文件名"""
        from jk2bt.data.storage.migrate import parse_index_pickle_filename

        result = parse_index_pickle_filename("invalid_file.pkl")
        assert result is None


class TestMigrationFunctions:
    """测试迁移函数"""

    @patch("jk2bt.data.storage.migrate.ParquetAdapter")
    def test_migrate_stock_pickles_nonexistent_dir(self, mock_adapter):
        """测试迁移不存在的目录"""
        from jk2bt.data.storage.migrate import migrate_stock_pickles

        result = migrate_stock_pickles("/nonexistent/path")
        assert result == 0

    @patch("jk2bt.data.storage.migrate.ParquetAdapter")
    def test_migrate_etf_pickles_nonexistent_dir(self, mock_adapter):
        """测试迁移不存在的 ETF 目录"""
        from jk2bt.data.storage.migrate import migrate_etf_pickles

        result = migrate_etf_pickles("/nonexistent/path")
        assert result == 0

    @patch("jk2bt.data.storage.migrate.ParquetAdapter")
    def test_migrate_index_pickles_nonexistent_dir(self, mock_adapter):
        """测试迁移不存在的指数目录"""
        from jk2bt.data.storage.migrate import migrate_index_pickles

        result = migrate_index_pickles("/nonexistent/path")
        assert result == 0

    @patch("jk2bt.data.storage.migrate.ParquetAdapter")
    def test_migrate_meta_pickles_nonexistent_dir(self, mock_adapter):
        """测试迁移不存在的元数据目录"""
        from jk2bt.data.storage.migrate import migrate_meta_pickles

        result = migrate_meta_pickles("/nonexistent/path")
        assert result == 0

    @patch("jk2bt.data.storage.migrate.ParquetAdapter")
    def test_migrate_index_weights_pickles_nonexistent_dir(self, mock_adapter):
        """测试迁移不存在的指数权重目录"""
        from jk2bt.data.storage.migrate import migrate_index_weights_pickles

        result = migrate_index_weights_pickles("/nonexistent/path")
        assert result == 0


class TestAutoMigrate:
    """测试自动迁移函数"""

    @patch("jk2bt.data.storage.migrate.ParquetAdapter")
    def test_auto_migrate_returns_dict(self, mock_adapter):
        """测试自动迁移返回字典"""
        from jk2bt.data.storage.migrate import auto_migrate

        with patch("os.path.exists", return_value=False):
            result = auto_migrate("/nonexistent/path")

        assert isinstance(result, dict)
        assert "stock" in result
        assert "etf" in result
        assert "index" in result
        assert "meta" in result
        assert "index_weights" in result


class TestMigrationFunctionSignatures:
    """测试迁移函数签名"""

    def test_migrate_stock_pickles_signature(self):
        """测试 migrate_stock_pickles 函数签名"""
        from jk2bt.data.storage.migrate import migrate_stock_pickles
        import inspect

        sig = inspect.signature(migrate_stock_pickles)
        params = list(sig.parameters.keys())
        assert "pickle_dir" in params
        assert "db" in params

    def test_migrate_etf_pickles_signature(self):
        """测试 migrate_etf_pickles 函数签名"""
        from jk2bt.data.storage.migrate import migrate_etf_pickles
        import inspect

        sig = inspect.signature(migrate_etf_pickles)
        params = list(sig.parameters.keys())
        assert "pickle_dir" in params
        assert "db" in params

    def test_migrate_index_pickles_signature(self):
        """测试 migrate_index_pickles 函数签名"""
        from jk2bt.data.storage.migrate import migrate_index_pickles
        import inspect

        sig = inspect.signature(migrate_index_pickles)
        params = list(sig.parameters.keys())
        assert "pickle_dir" in params
        assert "db" in params

    def test_auto_migrate_signature(self):
        """测试 auto_migrate 函数签名"""
        from jk2bt.data.storage.migrate import auto_migrate
        import inspect

        sig = inspect.signature(auto_migrate)
        params = list(sig.parameters.keys())
        assert "base_dir" in params


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
