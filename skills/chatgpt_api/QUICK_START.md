# ChatGPT API 快速开始指南

## 已完成的工作

✅ 项目结构已创建  
✅ 依赖已安装（Playwright + dotenv）  
✅ 登录功能已实现并测试成功  
✅ Session cookies 已保存到 `data/session.json`  

## 捕获的 Cookies

当前已捕获以下关键 cookies：
- `__Host-next-auth.csrf-token` - CSRF 保护 token
- `__Secure-next-auth.callback-url` - OAuth 回调 URL  
- `__cflb` - Cloudflare 负载均衡
- `_cfuvid` - Cloudflare 用户验证 ID
- `cf_clearance` - Cloudflare clearance token
- `__cf_bm` - Cloudflare bot management

## 下一步工作

### 1. 调试 API 调用

当前遇到的问题：
- ❌ 连接 `chatgpt.com/backend-api` 超时
- 可能原因：网络限制、需要代理、或 API 端点已变更

### 2. 可选方案

#### 方案 A：使用浏览器自动化（推荐）

不直接调用 API，而是通过 Playwright 控制浏览器：

```javascript
// 1. 加载 session cookies
// 2. 打开 chatgpt.com
// 3. 在页面中输入消息
// 4. 点击发送按钮
// 5. 等待并提取响应
```

优点：
- 不需要逆向 API
- 更稳定，不容易被检测
- 可以处理所有类型的交互

缺点：
- 速度较慢
- 需要保持浏览器运行

#### 方案 B：继续调试 API

需要：
1. 检查是否需要代理
2. 抓包分析真实的 API 请求
3. 可能需要更多的 headers 或 tokens

## 使用方法

### 登录（已完成）

```bash
node run-skill.js --login
```

### 发送消息（待实现）

```bash
# 方案 A：浏览器自动化
node run-skill.js --message "你好" --use-browser

# 方案 B：API 调用（需要调试）
node run-skill.js --message "你好"
```

## 文件说明

- `run-skill.js` - CLI 入口
- `browser/capture-session.js` - 登录和 session 捕获
- `browser/session-manager.js` - Session 管理
- `request/chatgpt-client.js` - API 客户端（待调试）
- `data/session.json` - 保存的 session 数据

## 建议

基于当前情况，建议采用**方案 A（浏览器自动化）**：

1. 更可靠，不依赖未公开的 API
2. 可以处理 Cloudflare 验证
3. 实现相对简单

如果你需要高性能和大量请求，再考虑调试 API 方案。

## 下一步操作

请告诉我你希望：
1. 继续调试 API 调用（需要网络调试）
2. 改用浏览器自动化方案（更稳定）
3. 两种方案都实现（API 优先，失败时降级到浏览器）
