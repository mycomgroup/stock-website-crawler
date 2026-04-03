# 任务 7：资金流接口

## 任务目标

实现 `get_money_flow`，支持现有策略中常见的资金流字段和常见查询方式。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/`
- 与资金流直接相关的兼容层代码
- 对应测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/market_data/`
  - `tests/`
- 任务结果写入：
  - `docs/0330_result/`
  - 建议文件名：`task07_money_flow_result.md`

## 给子 Agent 的提示词

你负责补资金流接口，请实现可直接给策略使用的 `get_money_flow`。

具体要求：

- 支持常见参数：
  - 标的
  - 日期区间
  - `count`
  - `fields`
- 返回 `DataFrame`
- 优先兼容常见字段：
  - `sec_code`
  - `date`
  - `change_pct`
  - `net_amount_main`
  - `net_pct_main`
  - 以及你能稳定支持的主力/超大单/大单/中单/小单字段
- 要处理不同数据源字段名不一致的问题
- 无数据或离线时，优先返回带稳定列名的空表
- 不要把任务扩展到北向资金或龙虎榜

## 任务验证

至少完成以下验证：

- 单标的资金流查询
- 日期区间或 `count` 查询
- 指定字段过滤
- 离线或失败时仍保持稳定 schema

建议命令：

```bash
python3 -m pytest -q tests
```

## 任务成功总结模板

```md
# Task 07 Result

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
