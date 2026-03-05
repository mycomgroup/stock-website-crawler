# HAR 自动化提取工具

自动从网页中提取 API 接口并生成可用的请求代码。

## 功能特性

- ✅ 自动录制 HAR 文件
- ✅ 智能识别数据接口（REST/GraphQL）
- ✅ 生成多种语言代码（Python/Node.js/curl）
- ✅ 自动验证接口可用性
- ✅ 生成 API 文档
- ✅ 检测签名参数
- ✅ 批量处理支持

## 快速开始

### 1. 单个 URL 提取

```bash
# 完整工作流（推荐）
node scripts/auto-extract-workflow.js https://example.com/api example

# 输出目录: output/har-extraction/example/
```

### 2. 分步执行

```bash
# 步骤 1: 录制 HAR
node scripts/record-har.js https://example.com/api output/example.har

# 步骤 2: 提取 API
node scripts/extract-apis.js output/example.har output/apis

# 步骤 3: 验证（可选）
node scripts/validate-apis.js output/example.har
```

### 3. 批量处理

创建 `urls.json`:

```json
[
  { "url": "https://example.com/api/users", "name": "users" },
  { "url": "https://example.com/api/products", "name": "products" }
]
```

执行批量提取:

```bash
node scripts/auto-extract-workflow.js --batch urls.json
```

## 命令详解

### record-har.js - 录制 HAR

```bash
node scripts/record-har.js <url> <output.har> [waitTime]

参数:
  url       - 要访问的 URL
  output    - HAR 文件保存路径
  waitTime  - 等待时间（毫秒），默认 3000

示例:
  node scripts/record-har.js https://api.example.com output/api.har
  node scripts/record-har.js https://api.example.com output/api.har 5000
```

### extract-apis.js - 提取 API

```bash
node scripts/extract-apis.js <har-file> <output-dir> [options]

选项:
  --formats <list>  生成的代码格式，逗号分隔 (默认: python,node,curl)
  --no-class        不生成类文件
  --no-docs         不生成文档

示例:
  node scripts/extract-apis.js output/api.har output/apis
  node scripts/extract-apis.js output/api.har output/apis --formats python,node
```

### validate-apis.js - 验证 API

```bash
node scripts/validate-apis.js <har-file|json-file> [options]

选项:
  --concurrent <n>  并发数 (默认: 3)
  --delay <ms>      请求间隔 (默认: 1000)
  --no-report       不保存报告

示例:
  node scripts/validate-apis.js output/api.har
  node scripts/validate-apis.js output/apis/apis.json --concurrent 5
```

### auto-extract-workflow.js - 完整工作流

```bash
node scripts/auto-extract-workflow.js <url> <name> [options]

选项:
  --output <dir>    输出目录 (默认: output/har-extraction)
  --formats <list>  代码格式 (默认: python,node,curl)
  --no-validate     跳过验证步骤
  --wait <ms>       等待时间 (默认: 3000)

示例:
  node scripts/auto-extract-workflow.js https://api.example.com example
  node scripts/auto-extract-workflow.js https://api.example.com example --no-validate
  
批量模式:
  node scripts/auto-extract-workflow.js --batch urls.json
```

## 输出结构

```
output/har-extraction/example/
├── example.har                 # 录制的 HAR 文件
├── SUMMARY.md                  # 总结文档
├── validation-report.md        # 验证报告
├── validation-report.json      # 验证数据
└── apis/
    ├── README.md               # API 文档
    ├── apis.json               # 原始 API 数据
    ├── api_client.py           # Python 客户端类
    ├── python/                 # Python 代码
    │   ├── api_1_users.py
    │   └── api_2_products.py
    ├── node/                   # Node.js 代码
    │   ├── api_1_users.js
    │   └── api_2_products.js
    └── curl/                   # curl 脚本
        ├── api_1_users.sh
        └── api_2_products.sh
```

## 使用生成的代码

### Python

```python
# 方式 1: 使用单个文件
from api_1_users import *
# 直接运行

# 方式 2: 使用客户端类
from api_client import APIClient

client = APIClient(
    base_url="https://api.example.com",
    headers={"Authorization": "Bearer token"}
)

users = client.get_users()
print(users)
```

### Node.js

```javascript
// 方式 1: 直接运行
node apis/node/api_1_users.js

// 方式 2: 导入使用
import axios from 'axios';
// 复制生成的配置
```

### curl

```bash
# 直接执行
bash apis/curl/api_1_users.sh

# 或复制命令使用
curl -X GET 'https://api.example.com/users' \
  -H 'Authorization: Bearer token'
```

## 高级功能

### 1. 自定义格式

只生成 Python 代码:

```bash
node scripts/extract-apis.js output/api.har output/apis --formats python
```

### 2. 跳过验证

快速提取不验证:

```bash
node scripts/auto-extract-workflow.js https://api.example.com example --no-validate
```

### 3. 调整等待时间

等待更长时间以捕获更多请求:

```bash
node scripts/record-har.js https://api.example.com output/api.har 10000
```

### 4. 控制验证并发

```bash
node scripts/validate-apis.js output/api.har --concurrent 10 --delay 500
```

## 识别的接口类型

工具会自动识别以下类型的接口:

1. **JSON API** - 响应类型为 `application/json`
2. **REST API** - URL 包含 `/api/`, `/data/`, `/v1/` 等
3. **GraphQL** - URL 包含 `graphql` 或请求体包含 `query`

自动排除:

- 静态资源 (.js, .css, .png, .jpg 等)
- HTML 页面
- 字体文件

## 签名检测

工具会自动检测以下签名参数:

- Headers: `sign`, `signature`, `x-sign`, `x-signature`, `auth-sign`
- Query: `sign`, `signature`, `token`

检测到签名会在文档中标注 ⚠️

## 验证报告

验证报告包含:

- 成功率和直连率
- 失败原因分析
- 反爬虫检测
- 每个接口的详细状态

## 常见问题

### Q: 为什么有些接口验证失败？

A: 可能原因:
- 需要认证 (401)
- 反爬虫保护 (403)
- CORS 限制
- 签名验证

### Q: 如何处理需要登录的页面？

A: 修改 `record-har.js`，在访问前先登录:

```javascript
await page.goto('https://example.com/login');
await page.fill('#username', 'user');
await page.fill('#password', 'pass');
await page.click('#submit');
await page.waitForNavigation();
```

### Q: 生成的代码可以直接使用吗？

A: 大部分情况可以，但可能需要:
- 添加认证信息
- 处理签名
- 调整参数

### Q: 如何处理动态参数？

A: 生成的代码包含捕获时的参数值，你需要根据实际需求修改。

## 性能建议

1. **批量处理**: 使用批量模式而不是循环调用
2. **并发控制**: 验证时控制并发数避免被封
3. **延迟设置**: 增加请求间隔避免触发限流
4. **选择性生成**: 只生成需要的代码格式

## 示例场景

### 场景 1: 快速测试单个 API

```bash
node scripts/auto-extract-workflow.js https://api.example.com/users users
cd output/har-extraction/users/apis/python
python api_1_users.py
```

### 场景 2: 批量提取多个站点

```bash
# 创建 urls.json
echo '[
  {"url": "https://site1.com/api", "name": "site1"},
  {"url": "https://site2.com/api", "name": "site2"}
]' > urls.json

# 批量提取
node scripts/auto-extract-workflow.js --batch urls.json

# 查看报告
cat output/har-extraction/BATCH_REPORT.md
```

### 场景 3: 只提取不验证

```bash
node scripts/auto-extract-workflow.js \
  https://api.example.com/data \
  example \
  --no-validate \
  --formats python
```

## 集成到项目

### 作为 npm 脚本

在 `package.json` 中添加:

```json
{
  "scripts": {
    "extract": "node scripts/auto-extract-workflow.js",
    "record": "node scripts/record-har.js",
    "validate": "node scripts/validate-apis.js"
  }
}
```

使用:

```bash
npm run extract https://api.example.com example
```

### 作为模块使用

```javascript
import { AutoExtractWorkflow } from './scripts/auto-extract-workflow.js';

const workflow = new AutoExtractWorkflow({
  outputDir: 'output/custom',
  formats: ['python'],
  validate: false
});

await workflow.run('https://api.example.com', 'myapi');
```

## 贡献

欢迎提交 Issue 和 PR！

## 许可

MIT
