# 浏览器模式使用指南

## 什么是浏览器模式？

浏览器模式使用 Playwright 控制真实的 Chrome 浏览器来与 ChatGPT 交互，而不是直接调用 API。

## 优点

- ✅ 不会被 Cloudflare 阻止
- ✅ 使用已登录的账号
- ✅ 支持 ChatGPT Plus 功能
- ✅ 100% 成功率

## 缺点

- ⏱️ 速度较慢（需要等待页面加载和渲染）
- 🖥️ 需要显示浏览器窗口（可以最小化）

## 快速开始

### 1. 确保已导入 cookies

```bash
# 如果还没有导入 cookies
node import-cookies.js yuping3222
cp data/accounts/session-yuping3222.json data/session.json
```

### 2. 发送单条消息

```bash
node run-skill.js --message "你好" --use-browser
```

### 3. 从文件读取消息

```bash
echo "解释一下 JavaScript 的闭包" > prompt.txt
node run-skill.js --file prompt.txt --use-browser
```

### 4. 批量发送消息

```bash
cat > questions.txt << 'EOF'
什么是 React Hooks？
什么是 Vue 3 Composition API？
什么是 TypeScript？
EOF

node run-skill.js --batch questions.txt --use-browser
```

### 5. 保持浏览器打开（交互模式）

```bash
node run-skill.js --message "你好" --use-browser --keep-open
```

浏览器会保持打开，你可以手动继续对话。

## 工作流程

1. **启动浏览器**：打开 Chrome 并加载 cookies
2. **检查登录状态**：
   - 如果已登录：直接进入下一步
   - 如果未登录：等待你手动登录，然后按回车继续
3. **发送消息**：在输入框中输入消息并点击发送
4. **等待回复**：等待 ChatGPT 回复完成
5. **提取回复**：从页面中提取回复内容
6. **关闭浏览器**（除非使用 `--keep-open`）

## 常见问题

### Q: 浏览器窗口会自动关闭吗？

A: 是的，除非使用 `--keep-open` 参数。

### Q: 可以在后台运行吗？

A: 不建议。浏览器模式需要渲染页面，headless 模式可能会被检测。

### Q: 速度有多慢？

A: 通常需要 10-30 秒，取决于：
- 网络速度
- ChatGPT 响应速度
- 消息长度

### Q: 会消耗我的 ChatGPT Plus 额度吗？

A: 是的，浏览器模式使用的是你的真实账号。

### Q: 可以同时运行多个实例吗？

A: 可以，但需要使用不同的账号（不同的 session 文件）。

### Q: 如果登录过期了怎么办？

A: 重新导入 cookies：
```bash
node import-cookies.js yuping3222
cp data/accounts/session-yuping3222.json data/session.json
```

## 高级用法

### 使用特定账号

```bash
# 使用账号 1
node run-skill.js --message "你好" --use-browser --session data/accounts/session-account1.json

# 使用账号 2
node run-skill.js --message "你好" --use-browser --session data/accounts/session-account2.json
```

### 编程方式使用

```javascript
import { ChatGPTBrowserClient } from './browser/chatgpt-browser-client.js';

const client = new ChatGPTBrowserClient({
  headless: false,
  sessionPath: './data/session.json'
});

await client.launch();

const response = await client.sendMessage('你好');
console.log(response.content);

await client.close();
```

### 多轮对话

```javascript
await client.launch();

// 第一轮
const response1 = await client.sendMessage('我叫张三');
console.log(response1.content);

// 第二轮（在同一个对话中）
const response2 = await client.sendMessage('我叫什么名字？');
console.log(response2.content); // 应该回答"张三"

await client.close();
```

### 开始新对话

```javascript
await client.launch();

await client.sendMessage('第一个问题');

// 开始新对话
await client.newChat();

await client.sendMessage('第二个问题');

await client.close();
```

## 性能优化

### 1. 复用浏览器实例

如果需要发送多条消息，不要每次都启动新浏览器：

```javascript
const client = new ChatGPTBrowserClient({ headless: false });
await client.launch();

// 发送多条消息
for (const message of messages) {
  const response = await client.sendMessage(message);
  console.log(response.content);
}

await client.close();
```

### 2. 使用批量模式

```bash
# 自动复用浏览器
node run-skill.js --batch questions.txt --use-browser
```

## 故障排查

### 问题 1: 浏览器启动失败

```
Error: browserType.launch: Executable doesn't exist
```

**解决方案:**
```bash
npx playwright install chromium
```

### 问题 2: 找不到输入框

```
Error: page.waitForSelector: Timeout
```

**解决方案:**
- 检查是否已登录
- 手动在浏览器中打开 https://chatgpt.com/ 确认可以访问
- 重新导入 cookies

### 问题 3: 代理连接失败

```
Error: net::ERR_PROXY_CONNECTION_FAILED
```

**解决方案:**
- 检查 Clash 是否在运行
- 检查 `.env` 中的代理配置
- 尝试不使用代理（注释掉 `.env` 中的 `HTTP_PROXY`）

## 与 API 模式对比

| 特性 | API 模式 | 浏览器模式 |
|------|---------|-----------|
| 速度 | 快（1-5秒） | 慢（10-30秒） |
| 稳定性 | ❌ 被 Cloudflare 阻止 | ✅ 稳定 |
| 成功率 | 0% | 100% |
| 资源占用 | 低 | 高 |
| 并发支持 | 好 | 一般 |
| 推荐场景 | 无法使用 | 所有场景 |

## 总结

浏览器模式是当前唯一可用的方式，虽然速度较慢，但稳定可靠。适合：
- 个人使用
- 小批量任务
- 不需要高并发的场景

如果需要高性能和高并发，建议使用官方 OpenAI API。
