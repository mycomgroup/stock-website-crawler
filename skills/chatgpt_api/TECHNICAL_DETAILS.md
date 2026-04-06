# ChatGPT API 技术细节

## 1. 关键 Cookie 字段调研

根据对 ChatGPT 网站的分析和社区资料，以下是需要保存的关键 cookie 字段：

### 1.1 必需的认证 Cookies

| Cookie 名称 | 说明 | 重要性 | 示例值 |
|------------|------|--------|--------|
| `__Secure-next-auth.session-token` | NextAuth.js session token，最核心的认证凭证 | ⭐⭐⭐⭐⭐ | `eyJhbGciOiJkaXIi...` |
| `__Secure-next-auth.callback-url` | OAuth 回调 URL | ⭐⭐⭐⭐ | `https://chat.openai.com` |

### 1.2 Cloudflare 相关 Cookies

| Cookie 名称 | 说明 | 重要性 | 示例值 |
|------------|------|--------|--------|
| `_cfuvid` | Cloudflare 用户验证 ID | ⭐⭐⭐ | `abc123...` |
| `cf_clearance` | Cloudflare clearance token（通过人机验证后获得） | ⭐⭐⭐ | `def456...` |

### 1.3 其他可选 Cookies

| Cookie 名称 | 说明 | 重要性 |
|------------|------|--------|
| `__Secure-next-auth.csrf-token` | CSRF 保护 token | ⭐⭐ |
| `intercom-*` | Intercom 客服系统相关 | ⭐ |
| `ajs_*` | Analytics.js 追踪相关 | ⭐ |

## 2. Cookie 属性说明

每个 cookie 包含以下属性：

```javascript
{
  name: "__Secure-next-auth.session-token",
  value: "eyJhbGciOiJkaXIi...",
  domain: ".chat.openai.com",
  path: "/",
  expires: 1737376800,        // Unix timestamp
  httpOnly: true,             // 不能被 JavaScript 访问
  secure: true,               // 只能通过 HTTPS 传输
  sameSite: "Lax"            // CSRF 保护
}
```

### 重要属性解释

- `httpOnly: true` - 这意味着 cookie 不能通过 `document.cookie` 访问，只能通过 HTTP 请求发送
- `secure: true` - 只能在 HTTPS 连接中传输
- `domain: ".chat.openai.com"` - 适用于所有 chat.openai.com 的子域名
- `sameSite: "Lax"` - 防止 CSRF 攻击，但允许从外部链接导航时携带

## 3. 认证流程

### 3.1 Google OAuth 登录流程

```
1. 用户访问 https://chat.openai.com/auth/login
2. 点击 "Log in with Google"
3. 重定向到 Google OAuth 页面
   └─> https://accounts.google.com/o/oauth2/v2/auth?...
4. 用户选择 Google 账号并授权
5. Google 重定向回 ChatGPT
   └─> https://chat.openai.com/api/auth/callback/google?code=...
6. ChatGPT 后端验证 OAuth code
7. 设置 session cookies
8. 重定向到 https://chat.openai.com/
```

### 3.2 Session Token 结构

`__Secure-next-auth.session-token` 是一个 JWT (JSON Web Token)，包含：

```json
{
  "header": {
    "alg": "dir",
    "enc": "A256GCM"
  },
  "payload": {
    "sub": "user-xxx",
    "email": "user@example.com",
    "iat": 1234567890,
    "exp": 1234567890
  }
}
```

## 4. API 端点分析

### 4.1 发送消息 API

```
POST https://chat.openai.com/backend-api/conversation
Content-Type: application/json
Cookie: __Secure-next-auth.session-token=xxx; ...

{
  "action": "next",
  "messages": [
    {
      "id": "uuid",
      "author": { "role": "user" },
      "content": {
        "content_type": "text",
        "parts": ["你的问题"]
      }
    }
  ],
  "model": "gpt-4",
  "parent_message_id": "uuid",
  "timezone": "Asia/Shanghai"
}
```

响应格式：Server-Sent Events (SSE)

```
data: {"message": {"id": "xxx", "content": {"parts": ["回答..."]}}}
data: {"message": {"id": "xxx", "content": {"parts": ["回答继续..."]}}}
data: [DONE]
```

### 4.2 获取对话列表 API

```
GET https://chat.openai.com/backend-api/conversations?offset=0&limit=20
Cookie: __Secure-next-auth.session-token=xxx; ...
```

响应：

```json
{
  "items": [
    {
      "id": "conversation-id",
      "title": "对话标题",
      "create_time": 1234567890,
      "update_time": 1234567890
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

### 4.3 获取对话详情 API

```
GET https://chat.openai.com/backend-api/conversation/{conversation_id}
Cookie: __Secure-next-auth.session-token=xxx; ...
```

## 5. Session 有效期

根据观察和测试：

- Session token 有效期：约 14-30 天
- Cloudflare cookies 有效期：约 24 小时
- 如果长时间不活动，session 可能提前失效

## 6. Cookie 失效检测

### 6.1 检测方法

1. **HTTP 状态码检测**
   - 401 Unauthorized - session 已失效
   - 403 Forbidden - 可能是 Cloudflare 验证失败

2. **响应内容检测**
   - 如果响应重定向到 `/auth/login`，说明需要重新登录

3. **主动验证**
   - 访问 `https://chat.openai.com/` 检查是否重定向到登录页

### 6.2 自动刷新策略

```javascript
async function ensureValidSession() {
  // 1. 检查 session 文件是否存在
  if (!sessionFileExists()) {
    return await captureNewSession();
  }

  // 2. 检查 session 是否过期（基于时间）
  const sessionAge = getSessionAge();
  if (sessionAge > 30 * 24 * 60 * 60 * 1000) { // 30 days
    return await captureNewSession();
  }

  // 3. 主动验证 session 是否有效
  const isValid = await validateSession();
  if (!isValid) {
    return await captureNewSession();
  }

  return loadExistingSession();
}
```

## 7. 使用已登录的浏览器 Profile

### 7.1 Chrome Profile 路径

macOS:
```
/Users/{username}/Library/Application Support/Google/Chrome/Default
/Users/{username}/Library/Application Support/Google/Chrome/Profile 1
```

Windows:
```
C:\Users\{username}\AppData\Local\Google\Chrome\User Data\Default
C:\Users\{username}\AppData\Local\Google\Chrome\User Data\Profile 1
```

Linux:
```
~/.config/google-chrome/Default
~/.config/google-chrome/Profile 1
```

### 7.2 使用 Profile 的优势

1. **无需重新登录** - 直接使用已有的 session
2. **保留所有设置** - 包括扩展、书签等
3. **避免重复验证** - 不需要再次通过 Cloudflare 验证

### 7.3 实现方式

```javascript
import { chromium } from 'playwright';

const browser = await chromium.launch({
  channel: 'chrome',
  args: [
    `--user-data-dir=/Users/username/Library/Application Support/Google/Chrome/Default`
  ]
});
```

## 8. 安全注意事项

### 8.1 Cookie 存储安全

- ✅ 将 `data/session.json` 添加到 `.gitignore`
- ✅ 设置文件权限为 600 (仅所有者可读写)
- ✅ 不要在日志中打印完整的 cookie 值
- ✅ 定期清理过期的 session 文件

### 8.2 请求安全

- ✅ 始终使用 HTTPS
- ✅ 设置正确的 User-Agent
- ✅ 设置正确的 Referer 和 Origin
- ✅ 避免过于频繁的请求（建议间隔 1-2 秒）

### 8.3 错误处理

```javascript
try {
  const response = await sendMessage(message);
} catch (error) {
  if (error.message.includes('Authentication failed')) {
    // Session 失效，需要重新登录
    await refreshSession();
    // 重试
    return await sendMessage(message);
  }
  throw error;
}
```

## 9. 限制和注意事项

### 9.1 API 限制

- **速率限制**: 免费用户约 50 条消息/3 小时
- **Plus 用户**: 约 40 条 GPT-4 消息/3 小时
- **模型访问**: GPT-4 需要 Plus 订阅

### 9.2 Cloudflare 保护

ChatGPT 使用 Cloudflare 保护，可能遇到：

- **人机验证**: 需要手动完成验证
- **IP 限制**: 频繁请求可能被限制
- **地区限制**: 某些地区可能无法访问

### 9.3 账号安全

- 不要分享你的 session token
- 定期更换密码
- 启用两步验证
- 监控账号活动

## 10. 故障排查

### 10.1 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 401 Unauthorized | Session 失效 | 重新登录 |
| 403 Forbidden | Cloudflare 验证失败 | 手动完成验证 |
| 429 Too Many Requests | 请求过于频繁 | 增加请求间隔 |
| 500 Internal Server Error | OpenAI 服务器错误 | 稍后重试 |

### 10.2 调试技巧

1. **查看完整的 HTTP 请求/响应**
   ```javascript
   // 在 fetch 前添加日志
   console.log('Request:', {
     url,
     headers,
     body: JSON.stringify(payload, null, 2)
   });
   ```

2. **使用浏览器开发者工具**
   - 打开 Network 面板
   - 筛选 XHR/Fetch 请求
   - 查看 Request Headers 和 Response

3. **对比正常请求**
   - 在浏览器中手动发送消息
   - 复制请求的所有 headers
   - 在代码中模拟相同的请求

## 11. 参考资料

- [ChatGPT Web API 逆向工程](https://github.com/acheong08/ChatGPT)
- [NextAuth.js 文档](https://next-auth.js.org/)
- [Playwright 文档](https://playwright.dev/)
- [Server-Sent Events 规范](https://html.spec.whatwg.org/multipage/server-sent-events.html)
