# Parquet 缓存迁移完成说明

## 迁移状态

项目已完成从 DuckDB/`.db` 到 **Parquet 分区缓存**的迁移。新架构消除了多进程并发时的数据库锁冲突问题，同时保持查询性能。

## 新的数据存储方式

- **日线/分钟线数据**：按 `symbol/adjust/date.parquet` 分区存储于 `data/parquet_cache/`
- **元数据**：交易日历、证券列表等存储于 `data/cache/meta_cache/`
- **指数权重**：按日期分区的 parquet 文件存储于 `data/cache/index_cache/`
- **查询层**：通过 `ParquetAdapter` 或 `parquet_cache.CacheManager` 读取，内部使用 DuckDB 进行只读 SQL 查询

## 验证缓存数据

### 方式一：通过 CacheManager 查看摘要

```python
from jk2bt.db.cache_status import get_cache_manager

manager = get_cache_manager()
summary = manager.get_cache_summary()
print(f"股票: {summary['stock_count']} 只")
print(f"ETF: {summary['etf_count']} 只")
print(f"指数: {summary['index_count']} 只")
print(f"总记录: {summary['total_records']}")
```

### 方式二：通过 ParquetAdapter 查询单只股票

```python
from jk2bt.db.parquet_adapter import ParquetAdapter

db = ParquetAdapter(read_only=True)
df = db.query("stock_daily", where={"symbol": "600519.XSHG"})
print(f"记录数: {len(df)}")
print(df.head())
```

---

*遗留的 `.db` 相关历史文档已归档至 `docs/archive/legacy_db_docs/`。*
