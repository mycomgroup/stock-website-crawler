# BigQuant Skill 使用指南

## 状态：已完成

BigQuant skill 已创建完成，支持通过 HTTP API 创建和运行策略。

**已完成的功能：**
- ✓ 核心 API 客户端 (request/bigquant-api-client.js)
- ✓ Notebook 客户端 (request/bigquant-notebook-client.js)
- ✓ 策略运行器 (run-backtest-api.js)
- ✓ Task 管理 (create-taskrun.js, check-task.js)
- ✓ 完整测试套件

## 架构说明

BigQuant 使用任务(Task)驱动的策略执行方式：

```
策略代码 -> 创建Task -> 创建TaskRun -> 调度执行 -> 获取结果
```

关键 API 端点：
- `POST /bigapis/aiflow/v1/tasks` - 创建任务
- `POST /bigapis/aiflow/v1/taskruns` - 创建任务运行
- `GET /bigapis/aiflow/v1/tasks/{id}` - 获取任务状态
- `GET /bigapis/aiflow/v1/tasks/{id}/result` - 获取运行结果

## 快速使用

### 1. 配置账号

Session 已保存在 `data/session.json`，包含登录后的 cookies。

### 2. 运行策略

```bash
# 使用默认测试策略
node run-backtest-api.js

# 运行指定策略文件
node run-backtest-api.js --strategy ../../strategies/bigquant/pure_cash_defense.py

# 自定义参数
node run-backtest-api.js --strategy my_strategy.py \
  --start-date 2022-01-01 \
  --end-date 2023-12-31 \
  --capital 500000
```

### 3. 检查任务状态

```bash
node check-task.js
```

### 4. 查看资源状态

```bash
node check-resources.js
```

## 文件结构

```
skills/bigquant_strategy/
├── .env                      环境变量配置
├── paths.js                  路径配置
├── load-env.js               环境变量加载
├── package.json              依赖配置
│
├── request/
│   ├── bigquant-api-client.js      HTTP API 客户端
│   └── bigquant-notebook-client.js Notebook 风格客户端
│
├── browser/
│   └── session-manager.js          Session 管理
│
├── run-backtest-api.js       策略运行器
├── check-task.js             检查任务状态
├── check-resources.js        检查资源状态
├── create-taskrun.js         创建任务运行
│
├── test-api.js               API 测试
├── test-notebook.js          Notebook 测试
│
└── data/
    └── session.json          登录 Session
```

## API 客户端

### BigQuantAPIClient

基础 HTTP API 客户端：

```javascript
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

const client = new BigQuantAPIClient();

// 用户信息
const user = await client.getCurrentUser();

// Studio 信息
const studio = await client.getDefaultStudio();

// 任务管理
const tasks = await client.listTasks({ size: 10 });
const task = await client.getTask(taskId);
const result = await client.createTask(taskData);
```

### BigQuantNotebookClient

Notebook 风格客户端，支持类似 Jupyter 的代码执行：

```javascript
import { BigQuantNotebookClient } from './request/bigquant-notebook-client.js';

const client = new BigQuantNotebookClient({ studioId });

// 运行回测
const result = await client.runBacktest(code, {
  name: 'my_strategy',
  startDate: '2023-01-01',
  endDate: '2023-12-31',
  capital: 100000
});

console.log('Task ID:', result.taskId);
console.log('Web URL:', result.webUrl);
```

## 注意事项

1. **任务执行**：BigQuant 的任务调度器可能需要从 Web 界面触发执行
2. **Session 有效期**：约 7 天，过期需要重新登录
3. **资源限制**：免费用户有资源规格限制

## 工作流程

1. 创建任务（包含 Jupyter Notebook JSON 格式的代码）
2. 创建 TaskRun 触发执行
3. 通过 Web URL 查看运行结果
4. 或使用 API 轮询获取结果

## 转换的策略

已转换的策略位于 `../../strategies/bigquant/`：

- `pure_cash_defense.py` - 纯现金防守策略
- `smallcap_quality_defense.py` - 小盘质量防守策略
- `rfscore7_base_800.py` - RF评分基础策略
- `rfscore7_pb10_final_v2.py` - RF评分优化策略
- 等等...

运行转换的策略：

```bash
node run-backtest-api.js --strategy ../../strategies/bigquant/rfscore7_base_800.py
```

---

**状态总结：API 客户端已完成，可以创建任务并通过 Web 界面运行。**