# Design Document: Stock Website Crawler

## Overview

本系统是一个通用的、配置化的网站爬虫系统，专门针对股票数据网站（如东方财富、雪球、理杏仁等）进行数据爬取。系统采用模块化设计，支持自动登录、链接发现、页面解析和内容提取等功能。

核心设计理念：
- **配置驱动**：通过JSON配置文件定义爬取规则，无需修改代码
- **模块化**：将功能分离到独立模块，便于维护和扩展
- **可恢复**：支持断点续爬，通过links.txt管理爬取状态
- **容错性**：优雅处理错误，不因单个页面失败而中断整体流程

## Architecture

系统采用分层架构，主要包含以下层次：

```
┌─────────────────────────────────────┐
│         Main Controller             │  主控制器
│    (crawler-main.js)                │
└──────────────┬──────────────────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌──▼───┐  ┌──▼────┐
│Config │  │Link  │  │Browser│  核心模块层
│Manager│  │Manager│ │Manager│
└───┬───┘  └──┬───┘  └──┬────┘
    │         │         │
    └─────────┼─────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼────┐ ┌─▼────┐ ┌─▼──────┐
│Login   │ │Link  │ │Page    │  功能模块层
│Handler │ │Finder│ │Parser  │
└────────┘ └──────┘ └────┬───┘
                          │
                     ┌────▼────┐
                     │Markdown │  输出层
                     │Generator│
                     └─────────┘
```

**数据流**：
1. Main Controller 读取配置和链接列表
2. Browser Manager 启动浏览器并访问URL
3. Login Handler 检测并处理登录（如需要）
4. Page Parser 解析页面内容
5. Link Finder 发现新链接并更新链接列表
6. Markdown Generator 生成输出文件

## Components and Interfaces

### 1. Config Manager (config-manager.js)

负责读取和验证配置文件。

**接口**：
```javascript
class ConfigManager {
  /**
   * 加载配置文件
   * @param {string} configPath - 配置文件路径
   * @returns {Config} 配置对象
   * @throws {Error} 配置文件不存在或格式错误
   */
  loadConfig(configPath)
  
  /**
   * 验证配置完整性
   * @param {Config} config - 配置对象
   * @returns {boolean} 是否有效
   */
  validateConfig(config)
}
```

**配置文件格式**：
```json
{
  "name": "lixinger-crawler",
  "seedUrls": [
    "https://www.lixinger.com/open/api/doc"
  ],
  "urlRules": {
    "include": [".*api-key=.*"],
    "exclude": [".*login.*", ".*logout.*"]
  },
  "login": {
    "required": true,
    "username": "13311390323",
    "password": "3228552",
    "loginUrl": "https://www.lixinger.com/login"
  },
  "crawler": {
    "headless": false,
    "timeout": 30000,
    "waitBetweenRequests": 500,
    "maxRetries": 3
  },
  "output": {
    "directory": "./output",
    "format": "markdown"
  }
}
```

### 2. Link Manager (link-manager.js)

负责管理URL列表的读取、写入、去重和状态跟踪。

**接口**：
```javascript
class LinkManager {
  /**
   * 从文件加载链接列表
   * @param {string} filePath - links.txt路径
   * @returns {Link[]} 链接对象数组
   */
  loadLinks(filePath)
  
  /**
   * 保存链接列表到文件
   * @param {string} filePath - links.txt路径
   * @param {Link[]} links - 链接对象数组
   */
  saveLinks(filePath, links)
  
  /**
   * 添加新链接
   * @param {string} url - URL字符串
   * @param {string} status - 状态：pending/crawled/failed
   */
  addLink(url, status = 'pending')
  
  /**
   * 更新链接状态
   * @param {string} url - URL字符串
   * @param {string} status - 新状态
   */
  updateLinkStatus(url, status)
  
  /**
   * 获取待爬取的链接
   * @returns {Link[]} 状态为pending的链接
   */
  getPendingLinks()
  
  /**
   * 去重和排序
   */
  deduplicateAndSort()
}
```

**Link数据结构**：
```javascript
{
  url: string,           // URL地址
  status: string,        // pending/crawled/failed
  addedAt: timestamp,    // 添加时间
  crawledAt: timestamp,  // 爬取时间
  retryCount: number     // 重试次数
}
```

### 3. Browser Manager (browser-manager.js)

负责浏览器实例的创建、管理和页面导航。

**接口**：
```javascript
class BrowserManager {
  /**
   * 启动浏览器
   * @param {Object} options - 浏览器选项（headless等）
   */
  async launch(options)
  
  /**
   * 创建新页面
   * @returns {Page} Playwright页面对象
   */
  async newPage()
  
  /**
   * 导航到URL
   * @param {Page} page - 页面对象
   * @param {string} url - 目标URL
   * @param {number} timeout - 超时时间
   */
  async goto(page, url, timeout)
  
  /**
   * 等待页面加载完成
   * @param {Page} page - 页面对象
   * @param {number} timeout - 超时时间
   */
  async waitForLoad(page, timeout)
  
  /**
   * 关闭浏览器
   */
  async close()
}
```

### 4. Login Handler (login-handler.js)

负责检测登录页面并执行自动登录。

**接口**：
```javascript
class LoginHandler {
  /**
   * 检测是否需要登录
   * @param {Page} page - 页面对象
   * @returns {boolean} 是否在登录页面
   */
  async needsLogin(page)
  
  /**
   * 执行登录
   * @param {Page} page - 页面对象
   * @param {Object} credentials - 登录凭证 {username, password}
   * @returns {boolean} 登录是否成功
   */
  async login(page, credentials)
  
  /**
   * 查找并填写用户名输入框
   * @param {Page} page - 页面对象
   * @param {string} username - 用户名
   */
  async fillUsername(page, username)
  
  /**
   * 查找并填写密码输入框
   * @param {Page} page - 页面对象
   * @param {string} password - 密码
   */
  async fillPassword(page, password)
  
  /**
   * 查找并点击登录按钮
   * @param {Page} page - 页面对象
   */
  async clickLoginButton(page)
}
```

**登录检测策略**：
1. 检查URL是否包含"login"关键字
2. 检查页面是否包含密码输入框
3. 检查页面是否包含"登录"按钮

**表单识别策略**：
- 用户名输入框：`input[placeholder*="手机"]`, `input[placeholder*="账号"]`, `input[type="tel"]`, `input[name="phone"]`, `input[name="username"]`
- 密码输入框：`input[type="password"]`
- 登录按钮：`button:has-text("登录")`, `button[type="submit"]`

### 5. Link Finder (link-finder.js)

负责从页面中发现和提取符合规则的链接。

**接口**：
```javascript
class LinkFinder {
  /**
   * 展开页面中的折叠内容
   * @param {Page} page - 页面对象
   */
  async expandCollapsibles(page)
  
  /**
   * 提取页面中的所有链接
   * @param {Page} page - 页面对象
   * @param {Object} urlRules - URL过滤规则
   * @returns {string[]} URL数组
   */
  async extractLinks(page, urlRules)
  
  /**
   * 过滤链接
   * @param {string[]} urls - URL数组
   * @param {Object} urlRules - 过滤规则 {include, exclude}
   * @returns {string[]} 过滤后的URL数组
   */
  filterLinks(urls, urlRules)
  
  /**
   * 将相对URL转换为绝对URL
   * @param {string} url - 相对或绝对URL
   * @param {string} baseUrl - 基础URL
   * @returns {string} 绝对URL
   */
  toAbsoluteUrl(url, baseUrl)
}
```

**展开策略**：
1. 展开所有`<details>`元素
2. 点击包含"展开"、"▶"等文本的元素
3. 点击class包含"expand"、"collapse"的元素
4. 等待动态内容加载

### 6. Page Parser (page-parser.js)

负责解析页面内容，提取表格、文本、代码块等结构化数据。

**接口**：
```javascript
class PageParser {
  /**
   * 解析页面内容
   * @param {Page} page - 页面对象
   * @param {string} url - 页面URL
   * @returns {PageData} 解析后的页面数据
   */
  async parsePage(page, url)
  
  /**
   * 提取页面标题
   * @param {Page} page - 页面对象
   * @returns {string} 标题
   */
  async extractTitle(page)
  
  /**
   * 提取页面描述
   * @param {Page} page - 页面对象
   * @returns {string} 描述
   */
  async extractDescription(page)
  
  /**
   * 提取所有表格
   * @param {Page} page - 页面对象
   * @returns {Table[]} 表格数组
   */
  async extractTables(page)
  
  /**
   * 提取tab内容
   * @param {Page} page - 页面对象
   * @returns {TabContent[]} tab内容数组
   */
  async extractTabContents(page)
  
  /**
   * 提取代码块
   * @param {Page} page - 页面对象
   * @returns {CodeBlock[]} 代码块数组
   */
  async extractCodeBlocks(page)
}
```

**PageData数据结构**：
```javascript
{
  url: string,              // 页面URL
  title: string,            // 页面标题
  description: string,      // 页面描述
  tables: Table[],          // 表格数组
  tabContents: TabContent[], // tab内容数组
  codeBlocks: CodeBlock[],  // 代码块数组
  rawText: string           // 原始文本
}
```

**Table数据结构**：
```javascript
{
  headers: string[],        // 表头
  rows: string[][]          // 数据行
}
```

**TabContent数据结构**：
```javascript
{
  tabName: string,          // tab名称
  content: string,          // tab内容
  codeBlocks: CodeBlock[]   // tab中的代码块
}
```

**CodeBlock数据结构**：
```javascript
{
  language: string,         // 语言类型（json/xml/html等）
  code: string              // 代码内容
}
```

**Tab处理策略**：
1. 查找所有tab按钮（通过常见的class名称和结构）
2. 逐个点击tab按钮
3. 等待内容更新
4. 提取当前tab的内容
5. 重复直到所有tab都被处理

### 7. Markdown Generator (markdown-generator.js)

负责将解析的页面数据转换为Markdown格式。

**接口**：
```javascript
class MarkdownGenerator {
  /**
   * 生成Markdown内容
   * @param {PageData} pageData - 页面数据
   * @returns {string} Markdown文本
   */
  generate(pageData)
  
  /**
   * 将表格转换为Markdown表格
   * @param {Table} table - 表格数据
   * @returns {string} Markdown表格
   */
  tableToMarkdown(table)
  
  /**
   * 将代码块转换为Markdown代码块
   * @param {CodeBlock} codeBlock - 代码块数据
   * @returns {string} Markdown代码块
   */
  codeBlockToMarkdown(codeBlock)
  
  /**
   * 生成安全的文件名
   * @param {string} title - 原始标题
   * @returns {string} 安全的文件名
   */
  safeFilename(title)
  
  /**
   * 保存Markdown文件
   * @param {string} content - Markdown内容
   * @param {string} filename - 文件名
   * @param {string} outputDir - 输出目录
   */
  saveToFile(content, filename, outputDir)
}
```

**Markdown格式规范**：
- 使用`#`表示标题层级
- 表格使用标准Markdown表格格式
- 代码块使用三个反引号包裹，并指定语言
- 特殊字符（如`|`）需要转义
- 换行使用`<br>`标签

### 8. Main Controller (crawler-main.js)

主控制器，协调所有模块完成爬取任务。

**接口**：
```javascript
class CrawlerMain {
  /**
   * 初始化爬虫
   * @param {string} configPath - 配置文件路径
   */
  async initialize(configPath)
  
  /**
   * 开始爬取
   */
  async start()
  
  /**
   * 处理单个URL
   * @param {string} url - 目标URL
   * @returns {boolean} 是否成功
   */
  async processUrl(url)
  
  /**
   * 记录进度
   * @param {number} current - 当前进度
   * @param {number} total - 总数
   */
  logProgress(current, total)
  
  /**
   * 记录错误
   * @param {string} url - 出错的URL
   * @param {Error} error - 错误对象
   */
  logError(url, error)
  
  /**
   * 生成统计报告
   * @returns {Object} 统计信息
   */
  generateStats()
}
```

**主流程**：
1. 加载配置文件
2. 初始化Link Manager，加载links.txt
3. 如果links.txt为空，使用seedUrls初始化
4. 启动浏览器
5. 执行登录（如需要）
6. 遍历待爬取的链接：
   - 访问URL
   - 解析页面内容
   - 发现新链接并添加到列表
   - 生成Markdown文件
   - 更新链接状态
   - 等待延迟时间
7. 关闭浏览器
8. 输出统计信息

## Data Models

### Config

```javascript
{
  name: string,                    // 爬虫名称
  seedUrls: string[],              // 起始URL列表
  urlRules: {
    include: string[],             // 包含规则（正则表达式）
    exclude: string[]              // 排除规则（正则表达式）
  },
  login: {
    required: boolean,             // 是否需要登录
    username: string,              // 用户名
    password: string,              // 密码
    loginUrl: string               // 登录页面URL
  },
  crawler: {
    headless: boolean,             // 是否无头模式
    timeout: number,               // 超时时间（毫秒）
    waitBetweenRequests: number,   // 请求间隔（毫秒）
    maxRetries: number             // 最大重试次数
  },
  output: {
    directory: string,             // 输出目录
    format: string                 // 输出格式（markdown）
  }
}
```

### Link

```javascript
{
  url: string,                     // URL地址
  status: 'pending' | 'crawled' | 'failed',  // 状态
  addedAt: number,                 // 添加时间戳
  crawledAt: number | null,        // 爬取时间戳
  retryCount: number,              // 重试次数
  error: string | null             // 错误信息
}
```

### PageData

```javascript
{
  url: string,                     // 页面URL
  title: string,                   // 页面标题
  description: string,             // 页面描述
  tables: Table[],                 // 表格数组
  tabContents: TabContent[],       // tab内容数组
  codeBlocks: CodeBlock[],         // 代码块数组
  rawText: string                  // 原始文本
}
```

### Table

```javascript
{
  headers: string[],               // 表头数组
  rows: string[][]                 // 数据行数组
}
```

### TabContent

```javascript
{
  tabName: string,                 // tab名称
  content: string,                 // tab内容
  codeBlocks: CodeBlock[]          // tab中的代码块
}
```

### CodeBlock

```javascript
{
  language: string,                // 语言类型
  code: string                     // 代码内容
}
```

### CrawlerStats

```javascript
{
  totalUrls: number,               // 总URL数
  crawledUrls: number,             // 已爬取数
  failedUrls: number,              // 失败数
  newLinksFound: number,           // 新发现链接数
  filesGenerated: number,          // 生成文件数
  startTime: number,               // 开始时间
  endTime: number,                 // 结束时间
  duration: number                 // 持续时间（秒）
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Acceptance Criteria Testing Prework

**Requirement 1: 配置化爬取管理**

1.1 THE Crawler_System SHALL 读取配置文件并解析爬取规则
  Thoughts: 这是一个通用规则，适用于所有有效的配置文件。我们可以生成随机的配置文件，调用解析函数，并验证返回的配置对象包含所有必需字段
  Testable: yes - property

1.2 WHERE 配置文件包含URL规则，THE Crawler_System SHALL 使用该规则过滤和匹配链接
  Thoughts: 这是关于URL过滤的通用行为。我们可以生成随机的URL规则和URL列表，验证过滤后的结果都符合规则
  Testable: yes - property

1.3 WHERE 配置文件包含起始种子链接，THE Crawler_System SHALL 从这些链接开始爬取
  Thoughts: 这是关于初始化行为的规则。我们可以验证系统是否正确加载种子链接
  Testable: yes - property

1.4 WHERE 配置文件包含登录信息，THE Crawler_System SHALL 使用该信息进行网站登录
  Thoughts: 这涉及到外部系统交互（实际网站登录），难以在单元测试中验证
  Testable: no

1.5 WHEN 配置文件格式错误或缺少必需字段，THE Crawler_System SHALL 返回描述性错误信息
  Thoughts: 这是关于错误处理的规则。我们可以生成各种无效配置，验证系统是否正确返回错误
  Testable: yes - property

**Requirement 2: 链接管理和持久化**

2.1 THE Link_Manager SHALL 从links.txt文件读取URL列表
  Thoughts: 这是关于文件读取的基本功能。我们可以创建测试文件并验证读取结果
  Testable: yes - property

2.2 WHEN 发现新的URL，THE Link_Manager SHALL 将其追加到links.txt文件
  Thoughts: 这是关于文件写入的功能。我们可以验证添加URL后文件内容是否正确更新
  Testable: yes - property

2.3 THE Link_Manager SHALL 对URL列表进行去重处理
  Thoughts: 这是一个不变性属性。添加重复URL后，列表中不应该有重复项
  Testable: yes - property

2.4 THE Link_Manager SHALL 对URL列表进行排序以保持一致性
  Thoughts: 这是一个不变性属性。保存后的URL列表应该是排序的
  Testable: yes - property

2.5 WHEN links.txt文件不存在，THE Link_Manager SHALL 使用配置文件中的起始种子链接创建该文件
  Thoughts: 这是一个特定场景的测试，可以作为示例测试
  Testable: yes - example

2.6 THE Link_Manager SHALL 记录每个URL的爬取状态（待爬取、已爬取、失败）
  Thoughts: 这是关于状态管理的规则。我们可以验证状态更新是否正确
  Testable: yes - property

**Requirement 3: 自动登录处理**

3.1 WHEN 页面包含登录表单，THE Login_Handler SHALL 检测并识别登录页面
  Thoughts: 这涉及到DOM解析和模式识别。我们可以创建包含登录表单的测试HTML，验证检测逻辑
  Testable: yes - property

3.2 WHEN 检测到登录页面，THE Login_Handler SHALL 使用配置文件中的账号和密码填写表单
  Thoughts: 这涉及到浏览器交互，难以在单元测试中验证，更适合集成测试
  Testable: no

3.3 THE Login_Handler SHALL 支持多种登录表单格式（手机号、邮箱、用户名等）
  Thoughts: 这是关于表单识别的规则。我们可以创建不同格式的登录表单HTML，验证都能被正确识别
  Testable: yes - property

3.4 WHEN 登录成功，THE Login_Handler SHALL 保存会话状态以供后续请求使用
  Thoughts: 这涉及到浏览器会话管理，难以在单元测试中验证
  Testable: no

3.5 WHEN 登录失败，THE Login_Handler SHALL 返回错误信息并记录失败原因
  Thoughts: 这是关于错误处理的规则，但涉及到实际登录交互
  Testable: no

3.6 WHERE 网站不需要登录，THE Login_Handler SHALL 跳过登录步骤
  Thoughts: 这是一个条件逻辑测试，可以验证
  Testable: yes - example

**Requirement 4: 链接发现和提取**

4.1 THE Crawler_System SHALL 从当前页面提取所有符合URL规则的链接
  Thoughts: 这是关于链接提取的通用规则。我们可以创建包含各种链接的测试HTML，验证提取结果
  Testable: yes - property

4.2 THE Crawler_System SHALL 展开页面中的折叠内容以发现隐藏的链接
  Thoughts: 这涉及到浏览器交互和DOM操作，难以在单元测试中验证
  Testable: no

4.3 WHEN 页面包含动态加载的内容，THE Crawler_System SHALL 等待内容加载完成后再提取链接
  Thoughts: 这涉及到异步加载和时序问题，难以在单元测试中验证
  Testable: no

4.4 THE Crawler_System SHALL 将相对URL转换为绝对URL
  Thoughts: 这是一个纯函数转换。我们可以生成随机的相对URL和基础URL，验证转换结果
  Testable: yes - property

4.5 THE Crawler_System SHALL 过滤掉不符合配置规则的链接
  Thoughts: 这与1.2重复，都是关于URL过滤
  Testable: yes - property (redundant with 1.2)

4.6 WHEN 发现新链接，THE Crawler_System SHALL 通过Link_Manager将其添加到links.txt
  Thoughts: 这与2.2重复
  Testable: yes - property (redundant with 2.2)

**Requirement 5: 页面内容解析**

5.1 THE Page_Parser SHALL 提取页面中的所有表格数据
  Thoughts: 这是关于表格解析的通用规则。我们可以创建包含各种表格的测试HTML，验证提取结果
  Testable: yes - property

5.2 THE Page_Parser SHALL 识别并提取表格的标题行和数据行
  Thoughts: 这是5.1的细化，可以合并
  Testable: yes - property (can merge with 5.1)

5.3 WHEN 页面包含多个tab，THE Page_Parser SHALL 逐个点击tab并提取每个tab的内容
  Thoughts: 这涉及到浏览器交互，难以在单元测试中验证
  Testable: no

5.4 THE Page_Parser SHALL 提取页面标题、描述和主要文本内容
  Thoughts: 这是关于文本提取的规则。我们可以创建测试HTML，验证提取结果
  Testable: yes - property

5.5 THE Page_Parser SHALL 识别并提取代码块（如JSON、XML等）
  Thoughts: 这是关于代码块识别的规则。我们可以创建包含各种代码块的测试HTML，验证提取结果
  Testable: yes - property

5.6 THE Page_Parser SHALL 处理表格中的特殊字符和换行符
  Thoughts: 这是边缘情况处理，应该作为edge case在生成器中处理
  Testable: edge-case

5.7 WHEN 页面包含折叠内容，THE Page_Parser SHALL 展开所有折叠项后再解析
  Thoughts: 这涉及到浏览器交互，难以在单元测试中验证
  Testable: no

**Requirement 6: 输出格式化**

6.1 THE Crawler_System SHALL 将解析的页面内容转换为Markdown格式
  Thoughts: 这是关于格式转换的通用规则。我们可以生成随机的PageData，验证生成的Markdown格式正确
  Testable: yes - property

6.2 THE Crawler_System SHALL 将表格转换为Markdown表格格式
  Thoughts: 这是6.1的一部分，可以合并
  Testable: yes - property (can merge with 6.1)

6.3 THE Crawler_System SHALL 将代码块使用Markdown代码块格式包裹
  Thoughts: 这是6.1的一部分，可以合并
  Testable: yes - property (can merge with 6.1)

6.4 THE Crawler_System SHALL 为每个页面生成独立的Markdown文件
  Thoughts: 这是关于文件生成的规则，涉及到文件系统操作
  Testable: yes - property

6.5 THE Crawler_System SHALL 使用安全的文件名（移除特殊字符）
  Thoughts: 这是一个纯函数转换。我们可以生成包含特殊字符的文件名，验证转换结果
  Testable: yes - property

6.6 THE Crawler_System SHALL 在Markdown文件中保留原始URL作为参考
  Thoughts: 这是6.1的一部分，验证生成的Markdown包含URL
  Testable: yes - property (can merge with 6.1)

**Requirement 7: 错误处理和重试**

7.1 WHEN 页面加载超时，THE Crawler_System SHALL 记录错误并继续处理下一个URL
  Thoughts: 这涉及到实际的网络请求和超时处理，难以在单元测试中验证
  Testable: no

7.2 WHEN 页面返回404或其他错误状态码，THE Crawler_System SHALL 记录错误并标记该URL为失败
  Thoughts: 这涉及到实际的HTTP请求，难以在单元测试中验证
  Testable: no

7.3 WHEN 网络连接失败，THE Crawler_System SHALL 记录错误并将URL标记为待重试
  Thoughts: 这涉及到实际的网络连接，难以在单元测试中验证
  Testable: no

7.4 THE Crawler_System SHALL 为每个URL设置合理的超时时间
  Thoughts: 这是配置验证的一部分，可以验证超时配置是否被正确应用
  Testable: yes - example

7.5 THE Crawler_System SHALL 在请求之间添加延迟以避免被封禁
  Thoughts: 这涉及到时序控制，难以在单元测试中验证
  Testable: no

7.6 THE Crawler_System SHALL 记录所有错误信息到日志文件
  Thoughts: 这是关于日志记录的规则，可以验证日志是否被正确写入
  Testable: yes - property

**Requirement 8: 进度跟踪和日志**

8.1 THE Crawler_System SHALL 在控制台输出当前爬取进度（已完成/总数）
  Thoughts: 这是关于输出格式的规则，可以验证输出内容
  Testable: yes - example

8.2 THE Crawler_System SHALL 输出每个URL的处理状态（成功、失败、跳过）
  Thoughts: 这是关于日志内容的规则，可以验证日志包含状态信息
  Testable: yes - property

8.3 THE Crawler_System SHALL 记录发现的新链接数量
  Thoughts: 这是关于统计信息的规则，可以验证统计数据正确
  Testable: yes - property

8.4 THE Crawler_System SHALL 记录每个页面的解析结果摘要
  Thoughts: 这是关于日志内容的规则，可以验证日志包含摘要信息
  Testable: yes - property

8.5 THE Crawler_System SHALL 在爬取完成后输出统计信息（总数、成功数、失败数）
  Thoughts: 这是关于统计报告的规则，可以验证统计数据正确
  Testable: yes - property

8.6 THE Crawler_System SHALL 将详细日志写入日志文件
  Thoughts: 这与7.6重复
  Testable: yes - property (redundant with 7.6)

**Requirement 9: 代码组织和可维护性**

9.1 THE Crawler_System SHALL 将不同功能模块分离到独立的文件中
  Thoughts: 这是关于代码组织的要求，不是功能性需求
  Testable: no

9.2 THE Crawler_System SHALL 使用清晰的目录结构组织代码
  Thoughts: 这是关于代码组织的要求，不是功能性需求
  Testable: no

9.3 THE Crawler_System SHALL 为每个模块提供清晰的接口定义
  Thoughts: 这是关于代码设计的要求，不是功能性需求
  Testable: no

9.4 THE Crawler_System SHALL 使用一致的命名约定
  Thoughts: 这是关于代码风格的要求，不是功能性需求
  Testable: no

9.5 THE Crawler_System SHALL 包含必要的代码注释和文档
  Thoughts: 这是关于文档的要求，不是功能性需求
  Testable: no

9.6 THE Crawler_System SHALL 将配置、代码和输出分离到不同的目录
  Thoughts: 这是关于目录结构的要求，不是功能性需求
  Testable: no

**Requirement 10: 浏览器自动化**

10.1 THE Crawler_System SHALL 使用Playwright进行浏览器自动化
  Thoughts: 这是技术选型，不是功能性需求
  Testable: no

10.2 THE Crawler_System SHALL 支持等待页面加载完成（networkidle状态）
  Thoughts: 这涉及到实际的浏览器操作，难以在单元测试中验证
  Testable: no

10.3 THE Crawler_System SHALL 支持执行JavaScript代码以操作页面
  Thoughts: 这涉及到实际的浏览器操作，难以在单元测试中验证
  Testable: no

10.4 THE Crawler_System SHALL 支持点击按钮、展开菜单等交互操作
  Thoughts: 这涉及到实际的浏览器操作，难以在单元测试中验证
  Testable: no

10.5 WHERE 配置指定，THE Crawler_System SHALL 支持headless和有头模式
  Thoughts: 这是配置选项，可以验证配置是否被正确应用
  Testable: yes - example

10.6 THE Crawler_System SHALL 在爬取完成后正确关闭浏览器资源
  Thoughts: 这涉及到资源管理，难以在单元测试中验证
  Testable: no

### Property Reflection

经过分析，我发现以下冗余属性需要合并或移除：

1. **URL过滤属性**：1.2和4.5都测试URL过滤功能，可以合并为一个属性
2. **链接添加属性**：2.2和4.6都测试添加链接功能，可以合并为一个属性
3. **表格解析属性**：5.1和5.2都测试表格解析，可以合并为一个综合属性
4. **Markdown生成属性**：6.1、6.2、6.3、6.6都测试Markdown生成的不同方面，可以合并为一个综合属性
5. **日志记录属性**：7.6和8.6都测试日志记录，可以合并为一个属性
6. **统计信息属性**：8.3和8.5都测试统计信息，可以合并为一个属性

### Properties

**Property 1: 配置文件解析完整性**

*For any* valid configuration file, parsing the configuration should return a Config object that contains all required fields (name, seedUrls, urlRules, crawler, output)

**Validates: Requirements 1.1**

**Property 2: URL规则过滤正确性**

*For any* URL list and URL filtering rules (include/exclude patterns), all URLs in the filtered result should match at least one include pattern and not match any exclude pattern

**Validates: Requirements 1.2, 4.5**

**Property 3: 种子链接初始化**

*For any* configuration with seed URLs, when initializing the Link Manager with an empty links file, the resulting link list should contain exactly the seed URLs from the configuration

**Validates: Requirements 1.3**

**Property 4: 无效配置错误处理**

*For any* configuration file with missing required fields or invalid format, the Config Manager should return a descriptive error message indicating which field is invalid

**Validates: Requirements 1.5**

**Property 5: 链接文件读写一致性**

*For any* list of links, saving the links to a file and then loading them back should produce an equivalent list (round-trip property)

**Validates: Requirements 2.1, 2.2**

**Property 6: URL去重不变性**

*For any* link list containing duplicate URLs, after deduplication, the resulting list should contain no duplicate URLs and preserve at least one instance of each unique URL

**Validates: Requirements 2.3**

**Property 7: URL排序不变性**

*For any* link list, after sorting, the resulting list should be in lexicographic order

**Validates: Requirements 2.4**

**Property 8: 链接状态更新正确性**

*For any* link and new status value, after updating the link's status, querying the link should return the new status

**Validates: Requirements 2.6**

**Property 9: 登录表单检测准确性**

*For any* HTML page containing a password input field and a submit button, the Login Handler should correctly identify it as a login page

**Validates: Requirements 3.1**

**Property 10: 多格式登录表单识别**

*For any* login form using different input field types (phone, email, username), the Login Handler should correctly identify and locate the username input field

**Validates: Requirements 3.3**

**Property 11: 链接提取完整性**

*For any* HTML page and URL rules, all extracted links should be valid absolute URLs that match the URL rules

**Validates: Requirements 4.1**

**Property 12: 相对URL转换正确性**

*For any* relative URL and base URL, converting the relative URL to absolute should produce a valid absolute URL that resolves correctly relative to the base

**Validates: Requirements 4.4**

**Property 13: 表格解析完整性**

*For any* HTML table with headers and data rows, the parsed Table object should contain all headers and all data rows in the correct order

**Validates: Requirements 5.1, 5.2**

**Property 14: 文本内容提取正确性**

*For any* HTML page with title and description elements, the extracted title and description should match the content of those elements

**Validates: Requirements 5.4**

**Property 15: 代码块识别准确性**

*For any* HTML page containing code blocks (pre/code elements or textareas with JSON/XML), all code blocks should be correctly identified and extracted with their content

**Validates: Requirements 5.5**

**Property 16: Markdown生成格式正确性**

*For any* PageData object, the generated Markdown should contain the title as a heading, all tables in Markdown table format, all code blocks in Markdown code block format, and the original URL

**Validates: Requirements 6.1, 6.2, 6.3, 6.6**

**Property 17: Markdown文件生成唯一性**

*For any* PageData object, generating a Markdown file should create exactly one file with a unique filename based on the page title

**Validates: Requirements 6.4**

**Property 18: 文件名安全性**

*For any* string containing special characters (/, \, ?, *, :, ", <, >, |), the safe filename function should return a string with all special characters replaced by underscores

**Validates: Requirements 6.5**

**Property 19: 错误日志记录完整性**

*For any* error that occurs during crawling, the error should be logged with the URL, error message, and timestamp

**Validates: Requirements 7.6, 8.6**

**Property 20: 统计信息准确性**

*For any* crawling session, the generated statistics should accurately reflect the total number of URLs, successfully crawled URLs, failed URLs, and new links discovered

**Validates: Requirements 8.3, 8.5**

## Error Handling

### Error Categories

1. **Configuration Errors**
   - Missing required fields
   - Invalid JSON format
   - Invalid regex patterns in URL rules
   - Missing or inaccessible file paths

2. **Network Errors**
   - Connection timeout
   - DNS resolution failure
   - HTTP error status codes (404, 500, etc.)
   - SSL/TLS certificate errors

3. **Parsing Errors**
   - Malformed HTML
   - Missing expected elements
   - Invalid table structure
   - Encoding issues

4. **File System Errors**
   - Permission denied
   - Disk full
   - Invalid file path
   - File already exists (when not expected)

5. **Browser Errors**
   - Browser launch failure
   - Page crash
   - JavaScript execution error
   - Navigation timeout

### Error Handling Strategies

**Configuration Errors**:
- Validate configuration on startup
- Provide detailed error messages indicating which field is invalid
- Exit gracefully with non-zero exit code

**Network Errors**:
- Log error with URL and error details
- Mark URL as failed in Link Manager
- Continue processing remaining URLs
- Support retry mechanism with exponential backoff

**Parsing Errors**:
- Log warning with URL and error details
- Save partial results if any data was extracted
- Mark URL as completed (not failed) to avoid retry
- Continue processing remaining URLs

**File System Errors**:
- Log error with file path and error details
- For output errors: retry once, then skip
- For input errors (config, links.txt): exit gracefully
- Ensure output directory exists before writing

**Browser Errors**:
- Log error with details
- Attempt to restart browser (up to max retries)
- If browser cannot be started: exit gracefully
- For page-level errors: close page and continue

### Error Recovery

**Retry Logic**:
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.pow(2, i) * 1000; // Exponential backoff
      await sleep(delay);
    }
  }
}
```

**Graceful Degradation**:
- If login fails: continue without authentication (may get limited content)
- If tab extraction fails: save content from current tab only
- If table parsing fails: save raw text content
- If Markdown generation fails: save raw HTML

## Testing Strategy

### Dual Testing Approach

本系统采用单元测试和属性测试相结合的策略：

**Unit Tests**：
- 验证特定示例和边缘情况
- 测试错误条件和异常处理
- 测试模块间的集成点
- 使用Jest作为测试框架

**Property-Based Tests**：
- 验证通用属性在所有输入下都成立
- 使用fast-check库进行属性测试
- 每个属性测试运行至少100次迭代
- 每个测试标注对应的设计属性编号

### Testing Configuration

**Property Test Setup**:
```javascript
import fc from 'fast-check';

// 每个属性测试至少100次迭代
const testConfig = { numRuns: 100 };

// 测试标注格式
// Feature: stock-website-crawler, Property 1: 配置文件解析完整性
```

### Test Coverage by Module

**Config Manager**:
- Unit tests: 有效配置示例、无效配置示例
- Property tests: Property 1, 4

**Link Manager**:
- Unit tests: 空文件处理、文件不存在处理
- Property tests: Property 5, 6, 7, 8

**Login Handler**:
- Unit tests: 常见登录表单示例
- Property tests: Property 9, 10

**Link Finder**:
- Unit tests: 空页面、无链接页面
- Property tests: Property 11, 12

**Page Parser**:
- Unit tests: 空表格、单行表格、特殊字符处理
- Property tests: Property 13, 14, 15

**Markdown Generator**:
- Unit tests: 空内容、单个表格、单个代码块
- Property tests: Property 16, 17, 18

**Main Controller**:
- Unit tests: 空链接列表、单个URL处理
- Property tests: Property 19, 20

### Integration Testing

虽然本系统主要关注单元测试和属性测试，但以下集成测试也很重要：

- 完整爬取流程测试（使用本地测试服务器）
- 登录流程测试（使用模拟登录页面）
- 多页面爬取测试（验证链接发现和递归爬取）

这些集成测试应该标记为可选，因为它们需要额外的测试基础设施。

### Test Data Generation

**Generators for Property Tests**:
```javascript
// URL生成器
const urlArbitrary = fc.webUrl();

// 配置对象生成器
const configArbitrary = fc.record({
  name: fc.string(),
  seedUrls: fc.array(fc.webUrl(), { minLength: 1 }),
  urlRules: fc.record({
    include: fc.array(fc.string()),
    exclude: fc.array(fc.string())
  }),
  // ... 其他字段
});

// HTML表格生成器
const tableArbitrary = fc.record({
  headers: fc.array(fc.string(), { minLength: 1 }),
  rows: fc.array(fc.array(fc.string()))
});
```
