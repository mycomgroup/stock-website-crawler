# 任务 3：JQ 行情 API 兼容层

## 任务目标

统一实现 JQ 风格行情接口，使 `get_price`、`history`、`attribute_history`、`get_bars` 在签名和返回结构上尽量兼容聚宽常见调用。

## 负责范围

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- `jqdata_akshare_backtrader_utility/market_api.py`
- 相关测试文件

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task03_market_api_result.md`

## 给子 Agent 的提示词

你负责统一 JQ 行情 API 兼容层，请直接完成代码和测试。

重点要求：

- 统一以下函数行为：
  - `get_price`
  - `history`
  - `attribute_history`
  - `get_bars`
- 重点兼容参数：
  - `count`
  - `start_date`
  - `end_date`
  - `frequency`
  - `fields`
  - `panel`
  - `df`
  - `fq`
  - `fill_paused`
  - `skip_paused`
- 至少覆盖高频字段：
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
  - `money`
  - `paused`
  - `pre_close`
  - `high_limit`
  - `low_limit`
- 不要只补签名，要保证返回形状也尽量一致。
- 如果底层源数据缺少某字段，可在兼容层推导，但要在结果文档写明推导方式。
- 不要处理 finance、timer、文件 IO。

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_api_compatibility.py
```

如果你新增了专门的行情测试，也请附上。

## 任务成功总结模板

```md
# Task 03 Result

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
