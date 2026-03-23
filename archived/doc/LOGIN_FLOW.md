# 登录流程说明

## 概述

爬虫现在在开始抓取任务时就会主动尝试登录，而不是等到遇到需要登录的页面才登录。

## 登录时机

1. **启动时登录**：在 `start()` 方法开始时，如果配置了 `login.required = true`，爬虫会立即尝试登录
2. **页面级登录**：如果启动时登录失败，在访问每个页面时仍会检查是否需要登录并尝试

## 登录策略

爬虫会按以下顺序尝试多种策略来找到登录页面：

### 策略 1: 使用配置的登录 URL

- 直接访问 `config.login.loginUrl` 中配置的 URL
- 检查页面是否有登录表单
- 如果有，尝试填写并提交登录表单

### 策略 2: 在主页查找登录链接

- 访问主页（`loginUrl` 或第一个 `seedUrl`）
- 查找包含以下文本或属性的链接/按钮：
  - `a[href*="login"]`
  - `a[href*="signin"]`
  - `a:has-text("登录")`
  - `a:has-text("登錄")`
  - `a:has-text("Login")`
  - `a:has-text("Sign in")`
  - `button:has-text("登录")`
  - `button:has-text("登錄")`
- 点击找到的链接，等待登录表单出现
- 尝试填写并提交登录表单

### 策略 3: 尝试常见登录 URL 路径

从网站的根域名开始，尝试以下常见路径：
- `/login`
- `/signin`
- `/user/login`
- `/account/login`
- `/auth/login`
- `/member/login`

对每个路径：
1. 访问该 URL
2. 检查是否有登录表单
3. 如果有，尝试填写并提交

## 登录检测

`needsLogin()` 方法使用多种策略检测是否需要登录：

1. **URL 检查**：URL 包含 `login`、`signin` 或 `auth`
2. **密码字段**：页面包含 `input[type="password"]`
3. **登录按钮**：页面包含登录相关的按钮
4. **登录表单**：页面包含 `form[action*="login"]`
5. **登录容器**：页面包含常见的登录容器类名

## 登录表单填写

### 用户名字段识别

支持多种用户名输入字段类型：
- 手机号：`input[placeholder*="手机"]`
- 账号：`input[placeholder*="账号"]`
- 用户名：`input[placeholder*="用户"]`
- 邮箱：`input[placeholder*="邮箱"]`
- 英文字段：`phone`, `username`, `email`
- 输入类型：`type="tel"`, `type="email"`, `type="text"`

### 密码字段识别

- 标准密码字段：`input[type="password"]`

### 登录按钮识别

支持多种登录按钮：
- 中文：`button:has-text("登录")`, `button:has-text("登錄")`
- 英文：`button:has-text("Login")`, `button:has-text("Sign in")`
- 提交按钮：`button[type="submit"]`, `input[type="submit"]`

## 配置示例

```json
{
  "login": {
    "required": true,
    "username": "your-username",
    "password": "your-password",
    "loginUrl": "https://example.com/"
  }
}
```

## 日志输出

登录过程会输出详细的日志信息：

```
[INFO] Login is required, attempting to login at start...
[INFO] Strategy 1: Trying configured login URL: https://example.com/
[INFO] Found login form on configured URL
[INFO] Login successful at start
```

或者如果需要尝试多个策略：

```
[INFO] Login is required, attempting to login at start...
[INFO] Strategy 1: Trying configured login URL: https://example.com/
[INFO] No login form found on configured URL, may already be logged in
[INFO] Strategy 2: Looking for login link on main page
[INFO] Found login link with selector: a:has-text("登录")
[INFO] Login form appeared after clicking link
[INFO] Login successful at start
```

## 状态管理

- 登录成功后，`isLoggedIn` 标志会被设置为 `true`
- 后续页面访问会跳过登录检查（除非遇到需要重新登录的情况）
- 如果启动时登录失败，每个页面仍会检查是否需要登录

## 故障处理

- 如果所有登录策略都失败，爬虫会记录警告但继续运行
- 在访问每个页面时，仍会检查是否需要登录并再次尝试
- 这确保即使启动时登录失败，仍有机会在后续页面登录
