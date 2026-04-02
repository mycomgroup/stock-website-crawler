# THSQuant 回测接口文档

> 通过逆向工程验证的真实 HTTP API，用于自动化提交和获取回测结果。
> Skill 目录：`skills/thsquant_strategy/`

---

## 一、快速开始

```bash
cd skills/thsquant_strategy

# 创建新策略并运行回测（推荐，保留历史）
node run-skill.js --file path/to/strategy.py --name rfscore7_pb10_v1

# 指定日期范围
node run-skill.js --file strategy.py --name my_strategy \
  --start 2023-01-01 --end 2024-12-31 \
  --capital 1000000 --freq DAILY --benchmark 000300.SH

# 复用已有策略 ID（不创建新策略）
node run-skill.js --file strategy.py --id 67c935e607887b957629ad72
```

### 策略命名规则

每次提交自动创建新策略，名称格式：
```
{strategyName}_{YYYYMMDD}_{beginDate}~{endDate}
例：rfscore7_pb10_v1_20260402_20230101~20241231
```

---

## 二、HTTP API 端点（已验证）

**Base URL：** `https://quant.10jqka.com.cn`

**重要：** 参数名全部用 camelCase，不是 snake_case！

### 认证

```
POST /platform/user/getauthdata
Body: isajax=1
Response: {"errorcode":0,"result":{"user_id":"772028948",...}}
```

### 策略管理

| 端点 | 参数 | 说明 |
|------|------|------|
| `POST /platform/algorithms/queryall2/` | `isajax=1` | 获取策略列表 |
| `POST /platform/algorithms/queryinfo/` | `algoId={id}&isajax=1` | 获取策略详情（含代码）|
| `POST /platform/algorithms/update/` | `algoId={id}&algo_name={name}&code={code}&isajax=1` | 更新策略代码 |
| `POST /platform/algorithms/add/` | `algo_name={name}&code={code}&stock_market=STOCK&isajax=1` | 创建新策略 |
| `POST /platform/algorithms/delete/` | `algo_id={id}&isajax=1` | 删除策略 |

### 回测运行

```
POST /platform/backtest/run/
Body: algoId={id}&beginDate=2023-01-01&endDate=2024-12-31&capitalBase=100000&frequency=DAILY&benchmark=000300.SH&isajax=1

Response: {"errorcode":0,"result":{"backtest_id":"69ce1eff...","progress":0}}
```

**参数说明：**
- `algoId` — 策略 ID（camelCase，不是 algo_id）
- `beginDate` / `endDate` — 日期格式 `YYYY-MM-DD`
- `capitalBase` — 初始资金（字符串）
- `frequency` — `DAILY` / `1d` / `1h` / `1m`
- `benchmark` — 基准指数，如 `000300.SH`

### 回测状态轮询

```
POST /platform/backtest/backtestloop/
Body: backTestId={id}&isajax=1   ← 注意 T 大写

Response: {"errorcode":0,"result":{"status":"SUCCESS","progress":1,...}}
```

**status 值：** `RUNNING` / `SUCCESS` / `FAILED` / `ERROR`

### 回测结果 API

所有结果 API 都用 `backTestId`（T 大写）：

| 端点 | 说明 | 返回数据 |
|------|------|---------|
| `POST /platform/backtest/queryinfo/` | 回测基本信息 | 名称、状态、时间 |
| `POST /platform/backtest/backtestdetail/` | 完整绩效指标 | alpha/beta/sharpe/收益率/回撤等 |
| `POST /platform/backtest/backtestperformance` | 绩效摘要 | sharpe/sortino/alpha/beta |
| `POST /platform/backtest/tradelog` | 交易记录 | 每笔买卖明细 |
| `POST /platform/backtest/backtestlog/` | 策略日志 | log.info 输出 |
| `POST /platform/backtest/dailypositiongains` | 每日持仓收益 | 逐日资产变化 |
| `POST /platform/backtest/backspecificinfo` | 月度/年度收益 | 需加 `type=profit` |
| `POST /platform/backtest/getriskanalysis` | 风险分析 | 暂不稳定 |

### 回测历史

```
POST /platform/backtest/querylatest/
Body: algoId={id}&query=status&isajax=1
Response: {"result":{"status":"SUCCESS","backtest_id":"..."}}

POST /platform/backtest/queryall/
Body: algo_id={id}&page=1&num=10&isajax=1   ← 注意这里用 algo_id（snake_case）
Response: {"result":{"count":2,"history":[...]}}
```

---

## 三、返回数据结构

### backtestdetail 绩效指标

```json
{
  "performance": {
    "yield": 0.0327,              // 总收益率
    "annual_yield": 0.0338,       // 年化收益率
    "benchmark_yield": 0.1468,    // 基准收益率
    "benchmark_annual_yield": 0.152,
    "max_drawdown": 0.2829,       // 最大回撤
    "drawdown_most": "20231229",  // 最大回撤日期
    "volatility": 0.3959,         // 波动率
    "downside_risk": 0.2205,      // 下行风险
    "tracking_error": 0.315,      // 跟踪误差
    "alpha": -0.1358,             // Alpha
    "beta": 1.1294,               // Beta
    "information_ratio": -0.1675, // 信息比率
    "win_rate": 0.4793,           // 胜率（日）
    "benchmark_win_rate": 0.4669, // 基准胜率
    "trade_winrate": null,        // 交易胜率
    "progress": 1
  }
}
```

### backtestperformance 绩效摘要

```json
{
  "sharpe_ratio": 0.0454,
  "sortino": 0.0816,
  "alpha": -0.1358,
  "beta": 1.1294,
  "benchmark_yield": 0.1468,
  "progress": 1
}
```

### tradelog 交易记录

```json
{
  "data": [
    {
      "trade_date": "2024-03-25 09:31:00",
      "asset_code": "600157.SH",
      "stock_name": "永泰能源",
      "operation": "buy",
      "price": 3.45,
      "amount": 1000,
      "value": 3450.0
    }
  ]
}
```

### backtestlog 策略日志

```json
{
  "total": 6,
  "list": [
    {
      "type": "INFO",
      "value": "INFO :回测开始运行",
      "now": "2026-04-02 15:47:11.571307",
      "time": "2024-01-01"
    }
  ]
}
```

### dailypositiongains 每日持仓

```json
{
  "data": [
    {
      "position_date": "2024-12-31T15:15:00",
      "total_asset_value": 103273.47,
      "ending_cash": 5000.0
    }
  ]
}
```

### backspecificinfo 月度收益（type=profit）

```json
{
  "table": {
    "2023-12": {
      "1": {"benchmark_yield": 0, "yield": 0},
      "3": {"yield": null, "benchmark_yield": null}
    }
  }
}
```

---

## 四、完整工作流代码

```javascript
import { THSQuantClient } from './request/thsquant-client.js';
import { ensureTHSQuantSession } from './browser/session-manager.js';

// 1. 获取 session
const cookies = await ensureTHSQuantSession({ username, password });
const client = new THSQuantClient({ cookies });

// 2. 创建新策略（每次新建，保留历史）
const created = await client.createStrategy('rfscore7_pb10_v1_20260402', code);
const algoId = created.algoId;

// 3. 运行回测
const run = await client.runBacktest(algoId, {
  beginDate: '2023-01-01',
  endDate: '2024-12-31',
  capitalBase: '1000000',
  frequency: 'DAILY',
  benchmark: '000300.SH'
});

// 4. 等待完成
const result = await client.waitForBacktest(run.backtestId, {
  maxWait: 300000,
  interval: 3000,
  onProgress: ({ status }) => console.log(status)
});

// 5. 获取完整报告
const report = await client.getFullReport(run.backtestId);
// report 包含: detail, performance, tradeLog, backtestLog, dailyGains, specificInfo
```

---

## 五、与 JoinQuant 接口对比

| 功能 | JoinQuant | THSQuant |
|------|-----------|---------|
| 获取策略列表 | `listStrategies()` | `listStrategies()` ✅ |
| 获取策略上下文 | `getStrategyContext(id)` 需要 CSRF token | `getStrategyContext(id)` 无需 token ✅ |
| 保存策略代码 | `saveStrategy(id, name, code, context)` | `saveStrategy(id, name, code)` ✅ |
| 运行回测 | `runBacktest(id, code, config, context)` | `runBacktest(id, config)` ✅ |
| 轮询状态 | `getBacktestResult(id, context)` | `pollBacktestStatus(id)` ✅ |
| 等待完成 | 手动轮询 | `waitForBacktest(id, opts)` ✅ |
| 交易记录 | `getTransactionInfo(id)` | `getTradeLog(id)` ✅ |
| 持仓记录 | `getPositionInfo(id)` | `getDailyPositionGains(id)` ✅ |
| 策略日志 | `getLog(id)` | `getBacktestLog(id)` ✅ |
| 绩效统计 | `getBacktestStats(id)` | `getBacktestDetail(id)` + `getBacktestPerformance(id)` ✅ |
| 归因分析 | `getAttributionBrinson(id)` 等5个 | 暂无 ❌ |
| 完整报告 | `getFullReport(id, context)` | `getFullReport(id)` ✅ |

**主要差异：**
- THSQuant 不需要 CSRF token，更简单
- THSQuant 参数全用 camelCase（`algoId`、`backTestId`、`beginDate`）
- THSQuant 没有归因分析 API
- THSQuant 的 `backtestloop` 是最高效的轮询方式

---

## 六、Session 管理

Session 存储在 `data/session.json`，有效期 7 天。

```bash
# 检查 session 状态
node list-strategies.js

# 手动刷新 session（需要浏览器）
node browser/auto-login-v6.js
```

Session 包含关键 cookie：
- `quantoken` — 主要认证 token
- `QUANT_RESEARCH_SESSIONID` — 研究环境 session

---

## 七、错误码

| errorcode | 含义 |
|-----------|------|
| 0 | 成功 |
| -1 | 未登录 |
| -777 | 参数设置错误（通常是参数名用了 snake_case 而不是 camelCase）|
| -404 | 资源不存在 |
| 301 | 策略或回测 ID 不合法 |
| 500 | 服务器错误 |
