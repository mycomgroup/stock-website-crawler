# Session管理快速总结

**更新时间：** 2026-04-02

---

## 一、Session管理对比

| 项目 | JoinQuant | RiceQuant |
|------|-----------|-----------|
| **有效期** | ~1天 | 7天 |
| **管理方式** | ⚠️ 手动抓取 | ✅ 自动登录 |
| **登录方式** | 有头浏览器 | Headless/有头 |
| **过期处理** | 手动重抓 | 自动重新登录 |
| **Cookies数量** | 8-12个 | 4-5个 |
| **推荐优先级** | Notebook优先 | 策略编辑器优先 |

---

## 二、JoinQuant Session

### 2.1 Session文件

**位置：** `skills/joinquant_notebook/data/session.json`

**内容示例：**
```json
{
  "capturedAt": "2026-03-31T08:07:33.734Z",
  "notebookUrl": "https://www.joinquant.com/user/notebook?url=/user/21333940833/notebooks/test.ipynb",
  "cookies": [
    {"name": "user-21333940833", "value": "..."},
    {"name": "jupyter-hub-token", "value": "..."},
    ...
  ]
}
```

### 2.2 抓取命令

```bash
# 进入目录
cd skills/joinquant_notebook

# 有头模式（推荐，可以看到浏览器操作）
node browser/capture-joinquant-session.js --headed

# 无头模式（后台运行）
node browser/capture-joinquant-session.js
```

### 2.3 验证Session

```bash
# 测试连接
node run-strategy.js --cell-source "print('test')" --timeout-ms 30000

# 预期输出
# 输出: test
```

### 2.4 Session过期处理

**症状：**
- 报错：`Session expired` 或 `401 Unauthorized`
- 解决：重新运行抓取命令

**建议：**
- 每次使用前检查session是否过期
- Session有效期约1天，建议每天重新抓取

---

## 三、RiceQuant Session

### 3.1 Session文件

**位置：** `skills/ricequant_strategy/data/session.json`

**内容示例：**
```json
{
  "capturedAt": "2026-04-02T02:29:00.000Z",
  "cookies": [
    {"name": "tgw_l7_route", "value": "..."},
    {"name": "RQSESSIONID", "value": "..."},
    ...
  ]
}
```

### 3.2 自动登录

**无需手动操作，系统自动处理：**

1. 检查现有session是否有效
2. Session无效时自动登录
3. 登录成功后自动保存session
4. 后续运行自动复用session

**使用命令：**
```bash
# 进入目录
cd skills/ricequant_strategy

# 运行策略（自动处理session）
node run-skill.js --id <策略ID> --file <策略文件> --start 2024-01-01 --end 2024-12-31

# 或运行Notebook
node run-strategy.js --strategy examples/simple_backtest.py
```

### 3.3 验证Session

```bash
# 测试session状态
npm run test-session

# 或列出策略（验证登录）
node list-strategies.js
```

### 3.4 Session过期处理

**无需手动处理：**
- 系统检测到session过期
- 自动启动headless登录
- 获取新session并保存
- 继续执行命令

**有效期：** 7天

---

## 四、快速命令参考

### JoinQuant

```bash
# 抓取session
cd skills/joinquant_notebook
node browser/capture-joinquant-session.js --headed

# 运行策略
node run-strategy.js --strategy examples/test.py --timeout-ms 600000

# 查看结果
cat output/joinquant-notebook-result-*.json
```

### RiceQuant

```bash
# 运行回测（自动处理session）
cd skills/ricequant_strategy
node run-skill.js --id 2415370 --file examples/mainline_final_v2.py --start 2024-01-01 --end 2024-12-31

# 列出策略
node list-strategies.js

# 获取报告
node fetch-report.js --id <backtest_id>
```

---

## 五、常见问题

### Q1: JoinQuant Session总是过期？

**原因：** JoinQuant session有效期短（约1天）

**解决：**
```bash
# 每次使用前重新抓取
node browser/capture-joinquant-session.js --headed
```

---

### Q2: RiceQuant自动登录失败？

**原因：** 登录页面变化或网络问题

**解决：**
```bash
# 有头模式手动登录
node browser/capture-ricequant-notebook-session.js --headed

# 手动登录后，session会自动保存
```

---

### Q3: 如何判断session是否有效？

**JoinQuant：**
```bash
node run-strategy.js --cell-source "print('ok')"
# 输出 "ok" = 有效
# 报错 = 过期
```

**RiceQuant：**
```bash
node list-strategies.js
# 列出策略列表 = 有效
# 提示登录 = 过期（会自动登录）
```

---

### Q4: Session文件可以复制吗？

**不建议：**
- Session包含敏感信息（cookies、tokens）
- 与特定浏览器/设备绑定
- 建议每个环境单独抓取

---

## 六、最佳实践

### JoinQuant

1. ✅ 每次使用前检查session
2. ✅ 使用有头模式抓取（可以看到操作）
3. ✅ Session过期后立即重新抓取
4. ⚠️ 不要跨设备复制session文件

### RiceQuant

1. ✅ 信任自动登录机制
2. ✅ 无需手动管理session
3. ✅ Session过期会自动处理
4. ⚠️ 如果自动登录失败，使用有头模式

---

## 七、安全提示

**Session文件包含敏感信息：**
- ❌ 不要提交到git
- ❌ 不要分享给他人
- ❌ 不要复制到其他设备
- ✅ 已在`.gitignore`中排除

**查看.gitignore：**
```bash
# skills/joinquant_notebook/.gitignore
data/session.json
output/*.json

# skills/ricequant_strategy/.gitignore
data/session.json
data/*.json
```

---

## 八、文档位置

**详细文档：**
- `session_management/JoinQuant_Session_Guide.md` - JoinQuant完整指南
- `session_management/RiceQuant_Session_Guide.md` - RiceQuant完整指南
- `session_management/SESSION_MANAGEMENT.md` - Session管理详解

**快速参考：**
- `session_management/JoinQuant_Quick_Reference.md`
- `session_management/RiceQuant_Quick_Reference.md`

---

**总结：**
- **JoinQuant：** 手动管理，每天抓取，Notebook优先
- **RiceQuant：** 自动管理，无需干预，策略编辑器优先