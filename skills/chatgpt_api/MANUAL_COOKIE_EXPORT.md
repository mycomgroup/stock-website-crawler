# 手动导出 Cookies 方法

由于 ChatGPT 会检测自动化浏览器，推荐使用手动方式导出 cookies。

## 方法 1：使用浏览器开发者工具（推荐）

### 步骤：

1. **在正常 Chrome 浏览器中登录 ChatGPT**
   - 打开 https://chatgpt.com/
   - 正常登录你的账号

2. **打开开发者工具**
   - 按 `F12` 或 `Cmd+Option+I` (Mac)
   - 切换到 `Console` 标签

3. **运行以下代码复制 cookies**

```javascript
// 复制所有 cookies
copy(JSON.stringify(document.cookie.split('; ').map(c => {
  const [name, ...v] = c.split('=');
  return {
    name,
    value: v.join('='),
    domain: '.chatgpt.com',
    path: '/',
    secure: true,
    httpOnly: false,
    sameSite: 'Lax'
  };
}), null, 2));
console.log('✅ Cookies 已复制到剪贴板');
```

4. **保存 cookies 到文件**

创建文件 `skills/chatgpt_api/data/accounts/session-yuping3222.json`：

```json
{
  "capturedAt": "2026-04-06T15:30:00.000Z",
  "cookies": [
    // 粘贴刚才复制的内容
  ],
  "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
```

5. **更新账号配置**

创建或编辑 `skills/chatgpt_api/data/accounts-config.json`：

```json
{
  "strategy": "round-robin",
  "accounts": [
    {
      "id": "yuping3222",
      "name": "yuping3222",
      "enabled": true,
      "weight": 1
    }
  ]
}
```

## 方法 2：使用浏览器扩展

### 推荐扩展：

1. **EditThisCookie** (Chrome)
   - 安装：https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
   - 登录 ChatGPT 后，点击扩展图标
   - 点击 "Export" 导出 cookies

2. **Cookie-Editor** (Chrome/Firefox)
   - 安装：https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm
   - 登录 ChatGPT 后，点击扩展图标
   - 导出所有 cookies

## 方法 3：使用命令行工具

我们可以创建一个简单的工具来导入手动复制的 cookies。

运行：
```bash
node run-skill.js --import-cookies yuping3222
```

然后粘贴从浏览器复制的 cookies。

## 验证 cookies 是否有效

```bash
node run-skill.js --validate
```

## 为什么要手动导出？

- ✅ 不会触发 ChatGPT 的自动化检测
- ✅ 使用真实浏览器的 cookies
- ✅ 更稳定，不会被封号
- ✅ 支持任何登录方式（Google、Microsoft、Apple、邮箱等）

## 注意事项

1. **Cookies 有效期**：通常 14-30 天，过期后需要重新导出
2. **安全性**：不要分享你的 cookies 文件
3. **多账号**：每个账号重复上述步骤，使用不同的文件名
