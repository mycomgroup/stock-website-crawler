# 离线数据预热脚本

本目录包含定期更新数据的预热脚本，支持离线运行策略时所需的数据。

## 数据更新频率

| 频率 | 数据类型 | 建议更新周期 |
|------|----------|--------------|
| **静态** | 公司基本信息、行业分类 | 每季度初 |
| **季度** | 分红送股、股东信息 | 财报季后 (1/4/7/10月下旬) |
| **月度** | 指数成分股、宏观数据 | 每月首日 |
| **周度** | 限售解禁、股东变动 | 每周一 |
| **日度** | 行情数据 | 每交易日收盘后 |

## 快速开始

### 一键预热

```bash
# 预热所有数据（不含日线）
python prewarm_all.py

# 强制更新所有数据
python prewarm_all.py --force

# 包含日线数据
python prewarm_all.py --include-daily

# 只预热静态数据
python prewarm_all.py --static-only
```

### 按频率预热

```bash
# 静态数据（公司信息、行业分类）
python prewarm_static.py

# 季度数据（分红、股东）
python prewarm_quarterly.py

# 月度数据（指数成分、宏观）
python prewarm_monthly.py

# 周度数据（解禁、股东变动）
python prewarm_weekly.py

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

# 时间范围
date_range:
  static_start: "2020-01-01"
  daily_start: "2023-01-01"

# 缓存路径
cache:
  duckdb_dir: "data"
  pickle_dir: "finance_cache"
```

## 定时任务配置

### Linux/Mac (cron)

```bash
# 编辑 crontab
crontab -e

# 添加以下任务
# 每季度初更新静态数据 (1/4/7/10月1日 6:00)
0 6 1 1,4,7,10 * cd /path/to/jk2bt && python scripts/offline_data/prewarm_static.py

# 每月1日更新月度数据
0 6 1 * * cd /path/to/jk2bt && python scripts/offline_data/prewarm_monthly.py

# 每周一更新周度数据
0 6 * * 1 cd /path/to/jk2bt && python scripts/offline_data/prewarm_weekly.py

# 每交易日收盘后更新日度数据 (工作日 18:00)
0 18 * * 1-5 cd /path/to/jk2bt && python scripts/offline_data/prewarm_daily.py --sample
```

### Windows (任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（每日/每周/每月）
4. 设置操作：启动程序
   - 程序：`python`
   - 参数：`scripts/offline_data/prewarm_all.py`
   - 起始位置：`C:\path\to\jk2bt`

## 数据存储位置

```
jk2bt/
├── data/                    # DuckDB 数据库
│   ├── market.db           # 行情数据
│   ├── company_info.db     # 公司信息
│   ├── dividend.db         # 分红数据
│   ├── shareholder.db      # 股东数据
│   ├── industry_sw.db      # 行业分类
│   └── ...
├── finance_cache/          # Pickle 缓存
│   └── *.pkl
└── reports/prewarm/        # 预热报告
    └── prewarm_report_*.json
```

## 常见问题

### 1. 如何检查缓存是否有效？

```python
from jqdata_akshare_backtrader_utility.db.cache_manager import get_cache_manager

manager = get_cache_manager()
summary = manager.get_cache_summary()
print(summary)
```

### 2. 如何清空缓存重新下载？

```bash
# 强制更新
python prewarm_all.py --force

# 或删除缓存文件
rm -rf data/*.db
rm -rf finance_cache/*.pkl
```

### 3. 网络请求失败怎么办？

脚本会自动重试3次。如果仍然失败，请检查：
- 网络连接是否正常
- AkShare 是否安装最新版本
- 是否触发了数据源的限流

### 4. 如何只预热特定股票？

```bash
python prewarm_static.py --stocks 600519.XSHG 000858.XSHE
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `config.yaml` | 配置文件 |
| `prewarm_static.py` | 静态数据预热 |
| `prewarm_quarterly.py` | 季度数据预热 |
| `prewarm_monthly.py` | 月度数据预热 |
| `prewarm_weekly.py` | 周度数据预热 |
| `prewarm_daily.py` | 日度数据预热 |
| `prewarm_all.py` | 一键预热 |
| `utils/stock_pool.py` | 股票池工具 |
| `utils/progress.py` | 进度显示 |
| `utils/report.py` | 报告生成 |
