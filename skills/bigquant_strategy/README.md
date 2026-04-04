# BigQuant Strategy Skill

## 架构说明

BigQuant AIStudio 是 VS Code Web + Jupyter 环境，执行模型与 JoinQuant/RiceQuant 不同：

| 特性 | JoinQuant/RiceQuant | BigQuant |
|------|---------------------|---------|
| 执行方式 | Jupyter kernel WebSocket | AIFlow task (notebook JSON) |
| 触发执行 | `POST /api/sessions` + WebSocket | `POST /taskruns {state:"trigger"}` |
| 输出获取 | WebSocket 实时流 | `GET /logs/{runId}` |
| 时间限制 | 180分钟/天 | 无限制（免费资源） |

**当前实现就是 BigQuant 的 notebook 运行方式**：代码以 notebook JSON 格式提交，在 Jupyter kernel 里执行，输出从日志读取。这是 BigQuant 唯一支持的程序化执行方式。

## 快速开始

```bash
cd skills/bigquant_strategy

# 运行策略（自动命名）
node run-skill.js --strategy examples/my_strategy.py

# 指定业务名称（推荐，方便在平台上识别）
node run-skill.js --strategy examples/my_strategy.py --name 小市值选股_2023H1

# 完整参数
node run-skill.js \
  --strategy examples/my_strategy.py \
  --name 小市值选股_2023H1 \
  --start-date 2023-01-01 \
  --end-date 2023-06-30 \
  --capital 1000000 \
  --timeout-ms 300000
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--strategy` | 策略文件路径 (.py) | — |
| `--cell-source` | 内联代码字符串 | — |
| `--name` | 任务名称（有业务含义） | 文件名+时间戳 |
| `--start-date` | 回测开始日期 | 2023-01-01 |
| `--end-date` | 回测结束日期 | 2023-12-31 |
| `--capital` | 初始资金 | 100000 |
| `--benchmark` | 基准指数 | 000300.XSHG |
| `--timeout-ms` | 超时毫秒 | 300000 |

## 策略代码格式

BigQuant 使用 DAI (Data Access Interface) 通过 SQL 查询数据，**没有内置回测框架**，需要手动实现：

```python
"""
策略名称 - BigQuant DAI 版本
"""
import dai
import pandas as pd
import numpy as np

DATE = "2024-01-02"

# 查询数据
df = dai.query("""
    SELECT instrument, close, upper_limit, float_market_cap
    FROM cn_stock_bar1d
    WHERE date = '{date}'
""".format(date=DATE)).df()

# 处理逻辑
result = df[df["float_market_cap"] < 30e8]

# 输出结果（系统自动解析指标）
print("选出股票数: " + str(len(result)))
print("总收益: 12.5%")
print("年化收益: 25.0%")
print("最大回撤: -8.3%")
```

## 可用数据（免费账户）

| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `cn_stock_bar1d` | 日K线 | open/high/low/close/volume/upper_limit/lower_limit |
| `cn_stock_valuation` | 估值 | pe_ttm/pb/total_market_cap/float_market_cap |
| `cn_stock_instruments` | 股票列表 | instrument/name/type（需 filters） |
| `cn_stock_industry` | 行业分类 | industry_level1/2/3/4_name |
| `cn_stock_balance_sheet` | 资产负债表 | 完整财务字段（需 filters） |
| `cn_stock_dividend` | 分红 | bonus_rate/cash_before_tax/ex_date |
| `cn_stock_suspend` | 停牌 | suspend_period/suspend_reason |

详细 API 参考：[skills/backtest_guide/reference/bigquant_api_reference.md](../backtest_guide/reference/bigquant_api_reference.md)

## 结果数据

每次运行结果保存在 `data/bigquant-result-*.json`，包含：
- `taskId` / `runId` — 平台任务 ID
- `taskName` — 有业务含义的名称
- `config` — 回测参数
- `metrics` — 自动解析的指标（总收益/年化/回撤/夏普等）
- `textOutput` — 完整输出文本
- `logs` — 执行日志

## 注意事项

1. 每次运行都创建新 Task，历史 Task 不删除
2. 市值单位是**元**（不是亿元）：50亿 = 5e9
3. 价格已前复权，`upper_limit`/`lower_limit` 也是复权后的值
4. 无指数K线（免费账户），需用大市值股票近似
5. Session 有效期约 7 天，过期自动重新登录

## 文件结构

```
skills/bigquant_strategy/
├── run-skill.js              # CLI 入口
├── get-output.js             # 调试用：直接获取输出
├── load-env.js               # 环境变量加载
├── paths.js                  # 路径配置
├── .env                      # 账号配置
├── request/
│   ├── bigquant-auth.js      # 登录认证（自动刷新）
│   ├── bigquant-client.js    # HTTP 客户端（核心 API）
│   ├── bigquant-runner.js    # 向后兼容导出
│   └── strategy-runner.js   # 工作流编排
├── examples/
│   ├── simple_backtest.py    # 简单测试
│   ├── probe_data_api.py     # 数据 API 探测
│   ├── probe_all_tables.py   # 全量数据表探测
│   └── ...
└── data/                     # 运行结果和 session
```
