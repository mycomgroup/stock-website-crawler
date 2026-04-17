# 任务 27：分钟回放引擎与日内触发语义

## 任务目标

补齐分钟策略真正落地所需的回放引擎与触发语义，不再只停留在时间规则解析层。

## 负责范围

- `jqdata_akshare_backtrader_utility/timer_rules.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
- 分钟回放相关测试或脚本

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task27_minute_replay_engine_result.md`

## 给子 Agent 的提示词

你负责分钟回放引擎和日内触发语义。

要求：

- 补齐或明确实现：
  - 分钟级回放
  - `every_bar`
  - `open+Nm`
  - `HH:MM`
  - 尾盘/盘中触发
- 优先让真实日内策略能进入回测循环并按分钟触发
- 如果某些语义当前做不到，必须在结果里明确写“未支持”，不要模糊表述

## 任务验证

- 至少选 2 到 5 个真实分钟策略样本
- 验证它们能否进入分钟回放、是否触发预期回调

## 任务成功总结模板

```md
# Task 27 Result

## 修改文件
- ...

## 支持的语义
- ...

## 未支持的语义
- ...

## 验证样本
- ...

## 已知边界
- ...
```
