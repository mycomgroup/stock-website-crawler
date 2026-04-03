# Task 38: LOF 与 OF 支持

## 任务目标

把多资产里的 LOF 和 OF 从“识别阶段”推进到“最小可用支持阶段”。

## 建议写入目录

- `jqdata_akshare_backtrader_utility/market_data/`
- `jqdata_akshare_backtrader_utility/`
- `tests/`
- `docs/0330_result/`

## 负责范围

- LOF 数据对接
- OF 净值/申赎最小模型
- 资产状态声明修正

## 给子 agent 的提示词

你负责 LOF 与 OF 的最小可用支持。

当前已知问题：
- LOF/OF 现在更多是识别，不是真支持
- 文档与实际能力之间还存在乐观声明风险

请推进：
- LOF 日线与必要分钟数据对接
- OF 净值获取
- OF 最小申赎模拟或至少净值跟踪能力
- 资产路由状态与真实能力一致

要求：
- 先做 MVP，不追求完整套利
- 不能支持的行为要明确报错

## 任务验证

- 增加 LOF 样例和 OF 样例测试
- 至少跑通 2 个 LOF/OF 相关策略或样本脚本
- 输出 `docs/0330_result/task38_lof_of_support_result.md`

## 任务成功总结

- 多资产支持从“只识别”向“可最小运行”推进
- 资产状态声明与真实能力一致

