# 任务 18：批量运行结果真值化

## 任务目标

让批量运行结果真正可信，不只是“跑完有个 summary.json”，而是能回答“为什么成功、为什么失败、失败能否自动归因”。

## 负责范围

- `run_strategies_parallel.py`
- `jqdata_akshare_backtrader_utility/strategy_scanner.py`
- `logs/strategy_runs/` 输出格式相关代码

## 建议写入目录

- 代码写入：
  - 仓库根目录
  - `jqdata_akshare_backtrader_utility/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task18_batch_runner_truth_result.md`

## 给子 Agent 的提示词

你负责批量运行结果的真值化和归因质量。

要求：

- 改进运行状态分类，避免“伪成功”
- 输出更可信的结果字段：
  - 加载是否成功
  - 是否进入回测循环
  - 是否有交易
  - 是否有净值序列
  - 是否因缺失 API 失败
  - 是否因依赖缺失失败
  - 是否因资源文件缺失失败
- 让 `summary.json` 和明细日志可交叉验证
- 最终能清楚回答：哪些策略值得继续补，哪些应暂时跳过

## 任务验证

- 用一小批真实策略样本做回归
- 样本里至少有：
  - 真成功
  - 真失败
  - 依赖缺失
  - 缺失 API
  - 数据缺失

## 任务成功总结模板

```md
# Task 18 Result

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
