# Notebook 自动关闭 Session 功能

## 功能说明

执行策略代码后，自动关闭运行中的 session，释放资源。避免在浏览器中手动操作。

**重要：关闭 session，不关闭 kernel**
- Session 是前端连接到 kernel 的概念
- Kernel 可能被多个 notebook 共享
- 关闭 session 不影响其他正在运行的 notebook

## 使用方法

### 默认行为（自动关闭）

```bash
# 执行后自动关闭 session（默认）
node run-strategy.js --strategy examples/simple_backtest.py
```

### 禁用自动关闭

```bash
# 保持 session 运行（用于调试）
node run-strategy.js --strategy examples/simple_backtest.py --no-shutdown

# 或显式指定
node run-strategy.js --strategy examples/simple_backtest.py --auto-shutdown false
```

## 执行流程

```
1. 执行代码 ✓
2. 保存 notebook ✓  ← 确保数据安全
3. 获取 metadata ✓
4. 关闭 session ✓    ← 释放资源（新增）
```

**执行顺序保证数据安全：**
- 先保存 notebook，确保执行结果不丢失
- 再关闭 session，释放服务器资源

## API 接口

### 新增方法（RiceQuantNotebookClient）

```javascript
// 获取所有运行中的 sessions
const sessions = await client.listSessions();
// 返回: [{ id, path, kernel: { id, name }, ... }]

// 删除指定 session
const result = await client.deleteSession(sessionId);
// 返回: { success: true, sessionId } 或 { success: false, error }
```

### REST API

```
GET  /api/sessions              - 获取所有活跃 sessions
DELETE /api/sessions/{session_id} - 删除指定 session
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--auto-shutdown` | true | 执行后自动关闭 session |
| `--no-shutdown` | false | 禁用自动关闭（调试模式） |

## 结果文件新增字段

```json
{
  "shutdownResult": {
    "success": true,
    "sessionId": "abc123-def456..."
  },
  "autoShutdown": true
}
```

## 错误处理

- 关闭失败不影响结果保存
- 错误记录到 `shutdownResult` 字段
- Session 会自动超时释放（不重试）

## 常见场景

### 场景 1：批量执行多个策略

```bash
# 连续执行多个策略，自动关闭避免资源堆积
node run-strategy.js --strategy strategy1.py
node run-strategy.js --strategy strategy2.py
node run-strategy.js --strategy strategy3.py
```

### 场景 2：调试单个策略

```bash
# 禁用自动关闭，保持 session 便于查看运行状态
node run-strategy.js --strategy test.py --no-shutdown

# 手动查看 https://www.ricequant.com/research
# 找到 "运行中" 查看状态

# 完成后手动关闭或等待自动超时
```

### 场景 3：创建独立 notebook 并自动清理

```bash
# 创建新 notebook，运行后关闭 session
node run-strategy.js --strategy test.py --create-new

# 创建临时 notebook，运行后删除 notebook 并关闭 session
node run-strategy.js --strategy test.py --create-new --cleanup
```

### 场景 4：关闭所有运行中的 notebook

如需批量关闭所有 session，可调用：

```javascript
const sessions = await client.listSessions();
for (const session of sessions) {
  await client.deleteSession(session.id);
}
```

## 技术细节

### Session vs Kernel

| 对象 | 说明 | 关闭影响 |
|------|------|---------|
| Kernel | 执行环境 | 关闭会影响所有使用它的 session |
| Session | 前端连接 | 只关闭当前连接，不影响 kernel |

**设计决策：关闭 session**
- 同一个 kernel 可能被多个 notebook 共享
- 关闭 kernel 会影响其他正在运行的 notebook
- 关闭 session 更安全，只释放当前连接

### Jupyter REST API 规范

RiceQuant 使用 Jupyter Notebook 架构，API 符合标准：

- `DELETE /api/sessions/{session_id}` 返回 204 No Content
- `DELETE /api/kernels/{kernel_id}` 也会关闭关联的 session

## 与 JoinQuant 的对比

| 特性 | RiceQuant | JoinQuant |
|------|-----------|-----------|
| API 架构 | Jupyter Notebook | JupyterHub + Jupyter |
| Session 管理 | 相同 | 相同 |
| 自动关闭实现 | 相同 | 相同 |
| 参数名称 | `--no-shutdown` | `--no-shutdown` |

## 相关文档

- 快速参考：[QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- 主要文档：[README.md](README.md)