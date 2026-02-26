# URL Pattern Analyzer

分析links.txt中的URL，识别URL模式并分组。

## 功能

- **读取links.txt文件**: 解析JSON格式的URL记录
- **提取URL特征**: 协议、主机、路径段、查询参数、路径深度
- **计算URL相似度**: 基于路径和参数的相似度评分
- **URL聚类**: 基于URL正则匹配和后端渲染判断
- **生成正则表达式**: 为URL组生成匹配模式
- **统计分析**: 提供URL状态和错误统计

## 安装

```bash
npm install
```

## 使用

### 完整工作流

```javascript
const LinksReader = require('./lib/links-reader');
const URLPatternAnalyzer = require('./lib/url-clusterer');

// 1. 读取links.txt文件
const reader = new LinksReader();
const records = await reader.readLinksFile('path/to/links.txt');

// 2. 提取有效的URL
const urls = reader.extractURLs(records, { 
  status: 'fetched', 
  excludeErrors: true 
});

// 3. URL聚类分析
const analyzer = new URLPatternAnalyzer();
const clusters = analyzer.clusterURLs(urls);

// 4. 为每个簇生成正则表达式
clusters.forEach(cluster => {
  const pattern = analyzer.generatePattern(cluster);
  console.log(pattern);
});
```

### LinksReader API

```javascript
const LinksReader = require('./lib/links-reader');
const reader = new LinksReader();

// 读取links.txt文件
const records = await reader.readLinksFile('path/to/links.txt');
// 返回: [{ url, status, addedAt, retryCount, error, fetchedAt }, ...]

// 提取URL列表
const allUrls = reader.extractURLs(records);
const fetchedUrls = reader.extractURLs(records, { status: 'fetched' });
const noErrorUrls = reader.extractURLs(records, { excludeErrors: true });

// 获取统计信息
const stats = reader.getStatistics(records);
// 返回: { total, byStatus: {}, withErrors, withoutUrl }
```

### URLPatternAnalyzer API

```javascript
const URLPatternAnalyzer = require('./lib/url-clusterer');
const analyzer = new URLPatternAnalyzer();

// 提取URL特征
const features = analyzer.extractFeatures('https://www.lixinger.com/open/api/doc?api-key=cn/company');
console.log(features);
// {
//   protocol: 'https',
//   host: 'www.lixinger.com',
//   pathSegments: ['open', 'api', 'doc'],
//   queryParams: ['api-key'],
//   pathDepth: 3
// }

// 计算URL相似度
const url1 = 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
const url2 = 'https://www.lixinger.com/open/api/doc?api-key=hk/index';
const similarity = analyzer.calculateSimilarity(url1, url2);
console.log(similarity); // 55

// URL聚类
const urls = [
  'https://www.lixinger.com/open/api/doc?api-key=cn/company',
  'https://www.lixinger.com/open/api/doc?api-key=hk/index',
  'https://www.lixinger.com/analytics/company/dashboard',
  'https://www.lixinger.com/analytics/index/dashboard'
];
const clusters = analyzer.clusterURLs(urls);
console.log(clusters);
// [
//   [
//     'https://www.lixinger.com/open/api/doc?api-key=cn/company',
//     'https://www.lixinger.com/open/api/doc?api-key=hk/index'
//   ],
//   [
//     'https://www.lixinger.com/analytics/company/dashboard',
//     'https://www.lixinger.com/analytics/index/dashboard'
//   ]
// ]
```

### 运行测试

```bash
# 运行单元测试
npm test

# 运行演示脚本
node test/test-analyzer.js
```

## API 文档

### LinksReader

#### `readLinksFile(filePath)`

读取JSON格式的links.txt文件。

**参数:**
- `filePath` (string): links.txt文件路径

**返回:**
- `Promise<Array>`: URL记录数组，每个记录包含:
  - `url` (string): URL地址
  - `status` (string): 状态（如 'fetched', 'pending', 'unfetched'）
  - `addedAt` (number): 添加时间戳
  - `retryCount` (number): 重试次数
  - `error` (string|null): 错误信息
  - `fetchedAt` (number): 抓取时间戳

**错误处理:**
- 文件不存在: 抛出 "Links file not found" 错误
- 权限不足: 抛出 "Permission denied" 错误
- JSON格式错误: 跳过错误行，记录警告，继续处理其他行

**示例:**
```javascript
const records = await reader.readLinksFile('stock-crawler/output/lixinger-crawler/links.txt');
console.log(`读取 ${records.length} 条记录`);
```

#### `extractURLs(records, options)`

从记录中提取URL列表。

**参数:**
- `records` (Array): URL记录数组
- `options` (Object): 过滤选项
  - `status` (string): 只包含特定状态的URL
  - `excludeErrors` (boolean): 排除有错误的URL

**返回:**
- `Array<string>`: URL字符串数组

**示例:**
```javascript
// 提取所有URL
const allUrls = reader.extractURLs(records);

// 只提取已抓取的URL
const fetchedUrls = reader.extractURLs(records, { status: 'fetched' });

// 排除有错误的URL
const noErrorUrls = reader.extractURLs(records, { excludeErrors: true });

// 组合条件
const validUrls = reader.extractURLs(records, { 
  status: 'fetched', 
  excludeErrors: true 
});
```

#### `getStatistics(records)`

获取URL记录的统计信息。

**参数:**
- `records` (Array): URL记录数组

**返回:**
- `Object`: 统计信息对象
  - `total` (number): 总记录数
  - `byStatus` (Object): 按状态统计，如 { fetched: 100, pending: 50 }
  - `withErrors` (number): 有错误的记录数
  - `withoutUrl` (number): 缺少URL字段的记录数

**示例:**
```javascript
const stats = reader.getStatistics(records);
console.log(`总记录: ${stats.total}`);
console.log(`已抓取: ${stats.byStatus.fetched}`);
console.log(`有错误: ${stats.withErrors}`);
```

### URLPatternAnalyzer

#### `extractFeatures(url)`

提取URL特征。

**参数:**
- `url` (string|URL): URL字符串或URL对象

**返回:**
- `Object`: 包含以下属性的特征对象
  - `protocol` (string): 协议（如 'https'）
  - `host` (string): 主机名（如 'www.lixinger.com'）
  - `pathSegments` (Array<string>): 路径段数组
  - `queryParams` (Array<string>): 查询参数键数组
  - `pathDepth` (number): 路径深度

### `calculateSimilarity(url1, url2)`

计算两个URL的相似度分数。

**参数:**
- `url1` (string|URL): 第一个URL
- `url2` (string|URL): 第二个URL

**返回:**
- `number`: 相似度分数
  - 协议和主机不同: 0
  - 路径深度相同: +20
  - 每个匹配的路径段: +10
  - 每个匹配的查询参数: +5

### `clusterURLs(urls)`

对URL列表进行聚类，将相似的URL分组。

**算法**:
- 使用层次聚类（Hierarchical Clustering）
- 基于相似度分数动态决定分组
- 不使用固定阈值，而是使用动态阈值（最小30分）
- 迭代合并最相似的簇，直到无法再合并

**参数:**
- `urls` (Array<string>): URL字符串数组

**返回:**
- `Array<Array<string>>`: 聚类结果，每个元素是一个URL数组（簇）
  - 簇按大小降序排列（最大的簇在前）
  - 每个簇包含相似的URL

**聚类规则:**
- 相似度 ≥ 30分的URL会被聚在一起
- 30分 = 路径深度相同(20分) + 至少一个路径段匹配(10分)
- 协议或主机不同的URL不会聚在一起（相似度为0）

**示例:**
```javascript
const urls = [
  'https://www.lixinger.com/open/api/doc?api-key=cn/company',
  'https://www.lixinger.com/open/api/doc?api-key=hk/index',
  'https://www.lixinger.com/analytics/company/dashboard',
  'https://www.lixinger.com/analytics/index/dashboard'
];

const clusters = analyzer.clusterURLs(urls);
// 返回:
// [
//   [  // 簇1: API文档 (4个URL)
//     'https://www.lixinger.com/open/api/doc?api-key=cn/company',
//     'https://www.lixinger.com/open/api/doc?api-key=hk/index'
//   ],
//   [  // 簇2: Dashboard (2个URL)
//     'https://www.lixinger.com/analytics/company/dashboard',
//     'https://www.lixinger.com/analytics/index/dashboard'
//   ]
// ]
```

### `generatePattern(urlGroup)`

为URL组生成正则表达式模式。

**参数:**
- `urlGroup` (Array<string>): URL字符串数组

**返回:**
- `Object`: 包含以下属性的模式对象
  - `pattern` (string): 正则表达式字符串
  - `pathTemplate` (string): 路径模板（如 '/open/api/{param2}'）
  - `queryParams` (Array<string>): 查询参数键数组

**算法:**
- 分析URL组，识别固定部分和变化部分
- 固定段保持不变，变化段用捕获组 `([^/]+)` 表示
- 查询参数使用宽松匹配 `(\\?.*)?`

**示例:**
```javascript
const urlGroup = [
  'https://www.lixinger.com/open/api/doc?api-key=cn/company',
  'https://www.lixinger.com/open/api/doc?api-key=hk/index'
];

const pattern = analyzer.generatePattern(urlGroup);
// 返回:
// {
//   pattern: '^https://www\\.lixinger\\.com/open/api/([^/]+)(\\?.*)?$',
//   pathTemplate: '/open/api/{param2}',
//   queryParams: ['api-key']
// }
```

## 运行测试

```bash
# 运行LinksReader单元测试
node test/links-reader.test.js

# 运行URLPatternAnalyzer单元测试
npm test

# 测试真实links.txt文件
node test/test-real-links.js

# 运行集成测试
node test/test-integration.js

# 运行演示脚本
node test/test-analyzer.js
```

## 测试覆盖

项目包含完整的测试套件：

### LinksReader 测试
- ✓ 读取有效的links文件
- ✓ 处理格式错误的行（跳过并继续）
- ✓ 提取URL列表（支持多种过滤条件）
- ✓ 获取统计信息
- ✓ 文件不存在错误处理
- ✓ 空文件处理
- ✓ 只有空行的文件处理

### URLPatternAnalyzer 测试
- ✓ URL特征提取（字符串和URL对象）
- ✓ 处理无查询参数的URL
- ✓ 处理多个查询参数
- ✓ 处理根路径
- ✓ 过滤空路径段
- ✓ 相似度计算（相同路径、不同协议、不同主机、部分匹配等）
- ✓ URL聚类算法
- ✓ 正则表达式生成

### 集成测试
- ✓ 完整工作流：读取 → 提取 → 聚类 → 生成模式
- ✓ 使用真实的8000+条URL数据测试

## 设计原则

- **不使用固定阈值**: 相似度计算返回分数，由聚类算法决定分组
- **基于URL正则匹配**: 判断URL是否属于同一模式
- **后端渲染判断**: 判断页面是否由同一个后端模板渲染
- **错误容忍**: 格式错误的行会被跳过，不影响整体处理
- **灵活过滤**: 支持按状态、错误等多种条件过滤URL

## 文件结构

```
skills/url-pattern-analyzer/
├── lib/
│   ├── url-clusterer.js      # URL聚类和模式识别
│   └── links-reader.js        # links.txt文件读取器
├── test/
│   ├── url-clusterer.test.js  # URLPatternAnalyzer单元测试
│   ├── links-reader.test.js   # LinksReader单元测试
│   ├── test-real-links.js     # 真实数据测试
│   ├── test-integration.js    # 集成测试
│   └── test-analyzer.js       # 演示脚本
├── README.md
├── package.json
└── skill.json
```

## 下一步

- [x] 实现 `readLinksFile()` 方法
- [x] 实现 `extractURLs()` 方法
- [x] 实现 `getStatistics()` 方法
- [x] 实现 `clusterURLs()` 方法
- [x] 实现 `generatePattern()` 方法
- [ ] 创建主入口文件 `main.js`
- [ ] 集成到完整的分析工作流
- [ ] 生成JSON和Markdown格式的分析报告
