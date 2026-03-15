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

# 交互式调用（按 URL 类型推荐）
node main.js interactive \
  --patterns=../../stock-crawler/output/lixinger-crawler/url-patterns.json
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
5. **字段语义推导**: interactive 模式可调用大模型自动解释参数含义并给建议值

## 配置

在项目根目录的 `.env` 文件中配置：

```
LIXINGER_USERNAME=your_username
LIXINGER_PASSWORD=your_password

# 可选：用于字段语义推导
LLM_API_KEY=your_api_key
LLM_API_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
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


## 新增：交互式 URL 类型调用

当你只知道“URL 类型”或业务语义（如 `company/detail`、`fund`、`行业`），可以使用交互式模式：

```bash
node main.js interactive --patterns=../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

交互流程：
1. 输入 URL 类型/关键词。
2. 系统推荐匹配 API 列表。
3. 选择 API，逐个输入路径参数。
4. 确认后立即调用并返回结构化 JSON。

同时，`call` 命令已支持“路径参数名”和`paramX`混用，方便从文档到实际调用平滑过渡。

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


### 关闭大模型推导（回退规则模式）

```bash
node main.js interactive --useLLM=false
```
