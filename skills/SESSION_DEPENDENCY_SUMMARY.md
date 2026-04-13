# 统一 Session 管理后的浏览器依赖分析

## 概述

使用 `skills/common_auth` 统一管理所有网站的 session，并将 session 存储在 `skills/.sessions/` 目录后，各个技能对浏览器的依赖情况如下：

## Session 管理架构

```
skills/
├── common_auth/              # 统一认证中心
│   ├── login.js             # 统一登录入口
│   ├── auth-manager.js      # Session 管理器
│   └── sites/               # 各站点适配器
│       ├── 10jqka.js
│       ├── guorn.js
│       └── thsquant.js
│
└── .sessions/               # 集中 Session 仓库
    ├── 10jqka.json
    ├── guorn.json
    └── thsquant.json
```

## 登录方式（common_auth 支持）

| 方式 | 命令 | 是否需要浏览器 | 说明 |
|------|------|---------------|------|
| **本地提取** | `--method=local` | ❌ 不需要 | 从本地 Chrome 进程提取 cookies（推荐） |
| **自动化登录** | `--method=auto` | ✅ 需要（headless） | 自动填写账号密码 |
| **手动捕获** | `--method=manual` | ✅ 需要（headed） | 用户手动登录，系统捕获 |
| **插件导入** | `--method=import` | ❌ 不需要 | 粘贴从浏览器插件导出的 JSON |

## 各技能浏览器依赖分析

### ✅ 完全不需要浏览器（仅用 HTTP API）

使用统一 session 后，以下技能**完全不需要浏览器**：

| Skill | Session 来源 | 运行方式 | 说明 |
|-------|------------|---------|------|
| **joinquant_strategy** | `.sessions/joinquant.json` | 纯 HTTP API | ✅ 已完全 HTTP 化 |
| **ricequant_strategy** | `.sessions/ricequant.json` | 纯 HTTP API | ✅ 已完全 HTTP 化 |
| **bigquant_strategy** | `.sessions/bigquant.json` | 纯 HTTP API | ✅ 已完全 HTTP 化 |
| **thsquant_strategy** | `.sessions/thsquant.json` | 纯 HTTP API | ✅ 已完全 HTTP 化 |
| **lixinger-screener** (request/) | `.sessions/lixinger.json` | 纯 HTTP API | ✅ request 模式完全 HTTP 化 |
| **chatgpt_api** | `.sessions/chatgpt.json` | 纯 HTTP API | ✅ 已完全 HTTP 化 |
| **gemini_api** | `.sessions/gemini.json` | 纯 HTTP API | ✅ 已完全 HTTP 化 |

### ⚠️ 部分依赖浏览器（特定功能）

这些技能的**核心功能**可以用 HTTP API，但**某些特定操作**仍需浏览器：

| Skill | Session 来源 | 仍需浏览器的场景 | 原因 |
|-------|------------|----------------|------|
| **guorn_strategy** | `.sessions/guorn.json` | 策略保存、回测触发 | 果仁网无公开 REST API |
| **10jqka_backtest** | `.sessions/10jqka.json` | 回测提交、滑块验证 | 问财平台有滑块验证 |
| **lixinger-screener** (browser/) | `.sessions/lixinger.json` | 自然语言筛选 | 复杂交互需要浏览器 |

### 🔴 必须依赖浏览器（核心功能）

这些技能的**核心功能**就是浏览器操作，无法避免：

| Skill | 用途 | 说明 |
|-------|------|------|
| **html-template-generator** | SPA 页面渲染 | 需要执行 JavaScript |
| **stock-crawler** | 动态内容抓取 | 需要渲染页面 |
| **web-api-generator** | HAR 文件录制 | 需要浏览器录制网络请求 |

## 详细分析

### 1. BigQuant Strategy

**Session 后状态：**
- ✅ **登录**：通过 `common_auth` 获取 session
- ✅ **策略提交**：HTTP API (`POST /taskruns`)
- ✅ **结果获取**：HTTP API (`GET /logs/{runId}`)
- ❌ **不再需要浏览器**

**使用方式：**
```bash
# 1. 统一登录（一次性）
cd skills/common_auth
node login.js bigquant --method=local

# 2. 运行策略（纯 HTTP）
cd skills/bigquant_strategy
node run-skill.js --strategy examples/my_strategy.py
```

### 2. THSQuant Strategy

**Session 后状态：**
- ✅ **登录**：通过 `common_auth` 获取 session
- ✅ **策略操作**：HTTP API
- ✅ **回测运行**：HTTP API
- ❌ **不再需要浏览器**

**使用方式：**
```bash
# 1. 统一登录（推荐手动模式）
cd skills/common_auth
node login.js thsquant --method=manual

# 2. 运行回测（纯 HTTP）
cd skills/thsquant_strategy
node run-skill.js --id <strategyId> --file examples/ma_strategy.py
```

### 3. Guorn Strategy

**Session 后状态：**
- ✅ **登录**：通过 `common_auth` 获取 session
- ✅ **数据查询**：HTTP API
- ⚠️ **策略保存**：仍需浏览器（无公开 API）
- ⚠️ **回测触发**：仍需浏览器（无公开 API）

**使用方式：**
```bash
# 1. 统一登录
cd skills/common_auth
node login.js guorn --method=local

# 2. 查询数据（纯 HTTP）
cd skills/guorn_strategy
node request/query-data.js

# 3. 运行回测（仍需浏览器）
node browser/run-backtest.js
```

**改进建议：**
- 通过浏览器开发者工具抓取策略保存和回测的 API
- 实现 HTTP 版本的策略保存和回测触发

### 4. RiceQuant Strategy

**Session 后状态：**
- ✅ **登录**：通过 `common_auth` 获取 session
- ✅ **Notebook 运行**：HTTP API
- ✅ **策略编辑器回测**：HTTP API
- ❌ **不再需要浏览器**

**使用方式：**
```bash
# 1. 统一登录
cd skills/common_auth
node login.js ricequant --method=local

# 2. Notebook 运行（纯 HTTP）
cd skills/ricequant_strategy
node run-strategy.js --strategy examples/simple_backtest.py

# 3. 策略编辑器回测（纯 HTTP）
node run-skill.js --id <strategyId> --file my-strategy.py
```

### 5. JoinQuant Strategy

**Session 后状态：**
- ✅ **登录**：通过 `common_auth` 获取 session
- ✅ **策略提交**：HTTP API
- ✅ **回测运行**：HTTP API
- ✅ **结果获取**：HTTP API
- ❌ **不再需要浏览器**

**使用方式：**
```bash
# 1. 统一登录
cd skills/common_auth
node login.js joinquant --method=local

# 2. 批量提交（纯 HTTP）
cd skills/joinquant_strategy
node batch_submit_selected.js
```

### 6. Lixinger Screener

**Session 后状态：**
- ✅ **登录**：通过 `common_auth` 获取 session
- ✅ **request 模式**：纯 HTTP API（推荐）
- ⚠️ **browser 模式**：仍需浏览器（自然语言筛选）

**使用方式：**
```bash
# 1. 统一登录
cd skills/common_auth
node login.js lixinger --method=local

# 2. request 模式（纯 HTTP，推荐）
cd skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --query "PE-TTM(扣非)统计值10年分位点小于30%，股息率大于2%" \
  --output markdown

# 3. browser 模式（仍需浏览器）
node run-skill.js --query "复杂自然语言查询" --headless false
```

### 7. ChatGPT API & Gemini API

**Session 后状态：**
- ✅ **登录**：通过 `common_auth` 获取 session
- ✅ **发送消息**：HTTP API
- ✅ **对话管理**：HTTP API
- ❌ **不再需要浏览器**

**使用方式：**
```bash
# 1. 统一登录
cd skills/common_auth
node login.js chatgpt --method=local
node login.js gemini --method=local

# 2. 发送消息（纯 HTTP）
cd skills/chatgpt_api
node run-skill.js --message "解释一下 JavaScript 的闭包"

cd skills/gemini_api
node run-skill.js --message "解释一下量子计算"
```

### 8. 10jqka Backtest

**Session 后状态：**
- ✅ **登录**：通过 `common_auth` 获取 session
- ⚠️ **回测提交**：仍需浏览器（滑块验证）
- ⚠️ **结果获取**：可能需要浏览器

**使用方式：**
```bash
# 1. 统一登录
cd skills/common_auth
node login.js 10jqka --method=manual

# 2. 运行回测（仍需浏览器处理滑块）
cd skills/10jqka_backtest
node run-skill.js examples/formula_strategy.json
```

**改进建议：**
- 研究滑块验证的绕过方法
- 或使用打码平台自动处理滑块

### 9. HTML Template Generator & Stock Crawler

**Session 后状态：**
- ⚠️ **核心功能就是浏览器操作**
- 无法避免浏览器依赖

**说明：**
这些是通用爬虫工具，核心功能就是：
- 渲染 SPA 页面
- 执行 JavaScript
- 抓取动态内容

**改进建议：**
- 增加 stealth plugin 防检测
- 实现请求频率控制
- 考虑使用无头浏览器服务（如 Browserless）

## 统一登录流程

### 一次性登录所有网站

```bash
cd skills/common_auth

# 方式1：本地提取（推荐，无需浏览器）
node login.js all --method=local

# 方式2：自动化登录（需要 headless 浏览器）
node login.js all --method=auto

# 方式3：手动登录（需要 headed 浏览器）
node login.js all --method=manual
```

### 验证 Session 是否有效

```bash
# API 验证（自动）
node login.js 10jqka

# 视觉验证（手动）
node login.js 10jqka --test
```

### Session 文件结构

```json
{
  "cookies": [
    {
      "name": "session_id",
      "value": "xxx",
      "domain": ".example.com",
      "path": "/"
    }
  ],
  "timestamp": 1234567890,
  "url": "https://example.com",
  "user": "username"
}
```

## 总结

### 完全不需要浏览器（7个）

使用统一 session 后，以下技能**完全不需要浏览器**：

1. ✅ **joinquant_strategy** - 纯 HTTP API
2. ✅ **ricequant_strategy** - 纯 HTTP API
3. ✅ **bigquant_strategy** - 纯 HTTP API
4. ✅ **thsquant_strategy** - 纯 HTTP API
5. ✅ **lixinger-screener** (request/) - 纯 HTTP API
6. ✅ **chatgpt_api** - 纯 HTTP API
7. ✅ **gemini_api** - 纯 HTTP API

### 部分依赖浏览器（3个）

这些技能的某些功能仍需浏览器：

1. ⚠️ **guorn_strategy** - 策略保存、回测触发需要浏览器
2. ⚠️ **10jqka_backtest** - 滑块验证需要浏览器
3. ⚠️ **lixinger-screener** (browser/) - 自然语言筛选需要浏览器

### 必须依赖浏览器（3个）

这些是通用爬虫工具，核心功能就是浏览器操作：

1. 🔴 **html-template-generator** - SPA 渲染
2. 🔴 **stock-crawler** - 动态内容抓取
3. 🔴 **web-api-generator** - HAR 录制

## 最佳实践

### 1. 登录策略

```bash
# 推荐：本地提取（最快，无需浏览器）
node login.js all --method=local

# 备选：手动登录（最可靠）
node login.js all --method=manual
```

### 2. Session 管理

- Session 有效期：通常 7-30 天
- 自动验证：每次使用前自动验证
- 自动刷新：失效时自动重新登录

### 3. 防封措施

即使使用统一 session，仍需注意：

- **请求频率控制**：避免过于频繁
- **User-Agent 轮换**：模拟不同设备
- **请求间隔随机化**：避免规律性
- **完整 headers 模拟**：包含所有必要字段

### 4. 错误处理

```javascript
// 示例：自动处理 session 失效
async function runWithSession(skill) {
  try {
    return await skill.run();
  } catch (error) {
    if (error.message.includes('401') || error.message.includes('403')) {
      console.log('Session 失效，正在刷新...');
      await refreshSession(skill.name);
      return await skill.run();
    }
    throw error;
  }
}
```

## 改进建议

### 高优先级

1. **guorn_strategy**
   - 抓取策略保存和回测的 API
   - 实现纯 HTTP 版本

2. **10jqka_backtest**
   - 研究滑块验证绕过
   - 或集成打码平台

3. **lixinger-screener**
   - 优先使用 request 模式
   - 减少 browser 模式使用

### 中优先级

1. **所有技能**
   - 统一使用 `common_auth`
   - 统一 session 存储路径
   - 统一错误处理

2. **防封措施**
   - 创建通用防封工具包
   - 统一请求频率控制
   - 统一 User-Agent 管理

### 低优先级

1. **爬虫工具**
   - 增加 stealth plugin
   - 实现代理池
   - 考虑云端浏览器服务

## 结论

使用 `skills/common_auth` 统一管理 session 后：

- **70%** 的技能（7/10）**完全不需要浏览器**
- **30%** 的技能（3/10）仍需浏览器处理特定场景
- 通用爬虫工具（3个）核心功能就是浏览器操作

**关键优势：**
1. ✅ 一次登录，全局复用
2. ✅ 自动验证和刷新
3. ✅ 集中管理，易于维护
4. ✅ 大幅减少浏览器使用
5. ✅ 降低被封风险

**建议：**
- 优先使用 `--method=local` 本地提取（最快，无需浏览器）
- 定期验证 session 有效性
- 为仍需浏览器的场景增加防封措施
