# THSQuant（同花顺 SuperMind）回测指南

目录：`skills/thsquant_strategy/`

---

## 环境配置

```bash
cd skills/thsquant_strategy
npm install
```

`.env` 需要：
```
THSQUANT_USERNAME=your_username
THSQUANT_PASSWORD=your_password
```

首次使用需手动登录（同花顺使用 iframe 登录，自动化较复杂）：
```bash
node browser/manual-login-capture.js
# 浏览器打开后，手动输入账号密码登录，60秒后自动保存 session
```

Session 有效期约 7 天，过期后重新执行上述命令。

---

## 提交回测

```bash
# 基本用法（更新已有策略并运行）
node run-skill.js --id <algoId> --file ./my_strategy.py

# 每次创建新策略（保留历史）
node run-skill.js --file ./my_strategy.py --name rfscore7_pb10

# 完整参数
node run-skill.js \
  --id <algoId> \
  --file ./my_strategy.py \
  --start 2023-01-01 \
  --end 2024-12-31 \
  --capital 100000 \
  --freq DAILY \
  --benchmark 000300.SH
```

参数说明：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--id` | 策略 ID（不填则创建新策略） | - |
| `--file` | 本地策略文件路径（必填） | - |
| `--name` | 策略名称（创建新策略时用） | 文件名 |
| `--start` | 回测开始日期 | 2023-01-01 |
| `--end` | 回测结束日期 | 2024-12-31 |
| `--capital` | 初始资金 | 100000 |
| `--freq` | DAILY / MINUTE | DAILY |
| `--benchmark` | 基准指数 | 000300.SH |

---

## 查询回测结果

```bash
# 列出策略所有历史回测（最多 50 条）
node fetch-backtest-results.js --algo-id <id> --list

# 最近一次完整结果
node fetch-backtest-results.js --algo-id <id> --latest

# 指定 backtestId 查询
node fetch-backtest-results.js --backtest-id <id>

# 保存结果到文件
node fetch-backtest-results.js --algo-id <id> --latest --save
```

---

## 策略代码格式

同花顺使用与 JoinQuant 相似的格式：

```python
def initialize(context):
    g.stock_pool = '000300.SH'
    run_monthly(rebalance, 1)

def rebalance(context, data):
    stocks = get_index_stocks(g.stock_pool)
    # 选股逻辑...
    order_target_percent(stock, 1.0 / len(selected))

def handle_data(context, data):
    pass
```

---

## 核心 API 端点

已验证的 API（通过逆向工程确认）：

```
策略管理：
  POST /platform/algorithms/queryall2/      列出所有策略
  POST /platform/algorithms/queryinfo/      获取策略详情（algoId=）
  POST /platform/algorithms/update/         更新策略代码（algoId= algo_name= code=）
  POST /platform/algorithms/add/            创建新策略（algoName= stock_market= algoCode=）

回测运行：
  POST /platform/backtest/run/              运行回测（algoId= beginDate= endDate= capitalBase= frequency= benchmark=）
  POST /platform/backtest/backtestloop/     轮询状态（backTestId=）
  POST /platform/backtest/querylatest/      最近一次回测（algoId= query=status）
  POST /platform/backtest/queryall/         历史回测列表（algo_id= page= num=）

回测结果：
  POST /platform/backtest/backtestdetail/   详情（backTestId=）
  POST /platform/backtest/backtestperformance  绩效（backTestId=）
  POST /platform/backtest/tradelog          交易记录（backTestId=）
  POST /platform/backtest/backtestlog/      运行日志（backTestId=）
```

注意：参数大小写敏感，`backTestId`（T 大写），`algoId`（camelCase）。

---

## 文件结构

```
thsquant_strategy/
├── .env                              # 账号配置
├── run-skill.js                      # 提交回测入口
├── fetch-backtest-results.js         # 查询回测结果
├── list-strategies.js                # 列出所有策略
├── fetch-report.js                   # 获取指定回测报告
├── request/
│   ├── thsquant-client.js            # HTTP 客户端（含重试）
│   └── strategy-runner.js            # 完整工作流
├── browser/
│   ├── session-manager.js            # Session 管理
│   └── manual-login-capture.js       # 手动登录
└── data/
    └── session.json                  # Session 存储
```

---

## 常见问题

**Q: 登录失败**
同花顺使用 iframe 登录，必须手动登录：
```bash
node browser/manual-login-capture.js
```

**Q: 回测状态一直是 RUNNING**
`waitForBacktest` 默认最多等 5 分钟。如果策略计算量大，增加 `maxWait`。

**Q: 参数格式错误**
注意 API 参数大小写：`backTestId`（T 大写），`algoId`（不是 algo_id）。

**Q: 获取策略列表为空**
确认 session 有效：`node test-session.js`
