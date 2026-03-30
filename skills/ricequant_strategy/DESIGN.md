# RiceQuant 策略回测系统设计文档

## 1. 概述

基于 `joinquant_strategy` 的架构，为 RiceQuant 实现在线回测的程序化调用接口。

**核心特性：**
- 无需浏览器，纯程序调用
- 接口与 `joinquant_strategy` 保持一致
- 支持完整的回测生命周期管理
- 支持归因分析、交易记录、持仓查询等高级功能

---

## 2. 账号信息

```yaml
username: "13311390323"
password: "3228552"
platform: ricequant.com
```

---

## 3. 目录结构

```
skills/ricequant_strategy/
├── .env                          # 环境变量（账号密码）
├── paths.js                      # 路径配置
├── load-env.js                   # 环境变量加载
├── package.json                  # 依赖配置
├── run-skill.js                  # 主入口：运行策略回测
├── list-strategies.js            # 列出所有策略
├── fetch-report.js               # 获取回测报告
├── browser/
│   ├── capture-session.js        # 浏览器会话捕获
│   └── session-manager.js        # 会话管理
└── request/
    ├── ricequant-client.js       # 核心客户端类
    ├── ensure-session.js         # 会话确保
    └── strategy-runner.js        # 策略运行器
```

---

## 4. 接口设计

### 4.1 核心类：RiceQuantClient

参考 `JoinQuantStrategyClient` 的接口设计：

```javascript
class RiceQuantClient {
  constructor(options)
  
  // 策略管理
  async listStrategies()           // 列出策略
  async getStrategyContext(strategyId)  // 获取策略上下文（CSRF Token等）
  async saveStrategy(strategyId, name, code, context)  // 保存策略代码
  
  // 回测管理
  async runBacktest(strategyId, code, config, context)  // 运行回测
  async getBacktestResult(backtestId, context)          // 获取回测结果
  async getBacktestStats(backtestId, context)           // 获取回测统计
  async getBacktestList(strategyId)                     // 获取回测列表
  
  // 交易与持仓
  async getTransactions(backtestId)  // 获取交易记录
  async getPositions(backtestId)     // 获取持仓信息
  async getLogs(backtestId)          // 获取回测日志
  
  // 归因分析
  async getAttributionContext(backtestId)
  async getAttributionReturnOverview(backtestId, context)
  async getAttributionRiskIndicator(backtestId, context)
  
  // 完整报告
  async getFullReport(backtestId, context)
  
  // 工具方法
  writeArtifact(baseName, data, extension)
}
```

### 4.2 会话管理

```javascript
// browser/session-manager.js
async function ensureRiceQuantSession(credentials)
async function captureRiceQuantSession(credentials)

// request/ensure-session.js  
async function ensureRiceQuantSession(options)
```

### 4.3 策略运行器

```javascript
// request/strategy-runner.js
async function runStrategyWorkflow(options) {
  // options: {
  //   strategyId,      // RiceQuant策略ID
  //   codeFilePath,    // 本地策略代码文件路径
  //   startTime,       // 开始日期 YYYY-MM-DD
  //   endTime,         // 结束日期 YYYY-MM-DD
  //   baseCapital,     // 初始资金（默认100000）
  //   frequency,       // 频率：day/minute（默认day）
  //   benchmark        // 基准指数（默认000300.XSHG）
  // }
}
```

---

## 5. CLI 命令

### 5.1 运行回测

```bash
node run-skill.js --id <strategyId> --file <codePath> [options]

Options:
  --id <id>          RiceQuant策略ID
  --file <path>      策略代码文件路径 (.py)
  --start <date>     回测开始日期 (默认: 2023-01-01)
  --end <date>       回测结束日期 (默认: 2023-12-31)
  --capital <num>    初始资金 (默认: 100000)
  --freq <freq>      回测频率: day/minute (默认: day)
  --benchmark <code> 基准指数 (默认: 000300.XSHG)
  --headed           使用有头浏览器（调试用）
```

### 5.2 列出策略

```bash
node list-strategies.js
```

### 5.3 获取回测报告

```bash
node fetch-report.js --id <backtestId> [--strategy <strategyId>]
```

---

## 6. API 端点分析（待验证）

基于 RiceQuant 网站架构推测：

```
Base URL: https://www.ricequant.com

# 认证
POST /api/v2/auth/login           # 登录

# 策略管理
GET  /api/v2/strategy/list        # 获取策略列表
GET  /strategy/{id}/edit          # 策略编辑页（提取Token）
POST /api/v2/strategy/save        # 保存策略

# 回测
POST /api/v2/backtest/run         # 运行回测
GET  /api/v2/backtest/{id}        # 获取回测结果
GET  /api/v2/backtest/{id}/stats  # 回测统计
GET  /api/v2/backtest/list        # 回测列表

# 交易与持仓
GET  /api/v2/backtest/{id}/transactions  # 交易记录
GET  /api/v2/backtest/{id}/positions     # 持仓信息
GET  /api/v2/backtest/{id}/logs          # 回测日志

# 归因分析
GET  /api/v2/backtest/{id}/attribution/return    # 收益归因
GET  /api/v2/backtest/{id}/attribution/risk      # 风险归因
```

---

## 7. 实现步骤

### Phase 1: 基础框架（预计2-3天）
1. [ ] 创建项目结构
2. [ ] 实现浏览器会话捕获（基于 Playwright）
3. [ ] 实现基础 HTTP 客户端
4. [ ] 实现登录与会话管理

### Phase 2: 策略管理（预计1-2天）
1. [ ] 策略列表接口
2. [ ] 策略上下文提取（CSRF Token）
3. [ ] 策略代码保存接口

### Phase 3: 回测核心（预计2-3天）
1. [ ] 回测启动接口
2. [ ] 回测结果轮询
3. [ ] 回测统计数据获取

### Phase 4: 报告功能（预计1-2天）
1. [ ] 交易记录获取
2. [ ] 持仓信息获取
3. [ ] 归因分析接口
4. [ ] 完整报告生成

### Phase 5: CLI 工具（预计1天）
1. [ ] run-skill.js 实现
2. [ ] list-strategies.js 实现
3. [ ] fetch-report.js 实现
4. [ ] 测试与文档

---

## 8. 关键技术点

### 8.1 认证机制
- RiceQuant 使用 Cookie + CSRF Token
- 会话有效期需要验证
- 可能需要处理验证码（如有）

### 8.2 API 差异
RiceQuant 与 JoinQuant 的主要差异：
- Token 提取方式不同
- 回测参数结构可能不同
- 响应数据结构需要适配

### 8.3 错误处理
- 网络超时重试
- 会话过期自动刷新
- 回测失败状态处理

---

## 9. 文件输出

所有输出文件保存到 `output/` 目录：
- `backtest-full-{backtestId}-{timestamp}.json`
- `strategy-list-{timestamp}.json`
- `session-{timestamp}.json`（调试用）

---

## 10. 环境变量配置

```bash
# .env
RICEQUANT_USERNAME=13311390323
RICEQUANT_PASSWORD=3228552
RICEQUANT_OUTPUT_ROOT=./output
```

---

## 11. 注意事项

1. **频率限制**：需要遵守 RiceQuant 的 API 调用频率限制
2. **并发限制**：同一账号同时只能运行有限数量的回测
3. **数据安全**：账号密码存储在本地 .env 文件，不要提交到 Git
4. **兼容性**：RiceQuant API 可能更新，需要定期维护

---

## 12. 与 JoinQuant 的接口对比

| 功能 | JoinQuant | RiceQuant | 备注 |
|------|-----------|-----------|------|
| 策略ID | algorithmId | strategyId | 命名不同 |
| 回测ID | backtestId | backtestId | 相同 |
| 基准指数 | 默认沪深300 | 默认000300.XSHG | 代码格式一致 |
| 频率 | day/minute | day/minute | 相同 |
| 归因分析 | 完整支持 | 需要验证 | 推测支持 |

---

## 13. 下一步行动

1. 确认本设计文档
2. 开始 Phase 1 实现
3. 在实际账号上验证 API 端点
4. 根据实际 API 调整接口设计
