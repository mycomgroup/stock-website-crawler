# 离线数据预热脚本实现计划

## 目标
创建离线数据预热脚本，支持定期更新不频繁变化的数据。

## 目录结构
```
scripts/offline_data/
├── README.md
├── config.yaml
├── prewarm_static.py      # 静态数据（季度更新）
├── prewarm_quarterly.py   # 季度数据
├── prewarm_monthly.py     # 月度数据
├── prewarm_weekly.py      # 周度数据
├── prewarm_daily.py       # 日度数据
├── prewarm_all.py         # 一键预热
└── utils/
    ├── __init__.py
    ├── stock_pool.py
    ├── progress.py
    └── report.py
```

## 实现步骤

### 1. 创建配置文件 config.yaml
- 股票池配置（沪深300、中证500、自定义）
- 时间范围配置
- 缓存路径配置
- 预热选项

### 2. 创建工具函数 utils/
- `stock_pool.py`: 股票池获取函数
- `progress.py`: 进度显示工具
- `report.py`: 预热报告生成

### 3. 创建预热脚本
- `prewarm_static.py`: 公司基本信息、行业分类
- `prewarm_quarterly.py`: 分红送股、股东信息
- `prewarm_monthly.py`: 指数成分股、宏观数据
- `prewarm_weekly.py`: 解禁数据、股东变动
- `prewarm_daily.py`: 日线数据、期权、可转债
- `prewarm_all.py`: 一键预热所有数据

### 4. 创建 README.md
- 使用说明
- 命令行参数
- 定时任务配置

## 数据更新频率
| 类型 | 数据 | 更新周期 |
|------|------|----------|
| 静态 | 公司信息、行业分类 | 季度初 |
| 季度 | 分红、股东 | 财报季后 |
| 月度 | 指数成分、宏观 | 月初 |
| 周度 | 解禁、股东变动 | 周一 |
| 日度 | 行情数据 | 每交易日 |

## 待确认
- [x] 用户已确认方案符合需求
- [ ] 开始实现