# 快速上手指南

欢迎使用浏览器防封工具包！本指南将帮助你在5分钟内开始使用。

## 🚀 5分钟快速开始

### 步骤1: 运行快速开始脚本

```bash
cd skills/common
./quick-start.sh
```

或者手动运行测试：

```bash
node test-anti-detection.js --all
```

### 步骤2: 查看测试结果

测试脚本会：
1. 打开浏览器访问检测网站
2. 测试请求限流
3. 测试Session管理
4. 测试HTTP请求

### 步骤3: 查看示例代码

```bash
# 查看BigQuant集成示例
cat ../bigquant_strategy/browser/anti-detection-capture.js
cat ../bigquant_strategy/request/enhanced-client.js
```

## 📚 三种使用方式

### 方式1: 浏览器自动化

适用于需要浏览器交互的场景（如登录、页面操作）。

```javascript
import { AntiDetection } from '../common/anti-detection.js';

// 创建反检测浏览器
const browser = await AntiDetection.setupBrowser();
const page = await browser.newPage();

// 注入反检测
await AntiDetection.injectAntiDetection(page);
await AntiDetection.setRealisticHeaders(page);

// 访问页面
await page.goto('https://example.com');

// 模拟人类行为
await AntiDetection.simulateHumanBehavior(page);
```

### 方式2: HTTP请求

适用于使用HTTP API的场景。

```javascript
import { AntiDetection, RateLimiter } from '../common/anti-detection.js';

// 创建限流器
const limiter = new RateLimiter({ minDelay: 1000, maxDelay: 3000 });

// 发送请求
await limiter.wait();
const headers = AntiDetection.createRealisticHeaders({
  'Cookie': 'session=xxx'
});

const response = await AntiDetection.fetchWithRetry(
  () => fetch('https://api.example.com/data', { headers }),
  { maxRetries: 3, backoff: true }
);
```

### 方式3: 混合模式

浏览器捕获Session + HTTP请求操作。

```javascript
import { AntiDetection, SessionManager } from '../common/anti-detection.js';

// 1. 使用浏览器捕获session（仅在需要时）
async function captureSession() {
  const browser = await AntiDetection.setupBrowser({ headless: false });
  const page = await browser.newPage();
  
  await AntiDetection.injectAntiDetection(page);
  await page.goto('https://example.com/login');
  
  // 等待登录...
  
  const cookies = await page.context().cookies();
  await sessionManager.save({ cookies });
  
  await browser.close();
}

// 2. 使用HTTP请求进行后续操作
const sessionManager = new SessionManager('data/session.json');
if (!(await sessionManager.isValid())) {
  await captureSession();
}

const session = await sessionManager.load();
// 使用session进行HTTP请求...
```

## 🎯 常见场景

### 场景1: 登录并保存Session

```javascript
import { AntiDetection, SessionManager } from '../common/anti-detection.js';

async function loginAndSaveSession() {
  const sessionManager = new SessionManager('data/session.json');
  
  // 检查现有session
  if (await sessionManager.isValid()) {
    console.log('Using existing session');
    return await sessionManager.load();
  }
  
  // 创建浏览器
  const browser = await AntiDetection.setupBrowser({ headless: false });
  const page = await browser.newPage();
  
  // 注入反检测
  await AntiDetection.injectAntiDetection(page);
  
  // 访问登录页
  await page.goto('https://example.com/login');
  
  // 等待用户手动登录
  console.log('Please login manually...');
  await page.waitForURL('**/dashboard', { timeout: 300000 });
  
  // 保存session
  const cookies = await page.context().cookies();
  await sessionManager.save({ cookies });
  
  await browser.close();
  return { cookies };
}
```

### 场景2: 批量API调用

```javascript
import { AntiDetection, RateLimiter } from '../common/anti-detection.js';

async function batchAPICall(items) {
  const limiter = new RateLimiter({ minDelay: 2000, maxDelay: 4000 });
  
  const results = [];
  for (const item of items) {
    await limiter.wait();
    
    const headers = AntiDetection.createRealisticHeaders({
      'Cookie': 'session=xxx'
    });
    
    try {
      const response = await AntiDetection.fetchWithRetry(
        () => fetch(`https://api.example.com/process`, {
          method: 'POST',
          headers,
          body: JSON.stringify(item)
        }),
        { maxRetries: 3, backoff: true }
      );
      
      const data = await response.json();
      results.push({ item, data, success: true });
      
    } catch (error) {
      results.push({ item, error: error.message, success: false });
    }
    
    // 额外的随机延迟
    await AntiDetection.randomDelay(1000, 2000);
  }
  
  return results;
}
```

### 场景3: 创建API客户端

```javascript
import { AntiDetection, RateLimiter, SessionManager } from '../common/anti-detection.js';

class MyAPIClient {
  constructor(baseURL, sessionFile) {
    this.baseURL = baseURL;
    this.sessionManager = new SessionManager(sessionFile);
    this.limiter = new RateLimiter({ minDelay: 1000, maxDelay: 3000 });
    this.session = null;
  }

  async init() {
    if (!(await this.sessionManager.isValid())) {
      throw new Error('No valid session. Please login first.');
    }
    this.session = await this.sessionManager.load();
  }

  async request(endpoint, options = {}) {
    await this.limiter.wait();

    const headers = AntiDetection.createRealisticHeaders({
      'Referer': this.baseURL,
      'Cookie': this.session.cookies.map(c => `${c.name}=${c.value}`).join('; '),
      ...options.headers
    });

    return await AntiDetection.fetchWithRetry(
      () => fetch(`${this.baseURL}${endpoint}`, { ...options, headers }),
      { maxRetries: 3, backoff: true }
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

// 使用
const client = new MyAPIClient('https://api.example.com', 'data/session.json');
await client.init();
const data = await client.get('/api/data');
```

## 🔍 检查集成是否成功

### 检查清单

浏览器自动化：
- [ ] 使用 `AntiDetection.setupBrowser()`
- [ ] 调用 `injectAntiDetection(page)`
- [ ] 调用 `setRealisticHeaders(page)`
- [ ] 使用 `simulateHumanBehavior(page)`
- [ ] 使用 `randomDelay()`

HTTP请求：
- [ ] 使用 `createRealisticHeaders()`
- [ ] 使用 `fetchWithRetry()`
- [ ] 使用 `RateLimiter`
- [ ] 处理401/403错误

Session管理：
- [ ] 使用 `SessionManager`
- [ ] 检查 `isValid()`
- [ ] 自动刷新失效session

### 测试方法

1. **测试浏览器反检测**
   ```bash
   node test-anti-detection.js --browser
   ```
   访问 https://bot.sannysoft.com/ 检查是否被识别为机器人。

2. **测试请求限流**
   ```bash
   node test-anti-detection.js --limiter
   ```
   检查请求间隔是否符合预期。

3. **测试Session管理**
   ```bash
   node test-anti-detection.js --session
   ```
   验证session的保存、加载和过期检测。

## 📖 下一步

### 深入学习

1. **详细API文档**: 阅读 `ANTI_DETECTION_GUIDE.md`
2. **集成指南**: 阅读 `INTEGRATION_GUIDE.md`
3. **完整示例**: 查看 `../bigquant_strategy/`

### 集成到你的技能

1. 复制示例代码
2. 根据你的需求修改
3. 运行测试验证
4. 查看文档解决问题

### 获取帮助

- 查看 [故障排除](./ANTI_DETECTION_GUIDE.md#故障排除)
- 查看 [常见问题](./INTEGRATION_GUIDE.md#常见问题)
- 查看示例代码

## 💡 最佳实践提示

1. **优先使用HTTP API** - 能用HTTP就不用浏览器
2. **最小化浏览器使用** - 仅用于登录和session捕获
3. **完整的反检测** - 使用所有反检测措施
4. **请求随机化** - 间隔、UA、操作都要随机化
5. **Session管理** - 自动检测和刷新

## 🎉 开始使用

现在你已经准备好了！选择一个场景，复制代码，开始使用吧！

```bash
# 运行快速开始脚本
./quick-start.sh

# 或者直接运行测试
node test-anti-detection.js --all
```

祝你使用愉快！🚀
