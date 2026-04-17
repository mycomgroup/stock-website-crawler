# Task 35: 长尾缺失 API 收口

## 任务目标

基于扫描结果，把最常见且最影响真实策略运行的长尾缺失 API 再收口一批。

## 建议写入目录

- `jqdata_akshare_backtrader_utility/`
- `docs/0330_result/`
- `tests/`

## 负责范围

- 非核心但高频出现的缺失 API
- 以“让更多 txt 真能跑”为目标，而不是追求接口大全

## 给子 agent 的提示词

你负责长尾缺失 API 收口。

请从策略扫描结果和失败日志中重新排序最值得补的一批 API。优先选择：
- 出现频率高
- 实现成本中等
- 一旦补上就能直接增加可运行策略数

候选包括但不限于：
- `get_ticks`
- `get_mtss`
- `get_margincash_stocks`
- `get_industry_stocks`
- `get_concept_stocks`
- `get_locked_shares`

要求：
- 每个 API 都给出支持级别：真实实现 / 部分实现 / stub + 显式告警
- 不允许静默返回误导性空结果

## 任务验证

- 对每个新增 API 至少补 1 个测试
- 对 10 个此前因缺失 API 失败的策略重新抽检
- 输出 `docs/0330_result/task35_missing_api_longtail_result.md`

## 任务成功总结

- 长尾缺口更少
- 跑批中的 `missing_api` 分类显著下降

