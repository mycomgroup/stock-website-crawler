# Task 34: 指数与基本面接口稳健性

## 任务目标

补强 `get_index_stocks`、`get_index_weights`、`get_fundamentals`、`get_history_fundamentals` 这组高频接口，减少“返回 None / 空表导致策略假跑通”的情况。

## 建议写入目录

- `jqdata_akshare_backtrader_utility/`
- `tests/`
- `docs/0330_result/`

## 负责范围

- 指数成分股
- 指数权重
- 基本面查询
- 历史基本面查询

## 给子 agent 的提示词

你负责高频选股数据接口的稳健性。

从现有文档看，多个“假跑通”策略都卡在这组接口：
- `get_index_stocks`
- `get_fundamentals`
- `get_history_fundamentals`

请重点改进：
- 不要轻易返回 `None`
- 空结果时返回稳定结构并带原因
- 对常见指数代码做兼容映射
- 对 query/entity/security 参数风格做统一兼容

优先检查：
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- `jqdata_akshare_backtrader_utility/finance_data/`
- 现有策略验证脚本里的失败样本

## 任务验证

- 选 5 到 10 个依赖指数/基本面的 txt 策略做回归
- 补单测覆盖空结果、断网、缓存命中三种情况
- 输出 `docs/0330_result/task34_index_fundamentals_robustness_result.md`

## 任务成功总结

- 假跑通率下降
- 指数与基本面依赖策略的可运行率提升

