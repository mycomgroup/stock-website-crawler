# 任务 05：纯 A 股 ETF 池重建

## 设计文档

### 任务定位

- 类型：ETF 线重构
- 优先级：高
- 目标：解决第一轮 ETF 择时失败的根本问题之一：池子混了跨市场资产

### 第一轮已知结论

- ETF 基线本身还能用
- 择时插件几乎全失败
- 失败的关键原因之一是 ETF 池混入了纳指、标普、黄金、国债等跨市场资产

### 本轮要回答的问题

1. 如果只保留 A 股内部宽基/行业 ETF，ETF 基线是否会更干净？
2. 候选池是否应该拆成 `宽基池` 与 `行业池` 两套版本？
3. 纯 A ETF 池是否更适合后续择时与行业增强？

### 参考材料

- `docs/parallel_strategy_tasks_20260328/02_etf_baseline_report.md`
- `docs/parallel_strategy_tasks_20260328/03_etf_timing_plugin_verify_result.md`
- `聚宽有价值策略558/66 手把手教你构建ETF策略候选池.ipynb`
- `聚宽有价值策略558/86 手把手教你构建ETF策略候选池优化版.ipynb`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 重建 ETF 候选池
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 做新池回测
- 必须输出旧池 vs 新池的对比结果

### 交付物

1. 一份纯 A 宽基 ETF 池
2. 一份纯 A 行业 ETF 池
3. 一张旧池 vs 新池基线对比表

### 成功判据

- ETF 线从“混杂资产集合”变成“可继续优化的中国市场内生策略”

## 子任务提示词

```text
你现在负责重建 ETF 候选池，目标是把第一轮混杂的跨市场 ETF 池拆干净。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/02_etf_baseline_report.md
- docs/parallel_strategy_tasks_20260328/03_etf_timing_plugin_verify_result.md
- 聚宽有价值策略558/66 手把手教你构建ETF策略候选池.ipynb
- 聚宽有价值策略558/86 手把手教你构建ETF策略候选池优化版.ipynb

强制要求：
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 构建新池
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做旧池 vs 新池回测

请完成：
1. 给出纯 A 宽基池
2. 给出纯 A 行业池
3. 重新做 ETF 动量基线回测

输出要求：
- 必须写清为什么删掉跨市场 ETF
- 必须保留候选池筛选理由
- 必须给一个推荐的“ETF 池正式版本”
```
