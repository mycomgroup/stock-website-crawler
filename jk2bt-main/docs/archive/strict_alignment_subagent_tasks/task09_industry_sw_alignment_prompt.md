# 任务 9：申万行业数据对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“申万行业 / 行业概念及成分股”相关接口，重点修复命名不一致和行业成分股统一入口问题。

## 负责范围

- `jqdata_akshare_backtrader_utility/market_data/industry_sw.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 如有必要：
  - `jqdata_akshare_backtrader_utility/market_data/__init__.py`
- 测试：
  - `tests/test_industry_sw_api.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task09_industry_sw_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 申万行业接口的严格对齐，请直接实现。

参考文档：

- `doc_JQDatadoc_10282_overview_申万行业.md`
- `doc_JQDatadoc_10283_overview_行业概念及成分股.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_stock_industry`
  - `get_industry_stocks`
  - `get_industry_category`
  - `finance.STK_INDUSTRY_SW`
  - 文档别名 `finance.STK_SW_INDUSTRY`
  - 文档接口 `finance.STK_SW_INDUSTRY_STOCK`
- 如果已有模块函数名与文档表名不一致，优先加兼容层，不要删原名
- 注意一级/二级/三级行业字段结构的一致性
- 行业成分股返回结构要稳定，便于策略直接消费

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_industry_sw_api.py
```

建议额外覆盖：

- 单股票行业归属查询
- 行业成分股统一入口查询
- 文档别名与现有表名都可用

## 任务成功总结模板

```md
# Task 09 Result

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
