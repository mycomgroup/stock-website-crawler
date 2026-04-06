# 导出 ChatGPT Cookies 完整指南

## 方法 1：使用 Cookie-Editor 扩展（推荐）

### 安装扩展

Chrome: https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm

### 导出步骤

1. 在 Chrome 中打开 https://chatgpt.com/ 并登录
2. 点击浏览器工具栏中的 Cookie-Editor 图标
3. 点击右上角的 "Export" 按钮（📤 图标）
4. 选择 "JSON" 格式
5. 复制所有内容
6. 运行命令：
   ```bash
   cd skills/chatgpt_api
   node import-cookies.js yuping3222
   ```
7. 粘贴复制的内容，按 Ctrl+D (Mac: Cmd+D) 结束

## 方法 2：使用 EditThisCookie 扩展

### 安装扩展

Chrome: https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg

### 导出步骤

1. 在 Chrome 中打开 https://chatgpt.com/ 并登录
2. 点击浏览器工具栏中的 EditThisCookie 图标
3. 点击底部的 "Export" 按钮
4. 复制导出的 JSON
5. 运行命令并粘贴

## 方法 3：手动从开发者工具复制

### 步骤

1. 打开 https://chatgpt.com/ 并登录
2. 按 F12 打开开发者工具
3. 切换到 "Application" 标签（或 "应用" 标签）
4. 左侧菜单选择 "Cookies" -> "https://chatgpt.com"
5. 找到以下关键 cookies 并记录：
   - `__Secure-next-auth.session-token` （最重要）
   - `__Secure-next-auth.callback-url`
   - `oai-sc`
   - `oai-did`
   - `_cfuvid`
   - `cf_clearance`

6. 手动创建 JSON 文件：

```json
[
  {
    "name": "__Secure-next-auth.session-token",
    "value": "你的token值",
    "domain": ".chatgpt.com",
    "path": "/",
    "secure": true,
    "httpOnly": true,
    "sameSite": "Lax"
  },
  {
    "name": "__Secure-next-auth.callback-url",
    "value": "https%3A%2F%2Fchatgpt.com",
    "domain": ".chatgpt.com",
    "path": "/",
    "secure": true,
    "httpOnly": true,
    "sameSite": "Lax"
  }
  // ... 其他 cookies
]
```

## 验证导入是否成功

```bash
# 查看账号列表
node run-skill.js --list-accounts

# 测试发送消息
node run-skill.js --message "你好"

# 查看账户信息
node run-skill.js --account
```

## 常见问题

### Q: 为什么 JavaScript 无法获取所有 cookies？

A: `__Secure-next-auth.session-token` 等关键 cookies 设置了 `HttpOnly` 属性，JavaScript 无法访问，必须使用浏览器扩展或手动复制。

### Q: 导入后还是报错 "fetch failed"？

A: 检查是否包含了 `__Secure-next-auth.session-token`，这是最关键的认证 cookie。

### Q: Cookies 有效期多久？

A: 通常 14-30 天，过期后需要重新导出。

### Q: 可以同时使用多个账号吗？

A: 可以！每个账号重复导出步骤，使用不同的账号名即可。

```bash
node import-cookies.js account1
node import-cookies.js account2
node import-cookies.js account3
```
