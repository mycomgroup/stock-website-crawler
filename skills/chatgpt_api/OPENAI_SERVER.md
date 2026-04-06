# OpenAI 兼容 API 服务器

## 概述

将 ChatGPT session 转换为标准的 OpenAI API 接口，让任何支持 OpenAI API 的应用都可以使用。

## 特性

- ✅ 完全兼容 OpenAI API 格式
- ✅ 支持流式和非流式响应
- ✅ 支持多种模型
- ✅ 简单的 API Key 认证
- ✅ CORS 支持
- ✅ 健康检查端点

## 快速开始

### 1. 确保已登录

```bash
node run-skill.js --login
```

### 2. 启动服务器

```bash
node server/openai-compatible-server.js
```

服务器将在 `http://localhost:3000` 启动。

### 3. 测试服务器

```bash
# 在另一个终端
node server/test-openai-client.js
```

## API 端点

### POST /v1/chat/completions

发送聊天消息

**请求:**
```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "你好"}
  ],
  "stream": false
}
```

**响应:**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "gpt-4",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "你好！我是 ChatGPT..."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

### GET /v1/models

获取可用模型列表

**响应:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4",
      "object": "model",
      "created": 1234567890,
      "owned_by": "openai"
    }
  ]
}
```

### GET /health

健康检查

**响应:**
```json
{
  "status": "ok"
}
```

## 使用方式

### 1. cURL

```bash
curl http://localhost:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-chatgpt-proxy" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'
```

### 2. OpenAI SDK (Node.js)

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'sk-chatgpt-proxy',
  baseURL: 'http://localhost:3000/v1'
});

// 非流式
const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [
    { role: 'user', content: '你好' }
  ]
});

console.log(completion.choices[0].message.content);

// 流式
const stream = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [
    { role: 'user', content: '你好' }
  ],
  stream: true
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

### 3. OpenAI SDK (Python)

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-chatgpt-proxy",
    base_url="http://localhost:3000/v1"
)

# 非流式
completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)

print(completion.choices[0].message.content)

# 流式
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "你好"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### 4. Fetch API

```javascript
const response = await fetch('http://localhost:3000/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-chatgpt-proxy'
  },
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [
      { role: 'user', content: '你好' }
    ]
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

## 配置

### 环境变量

```bash
# 端口（默认 3000）
PORT=3000

# API Key（默认 sk-chatgpt-proxy）
API_KEY=your-custom-api-key
```

### 使用自定义配置

```bash
PORT=8080 API_KEY=my-secret-key node server/openai-compatible-server.js
```

## 集成示例

### 1. 与 LangChain 集成

```javascript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  openAIApiKey: "sk-chatgpt-proxy",
  configuration: {
    baseURL: "http://localhost:3000/v1"
  },
  modelName: "gpt-4"
});

const response = await model.invoke("你好");
console.log(response.content);
```

### 2. 与 LlamaIndex 集成

```python
from llama_index.llms.openai import OpenAI

llm = OpenAI(
    api_key="sk-chatgpt-proxy",
    api_base="http://localhost:3000/v1",
    model="gpt-4"
)

response = llm.complete("你好")
print(response.text)
```

### 3. 与 AutoGPT 集成

在 `.env` 文件中配置:

```env
OPENAI_API_KEY=sk-chatgpt-proxy
OPENAI_API_BASE=http://localhost:3000/v1
```

### 4. 与 ChatGPT-Next-Web 集成

在设置中配置:

```
API Key: sk-chatgpt-proxy
API 地址: http://localhost:3000
```

## 支持的应用

理论上支持所有使用 OpenAI API 的应用，包括但不限于:

- ✅ OpenAI SDK (官方)
- ✅ LangChain
- ✅ LlamaIndex
- ✅ AutoGPT
- ✅ ChatGPT-Next-Web
- ✅ BetterChatGPT
- ✅ ChatBox
- ✅ OpenCat
- ✅ Bob (翻译工具)
- ✅ Raycast AI
- ✅ Continue (VS Code 插件)
- ✅ Cursor (AI 编辑器)

## 限制

1. **速率限制**: 继承 ChatGPT 的速率限制
2. **模型支持**: 仅支持你的 ChatGPT 账户可用的模型
3. **功能支持**: 不支持 function calling、embeddings 等高级功能
4. **并发**: 单个 session 不支持并发请求

## 故障排查

### 服务器无法启动

```bash
# 检查 session 是否有效
node run-skill.js --validate

# 如果失效，重新登录
node run-skill.js --login
```

### 401 Unauthorized

检查 API Key 是否正确:

```bash
# 默认 API Key
Authorization: Bearer sk-chatgpt-proxy

# 自定义 API Key
API_KEY=your-key node server/openai-compatible-server.js
```

### 端口被占用

```bash
# 使用其他端口
PORT=8080 node server/openai-compatible-server.js
```

### 响应超时

ChatGPT 响应时间较长，建议设置更长的超时时间:

```javascript
const openai = new OpenAI({
  apiKey: 'sk-chatgpt-proxy',
  baseURL: 'http://localhost:3000/v1',
  timeout: 60000 // 60 秒
});
```

## 性能优化

### 1. 使用流式响应

流式响应可以更快地开始显示结果:

```javascript
const stream = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [...],
  stream: true
});
```

### 2. 复用 session

服务器会自动复用 session，无需每次请求都重新登录。

### 3. 并发限制

建议不要并发发送多个请求，使用队列机制:

```javascript
const queue = [];
let processing = false;

async function addToQueue(request) {
  queue.push(request);
  if (!processing) {
    await processQueue();
  }
}

async function processQueue() {
  processing = true;
  while (queue.length > 0) {
    const request = queue.shift();
    await processRequest(request);
  }
  processing = false;
}
```

## 安全建议

1. **不要暴露到公网**: 仅在本地或内网使用
2. **使用强 API Key**: 如果需要暴露，使用复杂的 API Key
3. **添加速率限制**: 防止滥用
4. **使用 HTTPS**: 如果需要远程访问，使用反向代理添加 HTTPS
5. **监控使用**: 记录所有请求日志

## 部署

### Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server/openai-compatible-server.js"]
```

```bash
docker build -t chatgpt-proxy .
docker run -p 3000:3000 -v $(pwd)/data:/app/data chatgpt-proxy
```

### PM2

```bash
pm2 start server/openai-compatible-server.js --name chatgpt-proxy
pm2 save
pm2 startup
```

### Nginx 反向代理

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 高级功能

### 添加请求日志

```javascript
// 在 handleRequest 中添加
console.log(`[${new Date().toISOString()}] ${method} ${url}`);
```

### 添加速率限制

```javascript
const rateLimit = new Map();

function checkRateLimit(apiKey) {
  const now = Date.now();
  const requests = rateLimit.get(apiKey) || [];
  
  // 清理 1 分钟前的请求
  const recent = requests.filter(time => now - time < 60000);
  
  if (recent.length >= 10) {
    return false; // 超过限制
  }
  
  recent.push(now);
  rateLimit.set(apiKey, recent);
  return true;
}
```

### 添加缓存

```javascript
const cache = new Map();

function getCachedResponse(key) {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.time < 300000) { // 5 分钟
    return cached.data;
  }
  return null;
}

function setCachedResponse(key, data) {
  cache.set(key, { data, time: Date.now() });
}
```

## 总结

OpenAI 兼容服务器让你可以在任何支持 OpenAI API 的应用中使用 ChatGPT session，无需修改应用代码。这为集成和自动化提供了极大的便利。
