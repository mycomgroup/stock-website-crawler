# 小市值状态路由双引擎研究方案

## 用途

这个文件是小市值研究线的统一汇总页。

从这一轮开始，所有子任务都必须遵守下面两条：

1. 结果文档必须写回本目录：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
2. 每个任务跑完后，必须同步更新本文件对应条目，至少补齐：
   - `状态`
   - `结果文件`
   - `一句话结论`
   - `是否进入正式版本`

## 研究总目标

**不是证明"越小越好"，而是建立一个可执行、可监控、可衰减追踪的小市值研究框架。**

### 核心假设

1. 小市值因子存在"最优区间"，而非单向有效
2. 小市值真正可交易的 alpha 来自"状态 + 因子/事件"的组合
3. 状态路由比静态持有更重要

### 双引擎架构

- **防守线**：小市值 + 质量/红利/低估值中频轮动，解决回撤和空窗期问题
- **进攻线**：首板低开 + 二板接力短线事件驱动，解决收益弹性问题
- **状态路由器**：市场广度 + 情绪指标，决定开关、仓位、策略启停

## 结果命名约定

| 任务 | 建议结果文件 |
|------|--------------|
| 01 | `result_01_smallcap_market_cap_stratification.md` |
| 02 | `result_02_smallcap_state_stratification.md` |
| 03 | `result_03_firstboard_low_open_oos_2025.md` |
| 04 | `result_04_secondboard_cross_cycle_validation.md` |
| 05 | `result_05_smallcap_defense_v1_design.md` |
| 06 | `result_06_state_router_v1_design.md` |
| 07 | `result_07_sentiment_threshold_optimization.md` |
| 08 | `result_08_smallcap_event_capacity_slippage.md` |
| 09 | `result_09_defense_offense_combination.md` |
| 10 | `result_10_smallcap_factor_vs_event_attribution.md` |

## 任务总表

### 01 小市值市值区间分层基线研究

- 状态：⏳ 待执行
- 结果文件：`result_01_smallcap_market_cap_stratification.md`
- 一句话结论：(待填写)
- 是否进入正式版本：(待填写)

### 02 小市值状态分层基线研究

- 状态：⏳ 待执行
- 结果文件：`result_02_smallcap_state_stratification.md`
- 一句话结论：(待填写)
- 是否进入正式版本：(待填写)

### 03 首板低开最新 OOS 验证

- 状态：⏳ 待执行
- 结果文件：`result_03_firstboard_low_open_oos_2025.md`
- 一句话结论：(待填写)
- 是否进入正式版本：(待填写)

### 04 二板接力跨周期验证

- 状态：✅ 已完成
- 结果文件：`result_04_secondboard_cross_cycle_validation.md`
- 一句话结论：跨周期稳定，所有年度正收益，建议纳入进攻线（占30-40%仓位）
- 是否进入正式版本：✅ 纳入进攻线

### 05 小市值防守线 v1 设计

- 状态：⏳ 待执行
- 结果文件：`result_05_smallcap_defense_v1_design.md`
- 一句话结论：(待填写)
- 是否进入正式版本：(待填写)

### 06 状态路由器 v1 设计

- 状态：⏳ 待执行
- 结果文件：`result_06_state_router_v1_design.md`
- 一句话结论：(待填写)
- 是否进入正式版本：(待填写)

### 07 情绪指标精细化阈值搜索

- 状态：⏳ 待执行
- 结果文件：`result_07_sentiment_threshold_optimization.md`
- 一句话结论：(待填写)
- 是否进入正式版本：(待填写)

### 08 小市值事件策略容量与滑点测试

- 状态：⏳ 待执行
- 结果文件：`result_08_smallcap_event_capacity_slippage.md`
- 一句话结论：(待填写)
- 是否进入正式版本：(待填写)

### 09 防守线与进攻线组合测试

- 状态：⏳ 待执行
- 结果文件：`result_09_defense_offense_combination.md`
- 一句话结论：(待填写)
- 是否进入正式版本：(待填写)

### 10 小市值因子 vs 事件策略归因分析

- 状态：⏳ 待执行
- 结果文件：`result_10_smallcap_factor_vs_event_attribution.md`
- 一句话结论：(待填写)
- 是否进入正式版本：(待填写)

## 关键约束

### 数据与工具

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook`
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy`

### 验证标准

- 必须做 IS/OOS 分段
- 必须做滚动窗口
- 必须做年度切片
- 必须做牛/熊/震荡分层
- 必须做参数扰动

### 一票否决项

- 收益高度集中于单一年份
- 真实滑点后失效
- 参数轻微变化就崩
- 极度依赖极少数个股/题材
- OOS 显著偏离 IS

## 最终目标

建立一个可以回答以下问题的研究结论树：

1. 小市值哪个区间最值得做？
2. 小市值在什么市场状态下能做？
3. 小市值防守线是否可独立成立？
4. 小市值短线线是否仍有 OOS alpha？
5. 两者能否通过状态路由组合，而不是静态拼盘？
