# RiceQuant Session 管理 - 改进完成

## ✅ 已完成改进

### 1. 自动检查 Session 状态
- ✅ 检查 session 文件是否存在
- ✅ 验证 session 是否过期（7天有效期）
- ✅ 验证是否已登录
- ✅ 验证 cookies 是否有效

### 2. 自动登录获取 Session
- ✅ Session 无效时自动启动浏览器
- ✅ 自动填写账号密码
- ✅ 自动提交登录
- ✅ 自动保存新 session

### 3. Headless 模式（无界面）
- ✅ 默认使用无界面模式
- ✅ 不会跳出浏览器窗口
- ✅ 完全后台运行

---

## 🎯 使用方式

### 一次性配置
```bash
# 创建 .env 文件
vim .env
```

添加以下内容：
```env
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research
```

### 直接运行（自动管理 Session）
```bash
# 系统自动检查和登录
node run-strategy.js --strategy examples/simple_backtest.py
```

### 测试 Session 状态
```bash
npm run test-session
```

---

## 📊 工作流程

```
用户运行策略
    ↓
检查 session.json
    ↓
Session 有效？
    ├─ 是 → 直接使用 → 运行策略
    └─ 否 → 启动浏览器（headless）
              ↓
          自动登录
              ↓
          保存 session
              ↓
          运行策略
```

---

## 📝 输出示例

### 首次运行（自动登录）
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

### 后续运行（复用 Session）
```
✓ 使用现有 session（未过期）
  Session 文件: data/session.json
  Session 时间: 2024-03-30T10:00:00.000Z
✓ Session 验证成功
执行策略...
```

---

## 📚 文档

- **详细说明**：[SESSION_MANAGEMENT.md](SESSION_MANAGEMENT.md)
- **改进总结**：[SESSION_UPDATE.md](SESSION_UPDATE.md)
- **快速参考**：[QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 🔧 相关文件

### 新增/修改文件
- `request/ensure-ricequant-notebook-session.js` - Session 管理逻辑
- `browser/capture-ricequant-notebook-session.js` - 浏览器登录
- `test-session.js` - Session 测试脚本
- `SESSION_MANAGEMENT.md` - 详细文档
- `SESSION_UPDATE.md` - 改进总结

### 配置文件
- `.env` - 环境变量配置
- `data/session.json` - Session 存储

---

## ✨ 核心优势

| 特性 | 改进前 | 改进后 |
|------|--------|--------|
| Session 检查 | 手动检查 | ✅ 自动检查 |
| 登录方式 | 手动运行脚本 | ✅ 自动登录 |
| 浏览器模式 | 可能跳出界面 | ✅ Headless（无界面）|
| 状态提示 | 无清晰提示 | ✅ 详细日志 |
| 用户干预 | 需要多次操作 | ✅ 一次配置即可 |

---

## 🚀 立即开始

```bash
# 1. 配置环境变量
vim .env

# 2. 测试 session 管理
npm run test-session

# 3. 运行你的策略
node run-strategy.js --strategy your_strategy.py
```

**配置一次，后续全自动！**