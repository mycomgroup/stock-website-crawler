# ChatGPT API 参考文档

## ChatGPTClient 类

### 初始化

```javascript
import { ChatGPTClient } from './request/chatgpt-client.js';

const client = new ChatGPTClient({
  model: 'gpt-4' // 可选，默认 gpt-4
});
```

## 消息相关

### sendMessage(options)

发送消息到 ChatGPT

**参数:**
```javascript
{
  message: string,              // 必需：消息内容
  model: string,                // 可选：模型名称，默认 gpt-4
  conversationId: string,       // 可选：对话 ID，用于继续对话
  parentMessageId: string       // 可选：父消息 ID
}
```

**返回:**
```javascript
{
  conversationId: string,       // 对话 ID
  messageId: string,            // 消息 ID
  content: string,              // 响应内容
  model: string,                // 使用的模型
  rawResponse: string           // 原始 SSE 响应
}
```

**示例:**
```javascript
const response = await client.sendMessage({
  message: "你好，请介绍一下你自己",
  model: "gpt-4"
});

console.log(response.content);
```

## 对话管理

### getConversations(options)

获取对话列表

**参数:**
```javascript
{
  offset: number,    // 可选：偏移量，默认 0
  limit: number,     // 可选：数量限制，默认 20
  order: string      // 可选：排序方式，默认 'updated'
}
```

**返回:**
```javascript
{
  items: Array,      // 对话列表
  total: number,     // 总数
  limit: number,     // 限制数
  offset: number,    // 偏移量
  hasMore: boolean   // 是否有更多
}
```

**示例:**
```javascript
const result = await client.getConversations({ limit: 10 });

result.items.forEach(conv => {
  console.log(`${conv.title} (${conv.id})`);
});
```

### getConversation(conversationId)

获取特定对话的详细信息

**参数:**
- `conversationId` (string): 对话 ID

**返回:**
```javascript
{
  id: string,
  title: string,
  create_time: number,
  update_time: number,
  mapping: Object,           // 消息映射
  current_node: string,
  conversation_template_id: string
}
```

**示例:**
```javascript
const conv = await client.getConversation('conv-abc123');

console.log(`标题: ${conv.title}`);
console.log(`消息数: ${Object.keys(conv.mapping).length}`);
```

### deleteConversation(conversationId)

删除特定对话

**参数:**
- `conversationId` (string): 对话 ID

**返回:**
```javascript
{
  success: boolean,
  conversationId: string
}
```

**示例:**
```javascript
await client.deleteConversation('conv-abc123');
console.log('对话已删除');
```

### clearConversations()

清空所有对话

**返回:**
```javascript
{
  success: boolean
}
```

**示例:**
```javascript
await client.clearConversations();
console.log('所有对话已清空');
```

### renameConversation(conversationId, title)

重命名对话

**参数:**
- `conversationId` (string): 对话 ID
- `title` (string): 新标题

**返回:**
```javascript
{
  success: boolean,
  conversationId: string,
  title: string
}
```

**示例:**
```javascript
await client.renameConversation('conv-abc123', '关于 JavaScript 的讨论');
console.log('对话已重命名');
```

### searchConversations(query, options)

搜索对话

**参数:**
- `query` (string): 搜索关键词
- `options` (object): 可选参数
  - `limit` (number): 结果数量限制，默认 20

**返回:**
```javascript
Array<{
  id: string,
  title: string,
  create_time: number,
  update_time: number
}>
```

**示例:**
```javascript
const results = await client.searchConversations('JavaScript');

results.forEach(conv => {
  console.log(`找到: ${conv.title}`);
});
```

## 模型和账户

### getModels()

获取可用模型列表

**返回:**
```javascript
Array<{
  slug: string,
  title: string,
  description: string,
  max_tokens: number,
  tags: Array<string>
}>
```

**示例:**
```javascript
const models = await client.getModels();

models.forEach(model => {
  console.log(`${model.slug}: ${model.title}`);
});
```

### getAccountInfo()

获取账户信息

**返回:**
```javascript
{
  email: string,
  name: string,
  picture: string,
  plan_type: string,
  // ... 其他字段
}
```

**示例:**
```javascript
const account = await client.getAccountInfo();

console.log(`邮箱: ${account.email}`);
console.log(`计划: ${account.plan_type}`);
```

## 工具方法

### generateId()

生成 UUID

**返回:** string

**示例:**
```javascript
const id = client.generateId();
console.log(id); // "f0e11982-6003-4384-9b9e-197e26504ad1"
```

### parseSSEResponse(text)

解析 Server-Sent Events 响应

**参数:**
- `text` (string): SSE 响应文本

**返回:**
```javascript
{
  conversationId: string,
  messageId: string,
  content: string,
  model: string,
  rawResponse: string
}
```

## MessageSender 类

### 初始化

```javascript
import { MessageSender } from './request/message-sender.js';

const sender = new MessageSender({
  model: 'gpt-4',           // 可选
  saveHistory: true         // 可选，是否保存历史记录
});
```

### send(message, options)

发送单条消息

**参数:**
- `message` (string): 消息内容
- `options` (object): 可选参数（同 sendMessage）

**返回:** 同 sendMessage

**示例:**
```javascript
const response = await sender.send("你好");
console.log(response.content);
```

### sendBatch(messages, options)

批量发送消息

**参数:**
- `messages` (Array<string>): 消息列表
- `options` (object): 可选参数
  - `delay` (number): 消息间隔（毫秒），默认 2000

**返回:**
```javascript
Array<{
  success: boolean,
  message: string,
  response?: Object,
  error?: string
}>
```

**示例:**
```javascript
const messages = [
  "什么是 JavaScript?",
  "什么是 Python?",
  "什么是 Go?"
];

const results = await sender.sendBatch(messages, { delay: 3000 });

results.forEach((result, i) => {
  if (result.success) {
    console.log(`✅ 消息 ${i + 1}: ${result.response.content}`);
  } else {
    console.log(`❌ 消息 ${i + 1}: ${result.error}`);
  }
});
```

## SessionManager 类

### 初始化

```javascript
import { SessionManager } from './browser/session-manager.js';

const sessionManager = new SessionManager();
```

### loadSession()

加载已保存的 session

**返回:** Session 数据对象或 null

**示例:**
```javascript
const session = sessionManager.loadSession();
if (session) {
  console.log(`Session 捕获于: ${session.capturedAt}`);
}
```

### getCookies()

获取 cookie 字符串（用于 HTTP 请求）

**返回:** string

**示例:**
```javascript
const cookieString = sessionManager.getCookies();
// "__Secure-next-auth.session-token=xxx; ..."
```

### getCookie(name)

获取特定 cookie 的值

**参数:**
- `name` (string): Cookie 名称

**返回:** string 或 null

**示例:**
```javascript
const sessionToken = sessionManager.getCookie('__Secure-next-auth.session-token');
```

### getAuthCookies()

获取所有认证相关的 cookies

**返回:**
```javascript
{
  sessionToken: string,
  callbackUrl: string,
  cfuvid: string,
  cfClearance: string
}
```

**示例:**
```javascript
const authCookies = sessionManager.getAuthCookies();
console.log(`Session Token: ${authCookies.sessionToken ? '✓' : '✗'}`);
```

### validateSession()

验证 session 是否有效

**返回:** Promise<boolean>

**示例:**
```javascript
const isValid = await sessionManager.validateSession();
if (!isValid) {
  console.log('Session 已失效，需要重新登录');
}
```

### refreshSession(options)

刷新 session（重新登录）

**参数:**
- `options` (object): 可选参数
  - `headless` (boolean): 是否无头模式
  - `useProfile` (string): Chrome profile 路径

**返回:** Promise<SessionData>

**示例:**
```javascript
await sessionManager.refreshSession();
console.log('Session 已刷新');
```

### ensureValidSession(options)

确保有有效的 session（自动加载或刷新）

**参数:** 同 refreshSession

**返回:** Promise<SessionData>

**示例:**
```javascript
await sessionManager.ensureValidSession();
// 现在可以安全地使用 session
```

## CLI 命令

### 登录
```bash
node run-skill.js --login
```

### 发送消息
```bash
# 单条消息
node run-skill.js --message "你好"

# 从文件
node run-skill.js --file prompt.txt

# 批量
node run-skill.js --batch questions.txt

# 指定模型
node run-skill.js --message "你好" --model gpt-4o
```

### 对话管理
```bash
# 列出对话
node run-skill.js --list
node run-skill.js --list-all

# 搜索
node run-skill.js --search "JavaScript"

# 查看详情
node run-skill.js --show conv-abc123

# 删除
node run-skill.js --delete conv-abc123

# 重命名
node run-skill.js --rename conv-abc123 "新标题"

# 清空所有
node run-skill.js --clear
```

### 其他
```bash
# 验证 session
node run-skill.js --validate

# 列出模型
node run-skill.js --models

# 账户信息
node run-skill.js --account
```

## 错误处理

所有 API 方法都可能抛出错误，建议使用 try-catch：

```javascript
try {
  const response = await client.sendMessage({
    message: "你好"
  });
  console.log(response.content);
} catch (error) {
  if (error.message.includes('Authentication failed')) {
    console.log('需要重新登录');
    await sessionManager.refreshSession();
  } else {
    console.error('发生错误:', error.message);
  }
}
```

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `Authentication failed` | Session 失效 | 运行 `--login` 重新登录 |
| `HTTP 401` | 未授权 | 检查 cookies 是否有效 |
| `HTTP 403` | 被禁止 | 可能触发 Cloudflare 验证 |
| `HTTP 429` | 请求过多 | 增加请求间隔 |
| `Connect Timeout` | 网络问题 | 检查网络连接或配置代理 |

## 最佳实践

1. **Session 管理**
   - 定期验证 session 有效性
   - Session 失效时自动刷新
   - 不要频繁刷新 session

2. **请求频率**
   - 批量请求时设置合理的延迟（建议 2-3 秒）
   - 避免短时间内大量请求
   - 遵守 API 速率限制

3. **错误处理**
   - 始终使用 try-catch
   - 对不同错误类型采取不同策略
   - 记录错误日志便于调试

4. **数据安全**
   - 不要提交 session.json 到版本控制
   - 定期清理历史记录
   - 使用环境变量存储敏感信息
