# 防封措施集成指南

本指南说明如何将防封工具包集成到现有的技能中。

## 快速集成步骤

### 步骤1：安装依赖

确保你的项目已安装 Playwright：

```bash
npm install playwright
# 或
pnpm add playwright
```

### 步骤2：导入工具包

```javascript
import { 
  AntiDetection, 
  SessionManager, 
  RateLimiter 
} from '../common/anti-detection.js';
```

### 步骤3：选择集成方式

根据你的技能类型选择合适的集成方式：

## 集成方式A：浏览器自动化

适用于需要浏览器交互的技能（如登录、页面操作等）。

### 基础集成

```javascript
// 原有代码
import { chromium } from 'playwright';

async function captureSession() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  // ... 其他代码
}
```

```javascript
// 集成防封措施后
import { AntiDetection, SessionManager } from '../common/anti-detection.js';

async function captureSession() {
  // 使用反检测浏览器
  const browser = await AntiDetection.setupBrowser({
    headless: false
  });
  
  const page = await browser.newPage();
  
  // 注入反检测脚本
  await AntiDetection.injectAntiDetection(page);
  
  // 设置真实headers
  await AntiDetection.setRealisticHeaders(page, {
    'Referer': 'https://your-site.com/',
    'Origin': 'https://your-site.com'
  });
  
  // 访问页面
  await page.goto('https://your-site.com');
  
  // 模拟人类行为
  await AntiDetection.simulateHumanBehavior(page);
  
  // ... 其他代码
}
```

### 完整示例：Session捕获

```javascript
import { AntiDetection, SessionManager } from '../common/anti-detection.js';
import path from 'path';

const SESSION_FILE = path.join(__dirname, '../data/session.json');

async function captureSessionWithAntiDetection() {
  const sessionManager = new SessionManager(SESSION_FILE, {
    maxAge: 7 * 24 * 60 * 60 * 1000,
    validateUrl: 'https://your-site.com/api/user'
  });
  
  // 检查现有session
  if (await sessionManager.isValid()) {
    console.log('✅ Existing session is valid');
    return await sessionManager.load();
  }
  
  // 创建反检测浏览器
  const browser = await AntiDetection.setupBrowser({
    headless: false
  });
  
  try {
    const page = await browser.newPage();
    
    // 注入反检测
    await AntiDetection.injectAntiDetection(page);
    await AntiDetection.setRealisticHeaders(page);
    
    // 访问登录页
    await page.goto('https://your-site.com/login');
    
    // 模拟人类行为
    await AntiDetection.simulateHumanBehavior(page);
    
    // 等待用户登录
    console.log('Please login manually...');
    await page.waitForURL('**/dashboard', { timeout: 300000 });
    
    // 捕获session
    const cookies = await page.context().cookies();
    const session = {
      cookies,
      userAgent: await page.evaluate(() => navigator.userAgent),
      capturedAt: new Date().toISOString()
    };
    
    // 保存session
    await sessionManager.save(session);
    
    return session;
  } finally {
    await browser.close();
  }
}

export { captureSessionWithAntiDetection };
```

## 集成方式B：HTTP请求

适用于使用HTTP API的技能。

### 基础集成

```javascript
// 原有代码
async function fetchData() {
  const response = await fetch('https://api.example.com/data', {
    headers: {
      'Cookie': 'session=xxx'
    }
  });
  return await response.json();
}
```

```javascript
// 集成防封措施后
import { AntiDetection, RateLimiter } from '../common/anti-detection.js';

const limiter = new RateLimiter({ minDelay: 1000, maxDelay: 3000 });

async function fetchData() {
  // 限流
  await limiter.wait();
  
  // 创建真实headers
  const headers = AntiDetection.createRealisticHeaders({
    'Referer': 'https://api.example.com/',
    'Origin': 'https://api.example.com',
    'Cookie': 'session=xxx'
  });
  
  // 带重试的请求
  const response = await AntiDetection.fetchWithRetry(
    () => fetch('https://api.example.com/data', { headers }),
    {
      maxRetries: 3,
      retryDelay: 2000,
      backoff: true
    }
  );
  
  return await response.json();
}
```

### 完整示例：API客户端

```javascript
import { AntiDetection, RateLimiter, SessionManager } from '../common/anti-detection.js';

export class EnhancedAPIClient {
  constructor(baseURL, sessionFile, options = {}) {
    this.baseURL = baseURL;
    this.sessionManager = new SessionManager(sessionFile, {
      maxAge: options.sessionMaxAge || 7 * 24 * 60 * 60 * 1000,
      validateUrl: `${baseURL}/api/user`
    });
    this.limiter = new RateLimiter({
      minDelay: options.minDelay || 1000,
      maxDelay: options.maxDelay || 3000
    });
    this.session = null;
  }

  async init() {
    if (!(await this.sessionManager.isValid())) {
      throw new Error('No valid session. Please capture session first.');
    }
    this.session = await this.sessionManager.load();
  }

  getHeaders(customHeaders = {}) {
    const cookieString = this.session.cookies
      .map(c => `${c.name}=${c.value}`)
      .join('; ');

    return AntiDetection.createRealisticHeaders({
      'Referer': this.baseURL,
      'Origin': this.baseURL,
      'Cookie': cookieString,
      ...customHeaders
    });
  }

  async request(endpoint, options = {}) {
    await this.limiter.wait();

    const url = `${this.baseURL}${endpoint}`;
    const headers = this.getHeaders(options.headers);

    return await AntiDetection.fetchWithRetry(
      () => fetch(url, { ...options, headers }),
      {
        maxRetries: 3,
        retryDelay: 2000,
        backoff: true
      }
    );
  }

  async get(endpoint) {
    const response = await this.request(endpoint);
    return await response.json();
  }

  async post(endpoint, data) {
    const response = await this.request(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  }
}
```

## 集成方式C：混合模式

适用于既需要浏览器又需要HTTP请求的技能。

### 策略：浏览器捕获 + HTTP请求

```javascript
import { AntiDetection, SessionManager, RateLimiter } from '../common/anti-detection.js';

// 1. 使用浏览器捕获session（仅在需要时）
async function captureSession() {
  const browser = await AntiDetection.setupBrowser({ headless: false });
  const page = await browser.newPage();
  
  await AntiDetection.injectAntiDetection(page);
  await AntiDetection.setRealisticHeaders(page);
  
  // 登录并捕获session
  // ...
  
  await browser.close();
}

// 2. 使用HTTP请求进行后续操作
class HybridClient {
  constructor(sessionFile) {
    this.sessionManager = new SessionManager(sessionFile);
    this.limiter = new RateLimiter();
  }

  async init() {
    // 检查session
    if (!(await this.sessionManager.isValid())) {
      console.log('Session invalid, capturing new session...');
      await captureSession();
    }
    
    this.session = await this.sessionManager.load();
  }

  async apiCall(endpoint) {
    await this.limiter.wait();
    
    const headers = AntiDetection.createRealisticHeaders({
      'Cookie': this.session.cookies.map(c => `${c.name}=${c.value}`).join('; ')
    });
    
    return await AntiDetection.fetchWithRetry(
      () => fetch(endpoint, { headers })
    );
  }
}
```

## 技能特定集成示例

### BigQuant Strategy

```javascript
// skills/bigquant_strategy/browser/anti-detection-capture.js
import { AntiDetection, SessionManager } from '../../common/anti-detection.js';

async function captureBigQuantSession() {
  const sessionManager = new SessionManager('data/session.json');
  
  if (await sessionManager.isValid()) {
    return await sessionManager.load();
  }
  
  const browser = await AntiDetection.setupBrowser({ headless: false });
  const page = await browser.newPage();
  
  await AntiDetection.injectAntiDetection(page);
  await page.goto('https://bigquant.com');
  
  // 等待登录...
  
  const cookies = await page.context().cookies();
  await sessionManager.save({ cookies });
  
  await browser.close();
}
```

### THSQuant Strategy

```javascript
// skills/thsquant_strategy/request/enhanced-client.js
import { AntiDetection, RateLimiter } from '../../common/anti-detection.js';

class THSQuantClient {
  constructor() {
    this.limiter = new RateLimiter({ minDelay: 2000, maxDelay: 4000 });
  }

  async runBacktest(strategyId, config) {
    await this.limiter.wait();
    
    const headers = AntiDetection.createRealisticHeaders({
      'Referer': 'https://quant.10jqka.com.cn/',
      'Cookie': this.cookies
    });
    
    return await AntiDetection.fetchWithRetry(
      () => fetch(`https://quant.10jqka.com.cn/api/backtest`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ strategyId, config })
      })
    );
  }
}
```

### Guorn Strategy

```javascript
// skills/guorn_strategy/browser/enhanced-probe.js
import { AntiDetection } from '../../common/anti-detection.js';

async function probeGuornAPI() {
  const browser = await AntiDetection.setupBrowser();
  const page = await browser.newPage();
  
  await AntiDetection.injectAntiDetection(page);
  await AntiDetection.setRealisticHeaders(page, {
    'Referer': 'https://guorn.com/'
  });
  
  // 监听API请求
  page.on('request', request => {
    if (request.url().includes('/api/')) {
      console.log('API:', request.url());
    }
  });
  
  await page.goto('https://guorn.com');
  await AntiDetection.simulateHumanBehavior(page);
  
  // ... 探测逻辑
  
  await browser.close();
}
```

## 集成检查清单

在集成防封措施后，请检查以下项目：

### ✅ 浏览器自动化

- [ ] 使用 `AntiDetection.setupBrowser()` 创建浏览器
- [ ] 调用 `AntiDetection.injectAntiDetection(page)`
- [ ] 调用 `AntiDetection.setRealisticHeaders(page)`
- [ ] 使用 `AntiDetection.simulateHumanBehavior(page)` 模拟人类行为
- [ ] 使用 `AntiDetection.randomDelay()` 添加随机延迟
- [ ] 使用 `SessionManager` 管理session

### ✅ HTTP请求

- [ ] 使用 `AntiDetection.createRealisticHeaders()` 创建headers
- [ ] 使用 `AntiDetection.fetchWithRetry()` 进行请求
- [ ] 使用 `RateLimiter` 控制请求频率
- [ ] 使用 `SessionManager` 管理session
- [ ] 处理401/403错误（session失效）

### ✅ 通用

- [ ] 添加适当的日志输出
- [ ] 处理错误和异常
- [ ] 添加使用文档
- [ ] 测试防封效果

## 测试防封效果

### 测试1：检测webdriver标记

```javascript
const browser = await AntiDetection.setupBrowser();
const page = await browser.newPage();
await AntiDetection.injectAntiDetection(page);

await page.goto('https://bot.sannysoft.com/');
// 检查页面上的检测结果
```

### 测试2：检测请求频率

```javascript
const limiter = new RateLimiter({ minDelay: 2000, maxDelay: 4000 });

const startTime = Date.now();
for (let i = 0; i < 5; i++) {
  await limiter.wait();
  console.log(`Request ${i + 1} at ${Date.now() - startTime}ms`);
}
// 应该看到请求间隔在2-4秒之间
```

### 测试3：Session管理

```javascript
const sessionManager = new SessionManager('test-session.json', {
  maxAge: 1000 // 1秒，用于测试
});

await sessionManager.save({ cookies: [] });
console.log('Valid:', await sessionManager.isValid()); // true

await new Promise(resolve => setTimeout(resolve, 1100));
console.log('Valid:', await sessionManager.isValid()); // false
```

## 常见问题

### Q: 集成后仍然被检测？

A: 检查以下几点：
1. 确保调用了 `injectAntiDetection(page)`
2. 增加随机延迟时间
3. 检查是否有其他特征（如canvas指纹）
4. 使用 `headless: false` 调试

### Q: 请求太慢？

A: 调整限流参数：
```javascript
const limiter = new RateLimiter({
  minDelay: 500,  // 减少延迟
  maxDelay: 1500
});
```

### Q: Session频繁失效？

A: 检查：
1. `maxAge` 设置是否合理
2. 是否需要实现自动刷新
3. 使用 `validateUrl` 验证session

## 进阶优化

### 1. 自定义User-Agent池

```javascript
// 创建自定义User-Agent列表
const customUAs = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
  // 更多UA
];

// 扩展AntiDetection
class CustomAntiDetection extends AntiDetection {
  static getRandomUserAgent() {
    return customUAs[Math.floor(Math.random() * customUAs.length)];
  }
}
```

### 2. 代理支持

```javascript
const browser = await AntiDetection.setupBrowser({
  proxy: {
    server: 'http://proxy.example.com:8080',
    username: 'user',
    password: 'pass'
  }
});
```

### 3. 自动Session刷新

```javascript
class AutoRefreshSessionManager extends SessionManager {
  async ensureValid() {
    if (!(await this.isValid())) {
      await this.refresh();
    }
    return await this.load();
  }
  
  async refresh() {
    // 实现自动刷新逻辑
  }
}
```

## 相关文档

- [防封工具包使用指南](./ANTI_DETECTION_GUIDE.md)
- [浏览器 vs 请求分析](../BROWSER_VS_REQUEST_ANALYSIS.md)
- [Playwright文档](https://playwright.dev/)

## 支持

如有问题，请查看：
1. [常见问题](./ANTI_DETECTION_GUIDE.md#故障排除)
2. [示例代码](./ANTI_DETECTION_GUIDE.md#完整示例)
3. 现有技能的集成示例
