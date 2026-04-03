"""
db/cache_config.py
预定义的表结构和缓存策略配置。

使用方式:
    from jk2bt.db.cache_config import (
        META_SCHEMAS, MARKET_SCHEMAS, DEFAULT_POLICIES
    )
"""

from typing import List
from .unified_cache import TableSchema, CachePolicy


META_SCHEMAS: List[TableSchema] = [
    TableSchema(
        name="trade_days",
        columns=[
            ("date", "DATE NOT NULL"),
        ],
        primary_key=["date"],
        indexes=["date"],
    ),
    TableSchema(
        name="securities",
        columns=[
            ("code", "VARCHAR NOT NULL"),
            ("jq_code", "VARCHAR"),  # 聚宽格式代码，如 '600519.XSHG'
            ("display_name", "VARCHAR"),
            ("name", "VARCHAR"),  # 原始名称
            ("start_date", "DATE"),
            ("end_date", "DATE"),
            ("type", "VARCHAR"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["code"],
        indexes=["type", "jq_code", "start_date"],
    ),
    TableSchema(
        name="security_info",
        columns=[
            ("code", "VARCHAR NOT NULL"),
            ("info_json", "VARCHAR"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["code"],
        indexes=["update_time"],
    ),
]


MARKET_SCHEMAS: List[TableSchema] = [
    TableSchema(
        name="stock_daily",
        columns=[
            ("symbol", "VARCHAR NOT NULL"),
            ("datetime", "DATE NOT NULL"),
            ("open", "DOUBLE"),
            ("high", "DOUBLE"),
            ("low", "DOUBLE"),
            ("close", "DOUBLE"),
            ("volume", "BIGINT"),
            ("amount", "DOUBLE"),
            ("adjust", "VARCHAR DEFAULT 'qfq'"),
        ],
        primary_key=["symbol", "datetime", "adjust"],
        indexes=["symbol", "datetime"],
    ),
    TableSchema(
        name="etf_daily",
        columns=[
            ("symbol", "VARCHAR NOT NULL"),
            ("datetime", "DATE NOT NULL"),
            ("open", "DOUBLE"),
            ("high", "DOUBLE"),
            ("low", "DOUBLE"),
            ("close", "DOUBLE"),
            ("volume", "BIGINT"),
            ("amount", "DOUBLE"),
        ],
        primary_key=["symbol", "datetime"],
        indexes=["symbol", "datetime"],
    ),
    TableSchema(
        name="index_daily",
        columns=[
            ("symbol", "VARCHAR NOT NULL"),
            ("datetime", "DATE NOT NULL"),
            ("open", "DOUBLE"),
            ("high", "DOUBLE"),
            ("low", "DOUBLE"),
            ("close", "DOUBLE"),
            ("volume", "BIGINT"),
            ("amount", "DOUBLE"),
        ],
        primary_key=["symbol", "datetime"],
        indexes=["symbol", "datetime"],
    ),
    TableSchema(
        name="stock_minute",
        columns=[
            ("symbol", "VARCHAR NOT NULL"),
            ("datetime", "TIMESTAMP NOT NULL"),
            ("period", "VARCHAR NOT NULL"),
            ("open", "DOUBLE"),
            ("high", "DOUBLE"),
            ("low", "DOUBLE"),
            ("close", "DOUBLE"),
            ("volume", "BIGINT"),
            ("money", "DOUBLE"),
            ("adjust", "VARCHAR DEFAULT 'qfq'"),
        ],
        primary_key=["symbol", "datetime", "period", "adjust"],
        indexes=["symbol", "datetime", "period"],
    ),
    TableSchema(
        name="etf_minute",
        columns=[
            ("symbol", "VARCHAR NOT NULL"),
            ("datetime", "TIMESTAMP NOT NULL"),
            ("period", "VARCHAR NOT NULL"),
            ("open", "DOUBLE"),
            ("high", "DOUBLE"),
            ("low", "DOUBLE"),
            ("close", "DOUBLE"),
            ("volume", "BIGINT"),
            ("money", "DOUBLE"),
        ],
        primary_key=["symbol", "datetime", "period"],
        indexes=["symbol", "datetime", "period"],
    ),
]


OPTION_SCHEMAS: List[TableSchema] = [
    TableSchema(
        name="option_list",
        columns=[
            ("underlying", "VARCHAR NOT NULL"),
            ("option_code", "VARCHAR NOT NULL"),
            ("option_name", "VARCHAR"),
            ("strike_price", "DOUBLE"),
            ("expiry_date", "DATE"),
            ("option_type", "VARCHAR"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["underlying", "option_code"],
        indexes=["expiry_date", "option_type"],
    ),
    TableSchema(
        name="option_daily",
        columns=[
            ("option_code", "VARCHAR NOT NULL"),
            ("datetime", "DATE NOT NULL"),
            ("open", "DOUBLE"),
            ("high", "DOUBLE"),
            ("low", "DOUBLE"),
            ("close", "DOUBLE"),
            ("volume", "BIGINT"),
            ("amount", "DOUBLE"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["option_code", "datetime"],
        indexes=["option_code", "datetime"],
    ),
    TableSchema(
        name="option_greeks",
        columns=[
            ("option_code", "VARCHAR NOT NULL"),
            ("date", "DATE NOT NULL"),
            ("delta", "DOUBLE"),
            ("gamma", "DOUBLE"),
            ("theta", "DOUBLE"),
            ("vega", "DOUBLE"),
            ("implied_vol", "DOUBLE"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["option_code", "date"],
        indexes=["option_code", "date"],
    ),
]


CONVERSION_BOND_SCHEMAS: List[TableSchema] = [
    TableSchema(
        name="cb_list",
        columns=[
            ("bond_code", "VARCHAR NOT NULL"),
            ("bond_name", "VARCHAR"),
            ("stock_code", "VARCHAR"),
            ("conversion_price", "DOUBLE"),
            ("issue_date", "DATE"),
            ("maturity_date", "DATE"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["bond_code"],
        indexes=["stock_code", "maturity_date"],
    ),
    TableSchema(
        name="cb_daily",
        columns=[
            ("bond_code", "VARCHAR NOT NULL"),
            ("datetime", "DATE NOT NULL"),
            ("open", "DOUBLE"),
            ("high", "DOUBLE"),
            ("low", "DOUBLE"),
            ("close", "DOUBLE"),
            ("volume", "BIGINT"),
            ("amount", "DOUBLE"),
            ("conversion_value", "DOUBLE"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["bond_code", "datetime"],
        indexes=["bond_code", "datetime"],
    ),
]


MACRO_SCHEMAS: List[TableSchema] = [
    TableSchema(
        name="macro_data",
        columns=[
            ("indicator", "VARCHAR NOT NULL"),
            ("date", "DATE NOT NULL"),
            ("value", "DOUBLE"),
            ("unit", "VARCHAR"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["indicator", "date"],
        indexes=["indicator", "date"],
    ),
]


SHARE_CHANGE_SCHEMAS: List[TableSchema] = [
    TableSchema(
        name="share_change",
        columns=[
            ("code", "VARCHAR NOT NULL"),
            ("shareholder_name", "VARCHAR"),
            ("change_date", "DATE NOT NULL"),
            ("change_type", "VARCHAR"),
            ("change_amount", "BIGINT"),
            ("change_ratio", "DOUBLE"),
            ("hold_amount_after", "BIGINT"),
            ("hold_ratio_after", "DOUBLE"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["code", "shareholder_name", "change_date"],
        indexes=["code", "change_date"],
    ),
]


UNLOCK_SCHEMAS: List[TableSchema] = [
    TableSchema(
        name="unlock_data",
        columns=[
            ("code", "VARCHAR NOT NULL"),
            ("unlock_date", "DATE NOT NULL"),
            ("unlock_amount", "BIGINT"),
            ("unlock_ratio", "DOUBLE"),
            ("holder_name", "VARCHAR"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["code", "unlock_date", "holder_name"],
        indexes=["code", "unlock_date"],
    ),
    TableSchema(
        name="unlock_calendar",
        columns=[
            ("date", "DATE NOT NULL"),
            ("total_unlock_amount", "BIGINT"),
            ("unlock_count", "INTEGER"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["date"],
        indexes=["date"],
    ),
]


INDEX_COMPONENTS_SCHEMAS: List[TableSchema] = [
    TableSchema(
        name="index_weights",
        columns=[
            ("index_code", "VARCHAR NOT NULL"),
            ("stock_code", "VARCHAR NOT NULL"),
            ("weight", "DOUBLE"),
            ("update_date", "DATE"),
            ("update_time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ],
        primary_key=["index_code", "stock_code", "update_date"],
        indexes=["index_code", "stock_code"],
    ),
]


DEFAULT_POLICIES: List[CachePolicy] = [
    CachePolicy(domain="meta", ttl_hours=8760, max_memory_items=100),
    CachePolicy(domain="market", ttl_hours=0, max_memory_items=1000),
    CachePolicy(domain="option", ttl_hours=24, max_memory_items=500),
    CachePolicy(domain="conversion_bond", ttl_hours=24, max_memory_items=500),
    CachePolicy(domain="macro", ttl_hours=720, max_memory_items=200),
    CachePolicy(domain="share_change", ttl_hours=168, max_memory_items=500),
    CachePolicy(domain="unlock", ttl_hours=168, max_memory_items=500),
    CachePolicy(domain="index_components", ttl_hours=720, max_memory_items=200),
]


DOMAIN_DB_MAPPING = {
    "meta": {"db_path": "data/meta.db", "schemas": META_SCHEMAS},
    "market": {"db_path": "data/market.db", "schemas": MARKET_SCHEMAS},
    "option": {"db_path": "data/option.db", "schemas": OPTION_SCHEMAS},
    "conversion_bond": {
        "db_path": "data/conversion_bond.db",
        "schemas": CONVERSION_BOND_SCHEMAS,
    },
    "macro": {"db_path": "data/macro.db", "schemas": MACRO_SCHEMAS},
    "share_change": {
        "db_path": "data/share_change.db",
        "schemas": SHARE_CHANGE_SCHEMAS,
    },
    "unlock": {"db_path": "data/unlock.db", "schemas": UNLOCK_SCHEMAS},
    "index_components": {
        "db_path": "data/index_components.db",
        "schemas": INDEX_COMPONENTS_SCHEMAS,
    },
}


def init_default_cache() -> None:
    """初始化默认缓存配置"""
    from .unified_cache import UnifiedCacheManager
    import os

    cache = UnifiedCacheManager.get_instance()

    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    for domain, config in DOMAIN_DB_MAPPING.items():
        db_path = os.path.join(base_dir, config["db_path"])
        cache.register_db(domain, db_path, config["schemas"])

    for policy in DEFAULT_POLICIES:
        cache.register_policy(policy)

    logger.info("默认缓存配置初始化完成")


import logging

logger = logging.getLogger(__name__)
