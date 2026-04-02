# 同花顺量化手动登录指南

## 为什么需要手动登录？

同花顺量化平台使用特殊的 iframe 登录系统，包含:
- 多层iframe嵌套
- 动态验证码（可能）
- 特殊的session管理机制

为了确保登录成功并获取完整的session和API，建议使用手动登录方式。

## 登录步骤

### 步骤1: 运行登录脚本

```bash
cd skills/thsquant_strategy
node browser/manual-login-capture.js
```

### 步骤2: 等待浏览器打开

浏览器会自动打开同花顺量化页面:
```
https://quant.10jqka.com.cn/view/study-index.html
```

### 步骤3: 手动登录

1. 点击页面右上角的"登录"按钮
2. 在弹出的登录窗口中输入:
   - **账号**: `mx_kj1ku00qp`
   - **密码**: `f09173228552`
3. 点击登录按钮

### 步骤4: 等待登录成功

脚本会自动检测登录状态:
- 检测到"HI！"或用户名显示
- 显示 "✓ Login detected!"
- 自动等待30秒让你浏览策略页面

### 步骤5: 浏览策略页面

为了捕获完整的API端点，建议:
1. 点击"策略研究"菜单
2. 点击"我的研究"
3. 点击不同的策略项目
4. 尝试打开回测界面

这样可以触发各种策略相关的API请求。

### 步骤6: 自动保存

脚本会在以下时机自动保存:
- 登录成功后保存session
- 浏览页面时捕获API
- 60秒后自动关闭浏览器

## 验证登录

### 方法1: 检查session文件

```bash
cat data/session.json
```

应该看到:
```json
{
  "cookies": [
    {
      "name": "QUANT_RESEARCH_SESSIONID",
      "value": "...",
      "domain": "quant.10jqka.com.cn"
    },
    ...
  ],
  "timestamp": 1774966098355
}
```

### 方法2: 运行session测试

```bash
node test-session.js
```

期望输出:
```
✓ Login successful
✓ Found X strategies
```

## 查看捕获的API

登录后，查看捕获的API端点:

```bash
cat data/manual-login-api-capture.json
```

这个文件包含:
- 所有API请求URL
- 请求方法 (GET/POST)
- POST数据
- 响应内容

### 提取关键API

从捕获结果中提取策略相关的API:

```bash
# 查找包含 "strategy" 的API
grep -i "strategy" data/manual-login-api-capture.json

# 查找包含 "backtest" 的API
grep -i "backtest" data/manual-login-api-capture.json
```

## 常见问题

### Q: 浏览器没有打开？

A: 
1. 检查 Playwright 是否安装: `npm install`
2. 检查 Chromium 是否下载: 会自动下载
3. 检查终端输出是否有错误

### Q: 登录窗口没有弹出？

A: 
1. 查看页面右上角是否显示"登录"按钮
2. 如果显示"HI！用户名"，说明已经登录
3. 手动点击登录按钮

### Q: 登录失败？

A: 
1. 检查账号密码是否正确
2. 检查是否有验证码（需要手动输入）
3. 尝试直接在同花顺官网登录后再运行脚本

### Q: Session过期？

A: Session有效期约7天。过期后重新运行登录脚本。

### Q: 找不到策略API？

A: 
1. 登录成功后多浏览几个页面
2. 点击策略列表中的具体策略
3. 尝试打开回测界面
4. 查看完整的 `manual-login-api-capture.json`

## 替代方案

### 方法1: 直接浏览器录制

1. 手动打开浏览器
2. 登录同花顺量化
3. 使用浏览器开发者工具录制网络请求
4. 导出 HAR 文件

### 方法2: 使用现有session

如果你之前已经登录过:
```bash
# 直接使用现有session
node test-complete.js
```

## 下一步

登录成功后:

1. **查看策略列表**
   ```bash
   node list-strategies.js
   ```

2. **运行回测**
   ```bash
   node run-skill.js --id <strategyId> --file examples/ma_strategy.py
   ```

3. **获取回测报告**
   ```bash
   node fetch-report.js --id <backtestId>
   ```

## Session有效期管理

Session文件包含:
- Cookies（认证信息）
- Timestamp（保存时间）

系统会自动检查:
```javascript
const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000; // 7天
const isExpired = Date.now() - session.timestamp > SESSION_DURATION;
```

过期后需要重新登录。

## 技术细节

### 检测登录成功的方法

脚本使用多种方式检测登录:
1. 页面HTML包含 `header-usr-logined`
2. 页面HTML包含 `HI！`
3. 页面HTML包含用户名

### 保存的内容

Session文件保存:
- 所有cookies（包括session ID）
- 登录时间戳
- 当前页面URL

API捕获文件保存:
- 请求URL
- 请求方法
- POST数据
- 响应内容
- 时间戳

## 总结

手动登录虽然不如自动登录方便，但有以下优势:
- ✅ 100%成功率
- ✅ 可以处理验证码
- ✅ 可以完整捕获API
- ✅ 避免自动化检测

建议首次使用时耐心完成手动登录，后续可以直接使用保存的session。