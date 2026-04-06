# ChatGPT API 工具配置总结

## 已完成的配置

### 1. 代理配置 ✅
- 检测到 Clash Verge 运行在端口 7897
- 已配置 `.env` 文件中的代理设置
- 代理连接测试成功

### 2. Cookies 导入 ✅
- 成功从浏览器导入 9 个 cookies
- 包含关键的 `__Secure-next-auth.session-token`
- Cookie 格式已标准化

### 3. 工具安装 ✅
- 安装了 Playwright
- 安装了 undici (支持代理的 HTTP 客户端)
- 所有依赖已就绪

## 当前问题

### HTTP 403 Cloudflare 保护
ChatGPT 的 backend-api 有非常严格的保护：
- 检测自动化请求
- 需要完整的浏览器指纹
- Cookies 可能需要与特定的浏览器会话绑定

## 推荐解决方案

### 方案 1：使用官方 OpenAI API（推荐）

不使用逆向工程的方式，而是使用官方 API：

```bash
# 获取 API Key: https://platform.openai.com/api-keys
# 配置 .env
OPENAI_API_KEY=sk-...

# 使用官方 SDK
npm install openai
```

优点：
- 稳定可靠
- 官方支持
- 无需担心被封禁

缺点：
- 需要付费
- 无法使用 ChatGPT Plus 的免费额度

### 方案 2：使用 Playwright 自动化（当前最可行）

不直接调用 API，而是使用 Playwright 控制真实浏览器：

```bash
# 启动浏览器会话
node run-skill.js --browser-session

# 在浏览器中发送消息
node run-skill.js --message "你好" --use-browser
```

优点：
- 可以使用已登录的账号
- 不会被 Cloudflare 阻止
- 可以使用 ChatGPT Plus 功能

缺点：
- 速度较慢
- 需要保持浏览器运行

### 方案 3：使用第三方代理服务

使用已经实现好的 ChatGPT 代理服务：
- ChatGPT-to-API
- PandoraNext
- ChatGPT-Web

## 下一步建议

1. **如果你有 OpenAI API Key**：使用方案 1（官方 API）
2. **如果只想使用免费的 ChatGPT**：使用方案 2（Playwright 自动化）
3. **如果需要稳定的生产环境**：考虑方案 3（第三方代理）

## 文件说明

- `.env` - 环境配置（包含代理设置）
- `data/session.json` - 当前账号的 cookies
- `data/accounts/` - 多账号 cookies 存储
- `data/accounts-config.json` - 多账号配置

## 有用的命令

```bash
# 导入新的 cookies
node import-cookies.js <账号名>

# 查看账号列表
node run-skill.js --list-accounts

# 验证 session
node run-skill.js --validate

# 查看对话列表
node run-skill.js --list
```

## 技术细节

当前遇到的 403 错误是因为：
1. ChatGPT 检测到请求来自非浏览器环境
2. 缺少完整的浏览器指纹（TLS fingerprint, Canvas fingerprint等）
3. Cloudflare 的 bot 检测机制

即使有正确的 cookies，直接的 HTTP 请求也很难绕过这些检测。
