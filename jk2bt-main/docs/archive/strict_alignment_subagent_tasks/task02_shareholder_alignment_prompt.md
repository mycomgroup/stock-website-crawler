# 任务 2：股东数据对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“前10大股东 / 十大流通股东 / 股东户数”相关接口，确保接口签名、统一入口、返回结构、日期筛选能力与文档预期一致。

## 负责范围

- `jqdata_akshare_backtrader_utility/finance_data/shareholder.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 测试：
  - `tests/test_shareholder_api.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task02_shareholder_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 股东数据接口的严格对齐，请直接实现和补测试。

参考文档：

- `doc_JQDatadoc_10011_overview_上市公司前10大股东.md`
- `doc_JQDatadoc_10012_overview_十大流通股东.md`
- `doc_JQDatadoc_10015_overview_股东户数.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_top10_shareholders`
  - `get_top10_float_shareholders`
  - `get_shareholder_count`
  - `finance.STK_SHAREHOLDER_TOP10`
  - `finance.STK_SHAREHOLDER_FLOAT_TOP10`
  - `finance.STK_SHAREHOLDER_NUM`
- 统一：
  - 日期字段命名
  - 报告期 / 公告期过滤
  - 空结果 schema
- 保持已有缓存和稳健模式，不要重做整套实现
- 如果模块功能已存在但全局入口不一致，优先补统一入口和兼容层

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_shareholder_api.py
```

建议额外覆盖：

- query builder 对 3 张表都可跑
- 多股票批量查询
- 报告期过滤不丢列

## 任务成功总结模板

```md
# Task 02 Result

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
