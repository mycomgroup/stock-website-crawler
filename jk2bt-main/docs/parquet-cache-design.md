# 多进程并发缓存技术方案：Parquet 分区 + DuckDB 只读查询

## 1. 背景与问题

### 1.1 现状

JK2BT 回测框架采用多进程并发执行回测任务。当前缓存体系存在以下问题：

- **DuckDB 原生格式不支持多进程并发写入**，同一时刻只能一个进程以读写模式打开 `.db` 文件
- 回测进程 + 例行数据补充程序同时运行时，写入冲突导致重试排队，进程越多等待越久
- Pickle 文件缓存散落 126+ 处调用，无统一治理，存在安全风险和一致性隐患
- 缓存过期策略不统一，缺乏自动清理机制
- 仅 3/100+ 个 akshare 接口实现了缓存，大量接口反复请求网络

### 1.2 核心诉求

| 诉求 | 说明 |
|------|------|
| 多进程并发写入 | 每个回测进程发现缺数据时可自行填充缓存，互不阻塞 |
| 无中心化服务 | 不引入额外的数据同步进程，避免单点故障和额外复杂度 |
| 读写并发安全 | 写入进程和读取进程互不影响 |
| 查询性能 | 保持或优于当前 DuckDB 的查询能力 |
| 渐进式迁移 | 新方案独立实现，不破坏现有代码 |
| 接口级缓存抽象 | 以 akshare 接口为缓存单元，而非底层存储格式 |

### 1.3 接口特征分析

基于 `docs/akshare_interface_analysis.md`，100+ 个 akshare 接口按数据特征分为 5 类：

| 类别 | 数量 | 缓存策略 | 更新频率 |
|------|------|---------|---------|
| 1. 实时数据 | 12 | 不缓存 | 盘中实时 |
| 2. 低频静态数据 | ~64 | 可选缓存（TTL 长） | 季度/年度/不定期 |
| 3. 低频高价值数据 | ~87 | **必须缓存** | 日/周/月 |
| 4. 大数据量预存 | ~30 | **批量预存 + 增量更新** | 每日收盘后 |
| 5. 分钟级高频 | 5 | 缓存（按周/月分段） | 每日 240 条/股 |

---

## 2. 总体架构

```
┌──────────────────────────────────────────────────────────────────────┐
│                            回测进程 / 数据补充进程                      │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                    CacheManager（统一入口）                    │     │
│  │                                                              │     │
│  │  get(table, **conditions)  →  查内存 → 查 Parquet → 查 DB   │     │
│  │  put(table, df, **conditions)  →  写 Parquet                │     │
│  │  invalidate(table, **conditions)  →  标记过期                │     │
│  └──────────────────────┬──────────────────────────────────────┘     │
│                         │                                             │
│         ┌───────────────┼───────────────┐                            │
│         ▼               ▼               ▼                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                     │
│  │ 内存缓存层  │  │ Parquet层   │  │ 聚合任务层  │                     │
│  │ (LRU/TTL)  │  │ (分区文件)  │  │ (Compaction│                     │
│  └────────────┘  └──────┬─────┘  │  + 预聚合)  │                     │
│                         │        └──────┬─────┘                     │
│                         │               │                            │
└─────────────────────────┼───────────────┼────────────────────────────┘
                          │               │
┌─────────────────────────▼───────────────▼────────────────────────────┐
│                         存储层                                        │
│                                                                      │
│  data/cache/                                                         │
│  ├── daily/              ← 日频数据（日线、估值、资金流等）             │
│  │   ├── stock_daily/    ← 按接口分目录                                │
│  │   ├── etf_daily/                                                  │
│  │   ├── index_daily/                                                │
│  │   ├── valuation/                                                  │
│  │   └── money_flow/                                                 │
│  ├── minute/             ← 分钟级数据                                  │
│  │   ├── stock_minute/                                               │
│  │   └── etf_minute/                                                 │
│  ├── meta/               ← 低频静态数据                                │
│  │   ├── securities/     ← 证券列表、交易日历                          │
│  │   ├── industry/       ← 行业/概念/指数成分                          │
│  │   └── company/        ← 公司信息、财务指标                          │
│  ├── snapshot/           ← 每日快照（全市场批量数据）                    │
│  │   ├── spot/           ← 每日收盘行情快照                            │
│  │   ├── fund_flow/      ← 资金流向排名                                │
│  │   └── hsgt/           ← 北向资金持股                                │
│  └── aggregated/         ← 聚合层（预计算结果）                         │
│      ├── stock_daily_merged/   ← 多进程写入合并后的日线                  │
│      └── snapshot_merged/      ← 合并后的快照数据                       │
│                                                                      │
└─────────────────────────┬────────────────────────────────────────────┘
                          │
┌─────────────────────────▼────────────────────────────────────────────┐
│                      查询层：DuckDB 只读                               │
│                                                                      │
│  duckdb.sql("SELECT * FROM 'data/cache/daily/stock_daily/**/*.parquet' │
│              WHERE symbol = '600519' AND date >= '2024-01-01'")       │
│                                                                      │
│  • Filter pushdown：只读取匹配分区和文件                                │
│  • Projection pushdown：只读取需要的列                                 │
│  • 多进程只读无限制                                                   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. 目录结构设计

### 3.1 设计原则

| 原则 | 说明 |
|------|------|
| **按接口分目录** | 每个 akshare 接口对应一个缓存目录，独立管理 |
| **按更新频率分层** | daily / minute / meta / snapshot 四层，不同生命周期 |
| **聚合层独立** | 多进程写入的碎片文件通过聚合任务合并，查询优先读聚合层 |
| **分区键灵活** | 不同接口使用不同分区键（date / symbol / report_date 等） |

### 3.2 目录结构

```
data/cache/
│
├── daily/                          # 日频数据，按天更新
│   ├── stock_daily/                # 股票日线
│   │   ├── date=2024-04-01/
│   │   │   ├── part_1001_a1b2c3d4.parquet
│   │   │   └── part_1002_e5f6g7h8.parquet
│   │   ├── date=2024-04-02/
│   │   │   └── part_1001_m3n4o5p6.parquet
│   │   └── ...
│   │
│   ├── etf_daily/                  # ETF 日线
│   ├── index_daily/                # 指数日线
│   ├── futures_daily/              # 期货日线
│   ├── conversion_bond/            # 可转债日线
│   ├── valuation/                  # 估值数据（按报告日分区）
│   │   ├── report_date=2024-Q1/
│   │   └── report_date=2024-Q2/
│   ├── money_flow/                 # 资金流向
│   ├── north_flow/                 # 北向资金流
│   ├── holder/                     # 股东数据（按报告期分区）
│   │   ├── report_date=2024-Q1/
│   │   └── report_date=2024-Q2/
│   ├── dividend/                   # 分红数据
│   ├── unlock/                     # 解禁数据
│   └── margin/                     # 融资融券
│
├── minute/                         # 分钟级数据
│   ├── stock_minute/               # 股票分钟线
│   │   ├── week=2024-W14/          # 按周分区（数据量大）
│   │   └── week=2024-W15/
│   ├── etf_minute/
│   └── call_auction/               # 集合竞价
│
├── meta/                           # 低频静态数据（整个文件即可）
│   ├── securities.parquet          # 证券列表
│   ├── trade_calendar.parquet      # 交易日历
│   ├── industry_list.parquet       # 行业板块列表
│   ├── concept_list.parquet        # 概念板块列表
│   ├── index_info.parquet          # 指数信息
│   └── company_info.parquet        # 公司基本信息
│
├── snapshot/                       # 每日收盘后批量快照
│   ├── date=2024-04-01/
│   │   ├── spot.parquet            # 全市场行情快照
│   │   ├── fund_flow_rank.parquet  # 资金流向排名
│   │   ├── sector_flow.parquet     # 板块资金流向
│   │   ├── hsgt_hold.parquet       # 北向资金持股
│   │   ├── billboard.parquet       # 龙虎榜
│   │   └── st_status.parquet       # ST 状态
│   ├── date=2024-04-02/
│   └── ...
│
└── aggregated/                     # 聚合层（例行任务产出）
    ├── daily/
    │   ├── stock_daily/
    │   │   ├── date=2024-04-01.parquet    # 合并后的单文件
    │   │   ├── date=2024-04-02.parquet
    │   │   └── ...
    │   ├── etf_daily/
    │   └── index_daily/
    └── snapshot/
        ├── date=2024-04-01.parquet        # 合并后的快照
        └── ...
```

### 3.3 分区策略

| 数据类型 | 分区键 | 分区粒度 | 理由 |
|---------|--------|---------|------|
| 日线行情 | `date` | 天 | 查询通常按日期范围 |
| 分钟线 | `week` | 周 | 数据量大，按天分区文件太多 |
| 估值/财务 | `report_date` | 季度 | 按报告期更新 |
| 股东/分红 | `report_date` | 季度 | 按报告期更新 |
| 快照数据 | `date` | 天 | 每日批量生成 |
| 静态元数据 | 无分区 | 单文件 | 数据量小，整个文件即可 |

---

## 4. 接口级缓存抽象

### 4.1 缓存接口定义

以 akshare 接口为缓存单元，每个接口注册为一个 `CacheTable`：

```python
@dataclass
class CacheTable:
    name: str                    # 缓存表名，如 "stock_daily"
    partition_by: str            # 分区键，如 "date" / "report_date" / "week"
    ttl_hours: int               # 过期时间（0 = 永不过期）
    schema: dict                 # 字段类型定义
    primary_key: list[str]       # 唯一键，用于去重
    aggregation_enabled: bool    # 是否启用聚合层
    compaction_threshold: int    # 触发 compaction 的文件数阈值
    priority: str                # P0 / P1 / P2 / P3
```

### 4.2 接口注册表

```python
CACHE_TABLES = {
    # P0 - 日线行情类
    "stock_daily": CacheTable(
        name="stock_daily",
        partition_by="date",
        ttl_hours=0,
        schema={"symbol": "string", "date": "date", "open": "float64", ...},
        primary_key=["symbol", "date", "adjust"],
        aggregation_enabled=True,
        compaction_threshold=20,
        priority="P0",
    ),
    "etf_daily": CacheTable(...),
    "index_daily": CacheTable(...),
    "futures_daily": CacheTable(...),
    "conversion_bond_daily": CacheTable(...),

    # P0 - 指数成分/权重类
    "index_components": CacheTable(
        name="index_components",
        partition_by="date",
        ttl_hours=720,  # 30 天
        schema={"index_code": "string", "date": "date", "symbol": "string", "weight": "float64"},
        primary_key=["index_code", "date", "symbol"],
        aggregation_enabled=True,
        compaction_threshold=10,
        priority="P0",
    ),

    # P0 - 财务数据类
    "finance_indicator": CacheTable(
        name="finance_indicator",
        partition_by="report_date",
        ttl_hours=2160,  # 90 天
        schema={"symbol": "string", "report_date": "date", ...},
        primary_key=["symbol", "report_date"],
        aggregation_enabled=False,  # 按季度分区，不需要聚合
        compaction_threshold=5,
        priority="P0",
    ),

    # P1 - 资金流向类
    "money_flow": CacheTable(...),
    "north_money_flow": CacheTable(...),

    # P1 - 行业/概念类
    "industry_components": CacheTable(...),
    "concept_components": CacheTable(...),
    "industry_mapping": CacheTable(
        name="industry_mapping",
        partition_by=None,  # 单文件，无分区
        ttl_hours=720,
        schema={"symbol": "string", "industry": "string", ...},
        primary_key=["symbol"],
        aggregation_enabled=False,
        compaction_threshold=0,
        priority="P1",
    ),

    # 快照类
    "spot_snapshot": CacheTable(
        name="spot_snapshot",
        partition_by="date",
        ttl_hours=168,  # 7 天
        schema={"symbol": "string", "date": "date", "price": "float64", ...},
        primary_key=["symbol", "date"],
        aggregation_enabled=True,
        compaction_threshold=1,  # 每天只有一个文件，超过即需聚合
        priority="P0",
    ),
    "fund_flow_rank_snapshot": CacheTable(...),
    "sector_flow_snapshot": CacheTable(...),
    "hsgt_hold_snapshot": CacheTable(...),

    # 静态元数据
    "securities": CacheTable(
        name="securities",
        partition_by=None,
        ttl_hours=0,
        schema={"symbol": "string", "name": "string", "type": "string", ...},
        primary_key=["symbol"],
        aggregation_enabled=False,
        compaction_threshold=0,
        priority="P2",
    ),
    "trade_calendar": CacheTable(...),
}
```

### 4.3 缓存操作流程

```python
# 写入（回测进程发现缺数据时）
cache.put(
    table="stock_daily",
    data=df,                          # DataFrame
    partition_value="2024-04-01",     # 分区值
)

# 读取
df = cache.get(
    table="stock_daily",
    where={"symbol": "600519", "date": ("2024-04-01", "2024-04-30")},
    columns=["date", "open", "high", "low", "close", "volume"],
)

# 读取流程：
# 1. 查内存缓存（LRU + TTL）
# 2. 未命中 → 查聚合层（aggregated/daily/stock_daily/date=*.parquet）
# 3. 未命中 → 查原始层（daily/stock_daily/date=*/*.parquet）
# 4. 未命中 → 返回 None，调用方决定是否调用 akshare
```

---

## 5. 写入流程

### 5.1 单次写入

```
1. 根据 table 名获取 CacheTable 配置
2. 确定分区目录（如 daily/stock_daily/date=2024-04-01/）
3. 创建分区目录（如不存在）
4. 检查分区文件数，超过阈值则标记待聚合
5. Schema 校验（字段类型、主键完整性）
6. 生成唯一文件名：part_{pid}_{uuid8}.parquet
7. 写入临时文件：part_{pid}_{uuid8}.parquet.tmp
8. 原子重命名：os.replace(tmp, target)
9. 写入内存缓存
10. 返回成功
```

### 5.2 原子写入保证

```python
def atomic_write(df: pd.DataFrame, target_path: Path, schema: dict):
    # 1. Schema 校验
    validate_schema(df, schema)

    # 2. 写入临时文件
    tmp_path = target_path.with_suffix(".parquet.tmp")
    df.to_parquet(tmp_path, compression="snappy", row_group_size=100_000)

    # 3. 原子重命名
    os.replace(tmp_path, target_path)
```

**安全保障：**

| 异常场景 | 结果 |
|---------|------|
| 写入中途进程崩溃 | `.tmp` 文件残留，不影响查询 |
| 两个进程同时写入同分区 | 各自写不同文件，互不干扰 |
| 磁盘满 | `.tmp` 写入失败，不产生脏 `.parquet` |
| Schema 不匹配 | 拒绝写入，抛出异常 |

---

## 6. 聚合层与例行任务

### 6.1 为什么需要聚合层

多进程写入产生碎片文件，查询时需要扫描多个小文件。聚合层将碎片合并为单文件，提升查询性能。

| 场景 | 碎片文件数 | 查询延迟 | 聚合后 |
|------|-----------|---------|--------|
| 10 进程写同一天日线 | 10 个 part_*.parquet | +30% | 1 个 merged.parquet |
| 每日快照 | 1 个（但多个进程可能重复写） | 基准 | 去重后 1 个 |
| 分钟线（一周） | 50+ 个 part_*.parquet | +200% | 5-10 个 merged.parquet |

### 6.2 聚合任务设计

```
┌─────────────────────────────────────────────────────┐
│                AggregationTask（例行任务）            │
│                                                     │
│  触发方式：                                           │
│  1. 写入时检查：分区文件数 > threshold → 标记          │
│  2. 定时触发：每日凌晨执行全量聚合                     │
│  3. 手动触发：CLI 命令                                │
│                                                     │
│  执行流程：                                           │
│  1. 获取聚合锁（文件锁，防止多进程同时聚合）             │
│  2. 扫描需要聚合的分区                                │
│  3. 对每个分区：                                      │
│     a. 读取所有 part_*.parquet                        │
│     b. 按 primary_key 去重（INSERT OR REPLACE 语义）   │
│     c. 写入 aggregated/ 目录：date=YYYY-MM-DD.parquet │
│     d. 原子重命名                                     │
│     e. 标记原始文件为可删除                            │
│  4. 延迟删除原始文件（保留 24 小时，避免查询中断）       │
│  5. 释放聚合锁                                        │
└─────────────────────────────────────────────────────┘
```

### 6.3 聚合任务调度

```python
# 每日凌晨 2:00 执行（通过 cron 或 APScheduler）
AGGREGATION_SCHEDULE = {
    "daily_aggregation": {
        "cron": "0 2 * * *",
        "tables": ["stock_daily", "etf_daily", "index_daily", "futures_daily"],
        "mode": "merge",  # 合并同一天所有 part 文件
    },
    "snapshot_aggregation": {
        "cron": "0 16 * * 1-5",  # 工作日 16:00（收盘后）
        "tables": ["spot_snapshot", "fund_flow_rank_snapshot", "sector_flow_snapshot"],
        "mode": "dedup",  # 去重（可能有重复写入）
    },
    "minute_aggregation": {
        "cron": "0 3 * * 0",  # 每周日凌晨 3:00
        "tables": ["stock_minute", "etf_minute"],
        "mode": "compact",  # 压缩（合并周内文件）
    },
    "cleanup": {
        "cron": "0 4 * * *",  # 每天凌晨 4:00
        "action": "remove_old_files",
        "retention_hours": 24,  # 原始文件保留 24 小时
    },
}
```

### 6.4 聚合并发安全

```
data/cache/_locks/
├── aggregation.lock      # 聚合任务锁
└── compaction.lock       # Compaction 锁
```

- 使用 `filelock` 库（跨平台兼容 fcntl / msvcrt）
- 获取锁失败 → 跳过（其他进程正在执行）
- 聚合过程中新写入的 `part_*.parquet` 不受影响
- 查询优先读聚合层，聚合层不存在再回退到原始层

### 6.5 查询路径

```
cache.get(table, where)
    │
    ├── 1. 内存缓存命中 → 返回
    │
    ├── 2. 聚合层查询
    │   duckdb.sql("SELECT ... FROM 'aggregated/daily/{table}/*.parquet' WHERE ...")
    │   │
    │   └── 命中 → 写入内存缓存 → 返回
    │
    ├── 3. 原始层查询
    │   duckdb.sql("SELECT ... FROM 'daily/{table}/**/*.parquet' WHERE ...")
    │   │
    │   └── 命中 → 写入内存缓存 → 返回
    │
    └── 4. 未命中 → 返回 None
        │
        └── 调用方决定是否：
            a. 调用 akshare 获取数据
            b. cache.put() 写入缓存
            c. 返回空 DataFrame
```

---

## 7. 不同接口的存储策略

### 7.1 按数据特征分类存储

| 类别 | 存储路径 | 分区策略 | 聚合策略 | 示例接口 |
|------|---------|---------|---------|---------|
| **日线行情** | `daily/stock_daily/` | 按天 | 合并同一天所有 part | `get_daily_data`, `get_etf_daily`, `get_index_daily` |
| **分钟线** | `minute/stock_minute/` | 按周 | 周末压缩 | `get_minute_data`, `get_stock_minute_raw` |
| **财务/估值** | `daily/valuation/` | 按季度 | 不需要（文件少） | `get_finance_indicator`, `get_stock_valuation` |
| **股东/分红** | `daily/holder/` | 按季度 | 不需要 | `get_top10_holders`, `get_dividend` |
| **行业/概念成分** | `daily/industry_components/` | 按天 | 合并 | `get_index_components`, `get_industry_components` |
| **静态元数据** | `meta/*.parquet` | 单文件 | 不需要 | `get_securities_list`, `get_trade_dates` |
| **每日快照** | `snapshot/date=YYYY-MM-DD/` | 按天 | 去重合并 | `get_spot_em`, `get_sector_money_flow` |
| **实时数据** | 不缓存 | - | - | `get_spot_em`（盘中） |

### 7.2 非日频接口的特殊处理

| 接口类型 | 分区键 | 说明 |
|---------|--------|------|
| 财务数据 | `report_date`（季度） | 按报告期分区，如 `report_date=2024-Q1/` |
| 股东数据 | `report_date`（季度） | 同上 |
| 分红解禁 | `announce_date`（不定） | 按公告日分区 |
| 宏观数据 | `indicator` + `date` | 按指标名 + 日期分区 |
| 行业映射 | 无分区 | 单文件，整个替换 |

### 7.3 接口与缓存表映射

```python
# akshare 接口 → 缓存表的映射关系
INTERFACE_TO_CACHE = {
    # 日线行情
    "get_daily_data": "stock_daily",
    "get_etf_daily": "etf_daily",
    "get_index_daily": "index_daily",
    "get_futures_daily": "futures_daily",
    "get_conversion_bond_daily": "conversion_bond_daily",

    # 分钟线
    "get_minute_data": "stock_minute",
    "get_stock_minute_raw": "stock_minute",
    "get_etf_minute_raw": "etf_minute",

    # 财务/估值
    "get_finance_indicator": "finance_indicator",
    "get_financial_report": "financial_report",
    "get_stock_valuation": "valuation",
    "get_stock_pe_pb": "valuation",

    # 指数成分
    "get_index_components": "index_components",
    "get_index_stocks": "index_components",
    "get_industry_components": "industry_components",
    "get_concept_components": "concept_components",

    # 股东/分红
    "get_top10_holders": "holder",
    "get_dividend": "dividend",
    "get_unlock_summary": "unlock",

    # 资金流
    "get_money_flow": "money_flow",
    "get_north_money_flow": "north_flow",

    # 快照
    "get_spot_em": "spot_snapshot",
    "get_sector_money_flow": "sector_flow_snapshot",
    "get_hsgt_hold_stock": "hsgt_hold_snapshot",
    "get_billboard_list": "billboard_snapshot",

    # 静态元数据
    "get_securities_list": "securities",
    "get_trade_dates": "trade_calendar",
    "get_industry_list": "industry_list",
    "get_concept_list": "concept_list",
    "get_company_info": "company_info",
}
```

---

## 8. 并发安全保证

### 8.1 写入并发

| 场景 | 行为 |
|------|------|
| 多进程写不同分区 | 完全并发，无冲突 |
| 多进程写同分区 | 各自写独立文件，无冲突 |
| 写入 + 聚合任务 | 聚合任务持有锁，但新写入的文件名不同，不受影响 |

### 8.2 读取并发

| 场景 | 行为 |
|------|------|
| 多进程只读 | DuckDB 无限制，完全并发 |
| 读取 + 写入 | 互不影响，最终一致性 |
| 读取 + 聚合 | 聚合使用原子重命名，读取要么看到旧文件，要么看到新文件 |

### 8.3 一致性模型

**最终一致性**：写入后，其他进程可能在极短时间内看不到最新数据。对于回测场景可接受。

聚合层与原始层之间可能存在短暂不一致（聚合任务执行中），查询路径优先读聚合层，未命中回退原始层，保证数据不丢失。

---

## 9. 性能预期

### 9.1 写入性能

| 指标 | 预期 |
|------|------|
| 单进程写入延迟 | < 50ms（1000 行 × 10 列） |
| 多进程写入吞吐 | N 进程 = N × 单进程吞吐（完全线性扩展） |
| 写入冲突 | 零冲突，零等待 |

### 9.2 查询性能

| 查询类型 | 预期 | 对比 DuckDB 原生 |
|---------|------|-----------------|
| 单股票单日点查 | < 10ms | 相近 |
| 单股票单月范围查询 | < 50ms | 相近（filter pushdown） |
| 聚合层查询 | < 5ms | 优于原生（单文件） |
| 全市场单日聚合 | < 150ms | 慢 10-20%（多文件开销） |

### 9.3 存储效率

| 指标 | 预期 |
|------|------|
| 压缩率 | Snappy 压缩，约为原始 CSV 的 30-50% |
| 日线数据（全 A 股/天） | 约 1-5MB |
| 月数据量 | 约 50-100MB |
| 快照数据（全市场/天） | 约 10-20MB |

---

## 10. 与现有系统的集成

### 10.1 集成策略

```
Phase 1: 并行运行
├── 新 ParquetCache 独立实现（新目录）
├── 现有 DuckDB + Pickle 保持不变
└── 通过配置开关选择使用哪个缓存后端

Phase 2: 灰度迁移
├── P0 接口优先迁移（日线行情、指数成分、财务数据）
├── 读取时：ParquetCache → DuckDB → Pickle → akshare（fallback 链）
└── 验证数据一致性和性能

Phase 3: 全面切换
├── 默认使用 ParquetCache
├── 保留 DuckDB 作为只读备份
└── 逐步清理 Pickle 缓存
```

### 10.2 配置项

```python
CACHE_CONFIG = {
    "backend": "parquet",           # parquet | duckdb | pickle
    "base_dir": "data/cache",
    "memory_cache_max_items": 5000,
    "aggregation": {
        "enabled": True,
        "schedule": "daily",        # daily | weekly | manual
        "lock_dir": "data/cache/_locks",
    },
    "tables": {
        "stock_daily": {
            "partition_by": "date",
            "ttl_hours": 0,
            "compaction_threshold": 20,
            "aggregation_enabled": True,
        },
        "finance_indicator": {
            "partition_by": "report_date",
            "ttl_hours": 2160,
            "compaction_threshold": 5,
            "aggregation_enabled": False,
        },
    },
}
```

---

## 11. 风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|---------|
| 文件碎片 | 查询性能下降 | 聚合层 + 阈值控制 + 例行清理 |
| Schema 不一致 | 查询报错 | 写入前 Schema 校验 + 版本管理 |
| 磁盘空间不足 | 写入失败 | 监控告警 + 自动清理过期缓存 |
| 聚合任务中断 | 临时文件残留 | 启动时清理 `.tmp` 文件 |
| 跨平台兼容性 | Windows 文件锁 | 使用 `filelock` 库 |
| DuckDB 版本升级 | Parquet 读取兼容 | 锁定版本 + 升级测试 |
| 聚合层与原始层不一致 | 查询结果不完整 | 查询路径 fallback + 延迟删除原始文件 |

---

## 12. 实施计划

### Phase 1：核心实现（预计 3-5 天）

| 任务 | 产出 |
|------|------|
| CacheTable 注册表 | 接口配置、Schema 定义 |
| ParquetCache 类 | 原子写入、分区管理、唯一文件名 |
| 查询接口 | DuckDB 只读查询、聚合层优先 |
| 内存缓存层 | LRU + TTL |
| 单元测试 | 写入、读取、并发测试 |

### Phase 2：聚合任务（预计 2-3 天）

| 任务 | 产出 |
|------|------|
| 聚合核心逻辑 | 文件合并、去重、原子替换 |
| 文件锁机制 | filelock 跨平台兼容 |
| 调度器 | cron / APScheduler 集成 |
| 延迟删除 | 原始文件保留机制 |
| 集成测试 | 聚合并发安全测试 |

### Phase 3：接口适配（预计 3-5 天）

| 任务 | 产出 |
|------|------|
| P0 接口适配 | 日线行情、指数成分、财务数据 |
| Fallback 链 | Parquet → DuckDB → Pickle → akshare |
| 性能基准测试 | 对比现有方案 |
| 文档 | 使用指南、迁移指南 |

### Phase 4：全面迁移（预计 2-3 天）

| 任务 | 产出 |
|------|------|
| P1/P2 接口适配 | 资金流、行业、股东、估值等 |
| 快照层实现 | 每日批量预存 |
| 清理脚本 | Pickle 缓存清理 |
| 监控告警 | 磁盘空间、查询延迟、聚合状态 |

---

## 13. 技术选型总结

| 组件 | 选择 | 备选 |
|------|------|------|
| 存储格式 | Parquet | ORC（生态不如 Parquet） |
| 查询引擎 | DuckDB | Polars（查询能力不如 DuckDB 灵活） |
| 压缩算法 | Snappy | Zstd（压缩率更高但 CPU 开销大） |
| 文件锁 | filelock | fcntl（仅 Unix） |
| 序列化 | PyArrow | Pandas（底层也是 PyArrow） |
| 调度器 | APScheduler | cron（系统级） |

---

## 14. 参考

- [DuckDB Concurrency Documentation](https://duckdb.org/docs/current/connect/concurrency)
- [Parquet File Format Specification](https://parquet.apache.org/docs/file-format/)
- [PyArrow Parquet Documentation](https://arrow.apache.org/docs/python/parquet.html)
- [SQLite WAL Mode](https://www.sqlite.org/wal.html)
- [DuckLake: Multi-writer Support](https://duckdb.org/2026/04/01/ducklake.html)
- `docs/akshare_interface_analysis.md` — 本项目接口依赖调研
