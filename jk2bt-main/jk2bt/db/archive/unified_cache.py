"""
db/unified_cache.py
统一缓存管理器 - 提供单一入口管理所有缓存，消除各模块的重复 DBManager 实现。

架构:
    UnifiedCacheManager (统一入口)
        ├── SharedMemoryCache (共享内存缓存层)
        ├── CachePolicyRegistry (统一缓存策略)
        └── DuckDBAdapterRegistry (数据库适配器注册)

异常处理改进:
    - 使用自定义异常类 (CacheError, DatabaseError)
    - 捕获具体异常而非通用 Exception
    - 保留原始异常链 (raise ... from e)
    - 提供有意义的错误信息和上下文

使用方式:
    from jk2bt.db.unified_cache import UnifiedCacheManager

    # 获取单例
    cache = UnifiedCacheManager.get_instance()

    # 注册数据库
    cache.register_db('meta', 'data/meta.db', MetaSchema)
    cache.register_db('market', 'data/market.db', MarketSchema)

    # 统一查询接口
    df = cache.get('meta', 'trade_days')
    df = cache.get('market', 'stock_daily', symbol='sh600000', start='2020-01-01', end='2020-12-31')
"""

import os
import json
import logging
import threading
import time
from typing import Optional, Dict, Any, List, Tuple, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from contextlib import contextmanager
import pandas as pd

try:
    import duckdb
except ImportError:
    raise ImportError("请安装 duckdb: pip install duckdb")

logger = logging.getLogger(__name__)

# 导入自定义异常类
try:
    from jk2bt.core.exceptions import CacheError, DatabaseError, ValidationError
except ImportError:
    # 兼容无 exceptions 模块的情况
    class CacheError(Exception):
        """缓存错误"""
        def __init__(self, message: str, context: dict = None):
            self.message = message
            self.context = context or {}
            super().__init__(self.message)

    class DatabaseError(Exception):
        """数据库错误"""
        def __init__(self, message: str, context: dict = None):
            self.message = message
            self.context = context or {}
            super().__init__(self.message)

    class ValidationError(Exception):
        """数据验证错误"""
        pass

# 导入统一配置
try:
    from ..utils.config import get_config, CacheConfig
except ImportError:
    from jk2bt.utils.config import get_config, CacheConfig


@dataclass
class CachePolicy:
    """缓存策略配置"""

    domain: str
    ttl_hours: int = 24
    max_memory_items: int = 1000
    fallback_to_pickle: bool = False
    pickle_dir: str = ""

    @classmethod
    def from_config(cls, domain: str, config: CacheConfig = None) -> "CachePolicy":
        """从配置创建缓存策略"""
        if config is None:
            from jk2bt.utils.config import get_config
            config = get_config().cache
        return cls(
            domain=domain,
            ttl_hours=config.ttl_hours,
            max_memory_items=config.max_memory_items,
        )

    def is_valid(self, timestamp: float) -> bool:
        """检查缓存是否有效"""
        if self.ttl_hours <= 0:
            return True
        age_hours = (time.time() - timestamp) / 3600
        return age_hours < self.ttl_hours


@dataclass
class TableSchema:
    """表结构定义"""

    name: str
    columns: List[Tuple[str, str]]  # [(列名, 类型), ...]
    primary_key: List[str]
    indexes: List[str] = field(default_factory=list)

    def create_sql(self) -> str:
        """生成建表 SQL"""
        cols_def = ", ".join(f"{col} {typ}" for col, typ in self.columns)
        pk_def = ", ".join(self.primary_key)
        return f"CREATE TABLE IF NOT EXISTS {self.name} ({cols_def}, PRIMARY KEY ({pk_def}))"

    def index_sqls(self) -> List[str]:
        """生成索引 SQL"""
        return [
            f"CREATE INDEX IF NOT EXISTS idx_{self.name}_{col} ON {self.name}({col})"
            for col in self.indexes
        ]


class SharedMemoryCache:
    """共享内存缓存层 - 所有业务模块共用"""

    def __init__(self, max_items: int = None):
        # 使用配置中的 max_memory_items
        if max_items is None:
            config = get_config()
            max_items = config.cache.max_memory_items
        self._cache: Dict[str, pd.DataFrame] = {}
        self._timestamps: Dict[str, float] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._max_items = max_items

    def _make_key(self, domain: str, table: str, **conditions) -> str:
        """生成缓存 key"""
        parts = [domain, table]
        for k, v in sorted(conditions.items()):
            if v is not None:
                parts.append(f"{k}={v}")
        return ":".join(parts)

    def get(self, domain: str, table: str, **conditions) -> Optional[pd.DataFrame]:
        """获取缓存"""
        key = self._make_key(domain, table, **conditions)
        with self._lock:
            if key in self._cache:
                return self._cache[key].copy()
        return None

    def set(
        self,
        domain: str,
        table: str,
        df: pd.DataFrame,
        metadata: Dict = None,
        **conditions,
    ):
        """设置缓存"""
        key = self._make_key(domain, table, **conditions)
        with self._lock:
            if len(self._cache) >= self._max_items:
                self._evict_oldest()
            self._cache[key] = df.copy()
            self._timestamps[key] = time.time()
            if metadata:
                self._metadata[key] = metadata

    def get_timestamp(self, domain: str, table: str, **conditions) -> Optional[float]:
        """获取缓存时间戳"""
        key = self._make_key(domain, table, **conditions)
        with self._lock:
            return self._timestamps.get(key)

    def invalidate(self, domain: str = None, table: str = None, **conditions):
        """失效缓存"""
        with self._lock:
            keys_to_remove = []
            key_prefix = self._make_key(domain or "", table or "", **conditions)

            for key in self._cache:
                if key_prefix and not key.startswith(key_prefix):
                    continue
                if domain and not key.startswith(domain + ":"):
                    continue
                keys_to_remove.append(key)

            for key in keys_to_remove:
                self._cache.pop(key, None)
                self._timestamps.pop(key, None)
                self._metadata.pop(key, None)

    def clear(self):
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()
            self._metadata.clear()

    def _evict_oldest(self):
        """淘汰最旧的缓存"""
        if not self._timestamps:
            return
        oldest_key = min(self._timestamps, key=self._timestamps.get)
        self._cache.pop(oldest_key, None)
        self._timestamps.pop(oldest_key, None)
        self._metadata.pop(oldest_key, None)

    def stats(self) -> Dict:
        """缓存统计"""
        with self._lock:
            return {
                "total_items": len(self._cache),
                "max_items": self._max_items,
                "domains": list(set(k.split(":")[0] for k in self._cache.keys())),
            }


class DuckDBAdapter:
    """DuckDB 数据库适配器"""

    _WRITE_RETRY_COUNT = 3
    _WRITE_RETRY_DELAY = 0.5

    def __init__(
        self, db_path: str, schemas: List[TableSchema] = None, read_only: bool = False
    ):
        self.db_path = db_path
        self.read_only = read_only
        self._schemas: Dict[str, TableSchema] = {}
        self._initialized = False

        if schemas:
            for schema in schemas:
                self._schemas[schema.name] = schema

        if not read_only:
            os.makedirs(
                os.path.dirname(db_path) if os.path.dirname(db_path) else ".",
                exist_ok=True,
            )
            self._init_tables()

    @contextmanager
    def _get_connection(self, read_only: bool = None):
        """
        获取数据库连接

        异常处理:
        - duckdb.IOException: 数据库文件不存在或损坏
        - duckdb.ConnectionException: 连接失败
        - PermissionError: 文件权限问题

        Raises:
            DatabaseError: 数据库连接失败
        """
        if read_only is None:
            read_only = self.read_only

        conn = None
        try:
            conn = duckdb.connect(self.db_path, read_only=read_only)
            yield conn
        except PermissionError as e:
            logger.error(f"数据库文件权限错误: {self.db_path} - {e}")
            raise DatabaseError(
                f"数据库文件权限不足: {self.db_path}",
                context={"db_path": self.db_path, "error": str(e)}
            ) from e
        except duckdb.IOException as e:
            logger.error(f"数据库 IO 错误: {self.db_path} - {e}")
            raise DatabaseError(
                f"数据库 IO 错误: {self.db_path}",
                context={"db_path": self.db_path, "error": str(e)}
            ) from e
        except duckdb.ConnectionException as e:
            logger.error(f"数据库连接异常: {self.db_path} - {e}")
            raise DatabaseError(
                f"数据库连接失败: {self.db_path}",
                context={"db_path": self.db_path, "error": str(e)}
            ) from e
        except Exception as e:
            logger.error(f"数据库连接错误: {type(e).__name__}: {e}")
            raise DatabaseError(
                f"数据库连接未知错误",
                context={"db_path": self.db_path, "error_type": type(e).__name__, "error": str(e)}
            ) from e
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

    def _init_tables(self):
        """
        初始化表结构

        异常处理:
        - 创建表失败时记录日志但不抛出异常（允许后续重试）
        - 使用自定义异常类型记录具体错误
        """
        if self._initialized:
            return

        try:
            with self._get_connection(read_only=False) as conn:
                for schema in self._schemas.values():
                    try:
                        conn.execute(schema.create_sql())
                        for idx_sql in schema.index_sqls():
                            conn.execute(idx_sql)
                        # 迁移：添加缺失的列
                        self._migrate_table(conn, schema)
                    except duckdb.ParserException as e:
                        logger.warning(f"表 {schema.name} SQL 解析错误: {e}")
                    except duckdb.CatalogException as e:
                        logger.warning(f"表 {schema.name} 已存在或创建失败: {e}")
                self._initialized = True
                logger.info(f"数据库表初始化完成: {self.db_path}")
        except DatabaseError:
            # 已经是自定义异常，直接传递
            self._initialized = True  # 标记为已初始化，避免无限重试
        except Exception as e:
            logger.warning(f"初始化表结构失败: {type(e).__name__}: {e}")
            self._initialized = True

    def _migrate_table(self, conn, schema):
        """
        迁移表结构：添加缺失的列

        Args:
            conn: 数据库连接
            schema: 表结构定义
        """
        try:
            # 获取现有列
            result = conn.execute(f"DESCRIBE {schema.name}").fetchall()
            existing_columns = {row[0] for row in result}

            # 检查并添加缺失的列
            for col_name, col_type in schema.columns:
                if col_name not in existing_columns:
                    try:
                        conn.execute(f"ALTER TABLE {schema.name} ADD COLUMN {col_name} {col_type}")
                        logger.info(f"表 {schema.name} 添加列 {col_name}")
                    except Exception as e:
                        logger.warning(f"添加列 {col_name} 失败: {e}")
        except Exception as e:
            logger.warning(f"迁移表 {schema.name} 失败: {e}")

    def query(
        self,
        table: str,
        conditions: Dict = None,
        columns: List[str] = None,
        order_by: str = None,
    ) -> pd.DataFrame:
        """查询数据"""
        with self._get_connection(read_only=True) as conn:
            cols = "*" if not columns else ", ".join(columns)
            sql = f"SELECT {cols} FROM {table}"

            if conditions:
                where_clauses = []
                params = []
                for key, value in conditions.items():
                    if value is not None:
                        where_clauses.append(f"{key} = ?")
                        params.append(value)
                if where_clauses:
                    sql += " WHERE " + " AND ".join(where_clauses)

            if order_by:
                sql += f" ORDER BY {order_by}"

            return conn.execute(sql, params if conditions else []).fetchdf()

    def insert(self, table: str, df: pd.DataFrame, mode: str = "replace"):
        """插入数据

        Args:
            table: 表名
            df: 数据 DataFrame
            mode: 插入模式 - 'replace' (INSERT OR REPLACE), 'append' (INSERT)
        """
        if df is None or df.empty:
            logger.warning(f"{table}: 无数据需要插入")
            return

        # 过滤 DataFrame 列以匹配表结构
        if table in self._schemas:
            schema_columns = [col[0] for col in self._schemas[table].columns]
            # 只保留表结构中定义的列
            df_filtered = df[[col for col in schema_columns if col in df.columns]].copy()
            # 添加缺失的列（使用默认值）
            for col in schema_columns:
                if col not in df_filtered.columns:
                    if col == 'update_time':
                        df_filtered[col] = pd.Timestamp.now()
                    else:
                        df_filtered[col] = None
            # 按schema顺序排列列
            df_filtered = df_filtered[schema_columns]
        else:
            df_filtered = df

        # 构建列名列表
        columns = df_filtered.columns.tolist()
        columns_str = ", ".join(columns)

        def _do_insert():
            with self._get_connection(read_only=False) as conn:
                # 使用明确的列名进行插入
                conn.execute(f"CREATE TEMP TABLE _temp_insert AS SELECT * FROM df_filtered")
                if mode == "replace":
                    # DuckDB使用DELETE + INSERT实现UPSERT
                    pk_cols = self._schemas[table].primary_key if table in self._schemas else []
                    if pk_cols:
                        pk_str = ", ".join(pk_cols)
                        conn.execute(f"""
                            DELETE FROM {table} WHERE ({pk_str}) IN (SELECT {pk_str} FROM _temp_insert)
                        """)
                    conn.execute(f"INSERT INTO {table} ({columns_str}) SELECT {columns_str} FROM _temp_insert")
                else:
                    conn.execute(f"INSERT INTO {table} ({columns_str}) SELECT {columns_str} FROM _temp_insert")
                conn.execute("DROP TABLE IF EXISTS _temp_insert")
                logger.info(f"{table}: 插入 {len(df_filtered)} 条数据")

        self._retry_write(_do_insert)

    def _retry_write(self, func: Callable, *args, **kwargs):
        """写入重试机制"""
        last_error = None
        for attempt in range(self._WRITE_RETRY_COUNT):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                if "lock" in error_str or "conflict" in error_str:
                    logger.warning(
                        f"写入冲突，重试 {attempt + 1}/{self._WRITE_RETRY_COUNT}"
                    )
                    time.sleep(self._WRITE_RETRY_DELAY * (attempt + 1))
                else:
                    raise
        raise last_error

    def has_data(self, table: str, conditions: Dict = None) -> bool:
        """检查是否有数据"""
        with self._get_connection(read_only=True) as conn:
            sql = f"SELECT COUNT(*) FROM {table}"
            if conditions:
                where_clauses = []
                params = []
                for key, value in conditions.items():
                    if value is not None:
                        where_clauses.append(f"{key} = ?")
                        params.append(value)
                if where_clauses:
                    sql += " WHERE " + " AND ".join(where_clauses)

            count = conn.execute(sql, params if conditions else []).fetchone()[0]
            return count > 0

    def get_date_range(
        self, table: str, date_col: str = "datetime", conditions: Dict = None
    ) -> Tuple[Optional[datetime], Optional[datetime]]:
        """获取数据日期范围"""
        with self._get_connection(read_only=True) as conn:
            sql = f"SELECT MIN({date_col}), MAX({date_col}) FROM {table}"
            if conditions:
                where_clauses = []
                params = []
                for key, value in conditions.items():
                    if value is not None:
                        where_clauses.append(f"{key} = ?")
                        params.append(value)
                if where_clauses:
                    sql += " WHERE " + " AND ".join(where_clauses)

            result = conn.execute(sql, params if conditions else []).fetchone()
            if result[0] is None:
                return None, None
            return pd.to_datetime(result[0]), pd.to_datetime(result[1])

    def count(self, table: str, conditions: Dict = None) -> int:
        """统计记录数"""
        with self._get_connection(read_only=True) as conn:
            sql = f"SELECT COUNT(*) FROM {table}"
            if conditions:
                where_clauses = []
                params = []
                for key, value in conditions.items():
                    if value is not None:
                        where_clauses.append(f"{key} = ?")
                        params.append(value)
                if where_clauses:
                    sql += " WHERE " + " AND ".join(where_clauses)
            return conn.execute(sql, params if conditions else []).fetchone()[0]

    def delete(self, table: str, conditions: Dict = None):
        """删除数据"""
        with self._get_connection(read_only=False) as conn:
            sql = f"DELETE FROM {table}"
            if conditions:
                where_clauses = []
                params = []
                for key, value in conditions.items():
                    if value is not None:
                        where_clauses.append(f"{key} = ?")
                        params.append(value)
                if where_clauses:
                    sql += " WHERE " + " AND ".join(where_clauses)
            conn.execute(sql, params if conditions else [])
            logger.warning(f"已删除 {table} 中符合条件的数据")

    def register_schema(self, schema: TableSchema):
        """注册表结构"""
        self._schemas[schema.name] = schema
        if not self.read_only:
            with self._get_connection(read_only=False) as conn:
                conn.execute(schema.create_sql())
                for idx_sql in schema.index_sqls():
                    conn.execute(idx_sql)


class UnifiedCacheManager:
    """统一缓存管理器 - 单例模式"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        # 从配置获取缓存参数
        config = get_config()
        cache_config = config.cache

        self._memory_cache = SharedMemoryCache(max_items=cache_config.max_memory_items)
        self._db_adapters: Dict[str, DuckDBAdapter] = {}
        self._policies: Dict[str, CachePolicy] = {}
        # 使用配置中的 ttl_hours
        self._default_policy = CachePolicy(
            domain="default",
            ttl_hours=cache_config.ttl_hours
        )

    @classmethod
    def get_instance(cls) -> "UnifiedCacheManager":
        """获取单例实例"""
        return cls()

    @classmethod
    def reset_instance(cls):
        """重置单例（用于测试）"""
        with cls._lock:
            cls._instance = None

    def register_db(
        self,
        domain: str,
        db_path: str,
        schemas: List[TableSchema] = None,
        read_only: bool = False,
    ):
        """注册数据库适配器"""
        if domain in self._db_adapters:
            logger.warning(f"数据库 {domain} 已注册，将替换")

        self._db_adapters[domain] = DuckDBAdapter(db_path, schemas, read_only)
        logger.info(f"注册数据库: {domain} -> {db_path}")

    def register_policy(self, policy: CachePolicy):
        """注册缓存策略"""
        self._policies[policy.domain] = policy

    def get_policy(self, domain: str) -> CachePolicy:
        """获取缓存策略"""
        return self._policies.get(domain, self._default_policy)

    def get(
        self, domain: str, table: str, use_cache: bool = True, **conditions
    ) -> pd.DataFrame:
        """统一查询接口

        Args:
            domain: 业务域 (如 'market', 'meta', 'option')
            table: 表名 (如 'stock_daily', 'trade_days')
            use_cache: 是否使用内存缓存
            **conditions: 查询条件

        Returns:
            DataFrame 查询结果
        """
        if use_cache:
            cached = self._memory_cache.get(domain, table, **conditions)
            if cached is not None:
                policy = self.get_policy(domain)
                timestamp = self._memory_cache.get_timestamp(
                    domain, table, **conditions
                )
                if timestamp and policy.is_valid(timestamp):
                    logger.debug(f"[{domain}:{table}] 使用内存缓存")
                    return cached

        adapter = self._db_adapters.get(domain)
        if adapter is None:
            logger.error(f"数据库 {domain} 未注册")
            return pd.DataFrame()

        df = adapter.query(table, conditions)

        if use_cache and not df.empty:
            self._memory_cache.set(domain, table, df, **conditions)

        return df

    def set(self, domain: str, table: str, df: pd.DataFrame, **conditions):
        """写入数据"""
        adapter = self._db_adapters.get(domain)
        if adapter is None:
            logger.error(f"数据库 {domain} 未注册")
            return

        adapter.insert(table, df)
        self._memory_cache.invalidate(domain, table, **conditions)

    def has_data(self, domain: str, table: str, **conditions) -> bool:
        """检查是否有数据"""
        adapter = self._db_adapters.get(domain)
        if adapter is None:
            return False
        return adapter.has_data(table, conditions)

    def get_date_range(
        self, domain: str, table: str, date_col: str = "datetime", **conditions
    ) -> Tuple[Optional[datetime], Optional[datetime]]:
        """获取数据日期范围"""
        adapter = self._db_adapters.get(domain)
        if adapter is None:
            return None, None
        return adapter.get_date_range(table, date_col, conditions)

    def invalidate(self, domain: str = None, table: str = None, **conditions):
        """失效缓存"""
        self._memory_cache.invalidate(domain, table, **conditions)

    def clear_cache(self):
        """清空所有内存缓存"""
        self._memory_cache.clear()

    def stats(self) -> Dict:
        """缓存统计"""
        return {
            "memory_cache": self._memory_cache.stats(),
            "registered_domains": list(self._db_adapters.keys()),
            "policies": {d: p.ttl_hours for d, p in self._policies.items()},
        }

    def get_adapter(self, domain: str) -> Optional[DuckDBAdapter]:
        """获取数据库适配器"""
        return self._db_adapters.get(domain)


def get_unified_cache() -> UnifiedCacheManager:
    """获取统一缓存管理器单例"""
    return UnifiedCacheManager.get_instance()


def clear_unified_cache():
    """清空统一缓存"""
    UnifiedCacheManager.get_instance().clear_cache()


def reset_unified_cache():
    """重置统一缓存管理器（用于测试）"""
    UnifiedCacheManager.reset_instance()
