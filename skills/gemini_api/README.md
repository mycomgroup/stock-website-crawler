# Google Gemini API Skill

## 功能概述

通过程序化方式向 Google Gemini 提交问题，无需手动在网页上操作。支持 Google 账号登录，自动管理 session cookies。

## 核心特性

- 🔐 支持 Google 账号登录（弹出浏览器窗口）
- 💾 自动保存和管理 session cookies
- 🔄 自动检测 cookie 失效并提示重新登录
- 📝 支持发送消息到 Gemini
- 🎯 支持指定模型（gemini-pro, gemini-pro-vision 等）
- 📊 获取对话历史和响应
- 🔍 搜索和管理对话
- 📋 获取可用模型列表
- 👤 查看账户信息
- 🔄 多账号管理和负载均衡

## 快速开始

### 1. 安装依赖

```bash
cd skills/gemini_api
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
node run-skill.js --message "解释一下量子计算"

# 指定模型
node run-skill.js --message "分析这张图片" --model "gemini-pro-vision"

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
node run-skill.js --search "量子计算"

# 查看对话详情
node run-skill.js --show conv-abc123

# 删除对话
node run-skill.js --delete conv-abc123
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
import { GeminiClient } from './request/gemini-client.js';

const client = new GeminiClient();

// 发送消息
const response = await client.sendMessage({
  message: "解释一下量子计算",
  model: "gemini-pro"
});

console.log(response.content);
```

## 多账号管理

### 添加多个账号

```bash
# 添加账号
node run-skill.js --add-account "账号1"
node run-skill.js --add-account "账号2"
node run-skill.js --add-account "账号3"

# 查看账号列表
node run-skill.js --list-accounts

# 设置负载均衡策略
node run-skill.js --set-strategy weighted

# 设置账号权重
node run-skill.js --set-weight account-xxx 2
```

### 启动多账号服务器

```bash
USE_MULTI_ACCOUNT=true npm run server
```

## OpenAI 兼容服务器

本工具提供了一个 OpenAI 兼容的 API 服务器，可以让任何支持 OpenAI API 的应用使用你的 Gemini session。

### 单账号模式

```bash
npm run server
# 或
node server/openai-compatible-server.js
```

### 多账号模式（负载均衡）

```bash
USE_MULTI_ACCOUNT=true npm run server
```

### 使用 OpenAI SDK

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'sk-gemini-proxy',
  baseURL: 'http://localhost:3000/v1'
});

const completion = await openai.chat.completions.create({
  model: 'gemini-pro',
  messages: [{ role: 'user', content: '你好' }]
});
```

## 可用模型

- `gemini-pro` - 最强大的文本模型
- `gemini-pro-vision` - 支持图像和文本的多模态模型

## 负载均衡策略

- `round-robin` - 轮询（默认）
- `weighted` - 加权轮询
- `least-used` - 最少使用
- `least-recent` - 最久未使用

## 文档

- [API_REFERENCE.md](./API_REFERENCE.md) - API 参考
- [OPENAI_SERVER.md](./OPENAI_SERVER.md) - OpenAI 服务器文档
- [MULTI_ACCOUNT.md](./MULTI_ACCOUNT.md) - 多账号管理文档
- [TECHNICAL_DETAILS.md](./TECHNICAL_DETAILS.md) - 技术细节

## 注意事项

1. **Session 有效期**: Gemini session 通常有效期为 14-30 天
2. **请求频率**: 避免过于频繁的请求，建议间隔 1-2 秒
3. **数据安全**: `data/session.json` 包含敏感信息，不要提交到 git
4. **模型权限**: 某些模型可能需要特定权限

## 与 ChatGPT API 的对比

| 特性 | ChatGPT API | Gemini API |
|------|-------------|------------|
| 登录方式 | 多种方式 | Google 账号 |
| 模型 | GPT-4, GPT-3.5 | Gemini Pro, Gemini Pro Vision |
| 多模态 | 需要 GPT-4V | Gemini Pro Vision 原生支持 |
| API 格式 | 完全兼容 OpenAI | 完全兼容 OpenAI |
| 多账号 | 支持 | 支持 |
| 负载均衡 | 支持 | 支持 |

## 参考资料

- [Google Gemini](https://gemini.google.com/)
- [Gemini API 文档](https://ai.google.dev/)
- [Playwright 文档](https://playwright.dev/)
