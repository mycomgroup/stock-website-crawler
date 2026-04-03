# 任务 10：宏观数据对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“宏观数据”相关接口，重点修复表名兼容、指标列表完整性、统一入口与稳定 schema。

## 负责范围

- `jqdata_akshare_backtrader_utility/finance_data/macro.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 如有必要：
  - `jqdata_akshare_backtrader_utility/finance_data/__init__.py`
- 测试：
  - `tests/test_macro_api.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task10_macro_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 宏观数据接口的严格对齐，请直接实现。

参考文档：

- `doc_JQDatadoc_10289_overview_宏观数据.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_macro_data`
  - `get_macro_series`
  - `get_macro_indicators`
  - `get_macro_indicator`
  - `finance.MACRO_ECONOMIC_DATA`
  - 文档别名 `finance.MAC_ECONOMIC_DATA`
- 现有支持指标至少包括：
  - GDP
  - CPI
  - PPI
  - M2
  - 利率
  - 汇率
- 如果文档中还有当前未覆盖但非常基础的指标，请优先评估能否补到 `get_macro_indicators` 清单中
- 空结果要返回稳定字段，不要返回完全无列 DataFrame

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_macro_api.py
```

建议额外覆盖：

- `MACRO_ECONOMIC_DATA` 与 `MAC_ECONOMIC_DATA` 两个入口一致
- 指标列表字段稳定
- 时间范围过滤不会异常

## 任务成功总结模板

```md
# Task 10 Result

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
