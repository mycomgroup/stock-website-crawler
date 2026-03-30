# 果仁网策略回测接口设计文档

## 1. 项目概述

基于 `joinquant_strategy` 的架构，为果仁网 (guorn.com) 设计一套程序化的回测接口，实现无需浏览器的自动化策略回测。

### 目标
- 实现果仁网的登录认证
- 支持策略的创建、编辑、保存
- 支持策略回测的执行和结果获取
- 保持与 `joinquant_strategy` 相似的接口风格

### 技术栈
- Node.js + ES Modules
- Playwright (用于会话捕获)
- 原生 fetch API (用于接口调用)

## 2. 目录结构

```
guorn_strategy/
├── .env                    # 环境变量配置
├── package.json            # 项目配置
├── paths.js                # 路径配置
├── load-env.js             # 环境变量加载
├── DESIGN.md               # 设计文档
├── run-skill.js            # 主入口文件
├── browser/
│   ├── capture-session.js  # 会话捕获
│   └── session-manager.js  # 会话管理
├── request/
│   ├── ensure-session.js   # 会话验证
│   ├── guorn-strategy-client.js  # API 客户端
│   └── strategy-runner.js  # 策略运行器
├── data/
│   └── session.json        # 会话数据
└── output/                 # 输出目录
```

## 3. 核心模块设计

### 3.1 会话管理模块

#### browser/capture-session.js
```javascript
// 功能：使用 Playwright 自动登录并捕获会话
// 流程：
// 1. 打开登录页面
// 2. 输入账号密码
// 3. 完成登录
// 4. 保存 cookies 到 session.json
```

**登录流程：**
- 访问 `https://guorn.com/user/login`
- 选择密码登录方式
- 输入手机号和密码
- 点击登录按钮
- 等待登录成功
- 捕获 cookies

**会话数据结构：**
```json
{
  "capturedAt": "2024-01-01T00:00:00.000Z",
  "cookies": [
    {
      "name": "session_id",
      "value": "xxx",
      "domain": ".guorn.com",
      "path": "/"
    }
  ]
}
```

### 3.2 API 客户端模块

#### request/guorn-strategy-client.js
```javascript
// 功能：封装果仁网的 API 调用
// 主要方法：
```

| 方法 | 功能 | API 端点 |
|------|------|----------|
| `login()` | 用户登录 | POST `/user/login` |
| `getStrategyList()` | 获取策略列表 | GET `/user/home` |
| `getStrategy(id)` | 获取策略详情 | GET `/stock?id=xxx` |
| `createStrategy(config)` | 创建策略 | POST `/stock/save` |
| `updateStrategy(id, config)` | 更新策略 | POST `/stock/save` |
| `deleteStrategy(id)` | 删除策略 | POST `/stock/delete` |
| `runBacktest(config)` | 执行回测 | POST `/stock/backtest` |
| `getBacktestResult(id)` | 获取回测结果 | GET `/stock/result?id=xxx` |
| `getBacktestHistory(id)` | 获取历史持仓 | GET `/stock/history?id=xxx` |

### 3.3 策略运行器模块

#### request/strategy-runner.js
```javascript
// 功能：编排策略回测的完整流程
// 流程：
// 1. 验证/刷新会话
// 2. 创建或获取策略
// 3. 配置策略参数
// 4. 执行回测
// 5. 轮询回测状态
// 6. 获取完整报告
// 7. 保存结果
```

## 4. API 接口设计

### 4.1 策略配置结构

```javascript
const strategyConfig = {
  // 基本信息
  name: "策略名称",
  description: "策略描述",

  // 择股设置
  stockPool: {
    type: "system",  // system | custom | static | dynamic
    poolId: "hs300", // 股票池 ID
    stockLimit: 10,  // 股票上限
    rebalanceCycle: 20 // 调仓周期(交易日)
  },

  // 筛选条件
  filters: [
    {
      indicator: "pe_ttm",  // 指标名称
      operator: "between",  // 比较符: >, <, >=, <=, between, in
      value: [0, 30]        // 范围值
    }
  ],

  // 排名条件
  rankings: [
    {
      indicator: "roe",    // 指标名称
      order: "desc",       // 排序: asc, desc
      weight: 1.0          // 权重
    }
  ],

  // 交易模型
  tradingModel: {
    type: 1,  // 1: 定期轮动, 2: 条件触发, 3: 专业模型
    rebalanceCycle: 20,      // 调仓周期
    rebalanceTime: "close",  // 调仓时点: close, open, avg
    maxPosition: 10,         // 最大持仓数
    minPosition: 5,          // 最小建仓仓位
    positionWeight: "equal", // 仓位权重: equal, circulation_market_cap
    holdingRange: [9, 11]    // 个股仓位范围(%)
  },

  // 大盘择时
  marketTiming: {
    enabled: false,
    bullConditions: [],  // 牛市条件
    bearConditions: [],  // 熊市条件
    bearPosition: 0      // 熊市仓位
  },

  // 股指对冲
  hedging: {
    enabled: false,
    benchmark: "hs300",  // 对冲基准
    ratio: 100,          // 对冲比例(%)
    dynamic: false       // 是否动态
  }
};
```

### 4.2 回测配置结构

```javascript
const backtestConfig = {
  strategyId: "xxx",        // 策略 ID
  startTime: "2020-01-01",  // 回测开始时间
  endTime: "2024-01-01",    // 回测结束时间
  benchmark: "hs300",       // 收益基准
  transactionCost: 0.002,   // 交易成本(单边)
  excludePeriods: []        // 排除时间段
};
```

### 4.3 回测结果结构

```javascript
const backtestResult = {
  // 基本信息
  backtestId: "xxx",
  strategyId: "xxx",
  status: "completed",  // running, completed, failed

  // 收益统计
  summary: {
    totalReturn: 0.25,        // 总收益
    annualizedReturn: 0.15,   // 年化收益
    benchmarkReturn: 0.08,    // 基准收益
    excessReturn: 0.07,       // 超额收益
    sharpeRatio: 1.5,         // 夏普比率
    maxDrawdown: -0.12,       // 最大回撤
    volatility: 0.18,         // 收益波动率
    informationRatio: 0.8,    // 信息比率
    turnoverRate: 5.2,        // 年换手率
    winRate: 0.65             // 交易赢率
  },

  // 收益曲线
  equityCurve: [
    {
      date: "2020-01-01",
      strategyReturn: 0.01,
      benchmarkReturn: 0.005,
      position: 1.0
    }
  ],

  // 历史持仓
  positions: [
    {
      date: "2020-01-01",
      stocks: [
        {
          code: "000001.SZ",
          name: "平安银行",
          weight: 0.1,
          action: "buy"  // buy, sell, hold
        }
      ]
    }
  ],

  // 年度收益统计
  yearlyStats: [
    {
      year: 2020,
      return: 0.25,
      benchmarkReturn: 0.15,
      maxDrawdown: -0.08
    }
  ],

  // 月度收益统计
  monthlyStats: [
    {
      month: "2020-01",
      return: 0.03
    }
  ]
};
```

## 5. 使用方式

### 5.1 命令行接口

```bash
# 创建并运行回测
node run-skill.js \
  --name "低PE策略" \
  --start 2020-01-01 \
  --end 2024-01-01 \
  --capital 100000 \
  --config strategy.json

# 仅运行已有策略的回测
node run-skill.js \
  --id "strategy_id" \
  --start 2020-01-01 \
  --end 2024-01-01

# 获取回测结果
node run-skill.js \
  --result "backtest_id"
```

### 5.2 编程接口

```javascript
import { GuornStrategyClient } from './request/guorn-strategy-client.js';
import { runStrategyWorkflow } from './request/strategy-runner.js';

// 方式1: 使用工作流
const result = await runStrategyWorkflow({
  strategyConfig: {
    name: '低PE策略',
    stockPool: { type: 'system', poolId: 'hs300' },
    filters: [{ indicator: 'pe_ttm', operator: '<', value: 30 }],
    rankings: [{ indicator: 'roe', order: 'desc', weight: 1 }],
    tradingModel: { type: 1, rebalanceCycle: 20 }
  },
  backtestConfig: {
    startTime: '2020-01-01',
    endTime: '2024-01-01',
    benchmark: 'hs300',
    transactionCost: 0.002
  }
});

// 方式2: 使用客户端直接调用
const client = new GuornStrategyClient();

// 创建策略
const strategy = await client.createStrategy({
  name: '低PE策略',
  // ... 其他配置
});

// 执行回测
const backtest = await client.runBacktest({
  strategyId: strategy.id,
  startTime: '2020-01-01',
  endTime: '2024-01-01'
});

// 获取结果
const result = await client.getBacktestResult(backtest.id);
```

### 5.3 策略配置文件示例

```json
{
  "name": "低PE高ROE策略",
  "description": "选择PE低于30且ROE排名前10的股票",
  "stockPool": {
    "type": "system",
    "poolId": "hs300",
    "stockLimit": 10,
    "rebalanceCycle": 20
  },
  "filters": [
    {
      "indicator": "pe_ttm",
      "operator": "between",
      "value": [0, 30]
    },
    {
      "indicator": "turnover_rate",
      "operator": ">",
      "value": 1
    }
  ],
  "rankings": [
    {
      "indicator": "roe",
      "order": "desc",
      "weight": 0.6
    },
    {
      "indicator": "revenue_growth",
      "order": "desc",
      "weight": 0.4
    }
  ],
  "tradingModel": {
    "type": 1,
    "rebalanceCycle": 20,
    "rebalanceTime": "close",
    "maxPosition": 10,
    "positionWeight": "equal"
  }
}
```

## 6. 与 joinquant_strategy 的对比

| 特性 | joinquant_strategy | guorn_strategy |
|------|-------------------|----------------|
| 策略定义 | Python 代码 | 可视化配置(JSON) |
| 登录方式 | 账号密码 | 手机号密码 |
| 会话管理 | Cookies + XSRF | Cookies |
| 回测触发 | API 调用 | API 调用 |
| 结果获取 | 轮询 | 轮询 |
| 输出格式 | JSON | JSON |

## 7. 实现步骤

### Phase 1: 基础框架
1. 创建项目结构
2. 实现会话捕获模块
3. 实现 API 客户端基础框架

### Phase 2: 核心功能
1. 实现登录认证
2. 实现策略 CRUD
3. 实现回测执行和轮询

### Phase 3: 完善功能
1. 实现完整报告获取
2. 实现结果导出
3. 添加错误处理和重试机制

### Phase 4: 测试优化
1. 测试各种策略配置
2. 优化性能和稳定性
3. 编写使用文档

## 8. API 限制说明

经过分析，果仁网 (guorn.com) 的 API 有以下限制：

1. **策略保存**: 没有公开的 REST API，需要通过浏览器交互保存策略
2. **回测触发**: 回测功能可能需要通过浏览器交互触发
3. **会话管理**: 使用 Cookies 进行会话管理，有效期约 24 小时

### 已验证的 API

| API | 方法 | 说明 |
|-----|------|------|
| `/user/profile` | GET | 获取用户信息 |
| `/user/privilege` | GET | 获取用户权限 |
| `/stock/pool/all` | GET | 获取股票池列表 |
| `/stock/hotpool/all` | GET | 获取热门股票池 |
| `/stock/meta` | GET | 获取指标和函数元数据 |
| `/stock/rule/all` | GET | 获取规则列表 |

### 建议的实现方式

由于 API 限制，建议采用以下方式：

1. **会话捕获**: 使用 Playwright 登录并保存 Cookies
2. **策略管理**: 通过浏览器自动化创建和编辑策略
3. **回测执行**: 通过浏览器自动化触发回测
4. **结果获取**: 通过 API 获取回测结果

## 9. 注意事项

1. **API 发现**: 需要通过浏览器开发者工具分析实际的 API 端点和参数
2. **会话有效期**: Cookies 可能有过期时间，需要定期刷新
3. **请求频率**: 避免过于频繁的请求，防止被封禁
4. **错误处理**: 网络错误、登录失败、回测失败等情况的处理
5. **数据安全**: 不要在代码中硬编码账号密码，使用环境变量

## 9. 后续扩展

1. 支持批量回测
2. 支持策略组合回测
3. 支持实时选股
4. 支持实盘交易对接
5. 支持策略优化调参
