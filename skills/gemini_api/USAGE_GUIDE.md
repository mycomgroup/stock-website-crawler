# Gemini API 使用指南

## 快速开始（5 分钟）

### 1. 安装

```bash
cd skills/gemini_api
npm install
```

### 2. 首次登录

```bash
node run-skill.js --login
```

浏览器会自动打开 Gemini 登录页面，使用你的 Google 账号登录。脚本会等待 5 分钟让你完成登录。

### 3. 发送第一条消息

```bash
node run-skill.js --message "你好，Gemini！"
```

## 常用命令

### 消息发送

```bash
# 单条消息
node run-skill.js --message "解释一下量子计算"

# 从文件读取
node run-skill.js --file examples/example-prompt.txt

# 批量发送（每行一条）
node run-skill.js --batch examples/batch-questions.txt

# 指定模型
node run-skill.js --message "分析这张图片" --model gemini-pro-vision

# 继续已有对话
node run-skill.js --message "继续上面的话题" --conversation conv-abc123
```

### 对话管理

```bash
# 列出最近 10 个对话
node run-skill.js --list

# 列出所有对话
node run-skill.js --list-all

# 搜索对话
node run-skill.js --search "量子计算"

# 查看对话详情
node run-skill.js --show conv-abc123

# 删除对话
node run-skill.js --delete conv-abc123
```

### Session 管理

```bash
# 验证 session 是否有效
node run-skill.js --validate

# 强制重新登录
node run-skill.js --login --force

# 使用有头模式（显示浏览器窗口）
node run-skill.js --login --headed
```

### 模型和账户

```bash
# 列出可用模型
node run-skill.js --models

# 查看账户信息
node run-skill.js --account
```

## 多账号管理

### 添加账号

```bash
# 添加第一个账号
node run-skill.js --add-account "主账号"

# 添加第二个账号
node run-skill.js --add-account "备用账号"

# 添加第三个账号
node run-skill.js --add-account "测试账号"
```

每次添加账号时，都会打开浏览器让你登录。

### 管理账号

```bash
# 查看所有账号
node run-skill.js --list-accounts

# 验证所有账号
node run-skill.js --validate-accounts

# 查看账号统计
node run-skill.js --account-stats

# 启用账号
node run-skill.js --enable-account account-xxx

# 禁用账号
node run-skill.js --disable-account account-xxx

# 删除账号
node run-skill.js --remove-account account-xxx
```

### 负载均衡

```bash
# 设置负载均衡策略
node run-skill.js --set-strategy round-robin    # 轮询（默认）
node run-skill.js --set-strategy weighted       # 加权轮询
node run-skill.js --set-strategy least-used     # 最少使用
node run-skill.js --set-strategy least-recent   # 最久未使用

# 设置账号权重（仅在 weighted 策略下有效）
node run-skill.js --set-weight account-xxx 2
```

## OpenAI 兼容服务器

### 启动服务器

```bash
# 单账号模式
node server/openai-compatible-server.js

# 多账号模式（推荐）
USE_MULTI_ACCOUNT=true node server/openai-compatible-server.js

# 自定义端口和 API Key
PORT=8080 API_KEY=my-secret-key node server/openai-compatible-server.js
```

### 使用 curl 测试

```bash
curl http://localhost:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-gemini-proxy" \
  -d '{
    "model": "gemini-pro",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### 使用 OpenAI SDK

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: "sk-gemini-proxy",
  baseURL: "http://localhost:3000/v1"
});

// 非流式
const completion = await openai.chat.completions.create({
  model: "gemini-pro",
  messages: [{ role: "user", content: "你好" }]
});

console.log(completion.choices[0].message.content);

// 流式
const stream = await openai.chat.completions.create({
  model: "gemini-pro",
  messages: [{ role: "user", content: "你好" }],
  stream: true
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || "");
}
```

### 使用 Python OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-gemini-proxy",
    base_url="http://localhost:3000/v1"
)

response = client.chat.completions.create(
    model="gemini-pro",
    messages=[{"role": "user", "content": "你好"}]
)

print(response.choices[0].message.content)
```

## 编程方式使用

### 基础使用

```javascript
import { GeminiClient } from './request/gemini-client.js';

const client = new GeminiClient();

// 发送消息
const response = await client.sendMessage({
  message: "解释一下量子计算",
  model: "gemini-pro"
});

console.log(response.content);
console.log(response.conversationId);
```

### 使用 MessageSender

```javascript
import { sendMessage, sendBatchMessages } from './request/message-sender.js';

// 发送单条消息
await sendMessage("你好", { model: "gemini-pro" });

// 批量发送
const messages = [
  "什么是量子计算？",
  "什么是机器学习？",
  "什么是区块链？"
];

await sendBatchMessages(messages, {
  model: "gemini-pro",
  delay: 2000  // 每条消息间隔 2 秒
});
```

### 多账号管理

```javascript
import { MultiAccountManager } from './browser/multi-account-manager.js';

const manager = new MultiAccountManager();

// 获取下一个可用账号
const account = manager.getNextAccount();

// 使用账号
manager.useAccount(account);

// 获取统计信息
const stats = manager.getStats();
console.log(`总账号数: ${stats.total}`);
console.log(`有效账号: ${stats.active}`);
```

## 环境变量配置

创建 `.env` 文件：

```env
# 默认模型
DEFAULT_MODEL=gemini-pro

# Chrome Profile 路径（可选）
CHROME_PROFILE_PATH=/Users/username/Library/Application Support/Google/Chrome/Default

# 是否使用无头模式（登录时始终显示浏览器）
HEADLESS=false

# OpenAI 服务器配置
PORT=3000
API_KEY=sk-gemini-proxy
USE_MULTI_ACCOUNT=false
```

## 可用模型

| 模型 | 说明 | 适用场景 |
|------|------|----------|
| gemini-pro | 最强大的文本模型 | 复杂任务、长文本生成 |
| gemini-pro-vision | 多模态模型 | 图像分析、图文结合 |

## 负载均衡策略

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| round-robin | 轮询，依次使用每个账号 | 账号性能相同 |
| weighted | 加权轮询，根据权重分配 | 账号性能不同 |
| least-used | 使用请求数最少的账号 | 均衡负载 |
| least-recent | 使用最久未使用的账号 | 避免频繁使用同一账号 |

## 常见问题

### Session 失效

```bash
# 重新登录
node run-skill.js --login --force
```

### 多账号验证失败

```bash
# 验证所有账号
node run-skill.js --validate-accounts

# 删除失效账号
node run-skill.js --remove-account <id>

# 重新添加
node run-skill.js --add-account
```

### 查看详细日志

```bash
# 使用有头模式查看浏览器操作
node run-skill.js --login --headed
```

### API 端点错误

如果遇到 API 请求失败，可能需要更新 `request/gemini-client.js` 中的 API 端点。

## 数据文件

所有数据存储在 `data/` 目录：

```
data/
├── session.json              # 单账号 session
├── accounts/                 # 多账号数据
│   ├── session-xxx.json     # 账号 session
│   └── ...
├── accounts-config.json      # 账号配置
└── history-2026-04-06.jsonl # 历史记录
```

⚠️ **注意**: 不要将 `data/` 目录提交到 git，已在 `.gitignore` 中排除。

## 性能建议

1. **批量发送**: 使用 `--batch` 而不是多次单独发送
2. **设置延迟**: 批量发送时设置适当的延迟（1-2 秒）
3. **多账号**: 使用多账号可以提高并发能力
4. **负载均衡**: 根据实际情况选择合适的负载均衡策略

## 安全建议

1. **保护 Session**: `data/session.json` 包含敏感信息，不要分享
2. **API Key**: 使用强密码作为 API Key
3. **访问控制**: 如果暴露到公网，添加访问控制
4. **定期更新**: 定期重新登录以刷新 session

## 集成示例

### 与 LangChain 集成

```javascript
import { ChatOpenAI } from "langchain/chat_models/openai";

const chat = new ChatOpenAI({
  openAIApiKey: "sk-gemini-proxy",
  configuration: {
    baseURL: "http://localhost:3000/v1"
  }
});

const response = await chat.call([
  { role: "user", content: "你好" }
]);
```

### 与 LlamaIndex 集成

```python
from llama_index.llms import OpenAI

llm = OpenAI(
    api_key="sk-gemini-proxy",
    api_base="http://localhost:3000/v1"
)

response = llm.complete("你好")
print(response)
```

## 更多资源

- [README.md](./README.md) - 项目概述
- [API_REFERENCE.md](./API_REFERENCE.md) - API 详细文档
- [MULTI_ACCOUNT.md](./MULTI_ACCOUNT.md) - 多账号管理详解
- [OPENAI_SERVER.md](./OPENAI_SERVER.md) - OpenAI 服务器详解
- [TECHNICAL_DETAILS.md](./TECHNICAL_DETAILS.md) - 技术实现细节

---

**最后更新**: 2026-04-06
