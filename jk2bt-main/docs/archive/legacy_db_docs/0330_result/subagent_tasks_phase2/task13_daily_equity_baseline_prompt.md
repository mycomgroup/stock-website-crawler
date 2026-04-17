# 任务 13：日线股票 ETF 策略基线跑通

## 任务目标

先把“日线股票/ETF 基础策略”做成稳定基线，建立第一批高成功率样本池。

## 负责范围

- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- `jqdata_akshare_backtrader_utility/market_api.py`
- 跑批脚本中与日线策略有关的部分

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - 仓库根目录
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task13_daily_equity_baseline_result.md`

## 给子 Agent 的提示词

你负责把一批日线股票/ETF 策略稳定跑起来，目标是建立“第一批可靠基线策略”。

要求：

- 从现有策略中挑选一批不依赖分钟、期货、文件资源、ML 的纯日线策略
- 跑通并记录：
  - 能成功加载
  - 能完成回测
  - 不出现明显的占位 API 导致的假成功
- 输出一份白名单：
  - 策略文件
  - 运行状态
  - 收益/交易/净值是否正常
- 识别导致失败的共性原因并给出下一步建议

## 任务验证

- 至少跑一批真实 txt 策略样本
- 产出白名单报告
- 白名单中的策略可复跑

## 任务成功总结模板

```md
# Task 13 Result

## 修改文件
- ...

## 完成内容
- ...

## 白名单输出
- ...

## 验证方式
- ...

## 已知边界
- ...
```
