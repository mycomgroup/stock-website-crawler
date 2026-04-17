# Task 32: 分钟上层 API 打通

## 任务目标

解决当前分钟缓存可回放、但上层 `get_price/history/attribute_history/get_bars` 仍返回空数据的问题，让分钟策略真正能消费分钟数据。

## 建议写入目录

- `jqdata_akshare_backtrader_utility/`
- `tests/`
- `docs/0330_result/`

## 负责范围

- 分钟行情上层 API 适配
- 频率参数解析
- 时间窗口与 count/date 行为统一

## 给子 agent 的提示词

你负责打通分钟数据的上层 API。

当前证据表明：
- 缓存回放和分钟周期标准化已有基础
- 但 `get_price_1m/get_price_5m/history_5m/attribute_history_5m/get_bars_5m` 仍然失败或返回空数据

请重点检查：
- `jqdata_akshare_backtrader_utility/market_api.py`
- `jqdata_akshare_backtrader_utility/jq_price_api.py`
- `jqdata_akshare_backtrader_utility/market_data/minute.py`
- 分钟数据与日线数据在 symbol / period / datetime 对齐上的差异

要求：
- 统一 `1m/5m/15m/30m/60m`
- 支持 count 和 date range 两种入口
- 返回结构尽量贴近 JQ 常见语义
- 为空时给出可追踪原因，不要静默空表

## 任务验证

- 补或修测试，覆盖：
  - `get_price(..., frequency='1m'/'5m')`
  - `history(..., unit='5m')`
  - `attribute_history(..., unit='5m')`
  - `get_bars(..., unit='5m')`
- 结果写入 `docs/0330_result/task32_minute_upper_api_closure_result.md`

## 任务成功总结

- 分钟数据不再只停留在缓存层
- 上层 JQ API 能真实消费分钟数据
- 为分钟策略真实运行铺平入口

