# BigQuant 回测指南

目录：`skills/bigquant_strategy/`

---

## 核心概念

BigQuant 是 **Task-based 模型**，与其他平台不同：
- 没有"策略 ID"概念
- 每次提交创建一个新 Task，历史 Task 保留
- Task 名称格式：`{策略文件名}_{YYYYMMDD}_{HHMM}`
- 回测结果在 notebook cell 的 print 输出中，不是结构化 API

---

## 环境配置

```bash
cd skills/bigquant_strategy
npm install
```

`.env` 需要：
```
BIGQUANT_USERNAME=your_username
BIGQUANT_PASSWORD=your_password
# 可选：
BIGQUANT_STUDIO_ID=your_studio_id
BIGQUANT_RESOURCE_SPEC_ID=your_resource_spec_id
```

Session 自动管理。

---

## 提交回测

```bash
# 基本用法
node run-skill.js --strategy ./my_strategy.py \
  --start-date 2023-01-01 --end-date 2024-12-31

# 指定业务名称（方便后续查询）
node run-skill.js --strategy ./my_strategy.py \
  --name rfscore7_pb10 \
  --start-date 2023-01-01 --end-date 2024-12-31

# 完整参数
node run-skill.js \
  --strategy ./my_strategy.py \
  --name rfscore7_pb10 \
  --start-date 2023-01-01 \
  --end-date 2024-12-31 \
  --capital 100000 \
  --benchmark 000300.XSHG \
  --frequency day \
  --timeout-ms 300000
```

参数说明：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--strategy` | 策略文件路径（必填） | - |
| `--name` | 业务名称（建议填，方便查询） | 文件名 |
| `--start-date` | 回测开始日期 | 2023-01-01 |
| `--end-date` | 回测结束日期 | 2023-12-31 |
| `--capital` | 初始资金 | 100000 |
| `--benchmark` | 基准指数 | 000300.XSHG |
| `--frequency` | day / minute | day |
| `--timeout-ms` | 等待超时 | 300000 |

---

## 查询回测结果

```bash
# 列出所有 Task（最近 100 条）
node fetch-backtest-results.js --list

# 按策略名称前缀过滤
node fetch-backtest-results.js --name-prefix rfscore7_pb10 --list

# 最近一条（可配合前缀）
node fetch-backtest-results.js --name-prefix rfscore7_pb10 --latest

# 指定 taskId 查询
node fetch-backtest-results.js --task-id <id>

# 保存结果到文件
node fetch-backtest-results.js --name-prefix rfscore7 --latest --save
```

---

## 策略代码格式

BigQuant 策略在 notebook cell 中执行，结果通过 print 输出：

```python
# BigQuant 策略格式
import bigquant

# 回测参数由平台注入（通过 envs.strategy_params）
start_date = '2023-01-01'
end_date = '2024-12-31'
capital_base = 100000

# 选股逻辑
def select_stocks(date):
    # 使用 DAI 数据接口
    df = D.history_data(
        instruments=['000001.SZA'],
        start_date=date,
        end_date=date,
        fields=['close', 'pe_ttm']
    )
    return df

result = select_stocks(start_date)
print(f"选股结果: {len(result)} 条")
print(f"年化收益: {annual_return:.2%}")  # 必须 print 才能被解析
```

关键：策略必须用 `print` 输出关键指标，否则 `fetch-backtest-results.js` 无法解析结果。

---

## 数据接口（DAI）

BigQuant 使用 DAI 数据接口，主要数据表：

```python
# 日线行情
D.history_data(instruments, start_date, end_date, 
               fields=['open','close','high','low','volume'])

# 基本面数据
D.history_data(instruments, start_date, end_date,
               fields=['pe_ttm', 'pb_lf', 'market_cap'])

# 财务数据
D.history_data(instruments, start_date, end_date,
               fields=['net_profit', 'revenue', 'roe'])
```

完整数据表参考：[reference/bigquant_api_reference.md](reference/bigquant_api_reference.md)

---

## 文件结构

```
bigquant_strategy/
├── .env                              # 账号配置
├── run-skill.js                      # 提交回测入口
├── fetch-backtest-results.js         # 查询回测结果
├── request/
│   ├── bigquant-client.js            # HTTP 客户端（含重试）
│   ├── bigquant-auth.js              # 认证管理
│   └── strategy-runner.js            # 完整工作流
└── examples/                         # 示例策略
```

---

## 常见问题

**Q: 找不到之前的回测结果**
BigQuant 没有策略 ID，用 Task 名称前缀查：
```bash
node fetch-backtest-results.js --name-prefix 你的策略名 --list
```

**Q: 资源不足，无法创建 Task**
系统会自动选择 `usable:true` 的免费资源。如果没有可用资源，等待后重试。

**Q: 结果解析为空**
确认策略代码有 `print` 输出关键指标。BigQuant 的结果在 notebook 输出中，不是结构化 API。

**Q: Studio 激活失败**
可能已经激活，忽略此错误继续执行即可。
