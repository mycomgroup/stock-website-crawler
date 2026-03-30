# RiceQuant API 修复说明

## 问题诊断

### 1. API 端点格式

RiceQuant 使用 `.do` 后缀的 API 端点：

| 功能 | 正确端点 | 错误端点 |
|------|----------|----------|
| 检查登录 | `/api/user/isLogin.do` | `/api/user/v1/workspaces` |
| 登录 | `/api/user/login.do` | - |
| Workspaces | `/api/workspace/list.do` | `/api/user/v1/workspaces` |
| 策略列表 | `/api/workspace/strategies.do` | `/api/strategy/v1/...` |

### 2. 认证问题

登录 API 返回 `{"code":3,"message":"用户名或密码错误"}`

可能原因：
1. 密码不正确
2. 需要验证码
3. 需要其他验证方式

## 解决方案

### 方案一：手动登录捕获 Session（推荐）

```bash
cd skills/ricequant_strategy
node capture-session.js
```

然后：
1. 在打开的浏览器中手动登录
2. 导航到 workspace/strategies 页面
3. 等待脚本自动保存 session

### 方案二：检查密码

检查 `.env` 文件中的密码是否正确：
```
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
```

### 方案三：使用已登录的浏览器 Cookie

1. 打开 Chrome 浏览器
2. 登录 RiceQuant
3. 打开开发者工具 (F12)
4. 在 Application > Cookies 中找到 `sid` 和 `rqjwt`
5. 更新 `data/session.json`

## 文件结构

```
ricequant_strategy/
├── capture-session.js      # 手动捕获 session 脚本
├── login-test.js           # 登录测试脚本
├── debug-api.js            # API 调试脚本
├── request/
│   └── ricequant-client.js # 已更新的客户端（使用 .do 端点）
├── browser/
│   └── capture-api.js      # 高级 API 捕获脚本
└── data/
    ├── session.json        # Session 数据
    └── api_traces.json     # API 调用记录
```

## 更新内容

`ricequant-client.js` 已更新：

1. **API 端点**: 使用 `.do` 后缀
2. **登录方法**: 添加 `login()` 方法
3. **检查登录**: 添加 `checkLogin()` 方法
4. **Workspace**: 使用正确的端点获取

## 测试命令

```bash
# 测试登录
node login-test.js

# 调试 API
node debug-api.js

# 捕获 session
node capture-session.js

# 运行回测（登录成功后）
node run-skill.js --id <strategyId> --file ../strategies/Ricequant/rfscore7_pb10_final_v2.py
```

## 下一步

1. 运行 `node capture-session.js`
2. 在浏览器中登录
3. 登录成功后，session 会自动保存
4. 然后运行策略回测