# 任务 09：状态路由器 V2 + 真实切换回测

## 设计文档

### 任务定位

- 类型：顶层状态机
- 优先级：高
- 目标：把第一轮“状态判断”推进到“状态切换真的有用吗”

### 第一轮已知结论

- 当前状态是“底部试错”
- 路由器思路是对的，但 RSRS 趋势信号存在技术问题
- 还没有完成“按状态切换策略后的正式回测”

### 本轮要回答的问题

1. 修复趋势信号后，状态机能否稳定运行？
2. `RFScore / 红利小盘 / ETF / 防守底仓` 按状态切换，是否优于静态配置？
3. 路由器是否值得进入正式执行层？

### 参考材料

- `docs/parallel_strategy_tasks_20260328/11_macro_regime_router_validation.md`
- `docs/parallel_strategy_tasks_20260328/首批实跑组合验证报告_2026-03-28.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 修复并计算状态指标
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 做“状态切换组合”回测
- 不能只输出状态定义，必须输出切换效果

### 交付物

1. 一份状态机 V2 定义
2. 一份静态组合 vs 状态切换组合对比
3. 一个结论：状态机是否应该接入执行系统

### 成功判据

- 路由器从“理解市场”升级成“帮助赚钱或控回撤”

## 子任务提示词

```text
你现在负责状态路由器 V2。第一轮只做出了“当前状态是什么”，这一轮必须验证“按状态切换策略是否真的有用”。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/11_macro_regime_router_validation.md
- docs/parallel_strategy_tasks_20260328/首批实跑组合验证报告_2026-03-28.md

强制要求：
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 修复趋势信号并计算状态
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做状态切换回测

请完成：
1. 修复趋势信号
2. 定义状态机 V2
3. 比较静态配置 vs 状态切换配置

输出要求：
- 必须回答状态机有没有实际增益
- 如果没有增益，就把它降级为“解释层”
- 必须给出当前状态下的具体仓位建议
```
