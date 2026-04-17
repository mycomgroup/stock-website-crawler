"""
test_cache_config.py
测试缓存配置模块
"""

import pytest
from dataclasses import is_dataclass


class TestTableSchema:
    """测试 TableSchema 数据类"""

    def test_import(self):
        """测试导入"""
        from jk2bt.data.storage.cache_config import TableSchema

        assert is_dataclass(TableSchema)

    def test_creation(self):
        """测试创建"""
        from jk2bt.data.storage.cache_config import TableSchema

        schema = TableSchema(
            name="test_table",
            columns=[("col1", "VARCHAR"), ("col2", "INTEGER")],
            primary_key=["col1"],
            indexes=["col2"],
        )
        assert schema.name == "test_table"
        assert len(schema.columns) == 2
        assert schema.primary_key == ["col1"]


class TestCachePolicy:
    """测试 CachePolicy 数据类"""

    def test_import(self):
        """测试导入"""
        from jk2bt.data.storage.cache_config import CachePolicy

        assert is_dataclass(CachePolicy)

    def test_creation(self):
        """测试创建"""
        from jk2bt.data.storage.cache_config import CachePolicy

        policy = CachePolicy(domain="test", ttl_hours=24, max_memory_items=1000)
        assert policy.domain == "test"
        assert policy.ttl_hours == 24


class TestCacheSchemas:
    """测试预定义缓存架构"""

    def test_meta_schemas_exist(self):
        """测试 META_SCHEMAS 存在"""
        from jk2bt.data.storage.cache_config import META_SCHEMAS

        assert isinstance(META_SCHEMAS, list)
        assert len(META_SCHEMAS) > 0

    def test_meta_schemas_have_trade_days(self):
        """测试交易日历 schema"""
        from jk2bt.data.storage.cache_config import META_SCHEMAS

        names = [s.name for s in META_SCHEMAS]
        assert "trade_days" in names

    def test_meta_schemas_have_securities(self):
        """测试证券列表 schema"""
        from jk2bt.data.storage.cache_config import META_SCHEMAS

        names = [s.name for s in META_SCHEMAS]
        assert "securities" in names

    def test_market_schemas_exist(self):
        """测试 MARKET_SCHEMAS 存在"""
        from jk2bt.data.storage.cache_config import MARKET_SCHEMAS

        assert isinstance(MARKET_SCHEMAS, list)
        assert len(MARKET_SCHEMAS) > 0

    def test_market_schemas_have_stock_daily(self):
        """测试股票日线 schema"""
        from jk2bt.data.storage.cache_config import MARKET_SCHEMAS

        names = [s.name for s in MARKET_SCHEMAS]
        assert "stock_daily" in names

    def test_market_schemas_have_etf_daily(self):
        """测试 ETF 日线 schema"""
        from jk2bt.data.storage.cache_config import MARKET_SCHEMAS

        names = [s.name for s in MARKET_SCHEMAS]
        assert "etf_daily" in names

    def test_market_schemas_have_index_daily(self):
        """测试指数日线 schema"""
        from jk2bt.data.storage.cache_config import MARKET_SCHEMAS

        names = [s.name for s in MARKET_SCHEMAS]
        assert "index_daily" in names

    def test_option_schemas_exist(self):
        """测试 OPTION_SCHEMAS 存在"""
        from jk2bt.data.storage.cache_config import OPTION_SCHEMAS

        assert isinstance(OPTION_SCHEMAS, list)

    def test_conversion_bond_schemas_exist(self):
        """测试 CONVERSION_BOND_SCHEMAS 存在"""
        from jk2bt.data.storage.cache_config import CONVERSION_BOND_SCHEMAS

        assert isinstance(CONVERSION_BOND_SCHEMAS, list)

    def test_macro_schemas_exist(self):
        """测试 MACRO_SCHEMAS 存在"""
        from jk2bt.data.storage.cache_config import MACRO_SCHEMAS

        assert isinstance(MACRO_SCHEMAS, list)


class TestDefaultPolicies:
    """测试默认缓存策略"""

    def test_default_policies_exist(self):
        """测试 DEFAULT_POLICIES 存在"""
        from jk2bt.data.storage.cache_config import DEFAULT_POLICIES

        assert isinstance(DEFAULT_POLICIES, list)
        assert len(DEFAULT_POLICIES) > 0

    def test_policy_domains(self):
        """测试策略覆盖的域"""
        from jk2bt.data.storage.cache_config import DEFAULT_POLICIES

        domains = [p.domain for p in DEFAULT_POLICIES]
        assert "meta" in domains
        assert "market" in domains
        assert "option" in domains


class TestDomainDbMapping:
    """测试域数据库映射"""

    def test_domain_db_mapping_exist(self):
        """测试 DOMAIN_DB_MAPPING 存在"""
        from jk2bt.data.storage.cache_config import DOMAIN_DB_MAPPING

        assert isinstance(DOMAIN_DB_MAPPING, dict)
        assert len(DOMAIN_DB_MAPPING) > 0

    def test_mapping_has_required_domains(self):
        """测试映射包含必需的域"""
        from jk2bt.data.storage.cache_config import DOMAIN_DB_MAPPING

        assert "meta" in DOMAIN_DB_MAPPING
        assert "market" in DOMAIN_DB_MAPPING

    def test_mapping_structure(self):
        """测试映射结构"""
        from jk2bt.data.storage.cache_config import DOMAIN_DB_MAPPING

        for domain, config in DOMAIN_DB_MAPPING.items():
            assert "db_path" in config
            assert "schemas" in config
            assert isinstance(config["schemas"], list)


class TestInitDefaultCache:
    """测试默认缓存初始化"""

    def test_init_default_cache_exists(self):
        """测试 init_default_cache 函数存在"""
        from jk2bt.data.storage.cache_config import init_default_cache

        assert callable(init_default_cache)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
