# RiceQuant Session 管理改进总结

## 改进内容

根据您的需求，我已完成以下改进：

### ✅ 1. 自动检查 Session 是否已登录

**实现方式**：
- 在运行策略前自动检查 `data/session.json`
- 验证 session 是否有效（未过期、已登录、cookies 有效）
- 如果有效，直接使用，无需重复登录

**验证逻辑**：
```javascript
// 检查条件
✓ Session 文件存在
✓ 未过期（创建时间 < 7天）
✓ 已登录（login.loggedIn === true）
✓ Cookies 有效（至少2个有效 cookies）
```

---

### ✅ 2. 未登录时自动浏览器登录

**实现方式**：
- 如果 session 无效，自动启动浏览器登录
- 自动填写账号密码
- 自动提交登录
- 自动保存新 session

**工作流程**：
```
检查 session → 无效 → 启动浏览器 → 自动登录 → 保存 session → 继续运行
```

---

### ✅ 3. 浏览器 Headless 模式

**实现方式**：
- 默认使用 headless 模式（无界面）
- 不会跳出浏览器窗口
- 完全后台运行
- 除非明确指定 `--headed`

**配置方式**：
```javascript
// 默认配置
headless: true  // 无界面模式

// 如果需要界面（调试用）
headed: true    // 有界面模式
```

---

## 使用示例

### 场景 1：首次使用

```bash
# 1. 配置 .env 文件
vim .env
# RICEQUANT_USERNAME=your_username
# RICEQUANT_PASSWORD=your_password
# RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research

# 2. 直接运行（自动登录）
node run-strategy.js --strategy examples/simple_backtest.py
```

**输出**：
```
✗ 读取 session 失败: ENOENT
开始浏览器登录获取新 session...
=== RiceQuant Notebook Session Capture ===
模式: 无界面（headless）
启动浏览器...
访问 RiceQuant 主页...
填写登录信息...
✓ 登录成功
✓ Session 已保存: data/session.json
执行策略...
```

### 场景 2：后续使用（Session 有效）

```bash
# 直接运行（自动复用 session）
node run-strategy.js --strategy examples/simple_backtest.py
```

**输出**：
```
✓ 使用现有 session（未过期）
  Session 文件: data/session.json
  Session 时间: 2024-03-30T10:00:00.000Z
✓ Session 验证成功
执行策略...
```

### 场景 3：Session 过期

```bash
# Session 过期（自动重新登录）
node run-strategy.js --strategy examples/simple_backtest.py
```

**输出**：
```
✗ Session 已过期（超过7天）
开始浏览器登录获取新 session...
=== RiceQuant Notebook Session Capture ===
模式: 无界面（headless）
✓ 登录成功
✓ Session 已保存
执行策略...
```

---

## 测试验证

### 运行 Session 测试

```bash
# 测试 session 管理功能
npm run test-session
```

**测试内容**：
1. 检查现有 session 状态
2. 验证 session 是否可用
3. 测试自动登录功能

**预期输出**：
```
=== RiceQuant Session 管理测试 ===

步骤 1: 检查 session 状态...
✓ 使用现有 session（未过期）
✓ Session 验证成功

步骤 2: Session 管理结果:
  状态: 复用
  原因: existing-session-valid

步骤 3: 测试使用 session...
✓ Session 有效，可以访问 notebook

=== 测试成功 ===
```

---

## 改进对比

| 特性 | 改进前 | 改进后 |
|------|--------|--------|
| Session 检查 | ❌ 手动检查 | ✅ 自动检查 |
| 登录方式 | ❌ 手动运行脚本 | ✅ 自动登录 |
| 浏览器模式 | ❌ 可能跳出界面 | ✅ Headless（无界面）|
| 状态提示 | ❌ 无清晰提示 | ✅ 详细日志输出 |
| 用户干预 | ❌ 需要多次操作 | ✅ 一次配置即可 |

---

## 核心改进文件

### 1. `request/ensure-ricequant-notebook-session.js`

**改进内容**：
- 添加详细的 session 检查逻辑
- 添加清晰的状态日志输出
- 自动验证 session 可用性
- 自动触发浏览器登录

**关键代码**：
```javascript
// 检查现有 session
if (fs.existsSync(sessionFile)) {
  const sessionData = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
  
  if (!isSessionExpired(sessionData) && 
      sessionData.login?.loggedIn && 
      hasValidCookies(sessionData)) {
    console.log('✓ 使用现有 session（未过期）');
    return { refreshed: false };
  }
}

// Session 无效，自动登录
console.log('开始浏览器登录获取新 session...');
await captureRiceQuantNotebookSession({ headless: true });
```

### 2. `browser/capture-ricequant-notebook-session.js`

**改进内容**：
- 默认使用 headless 模式
- 添加详细的登录过程日志
- 自动填写账号密码
- 自动保存 session

**关键代码**：
```javascript
// 默认 headless 模式
const headless = args.headless !== false;

const browser = await chromium.launch({
  headless: headless && !headed
});

// 自动登录
console.log('填写登录信息...');
await usernameInput.fill(username);
await passwordInput.fill(password);
await submitButton.click();
```

### 3. `test-session.js`

**新增文件**：
- Session 管理测试脚本
- 验证 session 状态
- 测试自动登录功能

---

## 配置说明

### 环境变量（.env）

```env
# 必需配置
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research
```

### Session 有效期

- **有效期**：7 天
- **存储位置**：`data/session.json`
- **自动更新**：过期后自动重新登录

---

## 最佳实践

### 1. 日常使用

```bash
# 直接运行，系统自动管理 session
node run-strategy.js --strategy your_strategy.py
```

### 2. 首次配置

```bash
# 1. 配置 .env
vim .env

# 2. 测试 session
npm run test-session

# 3. 运行策略
node run-strategy.js --strategy examples/simple_backtest.py
```

### 3. 问题排查

```bash
# 测试 session 状态
npm run test-session

# 如果有问题，删除旧 session
rm data/session.json

# 重新运行
node run-strategy.js --strategy examples/simple_backtest.py
```

---

## 常见问题

### Q1: 为什么还是弹出浏览器？

**A**: 可能之前使用了 `--headed` 参数。解决方法：
```bash
# 删除旧 session，重新登录
rm data/session.json
node run-strategy.js --strategy examples/simple_backtest.py
```

### Q2: Session 一直提示过期？

**A**: 可能是系统时间问题或权限问题。解决方法：
```bash
# 检查系统时间
date

# 删除旧 session 重试
rm data/session.json
npm run test-session
```

### Q3: 登录失败怎么办？

**A**: 检查账号密码和网络连接：
```bash
# 检查环境变量
cat .env

# 测试网络
curl -I https://www.ricequant.com

# 手动测试登录（有界面模式）
node browser/capture-ricequant-notebook-session.js --headed
```

---

## 总结

✅ **自动检查 Session** - 无需手动检查  
✅ **自动登录获取** - Session 无效时自动登录  
✅ **Headless 模式** - 后台运行，不干扰用户  
✅ **详细日志输出** - 清晰的状态提示  
✅ **零用户干预** - 配置一次即可  

**用户只需配置一次账号密码，后续所有操作都会自动处理 session 管理！**