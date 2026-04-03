# 任务 3：分红送股与公司行为对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“公司行为 / 分红送股 / 除权除息 / 配股 / 复权因子”相关接口，重点解决表名别名、字段稳定性、统一入口和返回格式兼容。

## 负责范围

- `jqdata_akshare_backtrader_utility/finance_data/dividend.py`
- `jqdata_akshare_backtrader_utility/finance_data/__init__.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 测试：
  - `tests/test_dividend_api.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task03_dividend_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 分红送股与公司行为接口的严格对齐，请直接实现。

参考文档：

- `doc_JQDatadoc_10010_overview_公司行为.md`
- `doc_JQDatadoc_10022_overview_上市公司分红送股（除权除息）数据.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_dividend_info`
  - `get_rights_issue`
  - `get_adjust_factor`
  - `get_next_dividend`
  - `finance.STK_XR_XD`
  - 文档别名 `finance.STK_DIVIDEND_RIGHT`
- 统一：
  - 除权除息日期字段
  - 分红 / 送股 / 转增 / 配股字段名
  - 无数据时的空表 schema
- 若文档名和当前实现名不一致，优先补兼容别名，不要删现有接口
- 不要只补函数存在性，要保证全局入口也可用

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_dividend_api.py
```

建议额外覆盖：

- `STK_XR_XD` 和 `STK_DIVIDEND_RIGHT` 两个入口返回一致
- `get_rights_issue`、`get_next_dividend` 已通过包级导出调用
- 复权因子字段稳定

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
