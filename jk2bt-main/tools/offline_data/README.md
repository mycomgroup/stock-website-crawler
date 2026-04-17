# 离线数据预热脚本

本目录包含定期更新数据的预热脚本，支持离线运行策略时所需的数据。

## 数据更新频率

| 频率 | 数据类型 | 预热方式 |
|------|----------|----------|
| **日度** | 行情数据（股票/ETF/指数） | 按需预热，数据量大 |
| **静态** | 公司基本信息 | 按需预热，使用 `prewarm_company_info_cache()` |
| **其他** | 行业/分红/股东/宏观/解禁等 | 依赖内部缓存（7-180天TTL），按需自动获取 |

> 低频数据（行业分类、分红、股东变动、宏观指标等）已有内部缓存机制，
> 首次调用时自动缓存，后续请求直接使用缓存，无需单独预热。

## 快速开始

### 一键预热

```bash
# 预热元数据 + 公司信息（默认）
python prewarm_all.py

# 强制更新所有数据
python prewarm_all.py --force

# 包含日线数据
python prewarm_all.py --include-daily

# 只预热静态数据（元数据+公司信息）
python prewarm_all.py --static-only
```

### 按类型预热

```bash
# 公司信息（使用核心模块 prewarm_company_info_cache）
python prewarm_static.py

# 日度数据（行情）
python prewarm_daily.py --sample
```

### 自定义股票池

```bash
# 指定股票
python prewarm_static.py --stocks 600519.XSHG 000858.XSHE

# 使用预设股票池
python prewarm_static.py --pool core      # 沪深300
python prewarm_static.py --pool extended  # 中证500
```

## 配置文件

`config.yaml` 包含股票池、时间范围、缓存路径等配置。

```yaml
# 股票池配置
stock_pool:
  custom:
    - "600519.XSHG"
    - "000858.XSHE"

# 缓存路径
cache:
  duckdb_dir: "data_cache"
```

## 定时任务配置

### Linux/Mac (cron)

```bash
# 编辑 crontab
crontab -e

# 每季度初更新公司信息 (1/4/7/10月1日 6:00)
0 6 1 1,4,7,10 * cd /path/to/jk2bt && python tools/offline_data/prewarm_static.py

# 每交易日收盘后更新日度数据 (工作日 18:00)
0 18 * * 1-5 cd /path/to/jk2bt && python tools/offline_data/prewarm_daily.py --sample
```

## 数据存储位置

```
jk2bt/
├── data_cache/                # DuckDB 数据库 + parquet缓存
│   ├── market.db             # 行情数据
│   ├── meta.db               # 元数据
│   └── cache/                # parquet缓存
└── reports/prewarm/          # 预热报告
    └── prewarm_report_*.json
```

## 常见问题

### 1. 如何检查缓存是否有效？

```python
from jk2bt.cache import get_cache_manager

manager = get_cache_manager()
# 检查具体表
df = manager.get("stock_daily")
print(df.shape if df is not None else "无缓存")
```

### 2. 如何清空缓存重新下载？

```bash
# 强制更新
python prewarm_all.py --force

# 或删除缓存文件
rm -rf data_cache/*.db
rm -rf data_cache/cache/
```

### 3. 网络请求失败怎么办？

脚本会自动重试。如果仍然失败，请检查：
- 网络连接是否正常
- AkShare 是否安装最新版本
- 是否触发了数据源的限流

### 4. 为什么没有周度/月度/季度预热脚本？

行业分类、分红、股东变动、宏观指标等低频数据已有内部缓存机制
（TTL 7-180天），首次调用时自动缓存，无需单独预热脚本。

## 文件说明

| 文件 | 说明 |
|------|------|
| `config.yaml` | 配置文件 |
| `prewarm_static.py` | 公司信息预热 |
| `prewarm_daily.py` | 日度行情预热 |
| `prewarm_all.py` | 一键预热 |
| `utils/stock_pool.py` | 股票池工具 |
| `utils/progress.py` | 进度显示 |
| `utils/report.py` | 报告生成 |
| `enhanced_cache_manager.py` | 增强版缓存管理器（队列+重试） |
