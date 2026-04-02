# BigQuant Strategy Skill 实现状态

## 一、API 修复记录（2026-04-02）

### 已修复的问题

| 原问题 | 原因 | 修复方案 |
|--------|------|----------|
| PUT /tasks/{id} → 405 | BigQuant 使用 PATCH 而非 PUT | 改用 PATCH，格式 `{ "code": xxx }` |
| GET /taskruns/{id} → 404 | 不支持直接获取单个 taskrun | 改用 `GET /taskruns?constraints={"id":"xxx"}` |

### 无法修复的问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| POST /tasks/{id}/run → 404 | BigQuant 不暴露运行 API | 需 Web UI 手动运行 |
| GET /tasks/{id}/result → 404 | BigQuant 不暴露结果 API | 需 Web UI 查看 |

---

## 二、与 JoinQuant/RiceQuant 对比

| 功能 | JoinQuant | RiceQuant | BigQuant |
|------|-----------|-----------|----------|
| **架构** | Jupyter Notebook | Jupyter Notebook | VS Code Web (code-server) |
| **创建任务** | ✓ | ✓ | ✓ |
| **更新代码** | ✓ PUT | ✓ PUT | ✗ API 不支持 |
| **运行任务** | ✓ WebSocket | ✓ WebSocket | ✗ 无直接 API |
| **自动执行** | ✓ | ✓ | ✗ 停留在 pending |
| **获取输出** | ✓ WebSocket stream | ✓ WebSocket stream | ✗ 未知 |

## 二、深度 API 探索结论

### 已探索的方案

#### 1. WebSocket 协议分析

**发现**:
- WebSocket URL: `wss://bigquant.com/aistudio/studios/{studio_id}/stable-{hash}`
- 这是 VS Code Web 的通信通道，使用复杂的二进制帧协议
- 消息格式: 非 Jupyter 的简单 JSON，而是 VS Code 特有的帧格式
- 连接后只收到 ping 消息 `\t\u0000\u0000...` (空帧)

**结论**: VS Code WebSocket 协议复杂，无法直接用于任务执行

#### 2. HTTP API 触发尝试

测试的所有触发 API:

| API | 方法 | 结果 |
|-----|------|------|
| `/aiflow/v1/taskruns/{id}/start` | POST | 404 |
| `/aiflow/v1/taskruns/{id}/execute` | POST | 404 |
| `/aiflow/v1/taskruns/{id}/run` | POST | 404 |
| `/aiflow/v1/tasks/{id}/trigger` | POST | 404 |
| `/aiflow/v1/tasks/{id}/execute` | POST | 404 |
| `/aiflow/v1/taskruns/{id}` | PUT (state=running) | 404 |

**结论**: BigQuant 没有暴露任务触发 API

#### 3. Studio Instance 激活

- API: `POST /aistudio/v1/studios/{id}/instances`
- 成功激活 studio (`status: "running"`)
- 但 taskrun 仍然停留在 `pending` 状态

**结论**: Studio 激活 ≠ 任务执行触发

### 可用的 API

| API | 方法 | 状态 |
|-----|------|------|
| `/auth/v1/users/me` | GET | ✓ 用户信息 |
| `/aiflow/v1/tasks` | GET | ✓ 列出任务 |
| `/aiflow/v1/tasks` | POST | ✓ 创建任务 |
| `/aiflow/v1/tasks/{id}` | GET | ✓ 任务详情 |
| `/aiflow/v1/taskruns` | POST | ✓ 创建运行 (但不执行) |
| `/aiflow/v1/taskruns` | GET | ✓ 运行列表 |
| `/aiflow/v1/resourcespecs` | GET | ✓ 资源规格 |
| `/aistudio/v1/studios/{id}/instances` | POST | ✓ 激活 Studio |

### 不可用的 API

| API | 方法 | 原因 |
|-----|------|------|
| `/aiflow/v1/tasks/{id}` | PUT | 405 Method Not Allowed |
| `/aiflow/v1/tasks/{id}/run` | POST | 404 Not Found |
| `/aiflow/v1/tasks/{id}/result` | GET | 404 Not Found |
| `/aiflow/v1/taskruns/{id}` | GET | 404 Not Found |
| 所有触发 API | POST/PUT | 404 Not Found |

## 三、架构差异分析

### BigQuant vs JoinQuant/RiceQuant 核心差异

| 方面 | JoinQuant/RiceQuant | BigQuant |
|------|---------------------|----------|
| **前端** | Jupyter Notebook UI | VS Code Web (code-server) |
| **执行引擎** | Jupyter Kernel | VS Code Extension + BigQuant Backend |
| **通信协议** | Jupyter WebSocket (简单 JSON) | VS Code WebSocket (复杂二进制帧) |
| **运行触发** | HTTP API 或 WebSocket 消息 | 仅 Web UI 按钮 |
| **输出获取** | WebSocket stream 实时推送 | Notebook outputs 字段 (需刷新) |

### 为什么无法直接执行

1. **VS Code Web 协议复杂**: 
   - 使用二进制帧格式，非简单 JSON
   - 需要特定的握手和序列号
   - 是 VS Code 内部协议，未公开文档

2. **任务执行需要 UI 交互**:
   - BigQuant 的 VS Code Extension 处理执行逻辑
   - Extension 仅响应 UI 按钮点击
   - 没有暴露 HTTP API 触发接口

3. **后端调度器设计**:
   - POST /taskruns 创建运行记录
   - 但调度器不自动执行
   - 需要前端 Extension 发送执行信号

## 四、当前限制

### 1. 任务不会自动运行

创建 taskrun 后，任务停留在 `pending` 状态：
```json
{
  "state": "pending",
  "queue": "manual"
}
```

原因: BigQuant 设计为 Web UI 驱动，不是 API 驱动

### 2. 无法获取运行输出

- Notebook `outputs` 字段在 pending 状态下为空
- 无日志 API
- 无结果 API
- WebSocket 是 VS Code 内部协议

## 五、可行的解决方案

### 方案 A: 浏览器自动化 (当前实现)

使用 Playwright:
1. 创建任务 (HTTP API) ✓
2. 打开 Web URL ✓
3. 模拟点击运行按钮 (需要调整)
4. 等待执行完成 ✓
5. 截图保存 ✓

**限制**: 运行按钮位置动态，VS Code 界面复杂

### 方案 B: 半自动化工作流

提供 Web URL，用户手动运行:
1. 创建任务 (API) ✓
2. 返回 Web URL ✓
3. 用户手动运行
4. API 检查状态 ✓

**优点**: 可靠，无需复杂的 UI 自动化

### 方案 C: 官方 API (需联系 BigQuant)

请求 BigQuant 提供:
- POST /tasks/{id}/execute 触发执行
- GET /taskruns/{id}/output 获取输出
- GET /taskruns/{id}/logs 获取日志

## 六、当前实现功能

### 创建任务并获取 Web URL

```bash
node run-strategy.js --strategy ../../strategies/bigquant/pure_cash_defense.py
```

输出：
```
Task ID: b8cd1107-65e9-4795-9623-8430224320ed
Web URL: https://bigquant.com/aistudio/studios/.../?task=...

提示: 任务已创建，请在浏览器中打开 Web URL 运行
```

### 监控任务状态

```bash
node run-and-monitor.js --strategy ../../strategies/bigquant/pure_cash_defense.py
```

会轮询检查任务状态变化。

### 浏览器自动化 (开发中)

```bash
node run-with-browser.js --strategy ../../strategies/bigquant/pure_cash_defense.py
```

当前状态: 可创建任务、打开页面、尝试快捷键，但任务仍停留在 pending

## 七、文件结构

```
bigquant_strategy/
├── request/
│   ├── bigquant-api-client.js      # 基础 HTTP 客户端
│   ├── bigquant-task-client.js     # Task API 客户端
│   └── bigquant-notebook-client.js # Notebook 风格客户端 (已弃用)
│
├── run-strategy.js                 # 创建任务 + 返回 URL
├── run-and-monitor.js              # 创建并监控状态
├── run-with-browser.js             # 浏览器自动化执行 (开发中)
├── activate-and-run.js             # Studio 激活测试
│
├── websocket-test.js               # WebSocket 协议探索
├── vscode-websocket-test.js        # VS Code 协议测试
├── capture-websocket-frames.js     # WebSocket 帧捕获
├── capture-run-requests.js         # 网络请求捕获
│
├── check-task.js                   # 检查任务状态
├── check-all-tasks.js              # 检查所有任务
├── verify-api.js                   # API 验证
├── search-result-apis.js           # 结果 API 搜索
│
└── data/
    ├── session.json                # 登录 Session
    ├── websocket-*.json            # WebSocket 捕获数据
    └── bigquant-api-discovery.json # API 探索记录
```

## 八、结论

**BigQuant 架构与 JoinQuant/RiceQuant 完全不同，无法实现相同的 API 驱动工作流。**

### 技术差异总结

| 项目 | JoinQuant/RiceQuant | BigQuant |
|------|---------------------|----------|
| 是否支持纯 API 执行 | ✓ | ✗ |
| 是否支持 WebSocket 执行 | ✓ (Jupyter 协议) | ✗ (VS Code 内部协议) |
| 是否支持获取输出 | ✓ | ✗ (需 Web UI) |

### 当前可实现功能

- ✓ 创建策略任务
- ✓ 生成 Web URL
- ✓ 监控任务状态 (需手动运行后)
- ✗ 自动运行任务 (无 API)
- ✗ 程序化获取输出 (无 API)

### 推荐方案

**方案 B: 半自动化工作流** (当前最可靠)

1. 使用 API 创建任务
2. 返回 Web URL 给用户
3. 用户在浏览器中手动运行
4. API 监控状态变化
5. 用户在 Web UI 查看结果

这种方式:
- 可靠性高
- 无需复杂的 UI 自动化
- 用户有完整的执行控制
- 符合 BigQuant 的设计意图