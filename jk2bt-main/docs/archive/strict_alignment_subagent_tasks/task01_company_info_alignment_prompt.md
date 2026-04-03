# 任务 1：公司信息数据对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“上市公司基本信息 / 上市公司状态变动 / 上市信息”相关接口与当前实现，确保模块实现、全局统一入口、命名兼容、稳定 schema 四件事都成立。

## 负责范围

- `jqdata_akshare_backtrader_utility/finance_data/company_info.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 如确有必要，可补充：
  - `jqdata_akshare_backtrader_utility/finance_data/__init__.py`
  - `jqdata_akshare_backtrader_utility/__init__.py`
- 测试：
  - `tests/test_company_info_api.py`
  - 如有必要新增更细的对齐测试

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task01_company_info_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 公司信息相关数据接口的严格对齐，请直接实现，不只做分析。

参考文档：

- `doc_JQDatadoc_10016_overview_上市公司基本信息.md`
- `doc_JQDatadoc_10023_overview_上市公司状态变动.md`
- `doc_JQDatadoc_10025_overview_上市信息.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_company_info`
  - `get_security_status`
  - `get_listing_info`
  - `finance.STK_COMPANY_BASIC_INFO`
  - `finance.STK_STATUS_CHANGE`
- 确保：
  - 模块直接调用可用
  - 全局 `finance.run_query` 可用
  - 空结果也返回稳定列名
  - 常见代码格式都可识别，例如 `600000`、`sh600000`、`600000.XSHG`
- 如果文档里表名、字段名和当前实现不一致，优先补兼容别名，不要直接破坏现有调用
- 不要顺手大改其他 finance 表

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_company_info_api.py
```

建议额外覆盖：

- `finance.run_query(query(finance.STK_COMPANY_BASIC_INFO)...)`
- `finance.run_query(query(finance.STK_STATUS_CHANGE)...)`
- 空股票代码、未来日期、无结果场景仍返回稳定 schema

## 任务成功总结模板

```md
# Task 01 Result

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
