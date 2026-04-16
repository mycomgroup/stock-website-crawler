# Parquet Cache 模块接口契约

所有子 agent 基于此契约并行开发，互不依赖。

## 包结构

```
parquet_cache/
├── __init__.py
├── config.py            # Agent 1
├── table_registry.py    # Agent 2
├── schema_validator.py  # Agent 3
├── writer.py            # Agent 4
├── partition_manager.py # Agent 5
├── query_engine.py      # Agent 6
├── memory_cache.py      # Agent 7
├── cache_manager.py     # Agent 8
├── aggregator.py        # Agent 9
└── tests/
    ├── test_writer.py
    ├── test_query_engine.py
    ├── test_memory_cache.py
    ├── test_cache_manager.py
    ├── test_aggregator.py
    └── test_integration.py
```

## 核心数据结构

### CacheTable

```python
@dataclass
class CacheTable:
    name: str                    # 表名，如 "stock_daily"
    partition_by: str | None     # 分区键，如 "date" / "report_date" / "week"，None 表示单文件
    ttl_hours: int               # 过期时间（0 = 永不过期）
    schema: dict[str, str]       # 字段 → 类型映射，如 {"symbol": "string", "date": "date32[ms]"}
    primary_key: list[str]       # 唯一键，如 ["symbol", "date"]
    aggregation_enabled: bool    # 是否启用聚合层
    compaction_threshold: int    # 触发聚合的文件数阈值
    priority: str                # "P0" / "P1" / "P2" / "P3"
    storage_layer: str           # "daily" / "minute" / "meta" / "snapshot"
```

### 路径约定

```
base_dir/
├── {storage_layer}/{table_name}/         # 原始层
│   └── {partition_key}={value}/          # 分区目录（partition_by 为 None 时无此层）
│       └── part_{pid}_{uuid8}.parquet    # 数据文件
├── aggregated/{storage_layer}/{table_name}/  # 聚合层
│   └── {partition_key}={value}.parquet
└── _locks/                               # 锁目录
    └── {table_name}.lock
```

### CacheManager 公共接口

```python
class CacheManager:
    def __init__(self, base_dir: str, config: CacheConfig | None = None)

    def get(
        self,
        table: str,
        where: dict[str, Any] | None = None,
        columns: list[str] | None = None,
        order_by: list[str] | None = None,
        limit: int | None = None,
    ) -> pd.DataFrame | None:
        """查询缓存，未命中返回 None"""

    def put(
        self,
        table: str,
        data: pd.DataFrame,
        partition_value: str | None = None,
    ) -> str:
        """写入缓存，返回文件路径"""

    def invalidate(
        self,
        table: str,
        where: dict[str, Any] | None = None,
    ) -> int:
        """使缓存过期，返回删除的文件数"""

    def exists(
        self,
        table: str,
        where: dict[str, Any] | None = None,
    ) -> bool:
        """检查缓存是否存在"""

    def table_info(self, table: str) -> TableInfo:
        """获取表信息（文件数、大小、最后更新时间等）"""
```

### Writer 接口

```python
class AtomicWriter:
    def __init__(self, base_dir: Path)

    def write(
        self,
        data: pd.DataFrame,
        target_path: Path,
        schema: dict[str, str] | None = None,
        compression: str = "snappy",
        row_group_size: int = 100_000,
    ) -> Path:
        """原子写入，返回实际写入路径"""
```

### QueryEngine 接口

```python
class QueryEngine:
    def __init__(self, base_dir: Path)

    def query(
        self,
        paths: list[Path],
        where: dict[str, Any] | None = None,
        columns: list[str] | None = None,
        order_by: list[str] | None = None,
        limit: int | None = None,
    ) -> pd.DataFrame:
        """DuckDB 只读查询"""
```

### MemoryCache 接口

```python
class MemoryCache:
    def __init__(self, max_items: int = 5000, default_ttl_seconds: int = 3600)

    def get(self, key: str) -> pd.DataFrame | None:
    def put(self, key: str, value: pd.DataFrame, ttl_seconds: int | None = None) -> None:
    def invalidate(self, key: str | None = None) -> int:
    def has(self, key: str) -> bool:
```

### Aggregator 接口

```python
class Aggregator:
    def __init__(self, base_dir: Path, lock_dir: Path | None = None)

    def aggregate_table(
        self,
        table: str,
        storage_layer: str,
        partition_by: str | None,
        threshold: int = 20,
    ) -> int:
        """聚合指定表，返回聚合的分区数"""

    def aggregate_all(
        self,
        tables: dict[str, CacheTable],
    ) -> dict[str, int]:
        """聚合所有需要聚合的表"""

    def cleanup(
        self,
        retention_hours: int = 24,
    ) -> int:
        """清理过期原始文件，返回删除文件数"""
```

## 依赖关系

```
config.py ──────────────────────────────────────→ 所有模块
table_registry.py ──────────────────────────────→ cache_manager.py, aggregator.py
schema_validator.py ────────────────────────────→ writer.py
writer.py ──────────────────────────────────────→ cache_manager.py
partition_manager.py ───────────────────────────→ writer.py, query_engine.py, aggregator.py
query_engine.py ────────────────────────────────→ cache_manager.py, aggregator.py
memory_cache.py ────────────────────────────────→ cache_manager.py
cache_manager.py ───────────────────────────────→ 对外入口
aggregator.py ──────────────────────────────────→ 独立任务 / CLI
```

## 并行开发分组

| 组 | Agent | 模块 | 依赖 |
|----|-------|------|------|
| A | 1 | config.py | 无 |
| B | 2 | table_registry.py | config.py |
| C | 3 | schema_validator.py | 无 |
| D | 4 | writer.py | schema_validator.py |
| E | 5 | partition_manager.py | config.py |
| F | 6 | query_engine.py | partition_manager.py |
| G | 7 | memory_cache.py | 无 |
| H | 8 | cache_manager.py | writer + query_engine + memory_cache + partition_manager + table_registry |
| I | 9 | aggregator.py | query_engine + writer + partition_manager |
| J | 10 | tests/ | 所有模块 |

Agent 8 和 9 需要等 3-7 完成后再开发。Agent 10 最后集成。
