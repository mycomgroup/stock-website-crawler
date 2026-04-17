# 任务 4：分钟级数据后端

## 任务目标

补充股票和 ETF 的分钟级数据后端，为日内策略提供统一数据基础。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/`
- 与分钟数据获取直接相关的测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/market_data/`
  - `tests/`
- 任务结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task04_minute_data_result.md`

## 给子 Agent 的提示词

你负责实现股票和 ETF 的分钟级数据后端，请直接开发，不要只做调研。

具体要求：

- 支持至少：
  - `1m`
  - `5m`
  - `15m`
  - `30m`
  - `60m`
- 输出标准列：
  - `datetime`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
  - `money`
  - `openinterest`
- 优先做统一标准化层，不要在多个地方重复写字段转换。
- 增加本地缓存，减少重复抓取。
- 处理数据源字段名不一致、时间戳格式不一致、缺字段等问题。
- 不要改 timer 或 finance。

## 任务验证

至少完成以下验证：

- 一个股票分钟数据 smoke test
- 一个 ETF 分钟数据 smoke test
- 确认上层 `get_price` 或 `get_bars` 能消费分钟数据

建议命令：

```bash
python3 -m pytest -q tests
```

如只新增独立测试，可写明具体测试命令。

## 任务成功总结模板

```md
# Task 04 Result

## 修改文件
- ...

## 完成内容
- ...

## 验证命令
```bash
...
```

## 验证结果
- ...

## 已知边界
- ...
```
