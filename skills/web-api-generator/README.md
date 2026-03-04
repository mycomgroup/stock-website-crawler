# Web API Generator Skill

将 URL patterns 转换为 API 文档和客户端工具。

## 快速开始

### 方式 1: 使用 main.js（推荐）

```bash
# 生成 API 文档
node main.js generate-docs \
  --patterns=../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output=./output/web-api-docs

# 列出所有 API
node main.js list \
  --patterns=../../stock-crawler/output/lixinger-crawler/url-patterns.json

# 搜索 API
node main.js search \
  --patterns=../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --keyword=公司详情

# 调用 API
node main.js call \
  --patterns=../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --api=detail-sh \
  --param4=600519 \
  --param5=600519
```

### 方式 2: 使用独立脚本

```bash
# 生成文档
node scripts/generate-docs.js

# 使用客户端
node scripts/web-api-client.js list
node scripts/web-api-client.js search 公司详情
node scripts/web-api-client.js detail-sh --param4=600519 --param5=600519
```

## 目录结构

```
skills/web-api-generator/
├── SKILL.md                    # Skill 描述
├── README.md                   # 使用说明
├── main.js                     # 统一入口
├── lib/
│   ├── doc-generator.js        # 文档生成器
│   ├── api-client.js           # API 客户端
│   └── pattern-matcher.js      # Pattern 匹配器
├── scripts/
│   ├── generate-docs.js        # 独立文档生成脚本
│   └── web-api-client.js       # 独立客户端脚本
├── output/                     # 输出目录
│   └── web-api-docs/          # 生成的文档
└── test/                       # 测试文件
```

## 功能特性

1. **文档生成**: 自动生成 API 文档
2. **Pattern 匹配**: 根据关键词搜索 API
3. **实时抓取**: 按需抓取页面数据
4. **结构化输出**: 返回 JSON 格式

## 配置

在项目根目录的 `.env` 文件中配置：

```
LIXINGER_USERNAME=your_username
LIXINGER_PASSWORD=your_password
```

## 示例

### 生成文档

```bash
node main.js generate-docs \
  --patterns=../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output=./output/web-api-docs
```

### 调用 API

```bash
node main.js call \
  --patterns=../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --api=detail-sh \
  --param4=600519 \
  --param5=600519
```

输出：
```json
{
  "success": true,
  "api": "detail-sh",
  "url": "https://www.lixinger.com/analytics/company/detail/sh/600519/600519",
  "data": {
    "title": "贵州茅台(600519)",
    "tables": [...],
    "charts": 5
  }
}
```

## 集成到其他项目

```javascript
import { WebApiClient } from './skills/web-api-generator/lib/api-client.js';

const client = new WebApiClient({
  patternsPath: './url-patterns.json',
  username: process.env.LIXINGER_USERNAME,
  password: process.env.LIXINGER_PASSWORD
});

await client.initialize();
const result = await client.callApi('detail-sh', {
  param4: '600519',
  param5: '600519'
});

console.log(result);
```
