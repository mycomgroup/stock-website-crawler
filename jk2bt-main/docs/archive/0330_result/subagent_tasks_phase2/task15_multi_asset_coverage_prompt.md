# 任务 15：多资产与期货能力覆盖

## 任务目标

明确并推进股票之外的资产覆盖，优先梳理 ETF、LOF、OF、股指期货策略的真实阻塞点。

## 负责范围

- `jqdata_akshare_backtrader_utility/asset_router.py`
- `jqdata_akshare_backtrader_utility/subportfolios.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 相关多资产策略样本

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task15_multi_asset_coverage_result.md`

## 给子 Agent 的提示词

你负责股票之外资产类型的兼容推进，重点不是“接口存在”，而是“真实策略能不能用”。

要求：

- 盘点 ETF、LOF、OF、股指期货相关策略
- 识别阻塞点：
  - 资产识别
  - 数据获取
  - 交易能力
  - 子账户划分
  - 资金划转
  - 保证金/合约信息
- 先把最小可行路径梳理清楚：
  - 哪些类型已经可跑
  - 哪些类型只能识别，不能交易
  - 哪些类型需要额外数据源
- 形成一份多资产推进路线图

## 任务验证

- 至少选取每类资产 1 到 3 个真实策略样本做验证
- 输出按资产类型拆分的结果报告

## 任务成功总结模板

```md
# Task 15 Result

## 修改文件
- ...

## 完成内容
- ...

## 验证样本
- ...

## 验证方式
- ...

## 已知边界
- ...
```
