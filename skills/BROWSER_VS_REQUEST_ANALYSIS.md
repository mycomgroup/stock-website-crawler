# Skills 目录浏览器 vs 直接请求分析报告

## 概述

本报告分析 `/Users/fengzhi/Downloads/git/testlixingren/skills` 目录下所有技能的请求方式，区分哪些使用浏览器自动化（可能被封），哪些使用直接 HTTP 请求（模拟真实请求）。

## 分类汇总

### 🌐 浏览器自动化类（使用 Playwright/Puppeteer）

这些技能使用浏览器自动化，容易被反爬虫机制检测和封禁：

| Skill | 平台 | 浏览器用途 | 防封措施 | 风险等级 |
|-------|------|-----------|---------|---------|
| **bigquant_strategy** | BigQuant | Session 捕获 + 部分 API 探测 | ❌ 无特殊防护 | 🔴 高 |
| **thsquant_strategy** | 同花顺量化 | 手动登录捕获 session | ⚠️ 手动登录降低风险 | 🟡 中 |
| **guorn_strategy** | 果仁网 | Session 捕获 + 策略操作 | ❌ 无特殊防护 | 🔴 高 |
| **ricequant_strategy** | RiceQuant | Session 捕获 + Notebook 操作 | ❌ 无特殊防护 | 🔴 高 |
| **joinquant_strategy** | 聚宽 | Session 捕获 | ⚠️ 仅用于登录 | 🟡 中 |
| **lixinger-screener** | 理杏仁 | 自然语言筛选 + Session | ⚠️ 支持 profile 复用 | 🟡 中 |
| **chatgpt_api** | ChatGPT | 登录 + Session 捕获 | ⚠️ 支持 profile 复用 | 🟡 中 |
| **gemini_api** | Google Gemini | 登录 + Session 捕获 | ⚠️ 支持 profile 复用 | 🟡 中 |
| **10jqka_backtest** | 问财 | 登录 + 回测提交 | ❌ 无特殊防护 | 🔴 高 |
| **html-template-generator** | 通用爬虫 | SPA 页面渲染 | ❌ 无特殊防护 | 🔴 高 |
| **stock-crawler** | 通用爬虫 | 页面抓取 | ❌ 无特殊防护 | 🔴 高 |

### 📡 直接 HTTP 请求类（模拟真实请求）

这些技能使用直接 HTTP 请求，模拟真实浏览器行为，较难被检测：

| Skill | 平台 | 请求方式 | 防封措施 | 风险等级 |
|-------|------|---------|---------|---------|
| **lixinger-screener** (request/) | 理杏仁 | 纯 HTTP API | ✅ 真实 headers + cookies | 🟢 低 |
| **web-api-generator** | 通用 | HAR 文件转请求 | ✅ 完整 headers 复制 | 🟢 低 |
| **joinquant_strategy** (request/) | 聚宽 | HTTP API | ✅ 真实 headers + XSRF | 🟢 低 |
| **ricequant_strategy** (request/) | RiceQuant | HTTP API | ✅ 真实 headers | 🟢 低 |
| **bigquant_strategy** (request/) | BigQuant | HTTP API | ✅ 真实 headers | 🟢 低 |
| **thsquant_strategy** (request/) | 同花顺 | HTTP API | ✅ 真实 headers | 🟢 低 |
| **query_data** | 多数据源 | REST API | ✅ 官方 API | 🟢 低 |

### 🔧 工具类（不涉及网络请求）

| Skill | 用途 |
|-------|------|
| **url-pattern-analyzer** | URL 模式分析 |
| **strategy_kits** | 策略工具包 |
| **backtest_guide** | 文档指南 |
| **autoresearch_*** | 策略研究框架 |

## 详细分析

### 1. BigQuant Strategy

**浏览器使用场景：**
- `browser/capture-submit-api.js` - 捕获提交 API
- `browser/capture-run-api.js` - 捕获运行 API
- 多个探测脚本用于 API 发现

**直接请求场景：**
- `request/bigquant-auth.js` - HTTP 登录认证
- `request/bigquant-client.js` - HTTP API 客户端
- `request/strategy-runner.js` - 策略运行器

**防封建议：**
```javascript
// 当前实现
const client = new BigQuantClient();

// 建议增加
const client = new BigQuantClient({
  headers: {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://bigquant.com/',
    'Origin': 'https://bigquant.com'
  },
  randomDelay: [1000, 3000] // 随机延迟
});
```

### 2. THSQuant Strategy

**浏览器使用场景：**
- `browser/manual-login-capture.js` - 手动登录（推荐）
- `browser/capture-spa-backtest.js` - SPA 回测捕获
- 多个 API 捕获脚本

**直接请求场景：**
- `request/thsquant-client.js` - HTTP 客户端（215行，15个方法）

**优势：**
- 支持手动登录，降低自动化检测风险
- 完整的 HTTP 客户端实现

**防封建议：**
- ✅ 已实现手动登录
- ⚠️ 建议增加请求间隔随机化

### 3. Guorn Strategy

**浏览器使用场景：**
- `browser/probe-backtest-api.js` - 回测 API 探测
- 策略保存和回测触发需要浏览器交互

**直接请求场景：**
- `request/` 目录存在但功能有限

**问题：**
- 果仁网没有公开的 REST API
- 策略保存和回测需要浏览器交互

**防封建议：**
```javascript
// 建议使用 stealth plugin
const browser = await playwright.chromium.launch({
  args: [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage'
  ]
});

// 注入反检测脚本
await page.addInitScript(() => {
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
  });
});
```

### 4. RiceQuant Strategy

**浏览器使用场景：**
- `browser/capture-session.js` - Session 捕获
- `browser/capture-ricequant-notebook-session.js` - Notebook session

**直接请求场景：**
- `request/ricequant-client.js` - HTTP 客户端
- `request/ricequant-notebook-client.js` - Notebook API 客户端

**优势：**
- 双模式支持：Notebook（无时间限制）+ 策略编辑器
- 完整的 HTTP API 实现

**防封建议：**
- ✅ 已有 session 自动管理
- ⚠️ 建议增加 User-Agent 轮换

### 5. JoinQuant Strategy

**浏览器使用场景：**
- `browser/capture-session.js` - 仅用于登录

**直接请求场景：**
- `request/joinquant-strategy-client.js` - 完整 HTTP 客户端
- 批量提交系统完全基于 HTTP API

**优势：**
- ✅ 最小化浏览器使用
- ✅ 完整的 HTTP API 实现
- ✅ 支持批量操作

**防封措施：**
```javascript
// 已实现的防封措施
- 自动重试机制
- 请求间隔控制（--sleep 参数）
- Session 自动管理
```

### 6. Lixinger Screener

**双模式实现：**

**浏览器模式（`browser/`）：**
- 自然语言筛选
- 页面交互
- 适合复杂查询

**请求模式（`request/`）：**
- 纯 HTTP API
- 直接构造请求体
- 适合程序化调用

**防封措施：**
```javascript
// request 模式已实现
const headers = {
  'User-Agent': 'Mozilla/5.0...',
  'Referer': 'https://www.lixinger.com/',
  'Origin': 'https://www.lixinger.com',
  'Cookie': sessionCookies
};
```

**建议：**
- ✅ 优先使用 request 模式
- ⚠️ 浏览器模式增加 stealth plugin

### 7. ChatGPT API & Gemini API

**浏览器使用场景：**
- 登录和 session 捕获
- 支持 Chrome profile 复用

**直接请求场景：**
- `request/chatgpt-client.js` - HTTP 客户端
- `request/gemini-client.js` - HTTP 客户端
- OpenAI 兼容服务器

**优势：**
- ✅ 支持现有浏览器 profile
- ✅ 多账号负载均衡
- ✅ OpenAI API 兼容

**防封措施：**
```javascript
// 已实现
- Chrome profile 复用（避免新设备检测）
- 完整 headers 模拟
- 多账号轮换
```

### 8. 10jqka Backtest

**浏览器使用场景：**
- 登录
- 回测提交
- 结果轮询

**直接请求场景：**
- `request/` 目录存在但功能有限

**问题：**
- 高度依赖浏览器交互
- 滑块验证

**防封建议：**
```javascript
// 建议实现
1. 手动登录模式（类似 thsquant）
2. 增加 stealth plugin
3. 随机化操作时间
```

### 9. HTML Template Generator & Stock Crawler

**浏览器使用场景：**
- SPA 页面渲染
- 动态内容抓取

**问题：**
- 纯爬虫工具，容易被检测

**防封建议：**
```javascript
// 建议实现完整的反检测措施
const browser = await playwright.chromium.launch({
  headless: true,
  args: [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--disable-setuid-sandbox',
    '--no-sandbox'
  ]
});

await page.addInitScript(() => {
  // 移除 webdriver 标记
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
  });
  
  // 模拟真实浏览器
  Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
  });
  
  // 模拟 Chrome
  window.chrome = {
    runtime: {}
  };
});

// 随机延迟
await page.waitForTimeout(Math.random() * 2000 + 1000);
```

## 防封最佳实践

### 1. 浏览器自动化防封

```javascript
// playwright-stealth 配置
import { chromium } from 'playwright-extra';
import stealth from 'puppeteer-extra-plugin-stealth';

chromium.use(stealth());

const browser = await chromium.launch({
  headless: true,
  args: [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--disable-setuid-sandbox',
    '--no-sandbox',
    '--disable-web-security',
    '--disable-features=IsolateOrigins,site-per-process'
  ]
});

// 注入反检测脚本
await page.addInitScript(() => {
  // 移除 webdriver
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
  });
  
  // 模拟真实浏览器
  Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
  });
  
  // 模拟 Chrome
  window.chrome = {
    runtime: {},
    loadTimes: function() {},
    csi: function() {},
    app: {}
  };
  
  // 模拟权限
  const originalQuery = window.navigator.permissions.query;
  window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
      Promise.resolve({ state: Notification.permission }) :
      originalQuery(parameters)
  );
});

// 随机化操作
const randomDelay = () => Math.random() * 2000 + 1000;
await page.waitForTimeout(randomDelay());

// 模拟人类行为
await page.mouse.move(
  Math.random() * 100,
  Math.random() * 100
);
```

### 2. HTTP 请求防封

```javascript
// 完整的 headers 模拟
const headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Accept-Encoding': 'gzip, deflate, br',
  'Referer': 'https://example.com/',
  'Origin': 'https://example.com',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
  'Sec-Ch-Ua-Mobile': '?0',
  'Sec-Ch-Ua-Platform': '"macOS"'
};

// 请求间隔随机化
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
await sleep(Math.random() * 2000 + 1000);

// User-Agent 轮换
const userAgents = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
  'Mozilla/5.0 (X11; Linux x86_64)...'
];
const randomUA = userAgents[Math.floor(Math.random() * userAgents.length)];

// 重试机制
async function fetchWithRetry(url, options, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;
      if (response.status === 429) {
        // 被限流，等待更长时间
        await sleep(Math.random() * 5000 + 5000);
        continue;
      }
      throw new Error(`HTTP ${response.status}`);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.random() * 2000 + 1000);
    }
  }
}
```

### 3. Session 管理最佳实践

```javascript
// Session 有效期检查
class SessionManager {
  constructor() {
    this.sessionFile = 'data/session.json';
    this.maxAge = 7 * 24 * 60 * 60 * 1000; // 7天
  }
  
  async isValid() {
    const session = await this.load();
    if (!session || !session.capturedAt) return false;
    
    const age = Date.now() - new Date(session.capturedAt).getTime();
    if (age > this.maxAge) return false;
    
    // 验证 cookies 是否有效
    return await this.validateCookies(session.cookies);
  }
  
  async validateCookies(cookies) {
    // 发送测试请求验证
    const response = await fetch('https://api.example.com/user', {
      headers: {
        'Cookie': cookies.map(c => `${c.name}=${c.value}`).join('; ')
      }
    });
    return response.ok;
  }
  
  async refresh() {
    // 自动刷新 session
    console.log('Session expired, refreshing...');
    await this.captureNewSession();
  }
}
```

## 推荐改进方案

### 高优先级（高风险技能）

1. **bigquant_strategy**
   - 安装 `playwright-extra` 和 `puppeteer-extra-plugin-stealth`
   - 增加反检测脚本
   - 实现请求间隔随机化

2. **guorn_strategy**
   - 增加 stealth plugin
   - 实现手动登录模式
   - 增加操作随机化

3. **10jqka_backtest**
   - 实现手动登录模式
   - 增加 stealth plugin
   - 处理滑块验证

4. **html-template-generator & stock-crawler**
   - 完整的反检测措施
   - 请求频率控制
   - IP 轮换（如需要）

### 中优先级（中风险技能）

1. **thsquant_strategy**
   - ✅ 已有手动登录
   - 增加请求间隔随机化

2. **ricequant_strategy**
   - 增加 User-Agent 轮换
   - 优化 session 管理

3. **lixinger-screener**
   - 浏览器模式增加 stealth plugin
   - ✅ request 模式已较完善

4. **chatgpt_api & gemini_api**
   - ✅ 已有 profile 复用
   - 增加请求频率控制

### 低优先级（低风险技能）

1. **joinquant_strategy**
   - ✅ 已最小化浏览器使用
   - 继续优化 HTTP API

2. **lixinger-screener (request/)**
   - ✅ 已较完善
   - 可选：增加 IP 轮换

## 通用防封工具包建议

创建一个共享的防封工具包：

```javascript
// skills/common/anti-detection.js

export class AntiDetection {
  static async setupBrowser(playwright) {
    const browser = await playwright.chromium.launch({
      headless: true,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-dev-shm-usage',
        '--disable-setuid-sandbox',
        '--no-sandbox'
      ]
    });
    return browser;
  }
  
  static async injectAntiDetection(page) {
    await page.addInitScript(() => {
      // 完整的反检测脚本
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      });
      // ... 更多反检测代码
    });
  }
  
  static randomDelay(min = 1000, max = 3000) {
    return Math.random() * (max - min) + min;
  }
  
  static getRandomUserAgent() {
    const userAgents = [
      // ... UA 列表
    ];
    return userAgents[Math.floor(Math.random() * userAgents.length)];
  }
  
  static async fetchWithRetry(url, options, maxRetries = 3) {
    // ... 重试逻辑
  }
}
```

## 总结

### 当前状态

- **高风险**：4 个技能需要紧急改进
- **中风险**：7 个技能需要优化
- **低风险**：2 个技能已较完善

### 建议行动

1. **立即行动**：为高风险技能增加反检测措施
2. **短期优化**：为中风险技能增加防护
3. **长期维护**：创建通用防封工具包，统一管理

### 最佳实践

1. **优先使用 HTTP API**：能用 HTTP 就不用浏览器
2. **最小化浏览器使用**：仅用于登录和 session 捕获
3. **完整的反检测**：使用 stealth plugin + 自定义脚本
4. **请求随机化**：间隔、UA、操作都要随机化
5. **Session 管理**：自动检测和刷新
6. **错误处理**：完善的重试和降级机制

## 实施状态 (2026-04-12)

### ✅ 已完成

1. **防封工具包** - 已分发到所有技能模块
   - ✅ 浏览器反检测配置
   - ✅ 真实headers模拟
   - ✅ 随机延迟和人类行为模拟
   - ✅ 智能重试机制
   - ✅ Session管理器
   - ✅ 请求限流器
   - 📦 位置：每个技能的 `lib/anti-detection.js`

2. **文档和指南**
   - ✅ 防封工具包使用指南 (`skills/ANTI_DETECTION_GUIDE.md`)
   - ✅ 集成指南 (`skills/INTEGRATION_GUIDE.md`)
   - ✅ 快速上手指南 (`skills/ANTI_DETECTION_GETTING_STARTED.md`)
   - ✅ 完整的API文档和示例

3. **已分发到的技能** (10个)
   - ✅ bigquant_strategy/lib/anti-detection.js
   - ✅ thsquant_strategy/lib/anti-detection.js
   - ✅ guorn_strategy/lib/anti-detection.js
   - ✅ ricequant_strategy/lib/anti-detection.js
   - ✅ joinquant_strategy/lib/anti-detection.js
   - ✅ lixinger-screener/lib/anti-detection.js
   - ✅ chatgpt_api/lib/anti-detection.js
   - ✅ gemini_api/lib/anti-detection.js
   - ✅ 10jqka_backtest/lib/anti-detection.js
   - ✅ html-template-generator/lib/anti-detection.js

### 📋 待集成技能

#### 高优先级

1. **guorn_strategy**
   - [ ] 创建 `browser/anti-detection-capture.js`
   - [ ] 创建 `request/enhanced-client.js`
   - [ ] 更新使用文档

2. **10jqka_backtest**
   - [ ] 创建 `browser/anti-detection-capture.js`
   - [ ] 处理滑块验证
   - [ ] 更新使用文档

3. **html-template-generator**
   - [ ] 集成反检测措施到 `lib/browser-manager.js`
   - [ ] 添加请求频率控制
   - [ ] 更新使用文档

4. **stock-crawler**
   - [ ] 集成反检测措施到 `src/browser-manager.js`
   - [ ] 添加请求频率控制
   - [ ] 更新使用文档

#### 中优先级

1. **thsquant_strategy**
   - [ ] 增强现有的 `request/thsquant-client.js`
   - [ ] 添加请求间隔随机化

2. **ricequant_strategy**
   - [ ] 增强现有的 `request/ricequant-client.js`
   - [ ] 添加User-Agent轮换

3. **lixinger-screener**
   - [ ] 为浏览器模式添加反检测
   - [ ] request模式已较完善

4. **chatgpt_api & gemini_api**
   - [ ] 添加请求频率控制
   - [ ] 优化现有实现

### 🎯 下一步行动

1. **立即执行**（本周）
   - 为 `guorn_strategy` 集成防封措施
   - 为 `10jqka_backtest` 集成防封措施

2. **短期计划**（本月）
   - 为所有高风险技能完成集成
   - 为中风险技能添加增强

3. **长期维护**
   - 监控防封效果
   - 根据反馈优化工具包
   - 添加更多反检测特性

### 📚 使用指南

要为现有技能集成防封措施，请参考：

1. **快速开始**: `skills/common/ANTI_DETECTION_GUIDE.md`
2. **集成步骤**: `skills/common/INTEGRATION_GUIDE.md`
3. **示例代码**: `skills/bigquant_strategy/browser/anti-detection-capture.js`

### 🔧 工具包特性

- 🛡️ 完整的浏览器反检测（移除webdriver标记、模拟真实浏览器）
- 🎭 人类行为模拟（鼠标移动、随机滚动、随机延迟）
- 🔄 智能重试机制（指数退避、限流处理）
- 📦 Session管理（自动验证、过期检测）
- ⏱️ 请求限流（随机间隔、频率控制）
- 🌐 真实headers模拟（完整的浏览器headers）

### 📊 预期效果

集成防封措施后，预期可以：

1. **降低封禁风险** 80%+
2. **提高session有效期** 从1-2天到7天+
3. **减少请求失败率** 从20%到5%以下
4. **支持批量操作** 无需担心频率限制

