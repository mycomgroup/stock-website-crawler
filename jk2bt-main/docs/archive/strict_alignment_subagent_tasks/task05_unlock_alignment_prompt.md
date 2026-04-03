# 任务 5：限售解禁数据对齐

## 任务目标

严格对齐 JoinQuant 原始文档中“预计解禁 / 实际解禁 / 限售解禁数据”相关接口，重点解决文档别名、统一入口、稳定 schema 和历史/未来区间查询。

## 负责范围

- `jqdata_akshare_backtrader_utility/finance_data/unlock.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 测试：
  - `tests/test_unlock_api.py`

## 建议写入目录

- 代码写入：
  - `jqdata_akshare_backtrader_utility/`
  - `tests/`
- 任务结果写入：
  - `docs/strict_alignment_results/`
  - 建议文件名：`task05_unlock_alignment_result.md`

## 给子 Agent 的提示词

你负责完成 JoinQuant 限售解禁数据接口的严格对齐，请直接实现。

参考文档：

- `doc_JQDatadoc_10019_overview_上市公司上市公告日期和预计解禁日期.md`
- `doc_JQDatadoc_10020_overview_上市公司受限股份实际解禁的日期.md`
- `doc_JQDatadoc_10021_overview_限售解禁数据.md`
- 本地对照清单：`docs/strict_data_api_comparison.md`

重点要求：

- 核对并修复：
  - `get_unlock_schedule`
  - `get_unlock_pressure`
  - `get_unlock_calendar`
  - `get_upcoming_unlocks`
  - `get_unlock_history`
  - `analyze_unlock_impact`
  - `finance.STK_LOCK_UNLOCK`
  - `finance.STK_LOCK_SHARE`
  - 文档别名 `finance.STK_UNLOCK_DATE`
- 注意文档里的“预计解禁”和“实际解禁”语义是否已经被当前表结构覆盖；如果没完全覆盖，优先补兼容列或说明
- 不能只让函数能跑，要保证 query 入口行为一致

## 任务验证

至少完成以下验证：

```bash
python3 -m pytest -q tests/test_unlock_api.py
```

建议额外覆盖：

- `STK_LOCK_UNLOCK` / `STK_UNLOCK_DATE` 别名一致
- 日期范围查询稳定
- 空结果仍返回固定字段

## 任务成功总结模板

```md
# Task 05 Result

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
