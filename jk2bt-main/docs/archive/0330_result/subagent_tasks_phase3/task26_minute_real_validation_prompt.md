# 任务 26：分钟数据真实验证

## 任务目标

把分钟数据能力从“接口存在”推进到“真实可调用、真实可缓存、真实可被策略消费”。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/minute.py`
- `jqdata_akshare_backtrader_utility/market_api.py`
- 分钟数据相关 smoke/test 脚本

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/market_data/`
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task26_minute_real_validation_result.md`

## 给子 Agent 的提示词

你负责把分钟数据从“理论能力”推进到“真实验证能力”。

要求：

- 选股票和 ETF 各若干样本
- 验证：
  - 数据能取到
  - 数据能写缓存
  - 上层 `get_price/get_bars/history/attribute_history` 能消费
- 若当前环境下网络不可用，也要尽量做缓存回放验证
- 结果文档里必须明确区分：
  - 已真实验证通过
  - 仅接口存在
  - 明确还不支持

## 任务验证

- 至少验证 `1m/5m/15m/30m/60m` 中的主要周期
- 至少做一次缓存回放验证

## 任务成功总结模板

```md
# Task 26 Result

## 修改文件
- ...

## 验证通过项
- ...

## 未通过项
- ...

## 验证方式
- ...

## 已知边界
- ...
```
