# ChatGPT API Skill

## 功能概述

通过程序化方式向 ChatGPT 提交问题，无需手动在网页上操作。支持任意登录方式（Google、Microsoft、Apple、邮箱等），自动管理 session cookies。

## 核心特性

- 🔐 支持任意登录方式（弹出浏览器窗口，用户自行选择）
- 💾 自动保存和管理 session cookies
- 🔄 自动检测 cookie 失效并提示重新登录
- 📝 支持发送消息到 ChatGPT
- 🎯 支持指定模型（GPT-4, GPT-3.5 等）
- 📊 获取对话历史和响应
- 🔍 搜索和管理对话
- 📋 获取可用模型列表
- 👤 查看账户信息
- 🗑️ 删除和重命名对话

## 快速开始

### 1. 安装依赖

```bash
cd skills/chatgpt_api
npm install
```

### 2. 首次登录

```bash
# 弹出浏览器窗口，完成 Google 登录
node run-skill.js --login
```

登录成功后，session 数据会保存到 `data/session.json`，下次使用时无需重新登录。

### 3. 发送消息

```bash
# 发送单条消息
node run-skill.js --message "解释一下 JavaScript 的闭包"

# 指定模型
node run-skill.js --message "写一个快速排序算法" --model "gpt-4"

# 从文件读取消息
node run-skill.js --file prompt.txt

# 批量发送
node run-skill.js --batch questions.txt
```

### 4. 对话管理

```bash
# 列出最近对话
node run-skill.js --list

# 列出所有对话
node run-skill.js --list-all

# 搜索对话
node run-skill.js --search "JavaScript"

# 查看对话详情
node run-skill.js --show conv-abc123

# 删除对话
node run-skill.js --delete conv-abc123

# 重命名对话
node run-skill.js --rename conv-abc123 "新标题"
```

### 5. 其他功能

```bash
# 列出可用模型
node run-skill.js --models

# 查看账户信息
node run-skill.js --account

# 验证 session
node run-skill.js --validate
```

### 6. 编程方式使用

```javascript
import { ChatGPTClient } from './request/chatgpt-client.js';

const client = new ChatGPTClient();

// 发送消息
const response = await client.sendMessage({
  message: "解释一下 JavaScript 的闭包",
  model: "gpt-4"
});

console.log(response.content);
```

## 关键 Cookie 字段

根据调研，ChatGPT 认证需要以下关键 cookies：

| Cookie 名称 | 说明 | 必需 |
|------------|------|------|
| `__Secure-next-auth.session-token` | 主要的 session token | ✅ |
| `__Secure-next-auth.callback-url` | OAuth 回调 URL | ✅ |
| `_cfuvid` | Cloudflare 验证 ID | ⚠️ |
| `cf_clearance` | Cloudflare clearance token | ⚠️ |

## 目录结构

```
skills/chatgpt_api/
├── README.md                    # 本文档
├── package.json                 # 项目配置
├── run-skill.js                 # CLI 入口
├── load-env.js                  # 环境变量加载
├── paths.js                     # 路径配置
├── browser/
│   ├── capture-session.js       # 浏览器登录和 session 捕获
│   └── session-manager.js       # Session 管理和验证
├── request/
│   ├── chatgpt-client.js        # ChatGPT API 客户端
│   └── message-sender.js        # 消息发送器
├── data/
│   └── session.json             # Session 数据（自动生成）
└── examples/
    └── example-prompt.txt       # 示例 prompt
```

## API 使用说明

### ChatGPTClient

```javascript
import { ChatGPTClient } from './request/chatgpt-client.js';

const client = new ChatGPTClient();

// 发送消息
const response = await client.sendMessage({
  message: "你好",
  model: "gpt-4",              // 可选，默认 gpt-4
  conversationId: null,        // 可选，继续已有对话
  parentMessageId: null        // 可选，回复特定消息
});

// 获取对话历史
const conversations = await client.getConversations();

// 获取特定对话
const conversation = await client.getConversation(conversationId);
```

### Session 管理

```javascript
import { SessionManager } from './browser/session-manager.js';

const sessionManager = new SessionManager();

// 检查 session 是否有效
const isValid = await sessionManager.validateSession();

// 刷新 session（重新登录）
if (!isValid) {
  await sessionManager.refreshSession();
}
```

## Cookie 失效处理

当检测到 cookie 失效时（通常是 401 或 403 错误），工具会：

1. 提示用户 session 已失效
2. 自动执行重新登录流程
3. 弹出浏览器窗口让用户完成 Google 登录
4. 保存新的 session 数据
5. 重试原始请求

## 使用已登录的浏览器 Profile

如果你已经在 Chrome 中登录了 ChatGPT，可以直接使用该 profile：

```bash
# 使用现有的 Chrome profile 重新捕获 session
node run-skill.js --login --use-profile "/Users/你的用户名/Library/Application Support/Google/Chrome/Profile 5"
```

这里传入的是你真实的 Chrome profile 目录，例如 `Profile 5` 或 `Default`。程序会自动识别并转换成 Playwright 需要的 `userDataDir + --profile-directory` 组合，避免在 profile 目录里再错误创建一个新的 `Default` 子目录。

如果提示 profile 被占用，请先完全退出正在使用该 profile 的 Chrome，再重新运行。

## 注意事项

1. **Session 有效期**：ChatGPT session 通常有效期为 14-30 天
2. **请求频率**：避免过于频繁的请求，建议间隔 1-2 秒
3. **数据安全**：`data/session.json` 包含敏感信息，不要提交到 git
4. **Cloudflare 保护**：如遇到 Cloudflare 验证，需要手动完成验证
5. **模型权限**：GPT-4 需要 ChatGPT Plus 订阅

## 故障排查

### 登录失败

```bash
# 使用有头模式查看登录过程
node run-skill.js --login --headed
```

### Session 验证失败

```bash
# 强制重新登录
node run-skill.js --login --force
```

### 查看详细日志

```bash
# 启用调试模式
DEBUG=chatgpt:* node run-skill.js --message "测试"
```

## 后续扩展

- [ ] 支持流式响应（SSE）
- [ ] 支持上传文件/图片
- [ ] 支持多轮对话管理
- [ ] 支持自定义 system prompt
- [ ] 支持导出对话记录
- [ ] 支持批量提交问题

## OpenAI 兼容服务器

本工具还提供了一个 OpenAI 兼容的 API 服务器，可以让任何支持 OpenAI API 的应用使用你的 ChatGPT session。

### 单账号模式

```bash
npm run server
# 或
node server/openai-compatible-server.js
```

### 多账号模式（负载均衡）

```bash
# 添加多个账号
node run-skill.js --add-account "账号1"
node run-skill.js --add-account "账号2"
node run-skill.js --add-account "账号3"

# 启动多账号服务器
USE_MULTI_ACCOUNT=true npm run server
```

### 使用 OpenAI SDK

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'sk-chatgpt-proxy',
  baseURL: 'http://localhost:3000/v1'
});

const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: '你好' }]
});
```

详细文档: 
- [OPENAI_SERVER.md](./OPENAI_SERVER.md) - OpenAI 服务器文档
- [MULTI_ACCOUNT.md](./MULTI_ACCOUNT.md) - 多账号管理文档

## 参考资料

- [ChatGPT Web API 逆向分析](https://github.com/acheong08/ChatGPT)
- [OpenAI OAuth 文档](https://platform.openai.com/docs/guides/authentication)
- [Playwright 文档](https://playwright.dev/)
