# 任务 01：小市值市值区间分层基线研究

## 设计文档

### 任务定位

- 聚焦方向：`小市值因子基础研究`
- 目标：确定小市值因子是否存在"最优收益/风险区间"，而非单向"越小越好"

### 当前已知问题

- 小市值策略常被笼统定义为"买最小的票"，但缺乏对市值区间的精细分层验证
- 不清楚是否在某个市值区间存在收益/回撤/可交易性的最优平衡点
- 极小微盘可能存在流动性、退市、壳价值等不可交易风险

### 参考材料

- `docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md`
- `strategies/shadow_strategies_20260330/backtest_10years.ipynb`
- `聚宽有价值策略558/` 目录下的小市值策略

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 进行分层回测
- 必须覆盖 2018-01-01 至 2025-03-30 全样本期
- 必须做年度切片分析（2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025）

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_01_smallcap_market_cap_stratification.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 五档市值分层的收益/回撤/夏普/换手对比表
2. 年度切片稳定性分析
3. 最优市值区间推荐（附可交易性评估）

## 子任务提示词

```text
你现在负责小市值研究的第一个基础任务：市值区间分层基线研究。

请优先阅读：
- docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md
- strategies/shadow_strategies_20260330/backtest_10years.ipynb
- 聚宽有价值策略558/ 目录下的小市值策略

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 跑分层回测
- 必须覆盖 2018-01-01 至 2025-03-30
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_01_smallcap_market_cap_stratification.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：
1. 按"流通市值"分层为 5-15亿、15-30亿、30-60亿、60-100亿、100-200亿 五组
2. 每组做纯等权买入持有回测，月度调仓
3. 对比五组的：年化收益、最大回撤、夏普比率、换手率、平均成交额
4. 按年度切片（2018-2025），看各组的稳定性
5. 给出"最优市值区间"推荐

基础过滤：
- 非 ST/*ST
- 非停牌
- 上市 > 180 天
- PB > 0
- 剔除科创板（可选，单独说明）

输出要求：
- 必须有一张五组对比表（收益/回撤/夏普/换手/成交额）
- 必须说明是否存在"收益/可交易性"最优平衡区间
- 如果某组回测中出现大量无法成交的样本，必须单独标注
```
