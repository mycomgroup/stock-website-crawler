# 聚宽策略批量提交系统

一个用于批量提交和管理聚宽量化策略的自动化工具集。

## 快速开始

### 1. 安装依赖
```bash
cd /Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy
npm install
```

### 2. 配置环境
创建 `.env` 文件：
```env
JOINQUANT_USERNAME=your_username
JOINQUANT_PASSWORD=your_password
```

### 3. 捕获登录会话
```bash
node browser/capture-session.js
```

### 4. 运行工作流

#### 筛选策略
```bash
node select_top_strategies.js
```

#### 批量提交
```bash
# 提交Top100精选策略
node batch_submit_selected.js

# 或全量提交
node batch_submit_jq558_async.js --source-dir ../../jk2bt-main/strategies
```

#### 收集结果
```bash
node collect_jq558_results.js --dir data/jq558_batch_20260404
```

#### 生成报告
```bash
node analyze_all_batches.js
```

## 项目特点

- ✅ 智能策略筛选（基于关键词评分）
- ✅ 批量自动提交（支持断点续传）
- ✅ 自动重试机制（应对平台限制）
- ✅ 详细日志记录（JSONL + Markdown）
- ✅ 回测结果收集
- ✅ 多批次汇总分析

## 三批次提交成果

| 批次 | 日期 | 提交数 | 成功数 | 成功率 |
|------|------|--------|--------|--------|
| 批次1 | 2026-04-03 | 21 | 16 | 76.19% |
| 批次2 | 2026-04-04 | 585 | 211 | 36.07% |
| 批次3 | 2026-04-05 | 100 | 76 | 76.00% |
| **合计** | - | **706** | **303** | **42.92%** |

详细报告：[三批次总结](data/THREE_BATCHES_SUMMARY.md)

## Top10策略（已提交）

1. 窄基ETF轮动：年化82.68%，回撤13.54% (11.5分)
2. 胜率78%，6年36倍，年化50% (11.5分)
3. 年化55.7%，胜率79.9% (11.0分)
4. 小市值年化98%，胜率69% (10.5分)
5. ETF轮动加速10倍版 (10.0分)
6. 多策略整合十年百倍，年化64% (8.5分)
7. 多因子模板分位法，年化65% (8.5分)
8. 研报三因子高分红小市值，年化60% (8.5分)
9. 绩优小市值，模拟年化333.75% (7.5分)
10. 随机森林策略，年化近50% (7.5分)

## 核心脚本

### 策略筛选
- `select_top_strategies.js` - 基于关键词评分筛选策略

### 批量提交
- `batch_submit_jq558_async.js` - 通用批量提交脚本
- `batch_submit_selected.js` - Top100专用提交脚本
- `batch_submit_top100.sh` - Shell包装脚本

### 结果收集
- `collect_jq558_results.js` - 收集回测结果
- `analyze_all_batches.js` - 汇总分析

### 会话管理
- `browser/capture-session.js` - 捕获登录会话
- `request/ensure-session.js` - 确保会话有效

### API客户端
- `request/joinquant-strategy-client.js` - 聚宽API封装

## 数据目录

```
data/
├── jq558_batch_20260403/      # 批次1（21个策略）
├── jq558_batch_20260404/      # 批次2（585个策略）
├── jq558_top100_20260405/     # 批次3（100个Top策略）
├── selected_top100.json       # Top100筛选结果
├── all_batches_summary.json   # 汇总数据
├── all_batches_summary.md     # 汇总报告
└── THREE_BATCHES_SUMMARY.md   # 详细总结
```

每个批次目录包含：
- `submissions.jsonl` - 提交日志
- `submissions.md` - 提交汇总表格
- `state.json` - 实时状态
- `results_snapshot.json` - 回测结果快照

## 策略源文件

策略源文件位于：
```
../../jk2bt-main/strategies/
```

包含489个策略文件（.txt和.py格式）

## 使用示例

### 示例1：提交Top100策略
```bash
# 1. 筛选策略
node select_top_strategies.js

# 2. 查看筛选结果
cat data/selected_top100.json

# 3. 提交策略
node batch_submit_selected.js \
  --reuse-algorithm-id "cd45eba022e60387deb91ee6f725ef50" \
  --sleep 5000

# 4. 查看进度
tail -f data/jq558_top100_*/submissions.md
```

### 示例2：收集回测结果
```bash
# 收集批次2的结果
node collect_jq558_results.js --dir data/jq558_batch_20260404

# 查看结果
cat data/jq558_batch_20260404/results_snapshot.json
```

### 示例3：生成汇总报告
```bash
# 生成报告
node analyze_all_batches.js

# 查看报告
cat data/all_batches_summary.md
```

## 常见问题

### Q: 会话过期怎么办？
A: 重新运行 `node browser/capture-session.js` 捕获新会话

### Q: 遇到平台资源限制？
A: 脚本会自动等待60秒后重试，或者第二天再继续提交

### Q: 如何查看提交进度？
A: 查看 `data/*/state.json` 或 `submissions.md` 文件

### Q: 回测结果在哪里？
A: 运行 `collect_jq558_results.js` 后保存在 `results_snapshot.json`

### Q: 如何重新提交失败的策略？
A: 使用 `--noResume` 参数重新提交，或手动编辑 `submissions.jsonl`

## 技术栈

- Node.js - 脚本运行环境
- Playwright - 浏览器自动化
- 聚宽API - 策略提交和回测

## 项目结构

详细结构说明：[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 相关文档

- [项目结构说明](PROJECT_STRUCTURE.md)
- [三批次总结报告](data/THREE_BATCHES_SUMMARY.md)
- [Top100策略说明](data/TOP100_README.md)
- [汇总分析报告](data/all_batches_summary.md)

## 注意事项

1. **平台限制**
   - 每天回测时间：180分钟
   - 并发回测：最多10个
   - 建议分批提交

2. **会话管理**
   - 会话有效期约24小时
   - 定期更新 `data/session.json`

3. **数据备份**
   - 定期备份 `data/` 目录
   - 提交日志不可恢复

4. **策略源文件**
   - 不要移动 `jk2bt-main/strategies/` 目录
   - 脚本依赖该路径

## 维护

项目位置：
```
/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/
```

最后更新：2026-04-06
