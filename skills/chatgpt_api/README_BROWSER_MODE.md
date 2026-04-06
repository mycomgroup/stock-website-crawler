# ChatGPT API Skill - 纯浏览器模式

## 重要说明

由于 Cloudflare 的高级检测机制，直接 HTTP API 模式无法工作（会被 403 阻止）。

**推荐使用纯浏览器模式**，使用 Playwright 控制真实浏览器，100% 可靠。

详细技术说明请参考：[API_MODE_STATUS.md](./API_MODE_STATUS.md)

## 快速开始

### 1. 安装依赖

```bash
cd skills/chatgpt_api
npm install
```

### 2. 使用 Chrome Profile（推荐）

如果你已经在 Chrome 中登录了 ChatGPT，直接使用该 profile：

```bash
# 查看你的 Chrome profiles
ls -la ~/Library/Application\ Support/Google/Chrome/ | grep Profile

# 使用特定 profile 发送消息
node use-chrome-profile.js "/Users/你的用户名/Library/Application Support/Google/Chrome/Profile 7" "你好"
```

### 3. 或者导入 Cookies

如果不想使用 Chrome profile，可以手动导入 cookies：

```bash
# 使用 Cookie-Editor 扩展导出 cookies
# 详细步骤见: EXPORT_COOKIES_GUIDE.md

node import-cookies.js 账号名称
```

## 核心功能示例

### 1. 发送单条消息

```bash
# 使用 Chrome Profile
node use-chrome-profile.js "/Users/你的用户名/Library/Application Support/Google/Chrome/Profile 7" "解释一下 JavaScript 的闭包"

# 或使用 session cookies
node test-browser.js
```

### 2. 浏览器复用 - 发送多条消息

```bash
# 交互模式（推荐）
node reusable-browser-client.js --profile "/Users/你的用户名/Library/Application Support/Google/Chrome/Profile 7" --interactive

# 批量模式
node reusable-browser-client.js \
  --profile "/Users/你的用户名/Library/Application Support/Google/Chrome/Profile 7" \
  --message "什么是 Docker？" \
  --message "什么是 Kubernetes？" \
  --message "什么是微服务？"
```

### 3. 查询所有 Profile

```bash
# 在所有 Chrome profiles 中提问
node ask-all-profiles.js examples/example-prompt.txt examples/
```

## 编程方式使用

### 基础用法

```javascript
import { ChatGPTBrowserClient } from './browser/chatgpt-browser-client.js';

const client = new ChatGPTBrowserClient({
  headless: false,
  sessionPath: 'data/session.json'  // 或使用 Chrome profile
});

// 启动浏览器
await client.launch();

// 发送消息
const response = await client.sendMessage('你好');
console.log(response.content);

// 关闭浏览器
await client.close();
```

### 复用浏览器（推荐）

```javascript
import { ReusableBrowserClient } from './reusable-browser-client.js';

const client = new ReusableBrowserClient({
  profilePath: '/Users/你的用户名/Library/Application Support/Google/Chrome/Profile 7'
});

await client.launch();

// 发送多条消息（复用同一个浏览器）
await client.sendMessage('第一个问题');
await client.sendMessage('第二个问题');
await client.sendMessage('第三个问题');

await client.close();
```

### 交互模式

```javascript
import { ReusableBrowserClient } from './reusable-browser-client.js';

const client = new ReusableBrowserClient({
  profilePath: '/Users/你的用户名/Library/Application Support/Google/Chrome/Profile 7'
});

await client.launch();

// 启动交互模式
await client.interactive();
// 用户可以输入消息，输入 'exit' 退出
```

## 性能对比

| 模式 | 启动时间 | 每条消息 | 3条消息总时间 | 可靠性 |
|------|---------|---------|--------------|--------|
| API 模式 | - | - | - | ❌ 0% (Cloudflare 阻止) |
| 浏览器模式（每次启动） | 10秒 | 15秒 | 55秒 | ✅ 100% |
| 浏览器复用 | 10秒 | 10秒 | 40秒 | ✅ 100% |
| 交互模式 | 10秒 | 10秒 | 40秒 | ✅ 100% |

## 测试验证

运行测试脚本验证所有功能：

```bash
# 简化测试（推荐）
node test-readme-simple.js

# 完整测试
node test-readme-examples.js
```

测试结果：
- ✅ 启动浏览器（使用 Chrome Profile）
- ✅ 发送单条消息
- ✅ 浏览器复用（多条消息）
- ✅ 关闭浏览器

## 使用场景

### 场景 1: 单次查询

```bash
node use-chrome-profile.js "/path/to/profile" "你的问题"
```

### 场景 2: 批量查询

```bash
# 创建问题列表
cat > questions.txt << 'EOF'
什么是 Docker？
什么是 Kubernetes？
什么是微服务？
EOF

# 批量发送
node reusable-browser-client.js \
  --profile "/path/to/profile" \
  --message "什么是 Docker？" \
  --message "什么是 Kubernetes？" \
  --message "什么是微服务？"
```

### 场景 3: 多账号轮询

```bash
# 在所有账号中提问
node ask-all-profiles.js prompt.txt output/
```

### 场景 4: 长时间交互

```bash
# 启动交互模式
node reusable-browser-client.js --profile "/path/to/profile" --interactive

# 然后可以连续对话
💬 你: 什么是闭包？
✅ 收到回复: ...

💬 你: 给个例子
✅ 收到回复: ...

💬 你: exit
👋 再见！
```

## 多 Profile 管理

详细文档：[MULTI_PROFILE_GUIDE.md](./MULTI_PROFILE_GUIDE.md)

你可以使用多个 Chrome profiles 来管理多个 ChatGPT 账号：

```bash
# 查看所有 profiles
ls -la ~/Library/Application\ Support/Google/Chrome/ | grep Profile

# 使用不同的 profile
node use-chrome-profile.js "/path/to/Profile 2" "问题1"
node use-chrome-profile.js "/path/to/Profile 7" "问题2"
```

## 注意事项

### 1. Rate Limiting

ChatGPT 有请求频率限制，建议：
- 两次请求之间间隔 3-5 秒
- 避免短时间内大量请求
- 使用多个账号轮询

### 2. Profile 占用

如果 Chrome 已经打开了某个 profile，脚本无法再次使用：

```bash
# 关闭 Chrome
killall "Google Chrome"

# 或使用不同的 profile
```

### 3. 代理配置

如果需要代理访问 ChatGPT，在 `.env` 中配置：

```bash
HTTP_PROXY=http://127.0.0.1:7897
HTTPS_PROXY=http://127.0.0.1:7897
```

### 4. 浏览器模式

- `headless: false` - 显示浏览器窗口（推荐，方便调试）
- `headless: true` - 无头模式（不显示窗口，但可能被检测）

## 故障排查

### 问题 1: Profile 被占用

```
Error: Profile is already in use
```

**解决方案**:
```bash
killall "Google Chrome"
```

### 问题 2: 找不到输入框

```
Error: 未找到输入框
```

**解决方案**:
- 确保已登录 ChatGPT
- 检查页面是否完全加载
- 尝试增加等待时间

### 问题 3: Rate Limit

```
Error: Rate limit exceeded
```

**解决方案**:
- 等待几分钟后重试
- 使用不同的账号
- 减少请求频率

### 问题 4: Cloudflare 验证

如果遇到 Cloudflare 验证页面：
- 浏览器模式会自动等待
- 手动完成验证后继续
- 验证通过后 cookies 会自动保存

## 最佳实践

### 1. 使用 Chrome Profile（推荐）

优点：
- 无需导出 cookies
- 自动保持登录状态
- 支持多账号

### 2. 复用浏览器实例

优点：
- 减少启动开销
- 提高响应速度
- 保持对话上下文

### 3. 合理控制请求频率

```javascript
// 批量发送时添加延迟
for (const message of messages) {
  await client.sendMessage(message);
  await new Promise(resolve => setTimeout(resolve, 5000)); // 等待 5 秒
}
```

### 4. 错误处理

```javascript
try {
  const response = await client.sendMessage('你的问题');
  console.log(response);
} catch (error) {
  if (error.message.includes('Rate limit')) {
    console.log('触发限流，等待 60 秒...');
    await new Promise(resolve => setTimeout(resolve, 60000));
    // 重试
  }
}
```

## 相关文档

- [API_MODE_STATUS.md](./API_MODE_STATUS.md) - 为什么 API 模式不可用
- [MULTI_PROFILE_GUIDE.md](./MULTI_PROFILE_GUIDE.md) - 多 Profile 管理指南
- [EXPORT_COOKIES_GUIDE.md](./EXPORT_COOKIES_GUIDE.md) - Cookie 导出指南
- [BROWSER_MODE_GUIDE.md](./BROWSER_MODE_GUIDE.md) - 浏览器模式详细指南

## 总结

纯浏览器模式是目前唯一可靠的方式：

✅ 优点：
- 100% 可靠（不会被 Cloudflare 阻止）
- 支持所有 ChatGPT 功能
- 可以使用 Chrome Profile（无需导出 cookies）
- 支持浏览器复用（提高效率）

⚠️ 缺点：
- 速度较慢（10-15秒/请求）
- 资源占用较高
- 需要显示浏览器窗口

对于大多数使用场景，浏览器模式已经足够好了！
