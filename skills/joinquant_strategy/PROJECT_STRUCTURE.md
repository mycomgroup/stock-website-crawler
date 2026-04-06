# 聚宽策略批量提交项目结构说明

## 项目位置
```
/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/
```

## 目录结构

```
skills/joinquant_strategy/
├── README.md                           # 项目主文档
├── PROJECT_STRUCTURE.md                # 本文件：项目结构说明
├── package.json                        # Node.js依赖配置
├── .env                               # 环境变量配置（需自行创建）
│
├── browser/                           # 浏览器自动化相关
│   ├── capture-session.js            # 捕获登录会话
│   └── session-manager.js            # 会话管理
│
├── request/                           # API请求封装
│   ├── ensure-session.js             # 确保会话有效
│   ├── joinquant-strategy-client.js  # 聚宽API客户端
│   └── strategy-runner.js            # 策略运行器
│
├── data/                              # 数据和结果目录
│   ├── session.json                  # 登录会话数据
│   ├── selected_top100.json          # Top100策略筛选结果
│   ├── all_batches_summary.json      # 三批次汇总数据
│   ├── all_batches_summary.md        # 三批次汇总报告
│   ├── THREE_BATCHES_SUMMARY.md      # 三批次详细总结
│   ├── TOP100_README.md              # Top100策略说明
│   │
│   ├── jq558_batch_20260403/         # 批次1数据
│   │   ├── submissions.jsonl         # 提交日志（JSONL格式）
│   │   ├── submissions.md            # 提交汇总（Markdown表格）
│   │   ├── state.json                # 实时状态
│   │   └── results_snapshot.json     # 回测结果快照
│   │
│   ├── jq558_batch_20260404/         # 批次2数据
│   │   ├── submissions.jsonl
│   │   ├── submissions.md
│   │   ├── state.json
│   │   └── results_snapshot.json
│   │
│   └── jq558_top100_20260405/        # 批次3数据（Top100）
│       ├── submissions.jsonl
│       ├── submissions.md
│       ├── state.json
│       └── results_snapshot.json
│
├── 核心脚本/
│   ├── select_top_strategies.js      # 策略筛选脚本
│   ├── batch_submit_jq558_async.js   # 通用批量提交脚本
│   ├── batch_submit_selected.js      # Top100批量提交脚本
│   ├── batch_submit_top100.sh        # Shell包装脚本
│   ├── collect_jq558_results.js      # 收集回测结果
│   └── analyze_all_batches.js        # 汇总分析脚本
│
└── 其他策略文件/                      # 各种测试策略（Python）
    ├── rfscore*.py
    ├── weak_to_strong*.py
    ├── sentiment*.py
    └── ...
```

## 外部依赖

### 策略源文件位置
```
../../jk2bt-main/strategies/
```
包含489个策略文件（.txt和.py格式）

### 关系说明
- 提交脚本从 `jk2bt-main/strategies/` 读取策略源文件
- 提交记录和结果保存在 `skills/joinquant_strategy/data/`
- 所有代码和工具都在 `skills/joinquant_strategy/` 目录下

## 核心工作流程

### 1. 策略筛选
```bash
node select_top_strategies.js
```
- 输入：`../../jk2bt-main/strategies/` 下的所有策略文件
- 输出：`data/selected_top100.json`

### 2. 批量提交
```bash
# 方式1：提交Top100
node batch_submit_selected.js

# 方式2：全量提交
node batch_submit_jq558_async.js --source-dir ../../jk2bt-main/strategies

# 方式3：使用Shell脚本
./batch_submit_top100.sh
```

### 3. 收集结果
```bash
# 收集指定批次的回测结果
node collect_jq558_results.js --dir data/jq558_batch_20260404
```

### 4. 汇总分析
```bash
# 生成三批次汇总报告
node analyze_all_batches.js
```

## 配置文件

### .env
需要在项目根目录创建 `.env` 文件：
```env
JOINQUANT_USERNAME=your_username
JOINQUANT_PASSWORD=your_password
```

### session.json
登录会话数据，由 `browser/capture-session.js` 自动生成

## 数据文件说明

### submissions.jsonl
每行一个JSON对象，记录每个策略的提交信息：
```json
{
  "index": 1,
  "file": "strategies/01 策略名.txt",
  "strategyName": "JQ558_0001_策略名",
  "algorithmId": "xxx",
  "backtestId": "xxx",
  "status": "submitted",
  "submittedAt": "2026-04-05T..."
}
```

### submissions.md
Markdown表格格式的提交汇总

### state.json
实时状态信息：
```json
{
  "updatedAt": "2026-04-05T...",
  "totalFiles": 489,
  "alreadySubmitted": 100,
  "successCount": 80,
  "failCount": 20
}
```

### results_snapshot.json
回测结果快照：
```json
{
  "generatedAt": "2026-04-05T...",
  "totals": {
    "submitted": 100,
    "completed": 50,
    "pending": 50
  },
  "completed": [
    {
      "file": "...",
      "summary": {
        "total_returns": 0.5,
        "annualized_returns": 0.3,
        "sharpe": 1.5,
        "max_drawdown": -0.2
      }
    }
  ]
}
```

## 三批次提交总结

### 批次1: jq558_batch_20260403
- 日期: 2026-04-03
- 提交: 21个
- 成功: 16个（76.19%）
- 目的: 初次测试

### 批次2: jq558_batch_20260404
- 日期: 2026-04-04
- 提交: 585个
- 成功: 211个（36.07%）
- 目的: 全量提交

### 批次3: jq558_top100_20260405
- 日期: 2026-04-05
- 提交: 100个（计划）
- 成功: 76个（76.00%）
- 目的: 精选高潜力策略

### 总计
- 总提交: 706个
- 成功: 303个（42.92%）
- 失败: 403个（57.08%）

## 常用命令

### 查看提交进度
```bash
# 查看某批次的提交数量
wc -l data/jq558_batch_20260404/submissions.jsonl

# 查看成功提交数量
grep '"status":"submitted"' data/jq558_batch_20260404/submissions.jsonl | wc -l

# 查看失败数量
grep '"status":"failed"' data/jq558_batch_20260404/submissions.jsonl | wc -l
```

### 查看回测结果
```bash
# 查看已完成的回测数量
cat data/jq558_batch_20260404/results_snapshot.json | grep -o '"completed"' | wc -l

# 查看待完成的回测数量
cat data/jq558_batch_20260404/results_snapshot.json | grep -o '"pending"' | wc -l
```

### 重新生成报告
```bash
# 重新生成汇总报告
node analyze_all_batches.js

# 查看报告
cat data/THREE_BATCHES_SUMMARY.md
```

## 注意事项

1. **策略源文件位置**
   - 策略源文件在 `../../jk2bt-main/strategies/`
   - 不要移动或删除这些文件
   - 提交脚本会自动读取

2. **会话管理**
   - 会话数据保存在 `data/session.json`
   - 会话过期需要重新登录
   - 使用 `browser/capture-session.js` 重新捕获

3. **平台限制**
   - 每天回测时间限制: 180分钟
   - 并发回测限制: 最多10个
   - 遇到限制会自动等待重试

4. **数据备份**
   - 定期备份 `data/` 目录
   - 提交日志（.jsonl）不可恢复
   - 回测结果可以重新收集

## 相关文档

- [三批次总结报告](data/THREE_BATCHES_SUMMARY.md)
- [Top100策略说明](data/TOP100_README.md)
- [汇总分析报告](data/all_batches_summary.md)

## 维护者

项目位置: `/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/`
