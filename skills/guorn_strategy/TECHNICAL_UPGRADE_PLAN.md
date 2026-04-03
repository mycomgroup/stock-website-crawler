# 果仁网升级技术方案

## 一、参数获取方案

### 1.1 已发现的 API 端点

基于浏览器抓包分析，已识别以下关键 API：

| API 端点 | 方法 | 功能 | 参数 |
|---------|------|------|------|
| `/stock/meta` | GET | 获取所有可用指标 | `category=stock` |
| `/stock/pool/all` | GET | 获取用户股票池 | `category=stock` |
| `/stock/hotpool/all` | GET | 获取系统股票池 | `category=stock` |
| `/stock/rule/all` | GET | 获取规则列表 | - |
| `/user/profile` | GET | 获取用户信息 | - |
| `/user/privilege` | GET | 获取用户权限 | `filename`, `op` |
| `/frontend/config` | GET | 获取前端配置 | - |

### 1.2 参数提取工具实现

```javascript
// guorn-strategy-client.js 新增方法

/**
 * 获取所有可用指标元数据
 */
async getIndicators() {
  const url = '/stock/meta?category=stock';
  const result = await this.request(url);
  
  if (result.status !== 'ok') {
    throw new Error('Failed to get indicators');
  }
  
  return this.parseIndicators(result.data);
}

/**
 * 解析指标数据
 */
parseIndicators(data) {
  const indicators = {
    functions: [],      // 函数列表
    measures: [],       // 指标列表
    categories: {}      // 按类别分组
  };
  
  // 解析 function 字段
  if (data.function && data.function.measures) {
    data.function.measures.forEach(measure => {
      measure.values.forEach(v => {
        indicators.functions.push({
          name: v.name,
          expr: v.expr,
          desc: v.desc
        });
      });
    });
  }
  
  // 解析 measure 字段（按类别）
  if (data.measure) {
    Object.keys(data.measure).forEach(category => {
      indicators.categories[category] = data.measure[category].map(m => ({
        name: m.name,
        expr: m.expr,
        desc: m.desc
      }));
    });
  }
  
  return indicators;
}

/**
 * 获取所有股票池
 */
async getStockPools() {
  const [pools, hotPools] = await Promise.all([
    this.request('/stock/pool/all?category=stock'),
    this.request('/stock/hotpool/all?category=stock')
  ]);
  
  return {
    userPools: pools.data?.pool_list || [],
    systemPools: hotPools.data?.hot_pool_list || []
  };
}

/**
 * 获取完整的策略配置参数
 */
async getStrategyParameters() {
  const [indicators, stockPools, profile, privilege] = await Promise.all([
    this.getIndicators(),
    this.getStockPools(),
    this.request('/user/profile'),
    this.request('/user/privilege?filename=stockScreen&op=Show')
  ]);
  
  return {
    indicators,
    stockPools,
    profile: profile.data,
    privilege: privilege.data,
    tradingModels: [
      { id: 1, name: '模型Ⅰ--定期轮动' },
      { id: 2, name: '模型Ⅱ--条件触发' }
    ],
    benchmarks: [
      '沪深300', '中证500', '中证800', '中证流通',
      '创业板指数', '上证指数', '上证50', '中证1000'
    ],
    transactionCosts: [
      { value: 0, label: '零' },
      { value: 0.001, label: '千分之一' },
      { value: 0.002, label: '千分之二' },
      { value: 0.0025, label: '千分之二点五' },
      { value: 0.003, label: '千分之三' },
      { value: 0.005, label: '千分之五' },
      { value: 0.008, label: '千分之八' },
      { value: 0.01, label: '千分之十' }
    ]
  };
}
```

### 1.3 参数本地缓存

```javascript
// 创建参数缓存管理器
class ParameterCache {
  constructor(client) {
    this.client = client;
    this.cache = {
      indicators: null,
      stockPools: null,
      lastUpdate: null
    };
    this.cacheFile = path.join(DATA_ROOT, 'parameters-cache.json');
  }
  
  async load() {
    if (fs.existsSync(this.cacheFile)) {
      const data = JSON.parse(fs.readFileSync(this.cacheFile, 'utf8'));
      const age = Date.now() - new Date(data.lastUpdate).getTime();
      
      // 缓存有效期：24小时
      if (age < 24 * 60 * 60 * 1000) {
        this.cache = data;
        return this.cache;
      }
    }
    
    return await this.refresh();
  }
  
  async refresh() {
    const params = await this.client.getStrategyParameters();
    this.cache = {
      ...params,
      lastUpdate: new Date().toISOString()
    };
    
    fs.writeFileSync(this.cacheFile, JSON.stringify(this.cache, null, 2));
    return this.cache;
  }
  
  getIndicator(name) {
    // 从缓存中查找指标
    const all = [
      ...this.cache.indicators.functions,
      ...Object.values(this.cache.indicators.categories).flat()
    ];
    return all.find(i => i.name === name || i.expr === name);
  }
}
```

---

## 二、策略提交与运行 API

### 2.1 策略配置结构（完整版）

```javascript
const strategyConfig = {
  // 基本信息
  name: "策略名称",
  description: "策略描述",
  category: "stock",  // stock, fund, bond, HKstock, BJstock
  
  // 择股设置
  stockPool: {
    type: "system",     // system | custom | static | dynamic
    poolId: "1.P.xxx",  // 股票池ID
    stockLimit: 10,      // 股票上限
    rebalanceCycle: 20   // 调仓周期
  },
  
  // 股票池筛选条件
  poolFilters: {
    indexComponent: "全部",  // 指数成分
    listingBoard: "全部",     // 上市板块
    industry: {
      standard: "申万2014",
      level1: "全部",
      level2: "全部"
    },
    st: "排除ST",           // 包含ST, 排除ST, 仅有ST
    stib: "排除科创板",      // 包含科创板, 排除科创板, 仅有科创板
    filterSuspend: true     // 过滤停牌股票
  },
  
  // 筛选条件
  filters: [
    {
      indicator: "PE",
      operator: "<",
      value: 20,
      enabled: true
    }
  ],
  
  // 排名条件
  rankings: [
    {
      indicator: "总市值",
      order: "asc",  // asc, desc
      weight: 1.0,
      enabled: true
    }
  ],
  
  // 交易模型
  tradingModel: {
    type: 1,  // 1: 定期轮动, 2: 条件触发
    rebalanceTime: "close",  // close, open, avg
    maxPosition: 10,
    minPosition: 5,
    positionRange: [9, 11],  // 个股仓位范围
    positionWeight: "equal",  // equal, circulation_market_cap, total_market_cap
    tradeDate: "每月第一个交易日"
  },
  
  // 大盘择时
  marketTiming: {
    enabled: false,
    type: "none",  // none, template, custom
    conditions: {
      bull: [],
      bear: []
    },
    bearPosition: 0  // 熊市仓位
  },
  
  // 股指对冲
  hedging: {
    enabled: false,
    benchmark: "沪深300",
    ratio: 100,
    dynamic: false
  },
  
  // 回测参数
  backtest: {
    startDate: "2022-01-01",
    endDate: "2025-03-28",
    benchmark: "沪深300",
    transactionCost: 0.002,
    excludePeriods: []
  }
};
```

### 2.2 策略提交 API（推测）

基于网页行为分析，推测以下 API：

```javascript
/**
 * 保存策略
 * POST /stock/save
 */
async saveStrategy(config) {
  const url = '/stock/save';
  const formData = new URLSearchParams();
  
  // 基本信息
  formData.append('name', config.name);
  formData.append('desc', config.description);
  formData.append('category', config.category);
  
  // 股票池
  formData.append('poolid', config.stockPool.poolId);
  formData.append('stocknum', config.stockPool.stockLimit);
  formData.append('cycle', config.stockPool.rebalanceCycle);
  
  // 筛选条件 (JSON 格式)
  formData.append('filters', JSON.stringify(config.filters));
  
  // 排名条件 (JSON 格式)
  formData.append('rankings', JSON.stringify(config.rankings));
  
  // 交易模型
  formData.append('tradetype', config.tradingModel.type);
  formData.append('tradetime', config.tradingModel.rebalanceTime);
  formData.append('maxholding', config.tradingModel.maxPosition);
  
  // 择时和对冲
  if (config.marketTiming.enabled) {
    formData.append('timing', JSON.stringify(config.marketTiming));
  }
  if (config.hedging.enabled) {
    formData.append('hedge', JSON.stringify(config.hedging));
  }
  
  return this.request(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData.toString()
  });
}

/**
 * 运行回测
 * POST /stock/backtest/run
 */
async runBacktest(strategyId, backtestConfig) {
  const url = '/stock/backtest/run';
  const formData = new URLSearchParams();
  
  formData.append('id', strategyId);
  formData.append('startdate', backtestConfig.startDate);
  formData.append('enddate', backtestConfig.endDate);
  formData.append('benchmark', backtestConfig.benchmark);
  formData.append('cost', backtestConfig.transactionCost);
  
  return this.request(url, {
    method: 'POST',
    body: formData.toString()
  });
}

/**
 * 查询回测状态
 * GET /stock/backtest/status
 */
async getBacktestStatus(backtestId) {
  const url = `/stock/backtest/status?id=${backtestId}`;
  return this.request(url);
}

/**
 * 获取回测结果
 * GET /stock/backtest/result
 */
async getBacktestResult(backtestId) {
  const url = `/stock/backtest/result?id=${backtestId}`;
  return this.request(url);
}

/**
 * 获取历史持仓
 * GET /stock/backtest/positions
 */
async getBacktestPositions(backtestId) {
  const url = `/stock/backtest/positions?id=${backtestId}`;
  return this.request(url);
}

/**
 * 获取交易记录
 * GET /stock/backtest/trades
 */
async getBacktestTrades(backtestId) {
  const url = `/stock/backtest/trades?id=${backtestId}`;
  return this.request(url);
}
```

---

## 三、进展评估

### 3.1 已完成

| 功能 | 状态 | 完成度 |
|------|------|--------|
| 会话管理 | ✅ 完成 | 100% |
| API 客户端基础框架 | ✅ 完成 | 100% |
| 指标元数据获取 | ✅ 完成 | 100% |
| 股票池数据获取 | ✅ 完成 | 100% |
| 回测结果提取 | ⚠️ 部分完成 | 70% |
| 策略配置提交 | ❌ 未完成 | 0% |
| 参数本地缓存 | ❌ 未完成 | 0% |
| 完整 API 文档 | ❌ 未完成 | 0% |

### 3.2 技术债务

1. **网络超时问题**
   - 页面加载慢，经常超时
   - 需要：增加重试机制、优化超时策略

2. **API 端点未确认**
   - 保存策略的 API 端点是推测的
   - 需要：抓包确认实际 API

3. **错误处理不足**
   - 缺少详细的错误分类和处理
   - 需要：完善错误处理逻辑

4. **会话过期处理**
   - 会话过期后需要重新登录
   - 需要：自动检测和刷新机制

### 3.3 核心限制

| 限制 | 影响 | 解决方案 |
|------|------|----------|
| 无官方 API 文档 | 需要逆向工程 | 持续抓包分析 |
| 页面动态加载 | 元素定位困难 | 等待策略优化 |
| 网络不稳定 | 自动化失败率高 | 重试+超时优化 |
| 自定义因子不支持 | 部分策略无法实现 | 使用内置因子替代 |

---

## 四、下一步工作计划

### 4.1 短期目标（1-2周）

#### Priority 1: 完善参数提取
```bash
# 任务列表
- [ ] 实现完整的指标解析器
- [ ] 创建指标分类映射表
- [ ] 实现参数缓存机制
- [ ] 创建参数验证工具
```

**实现步骤**:
1. 增强 `getIndicators()` 方法
2. 创建 `ParameterCache` 类
3. 编写参数验证逻辑
4. 生成参数文档

#### Priority 2: 确认提交 API
```bash
# 任务列表
- [ ] 抓取保存策略的完整请求
- [ ] 分析请求参数格式
- [ ] 实现 saveStrategy() 方法
- [ ] 测试策略创建流程
```

**实现步骤**:
1. 使用 headed 模式手动创建策略
2. 记录所有网络请求
3. 分析请求体格式
4. 实现 API 方法

#### Priority 3: 优化网络处理
```bash
# 任务列表
- [ ] 增加重试机制
- [ ] 优化超时配置
- [ ] 实现请求队列
- [ ] 添加网络状态监控
```

### 4.2 中期目标（2-4周）

#### 目标 1: 创建策略模板系统
```javascript
// 定义策略模板
const templates = {
  smallCapGrowth: {
    name: "小市值成长",
    config: { /* 配置 */ }
  },
  dividendValue: {
    name: "高股息价值",
    config: { /* 配置 */ }
  }
};

// 模板管理器
class StrategyTemplate {
  apply(templateName, overrides = {}) {
    const template = templates[templateName];
    return deepMerge(template.config, overrides);
  }
}
```

#### 目标 2: 批量回测功能
```javascript
class BatchBacktestRunner {
  async runBatch(strategies) {
    const results = [];
    for (const strategy of strategies) {
      const result = await this.runStrategy(strategy);
      results.push(result);
    }
    return results;
  }
}
```

#### 目标 3: 结果分析和报告
```javascript
class BacktestAnalyzer {
  analyzeResults(results) {
    return {
      summary: this.generateSummary(results),
      comparison: this.compareStrategies(results),
      recommendations: this.generateRecommendations(results)
    };
  }
}
```

### 4.3 长期目标（1-3月）

#### 目标 1: 完整的 SDK
```javascript
// guorn-sdk
import { GuornSDK } from 'guorn-sdk';

const sdk = new GuornSDK({
  username: '...',
  password: '...'
});

// 创建策略
const strategy = await sdk.strategy.create(config);

// 运行回测
const backtest = await sdk.backtest.run(strategy.id, config);

// 获取结果
const result = await sdk.backtest.getResult(backtest.id);
```

#### 目标 2: CLI 工具
```bash
# 安装
npm install -g guorn-cli

# 使用
guorn login
guorn create --template smallCapGrowth
guorn backtest --id xxx
guorn result --id xxx --export csv
```

#### 目标 3: Web UI
- 可视化策略配置
- 实时回测进度
- 结果图表展示
- 策略对比分析

---

## 五、技术实现细节

### 5.1 完整的 API 客户端类

```javascript
// request/guorn-api-client.js

import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36';

export class GuornAPIClient {
  constructor(options = {}) {
    this.sessionFile = options.sessionFile || SESSION_FILE;
    this.outputRoot = options.outputRoot || OUTPUT_ROOT;
    this.origin = 'https://guorn.com';
    this.session = this.loadSession();
    this.cache = {
      indicators: null,
      stockPools: null,
      lastUpdate: null
    };
  }

  // === 会话管理 ===
  
  loadSession() {
    if (fs.existsSync(this.sessionFile)) {
      return JSON.parse(fs.readFileSync(this.sessionFile, 'utf8'));
    }
    return null;
  }

  get cookies() {
    return this.session?.cookies || [];
  }

  get cookieString() {
    return this.cookies.map(c => `${c.name}=${c.value}`).join('; ');
  }

  // === HTTP 请求 ===
  
  async request(url, options = {}) {
    const fullUrl = url.startsWith('http') ? url : `${this.origin}${url}`;
    
    const headers = {
      'User-Agent': USER_AGENT,
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'Cookie': this.cookieString,
      ...options.headers
    };

    const response = await fetch(fullUrl, {
      method: options.method || 'GET',
      headers,
      body: options.body
    });

    const text = await response.text();
    
    if (!response.ok) {
      throw new Error(`Request failed: ${response.status} ${fullUrl}`);
    }

    try {
      return JSON.parse(text);
    } catch {
      return text;
    }
  }

  // === 参数获取 ===
  
  async getIndicators(forceRefresh = false) {
    if (!forceRefresh && this.cache.indicators) {
      return this.cache.indicators;
    }

    const result = await this.request('/stock/meta?category=stock');
    if (result.status !== 'ok') {
      throw new Error('Failed to get indicators');
    }

    this.cache.indicators = this.parseIndicators(result.data);
    return this.cache.indicators;
  }

  parseIndicators(data) {
    const indicators = {
      functions: [],
      categories: {},
      flat: []
    };

    // 解析函数
    if (data.function?.measures) {
      data.function.measures.forEach(group => {
        group.values.forEach(v => {
          indicators.functions.push({
            type: 'function',
            name: v.name,
            expr: v.expr,
            desc: v.desc
          });
        });
      });
    }

    // 解析指标（按类别）
    if (data.measure) {
      Object.entries(data.measure).forEach(([category, items]) => {
        indicators.categories[category] = items.map(item => ({
          type: 'indicator',
          category,
          name: item.name,
          expr: item.expr,
          desc: item.desc
        }));
      });
    }

    // 扁平化列表
    indicators.flat = [
      ...indicators.functions,
      ...Object.values(indicators.categories).flat()
    ];

    return indicators;
  }

  async getStockPools(forceRefresh = false) {
    if (!forceRefresh && this.cache.stockPools) {
      return this.cache.stockPools;
    }

    const [pools, hotPools] = await Promise.all([
      this.request('/stock/pool/all?category=stock'),
      this.request('/stock/hotpool/all?category=stock')
    ]);

    this.cache.stockPools = {
      userPools: pools.data?.pool_list || [],
      systemPools: hotPools.data?.hot_pool_list || []
    };

    return this.cache.stockPools;
  }

  async getFullParameters() {
    const [indicators, stockPools] = await Promise.all([
      this.getIndicators(),
      this.getStockPools()
    ]);

    return {
      indicators,
      stockPools,
      tradingModels: [
        { id: 1, name: '模型Ⅰ--定期轮动' },
        { id: 2, name: '模型Ⅱ--条件触发' }
      ],
      benchmarks: [
        '沪深300', '中证500', '中证800', '中证流通',
        '创业板指数', '上证指数', '上证50', '中证1000'
      ],
      transactionCosts: [0, 0.001, 0.002, 0.0025, 0.003, 0.005, 0.008, 0.01]
    };
  }

  // === 策略操作 ===
  
  async createStrategy(config) {
    // 需要通过浏览器自动化实现
    throw new Error('Use browser automation for strategy creation');
  }

  async getStrategy(strategyId) {
    return this.request(`/stock?id=${strategyId}`);
  }

  async listStrategies() {
    const html = await this.request('/user/home?page=created');
    // 解析 HTML 提取策略列表
    return this.parseStrategyList(html);
  }

  parseStrategyList(html) {
    const matches = [...html.matchAll(/href="\/stock\?id=([^"]+)"[^>]*>([^<]+)<\/a>/g)];
    return matches.map(m => ({
      id: m[1],
      name: m[2].trim()
    }));
  }

  // === 回测操作 ===
  
  async runBacktest(strategyId, config) {
    // 需要通过浏览器自动化实现
    throw new Error('Use browser automation for backtest');
  }

  async getBacktestResult(backtestId) {
    return this.request(`/stock/backtest/result?id=${backtestId}`);
  }

  // === 工具方法 ===
  
  saveCache() {
    const cacheFile = path.join(this.outputRoot, 'parameter-cache.json');
    const data = {
      ...this.cache,
      lastUpdate: new Date().toISOString()
    };
    fs.writeFileSync(cacheFile, JSON.stringify(data, null, 2));
  }

  writeArtifact(name, data) {
    const file = path.join(this.outputRoot, `${name}-${Date.now()}.json`);
    fs.writeFileSync(file, JSON.stringify(data, null, 2));
    return file;
  }
}
```

### 5.2 工作流程图

```
┌─────────────────────────────────────────────────────────────┐
│                     果仁网策略自动化流程                      │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│  1. 参数获取  │
└──────┬───────┘
       │
       ├─> 获取指标元数据 (/stock/meta)
       ├─> 获取股票池列表 (/stock/pool/all, /stock/hotpool/all)
       ├─> 获取用户权限 (/user/privilege)
       └─> 本地缓存参数

┌──────────────┐
│  2. 策略配置  │
└──────┬───────┘
       │
       ├─> 选择股票池
       ├─> 设置筛选条件
       ├─> 设置排名条件
       ├─> 配置交易模型
       └─> 设置回测参数

┌──────────────┐
│  3. 策略提交  │
└──────┬───────┘
       │
       ├─> 验证参数有效性
       ├─> 序列化配置
       ├─> POST 提交
       └─> 获取策略 ID

┌──────────────┐
│  4. 运行回测  │
└──────┬───────┘
       │
       ├─> 触发回测
       ├─> 轮询状态
       └─> 等待完成

┌──────────────┐
│  5. 结果获取  │
└──────┬───────┘
       │
       ├─> 获取统计指标
       ├─> 获取收益曲线
       ├─> 获取持仓记录
       └─> 生成报告
```

---

## 六、风险与应对

### 6.1 技术风险

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|----------|
| API 变更 | 中 | 高 | 版本管理、兼容性检测 |
| 反爬虫限制 | 低 | 高 | 降低频率、模拟人类行为 |
| 会话过期 | 高 | 中 | 自动刷新机制 |
| 网络不稳定 | 高 | 中 | 重试机制、离线缓存 |

### 6.2 业务风险

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|----------|
| 功能限制 | 高 | 高 | 手动+自动化混合 |
| 数据准确性 | 低 | 高 | 结果验证 |
| 账号安全 | 中 | 高 | 敏感信息保护 |

---

## 七、资源需求

### 7.1 开发资源

| 角色 | 工作内容 | 时间 |
|------|---------|------|
| 后端开发 | API 客户端开发 | 2 周 |
| 自动化开发 | 浏览器自动化 | 2 周 |
| 测试 | 功能测试 | 1 周 |
| 文档 | 技术文档编写 | 1 周 |

### 7.2 技术栈

- **语言**: Node.js + ES Modules
- **自动化**: Playwright
- **HTTP**: 原生 fetch
- **数据存储**: JSON 文件
- **CLI**: minimist

---

## 八、里程碑

### Milestone 1: 参数提取完成 (Week 1)
- [x] 指标元数据解析
- [x] 股票池数据获取
- [ ] 参数缓存机制
- [ ] 参数验证工具

### Milestone 2: API 客户端完成 (Week 2)
- [ ] 完整的 API 方法
- [ ] 错误处理
- [ ] 重试机制
- [ ] 日志系统

### Milestone 3: 自动化流程完成 (Week 3)
- [ ] 策略创建自动化
- [ ] 回测执行自动化
- [ ] 结果提取自动化

### Milestone 4: 文档和测试 (Week 4)
- [ ] API 文档
- [ ] 使用文档
- [ ] 测试用例
- [ ] 示例代码

---

## 九、附录

### 9.1 相关文件

```
guorn_strategy/
├── request/
│   ├── guorn-api-client.js    # API 客户端
│   ├── guorn-strategy-client.js # 旧客户端
│   └── strategy-runner.js     # 策略运行器
├── browser/
│   ├── capture-session.js     # 会话捕获
│   └── run-all-strategies.js  # 批量运行
├── data/
│   ├── session.json          # 会话数据
│   ├── api-calls.json        # API 调用记录
│   └── parameters-cache.json # 参数缓存
├── output/
│   ├── results/              # 回测结果
│   └── logs/                 # 运行日志
└── docs/
    ├── API.md                # API 文档
    ├── PARAMETERS.md         # 参数文档
    └── EXAMPLES.md           # 示例文档
```

### 9.2 参考资料

- 果仁网帮助中心: https://guorn.com/stock/help
- 果仁网论坛: https://guorn.com/forum
- Playwright 文档: https://playwright.dev
- JoinQuant API 设计: `skills/joinquant_strategy/`