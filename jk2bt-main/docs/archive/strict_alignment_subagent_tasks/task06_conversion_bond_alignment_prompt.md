# 任务 6：可转债数据对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“可转债”相关接口，重点确认可转债基础信息、价格数据、转股信息在模块实现和统一入口里都能按文档表名使用。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/conversion_bond.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 如有必要：
  - `jqdata_akshare_backtrader_utility/market_data/__init__.py`
- 测试：
  - `tests/test_conversion_bond_api.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task06_conversion_bond_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 可转债数据接口的严格对齐，请直接实现。

参考文档：

- `doc_JQDatadoc_10293_overview_可转债.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_conversion_bond_list`
  - `get_conversion_bond_quote`
  - `get_conversion_info`
  - `get_conversion_value`
  - `query_conversion_bond_basic`
  - `query_conversion_bond_price`
  - `finance.STK_CONVERSION_BOND_BASIC`
  - `finance.STK_CONVERSION_BOND_PRICE`
- 确保可转债模块的 `finance` 能力与全局 `finance` 入口一致
- 如果存在旧表名或旧函数名，也请尽量做兼容别名
- 不要大改非可转债资产代码

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_conversion_bond_api.py
```

建议额外覆盖：

- `finance.run_query` 两张表都可走通
- 转股价值 / 溢价率相关字段稳定
- 空或非法代码返回稳定空表而不是报错

## 任务成功总结模板

```md
# Task 06 Result

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
