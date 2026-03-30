# RiceQuant Notebook 功能改进说明

## 改进内容

### 1. 创建独立 Notebook（`--create-new`）

**问题**：之前所有策略都在同一个 notebook 中运行，容易造成混乱。

**解决方案**：
- 添加 `createNotebook()` API 创建新的独立 notebook
- Notebook 名称格式：`strategy_run_<timestamp>_<random>.ipynb`
- 每次运行都是全新的环境

**使用方式**：
```bash
# 创建新的独立 notebook 并运行
node run-strategy.js --strategy examples/simple_backtest.py --create-new

# 指定基础名称
node run-strategy.js --strategy your_strategy.py --create-new --notebook-base-name "my_test"
```

### 2. 自动清理 Notebook（`--cleanup`）

**问题**：运行大量测试后会留下很多临时 notebook，需要手动清理。

**解决方案**：
- 添加 `deleteNotebook()` API 删除 notebook
- 配合 `--create-new` 使用，运行完成后自动删除
- 保留执行结果快照到本地

**使用方式**：
```bash
# 创建临时 notebook，运行后自动删除
node run-strategy.js --strategy examples/simple_backtest.py --create-new --cleanup
```

### 3. 功能验证测试

**新增测试脚本**：`test-functionality.js`

**测试内容**：
1. 基础连接测试 - 验证 API 连接
2. 创建独立 notebook 测试 - 验证 `--create-new` 功能
3. 自动清理测试 - 验证 `--cleanup` 功能

**运行测试**：
```bash
node test-functionality.js
# 或
npm test
```

## 使用场景

### 场景 1：快速验证策略逻辑

```bash
# 使用默认 notebook，快速测试
node run-strategy.js --cell-source "print(get_all_securities(['stock']).head())"
```

### 场景 2：策略开发调试

```bash
# 创建独立 notebook，保留调试记录
node run-strategy.js --strategy my_strategy.py --create-new
```

### 场景 3：批量测试

```bash
# 创建临时 notebook，运行后自动清理
for strategy in examples/*.py; do
  node run-strategy.js --strategy $strategy --create-new --cleanup
done
```

## 新增 API

### RiceQuantNotebookClient 新增方法

#### createNotebook(options)
创建新的 notebook

```javascript
const result = await client.createNotebook({
  notebookPath: 'my_notebook.ipynb',
  kernelName: 'python3'
});
// 返回：{ notebookPath, notebookUrl, ... }
```

#### deleteNotebook(options)
删除 notebook

```javascript
const result = await client.deleteNotebook({
  notebookPath: 'my_notebook.ipynb'
});
// 返回：{ success: true/false, notebookPath, error? }
```

#### generateUniqueNotebookName(baseName)
生成唯一的 notebook 名称

```javascript
const name = client.generateUniqueNotebookName('test_run');
// 返回：'test_run_1234567890_abc12.ipynb'
```

## 输出文件

所有运行结果都会保存到本地：

```
data/
├── ricequant-notebook-<timestamp>.ipynb      # Notebook 快照
├── ricequant-notebook-result-<timestamp>.json # 执行结果
└── session.json                               # Session 数据
```

即使使用了 `--cleanup` 删除远程 notebook，本地快照仍会保留。

## 参数对照表

| 参数 | 说明 | 推荐使用场景 |
|------|------|------------|
| 无参数 | 使用现有 notebook | 日常开发、调试 |
| `--create-new` | 创建独立 notebook | 验证新策略、保留记录 |
| `--create-new --cleanup` | 创建临时 notebook | 批量测试、CI/CD |

## 最佳实践

1. **开发阶段**：使用默认模式，快速迭代
2. **验证阶段**：使用 `--create-new`，保留验证记录
3. **测试阶段**：使用 `--create-new --cleanup`，避免污染环境

## 故障排查

### 创建 notebook 失败

**错误**：`Failed to create new notebook`

**原因**：
- 权限不足
- 磁盘空间不足
- Notebook 数量超限

**解决**：使用默认模式或清理旧 notebook

### 清理 notebook 失败

**错误**：`Failed to cleanup notebook`

**原因**：
- Notebook 正在被使用
- 权限问题

**解决**：手动删除或忽略（不影响结果）

## 示例代码

### Node.js 程序化调用

```javascript
import { runNotebookTest } from './request/test-ricequant-notebook.js';

// 创建临时 notebook 并运行
const result = await runNotebookTest({
  cellSource: 'print("hello")',
  createNew: true,
  cleanup: true,
  timeoutMs: 30000
});

console.log('执行结果:', result.executions[0].textOutput);
console.log('Notebook 已清理:', result.cleanupResult.success);
```

### 批量测试脚本

```javascript
import { runNotebookTest } from './request/test-ricequant-notebook.js';

const strategies = [
  'ma_strategy_notebook.py',
  'rfscore_simple_notebook.py'
];

for (const strategy of strategies) {
  console.log(`Testing ${strategy}...`);
  await runNotebookTest({
    strategy: `examples/${strategy}`,
    createNew: true,
    cleanup: true
  });
}
```