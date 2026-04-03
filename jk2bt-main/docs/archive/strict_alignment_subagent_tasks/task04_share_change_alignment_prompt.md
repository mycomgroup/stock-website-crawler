# 任务 4：股东变动数据对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“股东股份质押 / 股东股份冻结 / 大股东增减持 / 股本变动”相关接口，重点把模块内已有实现完全对齐到全局 `finance` 入口。

## 负责范围

- `jqdata_akshare_backtrader_utility/finance_data/share_change.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 测试：
  - `tests/test_share_change_api.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task04_share_change_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 股东变动类数据接口的严格对齐，请直接实现。

参考文档：

- `doc_JQDatadoc_10013_overview_股东股份质押.md`
- `doc_JQDatadoc_10014_overview_股东股份冻结.md`
- `doc_JQDatadoc_10017_overview_大股东增减持.md`
- `doc_JQDatadoc_10018_overview_上市公司股本变动.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_pledge_info`
  - `get_major_holder_trade`
  - `get_freeze_info`
  - `get_capital_change`
  - `get_topholder_change`
  - `finance.STK_SHARE_PLEDGE`
  - `finance.STK_SHARE_FREEZE`
  - `finance.STK_TOPHOLDER_CHANGE`
  - `finance.STK_CAPITAL_CHANGE`
- 如果模块内已有 `FinanceQuery`，重点检查它与全局 `finance` 入口是否等价
- 空结果必须返回稳定 schema
- 尽量保持现有缓存和数据源策略，不要大改底层抓取逻辑

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_share_change_api.py
```

建议额外覆盖：

- 4 张表都可通过统一入口调用
- 代码格式兼容
- 日期过滤 / limit 不会导致异常

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
