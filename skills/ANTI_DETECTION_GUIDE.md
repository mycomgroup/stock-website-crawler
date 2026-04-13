# 浏览器防封工具包使用指南

## 概述

`anti-detection.js` 提供了一套完整的浏览器防封和反检测工具，包括：

- 🛡️ 浏览器反检测配置
- 🎭 真实浏览器行为模拟
- 🔄 智能重试机制
- 📦 Session管理
- ⏱️ 请求限流

## 快速开始

### 1. 基础浏览器设置

```javascript
import { AntiDetection } from '../common/anti-detection.js';

// 创建反检测浏览器
const browser = await AntiDetection.setupBrowser({
  headless: true  // 可选：false 用于调试
});

const page = await browser.newPage();

// 注入反检测脚本
await AntiDetection.injectAntiDetection(page);

// 设置真实headers
await AntiDetection.setRealisticHeaders(page, {
  'Referer': 'https://example.com/',
  'Origin': 'https://example.com'
});

// 访问页面
await page.goto('https://example.com');

// 模拟人类行为
await AntiDetection.simulateHumanBehavior(page);
```

### 2. HTTP请求防封

```javascript
import { AntiDetection } from '../common/anti-detection.js';

// 创建真实的请求headers
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
    retryDelay: 1000,
    backoff: true  // 指数退避
  }
);

const data = await response.json();
```

### 3. Session管理

```javascript
import { SessionManager } from '../common/anti-detection.js';

// 创建session管理器
const sessionManager = new SessionManager('data/session.json', {
  maxAge: 7 * 24 * 60 * 60 * 1000,  // 7天
  validateUrl: 'https://api.example.com/user'  // 验证URL
});

// 检查session是否有效
if (await sessionManager.isValid()) {
  console.log('Using existing session');
  const session = await sessionManager.load();
  // 使用session
} else {
  console.log('Session invalid, need to login');
  // 重新登录并保存session
  const newSession = await login();
  await sessionManager.save(newSession);
}
```

### 4. 请求限流

```javascript
import { RateLimiter } from '../common/anti-detection.js';

// 创建限流器
const limiter = new RateLimiter({
  minDelay: 1000,  // 最小间隔1秒
  maxDelay: 3000   // 最大间隔3秒
});

// 批量请求
for (const item of items) {
  await limiter.wait();  // 自动限流
  const result = await processItem(item);
}
```

## 完整示例

### 示例1：浏览器自动化登录

```javascript
import { AntiDetection, SessionManager } from '../common/anti-detection.js';

async function loginWithBrowser() {
  const sessionManager = new SessionManager('data/session.json');
  
  // 检查现有session
  if (await sessionManager.isValid()) {
    return await sessionManager.load();
  }
  
  // 创建反检测浏览器
  const browser = await AntiDetection.setupBrowser({
    headless: false  // 显示浏览器用于手动登录
  });
  
  const page = await browser.newPage();
  
  // 注入反检测
  await AntiDetection.injectAntiDetection(page);
  await AntiDetection.setRealisticHeaders(page);
  
  // 访问登录页
  await page.goto('https://example.com/login');
  
  // 等待用户手动登录
  console.log('Please login manually...');
  await page.waitForURL('**/dashboard', { timeout: 300000 });
  
  // 模拟人类行为
  await AntiDetection.simulateHumanBehavior(page);
  
  // 捕获session
  const cookies = await page.context().cookies();
  const session = {
    cookies,
    userAgent: await page.evaluate(() => navigator.userAgent)
  };
  
  // 保存session
  await sessionManager.save(session);
  
  await browser.close();
  return session;
}
```

### 示例2：API调用防封

```javascript
import { AntiDetection, RateLimiter } from '../common/anti-detection.js';

class APIClient {
  constructor(baseURL, cookies) {
    this.baseURL = baseURL;
    this.cookies = cookies;
    this.limiter = new RateLimiter({
      minDelay: 1000,
      maxDelay: 2000
    });
  }
  
  async request(endpoint, options = {}) {
    // 限流
    await this.limiter.wait();
    
    // 创建headers
    const headers = AntiDetection.createRealisticHeaders({
      'Referer': this.baseURL,
      'Origin': this.baseURL,
      'Cookie': this.cookies.map(c => `${c.name}=${c.value}`).join('; '),
      ...options.headers
    });
    
    // 带重试的请求
    return await AntiDetection.fetchWithRetry(
      () => fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers
      }),
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
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    return await response.json();
  }
}

// 使用
const client = new APIClient('https://api.example.com', cookies);
const data = await client.get('/api/data');
```

### 示例3：批量操作防封

```javascript
import { AntiDetection, RateLimiter, SessionManager } from '../common/anti-detection.js';

async function batchProcess(items) {
  // 加载session
  const sessionManager = new SessionManager('data/session.json');
  const session = await sessionManager.load();
  
  // 创建限流器
  const limiter = new RateLimiter({
    minDelay: 2000,
    maxDelay: 5000
  });
  
  const results = [];
  
  for (const [index, item] of items.entries()) {
    console.log(`Processing ${index + 1}/${items.length}: ${item.name}`);
    
    // 限流
    await limiter.wait();
    
    try {
      // 带重试的请求
      const result = await AntiDetection.fetchWithRetry(
        async () => {
          const headers = AntiDetection.createRealisticHeaders({
            'Cookie': session.cookies.map(c => `${c.name}=${c.value}`).join('; ')
          });
          
          return await fetch(`https://api.example.com/process`, {
            method: 'POST',
            headers,
            body: JSON.stringify(item)
          });
        },
        {
          maxRetries: 3,
          retryDelay: 3000,
          backoff: true
        }
      );
      
      const data = await result.json();
      results.push({ item, data, success: true });
      
      // 随机延迟
      await AntiDetection.randomDelay(1000, 2000);
      
    } catch (error) {
      console.error(`Failed to process ${item.name}:`, error.message);
      results.push({ item, error: error.message, success: false });
    }
  }
  
  return results;
}
```

## API参考

### AntiDetection

#### setupBrowser(options)
创建配置了反检测的浏览器实例。

**参数：**
- `options.headless` (boolean): 是否无头模式，默认true
- `options.args` (Array): 额外的启动参数

**返回：** Promise<Browser>

#### injectAntiDetection(page)
向页面注入反检测脚本。

**参数：**
- `page` (Page): Playwright页面对象

#### setRealisticHeaders(page, customHeaders)
设置真实的浏览器headers。

**参数：**
- `page` (Page): Playwright页面对象
- `customHeaders` (Object): 自定义headers

#### randomDelay(min, max)
随机延迟。

**参数：**
- `min` (number): 最小延迟(ms)，默认1000
- `max` (number): 最大延迟(ms)，默认3000

**返回：** Promise<void>

#### getRandomUserAgent()
获取随机User-Agent。

**返回：** string

#### simulateHumanBehavior(page)
模拟人类行为（鼠标移动、滚动等）。

**参数：**
- `page` (Page): Playwright页面对象

#### fetchWithRetry(fetchFn, options)
带重试的HTTP请求。

**参数：**
- `fetchFn` (Function): 请求函数
- `options.maxRetries` (number): 最大重试次数，默认3
- `options.retryDelay` (number): 重试延迟(ms)，默认1000
- `options.backoff` (boolean): 是否使用指数退避，默认true

**返回：** Promise<Response>

#### createRealisticHeaders(customHeaders)
创建真实的HTTP请求headers。

**参数：**
- `customHeaders` (Object): 自定义headers

**返回：** Object

### SessionManager

#### constructor(sessionFile, options)
创建session管理器。

**参数：**
- `sessionFile` (string): Session文件路径
- `options.maxAge` (number): 最大有效期(ms)，默认7天
- `options.validateUrl` (string): 验证URL

#### load()
加载session。

**返回：** Promise<Object|null>

#### save(session)
保存session。

**参数：**
- `session` (Object): Session数据

#### isValid()
检查session是否有效。

**返回：** Promise<boolean>

#### validateCookies(cookies)
验证cookies是否有效。

**参数：**
- `cookies` (Array): Cookie数组

**返回：** Promise<boolean>

#### clear()
清除session。

### RateLimiter

#### constructor(options)
创建请求限流器。

**参数：**
- `options.minDelay` (number): 最小延迟(ms)，默认1000
- `options.maxDelay` (number): 最大延迟(ms)，默认3000

#### wait()
等待直到可以发送下一个请求。

**返回：** Promise<void>

## 最佳实践

### 1. 浏览器自动化

✅ **推荐做法：**
```javascript
// 使用反检测浏览器
const browser = await AntiDetection.setupBrowser();
await AntiDetection.injectAntiDetection(page);

// 模拟人类行为
await AntiDetection.simulateHumanBehavior(page);
await AntiDetection.randomDelay(1000, 3000);
```

❌ **避免：**
```javascript
// 直接使用默认浏览器
const browser = await chromium.launch();

// 没有延迟的快速操作
await page.click('#button');
await page.click('#submit');
```

### 2. HTTP请求

✅ **推荐做法：**
```javascript
// 使用真实headers和重试
const headers = AntiDetection.createRealisticHeaders({
  'Referer': 'https://example.com/'
});

await AntiDetection.fetchWithRetry(
  () => fetch(url, { headers }),
  { maxRetries: 3, backoff: true }
);
```

❌ **避免：**
```javascript
// 简单的fetch，没有headers
const response = await fetch(url);
```

### 3. 批量操作

✅ **推荐做法：**
```javascript
const limiter = new RateLimiter({ minDelay: 2000, maxDelay: 5000 });

for (const item of items) {
  await limiter.wait();
  await processItem(item);
  await AntiDetection.randomDelay(1000, 2000);
}
```

❌ **避免：**
```javascript
// 快速循环，没有延迟
for (const item of items) {
  await processItem(item);
}
```

### 4. Session管理

✅ **推荐做法：**
```javascript
const sessionManager = new SessionManager('data/session.json', {
  maxAge: 7 * 24 * 60 * 60 * 1000,
  validateUrl: 'https://api.example.com/user'
});

if (!(await sessionManager.isValid())) {
  await relogin();
}
```

❌ **避免：**
```javascript
// 不检查session有效性
const session = JSON.parse(fs.readFileSync('session.json'));
```

## 故障排除

### 问题1：仍然被检测为机器人

**解决方案：**
1. 确保调用了 `injectAntiDetection(page)`
2. 增加随机延迟时间
3. 使用 `headless: false` 检查浏览器行为
4. 检查是否有其他特征（如canvas指纹）

### 问题2：请求被限流

**解决方案：**
1. 增加 `RateLimiter` 的延迟时间
2. 使用指数退避策略
3. 检查是否需要IP轮换

### 问题3：Session频繁失效

**解决方案：**
1. 检查 `maxAge` 设置是否合理
2. 实现自动刷新机制
3. 使用 `validateUrl` 验证session

## 进阶技巧

### 1. 自定义User-Agent池

```javascript
// 扩展AntiDetection类
class CustomAntiDetection extends AntiDetection {
  static getRandomUserAgent() {
    const customUAs = [
      // 你的自定义UA列表
    ];
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
      console.log('Session invalid, refreshing...');
      await this.refresh();
    }
    return await this.load();
  }
  
  async refresh() {
    // 实现自动刷新逻辑
    const newSession = await loginAndCaptureSession();
    await this.save(newSession);
  }
}
```

## 相关资源

- [Playwright文档](https://playwright.dev/)
- [反爬虫技术研究](https://github.com/topics/anti-detection)
- [浏览器指纹识别](https://github.com/fingerprintjs/fingerprintjs)

## 更新日志

### v1.0.0 (2026-04-12)
- 初始版本
- 支持浏览器反检测
- 支持HTTP请求防封
- 支持Session管理
- 支持请求限流
