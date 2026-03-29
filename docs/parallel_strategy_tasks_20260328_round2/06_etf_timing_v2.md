# 任务 06：ETF 择时 V2（纯 A 池 + 分级仓位）

## 设计文档

### 任务定位

- 类型：ETF 风控修复
- 优先级：高
- 目标：在纯 A ETF 池上重新测试择时，不再使用第一轮失败的“全空/全满”思路

### 第一轮已知结论

- 宽度、BBI、当前 RSRS 在旧 ETF 池上表现很差
- 主要问题是阈值过高、资产池错配、空仓过多
- 第一轮已经明确提出要改成“分级仓位”

### 本轮要回答的问题

1. 纯 A ETF 池下，宽度阈值调低后是否有用？
2. `全空/全满` 改成 `满仓/半仓/空仓` 后，回撤和收益是否更平衡？
3. 修复后的 RSRS 是否还有必要保留？

### 参考材料

- `docs/parallel_strategy_tasks_20260328/03_etf_timing_plugin_verify_result.md`
- `docs/parallel_strategy_tasks_20260328/02_etf_baseline_report.md`
- `聚宽有价值策略558/52 市场宽度——简洁版.ipynb`
- `聚宽有价值策略558/59 研究 【复现】RSRS择时改进.ipynb`
- `聚宽有价值策略558/60 研究 【分享】对RSRS模型的一次修改.ipynb`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 验证择时信号
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 在纯 A ETF 池上做回测
- 必须比较旧逻辑和分级仓位逻辑

### 交付物

1. 一张择时 V2 对比表
2. 一个推荐版本：保留哪个信号、用什么阈值、用几级仓位
3. 一份当前市场仓位建议

### 成功判据

- ETF 择时从“证伪”变成“可再试”
- 如果仍然无效，也要明确给出彻底降级结论

## 子任务提示词

```text
你现在负责 ETF 择时 V2 任务。第一轮已经证明旧版插件几乎都不行，这一轮只允许在“纯 A ETF 池 + 分级仓位”框架里重试。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/03_etf_timing_plugin_verify_result.md
- docs/parallel_strategy_tasks_20260328/02_etf_baseline_report.md
- 聚宽有价值策略558/52 市场宽度——简洁版.ipynb
- 聚宽有价值策略558/59 研究 【复现】RSRS择时改进.ipynb
- 聚宽有价值策略558/60 研究 【分享】对RSRS模型的一次修改.ipynb

强制要求：
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 计算新信号
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 在纯 A ETF 池回测

请完成：
1. 测试宽度阈值 0.25 / 0.30
2. 测试满仓/半仓/空仓分级
3. 修复 RSRS 后重新测试
4. 判断 ETF 择时是否值得重新进入优先级

输出要求：
- 不能再用旧 ETF 池
- 必须比较“二元空仓”与“分级仓位”
- 如果还是无效，明确写 No-Go
```
