# RiceQuant Session 管理改进说明

## 改进内容

### ✅ 自动 Session 管理

**改进前的问题**：
- 每次运行都需要手动抓取 session
- 没有清晰的 session 状态检查
- 浏览器可能跳出界面干扰用户

**改进后的方案**：

#### 1. 智能 Session 检查
```javascript
// 自动检查 session 是否有效
✓ 使用现有 session（未过期）
  Session 文件: data/session.json
  Session 时间: 2024-03-30T10:00:00.000Z
✓ Session 验证成功
```

#### 2. 自动登录（Headless 模式）
```javascript
// Session 过期或不存在时自动登录
✗ Session 已过期（超过7天）
开始浏览器登录获取新 session...
=== RiceQuant Notebook Session Capture ===
模式: 无界面（headless）
启动浏览器...
访问 RiceQuant 主页...
填写登录信息...
✓ 登录成功
✓ Session 已保存: data/session.json
```

#### 3. 默认 Headless 模式
- 默认使用无界面模式（headless）
- 不会跳出浏览器窗口
- 完全后台运行

---

## 使用方式

### 方式 1：自动管理（推荐）

**直接运行策略，自动处理 session**：
```bash
node run-strategy.js --strategy examples/simple_backtest.py
```

**工作流程**：
1. 检查 `data/session.json` 是否存在
2. 验证 session 是否有效（未过期、已登录、cookies 有效）
3. 如果有效，直接使用
4. 如果无效，自动启动 headless 浏览器登录
5. 保存新 session 并继续运行

### 方式 2：测试 Session 状态

```bash
# 测试 session 管理功能
npm run test-session
```

**输出示例**：
```
=== RiceQuant Session 管理测试 ===

Notebook URL: https://www.ricequant.com/research

步骤 1: 检查 session 状态...

✓ 使用现有 session（未过期）
  Session 文件: data/session.json
  Session 时间: 2024-03-30T10:00:00.000Z
✓ Session 验证成功

步骤 2: Session 管理结果:
  状态: 复用
  原因: existing-session-valid
  文件: data/session.json

步骤 3: 测试使用 session...
✓ Session 有效，可以访问 notebook

=== 测试成功 ===
```

### 方式 3：强制重新登录

```bash
# 强制重新获取 session
node browser/capture-ricequant-notebook-session.js --force-login
```

---

## Session 验证逻辑

### 验证条件

Session 被认为有效需满足以下所有条件：

1. **文件存在**：`data/session.json` 存在
2. **未过期**：Session 创建时间 < 7天
3. **已登录**：`login.loggedIn === true`
4. **Cookies 有效**：
   - 至少有 2 个有效 cookies
   - Cookies 未过期
   - 包含必要的 session cookies

### 验证流程

```
开始
  ↓
检查 session.json 存在？ → 否 → 浏览器登录
  ↓ 是
检查未过期（< 7天）？ → 否 → 浏览器登录
  ↓ 是
检查已登录？ → 否 → 浏览器登录
  ↓ 是
检查 cookies 有效？ → 否 → 浏览器登录
  ↓ 是
尝试访问 notebook API
  ↓
成功？ → 是 → 使用现有 session
  ↓ 否
浏览器登录
```

---

## 详细日志输出

### Session 有效时的日志

```
✓ 使用现有 session（未过期）
  Session 文件: /path/to/data/session.json
  Session 时间: 2024-03-30T10:00:00.000Z
✓ Session 验证成功
```

### Session 无效时的日志

```
✗ Session 已过期（超过7天）
开始浏览器登录获取新 session...
=== RiceQuant Notebook Session Capture ===
模式: 无界面（headless）
Notebook URL: https://www.ricequant.com/research
启动浏览器...
访问 RiceQuant 主页...
当前 URL: https://www.ricequant.com/
切换到密码登录模式...
填写登录信息...
提交登录...
等待登录完成...
✓ 登录成功
访问 Notebook...
等待 Notebook 加载...
收集页面状态...
保存 session...
✓ Session 已保存: /path/to/data/session.json
```

---

## 配置说明

### 环境变量（.env）

```env
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research
```

### Session 文件结构

```json
{
  "capturedAt": "2024-03-30T10:00:00.000Z",
  "notebookUrl": "https://www.ricequant.com/research",
  "cookies": [
    {
      "name": "session",
      "value": "...",
      "domain": "ricequant.com",
      "path": "/",
      "expires": 1234567890
    }
  ],
  "login": {
    "loggedIn": true,
    "mode": "form-login"
  }
}
```

---

## 常见场景

### 场景 1：首次使用

```bash
# 1. 配置环境变量
vim .env

# 2. 直接运行，自动登录
node run-strategy.js --strategy examples/simple_backtest.py

# 输出：
✗ 读取 session 失败: ENOENT
开始浏览器登录获取新 session...
✓ 登录成功
✓ Session 已保存
执行策略...
```

### 场景 2：日常使用

```bash
# Session 有效，直接使用
node run-strategy.js --strategy examples/simple_backtest.py

# 输出：
✓ 使用现有 session（未过期）
✓ Session 验证成功
执行策略...
```

### 场景 3：Session 过期

```bash
# Session 过期，自动重新登录
node run-strategy.js --strategy examples/simple_backtest.py

# 输出：
✗ Session 已过期（超过7天）
开始浏览器登录获取新 session...
✓ 登录成功
✓ Session 已保存
执行策略...
```

---

## 优势对比

| 特性 | 改进前 | 改进后 |
|------|--------|--------|
| Session 检查 | 手动检查 | 自动检查 ✓ |
| 登录方式 | 手动登录 | 自动登录 ✓ |
| 浏览器模式 | 可能跳出 | Headless（无界面）✓ |
| 状态提示 | 无清晰提示 | 详细日志 ✓ |
| 用户干预 | 需要多次 | 一次配置即可 ✓ |

---

## 故障排查

### 问题 1：反复登录

**原因**：Session 文件损坏或权限问题

**解决**：
```bash
# 删除旧 session
rm data/session.json

# 重新运行
npm run test-session
```

### 问题 2：登录失败

**原因**：账号密码错误或网络问题

**解决**：
```bash
# 检查环境变量
cat .env

# 测试网络连接
curl -I https://www.ricequant.com

# 手动登录测试
node browser/capture-ricequant-notebook-session.js --headed
```

### 问题 3：Headless 模式失败

**原因**：某些网站需要界面渲染

**解决**：
```bash
# 临时使用有界面模式
node browser/capture-ricequant-notebook-session.js --headed
```

---

## 相关文件

- `request/ensure-ricequant-notebook-session.js` - Session 管理逻辑
- `browser/capture-ricequant-notebook-session.js` - 浏览器登录
- `test-session.js` - Session 测试脚本
- `data/session.json` - Session 存储

---

## 最佳实践

1. **首次配置**：确保 `.env` 文件正确
2. **日常使用**：直接运行，让系统自动管理 session
3. **问题排查**：使用 `npm run test-session` 诊断
4. **定期清理**：删除过期 session 文件（>7天）

---

## 总结

改进后的 Session 管理系统：

✅ **自动检查** session 状态  
✅ **自动登录** 获取新 session  
✅ **Headless 模式** 后台运行  
✅ **详细日志** 清晰的状态提示  
✅ **零干预** 一次配置即可  

用户只需配置一次账号密码，后续所有操作都会自动处理 session 管理！