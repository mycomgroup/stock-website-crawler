# ChatGPT API vs Gemini API 对比

## 概述

两个工具提供完全相同的功能和接口，唯一的区别是后端服务（ChatGPT vs Gemini）。

## 功能对比

| 功能 | ChatGPT API | Gemini API | 说明 |
|------|-------------|------------|------|
| 🔐 浏览器登录 | ✅ | ✅ | ChatGPT 支持多种方式，Gemini 仅 Google |
| 💾 Session 管理 | ✅ | ✅ | 完全相同 |
| 💬 发送消息 | ✅ | ✅ | 完全相同 |
| 📁 文件读取 | ✅ | ✅ | 完全相同 |
| 📦 批量发送 | ✅ | ✅ | 完全相同 |
| 📋 对话列表 | ✅ | ✅ | 完全相同 |
| 🔍 搜索对话 | ✅ | ✅ | 完全相同 |
| 👁️ 查看对话 | ✅ | ✅ | 完全相同 |
| 🗑️ 删除对话 | ✅ | ✅ | 完全相同 |
| ✏️ 重命名对话 | ✅ | ❌ | Gemini 不支持 |
| 🧹 清空对话 | ✅ | ❌ | Gemini 不支持 |
| 🤖 模型列表 | ✅ | ✅ | 不同的模型 |
| 👤 账户信息 | ✅ | ✅ | 完全相同 |
| 🔄 多账号管理 | ✅ | ✅ | 完全相同 |
| ⚖️ 负载均衡 | ✅ | ✅ | 完全相同 |
| 🌐 OpenAI API | ✅ | ✅ | 完全相同 |

## 命令对比

### 基础命令

| 命令 | ChatGPT | Gemini | 说明 |
|------|---------|--------|------|
| `--login` | ✅ | ✅ | 相同 |
| `--message` | ✅ | ✅ | 相同 |
| `--file` | ✅ | ✅ | 相同 |
| `--batch` | ✅ | ✅ | 相同 |
| `--model` | ✅ | ✅ | 不同的模型名称 |
| `--conversation` | ✅ | ✅ | 相同 |
| `--validate` | ✅ | ✅ | 相同 |

### 对话管理

| 命令 | ChatGPT | Gemini | 说明 |
|------|---------|--------|------|
| `--list` | ✅ | ✅ | 相同 |
| `--list-all` | ✅ | ✅ | 相同 |
| `--search` | ✅ | ✅ | 相同 |
| `--show` | ✅ | ✅ | 相同 |
| `--delete` | ✅ | ✅ | 相同 |
| `--rename` | ✅ | ❌ | Gemini 不支持 |
| `--clear` | ✅ | ❌ | Gemini 不支持 |

### 多账号管理

| 命令 | ChatGPT | Gemini | 说明 |
|------|---------|--------|------|
| `--add-account` | ✅ | ✅ | 相同 |
| `--list-accounts` | ✅ | ✅ | 相同 |
| `--remove-account` | ✅ | ✅ | 相同 |
| `--enable-account` | ✅ | ✅ | 相同 |
| `--disable-account` | ✅ | ✅ | 相同 |
| `--set-weight` | ✅ | ✅ | 相同 |
| `--set-strategy` | ✅ | ✅ | 相同 |
| `--validate-accounts` | ✅ | ✅ | 相同 |
| `--account-stats` | ✅ | ✅ | 相同 |

## 技术对比

### 登录方式

**ChatGPT**
```bash
# 支持多种登录方式
node run-skill.js --login
# 可以使用: Google, Microsoft, Apple, Email
```

**Gemini**
```bash
# 仅支持 Google 账号
node run-skill.js --login
# 必须使用 Google 账号
```

### 模型列表

**ChatGPT**
- gpt-4
- gpt-4-turbo
- gpt-3.5-turbo
- gpt-4-vision (图像)

**Gemini**
- gemini-pro (文本)
- gemini-pro-vision (图像+文本)

### API 端点

**ChatGPT**
```javascript
baseUrl: 'https://chatgpt.com'
apiUrl: 'https://chatgpt.com/backend-api'
```

**Gemini**
```javascript
baseUrl: 'https://gemini.google.com'
apiUrl: 'https://gemini.google.com/api'
```

### Session Cookie

**ChatGPT**
- `__Secure-next-auth.session-token`
- `__Secure-next-auth.callback-url`
- `__cf_bm`
- `_cfuvid`

**Gemini**
- 需要实际测试确认
- 可能包含 Google 特定的 auth cookies

## 使用示例对比

### 发送消息

**ChatGPT**
```bash
node run-skill.js --message "解释量子计算" --model gpt-4
```

**Gemini**
```bash
node run-skill.js --message "解释量子计算" --model gemini-pro
```

### OpenAI API 使用

**ChatGPT**
```javascript
const openai = new OpenAI({
  apiKey: "sk-chatgpt-proxy",
  baseURL: "http://localhost:3000/v1"
});

const completion = await openai.chat.completions.create({
  model: "gpt-4",
  messages: [{ role: "user", content: "你好" }]
});
```

**Gemini**
```javascript
const openai = new OpenAI({
  apiKey: "sk-gemini-proxy",
  baseURL: "http://localhost:3000/v1"
});

const completion = await openai.chat.completions.create({
  model: "gemini-pro",
  messages: [{ role: "user", content: "你好" }]
});
```

## 性能对比

| 指标 | ChatGPT | Gemini | 说明 |
|------|---------|--------|------|
| 响应速度 | 快 | 快 | 取决于网络和服务器 |
| 上下文长度 | 8K-128K | 32K | 取决于模型 |
| 速率限制 | 有 | 有 | 需要多账号避免 |
| Session 有效期 | 14-30 天 | 14-30 天 | 需要定期刷新 |

## 适用场景

### ChatGPT API 适合

- 需要 GPT-4 的高级推理能力
- 需要更长的上下文窗口
- 已有 ChatGPT Plus 订阅
- 需要重命名和管理对话

### Gemini API 适合

- 需要 Google 生态集成
- 需要多模态能力（Gemini Pro Vision）
- 偏好 Google 的 AI 模型
- 已有 Google 账号

## 迁移指南

### 从 ChatGPT 迁移到 Gemini

1. 复制配置
```bash
cp skills/chatgpt_api/.env skills/gemini_api/.env
```

2. 更新模型名称
```bash
# .env
DEFAULT_MODEL=gemini-pro  # 原来是 gpt-4
```

3. 重新登录
```bash
cd skills/gemini_api
node run-skill.js --login
```

4. 更新代码中的模型引用
```javascript
// 原来
model: "gpt-4"

// 改为
model: "gemini-pro"
```

### 从 Gemini 迁移到 ChatGPT

反向操作即可。

## 同时使用两个工具

可以同时运行两个服务器，使用不同的端口：

**ChatGPT**
```bash
cd skills/chatgpt_api
PORT=3000 node server/openai-compatible-server.js
```

**Gemini**
```bash
cd skills/gemini_api
PORT=3001 node server/openai-compatible-server.js
```

然后在代码中根据需要选择：

```javascript
// 使用 ChatGPT
const chatgpt = new OpenAI({
  apiKey: "sk-chatgpt-proxy",
  baseURL: "http://localhost:3000/v1"
});

// 使用 Gemini
const gemini = new OpenAI({
  apiKey: "sk-gemini-proxy",
  baseURL: "http://localhost:3001/v1"
});
```

## 总结

| 方面 | ChatGPT API | Gemini API |
|------|-------------|------------|
| 功能完整性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 易用性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 模型能力 | GPT-4 | Gemini Pro |
| 多模态 | GPT-4V | Gemini Pro Vision |
| 生态集成 | OpenAI | Google |
| 成本 | 需要 Plus | 免费/付费 |

两个工具功能基本相同，选择取决于你的具体需求和偏好。

---

**最后更新**: 2026-04-06
